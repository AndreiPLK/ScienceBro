---
id: CLAIM-THM2
statement: For j in {9, 12, 16, 17, 18, 20, 26} -- the depths where BOTH legs are certified -- inside n >= 2J-3, the far-below polynomial is positive for all y >= 0.
domain: j = 9, 12, 16, 17, 18, 20, 26 (intersection of the two legs; longest consecutive stretch 16..18)
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

CORRECTION 2026-08-30: this claim previously read j = 9..18, which required (R) at 10, 11,
13, 14, 15 -- depths where it was never run. Theorem 2 holds only where BOTH legs are
certified. The missing (R) depths are being computed.
