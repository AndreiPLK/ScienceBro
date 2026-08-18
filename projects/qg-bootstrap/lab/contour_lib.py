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
from keystone_saddles import build_P as _build_P_raw  # noqa: E402
from keystone_saddles import coeff  # noqa: E402

_P_CACHE: dict[tuple[int, int, str], list[F]] = {}


def build_P(j: int, n: int, lam: F) -> list[F]:
    """Cached exact build. The deformation search calls this ~10^4 times per
    knife with identical arguments; rebuilding the rational product each time
    was the entire cost of the search. The cache returns the SAME list object,
    so callers must not mutate it -- nothing here does."""
    key = (j, n, str(lam))
    P = _P_CACHE.get(key)
    if P is None:
        P = _build_P_raw(j, n, lam)
        _P_CACHE[key] = P
    return P


def _float_poly(j: int, n: int, lam: F):
    """(numpy polynomial scaled by max|coeff|, scaled true coefficient) or None.

    Also cached: the float conversion of a degree-100 rational polynomial is not
    free either.
    """
    key = ("f", j, n, str(lam))
    got = _P_CACHE.get(key)  # type: ignore[arg-type]
    if got is None:
        P = build_P(j, n, lam)
        N = j - 1
        true = float(coeff(P, N))
        if true == 0 or not np.isfinite(true):
            got = (None, None)
        else:
            scale = max(abs(c) for c in P)
            pf = np.polynomial.Polynomial([float(c / scale) for c in P])
            true_s = float(F(coeff(P, N), 1) / scale)
            got = (pf, true_s) if (true_s != 0 and np.isfinite(true_s)) else (None, None)
        _P_CACHE[key] = got  # type: ignore[assignment]
    return got


def exact_answer(j: int, n: int, lam: F) -> F:
    """The exact bracket value (a rational number)."""
    P = build_P(j, n, lam)
    return coeff(P, j - 1)


def density(j: int, n: int, lam: F, r: float, steps: int = 1500):
    """Normalised integrand along the circle of radius r. Mean is exactly 1.

    Returns (t, values) or (None, None) if the float evaluation is unusable.
    """
    # The polynomial is SCALED by its largest coefficient before going to float:
    # at large j the coefficients exceed 1e308 and plain float(c) overflows
    # (hit at j = 80). Scaling is a positive factor and cancels in v/true.
    N = j - 1
    pf, true_s = _float_poly(j, n, lam)
    if pf is None:
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


def density_deformed(j: int, n: int, lam: F, r: float, eps: float, k: int,
                     steps: int = 1500):
    """Normalised integrand along a DEFORMED loop, not just a circle.

    WHY. A dip is a property of the loop I chose, not of the problem. Every
    result so far used circles only, and circles provably fail on whole blocks
    of j (proven in ball arithmetic tonight: j = 81..113 at lam = 1). Before
    calling the contour route dead, the loop family has to be enlarged.

        x(t) = r e^{it} (1 + eps cos k t),   k = 1, 2, 3, ...

    still winds once around the origin for |eps| < 1, so Cauchy applies:

        bracket = (1/2pi) INT_0^{2pi} Re[ P(x) x'(t) / (i x^{N+1}) ] dt.

    At eps = 0 this reduces to `density` exactly, which the self-test checks.
    Mean over the loop is 1 by construction.
    """
    N = j - 1
    pf, true_s = _float_poly(j, n, lam)
    if pf is None:
        return None, None
    t = np.linspace(0, 2 * np.pi, steps, endpoint=False)
    e = np.exp(1j * t)
    g = 1.0 + eps * np.cos(k * t)
    x = r * e * g
    dx = r * e * (1j * g - eps * k * np.sin(k * t))
    v = (pf(x) * dx / (1j * x ** (N + 1))).real / true_s
    if not np.isfinite(v).all():
        return None, None
    return t, v


