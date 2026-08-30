---
id: CLAIM-LEGA
statement: Every y-coefficient c_k with k outside {J-2, J-3} is nonnegative.
domain: j = 9..18
status: CERTIFIED
certificate_artifact: projects/qg-bootstrap/results/farbelow_negative_pattern_j16.json
last_verified: 2026-08-29
dependencies:
evidence:
  - negative monomials occur only at y-degree J-2: 11,30,41,71,96,130,165,205,253,351 for j = 9..18
references:
---

The current ceiling of Theorem 2, and it is machine time rather than mathematics: the
verified coefficient formula gives each c_k separately (`lab/farbelow_coeff_signs.py`, now
with V_OFFSET for in-regime runs).
