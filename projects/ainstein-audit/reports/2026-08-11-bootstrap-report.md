# Bootstrap report — 2026-08-11

## What was independently verified today (facts, with commands)

1. **Verifier known-answer suite passes** (`uv run pytest projects/ainstein-audit/verifier -q`):
   Minkowski and Schwarzschild vacuum to |R_ab| < 1e-7 (measured floor ~1e-10 at h=3e-3),
   Kretschmann matches 48M²/r⁶ to <1e-7 relative, perturbed non-solution detected,
   invalid signature detected. Calibration: `verifier/CALIBRATION.md`.
2. **Upstream pipeline executes** (exit 0): smallest documented config
   (`hps_local_lorentzian.yaml`, 100 epochs, CPU, float64), final upstream loss 1.57e-10.
   Run record: `experiments/runs/RUN-BASELINE-SMOKE-2026-08-11.yaml` (artifacts hashed).
3. **Neutral export interface works end-to-end**: checkpoint → isolated-env exporter →
   plain arrays → independent FD geometry, zero upstream imports in the verifier.
   Smoke model metric is symmetric and 2D-Lorentzian at all probed points.

## First honest observation (NOT a claim)

Independent FD Ricci of the smoke model at (0.1, 0.2): max |R_ab| ≈ 3.3e-6,
while the upstream training loss ended at ~1.6e-10.

We do NOT conclude anything from this yet, because:
- the FD floor for wiggly NN metrics is uncalibrated (analytic-metric floor ~1e-10
  does not transfer automatically);
- the upstream dim-2 objective is normalized/integrated differently from raw |R_ab|;
- this smoke model is NOT a paper candidate (dim-2 local toy, 100 epochs).

This discrepancy is exactly what H-0001's convergence checks are designed to resolve.

## Open blockers

- No published candidate checkpoints in the repo (only supervised seed models):
  candidates must be re-trained locally (hps_petrovI_*.yaml) or requested from authors.
- AInstein license conflict: LICENSE=GPL-2.0 vs pyproject=MIT (question for authors).
- TF is CPU-only on native Windows; long 4D trainings may need WSL2.

## Next scientific step

Train/evaluate the 4D Schwarzschild known-answer case (`hps_schwarzschild.yaml`) and
push it through the same export → independent-verifier path; calibrate the NN-metric
FD floor on it. Then the candidate search configs.
