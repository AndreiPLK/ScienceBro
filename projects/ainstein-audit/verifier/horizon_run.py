"""Run the independent trapping diagnostics on the analytic control and the models.

Grid spans exterior and interior Penrose regions at fixed angular point, so the
Xi = 0 boundary (apparent horizon) can be located per model rather than assumed.

Output: results/processed/horizon_diagnostics.json
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.horizon import trapping_diagnostics  # noqa: E402
from verifier.interface import CHECKOUT, EXPORTER, UPSTREAM_PY  # noqa: E402
from verifier.penrose import r_of_TX  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "horizon_diagnostics.json"
H = 3e-3
Q = (0.1, 0.1)

MODELS = {
    "nn_schwarzschild_baseline": PROJ / "results" / "raw" / "schwarzschild-4d-final-2026-08-12" / "final_model.keras",
    "candidate_seed123": PROJ / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras",
    "candidate_seed124": PROJ / "results" / "raw" / "petrovI-bh-run2" / "final_model.keras",
}


def probe_points() -> list[np.ndarray]:
    """Points from deep exterior to deep interior along the Penrose block."""
    combos = [
        (0.00, 0.65), (0.05, 0.55), (0.10, 0.45), (0.15, 0.35),   # exterior side
        (0.30, 0.28), (0.40, 0.22), (0.45, 0.30), (0.50, 0.25),   # near the diagonal
        (0.55, 0.20), (0.60, 0.10), (0.65, 0.05), (0.55, 0.35),   # interior side
    ]
    return [np.array([t, x, *Q]) for t, x in combos]


def stencil(points: list[np.ndarray]) -> np.ndarray:
    out = []
    for p in points:
        out.append(p)
        for a in (0, 1):
            for s in (+H, -H):
                q = p.copy()
                q[a] += s
                out.append(q)
    return np.unique(np.round(np.array(out, dtype=np.float64), 12), axis=0)


def export(pts: np.ndarray, model: str | None) -> np.ndarray:
    with tempfile.TemporaryDirectory(prefix="sb-hor-") as td:
        pin, pout = Path(td) / "p.npy", Path(td) / "g.npy"
        arr = pts if model is None else np.hstack([pts, np.zeros((len(pts), 1))])
        np.save(pin, arr)
        cmd = [str(UPSTREAM_PY), str(EXPORTER), "--model", model or "x",
               "--points", str(pin), "--out", str(pout)]
        if model is None:
            cmd.append("--analytic")
        r = subprocess.run(cmd, cwd=CHECKOUT, capture_output=True, text=True,
                           timeout=1800, env=dict(os.environ, WANDB_MODE="disabled"))
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-1200:])
        return np.load(pout)


def evaluate(model: str | None) -> list[dict]:
    pts = probe_points()
    st = stencil(pts)
    vals = export(st, model)
    cache = {tuple(np.round(p, 12)): vals[i] for i, p in enumerate(st)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    rows = []
    for p in pts:
        row: dict = {"T": float(p[0]), "X": float(p[1]),
                     "r_analytic_LambertW": float(r_of_TX(p[0], p[1])),
                     "region_analytic": "interior" if abs(np.cos(2 * p[0]) / np.cos(2 * p[1])) < 1.0
                                        else "exterior"}
        try:
            row.update(trapping_diagnostics(g, p, h=H))
        except Exception as exc:
            row["error"] = str(exc)[:200]
        rows.append(row)
    return rows


def main() -> int:
    results: dict = {"date": "2026-08-12", "h": H, "q": Q,
                     "definition": "Xi = h^ab d_a R d_b R in the 2D block; Xi<0 and both "
                                   "null dR<0 => future-trapped",
                     "analytic_control": evaluate(None)}
    for name, path in MODELS.items():
        if not path.exists():
            results[name] = {"status": "checkpoint missing"}
            continue
        results[name] = {
            "model_sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:32],
            "rows": evaluate(str(path)),
        }
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

    def summarise(rows: list[dict]) -> str:
        ok = [r for r in rows if "Xi" in r]
        tr = [r for r in ok if r["classification"] == "future-trapped"]
        at = [r for r in ok if r["classification"].startswith("past")]
        un = [r for r in ok if r["classification"] == "untrapped"]
        return f"{len(tr)} future-trapped, {len(at)} anti-trapped, {len(un)} untrapped (of {len(ok)})"

    print("analytic_control:", summarise(results["analytic_control"]))
    for name in MODELS:
        if "rows" in results.get(name, {}):
            print(f"{name}:", summarise(results[name]["rows"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
