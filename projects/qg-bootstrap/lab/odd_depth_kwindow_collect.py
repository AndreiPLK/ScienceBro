"""Consolidate the per-job k-window certification states into the official
artifact. A job's state file (results/raw/kwindow_state/kwstate_*.json,
written by odd_depth_kwindow_cert.py) is final when it has done:true; the
depth is PROVED when every job of both parities is done with 0 open boxes.

Refuses to write anything if a job is missing or unfinished -- a partial
consolidation would be the ERR-0002 mistake (a consolidation JSON is a claim
and goes through the same gate).

Run: python lab/odd_depth_kwindow_collect.py <d>
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from odd_depth_kwindow_cert import DELTA, KMIN, STATE_DIR  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

JOBS = [
    ("even", "0", "1/2"),
    ("even", "1/2", "999/1000"),
    ("odd", "0", "1/2"),
    ("odd", "1/2", "999/1000"),
]


def main() -> int:
    d = int(sys.argv[1])
    rows = []
    for parity, ylo, yhi in JOBS:
        tag = f"d{d}_{parity}_y{ylo.replace('/', '-')}_{yhi.replace('/', '-')}"
        path = STATE_DIR / f"kwstate_{tag}.json"
        if not path.exists():
            print(f"MISSING job state: {path}")
            return 1
        st = json.loads(path.read_text(encoding="utf-8"))
        if not st.get("done"):
            print(f"UNFINISHED job: {tag} ({len(st.get('pending', []))} pending)")
            return 1
        rows.append(
            {
                "parity": parity,
                "y_range": [ylo, yhi],
                "boxes": st["boxes"],
                "open": len(st["open_boxes"]),
                "open_sample": st["open_boxes"][:3],
            }
        )
    proved = all(r["open"] == 0 for r in rows)
    out = {
        "claim": (
            f"REPAIRED step (a) for odd depth {d} (ERR-0013): the depth-{d} knife is "
            f"positive at D = T_{{k+delta}}(lam*(k)) for every level K >= 3 (compactified, "
            f"covered to K ~ 12000), every k in [{KMIN}, ~12000] on the critical curve "
            f"dT/dk = 0 (lam*({KMIN}) < 7, overlapping the fixed-k_s band below), and every "
            f"delta in [-{DELTA}, {DELTA}]. Combined with step (b) (integer argmin within 1 "
            f"of k* for lam >= 7, PROVED) and step (c) (monotonicity below the shore), this "
            f"replaces the refuted fixed-v-window lo piece at odd depths. Coverage is finite "
            f"in K and k, as for the even-depth certificates."
        ),
        "proved": proved,
        "jobs": rows,
        "method": (
            "G = A + B*w built by substitution from the validated build_branch "
            "(odd_depth_kwindow.py, self-check 0/296 mismatches, non-vacuous); Bernstein "
            "bisection on (K, k compactified, delta) with exact rational sqrt brackets on w "
            "per box (odd_depth_kwindow_cert.py), run as 4 resumable parallel jobs."
        ),
        "command": "python lab/odd_depth_kwindow_cert.py <d> <parity> <ylo> <yhi>",
        **stamp(),
    }
    path = RES / f"odd_depth_kwindow_cert_d{d}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"depth {d}: proved={proved}; jobs={[(r['parity'], r['y_range'], r['boxes'], r['open']) for r in rows]}")
    print(f"written {path}")
    return 0 if proved else 2


if __name__ == "__main__":
    raise SystemExit(main())
