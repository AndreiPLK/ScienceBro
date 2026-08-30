---
id: CLAIM-LEGA-LEMMA
statement: For k outside {J-2, J-3}, the sequence phi_i = tau_i / C(L-1,i) is absolutely monotone in i on the far-below region.
domain: far-below region, every depth J, coefficient indices k outside {J-2, J-3}
status: CONJECTURED
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - CORRECTED DOMAIN: the unrestricted version is FALSE -- at J=16, k=13=J-3 it fails at the first difference, verified at 250 digits. Proposition 1 excludes exactly those indices.
  - on the correct domain: 0 refutations across J = 9,12,14,16,18,20, 5751 cases
  - the increasing half is exactly K > 0 where the margin is 1 + K/n (CLAIM-LEADING-IDENTITY)
  - 378 of 378 (point, k) combinations at J = 9, zero violations
  - 2520 combinations across J = 6, 8, 9, 10, 12, zero violations
  - R = phi_{i+1}/phi_i is >= 1, increasing AND log-convex in all 2520 cases -- but all three together are insufficient as generic sequence conditions (counterexamples found)
  - the ratio does not decompose: only the constant factor (s^2 den) is both >= 1 and increasing
  - the awkward factor is E_{J-2-i}/E_{J-1-i}, the SAME central factorial ratio the Newton-excess lemma of Gap 2 controls
  - the factorisation route is CLOSED: tau itself is 0/378 absolutely monotone, and no grouping of the complementary half reaches it either, so the property is joint and the binomial division is essential
references:
---

The increasing half of Lemma A is EXACTLY the inequality

    (product of the other factor ratios) >= rho_{t-1},   rho = E_{t-1}^2/(E_{t-2} E_t)

with rho the Newton excess of the central factorial numbers, which is >= 1 by Newton
(classical, the generating polynomial is real-rooted). Measured margin: 1.0017 -- under two
parts in a thousand. The inequality is nearly tight, which is why no generic criterion
reaches it, and why a sharp Newton-excess bound is exactly what is needed.

If proved, leg (a) holds at EVERY depth at once -- Step 1 of THE_THEOREM.md.

What is known about the shape: G = poch_i (s^2 den)^i / prod_{r<i} A_r IS absolutely
monotone (378/378), while E_{J-1-i}, e_k(1/A_i..) and 1/prod A_r are not. So a proof must
use the interaction, not a product decomposition.
