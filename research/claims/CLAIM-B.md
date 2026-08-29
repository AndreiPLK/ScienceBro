---
id: CLAIM-B
statement: p_(t+1)^3 p_(t-1) >= p_t^3 p_(t+2) for the central factorial family.
domain: every t <= 200 proved individually; uniformity in t open; first half of the range
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-29
dependencies:
evidence:
  - 198 finite polynomial proofs, t = 3..200, 0 failures (conjecture_B_rungs.json)
  - each rung: all coefficients nonnegative after the shift n = m + 2t
references:
---

Each fixed t IS proved -- the shifted polynomial has nonnegative coefficients, which is an
argument and not a measurement. What is open is uniformity in t, so the general statement
sits at COMPUTATIONALLY_VERIFIED while the individual rungs are proofs.

(B) is the rung r = 3 of the log-difference hierarchy, so CLAIM-U -- if proved -- would
settle it uniformly along with every other rung.
