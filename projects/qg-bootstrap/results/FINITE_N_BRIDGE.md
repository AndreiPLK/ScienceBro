# The finite-n bridge: reduced to two conjectures and two numbers

2026-08-29. Machine checks: `lab/finite_n_bridge_check.py` ->
`results/finite_n_bridge_check.json`.

## The gap this closes

`LIMIT_SHAPE_BOUND.md` proves the asymptotic half of the named lemma:
`f(theta) < 2` on `(0, 1/2)`. What the certificate uses is the FINITE statement

    R_{n,t} := p_t^2/(p_{t-1}p_{t+1})  <=  1 + 2/n,   n >= 44,  t < n/2,
    p_t = e_t/C(N,t),  N = n-1,  e_t of {(n-2k)^2 : k = 1..n-1}.

Write `M_{n,t} = n(R_{n,t} - 1)`; the statement is `M_{n,t} <= 2`.

## The exact recursion, and where it comes from

A third answer from the parallel chat (`Finite_n_Bridge.pdf`, 29 Aug; untrusted,
so checked here) supplies the structure that makes a finite proof plausible. With
`F_n(z) = SUM_t e_t(n) z^t = PROD_{k=1}^{n-1} (1 + (n-2k)^2 z)`,

    F_{n+2}(z) = F_n(z) (1 + n^2 z)^2,
    e_t(n+2) = e_t(n) + 2 n^2 e_{t-1}(n) + n^4 e_{t-2}(n).

**Verified: 1760 checks over `n = 5..59`, 0 mismatches.** It is the doubling this
repository found earlier (`DOUBLED_MULTISET.md`) read as a step in `n`: going from
`n` to `n+2` adds the pair `+-n`, i.e. the value `n^2` twice. The step from
asymptotics to finite `n` is therefore an exact algebraic recursion, not an
approximation.

## The reduction, and its two conjectures

* **(B) ratio-log-concavity in `t`:** `p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}`. This
  makes `R_{n,t}` rise to the middle, so the maximum over `t` sits at the central
  index. **Tested: 2050 pairs `(n, t)` with `n = 8..89`, `t <= n/2+1`, 0
  failures.**
* **(C) parity monotonicity in `n`:** `M_{n+2, floor((n+1)/2)} <= M_{n,
  floor((n-1)/2)}`. This makes the central value fall as `n` grows, so the maximum
  over `n >= 44` sits at the two smallest cases, one per parity. **Tested: 72
  values of `n`, 0 failures.**

With both, the lemma reduces to **two numbers**, and both are computed exactly:

    M_{44,21} = 1.8393321287,     M_{45,22} = 1.8860353047,

against the 2 allowed. (The PDF quotes both to ten digits; they reproduce here
exactly, and `M_{44,21}` is the same maximum this repository had already measured
independently over `n >= 44`.) The central values fall as predicted: 1.882 at
`n = 20`, 1.843 at 40, 1.839 at 44, 1.830 at 60, 1.823 at 80, toward the proved
limit `f(1/2) = 1.804`.

## Narrowing (B) to the right class, and a classical handle

The fourth answer from the parallel chat restates (B) and (C) as a proof target
without proving them. So the target was narrowed here instead, by killing
generalisations:

| class | (B) |
|---|---|
| generic positive sets | **fails**, 1457 of 2940 random pairs |
| squares of an arbitrary real-rooted polynomial | **fails**, 1160 of 2300 |
| squares of an ARITHMETIC PROGRESSION `b_k = (a+kd)^2` | **0 failures of 1650** |

So the structure (B) needs is neither positivity, nor squareness, nor the doubling:
it is the arithmetic progression. Our family is `a = n-2`, `d = -2` — an AP that
crosses zero, which is where the doubling comes from — but the tested APs with
`a >= 0`, `d > 0` never cross zero and (B) still holds.

**And squares of an AP have a classical generating function.** Verified exactly:

    PROD_{k=0}^{N-1} (1 + (a+k)^2 z)
      = z^N * [Gamma(a+N-i/sqrt z)/Gamma(a-i/sqrt z)] * [Gamma(a+N+i/sqrt z)/Gamma(a+i/sqrt z)],

a ratio of Gamma functions at conjugate complex arguments. So the `e_t` of this
family are Taylor coefficients of a Gamma ratio, which is where a proof of (B)
should be looked for — and it is why generic real-rooted arguments cannot reach
it.

## What is proved and what is not

**Not proved:** (B) and (C). They are conjectures with 2050 and 72 clean tests
behind them, no more.

**Proved:** the exact recursion; the `t = 1` rung in closed form, which the same
PDF gives as `R_{n,1} = 5n(n-2)^2/(5n^3 - 24n^2 + 28n + 12)` — **verified over 75
values of `n`, 0 mismatches** — with `1 + 2/n - R_{n,1} = 2(3n^3 - 20n^2 + 34n +
12)/[n(5n^3 - 24n^2 + 28n + 12)] > 0` on the range; and the asymptotic half
`f < 2`.

**The fallback the same answer names**, if (B) or (C) resists: an explicit local
Edgeworth estimate targeting `M_{n,t} <= f(t/n) + 6/n`. Consistent with what this
repository measured independently — the gap constant is about 5.5 and cannot be
much below 5.65, since `45(M_{45,22} - f(22/45)) = 5.645`.

So the bridge is no longer an open analytic problem: it is two inequalities about
an explicitly recursive family, with every numerical precondition checked and the
two base cases already in hand.
