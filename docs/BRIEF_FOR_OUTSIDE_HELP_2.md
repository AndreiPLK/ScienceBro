# One polynomial, one question. Please look where I am not looking.

Self-contained. No context from our project is needed — every definition is
below, and everything marked VERIFIED was computed in exact rational arithmetic
(flint), not floating point.

Your previous reply killed a lemma I had "verified" on 966 configurations, in one
minute, by testing where the claim was most likely to fail rather than where my
grid already was. That was worth more than a week of my own work. Same request
again.

---

## 1. The object

Fix an integer `n >= 5` and a rational `lam > 0`. Put `N = n - 1`,
`s = lam + n - 1`, and

```
q(v) = PROD_{k=0}^{N-1} ( v - (N-1-2k)/s )
```

so the roots of `q` are an **arithmetic progression** symmetric about 0, with
spacing `2/s`, running from `-(N-1)/s` to `+(N-1)/s`. Equivalently
`q(v) = (2/s)^N (x)_N` with `x = (s v + N - 1)/2` and `(x)_N` the falling
factorial. (VERIFIED as polynomials, n = 5, 6, 9, 12.)

Fix also `gamma > 0` and expand `q` in Gegenbauer polynomials:

```
q(v) = SUM_i a_i C_i^gamma(v)
```

**The question is exactly: when are all `a_i >= 0`?**

## 2. Why that question and not another

Our physical problem is the positivity of an infinite family of quantities
("knives"). Three classical facts reduce it to the above:

1. **The knife IS a Gegenbauer coefficient.** With `u = v^2` our positive
   quantity is `F = q^2`, and the quadratic transformation
   `C_{2m}^g(v) = ((g)_m/(1/2)_m) P_m^{(g-1/2,-1/2)}(2v^2-1)` together with
   `P_m^{(a,b)}(-z) = (-1)^m P_m^{(b,a)}(z)` identifies knife number `m` with the
   Gegenbauer coefficient of `F` at index `2m`, up to a POSITIVE constant.
   (VERIFIED against our exact knife engine: 264 comparisons, 0 disagreements.)
2. **Dougall:** the linearization coefficients of Gegenbauer polynomials are
   non-negative for `gamma > 0`. So if `q` has non-negative coefficients, `q^2`
   does, and every knife is positive at once.
3. **DLMF 18.18.16:** non-negativity at `gamma` implies non-negativity at any
   smaller `gamma`, so it is enough to prove it at the largest `gamma` we need.

The largest `gamma` we need is set by a curve we already published,
`gamma_shore(lam) = (T_hat(lam) - 3)/2` where
`T_hat(lam) = min_{k>=3} [ 3(2k-3)/(k(k-2)) * (lam^2 + (2k-2) lam + 1) + 2k ]`.
Numerically `gamma_shore` is 3.615 at `lam = 1/10`, 10 at `lam = 1`, 18.2 at
`lam = 2`, and asymptotically `T_hat/lam -> 12 + 4 sqrt(3) = 18.9282`. The
minimising `k` sits at `k ~ sqrt(3) lam` (measured 1.7320 at lam = 100..900).

So: **for which `(n, lam)` is `q` non-negative in the Gegenbauer basis at
`gamma = gamma_shore(lam)`?**

## 3. What is measured, and the surprise in it

Write `Y` for "all `a_i >= 0` at the shore".

**Region A — small `n`, large `lam`.** `Y` holds exactly when `lam >= lam*(n)`,
and `lam*(n)/n` is measured at **4.7165 .. 4.7260** for `n = 20..130`. (That
resembles `3 + sqrt(3) = 4.7320508`. I am NOT claiming it is.)

**Region B — large `n`, small `lam`.** This is the part I did not expect, and I
only found it today. At fixed small `lam`, `Y` FAILS for moderate `n` and then
starts holding again above a threshold:

| lam | negatives at the shore, by n | threshold |
|---|---|---|
| 1/10 | n=150: 12, n=400: 12, n=600: 6, n=700: **0** | `n* in (656, 662]` |
| 1/5 | n=900: dirty, n=1300: clean | `n* in (900, 1300]` |
| 1/20 | n=350, 500: dirty | `n* > 500` |

So the good set is **not** a half-plane. For each `lam` the BAD set of levels
appears to be a finite interval, roughly `lam/4.72 < n < n*(lam)`, with
`n*(1/10) ~ 660` and `n*(1/5) ~ 1100`.

**If that is right, then for every `lam` all but finitely many levels are settled
by the classical argument** — and the finite remainder is exactly the range our
machine certificates already cover. That would finish the theorem. I cannot
prove the shape of the bad set, and I cannot rule out that it reopens at still
larger `n`.

## 4. Structure I have extracted (all exact, all verified)

* The roots are symmetric, so `e_1 = 0` and `SUM_k t_k^2 = N(N^2-1)/(3 s^2)` —
  the same value for even and odd `N`.
