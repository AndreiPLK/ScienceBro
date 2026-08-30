---
id: CLAIM-LEADING-IDENTITY
statement: Both sides of Lemma A's increasing half converge to the same limit t/(t-1) with t = J-1-i, so their difference is O(1/n) and the sign of the 1/n coefficient decides the lemma.
domain: J = 6, 9, 12; all k and i tested; limit taken in n
status: COMPUTATIONALLY_VERIFIED
last_verified: 2026-08-30
dependencies:
  - CLAIM-LEGA-REDUCTION
evidence:
  - 73 (J,k,i) combinations, Richardson extrapolation from n = 548 and 1548, the two limits agreeing to 1e-6 which is the extrapolation truncation error
  - the limit is independent of k
  - the rho side is PROVED in one line, E_t ~ S^t/t! giving t!(t-2)!/((t-1)!)^2 = t/(t-1)
  - the difference times n runs from 0.099 at n=44 to 0.078 at n=1004
references:
---

Turns Lemma A's increasing half from a razor-thin inequality (margin 1.0017) into the sign
of one explicit 1/n coefficient -- the same species of statement as the effective expansion
Gap 2 needs.

Still open beyond this: the higher differences of absolute monotonicity. R >= 1 and R
increasing give orders 1 and 2 only.
