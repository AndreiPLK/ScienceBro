# AI disclosure

This research was conducted by the author (Andrei Pluzhnik) working with an AI
research assistant (Claude, Anthropic), which performed derivations, wrote the
computational code, and drafted the text under the author's direction.

Safeguards applied:

- **Exact arithmetic only** in every claim-bearing computation
  (`fractions.Fraction`; the completeness sweep's region boundary uses an
  exact rational floor after an adversarial reviewer flagged a float there).
- **Independent adversarial review.** A separate review pass re-derived the
  master formula end-to-end, mechanically proved the key integral identity,
  and wrote its own from-scratch evaluator (no imports from the lab code);
  its suite was executed: exit 0, 4,060/4,060 sign agreements including
  regimes the lab never scanned (odd and non-integer D).
- **Blind tests.** Rung j=3 was checked on levels its fit never saw
  (2052/2052); the full formula was checked on trajectory j=6, which its
  construction never used (part of 702/702).
- **Honest failure records.** A known-answer gate failed once during an
  exploratory computation - correctly (wrong reference value, correct
  machinery); the event is preserved in the public log.
- **Human gate for publication.** No agent published, pushed, or submitted
  anything; every public step is a deliberate human action by the author.
