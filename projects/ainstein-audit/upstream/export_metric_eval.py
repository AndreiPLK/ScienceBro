"""Neutral metric-export interface — UPSTREAM SIDE (roadmap §15 Day 2).

This script runs inside the isolated upstream environment and MAY import upstream
code (allowed: "may read exported metrics, coordinates, parameters, and checkpoints").
It evaluates a trained model's METRIC COMPONENTS at requested coordinates and writes
plain float64 arrays. The independent verifier consumes only those arrays and never
imports this module or anything upstream.

Usage (from projects/ainstein-audit/upstream/checkout):
  ../.venv-upstream/Scripts/python.exe ../export_metric_eval.py \
      --model runs/<run>/final_model.keras --points points.npy --out metrics.npy

points.npy: (N, in_dim) float64 coordinates.
out: (N, d, d) float64 metric components g_ab at each point.
meta (out.json): model class, in_dim, d, lorentzian flag, model file sha256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--points", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(Path.cwd()))  # upstream checkout root

    import numpy as np
    import tensorflow as tf

    # Importing upstream network module registers the custom Keras classes.
    import network.schwarzschild  # noqa: F401
    from helper_functions.helper_functions import cholesky_from_vec

    model = tf.keras.models.load_model(args.model, compile=False)
    cfg = model.get_config().get("model_config", {})
    lorentzian = bool(cfg.get("model_specific", {}).get("lorentzian", True))

    pts = np.load(args.points).astype(np.float64)
    vec = model(tf.constant(pts, dtype=tf.float64))
    g = cholesky_from_vec(vec, lorentzian=lorentzian).numpy().astype(np.float64)

    np.save(args.out, g)
    meta = {
        "model_file": args.model,
        "model_sha256": hashlib.sha256(Path(args.model).read_bytes()).hexdigest(),
        "model_class": type(model).__name__,
        "n_points": int(pts.shape[0]),
        "in_dim": int(pts.shape[1]),
        "metric_dim": int(g.shape[-1]),
        "lorentzian": lorentzian,
        "raw_output_dim": int(np.array(vec).shape[-1]),
    }
    Path(args.out).with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
