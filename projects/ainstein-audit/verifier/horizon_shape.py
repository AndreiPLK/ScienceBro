"""Locate the apparent horizon (Xi = 0) per model and compare horizon shapes.

For a set of fixed time slices T, bisect along X to find where Xi changes sign. The
analytic Schwarzschild horizon in these coordinates is the line X = |T|, so the control
must return X_h ~ T; any departure of a candidate's horizon from that line is a measured
difference in geometry rather than a difference in labelling.

Bisection needs a metric callable at arbitrary points, so each iteration exports a small
batch. To keep the number of exporter calls low, all time slices are bisected in lockstep:
one export per bisection round rather than one per slice.

Output: results/processed/horizon_shape.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.horizon import trapping_diagnostics  # noqa: E402
from verifier.horizon_run import export  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "horizon_shape.json"
H = 3e-3
Q = (0.1, 0.1)
SLICES = [0.10, 0.20, 0.30, 0.40, 0.50]
X_LO, X_HI = 0.06, 0.74
ROUNDS = 7          # 0.68 / 2^7 ~ 0.005 in X

MODELS = {
    "analytic": None,
    "nn_schwarzschild_baseline": str(PROJ / "results" / "raw" / "schwarzschild-4d-final-2026-08-12" / "final_model.keras"),
    "candidate_seed124": str(PROJ / "results" / "raw" / "petrovI-bh-run2" / "final_model.keras"),
    "candidate_seed123": str(PROJ / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras"),
}


def _xi_batch(model: str | None, probes: list[np.ndarray]) -> list[float | None]:
    """Xi at each probe, one exporter call for the whole batch."""
    pts = []
    for p in probes:
        pts.append(p)
        for a in (0, 1):
            for s in (+H, -H):
                q = p.copy()
                q[a] += s
                pts.append(q)
    arr = np.unique(np.round(np.array(pts, dtype=np.float64), 12), axis=0)
    vals = export(arr, model)
    cache = {tuple(np.round(p, 12)): vals[i] for i, p in enumerate(arr)}

    def g(x: np.ndarray) -> np.ndarray:
        return cache[tuple(np.round(x, 12))]

    out: list[float | None] = []
    for p in probes:
        try:
            out.append(float(trapping_diagnostics(g, p, h=H)["Xi"]))
        except Exception:
            out.append(None)
    return out


def horizon_for(model: str | None) -> dict:
    lo = {t: X_LO for t in SLICES}
    hi = {t: X_HI for t in SLICES}

    # verify the bracket: Xi should be negative at small X (trapped) and positive at large X
    probes = [np.array([t, X_LO, *Q]) for t in SLICES] + [np.array([t, X_HI, *Q]) for t in SLICES]
    xis = _xi_batch(model, probes)
    n = len(SLICES)
    bracket = {}
    for i, t in enumerate(SLICES):
        a, b = xis[i], xis[n + i]
        bracket[t] = None if a is None or b is None else (a < 0 < b)

    for _ in range(ROUNDS):
        mids = {t: 0.5 * (lo[t] + hi[t]) for t in SLICES if bracket.get(t)}
        if not mids:
            break
        probes = [np.array([t, x, *Q]) for t, x in mids.items()]
        xis = _xi_batch(model, probes)
        for (t, _x), xi in zip(mids.items(), xis, strict=True):
            if xi is None:
                bracket[t] = None
                continue
            if xi < 0:
                lo[t] = mids[t]
            else:
                hi[t] = mids[t]

    rows = []
    for t in SLICES:
        if not bracket.get(t):
            rows.append({"T": t, "status": "no sign change in the sampled range"})
            continue
        x_h = 0.5 * (lo[t] + hi[t])
        rows.append({"T": t, "X_horizon": x_h, "uncertainty": 0.5 * (hi[t] - lo[t]),
                     "X_analytic_expectation": t, "delta_from_analytic": x_h - t})
    return {"slices": rows}


def main() -> int:
    results: dict = {"date": "2026-08-12", "q": Q, "h": H, "bisection_rounds": ROUNDS,
                     "note": "Analytic Schwarzschild horizon in these coordinates is X = |T|; "
                             "delta_from_analytic is the measured departure from that line."}
    for name, model in MODELS.items():
        if model is not None and not Path(model).exists():
            results[name] = {"status": "checkpoint missing"}
            continue
        print(f"{name}: bisecting...", flush=True)
        results[name] = horizon_for(model)
        for r in results[name]["slices"]:
            if "X_horizon" in r:
                print(f"   T={r['T']:.2f}  X_h={r['X_horizon']:.3f} +-{r['uncertainty']:.3f}"
                      f"  (analytic {r['X_analytic_expectation']:.2f}, "
                      f"delta {r['delta_from_analytic']:+.3f})")
            else:
                print(f"   T={r['T']:.2f}  {r['status']}")
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
