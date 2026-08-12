# Independent verification of machine-learned black-hole spacetimes

**Target:** Hirst, Schettini Gherardini, Stapleton, *Black Hole Black Boxes* (arXiv:2607.05489),
code pinned at `xand-stapleton/ainstein@54736e46` (branch `blackhole`).
**Status:** independent measurement, **not peer-reviewed**. NEEDS EXPERT REVIEW.
**Date:** 2026-08-12. Numbers trace to files with recorded SHA-256 checksums; failed runs are kept.

---

## 1. What was audited, and what could not be

The paper reports neural-network metrics that are numerically Ricci-flat, algebraically
general (Petrov type I) and possess trapped interiors — that is, black holes that are not
Schwarzschild or Kerr. Its Data Availability statement (p.22) publishes the code but **no
trained candidate checkpoints**. Consequently:

- **Auditable:** the method. We retrained the committed black-hole configuration and
  measured the results with an independent instrument.
- **Not auditable:** the paper's own reported candidates. Their weights do not exist
  publicly. A request was sent to the authors on 2026-08-12; nothing here depends on a reply.

Every sentence below respects that distinction.

## 2. The instrument, and why it can be trusted

`projects/ainstein-audit/verifier/` computes curvature from a metric callable by finite
differences in float64 and shares **no code** with the audited system: exported metric values
cross the boundary as plain arrays through a subprocess in an isolated environment.

