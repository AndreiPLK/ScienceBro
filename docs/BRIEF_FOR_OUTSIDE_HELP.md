# One open lemma. Everything else is done. Please look where I am not looking.

Self-contained brief. No context from our project is needed to work on this — all
definitions, formulas and data are below, and every claim marked VERIFIED was
checked in exact rational arithmetic.

---

## 1. The object, defined from scratch

Fix integers `n >= 3` and a rational `lam > 0`, and a real `D > 3`. Put

```
s   = lam + n - 1
a   runs over  n-2, n-4, n-6, ...   while positive        (so |{a}| = floor((n-1)/2))
eps = 1 if n is even, 0 if n is odd

F(u) = u^eps * prod_a ( u - (a/s)^2 )^2          for u in [0,1]
```

`F` is a polynomial of degree exactly `n-1`, and `F(u) >= 0` on `[0,1]` by
construction (a monomial times a square).

Expand `F` in the Jacobi basis on `[0,1]` with parameters

```
alpha = -1/2,     beta = D/2 - 2
```

that is, write `c_m` for the coefficient of `P_m^{(alpha,beta)}(1-2u)` in `F`.
Concretely (this is how the numbers below were produced):

```
c_m  proportional to  INT_0^1 F(u) u^alpha (1-u)^beta P_m^{(alpha,beta)}(1-2u) du
```

with a positive proportionality constant that does not depend on `m`.

Finally define the **signed coefficients**

```
C_m = (-1)^m c_m ,        m = 0, 1, ..., n-2
```

## 2. What is already known and not in question

**(a) `C_0 > 0` always, with no condition on `D`.** It is `INT F w` with `F >= 0`
and the weight positive. One line.

**(b) `C_{n-2} > 0` exactly when `D < T_n(lam)`,** where

```
T_n(lam) = 3(2n-3)/(n(n-2)) * ( lam^2 + (2n-2) lam + 1 ) + 2n
```

This is a published result of ours; we also re-derived it independently this week
by a completely different route and it matched exactly on 621 test cells.

**(c) The physical question we care about** is whether `C_m > 0` for EVERY `m`,
in the region `4 <= D <= T_hat(lam)` where `T_hat(lam) = min_{k>=3} T_k(lam)`.

VERIFIED: 525,346 individual `C_m` computed exactly across levels `n = 6..200`,
16 values of `lam` from 1/10 to 150, and 16 dimensions below the shore. **Zero
negatives.** Additional independent sweeps at `n` up to 150 also give zero.

## 3. The reduction that makes everything hinge on ONE lemma

We measured that the MINIMUM of `C_m` over `m` is always attained at an endpoint,
`m = 0` or `m = n-2`:

```
n:                    6, 8     10, 12    14 ... 60
minimum at an end:    fails     holds     holds, 0 violations in 46 configs/level
```

(the eight failures at all are at `n = 6` and `n = 8`, a finite set we can check
directly.)

If that is true in general, then by (a) and (b) **every** `C_m` is positive
whenever `D` is below the shore, and the whole infinite family collapses to two
cases, one trivial and one already published.

### THE OPEN LEMMA

> For `n >= 14`, the sequence `C_0, C_1, ..., C_{n-2}` has no interior local
> minimum. (Sufficient, and also measured: it is **log-concave**,
> `C_m^2 >= C_{m-1} C_{m+1}`, with zero violations for every `n >= 24`.)

That is the entire remaining gap.

## 4. What I already tried, so you do not repeat it

Each of these was actually run, not just considered.

1. **Real-rootedness → Newton's inequalities.** The natural mechanism for
   log-concavity. DEAD: the generating polynomial `sum_m C_m x^m` has **zero real
   roots** — all roots complex — at every level tested (`n = 14, 18, 24, 30, 40`,
   degrees 12 to 38, certified root isolation).
2. **A closed form for the ratio `r_m = C_m / C_{m-1}`.** The ratios are cleanly
   decreasing (e.g. `n=24, lam=1, D=6`: 1.909, 1.379, 1.180, 1.064, 0.981, 0.915,
   0.858, ..., 0.174, 0.118) with nearly constant differences in the tail. DEAD:
   no rational function of `m` of degree <= 3/3 fits them (fit on a subset,
   verified on held-out `m`).
