# Shift report -- 2026-08-17 15:04 (started this morning, machine clock)

Commit at writing: 9b93cf5. Full detail in article/DATA_LOG.md; live state
in HANDOFF.md; plan in research/keystone-plan.md.

## GREEN, with numbers

1. **The bracket became ONE Beta-weighted integral of a D-FREE polynomial**,
   and then a single univariate polynomial J(Q). exact_checks=6720, verified=True
   Consequence: the previously open Stokes-topology problem is GONE -- signs
   now come out without any asymptotics.

2. **THE DESCENT LEMMA, PROVED**: positivity at D+2 implies positivity at D,
   uniformly in the spin. forward_relation_exact=120/120, inverse_reconstruction_exact=120/120, all_verified=True
   Consequence: the theorem collapsed from a region of width ~19 lam to a
   STRIP OF WIDTH 2 below the shore. Everything below is free, for all knives
   at once.

3. **Three of four parameters are now carried symbolically.** lam: cells=7740, certified=7740, all_certified=True
   n: cells=432, certified=432, all_certified=True  Strip version (lam and n together, on the strip): closing
   branch after branch, j = 2..12 done as of writing, zero failures.

4. **The leading-coefficient fact, PROVED**: sign is (-1)^(j-1), so odd
   knives can never cut and even ones must. 

5. **Foreign-engine confirmation of the tightest zone** (Z3, not our code):
   branch k = 44..46, lam about 26, levels 38..52 -- 135 continuous cells,
   zero alarms, zero unknowns.

6. **A measured law**: D* - shore -> C (j-2), C = 2.398 +- 0.002, with the
   shore growing as (12+4 sqrt 3) lam. The absolute clearance SATURATES; the
   relative margin thins like 1/lam. Explicit falsifier recorded.

## WHAT IS LEFT

* positivity inside the width-2 strip, for ALL knives (j is the last
  unbounded index; certificates are finite in j);
* lam above the last branch (lam > about 26) -- outside coverage, needs a
  tail argument, and it is exactly where the relative margin is thinnest.

No claim of the grand theorem. Three proved lemmas plus certificates that are
finite in j.

## WHERE I WAS WRONG TODAY (five entries, all logged)

* **ERR-0003**: the shore itself was computed with a hard-coded cap k <= 60,
  overestimating it by 1.47x at lam = 150 and 5.96x at lam = 1000. It
  surfaced as an apparent COUNTEREXAMPLE to the grand theorem -- both the
  master formula and the reduction agreed P < 0 below the shore, and the
  shore was the bug. Published work unaffected; the older release code was
  already more careful than my new code.
* **A defect in my own instrument**: the threshold finder bisected assuming a
  single sign change; the polynomial can have up to 9. It reported 1.69 of
  the shore where the first flip is at 1.18. Fixed; both conclusions that
  rested on it were re-checked and survived unchanged.
* **Negatives #19-#26**: manifest positivity on the ray (twice, even and odd
  knives), total-positivity/Karlin route (bound is j-1, not 1), first-two-term
  balance (off by 356x), pointwise monotonicity in j, monotonicity across the
  strip, the naive dimension-walk test (ill-posed by my own hand).
* **Gosper summability**: timed out, recorded as a tool limitation, not a
  result.

## HOW EACH GREEN ITEM IS CHECKED

Every number above comes from an artifact regenerated from a clean tree
(dirty = false), by exact rational or fmpq arithmetic, never floating point
in a decision. The descent lemma is additionally checked against our own
independent partial-wave solver, which knows nothing about the connection
formula. The tightest zone is checked by a foreign engine that shares no code
with our certificates.

## SIDEWAYS LOOK (the 360 rule)

The problem turns out to be a classical one in another field: our partial
waves ARE Schoenberg coefficients on the sphere S^(D-2), the class of
positive definite functions shrinks with dimension, and therefore a shore
MUST exist -- sphere geometry, not string physics. Prior art read in full
text, not from abstracts: Bo Wang arXiv:2403.00906 proves manifest positivity
by a different route (harmonic numbers, contour integrals, coefficient by
coefficient) and states that manifest unitarity below the critical dimension
was still missing. His conjectured LOW SPIN DOMINANCE does NOT hold in our
family: over 46 cells the minimising spin was never <= 2, running from 8 to
90. Written up in research/schoenberg-direction.md with a deterministic
falsifier.
