"""Binomial collapse verification: zone clustering of all knives (paper 5).

For a grid of (n, lambda): compute, in exact arithmetic from the master
formula, the negativity zones of every knife j=2..JMAX and their offsets from
the level's critical line D_crit = 6 s^2/m - 4m (the leading-order line of
the FIRST knife). The collapse B_j ~ (1-X)^{j-1} predicts: all zones cluster
within O(sqrt(m)) of D_crit and split into floor(j/2) bands.
Artifact: results/collapse_zones.json
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from math import factorial
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
JMAX = 8


def e_doubled(n: int):
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


def knife_sign(n, j, lam, Dv, e):
    c = 4 * n - 4 * j - 1
    s = lam + n - 1
    B = F(0)
    for i in range(j):
        w = F(factorial(2 * n - 2 * j + 2 * i), factorial(i) * 2**i)
        tail = F(1)
        for k in range(i, j - 1):
            tail *= Dv + c + 2 * k
        B += (-1) ** i * e[j - 1 - i] * w * s ** (2 * i) * tail
    if j % 2 == 0:
        B = -B
    return (B > 0) - (B < 0)


def main() -> int:
    t0 = time.time()
    rows = []
    for n, lam in [
        (20, F(1)),
        (30, F(2)),
        (40, F(5)),
        (50, F(5)),
        (60, F(8)),
        (80, F(10)),
        (100, F(12)),
    ]:
        m = n - 3
        s = lam + n - 1
        Dcrit = float(6 * s * s / m - 4 * m)
        e = e_doubled(n)
        Dmax = int(Dcrit * 2) + 60
        entry = {"n": n, "lam": str(lam), "D_crit": round(Dcrit, 2), "zones": {}}
        for j in range(2, min(JMAX, n - 1) + 1):
            neg = [Dv for Dv in range(4, Dmax) if knife_sign(n, j, lam, Dv, e) < 0]
            runs = []
            if neg:
                start = prev = neg[0]
                for d in neg[1:]:
                    if d == prev + 1:
                        prev = d
                    else:
                        runs.append([start, prev])
                        start = prev = d
                runs.append([start, prev])
            entry["zones"][str(j)] = {
                "bands": len(runs),
                "expected_bands": j // 2,
                "offsets_from_Dcrit": [[round(a - Dcrit), round(b - Dcrit)] for a, b in runs],
            }
        rows.append(entry)
        print(f"n={n} lam={lam} done ({time.time() - t0:.0f}s)", flush=True)
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "rows": rows,
        "jmax": JMAX,
        "prediction": "B_j ~ term0*(1-X)^{j-1}, X=6rho^2/(delta+4); "
        "zones cluster near D_crit, floor(j/2) bands",
        "command": "python lab/collapse_zones.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "collapse_zones.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    # проверка предсказания о числе полос (последняя полоса j чётного —
    # полубесконечная зона, тоже считается)
    bad = []
    for r in rows:
        for j, z in r["zones"].items():
            if z["bands"] != z["expected_bands"] and int(j) <= r["n"] - 2:
                bad.append((r["n"], j, z["bands"], z["expected_bands"]))
    print(f"band-count check: {len(bad)} deviations", flush=True)
    for b in bad[:5]:
        print("  dev:", b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