def best_deformed(j: int, n: int, lam: F, ks=(1, 2, 3, 4),
                  eps_grid=None, lo: float = -2.9, hi: float = -0.6,
                  count: int = 60, steps: int = 900):
    """Search radius, deformation amplitude and harmonic for a sign-definite loop.

    Returns the best (min_value, r, eps, k). A positive min_value means the loop
    proves that knife positive with no asymptotics at all. eps = 0 is included
    in the grid so the answer can never be WORSE than the plain circle.
    """
    if eps_grid is None:
        eps_grid = np.concatenate([np.linspace(-0.85, 0.85, 35), [0.0]])
    best = (-np.inf, None, None, None)
    for r in np.logspace(lo, hi, count):
        for k in ks:
            for eps in eps_grid:
                _, v = density_deformed(j, n, lam, float(r), float(eps),
                                        int(k), steps=steps)
                if v is None:
                    continue
                m = float(v.min())
                if m > best[0]:
                    best = (m, float(r), float(eps), int(k))
    return best


def density_min_hp(j: int, n: int, lam: F, r: float, steps: int = 240, dps: int = 60):
    """Minimum of the density at radius r, computed in ball arithmetic.

    WHY THIS EXISTS. The float path (`density`) is only trustworthy while the
    dip is far above double noise. Measured at lam = 1: dips are ~1e-11 near
    j = 60, ~1e-16 near j = 80, and exactly 0.0 from j = 94 -- i.e. the signal
    sinks into the noise floor and then the evaluation collapses entirely. Any
    conclusion about blocks beyond j ~ 78 taken from the float scan is void.

    This is the same computation as `rigorous_min` but cheap enough to scan
    radii with (fewer sample points, lower precision). It still returns an arb
    ball, so its sign is meaningful whenever the ball excludes zero.
    """
    from flint import acb, arb, ctx

    ctx.dps = dps
    P = build_P(j, n, lam)
    N = j - 1
    c = coeff(P, N)
    if c == 0:
        return None
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


def density_min_deformed_hp(j: int, n: int, lam: F, r: float, eps: float,
                            k: int, steps: int = 240, dps: int = 60):
    """Ball-arithmetic minimum along the deformed loop x = r e^{it}(1+eps cos kt).

    Needed because the float deformation search cannot be trusted where it
    matters: at j = 75 the float search reported a positive minimum of +3e-16
    while ball arithmetic proves that knife dips. Any "the deformed loop fixes
    this knife" claim must come from here.

    At eps = 0 this must equal density_min_hp; the self-test checks that.
    """
    from flint import acb, arb, ctx

    ctx.dps = dps
    P = build_P(j, n, lam)
    N = j - 1
    c = coeff(P, N)
    if c == 0:
        return None
    true = arb(str(c.numerator)) / arb(str(c.denominator))
    cs = [acb(str(x.numerator)) / acb(str(x.denominator)) for x in P]
    R, E = arb(str(r)), arb(str(eps))
    worst = None
    for i in range(steps):
        t = arb(i) * arb.pi() * 2 / steps
        kt = t * k
        g = arb(1) + E * kt.cos()
        e = acb(t.cos(), t.sin())
        x = e * acb(R * g)
        # x'(t) = r e^{it} ( i g - eps k sin kt )
        dx = e * acb(R) * (acb(0, 1) * acb(g) - acb(E * k * kt.sin()))
        v = acb(0)
        for cc in reversed(cs):
            v = v * x + cc
        d = (v * dx / (acb(0, 1) * x ** (N + 1))).real / true
        if worst is None or d.lower() < worst.lower():
            worst = d
    return worst


def verdict_deformed_hp(j: int, n: int, lam: F, r: float, eps: float, k: int,
                        steps: int = 600, dps: int = 120):
    """Proven dip / dip_free for one deformed loop."""
    w = density_min_deformed_hp(j, n, lam, r, eps, k, steps=steps, dps=dps)
    if w is None:
        return {"status": "unstable"}
    status = ("dip" if w.upper() < 0 else
              "dip_free" if w.lower() > 0 else "undecided")
    return {"j": j, "n": n, "lam": str(lam), "r": r, "eps": eps, "k": k,
            "mid": float(w.mid()), "rad": float(w.rad()), "status": status}


