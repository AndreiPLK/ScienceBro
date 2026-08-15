# AI disclosure

This research was conducted by the author (Andrei Pluzhnik) working with an AI
research assistant (Claude, Anthropic), which performed derivations, wrote the
computational code, and drafted the text under the author's direction.

Safeguards applied throughout:

- **Exact arithmetic only.** Every claim-bearing computation uses Python
  `fractions.Fraction`; no floating point enters any verdict.
- **Independent adversarial review.** The central theorem was re-derived from
  scratch by an independent review pass (`research/gravity-review.md`), and a
  seven-battery falsification suite (`lab/attack_gravity.py`) was executed:
  no counterexample found.
- **Deterministic claim gating.** Theorem vs conjecture labels follow fixed
  promotion rules; the completeness statement is published as a conjecture
  with its falsification protocol.
- **Honest bug record.** A Pochhammer increment-step bug in the evaluator
  (it incremented ((1+λ)/2+λt)_{n−1} by λ instead of 1, coinciding with the
  correct evaluator only at λ=1) was discovered via an external anchor (CHR's
  reported D≥9 onset), disclosed in the research log
  (`research/DATA_LOG_gravity.md`), and fixed. All λ≠1 results were voided
  and recomputed; λ=1 results, which the bug could not affect, were
  re-verified independently.
- **Human gate for publication.** No agent published, pushed, or submitted
  anything; every public step is a deliberate human action by the author.
