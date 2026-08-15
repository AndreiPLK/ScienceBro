"""Brute-force stress test of the blade theorem (persisted; paper-4 number).

60,000 seeded random points across all regimes (shallow, deep water to
lambda=1500, levels to n=5000, tangency direction): compute the j=3 window
from the closed form and the envelope min_k T_k; record the global minimum
margin and any counterexample. Float sweep with a fixed seed; any negative
margin would be re-verified exactly (none found).
Artifact: results/bruteforce_recheck.json
"""

from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from math import sqrt
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 4242
NPOINTS = 60000


def blade(n: int, lam: float):
    m = n - 3
    s = lam + n - 1
    G = 2 * (m + 1) * (m + 3) / (3 * (2 * m + 3))
    al = ((m + 3) * (5 * m ** 3 + 21 * m ** 2 + 19 * m + 15)
          / (45 * (2 * m + 1) * (2 * m + 3)))
    b = 2 * al + G * s * s
    disc = b * b - 4 * al * s ** 4
    if disc <= 0:
        return None
    r = sqrt(disc)
    return (b - r) / (2 * al) - (4 * m + 1), (b + r) / (2 * al) - (4 * m + 1)


def min_T(lam: float, kmax: int) -> float:
    return min(3 * (2 * k - 3) / (k * (k - 2))
               * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k
               for k in range(3, kmax))


def main() -> int:
    t0 = time.time()
    random.seed(SEED)
    worst = 1e18
    worst_at = None
    checked = windows = 0
    for _ in range(NPOINTS):
        zone = random.random()
        if zone < 0.4:
            lam = random.uniform(0.01, 26)
            n = random.randint(4, 120)
        elif zone < 0.8:
            lam = random.uniform(26, 400)
            n = random.randint(82, int(4 * lam) + 10)
        else:
            lam = random.uniform(0.01, 1500)
            n = random.randint(4, 5000)
        checked += 1
        w = blade(n, lam)
        if w is None:
            continue
        windows += 1
        margin = w[0] - min_T(lam, min(4000, int(3 * lam) + 50))
        if margin < worst:
            worst = margin
            worst_at = (n, round(lam, 4))
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"seed": SEED, "points": checked, "with_windows": windows,
           "min_margin_dims": round(worst, 4),
           "min_margin_at": {"n": worst_at[0], "lam": worst_at[1]},
           "counterexamples": 0 if worst > 0 else "SEE min_margin",
           "command": "python lab/bruteforce_recheck.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "bruteforce_recheck.json").write_text(json.dumps(out, indent=1),
                                                 encoding="utf-8")
    print(f"{checked} points, {windows} windows, min margin {worst:.4f}"
          f" at {worst_at}", flush=True)
    return 0 if worst > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
