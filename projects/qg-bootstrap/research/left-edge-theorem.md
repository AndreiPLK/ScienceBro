# The left edge of the island: a_{n,n-1} in closed form (mu0=0, D=4, q=1)

Date: 2026-08-13. Status: analytic derivation below, numerically verified in exact
arithmetic at 66 points (6 targeted predictions incl. two exact zeros at off-grid
points + 60 random (n,r,w)). Independent review: NOT yet done (domain-critic pass
pending) — do not promote beyond "analytic derivation, numerically confirmed".

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
2. **The island's true left edge at mu0=0 is r = -1/2** (for w > 0): every point
   with r < -1/2 is excluded at depth n > w/|r+1/2|. Finite-depth maps overstate
   the island in the sliver r in (-0.6, -0.5); erosion is slow (depth ~ 1/dist)
   but total. At r = -1/2 the coefficient equals w * (positive) >= 0: marginal,
   never negative — the edge itself survives all depths on this trajectory.
3. **Practical**: fine-grid scans at fixed NMAX must be post-processed with this
   rule on the left edge; a cell at r = -1/2 - eps apparently "allowed" at
   NMAX=20 is doomed iff w > 20*eps.

## Open

- Same analysis for the leading trajectory a_{n,n} (top coefficient (n/2)^n > 0
  always — leading trajectory never kills; consistent with data).
- General mu0 (shifted substitution t = -(n-3mu0)(1-x)/2 - mu0) — next slice.
- a_{n,n-2} (third trajectory): does it produce the N>=2-depth edges elsewhere?
- Cross-check against Mansfield-Spradlin w=0 limit.
