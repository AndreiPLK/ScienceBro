"""STEP 2, the opening: n can be carried SYMBOLICALLY after all.

The obstacle looked structural: the kernel F_n(y) has a number of factors
that grows with n, so it is not a polynomial in n, and the operator weight
Q_n(t) = prod_{i=j}^{n-1}(i-t) grows factorially. Both objections dissolve
once the sum is written in the t-basis at FIXED j, because then only
t = 0..j-1 ever appears:

FACT A. For fixed t and fixed PARITY of n, E_2t(n) is a POLYNOMIAL in n.
  Reason: E_2t is the t-th elementary symmetric function of the squares
  {a^2 : a in S_n}, and for fixed t it is a fixed-length combination of
  power sums of an arithmetic progression, each of which is a polynomial in
  the number of terms. Parity enters only through whether S_n contains an
  odd or even ladder. Verified below by fitting on the first points and
  PREDICTING the remaining ones (never by fitting all of them).

FACT B. The factorially growing weight is only an overall constant:
        Q_n(t) / Q_n(0) = prod_{i=1}^{t} (j - i)/(n - i) = M1_t ,
  a RATIONAL function of n of degree t, and Q_n(0) > 0 divides out of any
  sign question. Likewise M2_t is rational in n, and s = lam + n - 1 is
  linear. So after clearing prod_{i=1}^{j-1}(n - i) and the M2 denominators
  UNIFORMLY, the whole bracket is a polynomial in (n, lam, D).

Consequence: at fixed j and fixed parity, n joins lam as a symbolic
variable, and the Polya certificate can in principle cover ALL n at once,
leaving j as the single remaining unbounded index.

This module verifies Facts A and B exactly. It does NOT yet build the
three-variable certificate -- that is the next step, and it must carry the
uniform-clearing discipline (the far-below port bug) into three variables.

Run: python lab/keystone_npoly.py -> results/keystone_npoly.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def interpolate(pts: list[tuple[Fraction, Fraction]]) -> list[Fraction]:
    """Newton interpolation, ascending coefficients."""
    xs = [Fraction(x) for x, _ in pts]
    ys = [Fraction(y) for _, y in pts]
    dd = [ys[:]]
    for k in range(1, len(xs)):
        prev = dd[-1]
        dd.append([(prev[i + 1] - prev[i]) / (xs[i + k] - xs[i]) for i in range(len(prev) - 1)])
    poly: list[Fraction] = []
    basis = [Fraction(1)]
    for k in range(len(xs)):
        c = dd[k][0]
        while len(poly) < len(basis):
            poly.append(Fraction(0))
        for i, b in enumerate(basis):
            poly[i] += c * b
        nb = [Fraction(0)] * (len(basis) + 1)
        for i, b in enumerate(basis):
            nb[i + 1] += b
            nb[i] -= b * xs[k]
        basis = nb
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def peval(poly: list[Fraction], x: Fraction) -> Fraction:
    v = Fraction(0)
    for c in reversed(poly):
        v = v * x + c
    return v


def main() -> int:
    t0 = time.time()
    fact_a = []
    for t in range(1, 9):
        for parity, label in ((0, "even"), (1, "odd")):
            fit_k = 3 * t + 4  # generous fitting budget
            # E_2t exists only once the level has at least t spectral roots
            start = 2 * t + 4
            start += (start % 2) ^ parity  # match the requested parity
            ns = [n for n in range(start, start + 2 * (fit_k + 8), 2)]
            pts = [(Fraction(n), Fraction(e_doubled_int(n)[t])) for n in ns]
            pol = interpolate(pts[:fit_k])
            held_out = pts[fit_k:]
            bad = [str(n) for n, y in held_out if peval(pol, n) != y]
            fact_a.append(
                {
                    "E_2t": 2 * t,
                    "parity": label,
                    "fitted_on": fit_k,
                    "degree": len(pol) - 1,
                    "held_out_points": len(held_out),
                    "predicted_all_held_out": not bad,
                    "failures": bad[:5],
                }
            )

    # FACT B: Q_n(t)/Q_n(0) == prod_{i=1}^t (j-i)/(n-i), exactly
    fact_b_checks, fact_b_bad = 0, []
    for j in range(2, 14):
        for n in range(max(4, j + 1), j + 30, 3):
            q0 = Fraction(1)
            for i in range(j, n):
                q0 *= i
            for t in range(j):
                qt = Fraction(1)
                for i in range(j, n):
                    qt *= i - t
                m1 = Fraction(1)
                for i in range(1, t + 1):
                    m1 *= Fraction(j - i, n - i)
                fact_b_checks += 1
                if qt / q0 != m1:
                    fact_b_bad.append({"j": j, "n": n, "t": t})

    a_ok = all(r["predicted_all_held_out"] for r in fact_a)
    out = {
        "purpose": "show that n can be carried symbolically at fixed j,"
        " which is what step 2 of the keystone needs",
        "fact_A": {
            "statement": "for fixed t and fixed parity of n, E_2t(n) is a polynomial in n",
            "method": "fit on the first points, PREDICT the rest",
            "rows": fact_a,
            "verified": a_ok,
        },
        "fact_B": {
            "statement": "Q_n(t)/Q_n(0) = prod_{i=1..t} (j-i)/(n-i)"
            " -- the factorial growth is an overall"
            " positive constant, the t-dependence is"
            " rational in n of degree t",
            "checks": fact_b_checks,
            "failures": fact_b_bad,
            "verified": not fact_b_bad,
        },
        "consequence": "at fixed j and parity, the bracket is a polynomial"
        " in (n, lam, D) after uniform clearing, so the"
        " Polya certificate can cover ALL n at once and j"
        " becomes the single remaining unbounded index",
        "not_done_yet": "the three-variable certificate itself; it must"
        " carry the uniform-clearing discipline into"
        " (w, v, n) or the same sign bug as the far-below"
        " port will reappear",
        "command": "python lab/keystone_npoly.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_npoly.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(
        f"Fact A (E_2t polynomial in n): "
        f"{'VERIFIED' if a_ok else 'FAILED'} "
        f"({len(fact_a)} cases, each predicting held-out points)",
        flush=True,
    )
    print(
        f"Fact B (weight is a constant times a rational function): "
        f"{fact_b_checks} checks, {len(fact_b_bad)} failures",
        flush=True,
    )
    return 0 if (a_ok and not fact_b_bad) else 1


if __name__ == "__main__":
    sys.exit(main())
