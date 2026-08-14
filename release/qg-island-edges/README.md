# The Island Has Edges

Exact boundary laws for unitary deformations of the Veneziano amplitude
(the (q,r,w) family of Cheung–Hillman–Remmen, arXiv:2406.02665 / PRL 133, 251601).

**Paper:** `paper/main.pdf` (LaTeX source alongside).

## What is here

- `lab/` — all computation scripts, exact rational arithmetic (Python `fractions`):
  two-route partial-wave evaluator (validated), island maps, depth studies,
  fine boundary scan, fixed-spin tails, `artifacts_battery.py` which reproduces
  every number cited in the paper, and the independent reviewer's adversarial
  script `attack_left_edge.py` (exit 0 = no counterexample found).
- `results/` — all raw and processed outputs (JSON), including
  `paper_artifacts.json` — one file backing every paper-cited number.
- `research/` — the derivation note and the independent review verdict.
- `validation/` — from-scratch validator (no imports from `lab/`) + report: PASS 5/5.

## Reproduce

Python 3.12+, `sympy` (for the symbolic checks only). Every script is
deterministic; no floating point is used in any claim-bearing computation.

```
python lab/artifacts_battery.py     # reproduces all paper-cited numbers
python lab/attack_left_edge.py      # adversarial falsification suite (exit 0)
python validation/validate_paper.py # independent from-scratch validation
```

## Honest status

The edge law and trajectory brackets are derived and independently reviewed.
The completeness of the boundary characterization is a **conjecture**,
verified on 11,994 exact verdicts to depth 80 and labeled as such in the paper.

## AI disclosure

Research conducted by the author with an AI research assistant (Claude,
Anthropic). Every scientific claim is backed by deterministic code in this
repository; the assistant's derivations passed an independent adversarial
review (see `research/left-edge-theorem-review.md`).

## License

MIT (code). Paper text and figures: CC BY 4.0.
