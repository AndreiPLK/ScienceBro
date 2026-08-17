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
