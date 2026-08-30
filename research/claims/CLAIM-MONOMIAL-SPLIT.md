---
id: CLAIM-MONOMIAL-SPLIT
statement: Every tau_i is monomially nonnegative, so [mu] c_k = den^k * Delta^{L-1}([mu] tau_i / C(L-1,i)) and the monomial certificate for leg (a) is equivalent to absolute monotonicity of the per-monomial sequences in Q(sqrt3).
domain: verified at J = 8, 10, 12, all k tested
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - every tau_i has zero negative monomials, at every (k,i) pair tested
  - the per-monomial failures match the certificate's negative-monomial counts EXACTLY -- 20 at J=10 k=J-2, 29 at J=12 k=J-2, 0 everywhere else
references:
---

Turns leg (a)'s four-variable positivity question into a family of one-dimensional
sequences with explicit combinatorial formulas, one per monomial. A proof that those are
absolutely monotone for k outside {J-2} gives leg (a) at every depth at once.

Two earlier versions of the test were wrong -- one ignored monomials with partial support in
i, the other ignored the sqrt3 component -- and both were exposed by passing at k = J-2,
where the certificate is known to fail.
