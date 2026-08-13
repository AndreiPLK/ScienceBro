# The left edge of the island: a_{n,n-1} in closed form (mu0=0, D=4, q=1)

Date: 2026-08-13. Status: analytic derivation below, numerically verified in exact
arithmetic at 66 points (6 targeted predictions incl. two exact zeros at off-grid
points + 60 random (n,r,w)). Independent review: domain-critic pass DONE
2026-08-13 (left-edge-theorem-review.md) — no algebraic error found in claims 1-3;
its adversarial script executed same day: 6/6 attacks survived, exit 0 (includes
route1-vs-route2 cross-validation at mu0 != 0, closing gap E1, and the
below-threshold sanity check). Review fixes E2-E4 and wording applied below.

DOMAIN (E3, binding for every sign statement in this note): 2+r > 0 and
1+r+w > 0; the poles 1+r = 0 and 1+r+w = 0 are excluded. Outside this domain
the prefactor (1+n+r+w)/((2+r)_n (1+r+w)) can flip sign and the raw bracket
laws do not apply (the full sign law with prefactor was checked separately).
EDGE CASE (E2): at n = 3*mu0 exactly, alpha = 0 and a_{n,n-1} vanishes
identically; the sign law is stated for n > 3*mu0.

## Claim

For the (r,w) deformation family of arXiv:2406.02665 at q=1, mu0=0, D=4, the
next-to-leading Regge partial-wave coefficient satisfies

    a_{n,n-1} = K(n) * (n(r+1/2) + w) * (1+n+r+w) / ((2+r)_n (1+r+w)),

with K(n) > 0 depending only on n. In the physical normalization domain
(2+r > 0, 1+r+w > 0, so both extra factors are positive for n >= 1):

    sign(a_{n,n-1}) = sign( n(r+1/2) + w ).

## Derivation

Level-n residue (q->1 of Eq. 16, the exact form used and two-route-validated in
repro_r4_positivity_spot.py):

    R(n,t) = (2+r+t)_{n-1} * (1+r+t+w)(1+n+r+w) / ((2+r)_n (1+r+w)),

a polynomial of degree n in t with roots t = -(2+r+k), k=0..n-2 and t = -(1+r+w).
Monic part: p(t) = t^n + A t^{n-1} + ..., where A = minus the sum of roots:

    A = (n-1)(2+r) + (n-1)(n-2)/2 + (1+r+w).

