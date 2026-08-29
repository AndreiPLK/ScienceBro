---
id: CLAIM-MOMENT
statement: A_t = -Delta^2 log p_t admits a positive-measure (moment) representation.
domain: centred family, first half
status: DISPROVED
counterexample: negative Hankel minor at order 4 (forward) and 5-9 (reversed), n = 21..101
last_verified: 2026-08-29
dependencies:
evidence:
  - moment_route_refutation.json: exact fmpq determinants of A rationalised to 300 digits, every decisive minor 200+ orders of magnitude above its error bound
references:
---

Killed in both orientations. On paper the un-reversed Hausdorff form was already excluded:
the hierarchy makes A absolutely monotone, hence a moment sequence on [1, infinity), not on
[0,1]. See `research/dead_routes.md`.
