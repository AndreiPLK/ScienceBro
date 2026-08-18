# The keystone, stated exactly (2026-08-18 03:35)

Everything below is exact algebra; nothing is numerical except the verification
counts, and each of those names the run that produced it.

## Setup (all explicit)

Fix a level n >= 3, a family parameter lam > 0 and a dimension D with
3 < D < T_hat(lam). Put

    s     = lam + n - 1
    a     ranges over {n-2, n-4, ...} positive          (K = #a values)
    eps   = 1 if n is even, 0 if n is odd
    F(u)  = u^eps prod_a (u - (a/s)^2)^2  >= 0,   deg F = n - 1
    alpha = -1/2,  beta = D/2 - 2

## The statement

For every m = 0, 1, ..., n-2,

    (-1)^m INT_0^1 F(u) u^alpha (1-u)^beta P_m^{(alpha,beta)}(1-2u) du  >  0 .

Equivalently (Schoenberg, after u = v^2): the polynomial G(v)^2, where
G(v) = prod_{k=1}^{n-1} (v - (n-2k)/s) has EQUALLY SPACED roots, is a positive
definite function on the sphere S^{D-2}.

Equivalently again (this is what the physics asks): every knife j = 2..n of the
CHR graviton family is positive, since knife j corresponds to m = n - j and
ell = 2n - 2j.

## What is known about it

* TRUE in everything checked: 50 752 knives certified across a (n, lam, D) grid
  with zero failures (results/normal_form_certificates.json); 7 084 coefficients
  below the shore with zero non-positive; levels n = 24..80 complete.
* The equivalence itself is verified on 4 500 exact cells against an
  independently computed value, zero mismatches (results/jacobi_normal_form.json).
* m = n-2 (knife j = 2) is EXACTLY the published shore condition D < T_n(lam),
  rederived here from scratch: 621 cells plus an algebraic identity.
* m = n-3 (knife j = 3) is the published blade theorem.
* So the open part is m <= n-4.

## What makes it hard, quantitatively

* The margin is exponentially thin at the binding end: the smallest coefficient
  of a level, relative to the largest, falls from 2.3e-2 at n = 10 to 2.2e-21 at
  n = 70 (lam = 1, D = 6).
* Writing c_m as the explicit finite sum SUM_q F_q M(q,m) with M in Saalschutz
  closed form, the terms cancel to relative size up to 1e33: the first term does
  NOT dominate (worst ratio 4.0e33 at n = 30, lam = 26).
* There is no closed product form: the numerators of c_m carry primes as large
  as 2.3e11 at n = 9, while a Gamma-product would keep them bounded by the
  parameters.

## Routes already closed (do not re-walk)

single-circle contours (provably impossible at specific j); Airy / fold caustic
(no saddle coalescence); a dominant conjugate saddle pair (constant period 14.87
against measured growing spacings); factor-by-factor Gasper induction (single
squares are not positive); term domination; closed product form.

## The one live route

Ladder induction, adding factors smallest root first. Verified to work at every
step, with the admissible step given exactly by

    CEILING(H) = min over m of the smallest positive root of
                 A_m - 2 c B_m + c^2 C_m,
    A_m = INT H u^2 w P_m,  B_m = INT H u w P_m,  C_m = INT H w P_m

(agrees with 18-step bisection to 3e-6 = the bisection precision). The ladder
stays under the ceiling with margin 1 + C(lam)/n, C(1) = 3.38 confirmed to
n = 81, C(7) ~ 17. It is asymptotically tight, and the ceiling's dependence on
which H (a few percent, growing with degree) becomes comparable to that margin
around n ~ 100 -- so a degree-only step lemma cannot carry the induction, and the
proof must use the ladder's own structure.

## The single missing statement

    For the ladder roots c_t = (a_t/s)^2 taken in increasing order,
    c_{t+1} < CEILING(H_t) for every t, where H_t is the product of the first t
    factors.
