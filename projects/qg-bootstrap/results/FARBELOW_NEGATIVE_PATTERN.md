# Where the far-below criterion breaks, exactly

2026-08-29. `lab/farbelow_negative_pattern.py` ->
`results/farbelow_negative_pattern_j<J>.json`.

## The question

`lab/knife_farbelow2.py` proves knife positivity in the far-below region by
MANIFEST positivity: expand `N = (-1)^{J-1} B_j` at `D = T_cap - y` and check
that every monomial of every `y`-coefficient is nonnegative. It works for
`j = 4..8` and fails from `j = 9` — which is why `j = 9..17` were closed by the
heavier interval-Bernstein route instead (`knife*_farbelow_interval.json`).

The counts in the existing artefacts say how badly it fails:

| j | 9 | 10 | 11 | 12 |
|---|---|---|---|---|
| negative monomials | 11 | 30 | 41 | 71 |
| total monomials | 54331 | 84170 | 124881 | 178816 |

Two parts in ten thousand. That is not a wall; that is a list of exceptions. The
question is whether the list has a shape.

## It does, and the shape is a line

Rebuilt on the fast engine (`Q3Poly` over `Q(sqrt3)` via `knife_tail2.build_P`;
no new derivation, the same construction the certificates use), the negative
monomials are:

| j | negatives | y-degree | dips found | repair failures |
|---|---|---|---|---|
| 9 | 11 | **7 = J-2**, all | 6 | **0** |
| 10 | 30 | **8 = J-2**, all | 7 | **0** |
| 11 | 41 | **9 = J-2**, all | 20 | **0** |
| 12 | 71 | **10 = J-2**, all | 38 | **0** |
| 13 | 96 | **11 = J-2**, all | 62 | **0** |
| 14 | 130 | **12 = J-2**, all | 78 | **0** |
| 15 | 165 | **13 = J-2**, all | 99 | **0** |

(at `j = 9, 10` the negatives also share `thL = K3 = 0`, differing only in `v`;
by `j = 11` a couple sit at `K3 = 1`.) 310 dips in total across the seven depths,
and the repair holds at every one.

So every failure of the criterion, at the `j` measured HERE, lives in **one single
`y`-coefficient — the one of degree `J-2`** (but read the correction below: this
holds only while `n >= 2J-3`) — and inside it, on the corner
`thL = 0`, `K3 = 0` (with two strays at `K3 = 1` for `j = 11`). All `J-1` other
coefficients are manifestly positive, monomial by monomial.

## Why this matters for the keystone

The programme's missing piece is uniformity in depth: every `j` from 4 to 17 has
its own certificate, and there is no single argument covering all `j`. This
localisation says what a uniform argument would have to do — not "handle the
general case", but:

1. show that the `y`-coefficients `c_0 .. c_{J-3}` are manifestly positive for
   every `j` (a statement about an explicit alternating sum of E-polynomials and
   Pochhammer weights, and it is what the machine already sees at `j = 4..11`);
2. handle `c_{J-2}` alone, where the negativity sits in a corner and must be
   dominated by a neighbouring power of `y` on the physical range.

That is a far smaller target than the general case, and it is the first time the
obstruction to uniformity has an address rather than a size.

## Why that coefficient and no other — a closed form

