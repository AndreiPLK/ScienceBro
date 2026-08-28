# The B-form, the derivative form, and an all-depths positivity theorem

2026-08-28. Derivations in `lab/bform_positivity.py` and
`lab/bform_derivative_form.py`; machine checks in
`results/bform_positivity.json` and `results/bform_derivative_form.json`.

This is the first statement in the programme that gives knife positivity at
EVERY depth at once from an argument rather than from a search. It is also
strictly weaker than what the programme has already measured, and the gap is
stated in full below rather than buried.

## 0. Setup

From the repository's exact closed form (`lab/knife_closed_form.py`, re-derived
in `lab/moment_kernel_probe.py`), with `j` the knife order, `r = j - 1`,
`H = (D + 4n - 7)/2`, `s = lam + n - 1` and `(a)_t = a(a-1)...(a-t+1)` the
falling factorial:

    sign(knife_j) = sign(K_r),
    K_r = sum_{t=0}^{r} (-1)^t C(r,t) M_t^(r),
    M_t^(r) = t! (H-r)_t E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ].

Physical domain: `3 <= j <= n-1` (so `2 <= r <= n-2`), `D > 3`, `lam > 0`.

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
`H - r - (t-1) >= H - 2r + 1 = (D-1)/2 + 2(n-2-r) > 0` for `D > 1` and
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
`H/2 = (D+4n-7)/4 > n-2` exactly when `D > 3`. So on `2 <= r <= n-2` the left
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

**Against what is already measured:** `results/asymptotic_regime_probe.json`
sees the Hausdorff mechanism — which also covers every depth at once — from
about `lam ~> 2n`, and with an exact depth cutoff `j <= n/2 + 1`. That region is
far larger in `lam` and is NOT proved. So:

- proved, all depths, no depth cutoff: `lam ~> 3 n^2`;
- measured, all depths up to `j <= n/2+1`, not proved: `lam ~> 2n`.

Both are corners of an unbounded domain, and neither is the keystone. What this
adds is that the first line no longer depends on any search.

**Why the gap is real and not slack.** The binding step is `f(0) <= 1`, i.e.
`T_1 <= T_0`, and at `t = 0` Newton's inequality is an EQUALITY
(`p_1/p_0 = bbar` exactly). So `(*)` is not a lossy consequence of Leibniz — it
is essentially Leibniz's first step itself. On the 612-case grid the closed-form
hypothesis and the full Leibniz criterion hold in exactly the same 265 cases.
Closing the gap therefore requires abandoning term-by-term monotonicity, not
sharpening the constant — which is what the derivative form of §4 is for.

## 7. Claim status and prior art (checked before any wording)

**Claim state: source-supported by internal derivation and machine
verification; NOT independently validated.** The proofs above are written out
and every identity they rest on is machine-checked against the exact reference
engine at non-vacuous points, but nothing here has had a literature pass by
someone who knows the genre, and the project's own rule is that a claim is never
approved by the role that produced it.

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

**Novelty status: POSSIBLY_KNOWN for the technique; the application to the CHR
knives is this project's.** Do not describe any of it as new in outward-facing
text without a literature pass.
