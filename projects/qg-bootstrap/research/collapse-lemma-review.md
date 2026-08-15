# Adversarial review: the binomial collapse lemma (paper 5)

Role: domain-critic. Date: 2026-08-15. Default stance: refute.
Objects: `research/collapse-lemma.md`, `paper5/main.tex`,
`lab/collapse_zones.py`, `results/collapse_zones.json`.
Attack battery: `lab/attack_collapse.py` (independent reimplementation,
gates frozen in its docstring).

EXECUTION STATUS: the numeric battery was WRITTEN but NOT EXECUTED in this
review session (shell access disabled for the reviewing agent). Every
numeric statement below is either (a) hand-verified algebra, (b) read off
the lab's existing artifact `results/collapse_zones.json`, or (c) marked
PENDING. `results/attack_collapse.json` does not exist yet; do not cite it
until `python lab/attack_collapse.py` has run (exit 0 iff no falsification).
No numbers in this file are invented.

## 1. What survived the attack (hand-verified)

- **Term-ratio formula.** Re-derived `term_{i+1}/term_i` from the bracket
  definition; it matches paper Eq. (2) exactly (factorial quotient
  `(2n-2j+2i+2)(2n-2j+2i+1)`, weight quotient `1/(2(i+1))`, tail quotient
  `1/(D+4n-4j-1+2i)`).
- **Limit algebra.** With E-ratio -> `(j-1-i)/Sigma`, `Sigma ~ m^3/3`:
  `ratio_i -> -[(j-1-i)/(i+1)] * 6 rho^2/(delta+4)`; binomial sum gives
  `(1-X)^{j-1}`. The constant 6 checks out.
- **T_8 = 94** (the "honest limits" spot check in collapse-lemma.md):
  j=2, n=8, lam=5 gives root `D = 91*144/112 - 23 = 94` exactly. Correct.
- **Tangency numbers.** `d/dm[6 s^2/m - 4m] = 12 rho - 6 rho^2 - 4 = 0`
  yields `rho* = 1 + 1/sqrt3`; envelope `(6 rho*^2 - 4)/(rho* - 1)
  = 12 + 4 sqrt3`. Both headline numbers are right (but see E2 below:
  the printed derivation in the paper is garbled).
- **Sign conventions** are internally consistent between
  collapse-lemma.md (`sign(a) = (-1)^{j-1} sign(B_j)`) and
  `collapse_zones.py` (flip for even j), and `term_0 > 0` always, so
  normalizing by `term_0` is legitimate.
- **Self-consistency of the sqrt(m) splitting** (new argument, supports the
  paper): all three `O(1/m)` corrections to `ratio_i` are LINEAR in the
  term index i at first order (E-ratio correction `(j-2-i)*kappa`,
  factorial pair `(15-4j+4i)/(2m)`, ladder `(11-4j+2i)/((delta+4)m)`).
  Hence in `B_j/term_0 = sum_i C(j-1,i)(-X)^i (1 + G_i/m + ...)` the
  first-order coefficient `G_i` is quadratic in i, and the (j-1)-th finite
  difference at X=1 annihilates every 1/m^r term whose i-degree (= 2r) is
  below j-1. Consequences:
  (i) at X=1 the deviation is `O(m^{-ceil((j-1)/2)})`, NOT just O(1/m);
  (ii) roots split by `O(m^{-1/2})` in X, i.e. `O(sqrt m)` in D. A GENERIC
  O(1/m) perturbation of a (j-1)-fold root would instead split it by
  `O(m^{-1/(j-1)})` in X = `O(m^{(j-2)/(j-1)})` in D, which is much wider
  than sqrt(m) for j >= 4. So the paper's sqrt(m) claim is true only
  because of this cancellation, which the paper asserts but never argues.
  PENDING numeric check: W1 gate (order at X=1 should measure `j//2`).
  Weak corroboration from the lab's own artifact: j=7,8 outer band edges
  scale by about 2.0-2.3 from n=20 to n=100 (sqrt(97/17) = 2.39;
  the m^{2/3} alternative predicts 3.2).

## 2. Errors found (each independently checkable)

- **E1 (paper, abstract line 24-26 and section 2).** Even-j band
  bookkeeping is wrong as written. The abstract: "splits at subleading
  order into exactly floor(j/2) thin negativity bands; even knives
  otherwise kill only on the already-dead side" -- this counts
  floor(j/2) thin bands PLUS a half-line for even j. Their own artifact
  contradicts it: j=4 at every level has 1 finite band + 1 semi-infinite
  region = 2 = floor(4/2) TOTAL. Correct statement: j-1 simple roots;
  odd j: (j-1)/2 thin bands; even j: (j-2)/2 thin bands plus the
  semi-infinite region. `expected_bands = j//2` in the battery counts the
  half-line as a band (the code comment admits this; the abstract hides it).
