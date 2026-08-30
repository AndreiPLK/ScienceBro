---
id: CLAIM-PSDCONE
statement: (B) holds for every positive semidefinite quadratic form b_k = A + 2Bk + Ck^2.
domain: all PSD Q, 1 <= t <= floor(N/2)
status: DISPROVED
counterexample: 15 of 300 PSD-interior points fail, all with B < 0 and large AC - B^2; e.g. N=8, A=30, B=-1, C=2 fails at t = 1,2,3,4
last_verified: 2026-08-30
dependencies:
evidence:
  - exact sweep over four regimes of the cone, 925 quadratic forms
  - rank-one boundary 0 failures of 300; near-boundary 0 of 300; interior 15 of 300
references:
---

Refuted, but informatively: (B) is NOT confined to the rank-one boundary either. Writing
b_k = C(k-v)^2 + h, it holds for all h below a critical relative height
rho = h/(C max(k-v)^2), measured at 0.122 (N=10) rising to 0.146 (N=44).

So (B) holds on a proper SUB-cone of the PSD cone, and the condition is scale-invariant,
hence still cone-shaped. Our case rho = 0 sits comfortably interior, not on a knife edge.

Consequence for the programme: cone-restricted Rayleigh / K-Lorentzian machinery is the
right KIND of tool, but no theorem quantified over all PSD Q can prove (B).
