# The first piece of leg (a) that is uniform in the depth

*2026-08-29 night. A proof, by hand, with no computation and no grid.*

## Statement

For every depth `J`, on the whole far-below region,

    c_{J-1} = den^{J-1} * E_{J-1}  >  0.

## Proof

The verified coefficient formula is

    c_k = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i} den^i
                                               e_{J-1-i-k}(A_i .. A_{J-2}).

At `k = J-1` the summation range collapses to `i = 0` alone, where `poch_0 = 1` and
`e_0 = 1`, and the outer sign is `(-1)^{2J-2} = +1`. So a single term survives:

    c_{J-1} = den^{J-1} E_{J-1}.

Both factors are positive on the region, for reasons that do not mention `J`:

* `den = kk (kk - 2)` with `kk = v + K3 + 53` and `v, K3 >= 0`, so `kk >= 53` and
  `den >= 53 * 51 > 0`;
* `E_{J-1} = e_{J-1}({(n-2k)^2})` is an elementary symmetric function of **squares** —
  a sum of products of nonnegative reals — hence nonnegative, and strictly positive
  whenever at least `J-1` of the `b_k` are nonzero, which holds throughout the region
  since `n = v + 44 >= 44`. ∎

## Why it matters

Proposition 1 (`THEOREM_STATE.md`) needs four things: `c_{J-1} > 0` as the leading
coefficient of the grouped quadratic, `c_{J-3} >= 0`, the repair inequality (R), and
nonnegativity of the remaining coefficients. **The first of those is now
unconditional and uniform in `J`** — it no longer needs a per-depth certificate.

## Why the same argument stops at the next coefficient

At `k = J-2` and below the range no longer collapses, and the sum alternates:

    c_{J-2} = -den^{J-2} [ E_{J-1} e_1(A_0..A_{J-2}) - E_{J-2} poch_1 s^2 den ],
    c_{J-3} =  den^{J-3} [ E_{J-1} e_2 - E_{J-2} poch_1 s^2 den e_1 + E_{J-3} poch_2 s^4 den^2 ].

`c_{J-2}` is exactly the first difference, which is why it is the exceptional
negative one. From `c_{J-3}` down, the sign depends on ratios
`E_{J-1-i} / E_{J-2-i}` measured against `poch_i s^2 den` — which is the Newton-excess
theme again, and the same obstruction the rest of the programme is reduced to.

So this is a small result, not a route: it removes one of the four ingredients from
the per-depth workload and confirms that the difficulty sits precisely where the
reduction already says it does.

## A background run this replaces

A job was computing, depth by depth, whether `den^{J-1} E_{J-1}` has nonnegative
monomials. That is a stronger statement than positivity and was not needed; the
one-line argument gives what Proposition 1 actually uses. The run was stopped —
also because the founder is playing and the cores are better left to the game.


## Addendum the same night: c_{J-3} was never a separate hypothesis

Proposition 1 was stated with `c_{J-3} >= 0` among its assumptions. It is not one.
(R) says `4 c_{J-1} c_{J-3} >= c_{J-2}^2`, the right side is a square, and
`c_{J-1} > 0` is now proved for every depth — so `c_{J-3} >= 0` follows.

So the reduction, which began with four ingredients, now needs two: (R), and
nonnegativity of the coefficients away from `J-2` and `J-3`. The two exceptional
indices are exactly the two that were hard.
