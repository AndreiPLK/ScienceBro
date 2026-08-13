"""Card A, decisive slice: does the island boundary move between N=40 and N=80?

Take every ALLOWED point at N=40 that touches an excluded neighbour (the boundary
cells) and re-test exactly those cells at NMAX=80. If none fall, the boundary is
stable under another doubling of the positivity depth at grid resolution 0.1.
Exact rational arithmetic throughout.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fig1_island_map import point_allowed  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def main() -> int:
    d = json.loads((RES / "fig1_map_mu0_1_N40.json").read_text())
    step = F(1, 10)
    allowed = {(F(r["r"]), F(r["w"])) for r in d["rows"] if r["allowed"]}
    all_pts = {(F(r["r"]), F(r["w"])) for r in d["rows"]}

    boundary = []
    for (r, w) in allowed:
        for dr, dw in ((step, 0), (-step, 0), (0, step), (0, -step)):
            nb = (r + dr, w + dw)
            if nb not in allowed and (nb in all_pts):
                boundary.append((r, w))
                break
    print(f"boundary cells at N=40: {len(boundary)}")

    fell = []
    for (r, w) in sorted(boundary):
        ok, first_neg = point_allowed(r, w, F(0), nmax=80)
        if not ok:
            fell.append({"r": str(r), "w": str(w), "first_negative": first_neg})
    out = {"boundary_cells": len(boundary), "fell_at_N80": fell,
           "stable": not fell}
    (RES / "boundary_N80_mu0.json").write_text(json.dumps(out, indent=2),
                                               encoding="utf-8")
    print(f"fell at N=80: {len(fell)}")
    for f_ in fell:
        print("  ", f_)
    print("BOUNDARY STABLE 40->80" if not fell else "BOUNDARY MOVED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
