---
id: CLAIM-LEGA-EXACT
statement: Inside the regime n >= 2J-3, c_k >= 0 for every k outside {J-2, J-3}, at every region point tested.
domain: J = 12..36, inside the regime, at rational region points
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - 15876 checks, exact over Q(sqrt3), zero failures
  - depths to J = 36, double the ceiling the certificate route reached, seconds per depth instead of hours
references:
---

This is POINT EVALUATION, not a certificate: it does not prove positivity on the whole
region, only at the points tested. Its value is that it is exact, fast, and reaches depths
the assembly route cannot.

The same test WITHOUT the regime shift reports failures at J >= 24 -- all at points with
n < 2J-3, outside the regime where leg (a) is claimed. That near-miss is recorded in
LEG_A_REDUCED_TO_ONE_LEMMA.md.
