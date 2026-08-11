"""P3 remainder: float32-vs-float64 sensitivity + spatial residual map (2D smoke model).

Outputs:
  results/processed/calibration_maps.json   — stats (median/p95/p99/max, float32 delta)
  results/figures/residual_map_2d.html      — plotly heatmap of max|Ricci| over the ball
Run: uv run python projects/ainstein-audit/verifier/calibration_maps.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.geometry import ricci_tensor  # noqa: E402
from verifier.interface import RecordingMetric  # noqa: E402
from verifier.discrepancy_experiment import export  # noqa: E402

OUT_JSON = Path(__file__).resolve().parents[1] / "results" / "processed" / "calibration_maps.json"
OUT_FIG = Path(__file__).resolve().parents[1] / "results" / "figures" / "residual_map_2d.html"
H = 3e-3


def main() -> int:
    # grid over the training ball (radius 0.95), 17x17 -> 217 in-ball points
    lin = np.linspace(-0.95, 0.95, 17)
    grid = [np.array([a, b]) for a in lin for b in lin if a * a + b * b <= 0.95**2]

    # one batched export for every stencil point
    seen, stencil = set(), []
    for x in grid:
        rec = RecordingMetric(2)
        try:
            ricci_tensor(rec, x, h=H)
        except Exception:
            pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                stencil.append(p)
    stencil = np.array(stencil, dtype=np.float64)
    g_vals, _ = export(stencil)
    cache64 = {tuple(np.round(p, 12)): g_vals[i] for i, p in enumerate(stencil)}
    cache32 = {k: v.astype(np.float32).astype(np.float64) for k, v in cache64.items()}

    def g64(x):
        return cache64[tuple(np.round(x, 12))]

    def g32(x):
        return cache32[tuple(np.round(x, 12))]

    res64, res32, xs, ys = [], [], [], []
    for x in grid:
        r64 = float(np.max(np.abs(ricci_tensor(g64, x, h=H))))
        r32 = float(np.max(np.abs(ricci_tensor(g32, x, h=H))))
        res64.append(r64)
        res32.append(r32)
        xs.append(float(x[0]))
        ys.append(float(x[1]))

    a64, a32 = np.array(res64), np.array(res32)
    stats = {
        "n_grid_points": len(grid),
        "h": H,
        "float64": {
            "median": float(np.median(a64)), "p95": float(np.percentile(a64, 95)),
            "p99": float(np.percentile(a64, 99)), "max": float(a64.max()),
        },
        "float32_metric_storage": {
            "median": float(np.median(a32)), "p95": float(np.percentile(a32, 95)),
            "p99": float(np.percentile(a32, 99)), "max": float(a32.max()),
        },
        "float32_vs_float64_median_ratio": float(np.median(a32) / np.median(a64)),
        "conclusion_data": "float32 storage of metric components inflates the FD residual "
                           "by the measured ratio; see numbers — no narrative here.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    import plotly.graph_objects as go

    fig = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker={"size": 9, "color": np.log10(a64), "colorscale": "Viridis",
                "colorbar": {"title": "log10 max|Ricci|"}},
        text=[f"{v:.2e}" for v in a64],
    ))
    fig.update_layout(
        title="Independent FD residual map, smoke model (float64, h=3e-3)",
        xaxis_title="x1", yaxis_title="x2", width=700, height=650,
    )
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUT_FIG, include_plotlyjs="cdn")
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
