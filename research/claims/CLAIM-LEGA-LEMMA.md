---
id: CLAIM-LEGA-LEMMA
statement: On the far-below region the sequence phi_i = tau_i / C(L-1,i) is absolutely monotone in i, i.e. Delta^j phi >= 0 for every j.
domain: far-below region, every depth J, every coefficient index k
status: CONJECTURED
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - 378 of 378 (point, k) combinations at J = 9, zero violations
  - 2520 combinations across J = 6, 8, 9, 10, 12, zero violations
  - the factorisation route is CLOSED: tau itself is 0/378 absolutely monotone, and no grouping of the complementary half reaches it either, so the property is joint and the binomial division is essential
references:
---

If proved, leg (a) holds at EVERY depth at once -- Step 1 of THE_THEOREM.md.

What is known about the shape: G = poch_i (s^2 den)^i / prod_{r<i} A_r IS absolutely
monotone (378/378), while E_{J-1-i}, e_k(1/A_i..) and 1/prod A_r are not. So a proof must
use the interaction, not a product decomposition.
