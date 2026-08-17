"""Hidden-point stress test of the trained NN-Schwarzschild baseline (EXP-0001).

Runs AFTER the 500-epoch run completes. Hidden points: freshly seeded (seed 20260812),
documented here BEFORE any results are seen, never used in any training or tuning.

Measures (per EXP-0001 analysis plan):
  - independent FD max|Ricci| distribution: median/p95/p99/max over hidden points
  - Kretschmann vs analytic 48 m^2/r^6 (independent Lambert-W r(T,X)): rel err stats
  - Lorentzian signature + determinant sign at every hidden point
  - negative control: same checks on a deliberately perturbed copy of the metric grid
Outputs: results/processed/baseline_stress.json (+ figure HTML).
Run: uv run python projects/ainstein-audit/verifier/baseline_stress.py <run_dir_name>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier import known_answer_4d as ka  # noqa: E402
from verifier.geometry import kretschmann_scalar, ricci_tensor  # noqa: E402
from verifier.penrose import kretschmann_analytic  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "baseline_stress.json"
H = 3e-3
N_HIDDEN = 24
SEED = 20260812  # frozen before results are seen


def hidden_points() -> list[np.ndarray]:
    """Exterior-region (T,X) with |T|<0.25, X in [0.4,0.75]; stereo |q|<0.4; patch 0.
    Region chosen to match the training domain interior, away from horizon/boundary,
    same criteria as the analytic-route validation."""
    rng = np.random.default_rng(SEED)
    pts = []
    while len(pts) < N_HIDDEN:
        T = rng.uniform(-0.25, 0.25)
        X = rng.uniform(0.40, 0.75)
        if np.cos(2 * T) / np.cos(2 * X) <= 1.05:  # keep clearly exterior
            continue
        q1, q2 = rng.uniform(-0.4, 0.4, 2)
        pts.append(np.array([T, X, q1, q2]))
    return pts


def evaluate(model_path: str, points: list[np.ndarray], perturb: bool = False) -> dict:
    ka.SNAPSHOT = model_path
    stencil4 = ka.stencil_for(points)
    pts5 = np.hstack([stencil4, np.zeros((len(stencil4), 1))])
    values = ka.export(pts5, analytic=False)
    if perturb:
        bump = np.array([0.0, 0.55, 0.1, 0.1])
        for i, p in enumerate(stencil4):
            d2 = float(np.sum((p - bump) ** 2))
            values[i] = values[i] + 0.05 * np.exp(-d2 / 0.02) * np.eye(4)
    cache = {tuple(np.round(p, 12)): values[i] for i, p in enumerate(stencil4)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    ricci_max, k_rel, sig_ok, det_neg = [], [], [], []
    for x in points:
        ric = ricci_tensor(g, x, h=H)
        k = kretschmann_scalar(g, x, h=H)
        kt = kretschmann_analytic(x[0], x[1])
        gm = g(x)
        eig = np.linalg.eigvalsh(gm)
        ricci_max.append(float(np.max(np.abs(ric))))
        k_rel.append(float(abs(k - kt) / kt))
        sig_ok.append(bool(np.linalg.det(gm) < 0 and (eig < 0).sum() == 1))
        det_neg.append(bool(np.linalg.det(gm) < 0))
    arr = np.array(ricci_max)
    kre = np.array(k_rel)
    return {
        "n_points": len(points),
        "ricci_median": float(np.median(arr)),
        "ricci_p95": float(np.percentile(arr, 95)),
        "ricci_p99": float(np.percentile(arr, 99)),
        "ricci_max": float(arr.max()),
        "kretschmann_rel_median": float(np.median(kre)),
        "kretschmann_rel_p95": float(np.percentile(kre, 95)),
        "kretschmann_rel_max": float(kre.max()),
        "signature_ok_fraction": float(np.mean(sig_ok)),
        "det_negative_fraction": float(np.mean(det_neg)),
        "per_point_ricci_max": [float(v) for v in arr],
    }


def main() -> int:
    run_dir = sys.argv[1]
    model = str(PROJ / "upstream" / "checkout" / "runs" / run_dir / "final_model.keras")
    import hashlib

    sha = hashlib.sha256(Path(model).read_bytes()).hexdigest()
    pts = hidden_points()
    results = {
        "date": "2026-08-12",
        "experiment": "EXP-0001",
        "model": model,
        "model_sha256": sha,
        "hidden_seed": SEED,
        "h": H,
        "trained": evaluate(model, pts, perturb=False),
        "negative_control_perturbed": evaluate(model, pts, perturb=True),
    }
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                k: v
                for k, v in results.items()
                if k not in ("trained", "negative_control_perturbed")
            },
            indent=2,
        )
    )
    print(
        "trained:",
        json.dumps(
            {k: v for k, v in results["trained"].items() if k != "per_point_ricci_max"}, indent=2
        ),
    )
    print(
        "control:",
        json.dumps(
            {
                k: v
                for k, v in results["negative_control_perturbed"].items()
                if k != "per_point_ricci_max"
            },
            indent=2,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
