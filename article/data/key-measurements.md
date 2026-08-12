# Key measured results (single source of truth for article numbers)

All values measured on 2026-08-11, Windows 11, Python 3.12, float64, RTX 4070 SUPER
(TF CPU-only on native Windows). Sources in parentheses are repository artifacts.

## Independent verifier calibration (analytic known answers)

| Quantity | Value | Source |
| --- | --- | --- |
| Vacuum floor, Schwarzschild coords, h=3e-3 | max abs Ricci ~ 8.7e-11 | verifier/CALIBRATION.md |
| Optimal FD step (4th-order nested central differences) | h = 3e-3 | step sweep, CALIBRATION.md |
| Kretschmann vs 48M^2/r^6 (Schwarzschild coords) | rel. err ~ 1.1e-9 | CALIBRATION.md |
| Vacuum floor, Penrose+stereo 4D route | 6.7e-9 … 1.5e-8 | known_answer_4d.json |
| Kretschmann vs analytic (independent Lambert-W r(T,X)) | rel. err 4.4e-9 … 1.2e-8 | known_answer_4d.json |
| Verifier self-test | 17/17 passed | verifier_selftest.json |

## The loss-scale discrepancy (resolved)

| Quantity | Value | Source |
| --- | --- | --- |
| Upstream final training loss (2D smoke model) | 1.57e-10 | training log |
| Independent FD max abs Ricci (same model) | 1.26e-5 | discrepancy_experiment.json |
| sqrt(upstream loss) vs our Ricci | 1.253e-5 vs 1.261e-5 (0.7% apart) | discrepancy_experiment.json |
| Upstream loss formula replicated with OUR Ricci | 8.08e-11 vs 1.57e-10 (factor 1.94) | discrepancy_experiment.json |
| FD-step stability on NN metric (h in [3e-4, 1e-2]) | max/min ratio 1.0002 | discrepancy_experiment.json |
| Verdict | quadratic-vs-linear scale, fully explained | discrepancy_table.md |

## Precision constraint

| Quantity | Value | Source |
| --- | --- | --- |
| float64 residual over 197-point grid | median 7.9e-6, p95 2.2e-5, max 5.7e-5 | calibration_maps.json |
| float32 metric storage penalty | 203x median inflation | calibration_maps.json |
| Protocol consequence | float64 mandatory for all metric exchange | THRESHOLDS_DRAFT.md |

## Five-seed sweep (2026-08-12, the headline result)

| Seed | Final training loss | Independent vacuum median | Vacuum verdict | Petrov S | Trapped points |
| --- | --- | --- | --- | --- | --- |
| 123 | 1.11e-2 | 0.915 | FAIL | 2.29–2.58 | 11/12 |
| 124 | 1.18e-2 | 0.233 | PASS | 2.27–2.55 | 11/12 |
| 125 | 1.10e-2 | 0.317 | FAIL | 2.30–2.58 | 11/12 |
| 126 | 1.32e-2 | 0.228 | PASS | 2.29–2.56 | 11/12 |
| 127 | 1.09e-2 | 1.100 | FAIL | 2.29–2.58 | 11/12 |

- All three legs satisfied: **2 of 5** seeds.
- Type I and trapping: **5 of 5**, S confined to 2.27–2.58.
- Vacuum spread: **4.8×** (0.228 … 1.100) against a training-loss spread of only **1.21×**.
- Ordering inverted in this sample (lowest loss → worst geometry); n = 5, suggestive only.
  Source: `loss_vs_vacuum.json`.

## Horizon shape (bisection of Xi = 0, ±0.003 in X)

| Model | Apparent horizon | Departure from analytic X = T |
| --- | --- | --- |
| Analytic Schwarzschild | X = T | 0.000 … −0.002 |
| Trained neural Schwarzschild | X = T | +0.000 … +0.009 |
| Candidate seed 124 | X ≈ 0.626 … 0.652 | +0.53 … +0.15 |
| Candidate seed 123 | X ≈ 0.615 … 0.711 | +0.52 … +0.21 |

## Independent Petrov diagnostics

| Model | speciality index S | abs(S − 1) |
| --- | --- | --- |
| Analytic Schwarzschild (type D control) | 1.0000000000000004 | 4.4e-16 |
| Trained neural Schwarzschild (control) | 1.000002 | ≤1.7e-6 |
| Candidates (all five seeds) | 2.27 … 2.58 | ≥1.27 |

## Side observation: supervised vs unsupervised

| Model | max abs Ricci | Kretschmann rel. err |
| --- | --- | --- |
| AL_embed supervised seed (component MSE fit) | 0.064 – 0.149 | 1.5% – 8.2% |
| Unsupervised PINN at 31/500 epochs | 0.092 – 0.178 | 0.4% – 1.7% |

Observation: pointwise metric fitting does not deliver curvature accuracy
(second-derivative error amplification). (al_embed_note.md)

## Engineering facts

- 49 automated tests green (unit + integration + scientific + gold evals + proofgate).
- Proof-gate stage-1 ENGINEERING VERIFIED (4/4), stage-2 VERIFIED (8/8), attestations
  with SHA-256 integrity, `sb proof verify-integrity` passes.
- Clean-clone reproduction passed (fresh clone -> uv sync -> tests -> doctor -> status).
- Upstream pinned at 54736e46; license conflict documented (LICENSE GPL-2.0 vs
  pyproject MIT); no upstream code copied.
- Paper facts: no trained candidate checkpoints published (Data Availability, p.22);
  author-reported Schwarzschild-run residuals: |S|-1 mean 7.8e-5 / max 1.3e-2 (FIG. 5, p.26).
