---
id: CLAIM-NOPF
statement: For every n >= 4 the 3x3 Toeplitz minor of p on rows (1,2,3) and columns (0,1,2) equals -(4/945) n(n+1)(7n^3-43n^2+58n+120) < 0, so (p_t) is never a Polya frequency sequence.
domain: every integer n >= 4
status: PROVED
proof_artifact: projects/qg-bootstrap/results/THEOREM_NO_POLYA_FREQUENCY.md
last_verified: 2026-08-30
dependencies:
evidence:
  - complete elementary proof in five steps; no certificate, no grid, no numerical step
  - closed forms of e_1,e_2,e_3 checked against direct evaluation at n = 4..59
  - closed form of the minor checked against the determinant at n = 4..60
  - the shift argument re-derived independently via -Num(m+3)
references:
  - Aissen, Schoenberg, Whitney (for the contrast: (e_t) IS a PF sequence)
---

The denominator `(n-1)^3 (n-2)(n-3)` cancels exactly, leaving a degree-five polynomial
with no denominator. With `n = m + 4` the cubic factor becomes `7m^3 + 41m^2 + 50m + 112`,
all coefficients positive.

Kills the total-positivity / LGV route to the log-difference hierarchy: `e` is totally
positive and lacks the hierarchy, `p` has the hierarchy and is provably never totally
positive. See `research/dead_routes.md` DR-09.
