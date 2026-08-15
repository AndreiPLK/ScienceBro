"""Extract the sign-carrying bracket of a_{n,2n-2j} as a POLYNOMIAL in (lam, D).

Generalized from t2n6_bracket.py (j=3). Pass J via env TJ_J (default 4 -> l=2n-8).

Method (the one that worked for T_n): build Q(x) symbolically in lam at level n,
square it, project onto the Gegenbauer mode l = 2n-6 with symbolic D using
polynomial Pochhammer ratios (no gamma soup), strip manifestly positive factors,
factor the remainder. Output: results/T2n6_brackets.json with the bracket per n
and its factorization, plus sanity sign-checks against the exact rational
evaluator at spot points.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import gegen_coeffs as gegen_exact  # noqa: E402
from grav_full_body import mono_int  # noqa: E402
from hunt_2n8 import a_l  # noqa: E402  (exact evaluator, any l)

RES = Path(__file__).resolve().parents[1] / "results"
lam, D = sp.symbols("lam D", positive=True)


def q_poly(n: int):
    """Coefficients of Q(x) = prod_k [((n+lam-1)x + (2k-n))/2], symbolic lam."""
    x = sp.symbols("x")
    Q = sp.expand(sp.prod(((n + lam - 1) * x + (2 * k - n)) / 2
                          for k in range(1, n)))
    return sp.Poly(Q, x).all_coeffs()[::-1]  # ascending


def gegen_sym(l: int):
    """Gegenbauer C_l^{(D-3)/2} coefficients (ascending in x), symbolic D."""
    a = (D - 3) / 2
    p0, p1 = [sp.Integer(1)], [sp.Integer(0), 2 * a]
    if l == 0:
        return p0
    if l == 1:
        return p1
    for m in range(2, l + 1):
        xp = [sp.Integer(0)] + p1
        new = [sp.expand(2 * (m - 1 + a) * c / m) for c in xp]
        for i, c in enumerate(p0):
            new[i] = sp.expand(new[i] - (m - 2 + 2 * a) * c / m)
        p0, p1 = p1, new
    return p1


def weight_ratio(k: int):
    """I_k / I_0 where I_k = int_{-1}^1 x^k (1-x^2)^{(D-4)/2} dx, as a RATIONAL
    function of D with no gammas: I_k/I_0 = (k-1)!! / prod_{j=1..k/2} (D-3+2j).
    """
    if k % 2:
        return sp.Integer(0)
    num = sp.Integer(1)
    for m in range(1, k, 2):
        num *= m                     # (k-1)!!
    den = sp.Integer(1)
    for j in range(1, k // 2 + 1):
        den *= (D - 3 + 2 * j)
    return sp.Rational(1) * num / den


import os
J = int(os.environ.get("TJ_J", "4"))


def bracket_for(n: int):
    l = 2 * n - 2 * J
    q = q_poly(n)                       # ascending, deg n-1
    deg = len(q) - 1
    # Q^2 ascending coefficients
    P = [sp.Integer(0)] * (2 * deg + 1)
    for i, a_ in enumerate(q):
        for j, b_ in enumerate(q):
            P[i + j] = sp.expand(P[i + j] + a_ * b_)
    cl = gegen_sym(l)
    total = sp.Integer(0)
    for i, ci in enumerate(cl):
        if ci == 0:
            continue
        for k2, ck in enumerate(P):
            if ck == 0:
                continue
            k = i + k2
            if k % 2:
                continue
            total = total + ci * ck * weight_ratio(k)
    total = sp.cancel(sp.together(sp.expand(total)))
    num, den = sp.fraction(total)
    return sp.factor(num), sp.factor(den)


def main() -> int:
    t0 = time.time()
    out = {}
    for n in range(J + 1, J + 7):
        fac, den = bracket_for(n)
        out[str(n)] = {"numerator_factored": str(fac),
                       "denominator_factored": str(den)}
        print(f"n={n} done ({time.time()-t0:.0f}s)", flush=True)
        # spot sign-check vs exact evaluator at 3 points
        import random  # noqa: F401  (not used; deterministic points below)
        for (lv, Dv) in [(F(1), 26), (F(2), 30), (F(1, 2), 14)]:
            exact = a_l(n, 2 * n - 2 * J, lv, Dv)
            sym = fac.subs({lam: sp.Rational(lv.numerator, lv.denominator),
                            D: Dv})
            s_exact = (exact > 0) - (exact < 0)
            s_sym = int(sp.sign(sym))
            # denominator/positive-factor sign must be accounted: compare only
            # whether the two agree up to a FIXED sign per n
            out[str(n)].setdefault("spot", []).append(
                {"lam": str(lv), "D": Dv, "sign_exact": s_exact,
                 "sign_bracket": s_sym})
            print(f"  spot lam={lv} D={Dv}: exact {s_exact}, bracket {s_sym}",
                  flush=True)
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out["_meta"] = {"command": f"python lab/tj_bracket.py (TJ_J={J})", "git": git,
                    "runtime_s": round(time.time() - t0, 1)}
    (RES / f"T2n{2*J}_brackets.json").write_text(json.dumps(out, indent=1),
                                            encoding="utf-8")
    print(f"written T2n{2*J}_brackets.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
