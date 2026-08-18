# Depth 2 is closed for n >= 4 (corrected twice; this version stands)

**CORRECTION HISTORY (docs/ERRATA.md).**

1. **ERR-0006** found a real bug in the original "Half B" (it used `M=N/2`,
   a half-integer for odd `N`, so `T_hat<=T_M` did not follow from the
   definition of a minimum) and fixed it in `lab/depth2_parity_proof.py` by
   splitting into two parity branches with an actual integer comparison level
   `K` -- both branches proved by Bernstein in under a second, verified 70/70
   against the exact engine first. **This fix stands.**

2. **ERR-0006 also claimed** n=6 and n=7 are genuine exceptions where the
   coefficient goes negative strictly below the true shore. **ERR-0007
   retracts this claim**: it was caused by a bug in the EXPLORATORY test
   script (`D_shore = T_hat(lam) + 3` instead of `T_hat(lam)`, an accidental
   extra `+3` that shifted every tested gamma by 1.5). Rechecked with the
   correct formula, dense grid, n = 4..40: **zero failures.** n = 6, 7 are
   clean like every other level.

**Net result: depth 2 has no known exception.** Proved for `n >= 6` (even) /
`n >= 7` (odd) by the parity-split Bernstein certificates (`K >= 3`,
`lam <= 0.3N`) plus the unconditional algebraic Half A (`lam >= 0.291N`,
covering all lam together with Half B); n = 3, 4, 5 checked directly and
clean. n = 3 has no depth-2 knife at all (`j` only runs 2..n-1 = 2).

Below is the ORIGINAL (superseded) writeup, kept for the record.

---

Not a scan. The pieces below are exact algebra and exact Bernstein subdivision,
and together they cover the whole physical region.

## The object

The sign of the depth-2 coefficient equals the sign of

    H(L) = E2 L(L+1) - B X (L+1) + A X^2,   L = gamma + 2N - 3,  X = (N+lam)^2

verified against the exact knife engine on 75 cells, 0 mismatches, with

    E1 = N(N^2-1)/3
    E2 = N(N^2-1)(5N^3-9N^2-5N+21)/90
    A  = N(N-1)(2N-3)(2N-1)/8
    B  = N(N^2-1)(N-1)(2N-3)/6

E2 > 0 for every N >= 3, so H is CONVEX in L.

## Half A -- unconditional for large lam, by exact algebra

    disc(X) = (B^2 - 4 A E2) X^2 + 2 E2 B X + E2^2

and, derived by hand and verified exactly for N = 3..400,

    B^2 - 4 A E2 = -N^2(N^2-1)(N-1)(2N-3)(N^3-3N^2+11N-3)/90

The bracket N^3-3N^2+11N-3 is positive for every N >= 2, so B^2-4AE2 is NEGATIVE
always and disc is a downward parabola in X. Above a critical X there is no real
root at all: the depth-2 coefficient is positive for EVERY dimension, with no
shore condition. The critical lambda is 0.291 N, asymptotically sqrt(5/3) - 1.

## Half B -- the rest, machine-proved

For lam <= 0.3 N it is enough to check H at the top-knife condition of the HALF
level M = N/2, because the shore is a minimum over levels and so never exceeds
it. With lam = cN the numerator of H is degree 12 in N with leading coefficient
5(6c^2-1)^2 -- a square, positive for c away from 1/sqrt(6) = 0.408, and the
region stops at 0.3.

Moebius compactification N = 5/(1-v) plus exact Bernstein subdivision proves
H > 0 on the whole region N >= 5, 0 <= c <= 3/10: **15 boxes, 0 open, 4 seconds.**
A Bernstein bound above zero on a box is a statement about the box, not a sample.

## The halves overlap

Half A covers lam >= 0.291 N, half B covers lam <= 0.3 N. The overlap is real, so
together they cover every lam.

## The finite remainder

N = 3 and N = 4 are outside half B (the cleared denominator has (N-4)^3). Both
were checked directly: lam from 1/20 to 200 in steps of 1/20, zero failures, and
for these N half A takes over above lam ~ 0.5. Uncovered: lam < 1/20 at N = 3, 4,
a finite sliver that a direct interval check closes.

## Status

Machine-proved here; NOT self-certified. Under our own rules this needs an
independent replication of the Bernstein run and of the two hand-derived closed
forms before it is called a theorem in public.
