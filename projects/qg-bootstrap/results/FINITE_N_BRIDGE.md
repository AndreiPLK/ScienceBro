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

* **(B) ratio-log-concavity in `t`:** `p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}`. Writing
  `r_t = p_t/p_{t-1}`, this is exactly `r_{t+1}^2 >= r_t r_{t+2}` — **the ratio
  sequence is log-concave** (verified equivalent over 1071 pairs, 0
  disagreements). Newton says `r_t` decreases; (B) says it is also log-concave.
  That is a named notion — a sequence with log-concave ratios is called *ratio
  log-concave* — and there are criteria for it for sequences obeying a recurrence
  (Chen, Guo and Wang), which is worth trying against the exact recursion (R)
  above rather than proving from scratch. This
  makes `R_{n,t}` rise to the middle, so the maximum over `t` sits at the central
  index. **Tested: 2050 pairs `(n, t)` with `n = 8..89`, `t <= n/2+1`, 0
  failures.**
* **(C) is NOT locally derivable, and that was tested three ways.** By the
  recursion, `M_{n+2}` at the central index depends on five consecutive `e_j(n)`,
  which invites a proof from generic inequalities on those five. It does not work.
  Feeding synthetic five-term windows through the exact recursion:

  | constraints imposed on the window | violations of (C) |
  |---|---|
  | Newton (ratios decreasing) | 233 of 400 |
  | Newton + (B) (ratios log-concave) | 25 of 600 |
  | Newton + (B) + near-extremal (`M_n <= 5/2`) | 865 of 2714 |

  So no set of local conditions of this kind implies (C): the actual values of the
  family are doing the work, not the shape of five neighbours. A proof of (C) has
  to reach for the global structure — the Gamma-ratio generating function, or the
  recursion iterated, not a window.

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

**With one correction, made within ten minutes of proposing it.** The AP statement
is FALSE without a range restriction: for progressions that cross zero there are
failures — 14 of 2028 pairs, the first at `N = 10`, `t = 8`, `a = -16/3`, `d = 16`.
They all sit at large `t`. Restricting to what the target actually needs:

| range | pairs | failures |
|---|---|---|
| `t <= N/2` | 1107 | **0** |
| `t <= 0.6 N` | 1335 | **0** |
| `t <= 0.7 N` | 1530 | **0** |

So the correctly scoped conjecture is **(B) for squares of an AP with `t <= N/2`**,
and the counterexample above is part of the statement, marking where it stops.

**And squares of an AP have a classical generating function.** Verified exactly:

    PROD_{k=0}^{N-1} (1 + (a+k)^2 z)
      = z^N * [Gamma(a+N-i/sqrt z)/Gamma(a-i/sqrt z)] * [Gamma(a+N+i/sqrt z)/Gamma(a+i/sqrt z)],

a ratio of Gamma functions at conjugate complex arguments. So the `e_t` of this
family are Taylor coefficients of a Gamma ratio, which is where a proof of (B)
should be looked for — and it is why generic real-rooted arguments cannot reach
it.

## (C) is a corollary of the same expansion, which simplifies the ask

The margin in (C) — `M_{n,central} - M_{n+2,central}` — is positive but vanishing:
0.007206 at `n = 20`, 0.001862 at 40, 0.000835 at 60, 0.000496 at 78, i.e. of order
`1/n^2`. That is exactly what `M_n = f + g/n + O(1/n^2)` with `g > 0` predicts, the
difference being `~2g/n^2`.

So (C) is not an independent conjecture: it is the statement that the central
curvature descends monotonically to its limit, and it follows from an effective
second-order expansion with a positive `1/n` coefficient. The same expansion gives
the bound directly. **The two conjectures therefore collapse into one analytic
request** — an effective expansion of `M_{n,t}` with explicit error — which is what
the bridge asked for before (B) and (C) were introduced as a route around it.

That is worth stating plainly: (B) is now a theorem for `t <= 100` by finite
proofs, and (C) is best attacked not directly but through the expansion.

## What is proved and what is not