- **E2 (paper, section 2, "The tangency explained").** Algebraic garble:
  "Minimizing $6\rho^2m-4m$ ... gives $12\rho-6\rho^2\cdot\rho^{-1}\cdot
  \ldots$". The correct stationarity condition is `12 rho - 6 rho^2 - 4
  = 0`. The conclusion (rho*, envelope) is right; the displayed reasoning
  is not printable as is.
- **E3 (collapse-lemma.md, Consequences item 2).** Kill-region inequality
  INVERTED for even j. The note says "even j: kill region = {X > 1}".
  Their own zone data show the even-j semi-infinite kill region on the
  D > D_crit side, which is X < 1. Derivation: large D => X small =>
  `(1-X)^{j-1} > 0` => `B_j > 0` => `a = -B_j < 0` (kill) for even j.
- **E4 (collapse-lemma.md, ingredient (a)).** "correction bounded via
  Newton inequalities ... the correction is O(m) against Sigma=O(m^3)".
  Writing `E_{2(t-1)}/E_{2t} = t/(Sigma + corr)`, the expansion gives
  `corr ~ -(3/5)(t-1) n^2`, i.e. Theta(m^2), not O(m). The relative
  O(1/m) conclusion is unaffected, but the stated order is wrong.
  PENDING numeric confirmation (part1 `corr_over_n2` should flatten at
  about `-0.6 (t-1)`).
- **E5 (paper + md, the proof gap in estimate (i)).** "Newton
  log-concavity of the E-sequence controls the correction" proves only
  ONE side. Log-concavity of `e_t` (true for elementary symmetric
  functions of nonnegative reals, here the squares multiset
  `{(n-2k)^2}`) gives the clean LOWER bound
  `E_{2(t-1)}/E_{2t} >= [N/(N-t+1)] * t/e_1 >= t/Sigma` (ratio chain on
  the normalized sequence), with no matching upper bound at any rate.
  The needed two-sided estimate follows instead from the elementary
  repeated-index bound: for nonnegative reals,
  `0 <= 1 - t! e_t / e_1^t <= C(t,2) p_2 / e_1^2`
  (count ordered t-tuples with a repeated index), and here
  `p_2 <= (n-2)^2 e_1`, so `p_2/e_1^2 <= 3/m (1+O(1/m))`; sharper,
  `p_2/e_1^2 = (9/5)/m (1+o(1))`, predicting
  `m * [E-ratio * Sigma/t - 1] -> (9/5)(t-1)`. This is a two-line lemma
  with explicit constants; with it, ingredients (ii) and (iii) being
  trivial, the theorem for fixed j is honestly provable at rate O_j(1/m).
  PENDING numeric check of the constant (W4 gate).
- **E6 (paper, abstract + Verification section).** Overstatements:
  (a) "every clustering offset matches the prediction ... zero
  deviations" -- the battery's only deterministic gate is band COUNTS;
  offsets are recorded, never compared to any predicted value (the
  clustering prediction has no constants to match). (b) "levels up to
  n=100" / caption "levels 20..100" -- the battery is 7 specific
  (n, lambda) pairs, one lambda per level, all with rho in [1.09, 1.15];
  the high-rho regime near rho* (where the tangency story lives) was
  never scanned. (c) The lab's Dmax = 2*D_crit + 60 truncation is
  untested against bands beyond the window (my F8 gate probes this).
- **E7 (minor).** collapse-lemma.md is dated 2026-08-16, in the future at
  review time. Also: no artifact anywhere in the repo DIRECTLY tests
  `B_j/term_0 -> (1-X)^{j-1}` -- collapse_zones.json tests sign structure
  only. The central limit claim currently has zero direct numeric
  evidence; part2 of the attack script fills this hole.

## 3. Scoping caveats for the theorem statement

- **Pointwise vs useful near X=1.** As stated (fixed rho, delta) the
  O_j(1/m) rate survives even at X=1 (where the deviation is in fact
  smaller, see section 1). But near X=1 the LIMIT is smaller than the
  error for any practical m: e.g. 1-X ~ 0.01, j=5 gives limit
  `(1-X)^4 ~ 1e-8` against error ~ C/m -- the limit value is not the
  dominant term until m ~ 1e8. The theorem's real content near the
  critical surface is the subleading (Hermite-type) structure, which is
  asserted, not proven. Recommend one scoping sentence in the paper.
  PENDING quantification: part2 case "X=1-eps" records
  `dev_over_limit_m320`.
- **Uniformity in j.** The correction in (i) scales like `t^2/m`
  (through `C(t,2) p_2/e_1^2`), so the error constant grows at least
  like j^2; the "uniform in j" organization of the completeness tail
  needs j = o(sqrt m) or better, and the paper's "uniformly in j"
  phrasing in the abstract should be scoped. Consistent with the md's
  own admission that uniform-in-j remainder bounds are "in progress".
- **Formal domain.** Along s = rho*m the implied lambda = (rho-1)m - 2 is
  negative for small m; the small-m rows of any convergence table are
  formal-polynomial checks, physical for m > 2/(rho-1) only. Irrelevant
  to the limit, worth a footnote.

## 4. Numeric battery (frozen, PENDING execution)

`lab/attack_collapse.py`, gates F1-F11 and W1-W5 frozen in the docstring
before first run. Coverage: (1) ratio estimate on m up to 640 with the
predicted constant 1.8(t-1); full log-concavity scan n <= 140; Newton
lower-bound positivity; (2) exact `B_j/term_0 - (1-X)^{j-1}` for j=2..8,
m up to 320, six (rho, delta) cases including X=1 exactly at two rho's,
X = 1-eps, X > 1, rho near rho* and near sqrt(5/3); measured convergence
orders; (3) independent zone battery at n=100 (exact reproduction of the
lab row, including their truncation and rounding), n=120, n=150 with
j up to 10, a high-rho probe (n=120, lam=60, rho ~ 1.53), far-field sign
checks, lab-truncation audit, and a splitting-exponent fit at matched
rho ~ 1.145 across m = 97, 117, 147; (4) T_8 = 94 and tangency numbers.
Artifact: `results/attack_collapse.json`; exit 0 iff no falsification.

## 5. Verdicts (per .claude/rules/claim-gates.md)

- **(a) The three ratio estimates.** Statements (ii), (iii) are trivially
  true. Statement (i) is true as an estimate and I found a complete
  elementary proof route (E5), but the paper's cited mechanism
  (log-concavity) proves only the lower half -- as written this is a
  proof SKETCH with a genuine gap. State: **source-supported**
  (own derivation); "experimentally-supported" only after the battery
  runs; NOT "proved" in the lab's sense until E5's lemma is written out.
- **(b) The limit theorem as stated.** Algebra of the derivation is
  verified by hand; no counterexample mechanism found; my sharper
  analysis (finite-difference cancellation) actively supports it.
  However: labelled "Theorem" with a QED box on a mechanism containing
  gap E5, while the research note admits remainder bounds are "in
  progress" -- this fails the lab's own gate. Relabel **Proposition**
  (with "proof sketch"), or close E5 and keep Theorem. Direct numeric
  evidence for the limit: currently NONE in the repo; state
  **source-supported**, upgrade to experimentally-supported only after
  `attack_collapse.json` (or equivalent) exists with F5/F6 green.
- **(c) The zone-battery interpretation.** The battery itself (band
  counts, j <= 8, 7 low-rho configs) is exact arithmetic and internally
  consistent: **experimentally-supported** for the literal count claim.
  The interpretation is overstated: E1 (even-j miscount in prose),
  E6 (offsets never gated, "levels 20..100" inflation, truncation
  untested, high-rho regime and j >= 9 unexplored). The phrase "zero
  deviations" must be scoped to "band counts equal floor(j/2), where the
  count includes the semi-infinite region for even j".

## 6. Required edits (concrete)

1. main.tex abstract + section 2: fix even-j band count wording (E1);
   replace "every clustering offset matches the prediction" with the
   count-only claim (E6a); replace "levels 20..100" with the actual
   7-config grid (E6b).
2. main.tex "Proof mechanism": replace the log-concavity sentence with
   the repeated-index lemma (E5); fix the minimization garble (E2);
   or relabel Theorem -> Proposition until done.
3. collapse-lemma.md: fix the inverted kill-region inequality (E3),
   the O(m) -> Theta(m^2) correction order (E4), and the file date (E7).
4. Run `lab/attack_collapse.py`; attach `results/attack_collapse.json`
   to the paper's verification section; treat any F-gate failure as a
   blocker for release.

## 7. Questions for external experts

- Is there a standard reference for the two-sided elementary-symmetric
  ratio estimate (E5's lemma) to cite instead of proving inline?
  (It is folklore-adjacent; a citation would shorten the paper.)
- The Hermite-type subleading structure (Rogers-Szego-like sum with
  q = 1 + beta/m) presumably has known root asymptotics; a citation
  would convert the sqrt(m) splitting from assertion to theorem.
- Does the intended "grand theorem" need uniformity in j up to j ~ n/2?
  If so the t^2/m correction growth makes the present route insufficient
  and this should be said out loud in paper 5.
