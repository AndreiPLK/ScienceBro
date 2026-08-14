"""Gravity slice 3: fate of the alternatives in D=4.

CHR claim positivity for ALL lambda>=0 in D=4 (their finite depth). We push
the lambda-family residues R(n,t)=[((1+l)/2+lt)_{n-1}]^2 (positive denominator
dropped) through exact Legendre projection (D=4) for low spins l=0..8 and
n<=NMAX, across a lambda grid including the extremal corners.

Output: results/grav_d4_lowspin.json; progress per lambda.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = int(os.environ.get("NMAX", "40"))
LMAX = 8

LAMBDAS = [F(1, 100), F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(9, 10),
           F(1), F(11, 10), F(3, 2), F(2), F(4), F(10), F(100)]


def legendre_coeffs(l):
    p0, p1 = [F(1)], [F(0), F(1)]
    if l == 0:
        return p0
    if l == 1:
        return p1
    for m in range(2, l + 1):
        xp = [F(0)] + p1
        new = [(2 * m - 1) * c / m for c in xp]
        for i, c in enumerate(p0):
            new[i] -= (m - 1) * c / m
        p0, p1 = p1, new
    return p1


def mono_int(k):
    return F(0) if k % 2 else F(2, k + 1)


PLS = [legendre_coeffs(l) for l in range(0, LMAX + 1)]


def scan_lambda(lam, nmax):
    first_neg = None
    for n in range(2, nmax + 1):
        A = (n + lam - 1) / 2
        poly = [F(1)]
        for k in range(1, n):
            b = (1 + lam) / 2 + lam * (k - 1) - A
            new = [F(0)] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c * b
                new[i + 1] += c * A
            poly = new
        P = [F(0)] * (2 * len(poly) - 1)
        for i, a_ in enumerate(poly):
            for j, b_ in enumerate(poly):
                P[i + j] += a_ * b_
        for l in range(0, min(LMAX, 2 * n - 2) + 1, 2):
            b = F(0)
            for i, ci in enumerate(PLS[l]):
                if ci == 0:
                    continue
                for k2, ck in enumerate(P):
                    if ck:
                        b += ci * ck * mono_int(i + k2)
            if b < 0:
                return [n, l]
    return None


def main() -> int:
    out = []
    t0 = time.time()
    for lam in LAMBDAS:
        fn = scan_lambda(lam, NMAX)
        out.append({"lambda": str(lam), "first_negative_low_spin": fn,
                    "nmax": NMAX, "lmax": LMAX})
        print(f"lambda={lam}: {fn if fn else f'clean (l<={LMAX}, n<={NMAX})'} "
              f"({time.time()-t0:.0f}s)", flush=True)
    (RES / "grav_d4_lowspin.json").write_text(json.dumps(out, indent=1),
                                              encoding="utf-8")
    print("written grav_d4_lowspin.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
