"""EXP-0002 candidate evaluation against THRESHOLDS_FROZEN.md (tag thresholds-frozen).

Criteria (frozen 2026-08-12 03:40, before this candidate existed):
  1. pipeline validity: analytic route < 1e-7 (Ricci and Kretschmann rel err)
  2. vacuum comparability: hidden max|Ricci| median <= 0.286 AND p95 <= 0.573
  3. signature: Lorentzian + det<0 at 100% of hidden points
  4. convergence: median stable to <20% over h in {1e-3, 3e-3, 1e-2}
  5. float64 only (by construction of the exporter)
  6. negative control (amp 0.5 bump) must break criterion 2
Hidden seed: int(sha256(checkpoint)[:8], 16) mod 2^31 — deterministic, not tunable.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier import baseline_stress as bs  # noqa: E402
from verifier import known_answer_4d as ka  # noqa: E402
from verifier.geometry import ricci_tensor  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
MODEL = PROJ / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras"
OUT = PROJ / "results" / "processed" / "candidate_stress.json"

MEDIAN_LIMIT = 0.286
P95_LIMIT = 0.573


def hidden_points_for(seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    pts: list[np.ndarray] = []
    while len(pts) < bs.N_HIDDEN:
        t = rng.uniform(-0.25, 0.25)
        x = rng.uniform(0.40, 0.75)
        if np.cos(2 * t) / np.cos(2 * x) <= 1.05:
            continue
        q1, q2 = rng.uniform(-0.4, 0.4, 2)
        pts.append(np.array([t, x, q1, q2]))
    return pts


def ricci_stats(model: str, pts: list[np.ndarray], h: float, amp: float = 0.0) -> dict:
    ka.SNAPSHOT = model
    stencil4 = ka.stencil_for(pts) if h == bs.H else _stencil_h(pts, h)
    pts5 = np.hstack([stencil4, np.zeros((len(stencil4), 1))])
    values = ka.export(pts5, analytic=False)
    if amp:
        bump = np.array([0.0, 0.55, 0.1, 0.1])
        for i, p in enumerate(stencil4):
            d2 = float(np.sum((p - bump) ** 2))
            values[i] = values[i] + amp * np.exp(-d2 / 0.02) * np.eye(4)
    cache = {tuple(np.round(p, 12)): values[i] for i, p in enumerate(stencil4)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    arr, sig = [], []
    for x in pts:
        arr.append(float(np.max(np.abs(ricci_tensor(g, x, h=h)))))
        gm = g(x)
        eig = np.linalg.eigvalsh(gm)
        sig.append(bool(np.linalg.det(gm) < 0 and (eig < 0).sum() == 1))
    a = np.array(arr)
    return {"h": h, "median": float(np.median(a)), "p95": float(np.percentile(a, 95)),
            "p99": float(np.percentile(a, 99)), "max": float(a.max()),
            "signature_ok_fraction": float(np.mean(sig))}


def _stencil_h(pts: list[np.ndarray], h: float) -> np.ndarray:
    from verifier.interface import RecordingMetric

    seen, out = set(), []
    for x in pts:
        rec = RecordingMetric(4)
        try:
            ricci_tensor(rec, x, h=h)
        except Exception:
            pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return np.array(out, dtype=np.float64)


def main() -> int:
    sha = hashlib.sha256(MODEL.read_bytes()).hexdigest()
    seed = int(sha[:8], 16) % 2**31
    pts = hidden_points_for(seed)

    # criterion 1: pipeline validity (analytic route, 4 probes)
    analytic = ka.run_route(analytic=True)
    worst_r = max(r["max_abs_ricci"] for r in analytic["rows"])
    worst_k = max(r["kretschmann_rel_err"] for r in analytic["rows"])
    c1 = worst_r < 1e-7 and worst_k < 1e-7

    # criteria 2+3 at frozen h
    main_stats = ricci_stats(str(MODEL), pts, bs.H)
    c2 = main_stats["median"] <= MEDIAN_LIMIT and main_stats["p95"] <= P95_LIMIT
    c3 = main_stats["signature_ok_fraction"] == 1.0

    # criterion 4: convergence
    sweep = [ricci_stats(str(MODEL), pts, h) for h in (1e-3, 1e-2)]
    medians = [s["median"] for s in sweep] + [main_stats["median"]]
    c4_spread = (max(medians) - min(medians)) / max(min(medians), 1e-30)
    c4 = c4_spread < 0.20

    # criterion 6: negative control
    control = ricci_stats(str(MODEL), pts, bs.H, amp=0.5)
    c6 = not (control["median"] <= MEDIAN_LIMIT and control["p95"] <= P95_LIMIT)

    verdict = "PASS" if all([c1, c2, c3, c4, c6]) else (
        "FAIL" if (c1 and c4 and not (c2 and c3)) else "INCONCLUSIVE")

    results = {
        "date": "2026-08-12",
        "experiment": "EXP-0002",
        "model_sha256": sha,
        "hidden_seed": seed,
        "criteria": {
            "c1_pipeline_validity": {"pass": bool(c1), "worst_ricci": worst_r, "worst_k_rel": worst_k},
            "c2_vacuum_comparability": {"pass": bool(c2), "limits": [MEDIAN_LIMIT, P95_LIMIT]},
            "c3_signature": {"pass": bool(c3)},
            "c4_convergence": {"pass": bool(c4), "median_spread": c4_spread},
            "c5_float64": {"pass": True, "note": "exporter is float64-only"},
            "c6_negative_control": {"pass": bool(c6)},
        },
        "hidden_stats_h3e-3": main_stats,
        "h_sweep": sweep,
        "negative_control_amp0.5": control,
        "frozen_thresholds": "validations/THRESHOLDS_FROZEN.md @ tag thresholds-frozen",
        "verdict_under_frozen_criteria": verdict,
        "note": "PASS here means 'meets the frozen audit criteria relative to the reproduced "
                "Schwarzschild baseline'; it is NOT a confirmation of a new solution.",
    }
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
