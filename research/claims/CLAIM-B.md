---
id: CLAIM-B
statement: p_(t+1)^3 p_(t-1) >= p_t^3 p_(t+2) for the central factorial family.
domain: every t <= 100 proved individually; uniformity in t open; first half of the range
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-29
dependencies:
evidence:
  - 100 finite polynomial proofs, degrees 22 to 1606, 0 failures (conjecture_B_rungs.json)
  - each rung: all coefficients nonnegative after the shift n = m + 2t
references:
---

Each fixed t IS proved -- the shifted polynomial has nonnegative coefficients, which is an
argument and not a measurement. What is open is uniformity in t, so the general statement
sits at COMPUTATIONALLY_VERIFIED while the individual rungs are proofs.
