# The keystone, stated exactly (rewritten 2026-08-18 16:30)

Everything below is exact algebra; nothing is numerical except the verification
counts, and each of those names the run that produced it. **Read this before
starting any new attempt** — sections 4 and 5 list what is already closed.

## 1. Setup (all explicit)

Fix a level `n >= 3`, a family parameter `lam > 0`, a dimension `D` with
`3 < D < T_hat(lam)`. Put

    N     = n - 1
    s     = lam + n - 1
    q(v)  = prod_{k=0}^{N-1} ( v - (N-1-2k)/s )        roots: an arithmetic progression
    F(u)  = q(v)^2  with u = v^2                       so F >= 0 by construction
    gamma = D/2 - 3/2
    T_hat(lam) = min_{k>=3} [ 3(2k-3)/(k(k-2)) (lam^2 + (2k-2) lam + 1) + 2k ]
    gamma_shore(lam) = (T_hat(lam) - 3)/2

## 2. The statement, in its best available form

> **Are all Gegenbauer coefficients of `q` non-negative at `gamma_shore(lam)`?**

That single question implies the whole physics claim, by three classical steps:

1. the quadratic transformation `C_{2m}^g(v) = ((g)_m/(1/2)_m) P_m^{(g-1/2,-1/2)}(2v^2-1)`
   with `P_m^{(a,b)}(-z) = (-1)^m P_m^{(b,a)}(z)` makes knife `m` EQUAL to the
   Gegenbauer coefficient of `F` at index `2m`, up to a positive constant
   (verified against the exact knife engine: 264 comparisons, 0 disagreements);
2. Dougall: linearization coefficients of Gegenbauer are non-negative for
   `gamma > 0`, so non-negative coefficients for `q` give non-negative
   coefficients for `q^2`;
3. DLMF 18.18.16 carries non-negativity down from the shore to every smaller
   `gamma`, i.e. to every dimension the family is allowed.

Only step 2's hypothesis is open. Everything else is classical and machine-checked.

## 3. What is settled

**Region A — small levels, large lam.** Clean for `lam >= lam*(n)`, and

    lam*(n)/n  ->  4.730616445749...   (NOT 3 + sqrt(3) = 4.732050807569)

Measured exactly: n = 100, 200 (0 mod 4) give 4.727823299, 4.729216596; n = 102,
202 (2 mod 4) give 4.718153761, 4.724319880. The distance to the limit halves as
n doubles, so the correction is `A/n`; Richardson per parity class gives 4.730611
and 4.730610. The constant was predicted by the outside analysis from a Stokes
balance BEFORE this test. `3 + sqrt(3)` is refuted, at 250x the residual.

**Region B — large levels, small lam.** Clean for `n >= n*(lam)`. Exact
thresholds, each bisected to a single level with both sides recorded:

    lam   1/40  1/20  1/16  1/10  1/8   1/6   1/5   1/4
    n*    454   516   550   660   744   906   1056  1322

The coarse model `n* ~ exp(2 gamma_shore/(lam+1))` overshoots by +3.1, +5.6,
+10.1, +12.7, +17.7 percent at lam = 1/40, 1/16, 1/8, 1/6, 1/4 — smooth and
monotone in lam, not noise.

**No reopening observed.** At lam = 1/20 (n* = 516) every coefficient is
non-negative at n = 600, 800, 1100, 1500, 1900 — out to 3.68x the threshold.
Also clean at (1/10, 700..1200) and (1/5, 1400).

## 4. The remaining gap, stated narrowly

> Prove that no coefficient goes negative for `m` above the edge zone, up to
> `m = N` — uniformly, not for each fixed `m`.

Localisation measured at the shore: the largest negative index divided by N falls
to 0.053, 0.101, 0.171 at N = 1599 for lam = 1/2, 1, 2. So the offenders live at
the low end and the bulk shows no sign of offending — evidence, not proof.

The outside analysis reduces this to a ONE-dimensional Hankel integral, all index
dependence sitting in a single factor `exp[-tau/(L - log t)]` with
`tau = (m+gamma)^2/s` and `L = log N`. That is the live route.

**Do NOT claim** that the bad band being finite means certificates cover it: the
endpoint model allows `n*` up to `exp(12 + 4 sqrt 3) ~ 1.7e8`, and no rigorous
upper bound on `n*(lam)` exists yet. Obtaining one is worth more than a sharp
asymptotic.

## 5. Closed routes — do not rewalk

1. Real-rootedness / Newton — the generating polynomial has zero real roots.
2. Closed form for the ratio `C_m/C_{m-1}` — no rational fit survives held-out data.
3. Log-convexity — wrong direction.
4. A recursion in the knife index — not hypergeometric there.
5. A closed product form — numerator primes of 16+ digits.
6. Term-by-term domination inside the sum — ratio reaches 1e33.
7. Total positivity / Karlin — 37-47 % of 2x2 minors negative.
8. Stieltjes moments — would force log-convexity.
9. Newton's inequalities on `F` itself — signs agree on 4-9 of 23 indices.
10. Creative telescoping in the summation index — central factorials not
    hypergeometric there.
11. **The endpoint-minimum lemma — FALSE** (ERR-0005, counterexample n=24,
    lam=10, D=177).
12. **Term-by-term via `(x)_N^2 = sum_j C(N,j)^2 j! (x)_{2N-j}`** — the weights
    are positive but ~45 % of the even coefficients of the individual `(x)_M` are
    negative; cancellation is essential.
13. **Block grouping under Dougall** — circular; a greedy partition puts
    everything in one block, i.e. verifies the product directly.
14. **Factor-by-factor** — `(v^2-t^2)` is clean iff `t^2 <= 1/(2(gamma+1))`,
    giving only `lam >~ 19 n^2`.
15. **Any `mu >= gamma_shore` instead of the shore itself** — the clean set in
    `mu` is the interval `(0, gamma*]` and nothing above it; checked in five band
    cells.
16. **Wilson generalized powers** — the connection structure exists (Area 2026)
    but Prop. 3.1(iii) is a SIGN OBSTRUCTION: the natural normalisation has mixed
    signs. Not a positivity route.
17. **Polya-type criteria on spheres** — all require monotonicity or convexity,
    which `q` violates by construction. Schoenberg remains a restatement, not a
    mechanism.

## 6. Errata that bear on this file

* ERR-0005 — the endpoint lemma is false; absolute grids under a moving boundary.
* ERR-0006 — "`a_{N-2}` binds from lam >= 4" is false in the regime `lam ~ c n`,
  where `a_1` (or `a_3`, by parity) binds; a boundary claim must be measured ON
  the boundary.
