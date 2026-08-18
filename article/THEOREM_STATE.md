# STATE OF THE GRAND THEOREM -- final position of 2026-08-17

Written 2026-08-17 17:45. This document is the endpoint the founder asked for: what is
proved, what is not, exactly what would close it, and why I could not.

## 1. What is PROVED

**P1. The Beta reduction (ours).** The sign of every knife equals the sign of a
single univariate polynomial J(Q), Q = D/2 + n - j - 2, with rational
coefficients in (n, lam), obtained because the bracket's weights form a
Stieltjes moment sequence with an explicit Beta density. 6720 exact rational
checks, zero mismatches. Artifact: keystone_beta.json.

**P2. The parity fact (ours, elementary).** The leading coefficient of J in Q
has sign (-1)^(j-1). Hence ODD knives can never develop a threshold and EVEN
knives must. 324 checks, zero mismatches. Artifact: keystone_margin_law.json.

**P3. The descent step (CLASSICAL -- Matheron's montee; not ours).** Positivity
of all partial waves at D+2 implies positivity at D, uniformly in the spin.
Verified here in the explicit two-term form for our family, 120+120 exact
checks. This reduces the theorem to a STRIP OF WIDTH 2 below the shore:
everything below follows for free. Artifact: keystone_dimension_walk.json.
References: doi:10.1007/s40314-022-01912-4; arXiv:1303.6856;
doi:10.1016/j.jat.2017.03.002.

**P4. The knife ladder (ours; prior-art search still pending).**
bracket_{j+1} = averaging with the positive kernel 1/(j-t) = int_0^1 u^{j-t-1}du
plus a boundary term carrying (-1)^j. 228 exact checks. Explains P2
mechanically. Artifact: keystone_j_ladder.json.

**P5. Certificates on the strip.** Polya certificates, symbolic in lam AND in
the level n, covering: every knife j in the tested range, both parities of n,
ALL levels of that parity (tail + base with the join condition checked), all
shore branches k <= 45 (lam up to about 26.1), and the whole stretch of D below
the shore (via P3). Artifact: keystone_strip_fast.json.

**P6. Adversarial checks.** Foreign-engine (Z3) confirmation of the tightest
zone: 135 continuous cells, zero alarms. High-spin counterexample hunt with the
corrected shore: 227,040 exact checks, zero violations. Artifacts:
z3_judge_tight.json, keystone_hunt_highspin.json.

## 2. What is NOT proved

**G1. Uniformity in the knife index j.** Certificates are finite in j. Beyond
the certified range there is no argument.

**G2. lam above the last branch** (lam > about 26.1). Outside coverage; the
margin law says this is where the RELATIVE margin is thinnest (it decays like
1/lam), so it is the delicate region, not a formality.

## 3. Exactly what would close it, and what I ruled out

The remaining statement is: the integral of a polynomial that has j-1 roots
INSIDE the unit interval, against a Beta weight, is positive. Equivalently: all
real roots of J lie above Q_shore.

Ruled out, each with a signature in article/DATA_LOG.md (negatives #19-#28):
  * manifest positivity on the ray -- false for both even and odd knives;
  * total positivity / Karlin variation-diminishing -- the bound is j-1, not 1,
    because Hhat has ALL j-1 of its roots inside (0,1);
  * domination by the first terms -- off by a factor of 356;
  * any local grouping (pairs, shifted pairs, tail sums) -- the cancellation is
    global, established four independent times;
  * Polya criterion on the sphere (arXiv:1110.2437) -- requires compact support
    inside the interval, our residue vanishes nowhere;
  * Schur-type factorisation into PD factors -- single factors are not PD;
  * an exact square root of the residue in the angular variable -- does not
    exist;
  * closed form at the shore -- the value does not collapse (its numerators
    factor into large random primes);
  * classical root bounds (Cauchy, Fujiwara) -- too weak by a factor of 6;
  * "one real root" as a universal structure -- false; the count ranges 0..12.

What is therefore REQUIRED: a sharp asymptotic estimate of an OSCILLATING
integral -- the integrand changes sign j-1 times and the answer is positive only
by global cancellation -- with error control better than the measured margin,
which is one percent in the tightest cells. Two techniques are candidates:
Riemann-Hilbert / Deift-Zhou steepest descent for oscillatory integrals with
moving saddles, or a representation-theoretic identity that exhibits the bracket
as a norm.

**Why I could not do it.** Every method I applied is either local (and the
cancellation here is global) or asymptotic with an uncontrolled remainder. The
two independent routes I pushed furthest -- deriving the margin constant
analytically, and the knife-ladder inequality -- hit the identical wall, and the
second turned out to be logically equivalent to the theorem itself. I can
certify any finite region and I cannot produce the uniform estimate.

## 4. Honest bottom line

The theorem is NOT proved, and I do not claim it is undecidable -- only that it
needs an asymptotic technique this programme has not brought to bear. What
exists is a complete reduction (four parameters down to one polynomial, then to
a strip of width 2), three exact ladders, a proved parity law, machine
certificates over a large finite region, and adversarial checks that found
nothing. Every claim above points at an artifact regenerated from a clean tree.

## 2026-08-17 22:55 -- current best statement of the keystone

EQUIVALENT FORM (machine-verified, 4500 sign checks against the independently
computed exact value, 0 mismatches):

    Let s = lam + n - 1, a running over {n-2, n-4, ...} positive, eps = n mod 2
    complemented (1 for even n, 0 for odd n), and

        F(u) = u^eps prod_a (u - (a/s)^2)^2    >= 0,   deg F = n - 1.

    Then for every knife j, with m = n - j,

        sign(knife j) = (-1)^m x sign of the m-th coefficient of F in the
                        Jacobi basis P_m^{(D/2-2, -1/2)}(1-2u).

    Since j runs 2..n, m runs over every index 0..n-2, so:

    THE GRAND THEOREM IS EQUIVALENT TO: F has an all-positive expansion in
    P_m^{(D/2-2, -1/2)}(1-2u) up to sign (-1)^m.

EVIDENCE: 7084 coefficients strictly below the shore, zero non-positive;
additionally n = 24..60 at lam = 1, 7 and D = 6, 11, all m, zero non-positive.

STATUS: reformulation VERIFIED, theorem UNPROVED. Known obstacles: the
factor-by-factor induction is impossible (single squares fail), and the
controlling quantity appears to be how close the largest double root sits to
u = 1, with an n-dependent threshold that has not been derived.

## 2026-08-17 23:34 -- the step lemma has a classical shape: the ceiling IS a Jacobi zero

The induction runs smallest-root-first (verified: every partial product is
all-positive at every step, while largest-first fails until enough factors
accumulate). Measuring the admissible step by exact bisection, 18 iterations:

    t (factors in place)   ceiling            largest zero of P_k^{(-1/2, D/2-2)}
     3                     0.8213234          0.8455426  (k=4)
     4                     0.8590775          0.8455426  (k=4)
     5                     0.8836708          0.8928346  (k=5)
     6                     0.9003677          0.8928346  (k=5)
     7                     0.9166565          0.9214753  (k=6)
     8                     0.9260788          0.9214753  (k=6)
     9                     0.9356689          0.9400622  (k=7)
    10                     0.9439964          0.9400622  (k=7)
    11                     0.9508476          0.9527821  (k=8)

EXACT INTERLACING over eight consecutive k: the largest zero of P_k lies between
ceiling(2k-5) and ceiling(2k-4). So the threshold is not an arbitrary curve -- it
is (bracketed by) the largest zero of a Jacobi polynomial of degree k ~ t/2 + 5/2,
and those zeros have classical bounds.

ASYMPTOTIC CHECK, and it is a PREDICTION that came out right:
  * measured 1 - u_max(k) = 2.051 k^(-1.824) over k = 4..21 (classical limit -2);
  * hence the ceiling gap at step t is about 7.2 t^(-1.82);
  * the ladder's top gap is 1 - ((n-2)/(lam+n-1))^2 ~ 4/n at lam = 1, and
    t_max ~ n/2, so the ladder gap ~ 2/t;
  * ratio ladder/ceiling ~ 0.28 t^0.82, which at n = 31 (t_max = 15) predicts a
    margin of 2.5x. MEASURED: 0.125 against 0.049, i.e. 2.5x.

So the margin does not close as the level grows -- it GROWS like n^0.82. That is
consistent with the direct checks at n = 60 and n = 80 finding no negative
coefficient.

WHAT REMAINS TO PROVE: exactly one statement -- why the admissible step is that
Jacobi zero. Everything else in the chain is either verified exactly or classical.
This is the smallest the keystone has ever been, and it is the first form of it
that is a candidate for Lean.

## 2026-08-17 23:41 -- CORRECTION: the Jacobi-zero identification of the ceiling is NOT a law

Checked the index relation k ~ (t+5)/2 at other D. It holds 7 of 9 steps at
D = 6 (where I found it) but only 4/9 at D = 4, 4/9 at D = 11 and 2/9 at D = 26:
the matching index grows with D. Worse, "the ceiling is near some Jacobi zero" is
close to vacuous, since every value in (0,1) has a nearest zero. So:

* WITHDRAWN: the statement that the ceiling IS (bracketed by) the largest zero of
  P_k with k ~ t/2 + 5/2. It was a D = 6 coincidence, and I should have varied D
  before writing it down. The consequence -- the asymptotic margin estimate
  ~ t^0.82 built on the classical zero asymptotics -- loses its support too, and
  the fact that its number matched the measured 2.5x at n = 31 does not rescue it:
  a right number from a wrong mechanism is still wrong.
* STANDS, because it is derived rather than fitted: the ceiling is exactly
      min over m of the smallest positive root of A_m - 2 c B_m + c^2 C_m,
  agreeing with 18-step bisection to 3e-6 = the bisection precision, and the
  binding index is low (m ~ t/2 + 3/2 at D = 6, also to be re-checked in D).
* STANDS: the direct measurements. Margin 2.5x at n = 31 (0.125 against 0.049);
  no negative coefficient at n = 24..80; 7084 coefficients below the shore clean;
  the growing certificate grid clean.

The honest way to ask the asymptotic question is to measure the margin of the
CLOSED FORM against the ladder as n grows, with no intermediate identification.
That is the next measurement.

## 2026-08-17 23:54 -- the induction is asymptotically TIGHT, and that is the real difficulty

Direct measurement, no intermediate identification (results/step_lemma.json):

    worst margin ceiling/ladder over all steps
    n:        11      15      21      31      41
    lam=1:   1.324   1.231   1.163   1.109   1.082
    lam=7:     -     2.371   1.898   1.566   1.414

The margin SHRINKS with the level. I wrote the opposite an hour ago, having only
measured at one n; that claim is withdrawn. The law is

    margin  ~  1 + C(lam)/n,   C(1) ~ 3.4,  C(7) ~ 17

since n(margin-1) = 3.56, 3.47, 3.42, 3.38, 3.36 for lam = 1 and 18.9, 17.5,
17.0 for lam = 7. C stays positive, so the inequality holds at every level
tested, but it is asymptotically tight rather than comfortable.

Note on interpretation: the partial products are scaffolding, not physics. Only
the full product is the physical object. If the margin ever crossed 1, the
INDUCTION would die, not the theorem.

HOW MUCH DOES THE CEILING DEPEND ON WHICH H? Little. At fixed degree, four
different ladders and a deliberately different geometric root set give c_max
within 0.7 to 4.5 percent of each other (spread grows with degree: 0.0075 at
t = 3 to 0.0269 at t = 6, D = 6). So a lemma stated in terms of (degree, beta)
alone is close to true.

AND HERE IS THE OBSTACLE, as arithmetic rather than intuition: the H-dependence
spread (a few percent, growing with degree) becomes comparable to the margin
(3.4/n) at around n ~ 100. A degree-only step lemma therefore cannot carry the
induction to arbitrary n; the proof has to use the ladder's own structure. That
is a precise statement of what makes this theorem hard, and it is the first time
the difficulty has been quantified rather than described.

## 2026-08-17 23:58 -- the crux is ONE inequality, and the assembly order is a red herring

Tested five assembly strategies on the same ladder (n = 15, 21, 31, lam = 1,
D = 6), measuring the worst margin over the whole assembly:

    smallest first (baseline)   1.231   1.163   1.109
    smallest first, in PAIRS    1.231   1.170   1.109
    middle out                  1.231   1.163   1.109
    largest first               fails
    alternating small/large     0.866 / fails

Every viable order gives the SAME worst margin, and in every case the worst step
is the LAST one (t = 9 at n = 21, t = 14 at n = 31, t = 19 at n = 41). So the
tightness is not an artefact of how the induction is organised, and no reordering
buys margin.

CONSEQUENCE -- the keystone is now one inequality about the physical object:

    (a_max/s)^2  <  CEILING( F divided by its last factor ),
    a_max = n-2,  s = lam + n - 1,

where CEILING is the explicit min-over-m smallest positive root of
A_m - 2 c B_m + c^2 C_m. The measured margin is 1 + C(lam)/n with C(1) ~ 3.4 and
C(7) ~ 17, i.e. true at every level tested and asymptotically tight.

This is the smallest the problem has ever been: everything else in the chain is
verified exactly or classical, the scaffolding is provably order-independent, and
what is left is a single explicit inequality with a measured margin law.

## 2026-08-18 00:04 -- WHICH knife holds the boundary: spin 2, exponentially tightly

Exact rational computation over every knife of every level n = 10..70 at
lam = 1, 7 and D = 6, 11 (`article/visuals/the_weakest_knife.py`):

* the weakest constraint is ALWAYS m = n-2, i.e. the LOWEST SPIN j = 2 -- at
  every level and every (lam, D) tested, without exception;
* its size relative to the largest coefficient of the same level falls
  exponentially in n: 2.3e-2 (n=10), 1.7e-3 (14), 2.6e-5 (20), 3.6e-7 (26),
  1.1e-9 (34), 6.5e-13 (44), 8.4e-17 (56), 2.2e-21 (70) at lam = 1, D = 6;
* the rate is about 0.33 decades per unit n and DRIFTS: upward for lam = 1
  (0.286 -> 0.327) and downward for lam = 7 (0.412 -> 0.364), both heading toward
  roughly 0.33-0.36. A straight line in n leaves 0.18 dex of residual, a
  quadratic 0.05 -- so it is exponential with a slowly moving rate, not a clean
  exponential. Recorded as measured behaviour, not as a law.

CONSEQUENCE FOR THE PROOF. The margin the theorem holds by, at low spin, is
exponentially small in the level. So no crude bound can prove it: any argument
has to track an exponentially small quantity exactly. That is a concrete
explanation of the difficulty, replacing the earlier hand-waving.

CONSEQUENCE FOR THE PHYSICS. This family of graviton amplitudes sits
exponentially close to the spin-2 positivity boundary as the level grows. The
binding constraint of the whole family is the lowest spin, which is also
consistent with the earlier finding that low-spin dominance FAILS here.

Margin trend continues to hold up: at n = 51, worst margin 1.06637, so
n(margin-1) = 3.385 -- against 3.36 at n = 41 and 3.38 at n = 31. The constant is
stable near 3.36-3.39 rather than drifting to zero, so the induction's inequality
is not about to fail.

## 2026-08-18 03:33 -- two more routes closed, and a map of what is left

With the Saalschutz closed form the m-th coefficient is an explicit finite sum
c_m = SUM_{q=m}^{n-1} F_q M(q,m). Two natural shortcuts were tested and both fail.

1. TERM DOMINATION. Does the first term (q = m) exceed the rest, so that the sign
   is decided term by term? NO, and not marginally: sum|rest| / |first| reaches
   3.1e3 at n = 9 (lam = 1, D = 6), 1.5e10 at n = 21, 4.0e33 at n = 30 with
   lam = 26. The worst index is m = 0 or 1. Positivity therefore rests on a
   delicate cancellation between huge alternating terms -- exactly the
   exponential thinness measured earlier, now seen at the level of the summands.

2. CLOSED PRODUCT FORM. If c_m were a product of Gamma factors, its numerator
   would only contain primes bounded by the parameters. Factored exactly: the
   denominators are smooth (largest prime <= 4n, as Pochhammers must be) but the
   numerators are not -- 2.3e11 at n = 9, 6.3e13 at n = 12 lam = 7, 3.5e12 at
   n = 14. So there is NO closed product form for general m. The exceptions are
   the last indices, m = n-2 and n-3, where the sum has two or three terms; that
   is precisely the case already exploited to rederive the shore.

CONSEQUENCE: the theorem cannot come from an identity. It needs an inequality
argument that survives cancellation of relative size 1e33.

MAP OF ROUTES TRIED THIS NIGHT (all conclusions from our own data):
  * per-knife contour certificates -- works but does not scale, and part of the
    failure structure was the instrument (radius searched outside the admissible
    window; argument principle fixes that);
  * single-circle contour -- provably impossible for specific j (conjugate root
    pair at equal modulus), deformed loops rescue some of those (j = 55, 58);
  * Airy / fold caustic -- no saddle coalescence anywhere, dropped;
  * conjugate saddle pair -- gives a constant period 14.87 against measured
    growing spacings, dropped;
  * factor-by-factor (Gasper-style) induction -- single squares are not positive,
    dropped;
  * ladder induction smallest-first -- works at every step, but asymptotically
    tight (margin 1 + 3.38/n, confirmed to n = 81) and the degree-only version
    runs out of room near n ~ 100;
  * term domination -- fails by up to 33 orders;
  * closed product form -- excluded by prime factorisation.

WHAT IS LEFT, precisely: a bound on the alternating sum c_m that keeps the
(-1)^m sign, valid for all m, using the ladder structure of the roots
u_a = (a/s)^2 with a in {n-2, n-4, ...}. Every ingredient is now explicit and
exact; nothing in the chain is numerical any more except the verification.

## 2026-08-18 04:09 -- AN EXPLICIT CLOSED FORM FOR EVERY KNIFE, and the fourth knife measured

The Saalschutz moments turn each knife into a finite sum, and the ratios of
consecutive moments collapse to elementary products. Writing m = n - j, dividing
by the (positive) t = 0 term and verifying every step against the exact engine:

    knife j > 0   <=>   SUM_{t=0}^{j-1} (-1)^t E_2t(n) / s^(2t) * R_t  >  0

    R_t = [prod_{i=1..t} (j-i)] [prod_{i=1..t} (D + 4n - 2j - 5 - 2(i-1))]
          / ( [prod_{i=1..t} (n-i)] [prod_{i=1..t} (2n - 1 - 2i)] ),   R_0 = 1

with the central factorial numbers now explicit polynomials, each verified on
BOTH parities for n up to 59:

    E_2 = n(n-1)(n-2)/3
    E_4 = n(n-1)(n-2)(5n^3 - 24n^2 + 28n + 12)/90
    E_6 = n(n-1)(n-2)(n-3)(n-4)(35n^4 - 154n^3 + 172n^2 + 292n + 120)/5670

VERIFICATION: the closed form's sign agrees with the exact engine on 24 cells for
each of j = 2, 3, 4 (n from j+3 to j+18, lam = 1 and 7, D = 6, 11, 23), zero
disagreements. Two off-by-one slips in my own derivation of R_t were caught by
exactly this check before anything was concluded from them.

## The fourth knife

Clearing positive denominators gives P4(n, D, lam), degree 9 in n, 3 in D, 6 in
lam, whose positivity IS the fourth knife. Exact evaluation on 1736 cells below
the shore: zero failures.

Since P4 is cubic in D with a negative leading coefficient, there is a critical
D*(n, lam) where the knife vanishes, and the theorem to prove is D* > T_hat(lam).
Measured (minimum of D* over n = 5..120):

    lam      1/4     1/2       1       2       3       5       7      14      26      60
    D*/shore 1.316  1.252   1.220   1.163   1.142   1.116   1.062  1.0205  1.010  1.0042

So knife 4 never cuts into the allowed region in anything tested, and the margin
shrinks toward 1 as lam grows -- i.e. it appears ASYMPTOTICALLY TANGENT to the
shore, the same delicacy the published blade theorem has for knife 3.

NOTE, so the table is not over-read: the lam = 150 row (1.115) is an artefact of
capping the search at n = 120. The minimising level grows roughly like 1.7 lam
(n = 102 at lam = 60), so at lam = 150 the true minimum lies outside the range
scanned. That row should be recomputed with a wider n before it is used.

STATUS: this is an explicit, verified closed form and a measured statement, NOT a
proof. What would make it a theorem is showing D*(n, lam) > T_hat(lam) for all
n and lam -- now a finite algebraic question about one explicit polynomial,
which is exactly the shape the published blade theorem took for knife 3.

## 2026-08-18 04:26 -- knife 4 is SINGLED OUT, and it is not a trend in j

E_8(n) derived and verified on both parities to n = 54, which unlocks knife 5.
All of j = 2, 3, 4, 5 now have verified closed forms (24 cells each against the
exact flint engine, zero disagreements).

min over levels of D*, divided by the shore:

    lam         1/4    1/2      1      2      3      5      7     10     14     20     26     40     60
    knife 3    1.187  1.170  1.138  1.105  1.088  1.081  1.080  1.081  1.083  1.084  1.086  1.087  1.087
    knife 4    1.316  1.252  1.220  1.163  1.142  1.117  1.062  1.032  1.0205 1.013  1.010  1.0064 1.0042
    knife 5    1.385  1.333  1.275  1.212  1.179  1.158  1.112  1.072  1.0665 1.0655 1.0654 1.0653 1.0658

So the earlier reading -- "each further knife is tighter" -- is WRONG, and I am
glad the fifth was computed before that was written down as a trend. Knives 3 and
5 level off (near 1.087 and 1.066). Knife 4 alone keeps descending toward 1.

That is a sharper statement than a trend: the family has ONE distinguished tight
constraint, the fourth trajectory ell = 2n-8, and its neighbours on both sides
settle away from the shore. Whether knife 4 stays above the shore as lam grows is
the open question, and it is now a finite algebraic question about one explicit
polynomial P4 (degree 9 in n, 3 in D, 6 in lam).

The minimising level grows with lam roughly like 1.7 lam for knife 4 (n = 102 at
lam = 60) and like 3 lam for knife 5 (n = 179 at lam = 60); the scan range is
tied to lam and reported per point, after an earlier fixed cap at n = 120
produced a spurious upturn.
