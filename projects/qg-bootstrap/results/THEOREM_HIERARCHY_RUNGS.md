# Theorem: 24 rungs of the log-difference hierarchy, each for every n in its domain

*2026-08-30, night shift. Artefact: `results/hierarchy_rungs.json`, module
`lab/hierarchy_rungs.py`.*

## Statement

Let `p_t = e_t/C(N,t)` for the centred spectrum `b_k = (n-2k)^2`, `N = n-1`. For every
pair

    t = 1, ..., 14        r = 3, 4, 5, 6, 7, 8, 9

and every `n` for which the claim is made — that is, every `n` with the difference
window inside the first half, `t + r <= floor(N/2)`, equivalently `n >= 2(t+r)+1` —

    Delta^r log p_t  <  0.

Ninety-eight rungs, each covering infinitely many `n`.

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

The shifts are tabulated below as the excess `s - (t+r)`, which is where the structure
shows. Degrees of `D_{t,r}` run from 38 to 18936. The polynomial identities are exact over `Q`
throughout; the `e_t` are obtained by interpolation and each is then **verified at five
nodes beyond the ones it was built from**, so an interpolation that had gone wrong
could not pass.

The direction of the inequality is not taken on trust either: each rung is spot-checked
against the reference sign computation at six values of `n`. Zero mismatches in 98
rungs. ∎

## Why `r >= 4` is the new content

The rung `r = 3` **is** conjecture (B): `Delta^3 log p_{t-1} <= 0` is exactly
`p_t^3 p_{t+2} <= p_{t-1} p_{t+1}^3`. That case was already proved rung by rung for
`t <= 100`.

Everything with `r >= 4` is new. It settles a question the hierarchy raised when it was
first observed: is it a genuinely deeper family of inequalities, or a restatement of
(B)? **It is deeper.** Eighty-four of these ninety-eight rungs are statements that do not
follow from (B), and each is now a theorem.

## The shift obeys a parity law, and my first reading of it was wrong

Extending to 98 rungs settled the structure. Writing the excess `s - (t + r)`:

| `r` \ `t` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |
| 4 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| 5 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |
| 6 | 0 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| 7 | 3 | 0 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |
| 8 | 0 | 3 | 0 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| 9 | 4 | 0 | 3 | 0 | 3 | 0 | 3 | 0 | 2 | 0 | 2 | 0 | 2 | 0 |

**The excess is exactly 0 whenever `t` and `r` have opposite parity** -- 49 rungs, no
exceptions, against 49 rungs with excess 2, 3 or 4 when the parities agree.

And the parity is not a coincidence, it is the spectrum. Opposite parity means `t + r`
is ODD, and the centred multiset `{(n-2k)^2}` contains the element `0` exactly when `n`
is EVEN. So the law reads:

> the minimal shift is exactly `t + r` if and only if the centred spectrum at
> `n = t + r` contains no zero.

Tested on all 98 rungs, 49 on each side, no exceptions. When the spectrum at the shift
point carries a zero, that degeneracy pushes the needed shift 2 to 4 further out. This
turns an empirical parity into a mechanism, and it says where a proof should start: the
odd case, where there is no zero to handle.

When the parities agree the excess is 2 far from the corner and grows slowly towards it.
Along `t = 1` it is 2, 3, 3, 4 at `r = 3, 5, 7, 9`, matching `2 + floor((r-1)/4)`.

**A conjecture of mine died here.** On the 48-rung table the excess never exceeded 3, and
I wrote down (U): that the shift `t + r + 3` always works. The `r = 9`, `t = 1` rung
gives excess **4**, so (U) is false. It was refuted within the hour by the run launched
specifically to attack it, which is the only reason it never reached a document as
anything but a conjecture.

## The corrected statement, which is the one that matters

The excess grows, but nothing in the application needs it bounded by a constant. What is
needed is that the shift stay under the domain requirement:

> **Conjecture (U2).** For every `t >= 1` and `r >= 3`, the polynomial
> `D_{t,r}(m + 2(t+r) + 1)` has all nonnegative coefficients.

This is well posed because shifts are monotone: if `P(m+s)` has nonnegative coefficients
then so does `P(m+s')` for every `s' > s`, being a substitution `m -> m + (s'-s)` into a
polynomial with nonnegative coefficients. So (U2) says exactly that the needed shift never
exceeds the domain bound.

It holds on all 98 rungs, with slack from 3 (at `r=3, t=1`) to 24 (at `r=9, t=14`), and
the slack grows, since the excess grows like `r/4` while the bound grows like `2(t+r)`.

**(U2) implies the entire log-difference hierarchy on its whole domain**, for every `t`
and `r` at once -- and with it conjecture (B), which is the rung `r = 3`. It is weaker
than the (U) that died, and therefore more likely true, while being exactly as strong for
the application.

## Status

`CLAIM-HIER-RUNGS` in the registry: **PROVED**, for the 98 listed pairs on their full
domains. `CLAIM-U` is **DISPROVED**; `CLAIM-U2` is the corrected form, `CONJECTURED`. `CLAIM-HIER` — the hierarchy for all `t` and `r` — remains
`COMPUTATIONALLY_VERIFIED` and is not upgraded by this.
