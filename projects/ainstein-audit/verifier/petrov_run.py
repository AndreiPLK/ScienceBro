"""Run the independent Petrov diagnostics on the candidates and the baseline.

Answers the question the frozen vacuum criteria cannot answer: is a candidate
algebraically GENERAL (Petrov type I, i.e. genuinely not Schwarzschild/Kerr-like),
or is it algebraically special (S = 1) and therefore not a new algebraic type?

Reference points:
  - analytic Schwarzschild (type D): S must be 1 -> validates the pipeline per point
  - reproduced NN Schwarzschild baseline: how far a *trained* type-D approximation
    lands from S = 1 with our finite differences (this is the noise floor for the
    claim "S differs from 1")
  - candidates seed 123 / 124

Output: results/processed/petrov_diagnostics.json
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
from verifier.known_metrics import schwarzschild  # noqa: E402
from verifier.petrov import petrov_invariants  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "petrov_diagnostics.json"
H = 3e-3

MODELS = {
    "nn_schwarzschild_baseline": PROJ
    / "results"
    / "raw"
    / "schwarzschild-4d-final-2026-08-12"
    / "final_model.keras",
    "candidate_seed123": PROJ / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras",
    "candidate_seed124": PROJ / "results" / "raw" / "petrovI-bh-run2" / "final_model.keras",
}

# exterior probe points (T, X, q1, q2), same family as the analytic validation
POINTS = [
    np.array([0.10, 0.60, 0.20, 0.10]),
    np.array([0.00, 0.50, -0.10, 0.30]),
    np.array([-0.15, 0.70, 0.00, 0.00]),
    np.array([0.05, 0.45, 0.25, -0.20]),
]


def stencil_for_petrov(points: list[np.ndarray]) -> np.ndarray:
    seen, out = set(), []
    for x in points:
        rec = RecordingMetric(4)
        for fn in (ricci_tensor, petrov_invariants):
            try:
                fn(rec, x, h=H)
            except Exception:
                pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return np.array(out, dtype=np.float64)


def evaluate_model(path: Path) -> list[dict]:
    ka.SNAPSHOT = str(path)
    stencil = stencil_for_petrov(POINTS)
    pts5 = np.hstack([stencil, np.zeros((len(stencil), 1))])
    values = ka.export(pts5, analytic=False)
    cache = {tuple(np.round(p, 12)): values[i] for i, p in enumerate(stencil)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    rows = []
    for x in POINTS:
        try:
            inv = petrov_invariants(g, x, h=H)
            rows.append(
                {
                    "point": [float(v) for v in x],
                    "S_real": float(np.real(inv["S"])),
                    "S_imag": float(np.imag(inv["S"])),
                    "abs_S_minus_1": inv["abs_S_minus_1"],
                    "abs_I": float(abs(inv["I"])),
                    "abs_J": float(abs(inv["J"])),
                    "weyl_scale": inv["weyl_scale"],
                }
            )
        except Exception as exc:  # keep failures visible, never silently skip
            rows.append({"point": [float(v) for v in x], "error": str(exc)[:200]})
    return rows


def main() -> int:
    results: dict = {
        "date": "2026-08-12",
        "h": H,
        "definition": "S = 27 J^2 / (4 I^3); S = 1 <=> algebraically special",
        "known_answer": {},
    }

    # per-point known answer on the analytic metric (Schwarzschild coords)
    for r in (8.0, 12.0):
        inv = petrov_invariants(schwarzschild, np.array([0.0, r, 1.1, 0.3]), h=H)
        results["known_answer"][f"analytic_schwarzschild_r{r:.0f}"] = {
            "S_real": float(np.real(inv["S"])),
            "abs_S_minus_1": inv["abs_S_minus_1"],
        }

    for name, path in MODELS.items():
        if not path.exists():
            results[name] = {"status": "checkpoint missing"}
            continue
        import hashlib

        results[name] = {
            "model_sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:32],
            "rows": evaluate_model(path),
        }

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
