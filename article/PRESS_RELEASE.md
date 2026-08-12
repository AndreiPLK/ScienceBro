# PRESS RELEASE (living draft — updated at every milestone)

**Status: DRAFT. Not for distribution until founder approval and stage-6 release gate.**
Wording constraints: no "discovery / confirmation / refutation" — none of these has
passed independent validation. Allowed claims only.

---

## One independent night: auditing AI-discovered black holes with a self-verifying research system

**2026-08-12.** ScienceBro — a one-machine autonomous research workbench built in a
single day by a founder and an AI agent — completed the first independent audit cycle
of the AInstein black-hole search (arXiv:2607.05489) overnight.

### What was measured (all numbers reproducible from the repository)

| Result | Number | Artifact |
| --- | --- | --- |
| Independent verifier floor (analytic Schwarzschild, two coordinate routes) | 1e-10 / 1e-8 | `known_answer_4d.json` |
| Reproduced neural Schwarzschild baseline (500 epochs), hidden-point residual | median 0.123 | `baseline_stress.json` |
| Validation thresholds | frozen + git-tagged BEFORE any candidate existed | `THRESHOLDS_FROZEN.md` |
| Black-hole candidate, seed 123 (authors' committed config, verbatim) | **FAIL** — median 0.915, failure global across the Penrose block | `candidate_stress.json`, `boundary_map.json` |
| Black-hole candidate, seed 124 (same config) | **PASS** — median 0.233, converged, Lorentzian everywhere | `candidate_stress_run2.json` |
| Seed-to-seed variability of the committed configuration | **~4×** | VAL-0001 / VAL-0002 |
| float32 checkpoint storage penalty on curvature | 203× residual inflation | `calibration_maps.json` |
| Consumer-GPU float64 penalty (RTX 4070 SUPER) | 10× slower than CPU | DATA_LOG 23:33 |

### Five-seed sweep: the instability has a precise location (added 2026-08-12, 16:10)

Five candidates trained from the identical committed configuration, differing only in the
random seed, each evaluated by the same independent code (`seed_sweep.json`):

| Seed | Its own training loss | Our vacuum residual | Vacuum | Petrov S | Trapped | All three |
| --- | --- | --- | --- | --- | --- | --- |
| 126 | 1.32e-2 | **0.228** | PASS | 2.29–2.56 | 11/12 | **yes** |
| 124 | 1.18e-2 | **0.233** | PASS | 2.27–2.55 | 11/12 | **yes** |
| 125 | 1.10e-2 | 0.317 | FAIL | 2.30–2.58 | 11/12 | no |
| 123 | 1.11e-2 | 0.915 | FAIL | 2.29–2.58 | 11/12 | no |
| 127 | **1.09e-2** | **1.100** | FAIL | 2.29–2.58 | 11/12 | no |

Three measured statements:

1. **Two of five** retrains satisfy all three black-hole properties at once.
2. **The instability is confined to one leg.** The exotic algebraic type and the trapped
   region appear in 5 of 5 runs, tightly clustered; the vacuum condition — the Einstein
   equation itself — holds in 2 of 5, spanning a factor 4.8 (0.228 to 1.100).
3. **The reported loss does not track independent quality.** It varies by a factor 1.21
   across seeds while the independent residual varies by 4.8, and in this sample the ordering
   is inverted: the lowest-loss run has the worst geometry. At n = 5 this is suggestive, not
   established — and it is precisely the failure mode an external instrument exists to catch.

Horizon shape, measured by bisecting the Ξ = 0 surface to ±0.003: a network trained to
imitate Schwarzschild recovers the textbook horizon X = T to within 0.009 (so the method is
sound), while the candidates' horizons are near-vertical lines at X ≈ 0.63–0.71 — a different
shape, not a displaced copy.

### The three-leg independent check

A "new black hole" claim needs three properties at once. Each was tested with our own
implementation, each with its own control:

| Property | Control behaviour | Candidate seed 124 | Source |
| --- | --- | --- | --- |
| Vacuum (Ricci-flat) | reproduced Schwarzschild baseline: median 0.123 | median 0.233, inside the pre-frozen limit 0.286 | `candidate_stress_run2.json` |
| Algebraically general (Petrov type I) | analytic Schwarzschild S = 1 to 4e-16; **trained** neural Schwarzschild S = 1 to 1.7e-6 | S = 2.27 … 2.55 | `petrov_diagnostics.json` |
| Future-trapped region | analytic: 4/4 exterior untrapped, 8/8 interior trapped; trained network reproduces the same split | 11/12 points future-trapped, areal radius up to 0.44 away from Schwarzschild's | `horizon_diagnostics.json` |

All three hold simultaneously for the seed-124 candidate under independent evaluation.
The seed-123 candidate is type I and trapped but fails the vacuum criterion.

**The caveat that must travel with this result:** the upstream objective trains all
three properties explicitly (Einstein term, speciality-index profile centred near 2,
trapping weight 25.0). So this corroborates that the published architecture achieves
what it was designed to achieve, measured by an outside instrument. It is not evidence
of a new exact solution, and it is not a statement about the authors' own checkpoints,
which were not published and have been requested.

### What this does and does not mean

- One of two retrained candidates reaches the vacuum quality of the reproduced
  Schwarzschild baseline under independent evaluation; the other misses it by 3×.
- **Not established:** that any candidate is algebraically general (Petrov type I),
  non-Schwarzschild, or a new solution. Those diagnostics are the next step.
- **Not a statement about the paper's own results:** the authors' trained
  checkpoints are not published; only retraining from their committed configs was
  possible.

### Verification model

Stage statuses are computed by deterministic proof gates from hashed artifacts; the
AI agent is structurally unable to mark its own work as verified. Stages 1–4 of 6
are VERIFIED as of this morning. Every failed run is preserved.

---

## Visuals (in `article/visuals/`)

| File | Caption |
| --- | --- |
| `dashboard-mission-control-2026-08-11.png` | Mission Control: quest-map roadmap, proof-gate statuses |
| `loss-curve-baseline-final.png` | Clean 500-epoch Schwarzschild baseline training curve |
| `loss-curve-candidate-run1.png` | First black-hole candidate training curve |
| `seed-variability.png` | Baseline vs seed 123 (FAIL) vs seed 124 (PASS) — the 4× spread |
| `candidate-boundary-map.png` | Seed-123 residual across the Penrose block incl. horizon — failure is global |
| `loss-curve-cpu-epoch275.png` | The interrupted first run (reboot for GPU experiment) |
| `residual_map_2d.html` | Verifier calibration heatmap (2D smoke model) |
| `quest-map-2026-08-11.svg` | Roadmap graphic, standalone |

## Timeline of the night (compressed)

23:35 clean baseline launched (full CPU) → 03:15 complete → 03:40 hidden-point
stress + thresholds frozen + tagged → 03:50 candidate seed-123 launched → 04:50
complete → 05:00 evaluated: FAIL → 05:10 boundary map: failure global → 05:15
seed-124 launched → 06:20 complete → 06:30 evaluated: PASS → gates stage-1..4
VERIFIED. Machine: one Windows desktop, CPU only (GPU measured and rejected: 10×
slower on float64).

Full data log: `article/DATA_LOG.md`. Communication record:
`article/data/communication-timeline.md`.
