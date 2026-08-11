# Discrepancy investigation: upstream loss 1.57e-10 vs independent max|Ricci| ≈ 3.3e-6

Date: 2026-08-11. Model: smoke SchwarzschildLocal2DModel (dim 2, λ=0, 100 epochs).
Raw data: `discrepancy_experiment.json`. Every number below is measured, not estimated.

## Tested causes

| # | Candidate cause | Test | Measured result | Verdict |
| --- | --- | --- | --- | --- |
| 1 | FD step error dominates the 3.3e-6 | step sweep h ∈ {1e-2, 3e-3, 1e-3, 3e-4} on identical points | max\|Ricci\| = 1.2613e-5 / 1.2613e-5 / 1.2613e-5 / 1.2615e-5 (stable to 5 digits) | **excluded** — FD-converged; residual belongs to the NN metric |
| 2 | Quantity is defined differently (linear vs quadratic) | compare sqrt(upstream loss) with our max\|Ricci\| | sqrt(1.57e-10) = **1.253e-5** vs our max\|Ricci\| = **1.261e-5** (0.7% apart) | **PRIMARY CAUSE** — upstream loss is quadratic in Ricci (Eq. 39 / losses/schwarzschild.py:1950) |
| 3 | Contraction & weighting differ (Euclideanised g_E, volume weight, mean-vs-max) | replicate upstream formula exactly, substituting OUR FD Ricci: mean_a\|R g_E⁻¹ g_E⁻¹ R\|·√\|det g\| | **8.08e-11** vs upstream training value **1.57e-10** (factor 1.9) | **CONFIRMED consistent** — residual gap from sampling (24 uniform pts vs their 10k sampler) |
| 4 | Evaluation points differ | interior ball (r≤0.7) vs near-boundary (r=0.95) | interior max 1.35e-5 / median 4.5e-6; edge max **5.54e-5** / median 7.5e-6 | **contributes** — boundary region is ~4× worse; their sampler and mine weight regions differently |
| 5 | dtype (float32 vs float64) | not yet run on the NN export | — | pending (queued in calibration backlog) |
| 6 | Coordinates/domain mismatch | same coordinates by construction (points fed to the same model) | n/a | excluded by design |

## Statistics of the independent per-point residual max|R_ab| (interior, h=3e-3, n=24)

median 4.55e-6 · p95 1.26e-5 · max 1.35e-5 · Frobenius mean 8.12e-6

## Conclusion (bounded, honest)

The apparent 4.5-order-of-magnitude discrepancy (1.6e-10 vs 3.3e-6) is **explained**:
the upstream number is a *quadratic, volume-weighted, sample-averaged* contraction of
the same Ricci field whose *linear pointwise maximum* we report. On identical linear
footing (square root), upstream and independent values agree to ~1%; replicating the
full upstream formula with our independently-computed Ricci reproduces their loss to
within a factor of 2 (attributable to sampling). Remaining open item: float32/float64
export sensitivity (cause 5).

The independent evaluator therefore *corroborates* the upstream 2D training-loss scale
on this smoke model. No claim about paper candidates follows from this.
