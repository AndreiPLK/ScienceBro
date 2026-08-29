# The B-form, the derivative form, and an all-depths positivity theorem

2026-08-28. Derivations in `lab/bform_positivity.py`,
`lab/bform_derivative_form.py` and `lab/bform_jacobi_bound.py`; machine checks
in `results/bform_positivity.json`, `results/bform_derivative_form.json` and
`results/bform_jacobi_bound.json`.

These are the first statements in the programme that give knife positivity at
EVERY depth at once from an argument rather than from a search. Two of them are
proved (§3 and §4b); both hold only in a corner of the domain, and the corner is
stated in full in §6 rather than buried. §4b supersedes §3 quantitatively — its
region is linear in `n` where §3's is quadratic — but §3 is kept because it is
the shorter argument and because the reason it loses a factor of `n` is itself
informative.

## 0. Setup

From the repository's exact closed form (`lab/knife_closed_form.py`, re-derived
in `lab/moment_kernel_probe.py`), with `j` the knife order, `r = j - 1`,
`H = (D + 4n - 7)/2`, `s = lam + n - 1` and `(a)_t = a(a-1)...(a-t+1)` the
falling factorial:

    sign(knife_j) = sign(K_r),
    K_r = sum_{t=0}^{r} (-1)^t C(r,t) M_t^(r),
    M_t^(r) = t! (H-r)_t E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ].

Physical domain: `3 <= j <= n-1` (so `2 <= r <= n-2`), `D > 3`, `lam > 0`.
The upper limit is load-bearing, not cosmetic: for even `n`, `e_{n-1}(b) = 0`
exactly (the root `b_{n/2} = 0` enters at the last order), which would be the
`t = r` term at `r = n-1`, i.e. `j = n`. Theorems 5 and 6 must not be quoted
there — their Newton step assumes no `e_t` vanishes for `t <= r`, which holds
precisely because `r <= n-2`.

## 1. The B-form

**Theorem 1.** With `b_k = (n-2k)^2 / s^2` for `k = 1..n-1`,

    K_r = sum_{t=0}^{r} (-1)^t c_t e_t(b),
    c_t = (r)_t (H-r)_t / [ (n-1)_t (n-3/2)_t ].

*Proof.* Two substitutions. First `C(r,t) t! = (r)_t`, which absorbs the
binomial. Second, `E_{2t}(n)` is by definition the `t`-th elementary symmetric
function of `{(n-2k)^2 : k = 1..n-1}`, and `e_t` is homogeneous of degree `t`,
so `E_{2t}(n)/s^{2t} = e_t(b)`. QED

**Why this form.** `max_k b_k = (n-2)^2/s^2 < 1` for every `lam > 0`, since
`s = lam + n - 1 > n - 2`. The alternating sum is now built from elementary
symmetric functions of numbers that all lie strictly inside the unit interval,
uniformly in `n` and `lam`; and `c_t` carries no `lam` at all, so the coupling
and the geometry are cleanly separated. The earlier route
(`results/measure_mass_test.json`) instead produced a measure whose support was
exactly the obstruction.

**Lemma 2.** `sum_{k=1}^{n-1} (n-2k)^2 = n(n-1)(n-2)/3`, hence
`e_1(b) = n(n-1)(n-2)/(3 s^2)` and the mean `bbar := e_1/(n-1) = n(n-2)/(3 s^2)`.

*Proof.* `sum (n^2 - 4nk + 4k^2) = n^2(n-1) - 4n·n(n-1)/2 + 4(n-1)n(2n-1)/6
= n(n-1)[ n - 2n + (4n-2)/3 ] = n(n-1)(n-2)/3`. QED

## 2. The Leibniz criterion, uniform in depth

Write `T_t = c_t e_t(b)`.

**Lemma 3.** `T_t > 0` for `0 <= t <= r` on the physical domain.

