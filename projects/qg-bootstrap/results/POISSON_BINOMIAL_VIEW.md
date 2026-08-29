# What f(theta) is: the variance of a tilted Bernoulli sum

*2026-08-29. Artefact: `results/poisson_binomial_view.json`, module
`lab/poisson_binomial_view.py`.*

The limit shape `f` entered this project as a formula with no interpretation:

    theta = 1 - arctan(u)/u,   f = (2/u)/(dtheta/du) - 1/theta - 1/(1-theta).

It is now decoded. `f` is the reciprocal variance of an exponentially tilted
Poisson-binomial distribution, and the two subtracted terms are exactly the
binomial normalisation. The reading came from a prior-art check on conjecture (B)
against Fatehi and Kittaneh (arXiv:1911.12167), whose Theorem 6 observes that the
central factorial array is Poisson-binomially distributed. The consequences below
are ours.

## The identification

    SUM_k e_k(b) s^k  =  PROD_i (1 + b_i s)

is, up to the constant `PROD (1 + b_i s)`, the probability generating function of

    Y(s) = SUM_i Bernoulli(q_i),   q_i = b_i s / (1 + b_i s).

So `e_k(b)` normalised is a pmf, and `s` is an exponential tilt that moves its
mean anywhere in `(0, N)`.

## Three consequences, and what holds each

**1. The raw Newton excess is tilt-invariant.** The `s^t` factors cancel in
`rho_t = e_t^2/(e_{t-1} e_{t+1})`, so it is the log-concavity excess of the pmf at
every tilt at once.

**2. `M` splits exactly.** With `beta_t = t(N-t)/((t+1)(N-t+1))`,

    M_{n,t} = n (rho_t * beta_t - 1),

and `n(beta_t - 1) -> -1/theta - 1/(1-theta)`, which is precisely the pair of terms
sitting inside `f`. **Exact, at finite `n`**: verified at every even `n = 8..40`
and every `2 <= t <= N-3`, 0 mismatches.

**3. The remaining piece is the tilted variance.** With
`sigma^2(s) = SUM_i b_i s/(1 + b_i s)^2` and `s_t` the tilt of mean `t`,

    n / sigma^2(s_t)  ->  f(theta) + 1/theta + 1/(1-theta).

Measured, not proved. The relative gap times `n` is FLAT in `n`:

| theta | gap x n at n=100 | at 200 | at 400 |
|---|---|---|---|
| 0.10 | 0.1893 | 0.1891 | 0.1890 |
| 0.20 | 0.4039 | 0.4025 | 0.4017 |
| 0.30 | 0.6559 | 0.6522 | 0.6504 |
| 0.40 | 0.9659 | 0.9586 | 0.9550 |
| 0.49 | 1.3252 | 1.3127 | 1.3065 |

so the gap is exactly of order `1/n` and the limit is equality.

The check by hand, which is what convinced me before the numbers did: with
`b_i = i^2` and `s = 1/a^2`, the tilted mean is `SUM i^2/(a^2+i^2) ~ n - a
arctan(n/a)`, so `theta = 1 - arctan(u)/u` with `u = n/a` — the SAME `u` the limit
shape was already written in. That substitution was never a change of variable; it
was the tilt all along.

## What this buys

The one remaining gap in the bridge was an effective expansion
`M = f + g/n + O(1/n^2)` with explicit remainder, stated about a ratio of
elementary symmetric functions — an object with no effective literature. It is now
the same statement about a **local limit theorem for a sum of independent Bernoulli
variables with explicitly known tilted cumulants**, a classical subject that does
have effective versions (Edgeworth expansions for lattice sums; Stein-method bounds
with explicit constants).

The target sharpens too. The numbers say

    rho_t - 1 = 1/sigma^2(s_t) * (1 + c/n + ...)   with c > 0,

and `g > 0` is exactly that positive correction — the Edgeworth term.

## A guess of mine that died here

I expected the clean inequality `rho_t - 1 <= 1/sigma^2(s_t)`. It fails in **12 of
12** tested cases, always the same way: the true excess EXCEEDS the Gaussian value,
by a factor 1.031 at `n = 60` falling to 1.009 at `n = 200`. Recorded because the
direction is the useful part — it is the sign of `g`, seen from a second side.

## Status

Parts 1 and 2 are exact identities. Part 3 is a numeric probe at 40 digits with a
measured convergence rate: a measurement, not a certificate, and labelled so in the
artefact.
