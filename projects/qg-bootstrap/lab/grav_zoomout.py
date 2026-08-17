"""Zoom-out scan of the closed-string family: lambda 0.05..10, D 4..60, depth 12.

Regenerates results/grav_zoomout.json (original committed 2026-08-14 from an
inline run; this script is its generator, added for the release package) as
results/grav_zoomout_v2.json WITH run metadata, and verifies every verdict
against the original artifact. Exact rational arithmetic throughout.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import first_negative  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = 12
LAMS = [
    F(1, 20),
    F(1, 10),
    F(1, 5),
    F(3, 10),
    F(2, 5),
    F(1, 2),
    F(3, 5),
    F(7, 10),
    F(4, 5),
    F(9, 10),
    F(1),
    F(11, 10),
    F(5, 4),
    F(3, 2),
    F(7, 4),
    F(2),
    F(5, 2),
    F(3),
    F(4),
    F(5),
    F(7),
    F(10),
]
DS = list(range(4, 61, 4))


def main() -> int:
    t0 = time.time()
    rows = []
    for D in DS:
        for lam in LAMS:
            fn = first_negative(lam, D, NMAX)
            rows.append({"lambda": str(lam), "D": D, "allowed": fn is None, "first_negative": fn})
        print(f"D={D} done ({time.time() - t0:.0f}s)", flush=True)
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "nmax": NMAX,
        "grid": {"lambdas": [str(x) for x in LAMS], "Ds": DS},
        "command": "python lab/grav_zoomout.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
        "rows": rows,
    }
    (RES / "grav_zoomout_v2.json").write_text(json.dumps(out), encoding="utf-8")

    orig = json.loads((RES / "grav_zoomout.json").read_text(encoding="utf-8"))
    omap = {(r["lambda"], r["D"]): r["allowed"] for r in orig}
    mism = [r for r in rows if omap.get((r["lambda"], r["D"])) != r["allowed"]]
    print(
        f"verdict match vs original: {len(rows) - len(mism)}/{len(rows)} (mismatches: {len(mism)})",
        flush=True,
    )
    return 1 if mism else 0


if __name__ == "__main__":
    sys.exit(main())
