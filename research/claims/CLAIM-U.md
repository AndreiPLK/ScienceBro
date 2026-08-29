---
id: CLAIM-U
statement: For every t >= 1 and r >= 3 the polynomial D_{t,r}(m + t + r + 3) has all nonnegative coefficients.
domain: all t >= 1, r >= 3
status: CONJECTURED
last_verified: 2026-08-30
dependencies:
evidence:
  - holds on all 48 proved rungs (t = 1..8, r = 3..8), degrees 38 to 6137
  - the shift excess obeys an exact parity law: 0 when t and r have opposite parity, 2 or 3 when the same
references:
---

(U) implies the ENTIRE log-difference hierarchy on its whole domain, because
`t + r + 3 <= 2(t+r) + 1` whenever `t + r >= 2` and the latter is the domain requirement
(the difference window inside the first half).

So the hierarchy -- and with it conjecture (B), which is the rung r = 3 -- reduces to one
coefficient-positivity statement about an explicit polynomial family.
