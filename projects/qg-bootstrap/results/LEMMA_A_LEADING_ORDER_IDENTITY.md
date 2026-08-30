# Lemma A: the inequality is an identity at leading order, and the 1/n term decides it

*2026-08-30 afternoon. The sharpest structural statement the far-below leg has reached.*

## Where this sits

`LEG_A_REDUCED_TO_ONE_LEMMA.md` proves `c_k = den^k Delta^{L-1} phi(0)` and reduces leg (a),
uniformly in the depth, to Lemma A: `phi` is absolutely monotone. Its increasing half is
exactly

    (product of the other factor ratios)  >=  rho_{t-1},     t = J - 1 - i,

with `rho = E_{t-1}^2 / (E_{t-2} E_t)` the Newton excess of the central factorial numbers.
The measured margin was `1.0017` — under two parts in a thousand, which is why no argument
with slack in it has reached.

## The reason it is thin: both sides have the same limit

As `n` grows with everything else fixed, **both sides converge to the same value, and that
value is elementary**:

    lim (other ratios) = lim rho_{t-1} = t / (t - 1),      t = J - 1 - i.

Verified at **73 combinations** of `(J, k, i)` with `J = 6, 9, 12`, by Richardson
extrapolation from `n = 548` and `n = 1548`. The two limits agree to `1e-6`, which is the
extrapolation's own truncation error. The value is independent of `k` — the same number
appears in every `k` row.

**The `rho` side is provable in one line.** For fixed `t` and large `n`,
`E_t ~ S^t / t!` with `S = SUM_k b_k`, so

    rho = E_{t-1}^2 / (E_{t-2} E_t)  ->  t! (t-2)! / ((t-1)!)^2  =  t / (t-1).

The other side must therefore have the same limit, and it does.

## What Lemma A has become

The inequality is an **identity at leading order plus a correction of size `1/n`**:

    (other ratios) - rho  =  c(J, k, i) / n  +  O(1/n^2),

measured with `(difference) * n` running from `0.099` at `n = 44` down to `0.078` at
`n = 1004`, and the margin itself behaving as `1 + c'/n` with `c'` around `0.07`, nearly
independent of `J`.

> **So the increasing half of Lemma A is exactly the statement that the `1/n` coefficient
> of the difference is positive.**

That is a completely different kind of task from the raw inequality. It is one explicit
expansion, of the same species as the effective expansion Gap 2 needs — which is now the
third independent sign that the two gaps are one problem.

## Honest status

* **Proved:** `c_k = den^k Delta^{L-1} phi(0)`; the reciprocal identity; the arithmetic
  progression; the `rho` limit `t/(t-1)`, in one line.
* **Measured:** that the other side shares that limit (73 combinations, agreement to the
  extrapolation error); that the difference is `O(1/n)` with a positive coefficient.
* **Open:** the sign of that coefficient, in general. That is now the whole of Lemma A's
  increasing half.
* **Not yet done:** the other half of absolute monotonicity — the higher differences beyond
  the second. `R >= 1` and `R` increasing give orders 1 and 2 only.

## Five routes that died getting here, all today

The `tau_i` decreasing; `phi` factoring into absolutely monotone pieces; `c_t` a positive
moment sequence; copositivity of the knife's Hankel matrix; generic sequence criteria
(`R >= 1`, increasing, log-convex — all three insufficient, with explicit counterexamples).
Each is recorded in `research/dead_routes.md` with what killed it.


## The 1/n coefficient, computed — and it is a single constant

Extracting the coefficient by Richardson in `1/n` from `n = 1048` and `n = 3048` gives a
structure much simpler than expected. Write `t = J - 1 - i`.

**The coefficient depends only on `t`, and only through the same factor `t/(t-1)`.**
Across `J = 9` and `J = 12` and every `k` tested, `c * (t-1)/t` is one constant:

| `t` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| `c * (t-1)/t` | .066025 | .066025 | .066025 | .066025 | .066025 | .066025 | .066025 | .066025 | .066025 |

So, writing that constant `K`,

    (other ratios) - rho  =  (K / n) * t/(t-1)  +  O(1/n^2),

and since the common limit is itself `t/(t-1)`,

    (other ratios) / rho  =  1 + K/n + O(1/n^2).

**The whole increasing half of Lemma A is the single statement `K > 0`.**

## `K` across the region

`K` does not depend on `y` at all — identical to eight digits at `y = 0, 3, 500`. It barely
depends on `thL` (`0.0660246` to `0.0660248` across `thL = 0, 1/2, 1`). It depends on `K3`
only through the ratio `K3/v`, and monotonically:

| `K3/v` | 0 | 0.01 | 0.1 | 0.5 | 1 | 10 | 100 | `10^5` |
|---|---|---|---|---|---|---|---|---|
| `K` | .06602 | .06699 | .07517 | .10193 | .12266 | .18391 | .19819 | .20000 |

**`K` is positive across five orders of magnitude**, rising monotonically from an infimum
near `0.0660` at the corner `K3 = 0` to what looks like exactly `1/5` in the limit.

## Status, stated exactly

* **Measured, and strongly:** `K > 0` on the whole region, bounded below by about `0.066`,
  independent of `y` and of `k` and of `i` beyond the factor `t/(t-1)`.
* **Consequence, if the expansion is made rigorous:** the increasing half of Lemma A holds
  for all sufficiently large `n`, uniformly in the depth, with an explicit constant.
* **What a proof still owes:** the expansion itself with a bounded remainder — the `O(1/n^2)`
  term — which is exactly the species of estimate Gap 2 needs. Fourth independent sign that
  the two gaps are one problem.
* **Still untouched:** the higher differences. `R >= 1` and `R` increasing give absolute
  monotonicity only to order 2.

**A constant not claimed.** The infimum reads `0.06602468` and the limit reads `0.19999676`,
which is `1/5` to five digits. `1/5` is worth stating as a measurement; the infimum is not
identified, and no closed form is asserted for either. The programme has been bitten once
already by naming a constant from a fit.
