"""Card A, next slice: refine the island boundary at 0.02 resolution.

Take the boundary strip of the N=40 map at mu0=0 — every ALLOWED cell touching an
excluded neighbour plus those excluded neighbours — and scan each such 0.1x0.1
square on a 0.02 sub-grid (36 points per square, exact rational arithmetic).

Depth NMAX (env, default 20) is justified by the depth study: the allowed set is
identical at N=20 and N=40, and the N=40 boundary survives N=80 unchanged.

Output: results/fine_boundary_mu0_N{NMAX}.json with per-point verdicts.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fig1_island_map import point_allowed  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = int(os.environ.get("NMAX", "20"))
SMOKE = int(os.environ.get("SMOKE", "0"))  # >0: only that many squares


def main() -> int:
    d = json.loads((RES / "fig1_map_mu0_1_N40.json").read_text())
    step = F(1, 10)
    allowed = {(F(r["r"]), F(r["w"])) for r in d["rows"] if r["allowed"]}
    all_pts = {(F(r["r"]), F(r["w"])) for r in d["rows"]}

    squares = set()
    for (r, w) in allowed:
        for dr, dw in ((step, 0), (-step, 0), (0, step), (0, -step)):
            nb = (r + dr, w + dw)
            if nb in all_pts and nb not in allowed:
                squares.add((r, w))
                squares.add(nb)
    squares = sorted(squares)
    if SMOKE:
        squares = squares[:SMOKE]
    print(f"boundary-strip squares: {len(squares)}, NMAX={NMAX}", flush=True)

    fine = F(1, 50)  # 0.02
    rows = []
    n_allowed = 0
    seen = set()
    t0 = time.time()
    for i, (r0, w0) in enumerate(squares, 1):
        sq_allowed = 0
        sq_total = 0
        for a in range(-2, 4):
            for b in range(-2, 4):
                r, w = r0 + a * fine, w0 + b * fine
                if (r, w) in seen:
                    continue
                seen.add((r, w))
                ok, first_neg = point_allowed(r, w, F(0), nmax=NMAX)
                sq_total += 1
                n_allowed += ok
                sq_allowed += ok
                rows.append({"r": str(r), "w": str(w), "allowed": ok,
                             "first_negative": first_neg})
        print(f"[{i}/{len(squares)}] square ({r0},{w0}): {sq_allowed}/{sq_total} "
              f"allowed, {time.time()-t0:.0f}s", flush=True)

    out = RES / f"fine_boundary_mu0_N{NMAX}.json"
    out.write_text(json.dumps({
        "nmax": NMAX, "mu0": "0", "fine_step": "1/50",
        "squares": len(squares), "points": len(rows),
        "allowed_count": n_allowed, "rows": rows,
    }), encoding="utf-8")
    print(f"fine boundary: {n_allowed}/{len(rows)} allowed; written {out}",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
