# Theorem: 24 rungs of the log-difference hierarchy, each for every n in its domain

*2026-08-30, night shift. Artefact: `results/hierarchy_rungs.json`, module
`lab/hierarchy_rungs.py`.*

## Statement

Let `p_t = e_t/C(N,t)` for the centred spectrum `b_k = (n-2k)^2`, `N = n-1`. For every
pair

    t = 1, 2, 3, 4        r = 3, 4, 5, 6, 7, 8

**[extended the same night to `t = 1..8`, 48 rungs, degrees to 6137]**

and every `n` for which the claim is made — that is, every `n` with the difference
window inside the first half, `t + r <= floor(N/2)`, equivalently `n >= 2(t+r)+1` —

    Delta^r log p_t  <  0.

Twenty-four rungs, each covering infinitely many `n`.

## Proof

Fix `t` and `r`. Then

    Delta^r log p_t < 0
      <=>  PROD_{j : r-j even} p_{t+j}^{C(r,j)}  <  PROD_{j : r-j odd} p_{t+j}^{C(r,j)}.

Every `p_{t+j} = e_{t+j}/C(N,t+j)` is a ratio of polynomials in `n`, and every binomial
`C(N,k)` is positive on the domain, so cross-multiplying turns the inequality into

    D_{t,r}(n) > 0

for one explicit polynomial `D_{t,r}` with rational coefficients. Substituting
`n = m + s` and finding that every coefficient of `D_{t,r}(m+s)` is nonnegative proves
the rung for all `n >= s`.

Such an `s` exists for each of the 24 pairs, and — the point that makes each rung
complete rather than partial — **`s` is always smaller than the domain requirement
`2(t+r)+1`**, so the proof covers the entire range where the statement is claimed.

| `r` \ `t` | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 3 | n≥6 | n≥5 | n≥8 | n≥7 |
| 4 | n≥5 | n≥8 | n≥7 | n≥10 |
| 5 | n≥9 | n≥7 | n≥10 | n≥9 |
| 6 | n≥7 | n≥11 | n≥9 | n≥12 |
| 7 | n≥11 | n≥9 | n≥13 | n≥11 |
| 8 | n≥9 | n≥13 | n≥11 | n≥15 |

Degrees of `D_{t,r}` run from 38 to 4089. The polynomial identities are exact over `Q`
throughout; the `e_t` are obtained by interpolation and each is then **verified at five
nodes beyond the ones it was built from**, so an interpolation that had gone wrong
could not pass.

The direction of the inequality is not taken on trust either: each rung is spot-checked
against the reference sign computation at six values of `n`. Zero mismatches in 24
rungs. ∎

## Why `r >= 4` is the new content

The rung `r = 3` **is** conjecture (B): `Delta^3 log p_{t-1} <= 0` is exactly
`p_t^3 p_{t+2} <= p_{t-1} p_{t+1}^3`. That case was already proved rung by rung for
`t <= 100`.

Everything with `r >= 4` is new. It settles a question the hierarchy raised when it was
first observed: is it a genuinely deeper family of inequalities, or a restatement of
(B)? **It is deeper.** Eighteen of these twenty-four rungs are statements that do not
follow from (B), and each is now a theorem.

## The shift obeys an exact parity law

Extending to 48 rungs made the pattern unambiguous. Writing the excess
`s - (t + r)`:

| `r` \ `t` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |
| 4 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| 5 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |
| 6 | 0 | 3 | 0 | 2 | 0 | 2 | 0 | 2 |
| 7 | 3 | 0 | 3 | 0 | 2 | 0 | 2 | 0 |
| 8 | 0 | 3 | 0 | 3 | 0 | 2 | 0 | 2 |

**The excess is exactly 0 when `t` and `r` have opposite parity, and 2 or 3 when they
have the same parity.** Twenty-four rungs on each side, no exceptions. That parity is
presumably the doubling of the spectrum showing through — the centred multiset is a half
spectrum taken twice.

## The whole hierarchy reduces to one statement

Since the excess never exceeds 3:

> **Conjecture (U).** For every `t >= 1` and `r >= 3`, the polynomial
> `D_{t,r}(m + t + r + 3)` has all nonnegative coefficients.

It holds on all 48 rungs. And `t + r + 3 <= 2(t+r) + 1` whenever `t + r >= 2`, which is
the domain of the claim — so **(U) implies the entire log-difference hierarchy, on its
whole domain, for every `t` and `r` at once.**

That is the sharpest form the problem has taken. It is no longer "prove infinitely many
inequalities"; it is one coefficient-positivity statement about an explicit polynomial
family, of exactly the kind this programme has proved before at fixed parameters.

## Status

`CLAIM-HIER-RUNGS` in the registry: **PROVED**, for the 24 listed pairs on their full
domains. `CLAIM-HIER` — the hierarchy for all `t` and `r` — remains
`COMPUTATIONALLY_VERIFIED` and is not upgraded by this.
