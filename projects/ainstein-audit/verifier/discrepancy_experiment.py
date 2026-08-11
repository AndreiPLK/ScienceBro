"""Discrepancy experiment: upstream loss 1.6e-10 vs independent max|Ricci| 3.3e-6.

Measures — does not narrate — the candidate causes on the 2026-08-11 smoke model
(SchwarzschildLocal2DModel, dim 2, lambda=0). Produces a machine-readable JSON and a
Markdown table under results/processed/.

Factors tested:
  A. Quantity definition: upstream loss is QUADRATIC in Ricci with Euclidean
     contraction and volume weighting (losses/schwarzschild.py:1944-1956):
       L = mean_a | R_ij gE^ik gE^jl R_kl | * sqrt|det g|
     while our residual is linear (max |R_ab| or Frobenius).
  B. Finite-difference step sweep on the NN metric.
  C. Evaluation points: interior training ball vs near its boundary.
  D. Norm choice on the same Ricci.
Run:  uv run python projects/ainstein-audit/verifier/discrepancy_experiment.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.geometry import ricci_tensor  # noqa: E402
from verifier.interface import CHECKOUT, EXPORTER, UPSTREAM_PY  # noqa: E402

MODEL = "runs/dummy-kjjf3e3e_2026-08-11_13-51-44/final_model.keras"
OUT_DIR = Path(__file__).resolve().parents[1] / "results" / "processed"
UPSTREAM_FINAL_LOSS = 1.57e-10  # from baseline_local_lorentzian.log, epoch 100


def export(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (g_lorentzian, g_euclideanised) at points via the isolated env."""
    import os

    with tempfile.TemporaryDirectory(prefix="sb-disc-") as td:
        pin, pout, peuc = (Path(td) / n for n in ("p.npy", "g.npy", "ge.npy"))
        np.save(pin, points.astype(np.float64))
        env = dict(os.environ, WANDB_MODE="disabled")
        r = subprocess.run(
            [str(UPSTREAM_PY), str(EXPORTER), "--model", MODEL, "--points", str(pin),
             "--out", str(pout), "--euclidean-out", str(peuc)],
            cwd=CHECKOUT, capture_output=True, text=True, timeout=900, env=env,
        )
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-1500:])
        return np.load(pout), np.load(peuc)


def make_metric_fn(cache: dict[tuple, np.ndarray]):
    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]
    return g


def fd_ricci_at(points: np.ndarray, h: float) -> np.ndarray:
    """Independent FD Ricci at each point, batching ALL stencil evaluations into
    one exporter call."""
    from verifier.interface import RecordingMetric

    all_needed: list[tuple] = []
    seen = set()
    for x in points:
        rec = RecordingMetric(2)
        try:
            ricci_tensor(rec, x, h=h)
        except Exception:
            pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                all_needed.append(p)
    stencil = np.array(all_needed, dtype=np.float64)
    g_vals, _ = export(stencil)
    cache = {tuple(np.round(p, 12)): g_vals[i] for i, p in enumerate(stencil)}
    g = make_metric_fn(cache)
    return np.array([ricci_tensor(g, x, h=h) for x in points])


def upstream_loss_replica(points: np.ndarray, ricci: np.ndarray) -> float:
    """Exact upstream quantity with OUR independent Ricci substituted for theirs:
    mean_a | R_ij gE^ik gE^jl R_kl | * sqrt|det g|  (lambda=0)."""
    g_vals, ge_vals = export(points)
    per_point = []
    for a in range(len(points)):
        ge_inv = np.linalg.inv(ge_vals[a])
        contr = np.einsum("ij,ik,jl,kl->", ricci[a], ge_inv, ge_inv, ricci[a])
        vol = np.sqrt(abs(np.linalg.det(g_vals[a])))
        per_point.append(abs(contr) * vol)
    return float(np.mean(per_point))


def main() -> int:
    rng = np.random.default_rng(0)
    # training domain: single ball patch; sample radius <= 0.7 interior points
    r = 0.7 * np.sqrt(rng.uniform(0, 1, 24))
    th = rng.uniform(0, 2 * np.pi, 24)
    pts_interior = np.column_stack([r * np.cos(th), r * np.sin(th)])
    pts_edge = np.column_stack([0.95 * np.cos(th[:12]), 0.95 * np.sin(th[:12])])

    results: dict = {"model": MODEL, "upstream_final_loss": UPSTREAM_FINAL_LOSS}

    # B: FD step sweep (interior, 8 points to keep runtime sane)
    sweep_pts = pts_interior[:8]
    sweep = {}
    for h in [1e-2, 3e-3, 1e-3, 3e-4]:
        ric = fd_ricci_at(sweep_pts, h)
        sweep[str(h)] = {
            "max_abs_ricci": float(np.max(np.abs(ric))),
            "median_max_per_point": float(np.median(np.max(np.abs(ric), axis=(1, 2)))),
        }
    results["fd_step_sweep"] = sweep

    # main measurement at calibrated h
    h0 = 3e-3
    ric_int = fd_ricci_at(pts_interior, h0)
    ric_edge = fd_ricci_at(pts_edge, h0)

    per_point_max = np.max(np.abs(ric_int), axis=(1, 2))
    results["interior_h3e-3"] = {
        "n_points": len(pts_interior),
        "max_abs_ricci": float(per_point_max.max()),
        "median": float(np.median(per_point_max)),
        "p95": float(np.percentile(per_point_max, 95)),
        "frobenius_mean": float(np.mean(np.linalg.norm(ric_int, axis=(1, 2)))),
    }
    results["edge_h3e-3"] = {
        "n_points": len(pts_edge),
        "max_abs_ricci": float(np.max(np.abs(ric_edge))),
        "median": float(np.median(np.max(np.abs(ric_edge), axis=(1, 2)))),
    }

    # A/D: exact upstream quantity with our Ricci
    results["upstream_loss_replica_with_our_ricci"] = upstream_loss_replica(pts_interior, ric_int)
    results["sqrt_upstream_final_loss"] = float(np.sqrt(UPSTREAM_FINAL_LOSS))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "discrepancy_experiment.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
