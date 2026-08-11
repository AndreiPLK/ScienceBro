"""P1: full 4D known-answer pipeline (checkpoint → export → verifier → analytic).

Stage 1 — route validation: run the independent FD verifier on the ANALYTIC
Schwarzschild metric exported in the model's own (T, X, q1, q2) Penrose+stereo
coordinates. Establishes the numerical floor of the 4D route (Ricci ≈ 0,
K vs 48 m²/r⁶ with an independently computed r(T,X)).

Stage 2 — NN snapshot: identical checks on the interim 4D checkpoint
(EXPLORATORY: the model is partially trained; numbers are recorded, no claims).

Run: uv run python projects/ainstein-audit/verifier/known_answer_4d.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.geometry import (  # noqa: E402
    kretschmann_scalar,
    lorentzian_signature_ok,
    ricci_tensor,
)
from verifier.interface import CHECKOUT, EXPORTER, UPSTREAM_PY, RecordingMetric  # noqa: E402
from verifier.penrose import kretschmann_analytic, r_of_TX  # noqa: E402

SNAPSHOT = str(Path(__file__).resolve().parents[1]
               / "results" / "raw" / "schwarzschild-4d-interim-2026-08-11"
               / "final_model.keras")
OUT = Path(__file__).resolve().parents[1] / "results" / "processed" / "known_answer_4d.json"

# Exterior-region base points (T, X, q1, q2); BI: cos2T/cos2X > 1, away from
# horizon (X≈|T|) and from the Penrose boundary. Stereo coords well inside patch 0.
BASE_POINTS = [
    np.array([0.10, 0.60, 0.20, 0.10]),
    np.array([0.00, 0.50, -0.10, 0.30]),
    np.array([-0.15, 0.70, 0.00, 0.00]),
    np.array([0.05, 0.45, 0.25, -0.20]),
]
H = 3e-3


def export(points5: np.ndarray, analytic: bool) -> np.ndarray:
    import os

    with tempfile.TemporaryDirectory(prefix="sb-ka4d-") as td:
        pin, pout = Path(td) / "p.npy", Path(td) / "g.npy"
        np.save(pin, points5.astype(np.float64))
        cmd = [str(UPSTREAM_PY), str(EXPORTER), "--model", SNAPSHOT,
               "--points", str(pin), "--out", str(pout)]
        if analytic:
            cmd.append("--analytic")
        env = dict(os.environ, WANDB_MODE="disabled")
        r = subprocess.run(cmd, cwd=CHECKOUT, capture_output=True, text=True,
                           timeout=900, env=env)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-1500:])
        return np.load(pout)


def stencil_for(points: list[np.ndarray]) -> np.ndarray:
    seen, out = set(), []
    for x in points:
        rec = RecordingMetric(4)
        try:
            ricci_tensor(rec, x, h=H)
        except Exception:
            pass
        try:
            kretschmann_scalar(rec, x, h=H)
        except Exception:
            pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return np.array(out, dtype=np.float64)


def run_route(analytic: bool) -> dict:
    stencil4 = stencil_for(BASE_POINTS)
    pts = stencil4 if analytic else np.hstack(
        [stencil4, np.zeros((len(stencil4), 1))])  # patch 0 column for NN
    values = export(pts, analytic)
    cache = {tuple(np.round(p, 12)): values[i] for i, p in enumerate(stencil4)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    rows = []
    for x in BASE_POINTS:
        ric = ricci_tensor(g, x, h=H)
        k = kretschmann_scalar(g, x, h=H)
        k_true = kretschmann_analytic(x[0], x[1])
        rows.append({
            "point_TXq1q2": [float(v) for v in x],
            "r_independent": float(r_of_TX(x[0], x[1])),
            "lorentzian_signature": bool(lorentzian_signature_ok(g, x)),
            "max_abs_ricci": float(np.max(np.abs(ric))),
            "kretschmann_fd": float(k),
            "kretschmann_analytic_48m2_r6": float(k_true),
            "kretschmann_rel_err": float(abs(k - k_true) / k_true),
        })
    return {"n_stencil_points": int(len(stencil4)), "rows": rows}


def main() -> int:
    results = {
        "date": "2026-08-11",
        "snapshot": SNAPSHOT,
        "note_stage2": "interim checkpoint, ~31/500 epochs — EXPLORATORY, no claims",
        "analytic_route": run_route(analytic=True),
        "nn_interim": run_route(analytic=False),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
