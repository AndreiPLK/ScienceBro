# Theorem: 24 rungs of the log-difference hierarchy, each for every n in its domain

*2026-08-30, night shift. Artefact: `results/hierarchy_rungs.json`, module
`lab/hierarchy_rungs.py`.*

## Statement

Let `p_t = e_t/C(N,t)` for the centred spectrum `b_k = (n-2k)^2`, `N = n-1`. For every
pair

    t = 1, 2, 3, 4        r = 3, 4, 5, 6, 7, 8

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

## What is still open, and it is now sharp

Uniformity in `(t, r)`. Each rung is proved separately, and the degrees grow like
`3(t+r)2^r`, so no amount of computation reaches all of them. What is wanted is one
argument: that `D_{t,r}(m + s)` has nonnegative coefficients for every `t` and `r`, with
`s` below the domain bound.

The shifts themselves show structure worth looking at — they depend on the parities of
`t` and `r`, not only on their sizes (`r=5,t=1` needs 9 while `r=6,t=1` needs 7). A
uniform argument will probably have to explain that parity, and explaining it may be the
way in.

## Status

`CLAIM-HIER-RUNGS` in the registry: **PROVED**, for the 24 listed pairs on their full
domains. `CLAIM-HIER` — the hierarchy for all `t` and `r` — remains
`COMPUTATIONALLY_VERIFIED` and is not upgraded by this.
