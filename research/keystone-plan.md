# Keystone plan (rewritten 2026-08-17 14:48 after the descent lemma)

The architecture changed today. What follows replaces the earlier plan; the
old one is in git history.

## The theorem we are after

For the CHR graviton family (arXiv:2408.03362), no positivity constraint
("knife") cuts anywhere strictly inside the allowed region: for every level
n, every knife j, every deformation lam and every dimension D below the
shore T_hat(lam), the partial wave is positive.

## What is PROVED

1. **The Beta reduction.** sign P_j = sign of a single Beta-weighted integral
   of a D-FREE polynomial; the integral collapses to one univariate
   polynomial J(Q), Q = D/2 + n - j - 2, with rational coefficients in
   (n, lam). Artifact: keystone_beta.json (6720 exact checks).
2. **The leading-coefficient fact.** The leading coefficient of J has sign
   (-1)^(j-1). Odd knives can never develop a threshold; even ones must.
   Artifact: keystone_margin_law.json (324 checks).
3. **THE DESCENT LEMMA.** Positivity of all partial waves at D+2 implies
   positivity at D, uniformly in the spin. Mechanism: the Gegenbauer
   connection at mu = a+1 truncates after two terms, c0 > 0 and c1 < 0, so
   the inverted relation is a positive combination and induction runs down
   the spin. Artifact: keystone_dimension_walk.json (120+120 exact checks,
   zero sign violations).

## What the lemma buys

Everything below the strip D in (T_hat - 2, T_hat] is FREE. The theorem
reduces to that strip, for all knives at once. Measured on the strip: the
Polya certificate is MANIFEST -- 1248 grid cells at bisection depth zero,
including j = 2, which on the full stretch could not be certified at all.

## The remaining task, in order

1. **Strip certificate, symbolic in lam and n** (running:
   lab/keystone_strip_symbolic.py). One cell = a whole shore branch x all
   levels of one parity. Closed so far through j = 10, zero failures.
   -> when this covers every branch k and both parities for a given j, that
      knife is PROVEN for all n, all lam on the covered branches, all D.
2. **The last infinity: j.** Options, in order of promise:
   a. find the pattern in the strip certificate's coefficients as j grows
      (they are explicit finite sums; the strip made them manifest, which is
      a much better starting point than the full stretch ever was);
   b. induction in j using Q_{j+1}(t) = Q_j(t)/(j - t);
   c. the level recursion F_{n+2} = F_n (1 - n^2 y)^2 with the Weyl operator
      step (keystone_induction.json) -- exact but not sign-preserving as it
      stands.
3. **lam above the last branch** (lam > about 26). Still outside coverage;
   needs a tail argument as in the knife theorems. Note the margin law says
   this is where the RELATIVE margin is thinnest (it shrinks like 1/lam),
   so it is the delicate region, not a formality.

## What must NOT be claimed yet

The grand theorem. Right now: three proved lemmas, a reduction that removes
almost all of the parameter space, and certificates that are finite in j.
No claim of "proved" until j is closed and the lam tail is covered, and not
before the deterministic gate passes on artifacts from a clean tree.

## Falsifiers on the table

* any cell with P_j <= 0 at 4 <= D < T_hat (exact rational) kills the
  theorem outright;
* any cell where the strip certificate fails and bisection cannot repair it
  bounds the method;
* any cell with D* - T_hat < 2.39 (j-2) - 0.05 at lam >= 100 kills the
  margin law (a regularity, not a theorem).