Scattering angle substitution at mu0=0: t = (n/2)(x-1). Then

    coeff of x^n     : (n/2)^n
    coeff of x^{n-1} : (n/2)^{n-1} [A - n^2/2]     (from t^n's -n x^{n-1} term
                                                    plus A t^{n-1}'s x^{n-1} term)

and, simplifying,

    A - n^2/2 = (n-1)(2+r) + (n^2-3n+2)/2 + 1+r+w - n^2/2 = n(r+1/2) + w.

Legendre projection (D=4): b_{n-1} = (2n-1)/2 * Int_{-1}^{1} P_{n-1}(x) poly(x) dx.
By parity and degree, only the x^{n-1} monomial contributes: x^n has parity n and
projects onto P_n, P_{n-2}, ...; monomials x^{n-3}, x^{n-5}, ... of parity n-1
have degree < n-1 and are orthogonal to P_{n-1}. Since
Int P_{n-1} x^{n-1} dx = 2^n ((n-1)!)^2 / (2n-1)! > 0, we get
K(n) = (2n-1)/2 * (n/2)^{n-1} * 2^n ((n-1)!)^2/(2n-1)! > 0.  QED (elementary).

## Numerical verification (exact rational, validated two-route evaluator)

- (r,w)=(-3/5,1): a_{10,9} = 0 exactly; a_{11,10} < 0. Matches map data (first
  negative [11,10]).
- Off-grid razor test (r,w)=(-13/25,1/2), never scanned before: predicted zero at
  n = w/|r+1/2| = 25. Measured: a_{24,23} > 0, a_{25,24} = 0 exactly, a_{26,25} < 0.
- (r,w)=(-2/5,1), n=50: positive (r > -1/2 safe on this trajectory). Confirmed.
- 60 random (n<=25, r in (-0.9,1.5), w in (-1.5,1.8)): full sign law (including
  the prefactor sign flip when 1+r+w < 0) holds in all cases.

## Corollaries

1. **All nine casualties explained.** At r = -3/5 (r+1/2 = -1/10), positivity on
   the (n, n-1) trajectory fails first at n = 10w+1 — exactly the measured kill
   list (w=1 -> [11,10] ... w=9/5 -> [19,18]), and exactly why these cells
   survived N=10 but died at N=20 (n_crit in 11..19), with no casualties after.
2. **Exclusion edge at mu0=0: nothing survives left of r = -1/2** (for w > 0):
   every point with r < -1/2 is excluded at depth n > w/|r+1/2|. (That the edge
   is attained — allowed points exist arbitrarily close to it — is empirical,
   from the scans, not proven here.) Finite-depth maps overstate
   the island in the sliver r in (-0.6, -0.5); erosion is slow (depth ~ 1/dist)
   but total. At r = -1/2 the coefficient equals w * (positive) >= 0: marginal,
   never negative — the edge itself survives all depths on this trajectory.
3. **Practical**: fine-grid scans at fixed NMAX must be post-processed with this
   rule on the left edge; a cell at r = -1/2 - eps apparently "allowed" at
   NMAX=20 is doomed iff w > 20*eps.

## Generalization to arbitrary mu0 (added same day, verified)

With the shifted substitution t' = alpha x + beta, alpha = (n-3mu0)/2,
beta = -alpha - mu0, the x^{n-1} coefficient becomes alpha^{n-1}(A + n*beta), and

    A + n*beta = n(r + (1+mu0)/2) + w.

So for n > 3mu0 (alpha > 0, which holds above threshold):

    sign(a_{n,n-1}) = sign( n(r + (1+mu0)/2) + w )   [same positive prefactor domain]

**The island's left edge at spectrum shift mu0 is r = -(1+mu0)/2.**
Razor tests passed (exact zeros at predicted (n, mu0) off-grid points):
mu0=3/5, (r,w)=(-82/100, 2/5): a_{19,18}>0, a_{20,19}=0, a_{21,20}<0.
mu0=-3/5, (r,w)=(-1/4, 3/4): a_{14,13}>0, a_{15,14}=0, a_{16,15}<0.
Prediction for the mu0 stack maps: left edges at -(1+mu0)/2 = -0.2 (mu0=-3/5),
-0.5 (mu0=0), -0.8 (mu0=3/5), etc. — to be checked against the N=10 stack with
the finite-depth caveat (cells die only at n > w/|r-edge| <= NMAX).

## Third trajectory a_{n,n-2} (mu0=0) — closed form

Same technique, two contributing monomials (x^n and x^{n-2} both project on
P_{n-2}). With rho = I(n,n-2)/I(n-2,n-2) = n(n-1)/(2(2n-1)):

    sign(a_{n,n-2}) = sign[ 12(2n-1)(1+r)(nr+2w) + n(n^2+5n-2) ]

(physical domain; constant C(n) = 24(2n-1)/(n-1) > 0 — the reviewer's re-derivation
proved the identity for ALL n via exact polynomial-degree argument, upgrading the
original n=3..8 brute-force check to a theorem; see left-edge-theorem-review.md).
Consequence: the cubic-in-n term dominates, so a_{n,n-2} is eventually positive
for every fixed (r,w) — the third trajectory only kills in a finite n-window.

## Killer census and CONJECTURED complete characterization (mu0=0)

Census of first-negative (n,l) over all 714 excluded cells of the N=40 map:
every killer is either (i) a constraint with n <= 5, or (ii) the l=n-1 ladder
(n=4..19), or (iii) a domain pole. No other constraint binds anywhere.

Conjectured complete characterization of the island at mu0=0:

    allowed(r,w)  <=>  all a_{n,l} >= 0 for n <= 5  (20 explicit curves, e.g.
                       a_{2,0}: 3(1+r)(r+w)+1 >= 0,
                       a_{3,0}: 4r^3+4r^2w+6r^2+8rw+8r+6w+3 >= 0)
                       AND the ladder condition: not(r < -1/2 and w > 0),
                       within the domain defined above. (E4 resolved: the former
                       extra clause "not(r=-1/2 and w<0)" is redundant — at
                       r=-1/2 the n=1 block already kills all w<0: a_{1,0} ~ w
                       for -1/2<w<0 and a_{1,1} flips via the prefactor for
                       w<-1/2; verified exactly at 6 sample points.)

Verified: 1369/1369 coarse cells (N=40 scan, boundary stable to N=80) and
2411/2411 fine boundary points (N=20 scan + theorem correction) — zero
mismatches on 3780 exact points. Status: conjecturally complete (killers with
l <= n-2, n > 5 assumed non-binding — proven only empirically to depth 80);
the l=n-1 part is analytic for all n.

## Open

- Prove non-binding of l <= n-2, n > n_min+4 killers (close the conjecture).
- General-D (Gegenbauer) version of all three closed forms.
- (done 2026-08-13) Mansfield-Spradlin w=0 cross-check — see section below, PASSED.

## Full mu0 stack: threshold structure and stack-wide characterization

Killer census for mu0>0 maps: the dominant constraints sit at the FIRST
above-threshold level n_min = min{n : n >= 3*mu0} (mu0=3/5 -> (2,l); 6/5 ->
(4,l); 9/5 -> (6,l)), mostly the scalar l=0: at threshold the residue
polynomial degenerates (alpha = (n-3mu0)/2 -> 0) toward pure l=0. Symbolic
threshold curve derived, e.g. a_{2,0}(r,w,mu0) ~ 6mu0^2+6mu0 r+3mu0 w-3mu0
+6r^2+6rw+6r+6w+2; at mu0=2/3 it factors as (3r+4)(3r+3w+1)/9.

Stack-wide test of the analytic verdict {a_{n,l}>=0 for n_min<=n<=n_min+4}
AND ladder edge r >= -(1+mu0)/2 AND domain, against all six mu0!=0 maps
(N=10, 1369 cells each): mu0=6/5, 9/5 PERFECT; the only discrepancies are
9+9+9 cells (mu0=-9/5,-6/5,-3/5) and 3 cells (mu0=3/5), ALL of type
map-allowed/analytic-doomed, all in the column at distance 0.1 left of the
edge — the same "nine casualties" phenomenon as mu0=0. Four sample cells
verified by direct evaluation: a_{10w, 10w-1} = 0 exactly and
a_{10w+1, 10w} < 0 (mu0 = -9/5, -6/5, -3/5, +3/5). Zero true mismatches on
11994 exact points across the stack.

## External control: Mansfield-Spradlin w=0 cross-check — PASSED

arXiv:2409.09561, Theorem 11 / Eq. (5.16) (p.25-27): on the w=0 slice their
double-contour Regge asymptotics for odd Delta = n-j carries the overall factor
(2r + m^2 + 1) — asymptotic positivity of the l=n-1 trajectory requires exactly
r > -(1+m^2)/2, the same critical line as our exact law sign(n(r+(1+mu0)/2)+w)
restricted to w=0. Independent method, matching edge (EV-QG-0002). Our result is
exact at every finite n and extends to w != 0, which their paper does not treat.
