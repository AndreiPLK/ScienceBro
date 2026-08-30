# The theorem we are going for

*Named and written down on 2026-08-30 so that it never gets confused with the results we
prove along the way. Nothing else in this repository is "the theorem".*

## Name

**Pluzhnik's Depth-Uniform Positivity Theorem**
(рус.: **теорема Плужника о положительности на всех глубинах**)

Short form in daily use: **the keystone**.

## Statement

For the CHR graviton family, the knife

    K_r = SUM_t (-1)^t c_t e_t(b),      c_t = (r)_t (H-r)_t / [ (n-1)_t (n-3/2)_t ],
    b_k = (n-2k)^2 / s^2,   s = lambda + n - 1,   H = (D + 4n - 7)/2,

is **strictly positive on the whole admissible parameter region, at every depth `j`
simultaneously** — one argument covering all depths, not a certificate per depth.

## Why this is the goal and not something smaller

Positivity at every depth is a statement about **which gravitational amplitudes are
admissible at all**. Proving it removes an entire class of candidate theories, which is
one of the six accepted currencies of progress in `NORTH_STAR.md`. A certificate at
depth 18 removes nothing: there are infinitely many depths, and the next one is always
open.

## What stands today

**Proved, every depth:**

* Proposition 1 — the grouping reduction: given (a) and (R), the far-below polynomial is
  positive. Two of its original four ingredients turned out to be free.
* `c_{J-1} > 0` on the whole region, at every depth, in one line.

**Certified, depth by depth — this is the part that is NOT yet the theorem:**

* (R), the repair inequality: 19 depths from 7 to 50.
* leg (a), the localisation of the negative coefficient: `j = 9..18`.
* Theorem 2, the far-below region closed at `j = 9..18`.

## The two gaps, named

**Gap 1 — uniformity in the depth.** Both (a) and (R) are supplied per depth. For (R) the
reduction is done: its leading obstruction is depth-uniform given a Newton-excess lemma
plus an elementary inequality, and the elementary half is proved. For (a) the current
line of attack is that `c_k` is an alternating sum whose terms decrease away from
`k = J-2`.

**Gap 2 — the Newton-excess lemma at finite `n`.** `M_{n,t} <= 2`. The asymptotic half is
proved; the finite half needs an effective expansion with an explicit remainder. The shape
of that expansion is now identified — `f` is the reciprocal tilted variance of a Bernoulli
sum, `g` is the Edgeworth term written out — and what a proof still owes is the remainder
bound.

## The rule this file exists to enforce

Results proved along the way are **named results, not the theorem**. As of today those
include: the no-Pólya-frequency theorem, the 98 rungs of the log-difference hierarchy, the
`e`/`p` complementarity, and the minor representation of `H_{N,t}`. Each is genuinely new
and each is worth publishing. **None of them is Pluzhnik's Depth-Uniform Positivity
Theorem**, and no document in this repository may imply otherwise.

The keystone is proved when, and only when, a single argument covers every depth. Until
then this file says so.
