"""CONTOUR LIBRARY: one vetted implementation, so ad-hoc scripts stop lying.

Written after three bugs in one hour, all of them from re-writing the same
computation inline each time:
  1. two different densities compared as if they were the same (one carried the
     contour element dx, the other did not);
  2. `if r is False` against a numpy.bool_, which is never True in Python -- a
     whole threshold table came out empty and looked like a solved theorem;
  3. a hand-typed radius substituted into the rigorous check instead of the
     optimal one, producing a "dip" twelve orders of magnitude too large.

Nothing here is new mathematics. It exists so that every future check calls the
SAME verified code, with a self-test that runs on import demand.

THE OBJECT. For knife j at level n with deformation lam, the verdict is

    bracket = [x^{j-1}] P(x),   P = G2 * Psi_rev  (build_P in keystone_saddles)

and by Cauchy, for any radius r > 0,

    bracket = (1/2pi) INT_0^{2pi} Re[ P(r e^{it}) e^{-i (j-1) t} ] / r^{j-1} dt.

`density` returns that integrand, normalised by the exact answer, so a value
below zero is a genuine dip and the mean over the loop is exactly 1.

Run: python lab/contour_lib.py   (executes the self-test)
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_saddles import build_P, coeff  # noqa: E402


def exact_answer(j: int, n: int, lam: F) -> F:
    """The exact bracket value (a rational number)."""
    P = build_P(j, n, lam)
    return coeff(P, j - 1)


def density(j: int, n: int, lam: F, r: float, steps: int = 1500):
    """Normalised integrand along the circle of radius r. Mean is exactly 1.

    Returns (t, values) or (None, None) if the float evaluation is unusable.
    """
    P = build_P(j, n, lam)
    N = j - 1
    true = float(coeff(P, N))
    if true == 0 or not np.isfinite(true):
        return None, None
    # SCALE the polynomial by its largest coefficient before going to float:
    # at large j the coefficients exceed 1e308 and plain float(c) overflows
    # (hit at j = 80). Scaling is a positive factor and cancels in v/true.
    scale = max(abs(c) for c in P)
    pf = np.polynomial.Polynomial([float(c / scale) for c in P])
    true_s = float(F(coeff(P, N), 1) / scale)
    if true_s == 0 or not np.isfinite(true_s):
        return None, None
    t = np.linspace(0, 2 * np.pi, steps, endpoint=False)
    v = (pf(r * np.exp(1j * t)) * np.exp(-1j * N * t) / r**N).real / true_s
    if not np.isfinite(v).all():
        return None, None
    return t, v


def best_circle(j: int, n: int, lam: F, lo: float = -2.9, hi: float = -0.6, count: int = 140):
    """Radius maximising the minimum of the density.

    Returns (radius, min_value) with PLAIN FLOATS -- never numpy scalars, which
    is what broke a comparison earlier today.
    """
    best_r, best_m = None, -np.inf
    for r in np.logspace(lo, hi, count):
        _, v = density(j, n, lam, float(r))
        if v is None:
            continue
        m = float(v.min())
        if m > best_m:
            best_r, best_m = float(r), m
    if best_r is None:
        return None, None
    return best_r, best_m


def rigorous_min(j: int, n: int, lam: F, r: float, steps: int = 1200, dps: int = 200):
    """Ball-arithmetic minimum of the density at radius r.

    Returns an arb interval PROVEN to contain the true minimum over the sampled
    points, so `.upper() < 0` means a dip for sure and `.lower() > 0` means
    dip-free for sure at those points.
    """
    from flint import acb, arb, ctx

    ctx.dps = dps
    P = build_P(j, n, lam)
    N = j - 1
    c = coeff(P, N)
    true = arb(str(c.numerator)) / arb(str(c.denominator))
    cs = [acb(str(x.numerator)) / acb(str(x.denominator)) for x in P]
    R = arb(str(r))
    worst = None
    for i in range(steps):
        t = arb(i) * arb.pi() * 2 / steps
        x = acb(R * t.cos(), R * t.sin())
        v = acb(0)
        for cc in reversed(cs):
            v = v * x + cc
        d = (v * (acb(0, -1) * N * acb(t)).exp() / acb(R) ** N).real / true
        if worst is None or d.lower() < worst.lower():
            worst = d
    return worst


def verdict(j: int, n: int, lam: F, steps: int = 1200):
    """Full pipeline: find the best circle, then judge it rigorously.

    This is the ONLY function callers should use for a dip/no-dip decision --
    it cannot be handed a wrong radius, which was bug 3.
    """
    r, m_float = best_circle(j, n, lam)
    if r is None:
        return {"j": j, "n": n, "lam": str(lam), "status": "unstable"}
    w = rigorous_min(j, n, lam, r, steps=steps)
    if w.upper() < 0:
        status = "dip"
    elif w.lower() > 0:
        status = "dip_free"
    else:
        status = "undecided"
    return {
        "j": j,
        "n": n,
        "lam": str(lam),
        "radius": r,
        "float_min": m_float,
        "rigorous_mid": float(w.mid()),
        "status": status,
    }


def self_test() -> list[str]:
    """Checks that would have caught all three bugs."""
    bad = []
    # 1. the density integrates to exactly 1 (catches a wrong normalisation)
    for j, n, lam, r in ((6, 10, F(1), 0.033), (8, 12, F(3), 0.03)):
        _, v = density(j, n, lam, r, steps=20000)
        if v is None or abs(v.mean() - 1.0) > 1e-6:
            bad.append(f"density mean != 1 at j={j} n={n}: {None if v is None else v.mean()}")
    # 2. best_circle returns plain floats (catches the numpy.bool / numpy scalar
    #    class of bug)
    r, m = best_circle(6, 10, F(1))
    if not (type(r) is float and type(m) is float):
        bad.append(f"best_circle returned {type(r)}, {type(m)}")
    # 3. rigorous and float minima agree AT THE SAME radius
    w = rigorous_min(6, 10, F(1), r)
    if not (abs(float(w.mid()) - m) <= 1e-6 * max(1.0, abs(m))):
        bad.append(f"rigorous {float(w.mid()):.3e} vs float {m:.3e} disagree")
    # 4. known result: j=10, n=14, lam=1 has a dip; j=18, n=22, lam=1 does not
    v1 = verdict(10, 14, F(1))
    v2 = verdict(18, 22, F(1))
    if v1["status"] != "dip":
        bad.append(f"j=10 expected dip, got {v1['status']}")
    if v2["status"] != "dip_free":
        bad.append(f"j=18 expected dip_free, got {v2['status']}")
    return bad


if __name__ == "__main__":
    problems = self_test()
    if problems:
        print("SELF-TEST FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("contour_lib self-test: PASSED (4 checks)")
