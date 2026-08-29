---
id: CLAIM-POISSON
statement: M_{n,t} = n(rho_t beta_t - 1) exactly, with rho tilt-invariant and beta = t(N-t)/((t+1)(N-t+1)).
domain: algebraic identity; verified at all even n = 8..40 and all 2 <= t <= N-3
status: PROVED
proof_artifact: projects/qg-bootstrap/results/POISSON_BINOMIAL_VIEW.md
last_verified: 2026-08-29
dependencies:
evidence:
  - 0 mismatches over the tested range; the split is an algebraic identity
references:
  - Fatehi and Kittaneh, arXiv:1911.12167, Theorem 6
---

prod(1 + b_i s) is the pgf of a Bernoulli sum and s is an exponential tilt; the s^t factors
cancel in rho, and beta is the binomial normalisation.
