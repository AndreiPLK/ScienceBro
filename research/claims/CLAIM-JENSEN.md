---
id: CLAIM-JENSEN
statement: Every Jensen polynomial J^{d,t}(X) = sum_j C(d,j) p_{t+j} X^j of the centred family is hyperbolic.
domain: d = 2..8, n = 11,15,21,27,33,41, window inside the first half; also verified past the midpoint at n = 21,27,33
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-30
dependencies:
evidence:
  - 332 of 332 hyperbolic, exact rational coefficients, roots isolated by flint in certified boxes
  - also holds past the midpoint, and also holds for the raw e_t
references:
---

Gives the whole family of higher-order Turan inequalities for p at once.

But it CANNOT be the mechanism behind the log-difference hierarchy: it holds past the
midpoint, where the hierarchy fails, and it holds for e as well as p, while the hierarchy
holds only for p. It is coarser than the phenomenon. See `JENSEN_HYPERBOLICITY.md`.
