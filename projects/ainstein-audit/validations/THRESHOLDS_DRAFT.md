# Validation thresholds — DRAFT (to be FROZEN before any candidate inspection)

Status: DRAFT. Per directive §6, these become frozen only after the Schwarzschild
known-answer baseline passes; freezing happens BEFORE looking at any Petrov-I
candidate output. All values trace to measured floors, not guesses.

## Measured floors (2026-08-11)

| Quantity | Route | Measured floor | Source |
| --- | --- | --- | --- |
| max\|Ricci\| vacuum floor | Schwarzschild coords, analytic, h=3e-3 | ~1e-10 | CALIBRATION.md |
| max\|Ricci\| vacuum floor | Penrose+stereo 4D route, analytic, h=3e-3 | 6.7e-9 … 1.5e-8 | known_answer_4d.json |
| Kretschmann rel. err | Penrose route, analytic | ≤1.2e-8 | known_answer_4d.json |
| NN-metric FD residual (2D, converged model) | float64 export | median 7.9e-6, p95 2.2e-5, max 5.7e-5 | calibration_maps.json |
| float32 storage penalty | 2D grid | 203× median inflation | calibration_maps.json |

## Proposed thresholds (NOT frozen; finalize after 4D baseline completes)

- Pipeline validity gate (per run): analytic-route max|Ricci| < 1e-7 AND
  Kretschmann rel. err < 1e-7 at all probe points, else the run's numbers are void.
- Candidate vacuum criterion (draft): normalized_independent_einstein_residual on
  hidden points ≤ the value achieved by the fully-trained Schwarzschild baseline
  under the SAME evaluation (same h, dtype, sampler), with convergence under
  precision/step sweep; signature Lorentzian on 100% of valid-domain probes.
- Negative control: deliberately perturbed metric must exceed the criterion by ≥10×.
- dtype: float64 everywhere; float32 anywhere voids the measurement (measured 203×).

## What must happen before freezing

1. Schwarzschild 4D baseline trains to completion (night CPU run or GPU).
2. Its converged NN-metric floor is measured on hidden points (median/p95/p99/max).
3. Thresholds above get numeric values from that measurement.
4. This file is renamed THRESHOLDS_FROZEN.md with a git tag, BEFORE any
   hps_petrovI_* output is generated or inspected.