*Proof.* `(r)_t > 0` for `t <= r`; `(n-1)_t > 0` and `(n-3/2)_t > 0` for
`t <= n-1`. For `(H-r)_t = prod_{i<t}(H-r-i)` the smallest factor is
`H - r - (t-1) >= H - 2r + 1 = (D-1)/2 + 2(n-1-r) > 0` for `D > 1` and
`r <= n-2`. Finally `e_t(b) > 0`: the `b_k` are nonnegative and at most one of
them vanishes (`b_k = 0` only for `n = 2k`), so at least `n-2` are strictly
positive and every `e_t` with `t <= n-2` has a strictly positive term. QED

**Theorem 4 (criterion).** If `T_{t+1} <= T_t` for all `0 <= t < r`, then
`K_r >= 0`; if moreover `T_1 < T_0`, then `K_r > 0`.

*Proof.* `K_r = (T_0 - T_1) + (T_2 - T_3) + ...`, a sum of nonnegative brackets
plus, when `r` is even, a final `+T_r > 0`. The grouping does not depend on the
parity of `r`, so the criterion is uniform in depth. QED

## 3. The closed-form region

**Theorem 5.** If

    r (H - r) n (n - 2)  <=  (3n - 9/2) s^2                              (*)

then `K_r >= 0`, strictly if the inequality is strict.

*Proof.* All `b_k >= 0`, so `prod_k (1 + b_k x)` has only real roots and
Newton's inequalities hold for `p_t = e_t / C(N,t)`, `N = n-1`:
`p_t^2 >= p_{t-1} p_{t+1}`, whence the ratios `p_{t+1}/p_t` are non-increasing
and `p_{t+1}/p_t <= p_1/p_0 = bbar`. (If some `p_t = 0` the chain terminates,
but by Lemma 3 no `e_t` with `t <= r` vanishes, so this does not occur here.)
Therefore

    e_{t+1}/e_t = (p_{t+1}/p_t)(N-t)/(t+1) <= bbar (n-1-t)/(t+1),

and since `c_{t+1}/c_t = (r-t)(H-r-t)/[(n-1-t)(n-3/2-t)]` the factor `(n-1-t)`
cancels:

    T_{t+1}/T_t <= f(t) := (r-t)(H-r-t) bbar / [ (n-3/2-t)(t+1) ].

`f` is decreasing on `0 <= t < r`: `(r-t)/(n-3/2-t)` has derivative in `t` of
sign `r - n + 3/2 < 0` (using `r <= n-2 < n-3/2`); `(H-r-t)` is decreasing and
positive by Lemma 3; `1/(t+1)` is decreasing; all three factors are positive.
Hence `f(t) <= f(0) = r(H-r) bbar/(n-3/2)`, and `f(0) <= 1` is exactly `(*)`
after substituting `bbar = n(n-2)/(3s^2)` and clearing `(n-3/2)`. Theorem 4
then applies. QED

**Theorem 6 (all depths at once).** For `D > 3`,

    D  <=  D*(n, lam) := (6n-9) s^2 / ( n (n-2)^2 ) - 2n + 3
      ==>  knife_j > 0 for every admissible j.

*Proof.* `r -> r(H-r)` is a downward parabola with vertex at `r = H/2`, and
`H/2 = (D+4n-7)/4 > n-2` exactly when `D > -1`, so in particular throughout the
physical domain `D > 3`. So on `2 <= r <= n-2` the left
side of `(*)` is increasing in `r` and its worst case is `r = n-2`, where
`H - r = (D+2n-3)/2`. Substituting and solving `(*)` for `D` gives the stated
bound; it is independent of `r`, so one inequality covers every depth. QED

## 4. The derivative form

The lam-free factor of `c_t` is `w_t = (r)_t/(n-1)_t`. Put `N = n-1`,
`m = N - r`.

**Theorem 7.** `w_t = C(N-t, N-r)/C(N,r)`, a polynomial in `t` of degree `m`
that vanishes identically for `t = r+1..N`. Consequently the sum may be run to
`t = N`, and with `eta_1..eta_r` the roots of the `m`-th derivative of
`prod_{k=1}^{n-1} (u - b_k)`:

    K_r  =  sum_{t=0}^{r} (-1)^t d_t e_t(eta),   d_t = (H-r)_t/(n-3/2)_t,
         =  INT_1^inf  prod_{i=1}^{r} (1 - eta_i y)  dsigma(y),

    dsigma(y) = [Gamma(C+eps+1)/(Gamma(C+1)Gamma(eps))] y^{-C-eps-1}(y-1)^{eps-1} dy

