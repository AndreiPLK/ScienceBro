"""Verifier-side bridge to exported metrics (roadmap §15 Day 2, independence contract).

The verifier never imports upstream code. It talks to a trained checkpoint only via
the batch exporter script (which runs in the isolated upstream environment) using a
record → export → replay scheme:

1. RecordingMetric: run the FD geometry once with a recorder that logs every
   coordinate the computation requests (returning zeros).
2. Batch-evaluate all recorded points through export_metric_eval.py (subprocess).
3. TabulatedMetric: replay the same computation with exact tabulated values.

Determinism note: the FD stencil point set depends only on (x, h, dim), so record
and replay request identical points.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

UPSTREAM_DIR = Path(__file__).resolve().parents[1] / "upstream"
UPSTREAM_PY = UPSTREAM_DIR / ".venv-upstream" / "Scripts" / "python.exe"
EXPORTER = UPSTREAM_DIR / "export_metric_eval.py"
CHECKOUT = UPSTREAM_DIR / "checkout"


class RecordingMetric:
    """Metric stand-in that records requested points and returns zeros-like data."""

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.points: list[tuple[float, ...]] = []
        self._seen: set[tuple[float, ...]] = set()

    def __call__(self, x: np.ndarray) -> np.ndarray:
        key = tuple(np.round(np.asarray(x, dtype=np.float64), 12))
        if key not in self._seen:
            self._seen.add(key)
            self.points.append(key)
        # Identity-like placeholder keeps linalg.inv from failing during recording.
        return np.eye(self.dim)


class TabulatedMetric:
    """Replays exported metric values; raises on any unrecorded point."""

    def __init__(self, table: dict[tuple[float, ...], np.ndarray]) -> None:
        self.table = table

    def __call__(self, x: np.ndarray) -> np.ndarray:
        key = tuple(np.round(np.asarray(x, dtype=np.float64), 12))
        if key not in self.table:
            raise KeyError(f"point {key} was not in the exported table")
        return self.table[key]


def export_points(model_path: str, points: np.ndarray) -> tuple[np.ndarray, dict]:
    """Evaluate metric components at `points` via the isolated upstream env."""
    if not UPSTREAM_PY.exists():
        raise RuntimeError(f"upstream venv missing: {UPSTREAM_PY}")
    with tempfile.TemporaryDirectory(prefix="sb-export-") as td:
        pin = Path(td) / "points.npy"
        pout = Path(td) / "metrics.npy"
        np.save(pin, points.astype(np.float64))
        import os

        env = dict(os.environ, WANDB_MODE="disabled")
        r = subprocess.run(
            [
                str(UPSTREAM_PY),
                str(EXPORTER),
                "--model",
                model_path,
                "--points",
                str(pin),
                "--out",
                str(pout),
            ],
            cwd=CHECKOUT,
            capture_output=True,
            text=True,
            timeout=600,
            env=env,
        )
        if r.returncode != 0:
            raise RuntimeError(f"exporter failed:\n{r.stderr[-2000:]}")
        values = np.load(pout)
        meta = json.loads(pout.with_suffix(".json").read_text(encoding="utf-8"))
    return values, meta


def tabulated_metric_for(
    model_path: str,
    compute,
    x: np.ndarray,
    dim: int,
    extra_cols: list[float] | None = None,
    **kwargs,
):
    """Record the stencil of `compute(g, x, **kwargs)`, export it, and return
    (result, meta) computed on the tabulated exported metric.

    `compute` is any verifier geometry function taking (g, x, ...).
    `extra_cols`: constant columns appended to every exported point but NOT part of
    the differentiated coordinates (e.g. the patch index of the 4D embedding model,
    whose exporter expects (T, X, q1, q2, patch_idx)).
    """
    rec = RecordingMetric(dim)
    try:
        compute(rec, x, **kwargs)
    except Exception:
        # Recording pass may fail numerically on placeholder data; points are
        # still recorded, which is all we need.
        pass
    pts = np.array(rec.points, dtype=np.float64)
    export_pts = pts
    if extra_cols:
        extra = np.tile(np.asarray(extra_cols, dtype=np.float64), (len(pts), 1))
        export_pts = np.hstack([pts, extra])
    values, meta = export_points(model_path, export_pts)
    table = {tuple(p): values[i] for i, p in enumerate(np.round(pts, 12))}
    result = compute(TabulatedMetric(table), x, **kwargs)
    return result, meta
