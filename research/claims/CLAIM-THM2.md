---
id: CLAIM-THM2
statement: For j = 9..18, inside n >= 2J-3, the far-below polynomial is positive for all y >= 0.
domain: j = 9..18
status: CERTIFIED
certificate_artifact: projects/qg-bootstrap/results/THEOREM_STATE.md
last_verified: 2026-08-29
dependencies:
  - CLAIM-R
  - CLAIM-LEGA
evidence:
  - 252 exact region points crossed with y up to 1e5 at j = 9,11,13,15, zero non-positive
references:
---

A theorem conditional on certificates that exist for these depths. CERTIFIED rather than
PROVED because its hypotheses are supplied per depth by certificates, not by an argument
covering all J.