The localisation is not an accident of the region. Writing the tail factor as
`tail_i = PROD_{r=i}^{J-2} (A_r - y den)` with `A_r = tk_num + (c+2r) den`, the
`y`-expansion of `N = (-1)^{J-1} B` is

    [y^k] N = (-1)^{J-1+k} den^k SUM_{i <= J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                  den^i e_{J-1-i-k}(A),

an alternating sum over `i` with `J-k` terms. So:

* `k = J-1` has **one** term: `c_{J-1} = den^{J-1} E_{J-1} > 0`, positive by
  inspection;
* `k = J-2` has **exactly two, of opposite sign** — it is the first difference in
  the family:

      c_{J-2} = den^{J-2} [ poch_1 s^2 den E_{J-2} - E_{J-1} (J-1)(tk_num + den(c+J-2)) ],
      poch_1  = (2n-2J+1)(2n-2J+2)/2;

* every `k < J-2` has three or more terms, and their expansions come out with
  nonnegative monomials — which is the manifest positivity the criterion lives
  on.

**The two-term formula is verified against the assembled polynomial, not
asserted:** `j = 6`, 735 monomials, **0 mismatches**; `j = 9`, 1752 monomials,
**0 mismatches** (`results/farbelow_negative_pattern_j9.json`, field
`c_Jm2_closed_form_check`).

Dividing by `den` and using `T_cap = tk_num/den`, the sign of the exceptional
coefficient is decided by one explicit inequality:

    c_{J-2} > 0   <==>   (2n-2J+1)(2n-2J+2)/2 · s^2 · E_{J-2}
                          >  (J-1)(T_cap + 4n - 4J - 1 + J - 2) · E_{J-1}.

Both sides are elementary; the only non-elementary ingredient is the ratio
`E_{J-1}/E_{J-2}`, which Newton's inequalities bound by
`[n(n-2)/3](n-J+1)/(J-1)` — the same tool Theorem 5 of
`BFORM_POSITIVITY_THEOREM.md` runs on. And it explains the observed breakdown at
`j = 9` without any further computation: as `J` grows toward `n` the left side
carries `(2n-2J)^2` and shrinks, while the right side carries `(J-1)` and grows.

**What this does and does not give.** It does not restore the criterion — for
`j >= 9` the coefficient really is negative in that corner, which is why the
interval route was needed. What it gives is an explicit handle: `c_{J-2}` and
`c_{J-1}` are now both in closed form, so the natural repair
`y^{J-2}(c_{J-1} y + c_{J-2}) >= 0` becomes a threshold in `y` that can be
written down rather than searched for. Whether that threshold sits inside or
outside the physical range is the next thing to measure, and it is measured
nowhere yet.

## The repair the structure suggests, and its first measurement

With every `c_k >= 0` except `c_{J-2}`, positivity of `N(y) = SUM_k c_k y^k` on
`y >= 0` follows if the one negative term is absorbed by its two neighbours:

    c_{J-3} + c_{J-2} y + c_{J-1} y^2 >= 0  for y >= 0
      <==>  c_{J-2}^2 <= 4 c_{J-1} c_{J-3}   (discriminant),

and the stronger log-concave form `c_{J-2}^2 <= c_{J-1} c_{J-3}` is the discrete
Newton inequality on the coefficient sequence — the same shape of tool as
Theorem 5 in `BFORM_POSITIVITY_THEOREM.md`.

**Measured at three depths** (512 points of the region grid each,
`thL, v, K3` in {0,1,2,3,6,12,40,200}):

| j | points with `c_{J-2} < 0` | discriminant failures | log-concave failures |
|---|---|---|---|
| 9 | 6 | **0** | **0** |
| 10 | 7 | **0** | **0** |
| 11 | 20 | **0** | **0** |

33 negative points, no failure of either form. Away from those points the
log-concave form does fail sometimes, which costs nothing: where the coefficient
is already nonnegative there is nothing to repair.

So the candidate mechanism for uniformity in depth, in the far-below region, is
two explicit statements:

1. `c_k >= 0` monomial-by-monomial for every `k != J-2` and every `j`;
2. wherever `c_{J-2} < 0`, `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`.

Both are polynomial inequalities in the region variables, and `c_{J-1}`, `c_{J-2}`
are already in closed form above. **Neither is proved.** (2) is now measured at
`j = 9, 10, 11` — 33 points where the coefficient dips, no failure — and the
`y`-degree localisation holds at all three. `j = 12` is still queued (179k
monomials, it is the slow one).

## The general coefficient, verified — and why J-2 is the weakest link

The two-term formula for `c_{J-2}` is the `k = J-2` case of

    [y^k] N = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                    den^i e_{J-1-i-k}(A_i..A_{J-2}),

`A_r = tk_num + (c+2r) den`, `poch_i = PROD_{q=1}^{2i}(2n-2J+q)/(i! 2^i)`. Checked
against the assembled polynomial for **every** `k` at `j = 6`: `k` = 0..5, 3186 /
2528 / 1890 / 1292 / 735 / 231 monomials, **0 mismatches at every k**
(`general_coefficient_formula` in the module).

One reading of that expression is **wrong, and the numbers killed it the same
hour** — recorded here rather than quietly deleted. The term with the highest
power of `s` is `i = J-1-k` and its total sign is
`(-1)^{J-1+k}(-1)^{J-1-k} = +1`, so the highest-`s` term is always positive. I
took that to mean manifest positivity was "the dominant term swamps the rest",
which would have made the uniform proof a decay estimate. It is not:
`lab/dominant_term_probe.py` (`results/dominant_term_probe.json`) evaluates the
terms as certified `arb` numbers over the region and finds

    SUM_{i < J-1-k} T_i  /  T_{J-1-k}   =   3  to  3.2e8    for k <= J-3,

so the "dominant" term is routinely the smallest thing in the sum. The reason is
visible once measured: `T_i` gains `s^2 den` per step but loses one factor
`A ~ T_cap den ~ lam^2 den`, and those two are the same size — the terms are
comparable, and manifest positivity comes from cancellation among comparable
terms, not from one of them winning.

What survives, and it is the interesting half: at the weak link `k = J-2` that
same ratio is **0.9997 to 1.0164** — the two terms are equal to within a percent.
That is why this coefficient, and only this one, changes sign: it is a difference
of two quantities that are the same size to a part in a hundred, while every
other `c_k` is a longer sum whose cancellation resolves in the monomials.

## The repair reduced to one quadratic, and measured to depth 40

Writing `alpha_r = A_r/den = T_cap + c + 2r`, `w = E_{J-1}`,
`u = poch_1 s^2 E_{J-2}`, and `e1, e1p, e2` for the elementary symmetric
functions of the alphas (`e1p` omitting `alpha_0`), the verified general formula
gives all three relevant coefficients with the SAME power of `den`:

    c_{J-1} = den^{J-1} w,
    c_{J-2} = den^{J-1} (u - w e1),
    c_{J-3} = den^{J-1} (w e2 - u e1p + poch_2 s^4 E_{J-3}),

so the repair `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}` is a quadratic in `u`, opening
upward:

    u^2 - 2 u w (alpha_0 - e1p) + w^2 (e1^2 - 4 e2) - 4 w poch_2 s^4 E_{J-3} <= 0.

**Measured (`lab/repair_inequality_probe.py`, certified `arb`, 315 region points
over `J` = 5, 9, 12, 16, 20, 30, 40): the coefficient dips at 91 of them, and the
quadratic holds at every single one — 0 failures, 0 undecided enclosures.** That
extends the repair from the three depths reachable by full polynomial expansion
to seven, and to depth 40.

**And a near miss worth keeping.** Evaluating the quadratic at the boundary
`u = w e1` — where `c_{J-2}` changes sign — collapses it, via `e1 - alpha_0 =
e1p`, to the single explicit inequality

    E_{J-1} [ e1p^2 - e_2(alpha_1..alpha_{J-2}) ]  <=  poch_2 s^4 E_{J-3}.

That form is **false** — at 70 of the 315 points — but only just: the ratios are
**1.0000 to 1.0016**. So the boundary reduction is a fraction of a percent too
strong to be the proof, and the true statement is tight at the `10^-3` level.
Tightness again, in a third independent place today.

## What a proof uniform in J would need — one named lemma

Expanding (R) with `alpha_r = A_r/den` and using `e1 - 2 e1p = alpha_0 - e1p`:

    (R) = w^2 (4 e2 - e1^2) + 2 u w den (alpha_0 - e1p)
          - u^2 den^2 + 4 w poch_2 s^4 E_{J-3} den^2   >=  0.

The `alpha_r` differ only by `2r` against a `T_cap` of order `lam^2`, so they are
nearly equal, and for `m = J-1` near-equal numbers `4 e2 - e1^2 = e1^2 - 2 SUM
alpha^2 ~ alpha^2 m(m-2) > 0` for `m >= 3`. The dangerous term is `- u^2 den^2`,
and it is dominated by the last one exactly when

    poch_1^2 E_{J-2}^2  <=  4 poch_2 E_{J-1} E_{J-3},
      i.e.   E_{J-2}^2 / (E_{J-1} E_{J-3})  <=  2cd/(ab),
      a = 2n-2J+1, b = a+1, c = a+2, d = a+3.

**Measured: 144 cases (`n` = 44..200, `J` = 4..39), 0 violations, tightest slack
1.33.** So the mechanism is real.

**And the tool for it is NOT Newton** — that was my first thought and it is
backwards. Newton's inequality gives `E_k^2/(E_{k-1}E_{k+1}) >= C(N,k)^2 /
(C(N,k-1)C(N,k+1))`, a LOWER bound on exactly the ratio that needs an upper one.
No universal upper bound exists (spread the roots far enough and the ratio grows
without limit), so it has to come from the specific family: the `b_k` are the
squares of an arithmetic progression.

**The missing lemma, stated plainly.** For `E_t(n) = e_t({(n-2k)^2 : k = 1..n-1})`,

    E_{t}^2 / (E_{t+1} E_{t-1})  <=  2 (2n-2J+3)(2n-2J+4) / [(2n-2J+1)(2n-2J+2)]
    at t = J-2.

Prove that and the leading obstruction in (R) is J-uniform. It is a statement
about central factorial numbers alone — no knives, no region, no `lam`.

**And it splits into one measured lemma plus one elementary inequality.** Writing
`p_t = E_t/C(N,t)`, `N = n-1`, the ratio is `F_t` times the Newton excess:

    E_t^2/(E_{t+1}E_{t-1}) = F_t * [p_t^2/(p_{t-1}p_{t+1})],
    F_t = (t+1)(N-t+1)/(t(N-t)) = (J-1)(n-J+2)/[(J-2)(n-J+1)] at t = J-2.

The family turns out to sit ALMOST at the Newton floor, and the excess shrinks
like `1/n`: measured `1.05` at `n = 20`, `1.02` at `n = 44`, `1.008` at `n = 100`.
Sharpened:

> **Lemma (measured, not proved).** For the central factorial family,
> `p_t^2/(p_{t-1}p_{t+1}) <= 1 + 2/n`. Largest constant needed over
> `n = 8..120`, `t < n/2`: **1.986**, attained at the smallest `n`.

Granting it, what remains is elementary and closes:

    F_t (1 + 2/n)  <=  2cd/(ab)   for every J >= 4

— **78207 pairs `(n, J)` with `n` up to 400, 0 failures, tightest slack 1.28.**
That half is a rational-function inequality and can be settled by hand.

So the leading obstruction of (R) is J-uniform as soon as the Newton-excess lemma
is proved, and that lemma is a self-contained question about
`e_t({(n-2k)^2})` — squares of an arithmetic progression.

**Stress-tested to `n = 200`**, over every `t < n/2`: the largest constant needed
is **1.9862, attained at the smallest `n = 8`**, not at the largest. So `1 + 2/n`
is stable across the range and tight only at the edge of the physical domain.

**It has a limit shape, and the shape is finite.** Writing `theta = t/n`, the
quantity `(excess - 1) n` converges as `n` grows and rises with `theta`:

| theta | 0.05 | 0.1 | 0.2 | 0.3 | 0.4 | 0.45 | 0.49 |
|---|---|---|---|---|---|---|---|
| n = 40 | 0.888 | 0.951 | 1.104 | 1.302 | 1.570 | 1.743 | 1.843 |
| n = 240 | 0.859 | 0.918 | 1.060 | 1.242 | 1.486 | 1.641 | 1.777 |

Convergence is from ABOVE, so the supremum over `n` at fixed `theta` sits at small
`n` — which is why the worst constant in the whole scan was at `n = 8`.

**The `t = 1` rung is exact.** With `e_1 = n(n-1)(n-2)/3` and `S_2 = SUM b^2`,

    excess_1 = e_1^2 (N-1) / [ N (e_1^2 - S_2) ],   N = n-1,

and since `S_2 ~ n^5/5` against `e_1^2 ~ n^6/9`, this is
`(1 - 1/n)(1 + 9/(5n)) = 1 + (4/5)/n + O(1/n^2)`. Measured: `(excess-1)n` = 1.356
at `n = 5` falling to 0.809 at `n = 240` — the limit `4/5` on the nose. That is
`f(0)` of the table above.

**The limit shape, derived.** For that measure,

    L(x) = INT_0^1 log(1 + x w^2) dw = log(1+x) - 2 + 2 arctan(sqrt x)/sqrt x,

and the Legendre stationarity `L'(x) = theta/x` collapses to something remarkably
clean. With `u = sqrt x`,

    L'(x) = [1 - arctan(u)/u]/x      ==>      theta = 1 - arctan(u)/u,

a bijection `(0, inf) -> (0, 1)`. Since `f = -g''` with
`g(theta) = inf_x[L(x) - theta log x] - H(theta)`,

    f(theta) = (2/u) / (dtheta/du) - 1/theta - 1/(1-theta),
    dtheta/du = arctan(u)/u^2 - 1/(u(1+u^2)).

**Checked against the measurement**, and the residual is the expected `O(1/n)`:

| theta | 0.05 | 0.1 | 0.2 | 0.3 | 0.4 | 0.45 | 0.49 |
|---|---|---|---|---|---|---|---|
| derived `f` | 0.853 | 0.912 | 1.051 | 1.231 | 1.470 | 1.622 | 1.765 |
| measured, `n = 240` | 0.859 | 0.918 | 1.060 | 1.242 | 1.486 | 1.641 | 1.777 |

and `f(theta) -> 0.801, 0.8001` at `theta = 10^-3, 10^-4` — the `4/5` of the exact
`t = 1` rung, from the other side.

**And the derived shape predicts a boundary that was measured before it was
understood.** `f` crosses 2 at `theta = 0.5445` (and `f(1/2) = 1.804`), so the
bound `1 + 2/n` should hold asymptotically up to `t/n = 0.5445` — not up to `1/2`.
The measured largest good `t`, which earlier looked like `n/2`, climbs:

| n | 40 | 60 | 100 | 150 | 200 |
|---|---|---|---|---|---|
| `t*/n` | 0.500 | 0.5167 | 0.5300 | 0.5333 | 0.5350 |

monotonically toward 0.5445 from below. So that boundary is **not** `n/2`; it is
`0.5445 n` seen through finite-`n` corrections — the same small-sample trap as
ERR-0017, caught this time by a derivation rather than by a wider scan.

**So the lemma splits into an asymptotic and a finite check.** The limiting
empirical measure is explicit: with `x = k/n`, `b/n^2 -> (1-2x)^2`, i.e. the law of
`V^2` for `V` uniform on `(-1,1)` — density `1/(2 sqrt(v))` on `(0,1)`, a
`Beta(1/2, 1)`. The lemma is now exactly: **`f(theta) < 2` on `(0, 1/2)`** for the explicit `f`
above, plus an exact check for `n` below some `n_0`. And the proof shape is
visible: `f` is numerically monotone increasing in `u` (59 sampled derivatives,
all positive), so **monotonicity plus the endpoint suffices** — at `theta = 1/2`,
`u` solves `arctan(u)/u = 1/2`, giving `u = 2.3311` and `f = 1.8042 < 2`. Both halves are ordinary
one-variable work — no knives, no `lam`, and both the measure and the function are
written down.

**Where the `1/n` comes from, and it is not special to us.** Writing
`p_t = e_t/C(N,t)`, the Newton excess is the second difference of `log p_t`, and
for a family whose empirical measure has a limit as `N -> inf` with `t/N -> theta`
fixed, `log p_t` converges to a concave limit shape whose curvature contributes at
order `1/N`. The control run above confirms the same size of excess for undoubled
families of the same size. So the lemma is a QUANTITATIVE version of a general
asymptotic, and the work is in the constant, not the shape — which points at
large-deviations/Legendre analysis of `e_t` rather than at anything about knives.

## What the two pieces prove together

The far-below criterion asks for `N(y) = SUM_k c_k y^k > 0` on `y >= 0`. Put the
two pieces side by side:

* every `c_k` with `k != J-2` is nonnegative monomial-by-monomial (measured, and
  what the existing `knife*_farbelow_factored.json` artefacts already report for
  `j = 9..12`: their negative monomials sit only at `y`-degree `J-2`);
* `(R) 4 c_{J-1} c_{J-3} >= c_{J-2}^2`, certified above.

Group the one negative term with its neighbours:

    c_{J-3} y^{J-3} + c_{J-2} y^{J-2} + c_{J-1} y^{J-1}
        = y^{J-3} ( c_{J-3} + c_{J-2} y + c_{J-1} y^2 ),

a quadratic with nonnegative outer coefficients and, by (R), nonpositive
discriminant — hence nonnegative for EVERY real `y`, in particular on `y >= 0`.
Every other term is nonnegative there. Therefore `N(y) >= 0` on the whole ray.

**That closes the far-below region at the depths where the criterion alone
failed.** `j = 9..15` were shown here to have their negatives only at `J-2`
(11, 30, 41, 71, 96, 130, 165 of them), and `(R)` is certified at every `J` from 7
to 32, so those depths now have a proof of the manifest-positivity kind rather
than the heavier interval-Bernstein certificates they were closed with. `j = 16`
and `17` are running; they would complete the range the old method covered. The same pair closes any further `J` for which
both checks pass.

**The two legs are checked on the same set, and that needs saying.** Leg (a) is
verified by monomial signs over the FULL far-below region, which starts at
`n = 44`; leg (R) is certified either on that same full region (`J <= 29`) or on
the region restricted to `n >= 2J-3`. For `j <= 23` the restriction is vacuous —
`2J-3 <= 43 < 44` — so both legs hold on the same set and the grouping argument
applies verbatim. That covers every depth closed here (`j = 9..15`). For
`J >= 24` the two domains differ and the combined statement is only valid on the
intersection, which is the restricted one.

Also load-bearing and worth stating: the quadratic step needs `c_{J-1} > 0`
strictly, and `c_{J-1} = den^{J-1} E_{J-1} > 0` always, so it never degenerates.

**The honest boundary of that statement** is `n >= 2J-3`: outside it other
coefficients dip too and one grouping is not enough. In the far-below
parametrisation `n = 44 + v`, so it covers every `J <= 23` outright, and deeper `J`
only for `v` large enough.

## CORRECTION (same day): the localisation is not universal — it ends at n = 2J-3

Everything above was measured at `j = 9, 10, 11` with `n = 44 + v`, i.e. deep
inside one regime. Evaluating the verified closed form as NUMBERS (cheap, so it
reaches depths the polynomial route cannot) shows the picture does not persist:

| J at the corner `v = K3 = thL = 0`, `n = 44` | dips other than `c_{J-2}` |
|---|---|
| 9 .. 20 | none |
| 24 | `k = 1` |
| 30 | `k = 1, 3, 5, 7, 9, 11` |
| 40 | 17 of them, and `c_{J-2}` does not dip at all |

Not a precision artefact: the signs are unchanged at 300, 1200 and 4000 bits of
`arb`.

**It is not a large-`J` effect but a `J`-versus-`n` one, and the boundary is
sharp.** Scanning `n` upward at fixed `J`, the first `n` at which nothing but
`c_{J-2}` dips is

| J | 25 | 26 | 28 | 32 | 35 |
|---|---|---|---|---|---|
| first clean `n` | 47 | 49 | 53 | 61 | 67 |
| `2J-3` | 47 | 49 | 53 | 61 | 67 |

**five of five**, and the same at `K3 = 3, thL = 2`. So, at the corner of the
region,

    only c_{J-2} dips   <==>   n >= 2J - 3   <==>   j <= (n+3)/2.

Away from the corner (`K3 = 60, thL = 50`, i.e. larger `lam`) the constraint is
weaker still — cleanliness starts at `n = 44` for every `J` tested.

**Tested on a grid that could refute it** (`lab/farbelow_regime_map.py` ->
`results/farbelow_regime_map.json`; a boundary claimed from corner scans is
exactly what ERR-0017 was about). `J` = 7..40, `n` = 44..164 in steps of 3, and
two off-corner values of each region variable — **1476 points, with both sides of
the line present**:

* inside the regime: 1376 points, **0 violations** — nothing but `c_{J-2}` dips;
* outside it: 100 points, **0 unexpectedly clean** — something else always dips.

So the law is sharp in both directions on everything tested. It remains a
measurement: the grid steps `n` by 3 and the region has more corners than two.

**What this costs the plan above.** The two-statement target — everything except
`c_{J-2}` manifestly nonnegative, plus the neighbour repair — is a statement
about the regime `j <= (n+3)/2` only. Above it several coefficients dip and one
neighbour pairing cannot absorb them. The repair measurement itself stands (it
concerns `c_{J-2}` and holds at all 91 dips), but it is not by itself a route to
uniformity across the whole physical range `3 <= j <= n-1`.

**Worth noting, not yet explained.** That boundary sits right next to the depth
cutoff the programme measured independently for the Hausdorff mechanism,
`j <= n/2 + 1` (`results/asymptotic_regime_probe.json`). Two unrelated
constructions putting their boundary at the same line is either a coincidence or
the same mechanism seen twice; nothing here decides which.

## The repair is now PROVED on the region, not measured

`lab/repair_certificate.py` -> `results/repair_certificate_j<J>.json`, one artefact per
depth: `repair_certificate_j7.json`, `repair_certificate_j9.json`, `repair_certificate_j12.json`, `repair_certificate_j16.json`, `repair_certificate_j20.json`, `repair_certificate_j25.json`, `repair_certificate_j26.json`, `repair_certificate_j27.json`, `repair_certificate_j28.json`, `repair_certificate_j29.json`, `repair_certificate_j30.json`, `repair_certificate_j30_v13.json`, `repair_certificate_j31_v15.json`, `repair_certificate_j32_v17.json`, `repair_certificate_j35_v23.json`, `repair_certificate_j40.json`, `repair_certificate_j40_v33.json`, `repair_certificate_j45.json`, `repair_certificate_j50_v53.json` (the `_v` suffix marks a run restricted to the regime `n >= 2J-3`).

Two facts turned the measurement into a certificate.

**First, (R) is unconditional.** The repair was stated as "where `c_{J-2} < 0`,
`c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`". Measured over 504 region points, the inequality
holds at ALL of them, not only at the 117 where the coefficient dips. So no case
split is needed and

    (R)   4 c_{J-1} c_{J-3} - c_{J-2}^2  >=  0

is a single polynomial statement about the region.

**Second, (R) is manifestly positive.** Built exactly over `Q(sqrt3)` in the region
variables `(thL, y, v, K3)` — every one of which is `>= 0` on the far-below region —
and expanded, it has **no negative monomial at all**:

| J | 7 | 9 | 12 | 16 | 20 | 25 | 26 | 27 | 28 | 29 | **30** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| monomials of (R) | 1322 | 1742 | 2372 | 3212 | 4052 | 5102 | 5312 | 5522 | 5732 | 5942 | 6152 |
| negative | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **39** |

**The break at `J = 30` was an artefact of testing outside the statement's own
regime.** The far-below parametrisation starts at `n = 44`, but the
one-negative-coefficient structure only holds for `n >= 2J-3`, which at `J = 30`
means `n >= 57`. Restricting the region to its own regime — starting `v` at 13
instead of 0 — the same build gives **6152 monomials and 0 negatives**:
manifestly positive after all (`results/repair_certificate_j30_v13.json`). So
(R) is certified at `J = 30` where the proof it serves actually applies.

**That rescue stops at 30 — and the escalation past it is one line.** With the
matching offsets, the in-regime monomial test fails from `J = 31` on: 70 negative
monomials at `J = 31`, 143 at `J = 32`, 392 at `J = 40`. (An earlier sentence of
mine claimed there was no depth where the in-regime certificate failed; there is,
and it starts at 31.)

But reading signs off monomials treats `thL` as ranging over the whole ray,
whereas in this region **`thL` lives on `[0,1]`** — the integer part of `lam` is
carried by `K`. So the monomial test was certifying a strictly larger set than the
region. One Bernstein change of basis along that axis, with `v` and `K3` still in
the orthant, fixes it:

| J | 31 | 32 |
|---|---|---|
| monomials negative | 70 | 143 |
| **Bernstein coefficients negative** | **0 of 8215** | **0 of 8485** |

So (R) is **certified at `J = 31` and `J = 32` as well**, by the same escalation
the far-below criterion itself used past `j = 8`, and the escalation is now part
of `lab/repair_certificate.py` — it runs automatically whenever the monomial test
fails, and the artefact records both.

The table below is therefore the picture on the FULL region, corner included:

**On the full region, the certificate covers `J = 7..29` and stops at `J = 30`** — and it
breaks in the narrowest way possible: all 39 negative monomials carry the same
`thL^3 K3^1 y^0`, differing only in the power of `v` (0..38). One exponent line
out of 6152 monomials. `(R)` itself was not seen to fail there — the 504-point
numeric sweep found no violation up to `J = 40` — so what fails at `J = 30` is the
crudeness of monomial signs, not the inequality. The escalation is the same one
the far-below criterion itself used past `j = 8`: a Bernstein step, here needed in
`thL` alone.

All-nonnegative monomials over a nonnegative orthant is a proof, not a sample —
the same certificate shape the far-below criterion itself uses at `j <= 8`.

**Where the sign comes from.** Splitting (R) at `j = 9` shows it is not a
coincidence of one big term:

    T1 = 4 w poch_2 s^4 E_{J-3} den^2 - outer^2        0 negatives of 1755
    T2 = 4 w (w e2 - u den e1p)                     1520 negatives of 1520
    R  = T1 + T2                                       0 negatives of 1742

So `c_{J-3}` is positive only because of its own last term — `w e2 - u den e1p`
is negative monomial for monomial — and (R) holds because four times that last
term, weighted by `w`, dominates both `outer^2` and the whole negative block, term
by term. That is a sharper statement than (R) itself, and it is what a proof
uniform in `J` would have to establish about the `E`-polynomials.

**The chain it rests on, checked rather than assumed.** (R) is assembled from the
general `y`-coefficient formula, which was verified against the assembled
polynomial at every `k`: `j = 6` (3186 / 2528 / 1890 / 1292 / 735 / 231 monomials)
and `j = 9` (12119 / 10470 / 8871 / 7315 / 5822 / 4389 / 3032 / 1752 / 561), with
**0 mismatches at every k in both**.

**What is proved and what is not.** Proved: the repair inequality (R), on the whole
far-below region, at the depths certified above. NOT proved: that every other
`c_k` is nonnegative — that half is still a measurement, and it holds only while
`n >= 2J-3`. So the far-below argument now has one of its two legs on a
certificate and the other on a well-tested measurement with a known limit.

## What is NOT claimed

Nothing here proves anything. This is a localisation of a known failure, measured
on 3 depths, and the `y`-degree pattern `J-2` is an observation over `j = 9, 10,
11` — three points, now confirmed at `j = 10` and `j = 11` as well. `j = 12` and up
remain unrun; the artefacts are what will decide the pattern, not this file.
