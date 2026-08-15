"""Knife hunt on the l = 2n-8 trajectory near the conjectured boundary.

Standalone generator for results/hunt_2n8.json (first run 2026-08-15 via the
night queue wrote a bare []; this script recreates the identical hunt and
persists it WITH run metadata, per the experiment contract).

For each lambda: D in the stress window [min_n T_n - 3, min_n T_n], even D
only, n = 5..14; alarm = any exact-rational a_{n,2n-8} < 0 at a point the
completeness conjecture calls alive. Zero alarms = the 2n-8 trajectory never
cuts deeper than the conjectured envelope on this grid.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import gegen_coeffs, mono_int  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def min_T(lamf: float) -> float:
    return min((3 * (2 * n - 3) / (n * (n - 2)))
               * (lamf * lamf + (2 * n - 2) * lamf + 1) + 2 * n
               for n in range(3, 400))


def a_l(n: int, l: int, lam: F, D: int) -> F:
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
    mW = (D - 4) // 2
    w = [F(0)] * (2 * mW + 1)
    for j in range(mW + 1):
        w[2 * j] = F((-1) ** j * comb(mW, j))
    Pw = [F(0)] * (len(P) + len(w) - 1)
    for i, c in enumerate(P):
        if c == 0:
            continue
        for jw, cw in enumerate(w):
            if cw:
                Pw[i + jw] += c * cw
    cl = gegen_coeffs(l, D - 3)
    b = F(0)
    for i, ci in enumerate(cl):
        if ci == 0:
            continue
        for k2, ck in enumerate(Pw):
            if ck:
                b += ci * ck * mono_int(i + k2)
    return b


def main() -> int:
    t0 = time.time()
    alarms = []
    lams = [F(i, 10) for i in range(1, 31)] + [F(4), F(5), F(7), F(10)]
    checks = 0
    for lam in lams:
        Dtop = int(min_T(float(lam)))
        for D in range(max(4, Dtop - 3), Dtop + 1):
            if D % 2:
                continue
            for n in range(5, 15):
                checks += 1
                if a_l(n, 2 * n - 8, lam, D) < 0:
                    alarms.append({"lam": str(lam), "D": D, "n": n})
                    break
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"alarms": alarms, "n_lambdas": len(lams), "n_range": "5..14",
           "window": "[minT-3, minT] even D", "checks": checks,
           "command": "python lab/hunt_2n8.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "hunt_2n8.json").write_text(json.dumps(out, indent=1),
                                       encoding="utf-8")
    print(f"2n-8 hunt: {len(alarms)} alarms over {len(lams)} lambdas,"
          f" {checks} checks, {time.time()-t0:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
