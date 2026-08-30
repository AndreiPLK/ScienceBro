# Leg (a)'s certificate splits into one-dimensional statements, one per monomial

*2026-08-30 evening. The best structural position Step 1 has reached.*

## The split

Every `tau_i` in the coefficient formula has **entirely nonnegative monomials** — verified
at every `(k, i)` pair at `J = 10`, zero exceptions, and each factor separately
(`den`, `s^2`, `A_0`, `E`, `poch`, and their product `W_i`) is monomially nonnegative too.

So all negativity in `c_k` comes from the alternating signs, and nothing else. Reading the
alternating sum monomial by monomial and applying the same binomial identity,

    [mu] c_k  =  den^k * Delta^{L-1} ( [mu] tau_i / C(L-1, i) ) (0),

with the sign factors cancelling exactly as before. **The four-variable positivity question
becomes a family of one-dimensional questions, one per monomial.**

## It is not merely sufficient — the counts match exactly

Absolute monotonicity of those per-monomial sequences, taken in `Q(sqrt3)` with `sign_q3`
deciding every sign:

| `J` | `k` | sequences | absolutely monotone | fail | certificate's negative monomials |
|---|---|---|---|---|---|
| 8 | 0 | 8555 | 8555 | 0 | 0 |
| 8 | `J-4` | 1659 | 1659 | 0 | 0 |
| 8 | `J-2` | 271 | 271 | 0 | 0 |
| 10 | 0 | 17575 | 17575 | 0 | 0 |
| 10 | `J-3` | 1020 | 1020 | 0 | 0 |
| 10 | **`J-2`** | 343 | 323 | **20** | **20** |
| 12 | 0 | 31395 | 31395 | 0 | 0 |
| 12 | `J-4` | 2499 | 2499 | 0 | 0 |
| 12 | **`J-2`** | 415 | 386 | **29** | **29** |

The failures land exactly where the certificate fails, and in exactly the same number. The
split is faithful, not merely a sufficient condition.

## Why this is the right shape for uniformity

Everything Step 1 needs is now a statement about explicit one-dimensional sequences of
rationals-with-a-`sqrt3`-part, indexed by `i`, with combinatorial formulas — coefficients of
products of `E`, a Pochhammer, powers of `s^2` and `den`, and an elementary symmetric
function of an arithmetic progression. That is a far smaller object than a four-variable
polynomial positivity problem, and it does not grow with the number of region variables.

A proof that those sequences are absolutely monotone for `k` outside `{J-2}` would give
leg (a) **at every depth at once** — which is exactly Step 1.

## Two errors of mine on the way, both caught by a check designed to catch them

The first version of this test looked only at monomials present at **every** `i`, and the
second looked only at the **rational part**, ignoring the `sqrt3` component. Both passed
`k = J-2` cleanly — where the certificate is known to fail — and that impossibility is what
exposed them. The consistency check was built precisely because a result at `k = J-2` that
looks fine is a result that must be wrong.
