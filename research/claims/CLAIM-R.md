---
id: CLAIM-R
statement: 4 c_(J-1) c_(J-3) - c_(J-2)^2 >= 0 on the far-below region.
domain: J = 7,9,12,16,20,25-32,35,40,45,50; from J=30 inside the regime n >= 2J-3
status: CERTIFIED
certificate_artifact: projects/qg-bootstrap/results/certificate_audit.json
last_verified: 2026-08-29
dependencies:
evidence:
  - nonnegative monomials to J=29
  - one Bernstein step in thL from J=31
references:
---

Certified depth by depth, audited by `lab/certificate_audit.py`. NOT known uniformly in J:
that is Gap 1 of the programme.