3. **Log-convexity.** Wrong direction; fails everywhere.
4. **A recursion in the knife index.** `C_m` as a function of the knife index is
   not hypergeometric, and an honest search for a linear recursion of order <= 3
   with polynomial coefficients of degree <= 3 (fit on a subset, checked on
   held-out values) finds nothing.
5. **A closed product form for `C_m`.** DEAD: prime factorisation of the exact
   values shows numerator primes with 16+ digits (e.g. 5753715783362507), which a
   ratio of Gamma factors cannot produce.
6. **Term-by-term domination inside the sum defining `C_m`.** DEAD by a wide
   margin: the ratio (sum of the rest)/(first term) reaches 1e33.
7. **Creative telescoping in the summation index.** The summand involves the
   central factorial numbers, which are not hypergeometric in their index, so the
   standard algorithm does not apply in that variable.

## 5. Where I suspect I am blind — please look here

I have been attacking this as a polynomial-positivity problem. Directions I have
NOT explored, and cannot easily see from inside:

* **Total positivity.** Log-concavity of `C_m` would follow from total positivity
  of a suitable moment matrix. Is there a natural TP structure here? The measure
  `F(u) w(u) du` is positive; the coefficients are its "Jacobi-Fourier" data, not
  plain moments, which is exactly why the classical Hankel results do not apply
  directly — but perhaps a different matrix does.
* **A representation of `C_m^2 - C_{m-1} C_{m+1}` as something manifestly
  positive** — a Gram determinant, a discriminant, an integral of a square. This
  quantity is a 2x2 determinant of Jacobi coefficients of a positive measure; is
  there a known positivity theorem for that?
* **The geometry of the roots.** The roots of `F` are `(a/s)^2` with `a` running
  over an ARITHMETIC PROGRESSION. Under the substitution `u = v^2` the roots
  become the equally spaced points `a/s`, and `F` becomes the square of a
  polynomial whose roots are an arithmetic progression, i.e. essentially a
  Pochhammer/Gamma-ratio polynomial. Is there a theory of Jacobi/Gegenbauer
  expansions of squares of such "lattice node polynomials"?
* **Schoenberg's theorem.** In the variable `v`, with `gamma = D/2 - 3/2`, the
  whole claim reads: *the square of a polynomial with equally spaced real roots is
  a positive definite function on the sphere `S^{D-2}`*. That is a clean
  statement, and the community around positive definite functions on spheres may
  know it, or know a counterexample.
* **Asymptotics as the honest half.** The ratio's tail is almost exactly linear in
  `m`. An asymptotic proof for large `m` plus a finite check for small `m` might
  be easier than a uniform argument, and I have not pursued it.

## 6. Data to check anything against

For `n = 24, lam = 1, D = 6`, the exact ratios `C_m / C_{m-1}` for `m = 1..22`:

```
1.90900 1.37900 1.18000 1.06400 0.98130 0.91520 0.85820 0.80670
0.75840 0.71190 0.66640 0.62100 0.57550 0.52940 0.48240 0.43430
0.38510 0.33450 0.28250 0.22910 0.17410 0.11770
```

Everything is reproducible from the definition in section 1; if it helps, the
central factorial numbers appearing there satisfy

```
E_2t(n) = coefficient of y^t in ( prod_a (1 - a^2 y) )^2
```

with the same `a` as above, and these are explicit polynomials in `n` (the same
polynomial for even and odd `n`, which follows from Faulhaber's formulas for the
power sums plus Newton's identities).

## 7. What a useful answer looks like

Either

* a proof (or a proof sketch with the key inequality) of the lemma in section 3, or
* a counterexample — some `n >= 14` and admissible `(lam, D)` with an interior
  minimum, or
* a pointer to the literature where squares of lattice-node polynomials, or
  Jacobi coefficients of positive measures, are shown to be log-concave, or
* an argument that the lemma is false but the positivity still holds for another
  reason.

Please do not spend effort re-deriving section 2 — it is solid and machine-checked.
The whole difficulty is section 3.
