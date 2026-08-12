# Limitations

See measured calibration limits (copied from verifier/CALIBRATION.md):
# Verifier calibration record

Date: 2026-08-11. Calibration performed on ANALYTIC baselines only — no AInstein
candidate had been evaluated before these values were fixed (roadmap §15: thresholds
may be set after baseline calibration but before inspecting candidate results).

## Finite-difference step-size sweep (Schwarzschild, M=1, x = (0, 8, 1.1, 0.3), float64)

| h     | max abs Ricci | Kretschmann rel. err |
|-------|---------------|----------------------|
| 1e-1  | 2.8e-04       | 5.2e-04              |
| 3e-2  | 2.2e-06       | 4.1e-06              |
| 1e-2  | 2.7e-08       | 5.0e-08              |
| 3e-3  | 8.7e-11       | 1.1e-09              |
| 1e-3  | 2.2e-09       | 1.1e-09              |
| 3e-4  | 2.0e-08       | 4.3e-08              |
| 1e-4  | 7.9e-08       | 2.5e-08              |

Interpretation: 4th-order nested central differences are truncation-dominated for
h ≳ 3e-3 and roundoff-dominated below; the sweet spot on O(1–25) coordinate scales is
**h = 3e-3** (set as the default in geometry.py).

## Predeclared tolerances (fixed 2026-08-11)

- `RICCI_VACUUM_TOL = 1e-7` — measured vacuum floor is ~1e-10..1e-9 at h=3e-3; ×100
  margin for point-to-point variation.
- `KRETSCHMANN_REL_TOL = 1e-7` — measured ~1e-9; ×100 margin.
- `PERTURBED_MIN_RESIDUAL = 1e-5` — the eps=1e-3 perturbed control produces residuals
  well above this; any candidate below the vacuum tolerance AND above this on controls
  region would be numerically distinguishable.

## Known limitations (honest)

- Calibration was done at 3 exterior points, r ∈ [6, 25], M=1. Near-horizon (r → 2M)
  behavior needs a separate calibration pass before candidate horizon claims.
- The numerical vacuum floor rises near coordinate singularities (θ → 0, π) — excluded
  domains must be mapped, not ignored (roadmap §15 check 15).
- These tolerances apply to THIS finite-difference route; the upstream autodiff route
  will have its own floor and must be cross-checked at selected points.