on `[1, inf)`, with `C = n-3/2` and `eps = H - r - C = D/2 + (n-2-r) > 0`.

*Proof.* The binomial identity `C(r,t)/C(N,t) = C(N-t,N-r)/C(N,r)` gives the
first claim, and `C(N-t,N-r) = 0` whenever `t > r`. Since `x^{N-t}` differentiated
`m` times at `x = 1` equals `(N-t)_m`, and `w_t = (N-t)_m/[m! C(N,r)]`,

    sum_{t=0}^{N} (-1)^t (N-t)_m e_t(b) y^t = (d/dx)^m [ prod_k (x - b_k y) ]|_{x=1}.

Substituting `x = y u` turns `prod_k (x - b_k y)` into `y^N prod_k (u - b_k)`,
so the roots in `x` are `y` times the roots of the `m`-th derivative of
`prod_k (u - b_k)`, which are independent of `y`. The leading coefficient
`N!/r!` divided by `m! C(N,r)` is exactly 1, so the constants cancel and the
sum equals `prod_i (1 - eta_i y)` weighted by `d_t`. For the integral, the
Beta integral `B(eps, C-t+1) = Gamma(eps)Gamma(C-t+1)/Gamma(C+eps-t+1)` turns
`d_t = (C+eps)_t/(C)_t = Gamma(C+eps+1)Gamma(C-t+1)/[Gamma(C+1)Gamma(C+eps-t+1)]`
into `INT_1^inf y^t dsigma(y)`, convergent for `t < C + 1 = n - 1/2`, hence for
every `t <= r <= n-2`. QED

**What it buys.** `prod_k (u - b_k)` has only real roots in `[0, B]`,
`B = (n-2)^2/s^2 < 1`, so by Rolle every `eta_i` is real and in `[0, B]` too.
The alternating sum is gone: what remains is a product of `r` real linear
factors integrated against one explicit density on one variable, strictly
positive for `y < 1/max_i eta_i`. Differentiating `m` times CONTRACTS the root
span — at `r = 1` the single root is the mean of the `b`'s and the span grows
back to the full range as `r -> N`. Measured at `n = 20`, `lam = 7`:
`max(eta)/B = 0.448, 0.561, 0.650, 0.795, 1.000` at `r = 2, 4, 6, 10, 18`.

This is a structural identity, **not** a positivity proof: `sigma` has unbounded
support, so positivity of the integrand on `y < 1/max(eta)` does not close the
argument by itself.


## 4b. The J-form: compact support, and a bound linear in n

The `sigma` of Theorem 7 lives on the unbounded ray `[1, inf)`, and that
unboundedness is exactly what stopped the derivative form from closing. It is
removable. Writing the same representation in its original variable,
`d_t = [1/B(eps,C+1)] INT_0^1 v^{eps-1}(1-v)^{C-t} dv`, and substituting
`w = 1 - v`:

**Theorem 8 (J-form).**

    K_r = [1/B(eps, C+1)] INT_0^1 w^{a-1} (1-w)^{b-1} prod_{i=1}^{r} (w - eta_i) dw,
    a := C - r + 1 = n - 1/2 - r,      b := eps = D/2 + (n - 2 - r).

*Proof.* Substituting `w = 1-v` in the Beta integral of Theorem 7 gives
`d_t = [1/B(eps,C+1)] INT_0^1 (1-w)^{eps-1} w^{C-t} dw`. Multiply by
`(-1)^t e_t(eta)` and sum: pulling out `w^{C-r}` leaves
`sum_t (-1)^t e_t(eta) w^{r-t} = prod_i (w - eta_i)`. The exponent `C-r = n-3/2-r
>= 1/2` is positive, so the integral converges at 0. QED