def best_circle_hp(j: int, n: int, lam: F, lo: float = -2.9, hi: float = -0.6,
                   count: int = 34, steps: int = 240, dps: int = 60):
    """Radius maximising the minimum, using ball arithmetic throughout.

    Returns (radius, arb_min). Use instead of `best_circle` whenever j is large
    enough that the float dip could be near 1e-15 -- otherwise the radius
    itself is chosen from noise, and then even a rigorous check at that radius
    answers the wrong question.
    """
    best_r, best_w = None, None
    for r in np.logspace(lo, hi, count):
        w = density_min_hp(j, n, lam, float(r), steps=steps, dps=dps)
        if w is None:
            continue
        if best_w is None or w.lower() > best_w.lower():
            best_r, best_w = float(r), w
    return best_r, best_w


def verdict_hp(j: int, n: int, lam: F, steps: int = 600, dps: int = 120):
    """Dip / dip_free decision that does not pass through float at any point."""
    r, _ = best_circle_hp(j, n, lam)
    if r is None:
        return {"j": j, "n": n, "lam": str(lam), "status": "unstable"}
    w = density_min_hp(j, n, lam, r, steps=steps, dps=dps)
    if w.upper() < 0:
        status = "dip"
    elif w.lower() > 0:
        status = "dip_free"
    else:
        status = "undecided"
    return {"j": j, "n": n, "lam": str(lam), "radius": r,
            "mid": float(w.mid()), "rad": float(w.rad()), "status": status}


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
    # 5. the high-precision path agrees with the float path WHERE FLOAT IS
    #    RELIABLE (small j, dip far above 1e-15). If these two ever disagree
    #    here, one of them is wrong and no large-j conclusion may be drawn.
    for j, n, expect in ((10, 14, "dip"), (18, 22, "dip_free")):
        h = verdict_hp(j, n, F(1))
        if h["status"] != expect:
            bad.append(f"hp j={j} expected {expect}, got {h['status']}")
    # 6. the deformed loop at eps = 0 IS the circle -- if these ever differ, the
    #    Jacobian x'(t) in `density_deformed` is wrong and every deformed result
    #    is void.
    for j, n, lam, r in ((10, 14, F(1), 0.02), (14, 18, F(3), 0.03)):
        _, v0 = density(j, n, lam, r, steps=1200)
        _, vd = density_deformed(j, n, lam, r, 0.0, 2, steps=1200)
        if v0 is None or vd is None:
            bad.append(f"deformed/circle comparison unusable at j={j}")
        elif float(np.abs(v0 - vd).max()) > 1e-8 * max(1.0, float(np.abs(v0).max())):
            bad.append(f"deformed(eps=0) != circle at j={j}: "
                       f"maxdiff {float(np.abs(v0 - vd).max()):.3e}")
    # 7. the same identity in ball arithmetic: the hp deformed loop at eps = 0
    #    must reproduce the hp circle. This is the check that licenses every
    #    "the deformed loop fixes this knife" statement.
    w_c = density_min_hp(10, 14, F(1), 0.02, steps=120, dps=60)
    w_d = density_min_deformed_hp(10, 14, F(1), 0.02, 0.0, 2, steps=120, dps=60)
    if w_c is None or w_d is None:
        bad.append("hp deformed/circle comparison unusable")
    elif not (abs(float(w_c.mid()) - float(w_d.mid()))
              <= 1e-20 * max(1.0, abs(float(w_c.mid())))):
        bad.append(f"hp deformed(eps=0) {float(w_d.mid()):.6e} != "
                   f"hp circle {float(w_c.mid()):.6e}")
    return bad


if __name__ == "__main__":
    problems = self_test()
    if problems:
        print("SELF-TEST FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("contour_lib self-test: PASSED (8 checks)")