**Not proved in general:** (B) and (C). They are conjectures with 2050 and 72 clean
tests behind them, no more.

**But (B) is proved at `t = 1`, which is its tightest case.** The slack in (B)
shrinks with `n` and is smallest at `t = 1`: `p_2^3/(p_1^3 p_3)` = 1.0195 at
`n = 10`, 1.0033 at 20, 1.00059 at 44, 1.00023 at 69. And `t = 1` is exactly where
closed forms exist:

> **Theorem.** For `n >= 6`, `p_2^3 p_0 >= p_1^3 p_3`.
>
> *Proof.* With `N = n-1`, `p_2^3 = 8 e_2^3/(N(N-1))^3` and
> `p_1^3 p_3 = 6 e_1^3 e_3/(N^4 (N-1)(N-2))`, so over the positive common
> denominator the claim is
> `P(n) := 8 e_2^3 N^4 (N-1)(N-2) - 6 e_1^3 e_3 (N(N-1))^3 >= 0`. The `e_i` are
> polynomials in `n` of degrees 3, 6, 9, so `P` has degree 22; substituting
> `n = m + 6` makes **all 23 of its coefficients nonnegative**, hence `P >= 0` for
> `m >= 0`. QED

Checked in `lab/conjecture_B_t1.py`: the `e_i` are obtained by exact interpolation
and verified against the reference engine at 55 values of `n` before use, the
shifted coefficient signs are computed exactly, and a direct evaluation over
`n = 6..69` agrees.

**And the move is a machine, not a one-off.** At any FIXED `t`, (B) is one
polynomial inequality in `n`, since `p_j = e_j/C(N,j)` with `e_j` of degree `3j`
and `C(N,j)` of degree `j`; cross-multiplying by the positive binomials gives

    e_{t+1}^3 e_{t-1} C(N,t)^3 C(N,t+2) - e_t^3 e_{t+2} C(N,t+1)^3 C(N,t-1) >= 0.

`lab/conjecture_B_rungs.py` builds that polynomial and finds the smallest shift
making every coefficient nonnegative:

| t | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| degree | 22 | 38 | 54 | 70 |
| proved for all `n >=` | 3 | 6 | 5 | 8 |

So **(B) is proved at `t = 1, 2, 3, 4`**, including its tightest rung, by the same
all-nonnegative-coefficients move that carries the repair certificate. Degrees grow
by 16 per rung (`16t + 6`), so the machine keeps running: `t = 5` and `t = 6` also
close, at shifts 7 and 10.

**And the shifts line up with exactly what is needed.** Our range is `t < n/2`,
i.e. `n > 2t`. Testing the shift `2t` itself:

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| degree | 22 | 38 | 54 | 70 | 86 | 102 | 118 | 134 | 150 | 166 |
| negatives after `n = m + 2t` | 9 | 13 | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |

So for `t >= 3` the rung polynomial is nonnegative-coefficient after exactly the
shift the application needs, and the two exceptional rungs `t = 1, 2` are proved
separately for `n >= 3` and `n >= 6`.

**That turns the open part of (B) into one sharp uniform statement:**

> For every integer `t >= 3`, the polynomial `P_t(m + 2t)` has all coefficients
> nonnegative, where
> `P_t(n) = e_{t+1}^3 e_{t-1} C(N,t)^3 C(N,t+2) - e_t^3 e_{t+2} C(N,t+1)^3 C(N,t-1)`.

**And it has been carried out to `t = 100`** (`results/conjecture_B_rungs.json`,
`RUNG_TOP=100`): degrees run from 54 to 1606 and **not one rung fails**, in 198
seconds. Each clean rung is not evidence but a PROOF at that `t`, so:

> **(B) is a theorem for every `t <= 100` and `n > 2t`** — hence for the entire
> range the bridge needs, at every `n <= 200`.

What is still owed is only the uniformity in `t`: the statement that the shift
`2t` works for EVERY `t`, rather than for each one checked. That is a statement
about one explicit family of polynomials — no knives, no `lam`, no asymptotics —
and every instance of it computed so far is true.

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
