# Validation thresholds — FROZEN 2026-08-12 ~03:40 (before any Petrov-I candidate exists)

Frozen per directive §6: BEFORE any candidate output is generated or inspected.
Every number below is measured, sources in parentheses. Git tag: `thresholds-frozen`.

## Measured baseline (EXP-0001: clean 500-epoch NN-Schwarzschild, seeds np/tf=66,
## checkpoint sha256 7651ff3d…, hidden points seed 20260812, h=3e-3, float64)

| Statistic (hidden points, n=24) | Value | Source |
| --- | --- | --- |
| max\|Ricci\| median / p95 / p99 / max | 0.123 / 0.286 / 0.295 / 0.297 | baseline_stress.json |
| Kretschmann rel. err median / max | 0.30% / 1.34% | baseline_stress.json |
| Lorentzian signature | 24/24 | baseline_stress.json |
| Corruption detection floor (bump amplitude) | ≥ 0.2 detectable via max (0.58 vs 0.30); 0.05 NOT detectable | control_scale.json |

## Frozen criteria for ANY Petrov-I candidate (evaluated on fresh hidden points,
## seed to be drawn as sha256(checkpoint) mod 2^31 — deterministic, not tunable)

1. **Pipeline validity gate** (per evaluation run): analytic-route max|Ricci| < 1e-7
   AND Kretschmann rel err < 1e-7 at 4 probe points, else the evaluation is void.
2. **Vacuum comparability**: candidate hidden-point max|Ricci| median ≤ 0.286
   (baseline p95) AND p95 ≤ 0.573 (2× baseline p95).
3. **Signature**: Lorentzian at 100% of valid-domain hidden points; det(g) < 0 at all.
4. **Convergence**: max|Ricci| median changes < 20% under h ∈ {1e-3, 3e-3, 1e-2}.
5. **Precision**: float64 export only (float32 voids the run — measured 203×).
6. **Negative control**: same-checkpoint metric corrupted with amplitude 0.5 bump
   must exceed criterion 2 (measured: 1.48 max vs 0.30 clean).

## Honest limitations (recorded at freeze time)

- The trained baseline's own pointwise residual (~0.12–0.30) is large; criterion 2
  therefore tests "as vacuum as the reproduced baseline", NOT "vacuum in an absolute
  sense". Corruptions below ~0.2 amplitude are NOT detectable at this baseline quality.
- The upstream paper's quadratic, volume-weighted, sample-averaged losses are NOT
  directly comparable to these pointwise maxima; the exact 4D normalization
  replication remains an open task and does not gate candidates.
- These thresholds may be tightened only by training a better baseline BEFORE any
  candidate inspection; they may never be loosened after seeing candidate results.
