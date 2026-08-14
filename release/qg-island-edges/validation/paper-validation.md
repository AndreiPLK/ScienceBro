# Independent validation of numerical claims — paper/main.tex

- Role: independent validator (did not write the implementation under test)
- Independence: `validate_paper.py` in this folder is a fresh implementation
  written only from the formulas printed in the paper (Eq. (1) residue, angle
  substitution t = alpha(x-1) - mu0, Legendre/Gegenbauer projection) and the
  task statement. It imports NOTHING from `projects/qg-bootstrap/lab` and
  shares no code with it. Only shared dependency: CPython stdlib
  (`fractions.Fraction`, `random`) — unavoidable, documented here.
- Arithmetic: exact rational throughout; every verdict is deterministic
  (no floating point, no statistical tests needed).
- Run metadata: git commit `0df959bf60ef8fee026be01e6ae92fbc7ae0b50a`,
  Python 3.12.10 (`C:/Users/user/ScienceBro/.venv/Scripts/python.exe`),
  Windows 11, 2026-08-14. Command:
  `python validate_paper.py` (exit code 0). Random seed for item 2 frozen at
  20260814 before any results were examined.

## Item 1 — Edge-law razor at (r,w) = (-13/25, 1/2), mu0 = 0, D = 4 — PASS

Residue Eq. (1) projected on Legendre P_{n-1} with t = (n/2)(x-1):

- a_{24,23} = 2134033593750000000000000000000000000000000000000 /
  47624870345780755977511483600418282926532429637940559977 > 0  (exact)
- a_{25,24} = 0  (exactly, in rational arithmetic)
- a_{26,25} < 0  (exact negative rational)

Matches the paper's razor prediction (zero at n = 25, sign change across it)
and the edge law sgn a_{n,n-1} = sgn[n(r+1/2)+w] = sgn[(25-n)/50].

## Item 2 — a_{2,0} sign law sgn a_{2,0} = sgn[3(1+r)(r+w)+1] — PASS

10 random rational (r,w) in the domain 2+r > 0, 1+r+w > 0 (seed 20260814,
rejection sampling). All 10 sign comparisons agree, including two genuinely
negative cases ((r,w) = (22/19, -53/26) and (-3/10, -4/11)), so the check is
not vacuous. 10/10 exact agreements, 0 mismatches.

## Item 3 — The nine casualties at r = -3/5 — PASS

For each w in {1, 11/10, ..., 9/5} (nine values), on the trajectory
l = n-1 in exact arithmetic:

| w     | a_{n,n-1} > 0 for all n < 10w | a_{10w,10w-1} = 0 | first negative n |
|-------|-------------------------------|-------------------|------------------|
| 1     | yes (n = 1..9)                | yes (exact)       | 11 (= 10w+1)     |
| 11/10 | yes                           | yes               | 12               |
| 6/5   | yes                           | yes               | 13               |
| 13/10 | yes                           | yes               | 14               |
| 7/5   | yes                           | yes               | 15               |
| 3/2   | yes                           | yes               | 16               |
| 8/5   | yes                           | yes               | 17               |
| 17/10 | yes                           | yes               | 18               |
| 9/5   | yes                           | yes               | 19               |

All nine first negatives occur exactly at n = 10w+1, with the exact marginal
zero at n = 10w, matching the paper's list w=1 -> (11,10), ..., w=9/5 -> (19,18).

## Item 4 — q-clock spot checks (r = w = 0) — PASS

Implemented fresh from the root structure of CHR Eq. (16): monic residue
prod over roots {[-1]_q, [-2]_q, ..., [-n]_q} with [m]_q = (q^m-1)/(q-1),
angle substitution t = [n]_q (x-1)/2, Legendre projection, scanning n
ascending and l = 0..n ascending:

- q = 6/5: first negative partial wave at (n,l) = (3,0)  — as claimed.
- q = 11/10: first negative at (n,l) = (4,1)  — as claimed (all l at n <= 3
  and l = 0 at n = 4 are non-negative).
- q = 1: no negative coefficient for any n <= 15, l <= n  — clean, consistent
  with the paper's q = 1 control (paper states clean to n = 25; verified here
  to the task's n = 15).

Assumption (documented): the positive overall prefactor of CHR Eq. (16) at
r = w = 0 is taken positive, so signs are computed from the monic root
product. This matches the task specification; the (n,l) positions of first
negatives are unaffected by any positive prefactor.

## Item 5 — D-universality spot at D = 6 — PASS

With Gegenbauer weight (1-x^2)^{(D-4)/2} = (1-x^2) and alpha_G = 3/2, at
(r,w) = (-3/5, 1), mu0 = 0:

- a_{10,9} = 0 exactly (rational arithmetic).

Confirms the dimension-universality of the edge zero (n(r+1/2)+w = 0 at
n = 10) in D = 6, consistent with Theorem 1's claim that the x^{n-1}
coefficient carries no D-dependence.

## Failure map

No failures observed. Boundary-adjacent behavior explicitly probed:
- exact zeros sit precisely on the edge line (items 1, 3, 5) and are exact
  rational zeros, not small numbers;
- sign flips across the zeros are exact (items 1, 3);
- domain boundary: item 2 sampling was restricted to the declared domain
  2+r > 0, 1+r+w > 0; sign law outside the domain was NOT tested here
  (the paper itself restricts the stated laws to the domain).

Not validated here (out of task scope): the 11,994-verdict census, the
depth-40 map, Eqs. (3)-(4) trajectory laws, the n_crit ~ 1.1 (q-1)^{-1/2}
fit across all six q values, the mu0 != 0 stack, and the fixed-spin tail
heuristic. No statement in this report covers those claims.

## Overall verdict: PASS

All five predeclared deterministic checks pass in exact rational arithmetic
using an implementation written independently of the code under test. Reasons:
exact zeros reproduce exactly (not approximately) at all three razor/edge
points including D = 6; the closed-form sign law for a_{2,0} agrees at 10/10
random rational points with both signs represented; all nine casualty
thresholds land exactly at n = 10w+1 with the predicted marginal zeros; and
the q-clock first-negative positions match at both tested q values with a
clean q = 1 control.

Claim-state recommendation: the specific numerical claims covered by items
1-5 are consistent with promotion to `independently-validated` (subject to
the deterministic gate `allowed_claim_promotion` and human approval). This
recommendation does NOT extend to the paper's conjectural or heuristic
statements (Conjecture 1, fixed-spin tails, general-k dichotomy) or to the
untested bulk censuses listed in the failure map.

Reproduce: `C:/Users/user/ScienceBro/.venv/Scripts/python.exe
C:/Users/user/ScienceBro/projects/qg-bootstrap/validation/validate_paper.py`
(exit 0 = all pass). Raw stdout: `run-output.txt` in this folder.
