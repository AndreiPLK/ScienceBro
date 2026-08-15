# THE MASTER FORMULA — every knife of the closed-string family in one line

Date: 2026-08-15. Status: derived + verified (see battery below). Candidate core
of paper 3.

## Statement

For the CHR graviton family (mu(n) = (n+lam-1)/lam, squared-Pochhammer
residues), the partial wave on ANY trajectory l = 2n-2j (j = 2, 3, ..., n-1)
satisfies, for D > 3, lam > 0:

sign a_{n, 2n-2j} = (-1)^{j-1} * sign SUM_{i=0}^{j-1} (-1)^i
    E_{2(j-1-i)}(n) * (2n-2j+2i)! / (i! 2^i) * s^{2i}
    * PROD_{r=i}^{j-2} (D + 4n - 4j - 1 + 2r)

where s = lam + n - 1 and E_{2t}(n) = |e_{2t}| of the doubled multiset
{n-2k : k=1..n-1} (generating polynomial PROD_k (1 + (n-2k) z)^2).

## Derivation (three ingredients)

1. Residue root structure: the level-n residue is proportional to Q(x)^2 with
   Q roots x_k = (n-2k)/s -> the x^{2n-2-2t} coefficient of Q^2 is
   (-1)^t E_{2t}(n) s^{-2t} times a positive factor (parity: only even t).
2. Monomial-Gegenbauer integral (exact, re-derived symbolically via beta
   functions): I(l+2u, l)/I(l, l) = (l+2u)! / (l! u! 4^u (alpha+l+1)_u),
   alpha = (D-3)/2. The Pochhammer (alpha+l+1)_u is the ONLY D-dependence.
3. Clearing (alpha+l+1)_{j-1} across the j contributing monomials produces the
   ladder tails PROD (D + c + 2r), c = 4n-4j-1, with the factorial weights
   (2n-2j+2i)!/(i! 2^i) (the 2^i from converting half-integer Pochhammer
   factors to integer ladder factors).

Special cases: j=2 reproduces the trajectory law T_n (paper 2, theorem);
j=3 reproduces Bhat = alpha*u(u-2) - G*u*s^2 + s^4 with all its "magic"
relations (R=8mA, W=A(16m^2-1), V=P(4m+1)) as ladder identities.

## Verification battery (all exact arithmetic)

- 21/21 symbolic matches against independently extracted brackets:
  j=2 (n=3..11, vs the published T_n law), j=3 (n=4..9), j=4 (n=5..10),
  j=5 (n=6) — match up to positive constant in every case.
- Overdetermination: at j=5, n=6 the ladder has 5 dof vs 16 monomials — all 16
  match.
- Sign grid vs the exact evaluator: 702/702 across j=2..6, n=4..10,
  lam in {1/4..7}, D in {4..36}, INCLUDING j=6 which was never symbolically
  extracted (blind prediction).
- Blind-level test for j=3 law earlier: 2052/2052 (n=10..12 unseen).

## What it buys

- The complete positivity anatomy of the family: every trajectory's kill
  region is the sign set of an explicit degree-(j-1)-in-D ladder polynomial.
- The completeness conjecture (paper 2) becomes a concrete finite question:
  does any j >= 3 ladder go negative above the j=2 envelope? (j=3: NO —
  window-vs-shore scan, worst margin 2.17 dims; j>=4 scan = next slice.)
- Scripts: lab/tj_bracket.py (extractor), lab/t2n6_law_check.py,
  results/T2n6_brackets.json, results/T2n8_brackets.json,
  results/t2n6_window_vs_shore.json.
