---
id: CLAIM-U2
statement: For every t >= 1 and r >= 3 the polynomial D_{t,r}(m + 2(t+r) + 1) has all nonnegative coefficients.
domain: all t >= 1, r >= 3
status: CONJECTURED
last_verified: 2026-08-30
dependencies:
evidence:
  - holds on all 98 proved rungs (t = 1..14, r = 3..9), degrees 38 to 18936
  - slack from 3 to 24 and growing: the excess grows like r/4, the bound like 2(t+r)
  - the excess is exactly 0 on all 49 rungs where t+r is ODD, i.e. exactly when the centred spectrum at n = t+r contains no zero; 49 rungs on each side, no exceptions
references:
---

Well posed because shifts are monotone: if P(m+s) has nonnegative coefficients then so
does P(m+s') for s' > s. So this says the needed shift never exceeds the domain bound
2(t+r)+1, which is the requirement that the difference window lie in the first half.

It implies the ENTIRE log-difference hierarchy on its whole domain, and with it
conjecture (B), which is the rung r = 3. It replaces CLAIM-U, which was false.
