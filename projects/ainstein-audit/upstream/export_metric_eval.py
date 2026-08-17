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
    ap.add_argument(
        "--euclidean-out",
        dest="euclidean_out",
        default=None,
        help="also save the Euclideanised metric (lorentzian=False Cholesky)",
    )
    ap.add_argument(
        "--analytic",
        action="store_true",
        help="ignore --model weights; export the upstream ANALYTIC Schwarzschild "
        "metric (geometry.AnalyticMetric_R2S2, m=1) at the same (T,X,q1,q2) "
        "coordinates — used to validate the 4D verifier route",
    )
    args = ap.parse_args()

    sys.path.insert(0, str(Path.cwd()))  # upstream checkout root

    # Importing upstream network module registers the custom Keras classes.
    import network.schwarzschild  # noqa: F401
    import numpy as np
    import tensorflow as tf
    from helper_functions.helper_functions import cholesky_from_vec

    pts = np.load(args.points).astype(np.float64)

    if args.analytic:
        from geometry.schwarzschild import AnalyticMetric_R2S2

        q4 = tf.constant(pts[:, :4], dtype=tf.float64)
        g = AnalyticMetric_R2S2(q4, identity=False, lorentzian=True, m=1.0)
        g = np.asarray(g).astype(np.float64)
        np.save(args.out, g)
        meta = {
            "model_file": "ANALYTIC Schwarzschild (upstream geometry, m=1)",
            "model_class": "AnalyticMetric_R2S2",
            "n_points": int(pts.shape[0]),
            "in_dim": int(pts.shape[1]),
            "metric_dim": int(g.shape[-1]),
            "lorentzian": True,
        }
        Path(args.out).with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(json.dumps(meta))
        return 0

    model = tf.keras.models.load_model(args.model, compile=False)
    cfg = model.get_config().get("model_config", {})
    lorentzian = bool(cfg.get("model_specific", {}).get("lorentzian", True))
    vec = model(tf.constant(pts, dtype=tf.float64))
    cls = type(model).__name__

    if cls == "SchwarzschildGlobalModel":
        # 4D embedding architecture (network/schwarzschild.py):
        # inputs (N,5) = [T, X, q1, q2, patch_idx]; model returns 15 Cholesky
        # components of the 5D ambient metric. Pull back to the 4D intrinsic
        # metric with the analytic embedding Jacobian, exactly as
        # SchwarzschildSupervisedWrapper.call does.
        from geometry.schwarzschild import embedding_jacobian_stereo

        q4 = tf.constant(pts[:, :4], dtype=tf.float64)
        patch_idx = tf.cast(tf.constant(pts[:, 4]), tf.int32)
        g5 = cholesky_from_vec(vec, lorentzian=lorentzian)  # (N,5,5)
        jac = embedding_jacobian_stereo(q4, patch_idx)  # (N,5,4)
        g = tf.einsum("sAB,sAm,sBn->smn", g5, jac, jac).numpy().astype(np.float64)
    else:
        # Direct local models: output is the Cholesky vector of the metric itself.
        g = cholesky_from_vec(vec, lorentzian=lorentzian).numpy().astype(np.float64)

    np.save(args.out, g)
    if args.euclidean_out:
        # Euclideanised variant used by the upstream loss contraction
        # (losses/schwarzschild.py:1949): same Cholesky vector, lorentzian=False.
        ge = cholesky_from_vec(vec, lorentzian=False).numpy().astype(np.float64)
        np.save(args.euclidean_out, ge)
    meta = {
        "model_file": args.model,
        "model_sha256": hashlib.sha256(Path(args.model).read_bytes()).hexdigest(),
        "model_class": cls,
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
