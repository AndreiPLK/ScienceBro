# Leg (a), uniformly in the depth, reduced to one lemma

*2026-08-30, working on Step 1 of `THE_THEOREM.md`. The reduction below is proved; the
lemma it ends at is measured, and this file says exactly which is which.*

## The reduction (proved)

The verified coefficient formula makes each `y`-coefficient an alternating sum,

    c_k = (-1)^{J-1+k} den^k SUM_{i=0}^{L-1} (-1)^i tau_i,        L = J - k,
    tau_i = E_{J-1-i} * poch_i * s^{2i} * den^i * e_{J-1-i-k}(A_i .. A_{J-2}).

**Step 1 — the alternating sum is a finite difference.** Put `phi_i = tau_i / C(L-1, i)`.
By the classical identity `SUM_i (-1)^i C(m,i) f(i) = (-1)^m Delta^m f(0)`,

    SUM_i (-1)^i tau_i = (-1)^{L-1} Delta^{L-1} phi (0).

**Step 2 — the signs cancel identically.** Since `L = J - k`,

    (-1)^{J-1+k} * (-1)^{L-1} = (-1)^{J-1+k} * (-1)^{J-k-1} = (-1)^{2J-2} = +1,

with no dependence on the parity of `J` or `k`. Therefore

    c_k = den^k * Delta^{L-1} phi (0)          exactly, at every depth and every k.

Since `den = kk(kk-2) >= 53 * 51 > 0` on the region, **the sign of every coefficient is
the sign of one top finite difference**.

**Consequence.** If `phi` is absolutely monotone in `i` — every forward difference
nonnegative — then `c_k >= 0` for every `k` at every depth simultaneously. That is leg (a),
uniformly in `J`, which is exactly what Step 1 of the keystone needs.

## Two exact simplifications found along the way

**The `A_r` form an arithmetic progression.** `A_r = A_0 + 2 den r`, difference exactly
`2 den`, verified numerically to machine precision.

**The elementary function stops growing.** Since the index `J-1-i-k` equals
(number of terms) minus `k`, the reciprocal identity `e_{N-k}(x) = (PROD x) e_k(1/x)` gives

    e_{J-1-i-k}(A_i..A_{J-2}) = [PROD_{r=i}^{J-2} A_r] * e_k(1/A_i, ..., 1/A_{J-2}),

with **`k` fixed**. Verified, 0 mismatches. So

    tau_i = PROD * E_{J-1-i} * poch_i * (s^2 den)^i * e_k(1/A_i..) / PROD_{r<i} A_r.

## The lemma, named

> **Lemma A (absolute monotonicity).** On the far-below region, the sequence
> `phi_i = tau_i / C(L-1, i)` satisfies `Delta^j phi >= 0` for every `j`.

**Status: measured, not proved.** 378 of 378 (point, `k`) combinations at `J = 9`, and
earlier 2520 combinations across `J = 6, 8, 9, 10, 12`, with zero violations. An
adversarial sweep over region corners and extreme values is running.

## The route that is now closed

Absolute monotonicity is preserved by products — by the Leibniz rule for finite
differences, every term of `Delta^m(ab)` is nonnegative when `a` and `b` are absolutely
monotone. So the obvious proof is to factor `phi` into absolutely monotone pieces. That
does not work, and the measurements say so precisely:

| factor | absolutely monotone |
|---|---|
| `poch_i` | 378/378 |
| `(s^2 den)^i` | 378/378 |
| `G = poch_i (s^2 den)^i / PROD_{r<i} A_r` | **378/378** |
| `E_{J-1-i}` | 0/378 |
| `e_k(1/A_i..)` | 54/378 |
| `1 / PROD_{r<i} A_r` | 0/378 |
| `tau_i` itself | 0/378 |
| **`phi_i = tau_i / C(L-1,i)`** | **378/378** |

And the complementary half does not split either — `E*R/C`, `E/C`, `R/C` and
`E*PROD*R/C` are all 0 of 378.

So `phi`'s absolute monotonicity is a **joint** property of factors that individually lack
it, and the binomial division is essential rather than cosmetic. A proof will not come from
factorisation.

## What today produced, stated plainly

