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
