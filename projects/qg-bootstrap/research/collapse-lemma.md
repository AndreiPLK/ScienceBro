# THE COLLAPSE LEMMA — every knife is a power of the first (paper 5 core)

Date: 2026-08-16. Status after critic round 1 (collapse-lemma-review.md): PROPOSITION (not
theorem-gated yet): limit derived, ratio upper bound closed by the critic's
repeated-index lemma; RATE claim rescoped (see below); zone battery gated
counts only, scope = window belt.

## Statement (leading-order limit theorem)

Fix j >= 2 and (rho, delta) with rho > 1, delta > 0. Let m -> infinity along
integers with s = lam + m + 2 = rho*m (lam = (rho-1)m - 2) and D = delta*m.
Normalize the master bracket by its i=0 term. Then

    B_j / term_0  --->  (1 - X)^{j-1},     X = 6 rho^2 / (delta + 4).

RATE (rescoped after critic F5): absolute deviation is O_j(1/m); the
RELATIVE rate degrades where (1-X)^{j-1} is exponentially small in j
(measured p ~ 0.5-0.6 at X=1.1, j=7,8): state the rate for the absolute
error, not the relative one. At X=1 the deviation is O(m^{-ceil((j-1)/2)})
by the critic's finite-difference cancellation argument (corrections are
LINEAR in the term index) - exactly what sqrt(m) band splitting requires.

## Proof mechanism (exact, term by term)

The master formula gives term_{i+1}/term_i exactly:

  ratio_i = - [ E_{2(j-2-i)} / E_{2(j-1-i)} ] * (2n-2j+2i+2)(2n-2j+2i+1)
              * s^2 / ( 2 (i+1) (D + 4n - 4j - 1 + 2i) )

Three exact ingredients:
  (a) E_{2t}(n) = e_t of the multiset {(n-2k)^2 doubled}; the ratio
      E_{2(t-1)}/E_{2t} = t/(Sigma + correction) with
      Sigma = n(n-1)(n-2)/3; the additive correction is Theta(m^2)
      (~ -0.6(t-1)n^2), relative O(1/m). Lower bound: Newton log-concavity
      (E-ratio >= t/Sigma). Upper bound (gap E5, closed by the critic):
      repeated-index lemma 0 <= 1 - t! e_t/e_1^t <= C(t,2) p_2/e_1^2 with
      p_2/e_1^2 <= 3/m;
  (b) (2n-2j+2i+2)(2n-2j+2i+1) = 4m^2 (1 + O(1/m)) uniformly for i <= j-1;
  (c) the ladder factor D + 4n - 4j - 1 + 2i = (delta+4)m (1 + O(1/m)).
Multiplying: ratio_i -> -[(j-1-i)/(i+1)] * X, and the binomial theorem gives
the product form. Rate: each factor converges at O(1/m), j fixed => overall
O_j(1/m).

## Consequences (why this is the master key)

1. ONE critical surface u = 6 rho^2 m for all knives: the (j-1)-fold
   degenerate root of (1-X)^{j-1}. At subleading order it splits into j-1
   simple roots spread O(sqrt m) - exactly the floor(j/2) negativity bands
   seen in exact zone scans (collapse_zones.json).
2. Sign structure: with sign(a) = (-1)^{j-1} sign(B_j) and term_0 > 0:
   even j: kill region = the semi-infinite side D > D_crit (X < 1, the
   first knife's own dead side) + (j-2)/2 thin bands;
   odd  j: (j-1)/2 thin bands hugging the surface only.
   SCOPE: the band-count prediction applies in the window belt
   rho < sqrt(5/3); outside it windows die (critic probe at rho=1.53:
   fewer/no bands, as containment predicts).
3. Minimizing the surface over levels: d/dm [6 s^2/m - 4m] = 0 at
   rho* = 1 + 1/sqrt3 - the blade theorem's exact tangency is the j=3
   shadow of this universal structure; the envelope asymptote
   (12+4sqrt3)lambda is the collapse surface optimized over levels.

## Honest limits of the tool

- The collapse controls the LARGE-m tail; at moderate m the exact critical
  line differs strongly from 6s^2/m - 4m (checked: n=8, lam=5: asymptotic
  152.8 vs exact T_8 = 94). Moderate m stays on certificates.
- The grand theorem still needs: uniform-in-j remainder bounds (in progress)
  and sqrt(m)-order control of band edges near the optimal level.

## Verification battery

- collapse_zones.json: exact zones for j=2..8, 7 configs n=20..100 (all
  rho in [1.09, 1.15], i.e. inside the belt): BAND COUNTS gated, 0
  deviations. (Offsets reported, not gated - critic E6.)
- attack_collapse.json (critic battery, executed): direct measurement of
  B_j/term_0 vs (1-X)^{j-1} - first direct evidence for the central limit;
  two F5 rate flags at X=1.1 (see rescoped rate above); W5 probes outside
  the belt confirm the scope; splitting-exponent fit consistent with
  sqrt(m).
- Earlier: 3,053,832-point completeness sweep (all j) consistent with all
  bands staying above the envelope.
