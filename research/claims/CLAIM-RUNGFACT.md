---
id: CLAIM-RUNGFACT
statement: D_{t,r}(n) = c (n+1) PROD_{k=0}^{t+r} (n-k)^{m_k} Q_{t,r}(n) with all roots integers in [-1, t+r] and m_{t+r} = 1; hence for any shift s >= t+r, nonnegativity of the coefficients of Q(m+s) implies it for D(m+s).
domain: verified at (t,r) = (2,3),(1,4),(4,3),(3,4),(2,5),(1,6),(1,3),(2,4),(3,3),(1,5),(2,6),(3,5)
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-30
dependencies:
evidence:
  - exact factorisation over Q at twelve (t,r) pairs, degrees 38 to 635
  - every root an integer in [-1, t+r]; simple root exactly at n = t+r in all twelve
  - deg Q is 2.3 to 2.6 times smaller than deg D
  - Q(m+t+r) nonnegative in all 6 odd cases and in none of the 6 even ones, so the parity lives inside Q
references:
---

The reduction step is a PROOF given the factorisation: under a shift s >= t+r every linear
factor becomes m + (nonnegative), and a product of such has nonnegative coefficients. What
is COMPUTATIONALLY_VERIFIED rather than proved is that the factorisation has that shape for
every (t,r) -- it should follow from e_j(n) vanishing for n <= j, which is not yet written
out.

Consequence: (U2) reduces to (U2-core), the same statement about Q, at two-fifths of the
degree.
