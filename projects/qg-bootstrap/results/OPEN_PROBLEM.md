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


---

# Updated state of the problem (2026-08-18 04:49)

The night moved the boundary of what is open. Restating it in the sharpest form
now available.

## What is settled

* THE EQUIVALENCE. knife j > 0 iff the m-th Jacobi coefficient of an explicit
  nonnegative polynomial has sign (-1)^m, m = n - j. 4 500 exact checks, zero
  mismatches.
* CLOSED FORM PER KNIFE. knife j > 0 iff SUM_t (-1)^t E_2t(n) s^-2t R_t > 0 with
  R_t elementary and E_2t explicit polynomials (E_2 through E_10 derived and
  verified on both parities). Checked against the exact engine on 24 cells for
  each of j = 2..6, zero disagreements.
* THE SCALING LIMIT, for fixed j: the sum collapses by Newton's binomial to
  (2rho^2 + 12rho + 6 - d rho)^(j-1) / (6(rho+1)^2)^(j-1). Odd j -> even power,
  never negative. Even j -> odd power, safe exactly below d = 2rho + 12 + 6/rho,
  whose minimum is 12 + 4 sqrt(3), the shore asymptote.
* THE TANGENCY IS SAFE. On the curve the first two orders vanish (A_0 and A_1
  share the bracket) and A_2 decides; at rho = sqrt(3) it equals
  22896 sqrt(3) + 128952 > 0 for knife 4 and 1811652480 sqrt(3) + 3362078016 > 0
  for knife 6.
* THE OTHER LIMIT. At fixed (lam, D) and n -> infinity the leading coefficient is
  a positive constant (20, 280, 2800, 12320 for j = 3..6).
* COVERAGE. Over 115 000 knives certified exactly with zero failures, levels up
  to n = 150.

## What is open, exactly

Write the knife-4 polynomial in scaling variables:

    P4(rho lam, d lam, lam) = SUM_{k=0}^{9} lam^{9-k} A_k(rho, d)

with all ten A_k explicit. The finite-lam theorem for knife 4 is:

    for every rho > 0 and every d <= 12 + 4 sqrt(3),
    SUM_k lam^{-k} A_k(rho, d) > 0  for all lam above an explicit lam_0.

Away from the curve A_0 dominates; near it A_0 and A_1 vanish and A_2 > 0 takes
over. So the proof is a bound on the remaining A_k over a compact region -- a
concrete finite computation rather than a search for a method.

The generic Cauchy bound is NOT good enough for this (it gives n_0 ~ 1e13 at
lam = 60, against a true threshold of order lam); the bound has to be written in
the scaling variables.

## For the odd knives

Nothing is open at leading order: the even power makes them non-negative for all
d. What is open is the same subleading question at the curve, where they touch
zero.

## 2026-08-18 10:11 -- KNIFE 4 PROVED on a compact region (machine proof, not a scan)

Method: exact Bernstein subdivision. On each box the polynomial is re-expanded in
the Bernstein basis with rational arithmetic; the minimum of those coefficients is
a rigorous lower bound by the convex-hull property, and a box is accepted only
when it is strictly positive, otherwise split. Subdivision tightens the bound
quadratically, so the recursion terminates when the statement is true with margin.

PROVED (no open boxes anywhere):

    lam in [1/10, 1],  4 <= n <= 200,  4 <= D <= shore(lam):     47 boxes
    lam in [1, 10],    4 <= n <=  50,  4 <= D <= shore(lam):  1 325 boxes
    lam in [1, 30],    4 <= n <= 200,  4 <= D <= shore(lam): 12 929 boxes

so knife 4 is proved for lam in [1/10, 30], n up to 200, D up to the shore.

The shore bound is exact per box: T_hat <= T_k for every k and each T_k increases
in lam, so min_k T_k(lam_hi) is a rational majorant valid on the whole box.

TWO WRONG METHODS, recorded rather than deleted:
* naive per-monomial interval arithmetic -- the dependency problem makes the
  enclosure useless here (103 monomials, heavy cancellation); it never closed a
  single region;
* "all coefficients non-negative after shifting to the corner" -- far too strong
  a test, it failed even on tiny boxes where the polynomial is obviously positive.
  The correct crude bound is c_0 plus the sum of negative coefficients; Bernstein
  is sharper still and closed n in [4,12], D in [4,24], lam in [1,2] in ONE box.

AND ONE WRONG DOMAIN: the first Bernstein run left 739 boxes open, all of them in
a slab ABOVE the shore (D = 191 at lam = 10, where the shore is 187.5), because I
had used the crude majorant 18.93 lam + 5. With the exact per-box shore bound the
same region closes completely. Third time this night that a wrong domain produced
a fake problem.

WHAT REMAINS for knife 4: lam > 30 and n > 200. Runs are in progress at
(n <= 400, lam <= 60) and (n <= 1000, lam <= 120); beyond them the two asymptotic
statements take over (n -> infinity at fixed lam, D has leading coefficient +280;
lam -> infinity is the scaling form with the tangency approached from the safe
side). Joining those to the box with explicit thresholds is the last gap.