So the knife is a **Jacobi (Beta) moment of a real-rooted polynomial over the
compact interval [0,1]**, with every root in `[0, B]`, `B = (n-2)^2/s^2 < 1`.
The integrand is positive for `w > eta_max` and alternates below it, and the
whole question becomes how far above the roots the `Beta(a,b)` weight sits.

**Theorem 9 (the bound).** Let `eta = max_i eta_i`. If `b >= 1` and

    a (1 - eta)^{a+b+r-1} B(a+r, b)  >=  eta^{a+r}                        (**)

then `K_r >= 0`.

*Proof.* Split the integral at `w = eta`. On `[eta, 1]` every factor satisfies
`w - eta_i >= w - eta >= 0`, so the product is at least `(w-eta)^r`;
substituting `w = eta + (1-eta)u` and using `w >= (1-eta)u` — which may be
raised to the power `a-1` because `a = n-1/2-r >= 3/2 >= 1` on the physical
domain — gives

    INT_eta^1 >= (1-eta)^{a+b+r-1} INT_0^1 u^{a+r-1}(1-u)^{b-1} du
              = (1-eta)^{a+b+r-1} B(a+r, b).

On `[0, eta]` each `|w - eta_i| <= max(w, eta_i) <= eta`, so the product is at
most `eta^r` in absolute value, and for `b >= 1` we have `(1-w)^{b-1} <= 1`, so
`INT_0^eta <= eta^r · eta^a/a`. The difference of the two bounds is nonnegative
exactly under `(**)`. QED

Both sides of `(**)` are monotone in `eta`, so the uniform bound
`eta <= B = (n-2)^2/s^2` may be substituted, leaving a hypothesis in
`(n, r, lam, D)` alone. Note `b >= 1` holds throughout the physical domain:
`b = D/2 + (n-2-r) >= D/2 > 3/2`.

**Verification** (`lab/bform_jacobi_bound.py`,
`results/bform_jacobi_bound.json`). Soundness against the exact reference
engine: over 1239 cases the hypothesis fired 469 times, and in **0** of those
was the reference knife non-positive. Every inequality is decided on a certified
`arb` enclosure in log form — accepted only when the enclosure of the difference
is strictly positive — never on a midpoint.

**The region, and it is linear.** The smallest `lam` at which `(**)` holds for
every depth at the shore:

| n | 6 | 20 | 40 | 60 | 100 | 160 | 260 | 420 |
|---|---|---|---|---|---|---|---|---|
| lam | 83 | 531 | 1179 | 1824 | 3112 | 5040 | 8249 | 13380 |
| lam / n | 13.8 | 26.6 | 29.5 | 30.4 | 31.1 | 31.5 | 31.7 | 31.9 |
| lam / (n ln n) | 4.9 | 8.9 | 8.0 | 7.4 | 6.8 | 6.2 | 5.7 | 5.3 |

`lam/n` plateaus near 32 while `lam/(n ln n)` keeps falling, so the growth is
LINEAR in `n`, not `n log n`. Using the exact `eta_max` in place of the uniform
bound `B` closed 0 extra cases of 16 tested, so `B` is not the bottleneck.

## 5. Verification

`lab/bform_positivity.py` (`results/bform_positivity.json`):

- B-form identity against the reference engine: **870 trials, 0 mismatches**,
  including **37 points where the reference knife is negative** — so the check
  is not vacuous.
- `e_1(b) = n(n-1)(n-2)/(3s^2)`: 0 violations over `n = 3..59`.
- Both implications, exactly, over 612 cases: closed form true but Leibniz
  false — **0**; Leibniz true but `K_r < 0` — **0**. Either would have broken
  the proof.
- The fast shore used at the `lam ~ n^2` scale agrees with the linear scan on
  `lam = 1/2..300`: 0 disagreements.

`lab/bform_derivative_form.py` (`results/bform_derivative_form.json`):

- `w_t = C(N-t,N-r)/C(N,r)` including the automatic zeros: 18200 checks, 0
  violations.
- D-form against the B-form and against the reference engine: 870 trials, 0
  disagreements either way, again with 37 negative reference points.
