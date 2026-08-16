"""Prover v2 (flint engine): shallow stage of the general-knife prover.

Same mathematics and cell logic as lab/knife_proof.py (v1), only the
arithmetic engine changes: exact fmpq (C-speed) instead of sympy symbols.
Key structural wins over v1:
  - B_j(lam, D) coefficients computed ONCE per (j, m) as exact integers
    and reused by all 43 branches (v1 rebuilt the polynomial per subcell);
  - interval substitutions lam = a+(b-a)w/(1+w), D = 4+(T_k-4)u/(1+u) are
    cleared of denominators analytically: p + 2q <= 2(j-1) uniformly, so
    N = (1+w)^{2(j-1)} (1+u)^{j-1} P is a polynomial with the same sign;
  - positivity certificate: all coefficients of N nonnegative in (u, w)
    (the exact v1 certificate), pure fmpq arithmetic.

Usage: KNIFE_J=4 python lab/knife_proof2.py
Artifact: results/knife_proof2_j{J}.json; exit 0 iff every cell certifies.
Validation contract: verdict and cell count must reproduce v1 artifacts.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from math import factorial
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402
from prover2_core import QPoly  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))
MFIX = int(os.environ.get("MFIX", "40"))

U, W = 0, 1  # variable indices


def e_doubled_int(n: int):
    poly = [1]
    for k in range(1, n):
        r = n - 2 * k
        for _ in range(2):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] += c * r
            poly = new
    return [abs(poly[2 * t]) for t in range(len(poly) // 2 + 1)]


def binom_int(a, b):
    if b < 0 or b > a:
        return 0
    return factorial(a) // (factorial(b) * factorial(a - b))


def Bj_coeffs(j, mv):
    """{(p, q): int} for (-1)^{j-1} B_j(lam, D) at fixed m=mv (exact)."""
    n = mv + 3
    e = e_doubled_int(n)
    c = 4 * n - 4 * j - 1
    coeffs = {}
    for i in range(j):
        wgt = factorial(2 * n - 2 * j + 2 * i) // (factorial(i) * 2 ** i)
        # tail = prod_{k=i}^{j-2} (D + c + 2k): integer coeffs by D-power q
        tail = [1]
        for k in range(i, j - 1):
            const = c + 2 * k
            new = [0] * (len(tail) + 1)
            for q, tq in enumerate(tail):
                new[q] += tq * const
                new[q + 1] += tq
            tail = new
        base = (-1) ** i * e[j - 1 - i] * wgt
        # s^{2i} = sum_p C(2i,p) (n-1)^{2i-p} lam^p
        for p in range(2 * i + 1):
            sp_c = binom_int(2 * i, p) * (n - 1) ** (2 * i - p)
            for q, tq in enumerate(tail):
                key = (p, q)
                coeffs[key] = coeffs.get(key, 0) + base * sp_c * tq
    if j % 2 == 0:
        coeffs = {k: -v for k, v in coeffs.items()}
    return {k: v for k, v in coeffs.items() if v != 0}


def cell_certify(coeffs, j, kk, a, b, onto_zero=False):
    """All coefficients of N(u, w) nonnegative? Exact, denominator-free.

    onto_zero (k=3 head branch, blade-proof substitution): (a, b) is a
    t-interval in [0, 1] and lam = (2/3)(1 - t), t = a + (b-a)w/(1+w);
    numerator of lam is (2/3)((1-a) + (1-b)w) — nonnegative coefficients,
    and the cell covers lam in ((2/3)(1-b), (2/3)(1-a)], so the union over
    the bisection tree is ONTO (0, 2/3] including arbitrarily small lam.
    Fixes the (0, 1/1000) strip the fleet review found uncovered (ERR-0002).
    """
    a = fmpq(a.numerator, a.denominator)
    b = fmpq(b.numerator, b.denominator)
    onepw = QPoly(2, {(0, 0): fmpq(1), (0, 1): fmpq(1)})
    onepu = QPoly(2, {(0, 0): fmpq(1), (1, 0): fmpq(1)})
    if onto_zero:
        c = fmpq(2, 3)
        numlam = QPoly(2, {(0, 0): c * (1 - a), (0, 1): c * (1 - b)})
    else:
        numlam = QPoly(2, {(0, 0): a, (0, 1): b})
    r = fmpq(3 * (2 * kk - 3), kk * (kk - 2))
    onepw2 = onepw * onepw
    tk_num = r * (numlam * numlam + (2 * kk - 2) * (numlam * onepw)
                  + onepw2) + (2 * kk) * onepw2
    u_poly = QPoly(2, {(1, 0): fmpq(1)})
    numd = (4 * onepw2) * onepu + (tk_num - 4 * onepw2) * u_poly
    dmax = 2 * (j - 1)
    qmax = j - 1
    lam_pows = {0: QPoly.const(2, 1)}
    d_pows = {0: QPoly.const(2, 1)}
    w_pows = {0: QPoly.const(2, 1)}
    u_pows = {0: QPoly.const(2, 1)}
    for name, basep, store, top in ((0, numlam, lam_pows, dmax),
                                    (1, numd, d_pows, qmax),
                                    (2, onepw, w_pows, dmax),
                                    (3, onepu, u_pows, qmax)):
        for t in range(1, top + 1):
            store[t] = store[t - 1] * basep
    N = QPoly(2)
    for (p, q), cpq in coeffs.items():
        term = lam_pows[p] * d_pows[q]
        wdef = dmax - p - 2 * q
        udef = qmax - q
        if wdef:
            term = term * w_pows[wdef]
        if udef:
            term = term * u_pows[udef]
        N = N + fmpq(cpq) * term
    return all(v >= 0 for v in N.c.values())


def cell_shallow(coeffs, j, kk, mu_lo, mu_hi, depth, log, tag,
                 onto_zero=False):
    def try_cell(a, b, d):
        okc = cell_certify(coeffs, j, kk, a, b, onto_zero)
        log.append({"cell": tag, "ok": bool(okc)})
        if okc:
            return True
        if d == 0:
            return False
        mid = (a + b) / 2
        return try_cell(a, mid, d - 1) and try_cell(mid, b, d - 1)

    return try_cell(mu_lo, mu_hi, depth)


def j_min_m(j):
    return max(1, j - 2)


def main() -> int:
    t0 = time.time()
    log = []
    ok = True
    bj_cache = {mv: Bj_coeffs(J, mv)
                for mv in range(j_min_m(J), MFIX + 1)}
    for kk in range(3, 46):
        onto = kk == 3
        if kk == 3:
            # blade substitution lam=(2/3)(1-t), t in [0,1]: ONTO (0, 2/3]
            mu_lo, mu_hi = Fraction(0), Fraction(1)
        else:
            mu_lo = Fraction(3, 5) * (kk - Fraction(5, 2))
            mu_hi = Fraction(3, 5) * (kk - Fraction(3, 2))
            if kk == 4:
                mu_lo = Fraction(2, 3)
        branch_ok = True
        for mv in range(j_min_m(J), MFIX + 1):
            got = cell_shallow(bj_cache[mv], J, kk, mu_lo, mu_hi, 4, log,
                               f"j{J}_k{kk}_m{mv}", onto_zero=onto)
            branch_ok &= got
            if not got:
                print(f"  FAIL j={J} k={kk} m={mv}", flush=True)
        ok &= branch_ok
        print(f"branch k={kk}: {'OK' if branch_ok else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)
    prov = stamp()
    out = {"j": J, "ok_so_far": bool(ok), "engine": "prover2-flint",
           "scope": f"shallow branches k=3..45, m={j_min_m(J)}..{MFIX}; "
                    "k=3 via blade substitution lam=(2/3)(1-t), ONTO (0,2/3]"
                    " incl. lam<1/1000 (ERR-0002 repair)",
           "cells": len(log),
           "command": f"KNIFE_J={J} python lab/knife_proof2.py",
           **prov, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"knife_proof2_j{J}.json").write_text(json.dumps(out, indent=1),
                                                 encoding="utf-8")
    print(("SHALLOW CERTIFIED" if ok else "INCOMPLETE") +
          f" (cells {len(log)})", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