## 2026-08-18 10:40 -- E_2t DERIVED, not fitted: the weakest link in the chain is closed

Until now the central factorial polynomials were guessed from data and verified.
That was the most vulnerable point for publication -- verification is not
derivation, and it is the first thing a referee would ask about. It is now
derived from the definition:

1. The generating product is prod_{k=1}^{n-1} (1 + (n-2k) x)^2. The set
   {n-2k} is symmetric about zero, so in y = x^2 it is prod_{a>0} (1-a^2 y)^2
   with a = n-2, n-4, ... (verified directly against the integer sequence at
   n = 7, 8, 11, 12).
2. The power sums p_r = SUM_a a^{2r} have Faulhaber closed forms, and -- this is
   the structural point -- the odd-n and even-n formulas are THE SAME polynomial
   in n (checked for r = 1, 2, 3). That is why E_2t never depended on parity, a
   fact previously only observed.
3. Newton's identities turn the p_r into the elementary symmetric functions s_r.
4. E_2t is then a coefficient of (SUM_r (-1)^r s_r y^r)^2.

Carried out to t = 6, giving E_2, E_4, E_6, E_8, E_10 and the new E_12, each
verified against the exact integer sequence on both parities for n up to 39:
ZERO mismatches. E_12 also unlocks knife 7 for the closed form.

Effect on the programme: the chain from the CHR family to the knife condition is
now a derivation end to end -- Beta reduction, Jacobi normal form (4500 checks),
Saalschutz moments (432 checks), the moment recursion R_t (verified per knife),
and now E_2t. Nothing in it is fitted.

## 2026-08-18 11:00 -- the uniform-in-j route via a recursion is CLOSED, and a fake fit caught

The founder's point, and he is right: finishing knives one at a time is the trap
we already named, and the real target is a statement uniform in j. The natural
handle would be a linear recursion in j -- then positivity for all j follows by
induction from the first cases. Tested and it does not exist in usable form.

* K_j / K_{j-1} is NOT a rational function of j (no low-degree fit at three
  different (n, lam, D)), so the sequence is not hypergeometric and there is no
  first-order recursion.
* An honest search for sum_r c_r(j) K_{j+r} = 0 with order <= 3 and coefficient
  degree <= 3, fitted on a subset and VERIFIED ON HELD-OUT j: nothing survives.

NEAR-MISS WORTH RECORDING. The first search reported a recursion of order 4 with
degree-4 coefficients, "verified on j = 2..21". It was an artefact: 25 unknowns
against 21 equations, i.e. underdetermined, so the solver fitted all the data and
the verification was circular. The tell was the size of the coefficients
(hundreds of digits) -- a structural recursion does not look like that. The fix
is the standard one and is now the rule: fewer unknowns than fitting equations,
and always verify on held-out values.

WHERE THAT LEAVES THE UNIFORM PROBLEM. The scaling limit gives the mechanism for
every j at once, but only at leading order and at fixed j. A recursion in j is
now excluded at low order. What is left to try: creative telescoping in the
variable (t, j) at higher order, a generating function in j, or an argument
that bounds the whole family by the two extreme knives rather than treating them
separately.


## 2026-08-18 11:08 -- three routes to the UNIFORM theorem tried today, all closed

The founder's instruction was to put the weight on the uniform-in-j statement
rather than finishing knives one at a time. Three natural handles were tried.

1. HYPERGEOMETRIC IN j. K_j/K_(j-1) is not a rational function of j (no
   low-degree fit at three different (n, lam, D)). No first-order recursion.
2. HIGHER-ORDER RECURSION IN j. An honest search (order <= 3, coefficient degree
   <= 3, fitted on a subset and verified on held-out j) finds nothing. A first
   attempt appeared to succeed at order 4, but it had 25 unknowns against 21
   equations -- underdetermined, so the "verification" was on the fitting data
   itself. Recorded as a near-miss; the tell was coefficients hundreds of digits
   long.
3. POLYNOMIALITY IN j ABOVE THE TRUNCATION. The t-sum is cut at min(j-1, K), so
   above K the knife should be a plain polynomial in j and the whole tail of the
   family would follow from one polynomial positivity. It fails for a simple
   reason: K is the DEGREE of G2, which is n-1, not the number of roots (about
   n/2). "Above the truncation" therefore means j >= n, a single knife. I had
   conflated the root count with the degree of the square.

WHAT THIS LEAVES. The uniform statement needs an idea that is not a recursion and
not a term-by-term bound. The candidates that remain untried:
  * creative telescoping in BOTH indices (t, j) at higher order, with proper
    software rather than an ansatz;
  * a generating function in j for the whole family;
  * bounding the family by its two extreme knives, using that the binding one is
    always at an end of the spectrum (measured, article/visuals/which-end-binds.png);
  * a positivity argument for the Jacobi expansion of a product of squares with
    prescribed root spacing, i.e. attacking the Schoenberg form directly rather
    than knife by knife.

The last one is the most promising: it is the only formulation in which "all j"
is a single statement rather than a family of them.