* Hence a closed form for the second-highest coefficient:
  **`a_{N-2} >= 0` iff `gamma <= 3(lam+N)^2/(2(N+1)) - N + 1`.**
  (VERIFIED: 30 checks either side of the threshold, 0 mismatches.) This IS the
  binding coefficient for `lam >= 4`: at `n = 13, lam = 8` formula and
  measurement both give 35.1538; at `n = 21, lam = 8` both give 37.0000.
* The lowest coefficient is the weighted mean of `q`, with the Beta closed form
  **`a_0 = SUM_j q_{2j} (1/2)_j / (gamma+1)_j`**, i.e.
  `a_0 ∝ INT_{-1}^{1} q(v)(1-v^2)^{gamma-1/2} dv`.
  (VERIFIED against the full expansion: 24 cells, ratio 1.000000 in every one.)
  Equivalently `a_0 = E[ PROD_i (Y - r_i) ]` where `Y ~ Beta(1/2, gamma+1/2)`
  and `r_i = (a_i/s)^2` with `a_i` odd.
* **The binding index MIGRATES with `lam`**: index 0 at `lam <= 2`, then 8 or 12
  at `lam = 4`, then `N-2` from `lam = 8` upward. (I first concluded "index 0
  always binds" from measurements at `lam = 1` only. That was wrong.)
* `a_0` is **not monotone** in `gamma` — at `n = 7, lam = 1` its sign runs
  `+, -, +` as `gamma` goes 2, 4, 9 — so bisecting on it finds spurious roots.
  Only the first crossing is meaningful.
* At `lam = 1` the first positive root of `a_0(gamma) = 0` equals the true
  threshold in 6 of 6 cells, and grows like `gamma* ~ 2.8 n^0.145` (measured
  n = 9..321: 3.859, 4.050, 4.337, 4.639, 4.955, 5.311, 5.688, 6.061, 6.466).

## 5. What I tried that failed, so you do not repeat it

1. **Term-by-term via `(x)_N^2 = SUM_j C(N,j)^2 j! (x)_{2N-j}`** (all weights
   positive, so it looks like it should transfer positivity). REFUTED: about 45
   percent of the even-index Gegenbauer coefficients of the individual
   `(x)_M` are negative. The cancellation is essential.
2. **Block grouping under Dougall** — split `q^2` into blocks, prove each clean.
   CIRCULAR in practice: a greedy partition puts everything in one block, i.e.
   verifies the product directly. Cleanliness appears to be a property of the
   whole product, not of any sub-product.
3. **Factor-by-factor.** `(v^2 - t^2)` is clean iff `t^2 <= 1/(2(gamma+1))`, and
   requiring that of every factor gives only `lam >~ 19 n^2` — far worse than the
   measured `4.72 n`.
4. **`q` itself as a positive combination in some other basis** — every version I
   wrote collapsed back into checking `q^2` directly.
5. Ten earlier mechanisms (real-rootedness/Newton, total positivity/Karlin,
   Stieltjes moments, creative telescoping, closed product forms, ...) are closed
   and recorded; ask if you want that list.

## 6. Where I am probably blind — please look here

* **Is there a known theorem about Gegenbauer/ultraspherical expansions of
  polynomials whose zeros are an ARITHMETIC PROGRESSION?** That is the entire
  structure of `q`. Equivalently, the Gegenbauer projection of a single falling
  factorial `(x)_N` under an affine change of variable. This smells like a
  Hahn/Racah connection-coefficient problem and I have not found the reference.
* **The non-monotonicity in `n` is the real mystery.** Why should a level be
  bad at `n = 400` and good at `n = 700` with everything else fixed? A heuristic
  that explains the RETURN of positivity would probably also give `n*(lam)`.
* **Asymptotics of `a_0`.** In the continuum limit the root density of `q` is
  `1/(2 sqrt(r))` on `(0,1)`, and `SUM_k log(y - t_k^2) -> N * G(sqrt(y))` with
  `G(w) = (w+1)log(w+1) - (w-1)log(w-1) - 2`. The integral
  `INT_0^1 exp(N G(sqrt y)) y^{-1/2}(1-y)^{gamma-1/2} dy` is oscillatory — the
  number of negative factors is `~ N(1 - sqrt y)/2` — so its sign is decided by
  delicate cancellation. A proper steepest-descent evaluation should give the
  threshold curve. I have set this up but not carried it through.
* **Is `3 + sqrt(3)` really the constant in region A?** If the asymptotics above
  are done, this should fall out or be refuted.
* **Positive-definite functions on spheres.** By Schoenberg the whole claim reads:
  *the square of a polynomial whose roots are an arithmetic progression is
  positive definite on `S^{D-2}`, for `D` up to the shore.* Someone in that
  community may know this, or know the counterexample.

## 7. What a useful answer looks like

Any of: a proof that `q` is Gegenbauer-non-negative in region A or B; a formula
or bound for `n*(lam)`; a counterexample showing the bad set is NOT finite for
some `lam`; a literature pointer for expansions of lattice-root polynomials; or
a reason the whole approach cannot close the middle band.

Please do not re-derive section 2 — it is classical and machine-checked. The
difficulty is entirely in section 3.
