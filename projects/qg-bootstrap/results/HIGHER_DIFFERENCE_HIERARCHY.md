# The anomaly map, checked: the hierarchy is real, and its "jackpot" needs the reversal

*2026-08-29 night. Artefact: `results/higher_difference_hierarchy.json`, module
`lab/higher_difference_hierarchy.py`. Source: a brief from the parallel chat,
untrusted until checked.*

## H1 — the hierarchy of higher-difference signs

The brief claims `Delta^r log p_t < 0` for **every** `r >= 2` on the admissible
first-half domain, which would make our conjecture (B) — exactly
`Delta^3 log p_{t-1} <= 0` — the first nontrivial member of an infinite family.

Tested exactly. No logarithm is ever taken: the sign of
`Delta^r log p_t = SUM_j (-1)^{r-j} C(r,j) log p_{t+j}` is decided by comparing two
products of rationals, so no float touches a verdict.

| order `r` | cases | negative | not negative |
|---|---|---|---|
| 2 | 396 | 396 | 0 |
| 3 | 372 | 372 | 0 |
| 4 | 348 | 348 | 0 |
| 5 | 324 | 324 | 0 |
| 6 | 300 | 299 | 1 |
| 7 | 276 | 274 | 2 |
| 8 | 253 | 251 | 2 |

**With the whole difference window kept inside the first half, H1 holds: 0
violations**, `n = 9..32`, `r = 2..8`.

The five failures in the table are all from the looser reading, where the index `t`
is in the first half but the window `t..t+r` runs past the midpoint. That is not a
counterexample: it is the brief's own Section 7 showing up, where past the midpoint
the coefficients are governed by the reciprocal spectrum `1/(a+kd)^2`, which is no
longer a squared arithmetic progression.

*A correction to my own first run.* It allowed the window to reach the very end of
the spectrum and produced 19 "violations" — every one of them with `t + r` at the
last index, where for even `n` the multiset contains a zero and `p_N = 0`. My domain
was sloppier than their claim. Recorded because declaring a refutation from a
carelessly chosen domain is exactly the failure this lab keeps meeting.

## H2 — the "potential jackpot", and why the reversal is compulsory

The brief hopes `A_t = -Delta^2 log p_t` is a Hausdorff moment sequence,
`A_t = int_0^1 x^t dmu` with `mu >= 0`, from which the whole hierarchy would follow.

Taken literally that cannot hold, and the reason is one line. With
`R_t = p_t^2/(p_{t-1} p_{t+1})`,

    R_{t+1}/R_t = p_{t+1}^3 p_{t-1} / (p_t^3 p_{t+2}),

so **(B) says exactly that `R` is increasing**, i.e. `A_t = log R_{t+1}` increases.
But a Hausdorff sequence decreases: `Delta A_t = int x^t (x-1) dmu <= 0` because
`x <= 1`.

The brief hedges — "or becomes one after reversing the index from the center" — and
that hedge is **not optional; it is forced**. Only the reversed sequence can carry a
positive-measure representation, so any attempt at this route must begin with the
reversal rather than treat it as a fallback.

## Standing

H1 is now a measured fact on a precisely stated domain, not a rumour, and (B) is
confirmed as one member of a family that holds to at least order 8. That does not
prove anything by itself, but it says the object has more structure than (B) alone
and tells anyone trying the moment route which side of the index to start from.
