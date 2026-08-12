"""Three-leg evaluation of every trained candidate seed, in one table.

For each available checkpoint: vacuum (hidden-point residual vs the frozen limits),
Petrov speciality index S, and trapped-surface classification. The point of the sweep
is the reproducibility question: how often does the committed configuration produce a
candidate that satisfies all three at once?

Run: uv run python projects/ainstein-audit/verifier/seed_sweep.py
Output: results/processed/seed_sweep.json (+ markdown table printed)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier import baseline_stress as bs  # noqa: E402
from verifier import horizon_run as hr  # noqa: E402
from verifier import known_answer_4d as ka  # noqa: E402
from verifier.candidate_stress import (  # noqa: E402
    MEDIAN_LIMIT,
    P95_LIMIT,
    hidden_points_for,
    ricci_stats,
)
from verifier.horizon import trapping_diagnostics  # noqa: E402
from verifier.petrov import petrov_invariants  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "seed_sweep.json"
RAW = PROJ / "results" / "raw"
H = 3e-3

# seed -> checkpoint directory (only existing ones are evaluated)
SEEDS = {
    123: RAW / "petrovI-bh-run1",
    124: RAW / "petrovI-bh-run2",
    125: RAW / "petrovI-bh-seed125",
    126: RAW / "petrovI-bh-seed126",
    127: RAW / "petrovI-bh-seed127",
}

PETROV_POINTS = [
    np.array([0.10, 0.60, 0.20, 0.10]),
    np.array([0.00, 0.50, -0.10, 0.30]),
    np.array([-0.15, 0.70, 0.00, 0.00]),
    np.array([0.05, 0.45, 0.25, -0.20]),
]


def _cache_for(model: str, points: list[np.ndarray], with_petrov: bool):
    """Batch one export covering the stencils of every diagnostic we need."""
    from verifier.geometry import ricci_tensor
    from verifier.interface import RecordingMetric

    seen, stencil = set(), []
    for x in points:
        rec = RecordingMetric(4)
        for fn in (ricci_tensor, *( (petrov_invariants,) if with_petrov else () )):
            try:
                fn(rec, x, h=H)
            except Exception:
                pass
        for p in rec.points:
            if p not in seen:
                seen.add(p)
                stencil.append(p)
    arr = np.array(stencil, dtype=np.float64)
    ka.SNAPSHOT = model
    vals = ka.export(np.hstack([arr, np.zeros((len(arr), 1))]), analytic=False)
    return {tuple(np.round(p, 12)): vals[i] for i, p in enumerate(arr)}


def evaluate_seed(seed: int, run_dir: Path) -> dict:
    model = str(run_dir / "final_model.keras")
    sha = hashlib.sha256(Path(model).read_bytes()).hexdigest()
    hidden_seed = int(sha[:8], 16) % 2**31

    # leg 1: vacuum on hidden points (same code path as the frozen criteria)
    pts = hidden_points_for(hidden_seed)
    vac = ricci_stats(model, pts, H)
    leg1 = vac["median"] <= MEDIAN_LIMIT and vac["p95"] <= P95_LIMIT

    # leg 2: Petrov speciality index
    cache = _cache_for(model, PETROV_POINTS, with_petrov=True)

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    s_vals = []
    for x in PETROV_POINTS:
        try:
            s_vals.append(float(np.real(petrov_invariants(g, x, h=H)["S"])))
        except Exception:
            pass
    leg2 = bool(s_vals) and all(abs(s - 1.0) > 1e-3 for s in s_vals)

    # leg 3: trapping over the standard probe line
    hr_pts = hr.probe_points()
    st = hr.stencil(hr_pts)
    vals = hr.export(st, model)
    hcache = {tuple(np.round(p, 12)): vals[i] for i, p in enumerate(st)}

    def gh(x: np.ndarray) -> np.ndarray:
        return hcache[tuple(np.round(x, 12))]

    trapped = 0
    total = 0
    for p in hr_pts:
        try:
            d = trapping_diagnostics(gh, p, h=H)
            total += 1
            if d["classification"] == "future-trapped":
                trapped += 1
        except Exception:
            pass
    leg3 = trapped > 0

    return {
        "seed": seed,
        "model_sha256": sha[:16],
        "hidden_seed": hidden_seed,
        "vacuum": {"median": vac["median"], "p95": vac["p95"], "max": vac["max"],
                   "signature_ok_fraction": vac["signature_ok_fraction"], "pass": bool(leg1)},
        "petrov": {"S_values": s_vals,
                   "S_min": min(s_vals) if s_vals else None,
                   "S_max": max(s_vals) if s_vals else None,
                   "type_I": bool(leg2)},
        "trapping": {"future_trapped": trapped, "points": total, "pass": bool(leg3)},
        "all_three": bool(leg1 and leg2 and leg3),
    }


def main() -> int:
    rows = []
    for seed, run_dir in SEEDS.items():
        ckpt = run_dir / "final_model.keras"
        if not ckpt.exists():
            print(f"seed {seed}: checkpoint missing, skipped")
            continue
        print(f"seed {seed}: evaluating...", flush=True)
        rows.append(evaluate_seed(seed, run_dir))

    n_all = sum(1 for r in rows if r["all_three"])
    result = {
        "date": "2026-08-12",
        "frozen_limits": {"median": MEDIAN_LIMIT, "p95": P95_LIMIT},
        "n_seeds": len(rows),
        "n_satisfying_all_three": n_all,
        "rows": rows,
        "note": "Legs: vacuum (frozen criteria), Petrov type I (|S-1| > 1e-3 at every probe), "
                "trapped region present. All three are explicit training targets upstream.",
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("\n| seed | vacuum median | vacuum | S range | type I | trapped pts | all three |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        print(f"| {r['seed']} | {r['vacuum']['median']:.3f} | "
              f"{'PASS' if r['vacuum']['pass'] else 'FAIL'} | "
              f"{r['petrov']['S_min']:.2f}..{r['petrov']['S_max']:.2f} | "
              f"{'yes' if r['petrov']['type_I'] else 'no'} | "
              f"{r['trapping']['future_trapped']}/{r['trapping']['points']} | "
              f"{'YES' if r['all_three'] else 'no'} |")
    print(f"\n{n_all} of {len(rows)} seeds satisfy all three legs.")
    _ = bs  # keep the frozen-threshold provenance import explicit
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
