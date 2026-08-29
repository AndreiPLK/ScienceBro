# The theorem, stated exactly: what is proved, and what the remaining distance is

*2026-08-29, end of shift. Every hypothesis below names the artefact that carries
it. Nothing here is a plan; it is the statement as it stands tonight.*

## Proposition 1 (the reduction). Unconditional, every depth.

Let `N(y)` be the far-below polynomial of the knife at depth `j = J`. If

* **(a)** every `y`-coefficient `c_k` with `k != J-2` is nonnegative, and
* **(R)** `4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0` on the region,

then `N(y) > 0` for all `y >= 0`.

*Proof.* By (a) the only negative coefficient is `c_{J-2}`. Group it with its two
neighbours: `c_{J-1} y^{J-1} + c_{J-2} y^{J-2} + c_{J-3} y^{J-3}` is `y^{J-3}` times
a quadratic in `y` whose discriminant is `c_{J-2}^2 - 4 c_{J-1} c_{J-3} <= 0` by (R).
A quadratic with positive leading coefficient and nonpositive discriminant is
nonnegative, and the remaining terms are nonnegative by (a). ∎

This is a proof, not a measurement, and it holds at every depth. Everything below is
about supplying its two hypotheses.

## Theorem 2 (what that gives today). Depths 9 to 16.

For `j = 9, 10, ..., 16`, in the far-below region with `n >= 2J-3`,

    N(y) > 0   for every y >= 0.

*One ingredient is now unconditional.* `c_{J-1} > 0` at every depth, by hand and
with no computation: the coefficient formula collapses to one term there, and it is
a product of `den = kk(kk-2) >= 53*51` and an elementary symmetric function of
squares (`UNIFORM_TOP_COEFFICIENT.md`).

*Hypotheses discharged:* (a) certified per depth over `j = 9..16`
(`farbelow_negative_pattern_j*.json`, and independently by the faster coefficient
route, `farbelow_coeff_signs_j*.json`); (R) certified
(`repair_certificate_j*.json`, audited by `lab/certificate_audit.py`).

*Independent check of the conclusion, not of its parts:* `N(y)` evaluated exactly at
252 region points crossed with `y` up to `10^5`, at `j = 9, 11, 13, 15` — zero
non-positive values (`farbelow_endtoend_j*.json`).

## Where the ceiling actually is

It is **(a)**, not (R).

| depth | (R) | (a) |
|---|---|---|
| 7 – 16 | certified | **certified** |
| 17 – 50 | certified at 7, 9, 12, 16, 20, 25–32, 35, 40, 45, 50 | not yet computed |

(R) is certified at 17 depths up to 50; (a) has been computed only to 16 because it
used to require assembling the whole polynomial. That cost is now down — the
verified coefficient formula gives each `c_k` on its own — so the depth range of
Theorem 2 is currently limited by machine time, not by mathematics. Runs at
`j = 17, 18` are in progress.

## The two gaps to a depth-uniform theorem

**Gap 1 — uniformity in `J`.** Both (a) and (R) are certified depth by depth. A
keystone needs one argument covering all `J`. For (R) the reduction is done: its
leading obstruction is `J`-uniform given a Newton-excess lemma plus an elementary
inequality, and the elementary half is **proved** (`elementary_half_check.json`, two
independent proofs).

**Gap 2 — the Newton-excess lemma at finite `n`.** It asks `M_{n,t} <= 2`. Its
asymptotic half is **proved** (`LIMIT_SHAPE_BOUND.md`). Its finite-`n` half needs an
effective expansion with an explicit remainder.

## What today moved, precisely

Gap 2 was, this morning, "an asymptotic for a ratio of elementary symmetric
functions with an explicit remainder" — a statement with no established shape and no
effective literature. Tonight it is:

* the family is a **tilted Poisson-binomial**, and the split `M = n(rho beta - 1)` is
  **exact at finite `n`** (`POISSON_BINOMIAL_VIEW.md`);
* `f` is its **reciprocal tilted variance** — verified, gap exactly `O(1/n)`;
* `g` is the **Edgeworth term, written out**:

      log rho = 1/K'' + K''''/(2 K''^3) - K'''^2/K''^4,

  in the tilted cumulants `K''`, `K'''`, `K''''`. Tested as a rate, not by eye: with
  this term the residual against exact `rho` falls like `1/n^3` (column flat to ~5%
  over `n = 41..201`), while the Gaussian term alone leaves `O(1/n^2)`
  (`edgeworth_prediction.json`).

So Gap 2 is no longer "find the expansion". The expansion is identified and checked;
what a proof still owes is a **remainder bound** for a saddle-point expansion of a
Bernoulli sum — and, by the doubling `F = G^2`, a sum of two i.i.d. halves, whose
cumulants are exactly twice the half's at every tilt.

## Honest summary in one line

Proposition 1 is a theorem for every depth. Theorem 2 is a theorem for `j = 9..16`
and is currently limited by computation, not by mathematics. The depth-uniform
keystone is not proved, and stands on exactly two named gaps, of which one is now
reduced to a remainder estimate for a classical object.
