"""Gravity slice 1: the D-clock of Virasoro-Shapiro.

VS residues R_n(t) = [prod_{k=1}^{n-1}(t+k)]^2 (exact, double zeros). Unitarity
in D dims = non-negativity of Gegenbauer coefficients. Known lore: fails for
D > 10 asymptotically. We measure the finite-depth threshold n_crit(D) exactly
(even D), mirroring the q-clock methodology.

Output: results/vs_d_clock.json; per-cell progress printed.
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
NMAX = int(os.environ.get("NMAX", "24"))


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


def first_negative(D, nmax):
    mW = (D - 4) // 2
    w = [F(0)] * (2 * mW + 1)
    for j in range(mW + 1):
        w[2 * j] = F((-1) ** j * comb(mW, j))
    for n in range(2, nmax + 1):
        poly_t = [F(1)]
        for k in range(1, n):
            new = [F(0)] * (len(poly_t) + 1)
            for i, c in enumerate(poly_t):
                new[i + 1] += c
                new[i] += c * k
            poly_t = new
        sq = [F(0)] * (2 * len(poly_t) - 1)
        for i, a_ in enumerate(poly_t):
            for j, b_ in enumerate(poly_t):
                sq[i + j] += a_ * b_
        px = [F(0)] * len(sq)
        half = F(n, 2)
        for m, cm in enumerate(sq):
            if cm == 0:
                continue
            am = cm * half**m
            for j in range(m + 1):
                px[j] += am * comb(m, j) * (-1) ** (m - j)
        # fold weight into px once: pxw = px * w
        pxw = [F(0)] * (len(px) + len(w) - 1)
        for i, c in enumerate(px):
            if c == 0:
                continue
            for jw, cw in enumerate(w):
                if cw:
                    pxw[i + jw] += c * cw
        moments = [mono_int(k) for k in range(len(pxw) + 2 * n + 2)]
        for l in range(0, 2 * n - 1):
            cl = gegen_coeffs(l, D - 3)
            b = F(0)
            for i, ci in enumerate(cl):
                if ci == 0:
                    continue
                for k2, ck in enumerate(pxw):
                    if ck:
                        b += ci * ck * moments[i + k2]
            if b < 0:
                return [n, l]
    return None


def main() -> int:
    out = []
    t0 = time.time()
    for D in (12, 14, 16, 18, 20, 22, 24, 26, 28, 30):
        fn = first_negative(D, NMAX)
        out.append({"D": D, "first_negative": fn, "nmax_checked": NMAX})
        print(f"D={D}: {fn if fn else f'clean to {NMAX}'} ({time.time() - t0:.0f}s)", flush=True)
    (RES / "vs_d_clock.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written vs_d_clock.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