- `eta` real and inside `[0, B]` via certified root enclosures: 0 violations
  over 45 cases.
- The `sigma` representation of `d_t` by interval arithmetic on the Gamma
  ratio: 0 violations.

## 6. The honest size of the region

`D*(n, lam)` reaches the shore at

| n | 8 | 12 | 16 | 20 | 28 | 40 | 60 | 100 |
|---|---|---|---|---|---|---|---|---|
| smallest lam | 127 | 340 | 654 | 1069 | 2202 | 4659 | 10773 | 30572 |
| lam / n^2 | 1.98 | 2.36 | 2.56 | 2.67 | 2.81 | 2.91 | 2.99 | 3.06 |

So the proved region is `lam ~> 3 n^2` at the shore, and the ratio is still
drifting upward at `n = 100`. End-to-end spot check inside the region: at
`n = 8, 12, 16, 20` with `lam` just above the threshold, every knife
`j = 3..n-1` is positive at the shore, as the theorem requires.

**Against what is already measured:**
`results/asymptotic_regime_probe.json` sees the Hausdorff mechanism — which also
covers every depth at once — from about `lam ~> 2n`, with an exact depth cutoff
`j <= n/2 + 1`. That region is not proved. So the three statements stand as:

| route | status | region | depth coverage |
|---|---|---|---|
| Leibniz + Newton (Thm 6) | proved | `lam ~> 3 n^2` | all depths |
| J-form bound (Thm 9) | proved | `lam ~> 32 n` | all depths |
| Hausdorff corner | measured only | `lam ~> 2n` | `j <= n/2 + 1` |

The J-form bound is the same object handled better: at `n = 60` it needs
`lam = 1824` where Leibniz needs `10773`, and the ratio between them grows with
`n` because one region is linear and the other quadratic. It is now within a
constant factor — about 16 — of what the programme has measured, instead of a
factor growing like `n`. None of the three is the keystone: all are corners of
an unbounded domain, and the whole region below the shore at small `lam` remains
open.

**Why the gap is real and not slack.** The binding step is `f(0) <= 1`, i.e.
`T_1 <= T_0`, and at `t = 0` Newton's inequality is an EQUALITY
(`p_1/p_0 = bbar` exactly). So `(*)` is not a lossy consequence of Leibniz — it
is essentially Leibniz's first step itself. On the 612-case grid the closed-form
hypothesis and the full Leibniz criterion hold in exactly the same 265 cases.
Closing the gap therefore required abandoning term-by-term monotonicity, not
sharpening the constant — which is what §4b does, and it is where the factor of
`n` was recovered.


## 6b. What the domain-critic pass changed (2026-08-28)

The critique is in `results/BFORM_CRITIQUE.md`. Every one of its checkable
findings was re-verified exactly here before being accepted; four changed the
content of this file.

