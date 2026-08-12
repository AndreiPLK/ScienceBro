"""Boundary/horizon residual map for a 4D candidate (stage-4 'boundary-maps').

Grid over the Penrose (T,X) block at fixed stereo point (0.1, 0.1), patch 0,
covering exterior AND interior regions through the horizon X=|T|. Independent FD
max|Ricci| at each valid grid point; horizon and diagram boundary marked.
Output: results/processed/boundary_map.json + article/visuals HTML+PNG.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier import known_answer_4d as ka  # noqa: E402
from verifier.geometry import ricci_tensor  # noqa: E402
from verifier.interface import RecordingMetric  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
MODEL = PROJ / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras"
OUT = PROJ / "results" / "processed" / "boundary_map.json"
H = 3e-3
Q = (0.1, 0.1)


def valid(t: float, x: float) -> bool:
    # inside the sampled Penrose block (R_rho = 0.85 scaling, keep margin) and
    # away from the exact diagram corners
    return abs(t) + abs(x) < 0.80 and abs(t) < 0.62 and 0.05 < x < 0.80


def main() -> int:
    ts = np.linspace(-0.6, 0.6, 13)
    xs = np.linspace(0.08, 0.78, 13)
    grid = [np.array([t, x, *Q]) for t in ts for x in xs if valid(t, x)]

    ka.SNAPSHOT = str(MODEL)
    seen, stencil = set(), []
    for p in grid:
        rec = RecordingMetric(4)
        try:
            ricci_tensor(rec, p, h=H)
        except Exception:
            pass
        for q in rec.points:
            if q not in seen:
                seen.add(q)
                stencil.append(q)
    stencil = np.array(stencil, dtype=np.float64)
    pts5 = np.hstack([stencil, np.zeros((len(stencil), 1))])
    values = ka.export(pts5, analytic=False)
    cache = {tuple(np.round(p, 12)): values[i] for i, p in enumerate(stencil)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    rows = []
    for p in grid:
        r = float(np.max(np.abs(ricci_tensor(g, p, h=H))))
        region = "interior" if abs(np.cos(2 * p[0]) / np.cos(2 * p[1])) < 1.0 else "exterior"
        rows.append({"T": float(p[0]), "X": float(p[1]), "max_abs_ricci": r, "region": region})
    OUT.write_text(json.dumps({"model": str(MODEL), "h": H, "q": Q, "rows": rows},
                              indent=2), encoding="utf-8")
    print(f"points={len(rows)} "
          f"exterior_median={np.median([r['max_abs_ricci'] for r in rows if r['region']=='exterior']):.3f} "
          f"interior_median={np.median([r['max_abs_ricci'] for r in rows if r['region']=='interior']):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
