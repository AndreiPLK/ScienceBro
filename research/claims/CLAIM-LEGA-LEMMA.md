---
id: CLAIM-LEGA-LEMMA
statement: For k outside {J-2, J-3}, the sequence phi_i = tau_i / C(L-1,i) is absolutely monotone in i on the far-below region.
domain: far-below region, coefficient indices k outside {J-2, J-3}
status: DISPROVED
counterexample: exact over Q(sqrt3) -- 63 violations at J = 24 and 444 at J = 28; at k = J-4 the first difference is already negative, at k = 0,1 the failure is at order 22 of 23
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - checked exactly with no floating point; phi lives in Q(sqrt3) at a rational region point
references:
---

Absolute monotonicity was a SUFFICIENT condition I imposed, not what the programme needs.
Proposition 1 asks only for c_k >= 0, which by the reduction is the TOP difference
Delta^{L-1} phi(0); the intermediate differences are free to go negative, and they do.

The requirement itself holds: see CLAIM-LEGA-EXACT.