**Two arithmetic slips, both mine, both corrected above** (Lemma 3's identity and
Theorem 6's parenthetical) and recorded as ERR-0014. Both were conservative,
which is exactly why the machine checks did not catch them.

**Theorem 6 is VACUOUS at the small `lam` the programme actually works at.**
`D*(n, lam)` must exceed 3 to say anything, and it does not:

| | lam = 1 | lam = 5/2 | lam = 7 |
|---|---|---|---|
| `D*(4, ·)` | 10.00 | 23.36 | 88.75 |
| `D*(6, ·)` | **1.13** | 6.82 | 31.50 |
| `D*(12, ·)` | **-13.44** | **-11.43** | **-3.99** |

So at `n = 12` the theorem is empty at `lam = 1, 5/2, 7` — every value used in
the project's own cancellation sweeps — and at `lam = 1` (Virasoro–Shapiro) it is
empty for every `n >= 6`. This belongs in the statement, not in a footnote.

**The all-depths threshold understates the theorem by a factor of `n` at shallow
depth.** Condition `(*)` is depth-resolved; Theorem 6 quotes only its worst case
`r = n-2`. Solving `(*)` at FIXED `r` gives a threshold linear in `n`:

| | r = 2 | r = 4 | r = 8 |
|---|---|---|---|
| n = 12 | 51 | 124 | 268 |
| n = 24 | 104 | 253 | 550 |
| n = 48 | 209 | 512 | 1112 |

`lam*/(r n)` sits at 2.13–2.90 and is flat in `n`, so the honest statement of the
Leibniz route is `lam* ~ c · r · n` per depth, with the quadratic `3 n^2` being
only what one gets after taking the worst depth. The critic's closed form for the
all-depths asymptote, `lam*/n^2 -> (12 + 4 sqrt 3)/6 = 3.1547`, matches the
measurement (3.131 at `n = 420`, still rising).

**The representation explains the parity dichotomy in one line.** As `D -> inf`
the Beta weight's mass goes to 0, so the `w -> 0` end dominates and
`sign(K_r) -> sign(prod_i (-eta_i)) = (-1)^r = (-1)^{j-1}`. **Read ERR-0016 before
quoting this.** What the limit proves is that every even-`j` knife is negative for
all sufficiently large `D`. What it does NOT prove — and what I wrongly wrote here
— is that odd-`j` knives never dip: the limit constrains the sign at infinity, not
at finite `D`. Odd-`j` knives DO dip negative at small `lam` (72 cases in
`results/shore_gap_scan.json`; `n = 6`, `j = 3`, `lam = 1/10` is `+` at `D = 12`,
`-` at `D = 13`, and `+` again from `D = 20` on, on both engines). Every such dip
lies above the shore — the closest odd-`j` approach is `D0/T_hat = 1.146` — so
nothing below the shore, and no theorem in this file, is affected. Verified at
`n = 12`, `lam = 7`, `D = 50 .. 2e5`: `j = 3, 5` stay `+1` throughout, `j = 4, 6`
are `+1` at `D = 50` and `-1` from `D = 500` on — which is the even-`j` half, the
half the limit actually derives.

## 6c. Why no constant-factor fix to this route can matter

The obvious repair to Theorem 9 is to replace the crude `|prod_i (w-eta_i)| <=
eta^r` on `[0, eta]` by the true envelope `max_{[0,eta]}|prod_i (w-eta_i)|`. That
envelope is scale-invariant in `lam` (both numerator and `eta^r` scale together),
so it is a pure function of `(n, r)`, and it is genuinely much smaller: measured
`max|P|/eta^r` is about `2.4^{-r}`, e.g. `3.96e-7` at `n = 20, r = 18`.

Substituting the measured envelope moves the threshold by **1.1x to 1.2x**
(n = 12: 272 -> 229; n = 20: 531 -> 472; n = 28: 791 -> 721).

The reason is worth stating because it closes the route. `NEG` carries
`eta^{n-1/2}` and `eta ~ 1/lam^2`, so `NEG ~ lam^{-(2n-1)}`: a gain of factor `G`
in `NEG` buys only `G^{1/(2n-1)}` in `lam`. A 2.5-million-fold improvement at
`n = 20` is `(2.5e6)^{1/39} = 1.45`. **No constant, and no factor exponential in
`r`, can move this threshold meaningfully.** Reaching `lam ~ 2n` requires a
different decomposition, not a better bound inside this one. Together with the
two fixes killed in `results/bform_gap_diagnosis.json`, that is three dead ends
on the same split, measured rather than guessed.

The critic also notes the deepest depth is structurally immune to the root
contraction: `b_1 = b_{n-1} = B` is a double root of `prod_k (u - b_k)`, so one
differentiation leaves it in place and `eta_max = B` exactly at `r = n-2`. That
matches the measurement (`max(eta)/B = 1.0000` at `r = 18`, `n = 20`) and means
any argument leaning on contraction cannot close the deepest knife.

## 7. Claim status and prior art (checked before any wording)

**Claim state: independently-validated for the mathematics; NOT validated for
novelty.** Two review passes ran on 2026-08-28, neither by the role that wrote
the proofs.

The independent-validator pass (`validation/VAL-BFORM-0001.yaml`,
`lab/validator_bform_check.py`) rebuilt the closed form from
`lab/jacobi_normal_form.py` alone — never importing the modules under review —
and returned **PASS**. It hunted 13380 adversarially chosen points with `(*)`
true (at equality in `(*)`, at `D = 3 + 1e-9`, `n = 4..60`, `lam = 1e-3..1e15`)
and found **no counterexample**; it confirmed each monotonicity factor of
Theorem 5 separately over 3952 cells, every step of Theorem 7 exactly, and the
J-form and `(**)` of §4b. Non-vacuity: 77 of 544 probes just outside `(*)` have
a NEGATIVE reference knife, so the hypothesis is not describing a trivially safe
region. It also found the two arithmetic slips (ERR-0014) and the two writing
gaps now fixed above.

The domain-critic pass (`results/BFORM_CRITIQUE.md`) supplied §6b and §6c.

**Not validated: any novelty or prior-art claim.** The literature pass has not
been done; §7's POSSIBLY_KNOWN wording stands, and the critic would strengthen
it — see below.

**The ingredients are all classical** and this file does not pretend otherwise:
Newton's inequalities on elementary symmetric functions of nonnegative reals;
Rolle (equivalently Gauss–Lucas) for the roots of a derivative; the Beta
integral for a ratio of Gamma functions; the binomial identity
`C(r,t)/C(N,t) = C(N-t,N-r)/C(N,r)`. The operation in §4 — passing from a
real-rooted polynomial to the roots of its `m`-th derivative — is precisely the
object studied in finite free probability (Marcus–Spielman–Srivastava), where
differentiation is a finite free convolution and root-span contraction is a
known phenomenon. Any claim about `max(eta)` should be checked against that
literature before being called new.

What is specific to this project is the reorganization itself: that the CHR
knife sum has a form in which all the variables `b_k` lie below 1 uniformly, and
that its lam-free weight is a polynomial in `t` that makes the depth truncation
automatic and converts the whole sum into a derivative.

**Novelty status: KNOWN for the technique (settled 2026-08-29; see
`results/FFP_LITERATURE_PASS.md`).** The literature pass was done and the answer
is unambiguous: multiplying `e_t` by a Pochhammer ratio is the finite free
multiplicative convolution `BOX_N`, classically the **Schur–Szegő composition**
(arXiv:2309.10970 §1; the preservation results are Szegő 1922 and Walsh 1922).
Verified exactly, not by resemblance: `K_r = (p BOX_{n-1} q)(1)` over 336 cases
with 0 mismatches and 65 negative-knife points
(`results/ffp_convolution_check.json`). So §1, §4 and §4b introduce **no new
operation**; what is specific here is the identification of the CHR knife with
such a composition and the two region theorems proved for it. The pass also
closed the route it opened: `q` has complex zeros in 336 of 336 cases, so the
Szegő–Walsh preservation theorem does not apply and `theta_max < 1` is not
available as a lossless criterion.

The paragraph below is the pre-pass wording, kept because its reading of the
genre turned out to be right — the same paper remarks that `BOX_n` belongs to the
framework of finite multiplier sequences.

**Pre-pass wording (2026-08-28): POSSIBLY_KNOWN for the technique, and the
domain-critic pass would nudge that to LIKELY KNOWN.** Its reading: the transform is a composition
of truncation-by-differentiation with a Pochhammer-ratio multiplier, i.e. an
Erdelyi-Kober/Weyl fractional integral, and the genre to search first is
Malo-Schur-Szego composition and Polya-Schur multiplier sequences (with
`{e_t(b)}` a Polya frequency sequence by Aissen-Schoenberg-Whitney), modernised
by Borcea-Branden; the multiplier step is the Askey-Gasper method reached from
the other end. Finite free probability (Marcus-Spielman-Srivastava, and
Hoskins-Kabluchko for derivative root distributions) is the right home for any
`max(eta)` claim. The critic explicitly ran NO literature search, so this is a
list of places to look, not a finding. Do not describe any of this as new in
outward-facing text until someone has actually looked.