* **Proved:** `c_k = den^k Delta^{L-1} phi(0)`, exactly, every depth, every `k`, with the
  sign ambiguity removed identically. Leg (a) is now a single statement about one finite
  difference instead of a per-depth certificate.
* **Proved:** the two structural simplifications (arithmetic progression, reciprocal
  identity), which is what makes `phi` explicit.
* **Measured:** Lemma A.
* **Closed:** the product route to proving Lemma A.

Step 1 of the keystone is not finished. It is now one named lemma with an explicit
formula, which is a different situation from where the day started.

## A false start, recorded

The first guess was that the `tau_i` simply decrease, which would make the alternating sum
nonnegative term by term. That was refuted in minutes — but the instrument that refuted it
also failed its own self-check, because the check compared against the wrong expectation:
leg (a) says the negative MONOMIAL sits at `k = J-2`, not that `c_{J-2}` is negative at
region points. The instrument was right and the expectation was wrong. Both were fixed
before any conclusion was recorded.


## Afternoon of 30 August: Lemma A does not come from generic sequence conditions

`phi` satisfies three natural conditions, each verified on 2520 (point, `k`) combinations
across `J = 6, 8, 9, 10, 12`, with zero exceptions:

* `R_i = phi_{i+1}/phi_i >= 1`;
* `R` is increasing;
* `R` is log-convex.

On paper the first two already give `Delta phi >= 0` and `Delta^2 phi >= 0`. They do not
give the rest: **as general facts about sequences, all three together are insufficient.**
Random search produced counterexamples in both cases — for `R >= 1` and increasing, within
1112 tries; for `R >= 1` and log-convex, within 25978. So no generic criterion of this shape
will prove Lemma A.

Nor does the ratio decompose. Writing `R_i` as the explicit product

    R_i = [E_{J-2-i}/E_{J-1-i}] * [poch ratio] * (s^2 den) * [1/A_i]
          * [e_k(1/A_{i+1}..)/e_k(1/A_i..)] * [(i+1)/(L-1-i)],

only the constant factor `(s^2 den)` is both `>= 1` and increasing. The Pochhammer ratio is
`>= 1` but not increasing; `(i+1)/(L-1-i)` is increasing but not `>= 1`; the central
factorial ratio and `1/A_i` are neither. **`R`'s good behaviour is a balance between
growing and shrinking factors, not a property any of them has.**

### What that says about the programme

The awkward factor is `E_{J-2-i}/E_{J-1-i}` — the ratio of consecutive central factorial
numbers. That is the same quantity the Newton-excess lemma of Gap 2 exists to control.

So **Gap 1 and Gap 2 are not independent.** Both come down to controlling consecutive
ratios of the central factorial numbers, from opposite directions. A bound good enough for
one is likely to serve the other, and the programme should stop treating them as separate
problems.


## And the inequality is razor-thin

Making the balance explicit turns Lemma A's "R increasing" half into a single inequality
with no slack to spare.

The awkward factor `E_{t-1}/E_t` decays as `i` grows, and the rate of that decay is exactly

    [E_{t-2}/E_{t-1}] / [E_{t-1}/E_t] = E_{t-2} E_t / E_{t-1}^2 = 1 / rho_{t-1},

where `rho` is the **Newton excess of the central factorial numbers**. So

> `R` is increasing  <=>  (product of the other factor ratios)  >=  `rho_{t-1}`.

`E` is log-concave — classical, since its generating polynomial is real-rooted — so
`rho >= 1` and the inequality is not free.

**Measured margin: 1.0017.** The left side exceeds the right by under two parts in a
thousand, uniformly across the sampled points, with `rho` running from 1.20 to 1.39 and the
other-ratios tracking it almost exactly.

Three things follow.

* It explains why every generic criterion failed today. The inequality is nearly tight, so
  no structural argument with slack in it can reach.
* A proof must be **quantitative and sharp**, not qualitative.
* The link to Gap 2 is not a family resemblance. A sharp bound on the Newton excess is
  precisely what Lemma A needs, with almost no room, which is the strongest evidence yet
  that the two gaps are one.

It is also the best place to hunt for a counterexample: any point where the margin drops
below 1 kills Lemma A outright. A broad scan over depths `J = 6..13` and region extremes is
running.
