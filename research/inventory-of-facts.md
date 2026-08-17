# INVENTORY OF EVERY STRUCTURAL FACT WE OWN

Written 2026-08-17 17:48, on the founder's instruction: stop trying new tricks and go
back over EVERY small formula and every stage of the work, looking for
something already in our hands that has not been used.

Format: fact -- status -- where it could still be applied.

## A. Facts about the bracket (the sum itself)

A1. **Closed hypergeometric form** of P_j (4320 exact checks).
    USED -- it is the base of everything after it.

A2. **The square identity**: SUM (-1)^t E_2t x^t = [prod (1 - a^2 x)]^2.
    USED for the kernel. NOT used for the weights. The reason the "square
    root of the residue" attempt failed is that the square lives in the
    spectral variable, not the angular one -- so any future use must stay in
    the spectral variable.

A3. **Beta / Stieltjes moment representation** -> one univariate polynomial J.
    USED -- our main reduction.

A4. **Contour representation** (verified to 1e-13).
    NOT USED since the Beta reduction replaced it. Worth revisiting for one
    specific purpose: the remaining gap is an OSCILLATORY estimate, and
    contour methods are the natural home of those (Riemann-Hilbert). This is
    the strongest unused asset we have.

A5. **Saddle = the largest double root**, cancellation localised at theta = pi.
    NOT USED. Same note as A4: it is asymptotic information we never fed into
    an actual estimate.

A6. **Abel-Plana-type mechanism**, exponent pi*alpha with alpha = 0.380
    matching the measured saddle.
    NOT USED. It was abandoned when the naive saddle sum failed (Stokes).

A7. **D = 6 is an exact Saalschutz point** (the sum collapses there).
    NOT USED. Today's attempt to find OTHER collapse points failed because my
    smoothness detector was noisy. A proper search would test for rational
    roots / Pochhammer-product structure instead of prime smoothness.

## B. Facts about the ladders

B1. **Descent in D** (classical Matheron montee): positivity at D+2 => at D.
    USED -- gives the width-2 strip. Note the direction: it moves DOWN in D.
    We would need the UP direction to lift a closed form at D=6 toward the
    shore, and the up direction does NOT preserve positivity in general.
    That asymmetry is exactly why A7 has not helped yet.

B2. **Level recursion** F_{n+2} = F_n (1 - n^2 y)^2, one new double root per
    level, entering at the outer edge.
    PARTIALLY USED (the Weyl-operator step is exact but not sign-preserving).

B3. **Knife ladder**: averaging with the positive kernel 1/(j-t) plus a
    boundary term carrying (-1)^j.
    USED to explain parity. Its inequality turned out to be equivalent to the
    theorem, so it is not a route by itself.

## C. Facts about the geometry of the answer

C1. **Parity law**: leading coefficient sign (-1)^(j-1); odd knives never cut.
    PROVED and USED.

C2. **Margin law**: D* - shore -> C(j-2), C = 2.398 +- 0.002; shore ->
    (12 + 4 sqrt 3) lam.
    MEASURED, used only as a target. The constant is unidentified.

C3. **Tightest level n* = k(lam) - 1**: the closest knife rides the very
    trajectory that defines the shore.
    NOT USED. Tested today for an identity linking T_k to the bracket at
    n = k-1: none found; the region k +- 1 is flat.

C4. **Low spin dominance FAILS here** (minimising spins 8..90).
    USED as a result in its own right (it contradicts a published conjecture)
    and as the reason to re-run the counterexample hunt at high spin.

C5. **Residue's angular coefficients strictly alternate**, pattern independent
    of lam; all roots real and positive in cos^2.
    USED to explain why a shore must exist at all (Schoenberg nesting).

C6. **J has 0..12 real roots** depending on the cell (not a fixed structure).
    Measured today; kills the "one real root" shortcut.

## D. What this inventory says

The unused assets cluster in ONE place: A4, A5, A6 -- the contour /
saddle / Abel-Plana material. And the remaining gap is precisely an
oscillatory asymptotic estimate. That is not a coincidence: we abandoned that
line in the morning when the naive saddle sum failed by 250 orders of
magnitude, and then spent the day on algebraic routes, all of which died on
the same global-cancellation wall.

So the honest conclusion of the inventory is that the ONE line we own and
never finished is the one the problem actually calls for. The failure in the
morning was not "the method is wrong" -- it was "the Stokes topology was not
determined", which is a specific, solvable sub-task with a known technique
(steepest-descent path tracking / Riemann-Hilbert).

## E. Concrete next actions in priority order

E1. Return to A4/A5 and determine which saddles are ACTIVE, properly:
    track the steepest-descent path numerically in high precision and read
    off the contributing critical points, instead of summing all of them.

E2. Redo the collapse-point search (A7) with a correct detector: test whether
    J(Q) has rational roots or whether its value is a ratio of Pochhammer
    products, not prime smoothness.

E3. If E1 gives the active saddles, the margin constant C (C2) becomes
    computable, and the same estimate is what the strip needs -- one technique
    closing two open items.
