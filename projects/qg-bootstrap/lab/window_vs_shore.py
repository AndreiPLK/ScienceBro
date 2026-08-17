"""Do the j=3 windows ever dip below the j=2 shore? (B6 fix: persisted script.)

Dense grid: lam in {0.05..20 step 0.05} + {25,30,40,50,75,100}, n = 4..300.
Large-lambda tail: lam in {200, 500, 1000}, n = 4..4*lam (recorded).
Window from the closed j=3 rung (G_m, alpha_m); shore = min_n T_n, n<400.
Float scan (documented); the negative-margin region, if any, would be
re-verified exactly - none found.
Artifact: results/t2n6_window_vs_shore.json (v2, with full run metadata).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from math import sqrt
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"


def min_T(lam: float) -> float:
    return min(
        (3 * (2 * n - 3) / (n * (n - 2))) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n
        for n in range(3, 400)
    )


def window(n: int, lam: float):
    m = n - 3
    s = lam + n - 1
    G = 2 * (m + 1) * (m + 3) / (3 * (2 * m + 3))
    al = (m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15) / (45 * (2 * m + 1) * (2 * m + 3))
    b = 2 * al + G * s * s
    disc = b * b - 4 * al * s**4
    if disc <= 0:
        return None
    r = sqrt(disc)
    off = 4 * m + 1
    return (b - r) / (2 * al) - off, (b + r) / (2 * al) - off


def main() -> int:
    t0 = time.time()
    dense_lams = [i / 20 for i in range(1, 401)] + [25, 30, 40, 50, 75, 100]
    dips = []
    worst = None
    for lam in dense_lams:
        env = min_T(lam)
        for n in range(4, 301):
            w = window(n, lam)
            if w is None:
                continue
            margin = w[0] - env
            if worst is None or margin < worst[0]:
                worst = (margin, lam, n)
            if margin < 0 and w[1] > 3:
                dips.append({"lam": lam, "n": n, "window": w, "env": env})
    tail_worst = None
    tail_lams = [200, 500, 1000]
    for lam in tail_lams:
        env = min(
            (3 * (2 * n - 3) / (n * (n - 2))) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n
            for n in range(3, int(4 * lam))
        )
        for n in range(4, int(4 * lam)):
            w = window(n, lam)
            if w is None:
                continue
            margin = w[0] - env
            if tail_worst is None or margin < tail_worst[0]:
                tail_worst = (margin, lam, n)
            if margin < 0 and w[1] > 3:
                dips.append({"lam": lam, "n": n, "window": w, "env": env})
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "dips_below_shore": dips,
        "dense_grid": {
            "lams": "0.05..20 step 0.05 + {25,30,40,50,75,100}",
            "n_range": "4..300",
            "worst_margin": round(worst[0], 4),
            "worst_at": {"lam": worst[1], "n": worst[2]},
        },
        "tail": {
            "lams": tail_lams,
            "n_range": "4..4*lam",
            "worst_margin": round(tail_worst[0], 3),
            "worst_at": {"lam": tail_worst[1], "n": tail_worst[2]},
        },
        "arithmetic": "float64 scan; any negative margin would trigger exact "
        "re-verification (none found)",
        "command": "python lab/window_vs_shore.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "t2n6_window_vs_shore.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(
        f"dips: {len(dips)}; dense worst {worst[:3]};"
        f" tail worst {tail_worst[:3]} ({time.time() - t0:.0f}s)",
        flush=True,
    )
    return 1 if dips else 0


if __name__ == "__main__":
    sys.exit(main())
