"""The FULL BODY: allowed region of the closed-string family in (lambda, D).

Corrected evaluator (Pochhammer step 1). For each grid point: first negative
over ALL even l <= 2n-2, n <= NMAX. Paints the whole continent of life whose
edges our formulas describe.

Output: results/grav_full_body.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F
from math import comb
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = int(os.environ.get("NMAX", "14"))

LAMS = [F(i, 20) for i in range(1, 41)]          # 0.05 .. 2.00
DS = list(range(4, 31, 2))


def gegen_coeffs(l, alpha2):
    a = F(alpha2, 2)
    p0, p1 = [F(1)], [F(0), 2 * a]
    if l == 0:
        return p0
    if l == 1:
        return p1
    for m in range(2, l + 1):
        xp = [F(0)] + p1
        new = [2 * (m - 1 + a) * c / m for c in xp]
        for i, c in enumerate(p0):
            new[i] -= (m - 2 + 2 * a) * c / m
        p0, p1 = p1, new
    return p1


def mono_int(k):
    return F(0) if k % 2 else F(2, k + 1)


def first_negative(lam, D, nmax):
    mW = (D - 4) // 2
    w = [F(0)] * (2 * mW + 1)
    for j in range(mW + 1):
        w[2 * j] = F((-1) ** j * comb(mW, j))
    for n in range(2, nmax + 1):
        mu = (n + lam - 1) / lam
        A = lam * mu / 2
        poly = [F(1)]
        for k in range(1, n):
            b = (1 + lam) / 2 + (k - 1) - A
            new = [F(0)] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c * b
                new[i + 1] += c * A
            poly = new
        P = [F(0)] * (2 * len(poly) - 1)
        for i, a_ in enumerate(poly):
            for j, b_ in enumerate(poly):
                P[i + j] += a_ * b_
        Pw = [F(0)] * (len(P) + len(w) - 1)
        for i, c in enumerate(P):
            if c == 0:
                continue
            for jw, cw in enumerate(w):
                if cw:
                    Pw[i + jw] += c * cw
        for l in range(0, 2 * n - 1, 2):
            cl = gegen_coeffs(l, D - 3)
            b = F(0)
            for i, ci in enumerate(cl):
                if ci == 0:
                    continue
                for k2, ck in enumerate(Pw):
                    if ck:
                        b += ci * ck * mono_int(i + k2)
            if b < 0:
                return [n, l]
    return None


def main() -> int:
    rows = []
    t0 = time.time()
    for D in DS:
        alive = 0
        for lam in LAMS:
            fn = first_negative(lam, D, NMAX)
            rows.append({"lambda": str(lam), "D": D, "allowed": fn is None,
                         "first_negative": fn})
            alive += fn is None
        print(f"D={D}: {alive}/{len(LAMS)} alive ({time.time()-t0:.0f}s)",
              flush=True)
    (RES / "grav_full_body.json").write_text(
        json.dumps({"nmax": NMAX, "rows": rows}, indent=None), encoding="utf-8")
    print("written grav_full_body.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
