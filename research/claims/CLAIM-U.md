---
id: CLAIM-U
statement: For every t >= 1 and r >= 3 the polynomial D_{t,r}(m + t + r + 3) has all nonnegative coefficients.
domain: all t >= 1, r >= 3
status: DISPROVED
counterexample: r = 9, t = 1 needs shift 14, an excess of 4, while this allows only 3
last_verified: 2026-08-30
dependencies:
evidence:
  - held on all 48 rungs of the first table (t <= 8, r <= 8), which is why it was written
  - refuted by the run launched specifically to attack it, at r = 9
references:
---

Mine, and killed within the hour by the test written to attack it. Superseded by
CLAIM-U2, which is weaker and equally sufficient. See `research/dead_routes.md` DR-11.
