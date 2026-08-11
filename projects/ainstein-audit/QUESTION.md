# Primary research question

Do the reported candidate metrics from the AInstein blackhole project
(arXiv:2607.05489, github.com/xand-stapleton/ainstein@blackhole) remain vacuum-like,
Lorentzian, black-hole-like, and non-Schwarzschild under:

1. an **independent evaluator** (separate formulation, no upstream loss functions);
2. **unseen sample points** (hidden interior/exterior points, horizon oversampling);
3. **precision and convergence tests** (float32 vs float64 vs selected higher precision;
   grid/sample-density sweeps);
4. **boundary/horizon stress tests** (explicit failure maps near boundaries,
   horizons, and excluded singular domains)?

## Important separation

- Upstream answers: can its own model minimize its own training objective?
- We must answer: does an independently constructed evaluator verify the physical and
  numerical claims **outside the upstream training path**?

## Scope

- In: exported candidate metrics/checkpoints, Schwarzschild baseline, perturbed
  controls, curvature invariants, signature/determinant checks, convergence analysis.
- Out (V1): new physics interpretation, horizon-structure proofs beyond diagnostics,
  training new models.

## Measurable completion condition

One of three honest outcomes (roadmap §2): confirmation of at least one candidate under
documented checks; a reproducible failure/artifact; or an inconclusive-but-useful
release (independent validator + reproducibility report + exact blockers).

## Stop conditions

- Compute budget exceeded (12 h single run cap) without convergent results → document.
- Upstream artifacts (checkpoints/configs) unavailable and not reconstructible →
  document blocker, pivot to validator-only release.
