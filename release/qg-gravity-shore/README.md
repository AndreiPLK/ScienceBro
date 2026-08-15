# The Shore of Closed-String Gravity

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21944818.svg)](https://doi.org/10.5281/zenodo.21944818)

An exact unitarity boundary for the Cheung–Hillman–Remmen graviton family
(arXiv:2408.03362 / PRD 111, 086034), containing Virasoro–Shapiro at λ=1.

**Paper:** `paper/main.pdf` (LaTeX source and all figures alongside).
Companion open-string work: DOI [10.5281/zenodo.21934462](https://doi.org/10.5281/zenodo.21934462).

## Results in one breath

- **Trajectory law (theorem):** a_{n,2n−4} ≥ 0 ⟺ D ≤ T_n(λ) with
  T_n(λ) = 3(2n−3)/(n(n−2))·(λ²+(2n−2)λ+1) + 2n — proven for general n
  (independent re-derivation) and verified symbolically for n ≤ 14 (12/12).
- **The shore is born at D=9** (T_3(0)=9) — reproducing, as a formula, the
  onset CHR observed numerically.
- **The magic point:** λ_min(23)=1 exactly — the shore passes exactly through
  the string; on this trajectory pure Virasoro–Shapiro first loses positivity
  at D=24 via its level-4 spin-4 wave (exact scans: D=22 clean to depth 40).
- **The straight far edge:** exact asymptote D=(12+4√3)λ, active level n*≈√3λ.
- **Completeness is a conjecture** (labelled as such): boundary of the full
  family = min_n T_n. Battery: 494/494 exact-scan agreements, zero alarms;
  knife hunts on the 2n−6 and 2n−8 trajectories and a low-spin stress test at
  the boundary — all clean; two doomed-cell executions killed at the predicted
  level.
- **D=4:** the entire family survives every test we can run — within these
  assumptions, four-dimensional gravity is *not* forced to be string-like.

## What is here

- `lab/` — all computation scripts, exact rational arithmetic (Python
  `fractions`): the corrected evaluator (`grav_full_body.py`), the model test
  (`model_test.py`, 494/494), the independent reviewer's adversarial suite
  (`attack_gravity.py`, exit 0 = no counterexample), knife hunts
  (`hunt_2n6.py`, `hunt_2n8.py`, `lowspin_stress.py`), VS depth clock
  (`vs_d_clock.py`), D=4 scans and more.
- `results/` — all raw and processed outputs (JSON) with run metadata,
  including `paper2_artifacts.json` — one file backing every paper-cited
  number. `grav_zoomout_v2.json` regenerates the original zoom-out scan with
  metadata and matches it 330/330.
- `research/` — the research card (frozen hypothesis and metric), the
  independent review verdict, exact T_n bracket transcripts, evidence records
  for the sources, and the gravity extract of the append-only research log —
  including the honest record of an implementation bug (see below).
- `media/` — the 3D cliff of survival, the companion ship's bow, and lay
  explainer panels.

## Reproduce

Python 3.12+; `sympy` for the symbolic checks only. Every claim-bearing
computation is exact rational (no floating point).

```
python lab/model_test.py       # conjecture vs exact scans: 494/494
python lab/attack_gravity.py   # adversarial falsification suite (exit 0)
python lab/hunt_2n8.py         # knife hunt at the boundary (0 alarms)
```

## Honest status

The trajectory law T_n is a theorem (independent hand re-derivation, general
n). The claim that its envelope is the **complete** boundary of the family is
a **conjecture**, clearly labelled, with its falsification battery published
here. During this work a Pochhammer increment-step bug (coinciding with the
correct evaluator only at λ=1) was found via an external anchor, disclosed in
the log, and fixed; all λ≠1 results were voided and recomputed.

## Explain it to anyone

Every candidate theory of gravity in this family is a hiker on a high plateau.
Adding spacetime dimensions means walking toward the edge. Below nine
dimensions there is no edge at all — everyone is safe, including our own
four-dimensional world. From nine dimensions on, a cliff appears, and we found
the exact formula for where it runs. String theory walks the plateau and
reaches the very edge at exactly 23 dimensions — one more step and it falls.
The boundary of consistency passes exactly through the string, and only in
high dimensions. `media/gravity-cliff-3d.png` is that picture.

## AI disclosure

Research conducted by the author with an AI research assistant (Claude,
Anthropic). Every scientific claim is backed by deterministic code in this
repository; the assistant's derivations passed an independent adversarial
review (`research/gravity-review.md`). See `AI_DISCLOSURE.md`.

## License

MIT (code and text in this repository). Figures and media: CC BY 4.0.
