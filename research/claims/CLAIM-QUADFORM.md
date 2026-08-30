---
id: CLAIM-QUADFORM
statement: knife = g^T H g = h^T D h, where H_ij = c_{i+j}, D_ij = (-1)^{i+j} c_{i+j}, g is the coefficient vector of the half-spectrum product and h_i = e_i(half spectrum) > 0.
domain: every depth j, every n, lambda, D where the B-form applies
status: PROVED
proof_artifact: projects/qg-bootstrap/results/KNIFE_IS_A_QUADRATIC_FORM.md
last_verified: 2026-08-30
dependencies:
evidence:
  - follows from the doubled multiset: sum_t (-1)^t e_t x^t = prod(1 - x b_k) is a perfect square g(x)^2
  - verified exactly at 108 parameter settings for the g-form and 36 for the h-form, 0 mismatches
references:
---

The knife is a quadratic form with a Hankel matrix, and h is entrywise positive.

Copositivity of D would give the keystone in one line for every depth. It is FALSE:
random h > 0 gives negative values in all 36 settings tested. So no argument about D alone
can work and the proof must use the structure of h.

That structure is what the rest of the programme already studies: h is a Polya frequency
sequence, its normalisation is ratio log-concave on its whole range, it satisfies (B) for
every t <= 200, and its Jensen polynomials are hyperbolic. The keystone and (B) are the
same object seen twice, now by an identity rather than an analogy.