| Check | Measured | Artifact |
| --- | --- | --- |
| Analytic Schwarzschild is vacuum (Schwarzschild coordinates) | max abs Ricci 8.7e-11 | `verifier/CALIBRATION.md` |
| Kretschmann equals 48M²/r⁶ | rel. err 1.1e-9 | same |
| Analytic Schwarzschild is vacuum (paper's Penrose + stereographic route) | 6.7e-9 … 1.5e-8 | `known_answer_4d.json` |
| Areal radius from the metric vs an independent Lambert-W r(T,X) | agrees to 3 decimals at 12 points | `horizon_diagnostics.json` |
| Schwarzschild is algebraically special (speciality index) | abs(S−1) = 4.4e-16 | `petrov_diagnostics.json` |
| A *trained network* imitating Schwarzschild still reads type D | abs(S−1) ≤ 1.7e-6 | same |
| Trapped-surface test on the analytic metric | 4/4 exterior untrapped, 8/8 interior future-trapped | `horizon_diagnostics.json` |
| Deliberately corrupted metric is rejected | detected and localized to the perturbation | `verifier/test_*.py` |
| Precision requirement | float32 storage inflates the residual 203× | `calibration_maps.json` |
| Finite-difference convergence on a network metric | stable to 5 digits over h ∈ [3e-4, 1e-2] | `discrepancy_experiment.json` |

Three independent routes (Schwarzschild coordinates, the paper's Penrose route, and an
independently reimplemented r(T,X)) agree, which is what makes the floor believable.

## 3. The loss-scale discrepancy, resolved by measurement

The first apparent contradiction was a factor of 20 000: the upstream training loss read
1.57e-10 where our independent evaluation of the same network read 1.26e-5. It was settled
by measurement, not argument (`results/processed/discrepancy_table.md`):

- Their loss is **quadratic** in the residual, metric-contracted and volume-weighted
  (`losses/schwarzschild.py:1944-1956`, paper Eq. 39/46); ours is a linear pointwise maximum.
- On a common scale: sqrt(1.57e-10) = 1.253e-5 versus our 1.261e-5 — **0.7 % apart**.
- Replicating their exact formula while substituting *our* independently computed Ricci
  returns 8.08e-11 against their 1.57e-10, a factor 1.9 attributable to sampling.

Finite-difference error and float32 were both excluded by measurement rather than assumed.

## 4. Protocol integrity

- A neural Schwarzschild baseline was retrained (500 epochs, seeds 66/66) to serve as the
  ruler: hidden-point residual median 0.123, p95 0.286, max 0.297 (`baseline_stress.json`).
- Pass criteria were derived from that baseline, committed and **git-tagged
  `thresholds-frozen` before any candidate existed** (`validations/THRESHOLDS_FROZEN.md`).
- Hidden evaluation points are drawn from a seed derived deterministically from each
  checkpoint's SHA-256, so they cannot be chosen to flatter a result.
- Stage statuses come from `sciencebro.proofgate`, which computes them from hashed
  artifacts; a changed artifact invalidates its attestation automatically.

## 5. Findings

### 5.1 The method reaches its stated targets under independent measurement

For the seed-124 retrain, all three properties hold simultaneously:

| Property | Candidate seed 124 | Reference |
| --- | --- | --- |
| Vacuum on hidden points | median 0.233 (limit 0.286) | baseline 0.123 |
| Algebraically general (Petrov type I) | S = 2.27 … 2.55 | Schwarzschild = 1; trained-network floor 1.7e-6 |
| Future-trapped region | 11/12 probe points | controls reproduce the textbook horizon exactly |

**Interpretation, stated carefully.** All three are *explicit training targets* of the
upstream objective (Einstein term; speciality-index profile centred near 2, Eq. 47; trapping
weight 25.0). Measuring them therefore corroborates that the published architecture achieves
what it was designed to achieve, **as judged by an outside instrument for the first time**. It
is not evidence that a new exact solution of Einstein's equations exists.

### 5.2 The configuration is seed-unstable

Two runs differing only in random seed, same code, same 500 epochs, near-identical training
loss curves (final 1.11e-2 vs 1.18e-2):

| Seed | Hidden-point vacuum median | Verdict under the frozen criteria |
| --- | --- | --- |
| 124 | 0.233 | PASS |
| 123 | 0.915 | FAIL (3.2× over the limit) |

The seed-123 failure is **global** across the Penrose block, not localized near the horizon
or the boundary (`boundary_map.json`, 95 grid points: exterior median 1.098, interior 0.986).
Both runs are type I and both trap light; they differ in whether the vacuum condition is met.
This sensitivity is not reported in the paper. A five-seed sweep is in progress to bound how
often the recipe produces a candidate satisfying all three legs.

### 5.3 Incidental measurement: fitting a metric is not fitting its curvature

The repository's supervised seed model `AL_embed`, trained to match the analytic metric
componentwise, has *worse* curvature than a 6 %-trained physics-informed network
(Kretschmann error 1.5–8.2 % vs 0.4–1.7 %) — second-derivative error amplification in
practice (`al_embed_note.md`). Consequence for any audit of this kind: pointwise metric
agreement is not evidence of geometric agreement.

## 6. Claims, in the exact wording permitted by the gates

- **CL-0003** (experimentally-supported): a candidate retrained from the committed
  configuration with seed 123 does not meet the pre-frozen vacuum criteria.
- **CL-0004** (experimentally-supported): the seed-124 retrain is simultaneously
  vacuum-comparable to our reproduced baseline, algebraically general, and trapped.
- **CL-0002** (speculative, blocked): nothing is claimed about the paper's own candidates;
  their checkpoints are unavailable.

The words *discovery*, *confirmation* and *refutation* are not used anywhere in this report.

## 7. Limitations

1. No qualified relativist has reviewed this. Until that happens it is a measurement, not
   accepted physics.
2. Our retrains are not the authors' models; a failed replication is not a refutation.
3. Seed statistics rest on a small number of runs.
4. The marginally trapped surface (Ξ = 0) is located only to the resolution of the
   bisection, and the angular direction was sampled at one stereographic point.
5. The 4D equivalent of the upstream loss has not been replicated exactly; comparisons on
   their own scale are therefore restricted to the 2D case.
6. Trained on CPU because consumer-GPU float64 measured 10× slower; no GPU-specific
   numerical behaviour was explored.

## 8. Reproducing this

```
uv sync --all-groups
uv run sb verify-all ainstein-audit      # stage statuses from hashed artifacts
uv run pytest -q                          # known-answer tests, negative controls
uv run python projects/ainstein-audit/verifier/known_answer_4d.py
uv run python projects/ainstein-audit/verifier/seed_sweep.py
```

Proof packs with attestations, commands and checksums: `projects/ainstein-audit/proof/stage-*/`.
AI use is disclosed in `AI_DISCLOSURE.md`: an AI agent wrote the code and ran the experiments;
the deterministic gates and preserved artifacts are what make the result checkable.
