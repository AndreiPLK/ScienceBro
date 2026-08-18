# The AEHM / Mansfield route: calibrated, then closed for our regime

Date: 2026-08-18 (night). Engine 2 throughout (`flint.fmpq_poly`), exact
rational series arithmetic, no floats in any comparison.

## Why this was worth testing

The literature pass (`research/reading-notes/keystone-uniformity-2026-08-18.md`)
found that our object is a `lam`-deformation of one already solved: with
`y = s*v` we have `s^N q = 2^N ((y-N+1)/2)_N`, and `F = q^2` is the square of a
Pochhammer product -- exactly the structure of the Virasoro-Shapiro residue,
which is the square of the Veneziano residue (Mansfield arXiv:2502.20372,
Eqs. (3.5)-(3.7)).

Mansfield proves `B^D_{n,j} >= 0` for ALL `n` and ALL `j` at `D <= 10` --
precisely the kind of uniform-in-trajectory statement our keystone needs, and
by a mechanism (a manifestly positive Laurent expansion) that is NOT on our
closed-routes list. So it had to be tested, not assumed inapplicable.

## The mechanism, and the quantity that decides whether it transfers

Their central formula (2.11) writes the partial-wave coefficient as a double
contour residue of a product of two Laurent series. Positivity is MANIFEST
whenever both series have only non-negative coefficients: a residue of a
product of positive series is positive, and that single argument covers every
`n` and every `j` at once, with no induction.

The `D`-dependence sits in one factor, `(1-z)^{-1} / log(1-z)^{(D-2)/2}`. Their
proof needs that series to have FEW negative coefficients, because each one has
to be cancelled by hand with a rational corrector `P_j(x,y)` of vanishing
residue (their (2.14)) -- a finite computation only while the negatives are
finite and few.

## Known-answer calibration (done FIRST, per the experiment contract)

Our exact series computation reproduces all three of the paper's own printed
counts:

| D | (D-2)/2 | negatives, ours | paper | leading coefficients (ours) |
|---|---|---|---|---|
| 6 | 2 | **0** | "only positive coefficients" | 1, 0, 1/12, 1/12, 19/240 |
| 8 | 3 | **1** | "a single negative term `-z^{-2}/2`" (2.12) | 1, **-1/2**, 0, 0, 1/240 |
| 10 | 4 | **8** | "at least eight negative coefficients" | 1, -1, 1/6, 0, -1/720 |

The `D = 8` head `1, -1/2, 0, 0, 1/240` matches their Eq. (2.12)
`z^{-3} - (1/2) z^{-2} + z/240 + ...` term for term. The calibration also caught
a sign error in our first attempt (we had normalised by `(-1)^{p+1}` rather than
on the leading coefficient), which is exactly what a known-answer baseline is
for.

## The verdict for our regime

Their `D` is capped at 10 by `B^D_{3,0} = (10-D)/(24(D-1))`. **Ours is not.** Our
shore grows with the deformation, `T_hat(lam) ~ 18.9*lam` for large `lam`
(consistent with the `12 + 4*sqrt(3)` constant already noted in ERR-0006), so at
`lam = 100` the admissible `D` is about 1890.

Negative-coefficient count in the first 60 coefficients:

| D | 6 | 8 | 10 | 12 | 16 | 24 | 40 | 80 | 160 | 400 | 1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| negatives | 0 | 1 | 8 | 32 | 46 | 22 | 34 | 28 | 30 | 30 | 30 |

The count does not stay small and does not decay: past `D ~ 12` roughly HALF the
coefficients are negative, and that fraction is flat out to `D = 1000`. A finite
hand-built corrector `P_j` cannot absorb a constant fraction of an infinite
series.

**Conclusion: the manifest-positivity mechanism does not transfer to our regime.**
Not because the algebra fails, but because the very feature that makes their
`D <= 10` proof finite -- a handful of negative Laurent coefficients -- is a
low-`D` accident, and our physically admissible `D` is unbounded in `lam`.

## The honest limit of this test

What was computed is the UNDEFORMED series (`lam = 0`) at large `D`, not a
`lam`-deformed analogue of (2.11) -- no such deformed representation exists in
the literature, and deriving one is itself open work. The `D`-dependence enters
through the power of the logarithm, which is why the obstruction is expected to
persist under deformation; but this is an argument, not a proof. The correct
statement is: **the route is closed under the natural transfer, and reopening it
would require a deformed contour representation whose `D`-factor behaves
differently from `(1-z)^{-1}/log(1-z)^{(D-2)/2}`.** That is a specific, checkable
thing to look for, not a dead end by fiat.

## What this settles about priority, and it is the useful part

Mansfield's theorem covers `lam = 0, D <= 10`. Our problem lives at `lam > 0`
with `D` up to `T_hat(lam)`, growing without bound. The two do not overlap
except at a single endpoint. So:

* their result does NOT already contain ours -- the gap identified in the
  literature pass (nobody has done all `j` for the CHR family) stands;
* and their method does not hand us the keystone either.

Both halves are worth stating plainly in the paper: we engage with the closest
prior art, reproduce its numbers exactly, and show precisely where the regimes
part company.
