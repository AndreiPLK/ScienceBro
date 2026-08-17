# The knife problem is a Schoenberg positive-definiteness problem

Written 2026-08-17 14:29. This is a DIRECTION, not a result: it names an existing
body of mathematics that matches our structure exactly, plus the concrete
first step to test it.

## The observation

Our object of study is: for a fixed level n, are ALL partial-wave
coefficients P_j (j = 2, 3, ...) of the residue nonnegative, as a function
of the spacetime dimension D?

That is verbatim the classical question answered by Schoenberg (1942): a
continuous isotropic function on the sphere S^(d-1) is POSITIVE DEFINITE if
and only if its expansion in Gegenbauer polynomials has nonnegative
coefficients. Those coefficients are called the d-dimensional Schoenberg
coefficients. Our partial-wave coefficients ARE Schoenberg coefficients, and
our D is the sphere dimension (partial waves live on S^(D-2)).

## Why this explains the shore without any amplitude physics

The class of positive definite functions on S^(d-1) SHRINKS as d grows: a
function positive definite on a larger sphere is positive definite on every
smaller one, never the other way round. Therefore, for a fixed residue
function, there is a largest dimension at which positive definiteness still
holds -- a CRITICAL DIMENSION. That is exactly what we call the shore,
T_hat(lam), and it explains structurally why a shore must exist at all,
independently of anything specific to string amplitudes.

## The tool this points at: dimension walks

There is an explicit apparatus for moving positivity between dimensions --
"dimension walks" (montee and descente operators, Matheron; see Gneiting,
"From Fourier to Gegenbauer: Dimension walks on spheres", arXiv:1303.6856,
and the strictly-positive-definite refinements in
doi:10.1016/j.jat.2017.03.002). These are operators relating the Gegenbauer
coefficients in dimension d and d+2, and monotonicity properties of those
coefficients guarantee positive definiteness in higher dimensions.

If our residue's coefficient family fits one of those monotonicity classes,
the D-dependence we have been fighting cell by cell may be available
wholesale -- and, more importantly, UNIFORMLY IN j, which is precisely the
one gap left in the keystone (lam, D and n are already carried symbolically;
j is closed only finitely).

## Concrete first step (falsifiable)

Take our exact P_j at fixed (n, lam) and test the descente/montee relation
numerically: does the operator that maps dimension D to D+2 send our
coefficient sequence to the coefficient sequence we compute directly at
D+2? Exact rational check, cheap with the machinery we already have.
  * If YES: we inherit the whole dimension-walk toolkit, and the natural
    next question is whether our sequence is in a class where positivity at
    the shore propagates for all j at once.
  * If NO: the analogy is superficial, record it as a negative with the
    mismatch, and drop it.

## Honest caveats

  * Schoenberg's theorem concerns positive definiteness of a FUNCTION; our
    residue is a polynomial in the scattering angle at fixed level, so the
    correspondence must be checked, not assumed.
  * The literature answers "positive definite on S^(d-1)?" for fixed d; the
    critical-dimension question ("largest d") is standard in principle but I
    have not yet found it treated with the sharpness we need.
  * Nothing here is evidence for our claims. It is a map of where to look
    next, with a deterministic test attached.
