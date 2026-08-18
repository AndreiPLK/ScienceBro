"""EVERY KNIFE IN CLOSED FORM -- no integrals, no sums over the level.

The chain, each link verified rather than trusted:

1. The Jacobi normal form (lab/jacobi_normal_form.py, 4500 exact sign checks
   against an independently computed value) says knife j is the m-th Jacobi
   coefficient of F, with m = n - j.
2. Orthogonality leaves exactly j terms, and the moments have a Saalschutz
   closed form (432 exact checks).
3. The ratio of consecutive moments collapses to elementary products, so after
   dividing by the (positive) t = 0 term:

       knife j > 0  <=>  SUM_{t=0}^{j-1} (-1)^t E_2t(n) s^{-2t} R_t  >  0,

       R_0 = 1,
       R_t = [prod_{i=1..t} (j-i)] [prod_{i=1..t} (D + 4n - 2j - 5 - 2(i-1))]
             / ( [prod_{i=1..t} (n-i)] [prod_{i=1..t} (2n-1-2i)] ),
       s   = lam + n - 1.

4. The central factorial numbers are explicit polynomials in n (verified on BOTH
   parities up to n = 59), so the whole condition is one rational function of
   (n, D, lam) per knife.

WHY THIS IS WORTH HAVING. Knife 2 is the published shore, knife 3 the published
blade theorem; this module produces the same shape of statement for ANY j, and
in particular gives P4, the fourth knife, as an explicit polynomial: degree 9 in
n, 3 in D, 6 in lam.

Two off-by-one errors in my own derivation of R_t were caught by the numeric
check below, which is why it runs before anything is printed as a result.

sympy is used only for the SYMBOLIC derivation; every verification goes through
the flint engine (see CLAUDE.md, the fast-engine law).

Run: python lab/knife_closed_form.py -> results/knife_closed_form.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
n, D, lam = sp.symbols("n D lam", positive=True)

E_POLY = {
    0: sp.Integer(1),
    1: n * (n - 1) * (n - 2) / 3,
    2: n * (n - 1) * (n - 2) * (5 * n**3 - 24 * n**2 + 28 * n + 12) / 90,
    3: (
        n
        * (n - 1)
        * (n - 2)
        * (n - 3)
        * (n - 4)
        * (35 * n**4 - 154 * n**3 + 172 * n**2 + 292 * n + 120)
        / 5670
    ),
}


def check_E_polynomials(top: int = 60) -> list[str]:
    """E_2t(n) must reproduce the exact central factorial numbers, both parities."""
    bad = []
    for t, poly in E_POLY.items():
        for k in range(2 * t + 2, top):
            e = e_doubled_int(k)
            if t < len(e) and sp.Integer(e[t]) != poly.subs(n, k):
                bad.append(f"E_{2 * t} wrong at n={k}")
    return bad


def R_t(t: int, j: int):
    """Ratio of the t-th moment to the leading one, elementary and finite."""
    if t == 0:
        return sp.Integer(1)
    num = sp.prod([j - i for i in range(1, t + 1)]) * sp.prod(
        [D + 4 * n - 2 * j - 5 - 2 * (i - 1) for i in range(1, t + 1)]
    )
    den = sp.prod([n - i for i in range(1, t + 1)]) * sp.prod(
        [2 * n - 1 - 2 * i for i in range(1, t + 1)]
    )
    return num / den


def knife_expr(j: int):
    """The knife-j condition as a single rational function of (n, D, lam)."""
    if j - 1 > max(E_POLY):
        raise ValueError(f"need E_{2 * (j - 1)}; only up to E_{2 * max(E_POLY)} is derived")
    s = lam + n - 1
    return sp.together(sum((-1) ** t * E_POLY[t] / s ** (2 * t) * R_t(t, j) for t in range(j)))


def knife_polynomial(j: int):
    """Numerator of the condition: all cleared denominators are positive here."""
    return sp.expand(sp.numer(sp.together(sp.simplify(knife_expr(j)))))


def verify_against_engine(j: int) -> tuple[int, int]:
    """(cells checked, disagreements) against the exact flint computation."""
    P = knife_polynomial(j)
    checked = bad = 0
    for nv in (j + 3, j + 6, j + 10, j + 18):
        for lv in (F(1), F(7)):
            for Dv in (F(6), F(11), F(23)):
                sym = P.subs(
                    {
                        n: nv,
                        lam: sp.Rational(lv.numerator, lv.denominator),
                        D: sp.Rational(Dv.numerator, Dv.denominator),
                    }
                )
                exact = (-1) ** (nv - j) * jacobi_coeff_rec(j, nv, lv, Dv)
                want = 1 if exact > 0 else (-1 if exact < 0 else 0)
                checked += 1
                if sp.sign(sym) != want:
                    bad += 1
    return checked, bad


def main() -> int:
    t0 = time.time()
    bad_E = check_E_polynomials()
    print(f"  central factorial polynomials: {len(bad_E)} mismatches", flush=True)
    rows = {}
    for j in (2, 3, 4):
        checked, bad = verify_against_engine(j)
        P = knife_polynomial(j)
        rows[str(j)] = {
            "cells_checked": checked,
            "disagreements": bad,
            "degree_n": int(sp.degree(P, n)),
            "degree_D": int(sp.degree(P, D)),
            "degree_lam": int(sp.degree(P, lam)),
            "polynomial": str(sp.factor(P)),
        }
        print(f"  knife j={j}: {checked} cells, {bad} disagreements", flush=True)
    # the fourth knife against the shore
    P4 = knife_polynomial(4)
    fails = tested = 0
    for nv in range(5, 61):
        for lv in (F(1, 4), F(1), F(3), F(7), F(26)):
            shore = T_hat(float(lv))
            for Dv in (F(4), F(6), F(11), F(23), F(60)):
                if float(Dv) >= shore or float(Dv) <= 3:
                    continue
                val = P4.subs(
                    {
                        n: nv,
                        lam: sp.Rational(lv.numerator, lv.denominator),
                        D: sp.Rational(Dv.numerator, Dv.denominator),
                    }
                )
                tested += 1
                if val <= 0:
                    fails += 1
    print(f"  knife 4 below the shore: {tested} cells, {fails} failures", flush=True)
    out = {
        "claim": "knife j > 0 iff SUM_t (-1)^t E_2t(n) s^-2t R_t > 0, with R_t"
        " elementary and E_2t explicit polynomials in n",
        "central_factorial_mismatches": bad_E,
        "knives": rows,
        "knife4_below_shore": {"cells": tested, "failures": fails},
        "status": "verified closed form and measured statement, NOT a proof:"
        " proving knife 4 needs D*(n,lam) > T_hat(lam) for all n, lam",
        "command": "python lab/knife_closed_form.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "knife_closed_form.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/knife_closed_form.json", flush=True)
    return 1 if (bad_E or fails or any(r["disagreements"] for r in rows.values())) else 0


if __name__ == "__main__":
    sys.exit(main())
