# Theorem: the normalised means are never a Pólya frequency sequence

*2026-08-30, night shift. A complete, human-readable proof. Every step is an identity
the reader can check; nothing here rests on a certificate or on a grid.*

## Setting

Fix an integer `n >= 4`, put `N = n - 1`, and let

    b_k = (n - 2k)^2,   k = 1, ..., N

be the centred spectrum of the graviton problem. Write `e_t = e_t(b)` for its
elementary symmetric functions and

    p_t = e_t / C(N, t)

for the normalised elementary means. Set `p_t = 0` for `t < 0`, so `p_0 = 1`.

## Theorem

For every `n >= 4`,

    p_1^3 - 2 p_1 p_2 + p_3  =  -(4/945) · n (n+1) (7n^3 - 43n^2 + 58n + 120)  <  0.

The left-hand side is the `3 x 3` Toeplitz minor of `(p_t)` on rows `(1,2,3)` and
columns `(0,1,2)`. Consequently **`(p_t)` is not a Pólya frequency sequence for any
`n >= 4`**, and the failure is not marginal: the minor grows like `-(4/135) n^5`.

By contrast `(e_t)` **is** a Pólya frequency sequence for every `n`, since
`SUM_t e_t z^t = PROD_k (1 + b_k z)` has only real nonpositive roots and
Aissen–Schoenberg–Whitney applies.

## Proof

**Step 1 — the minor.** For a sequence with `a_0 = 1` and `a_{-1} = 0`, the Toeplitz
matrix `[a_{i-j}]` restricted to rows `(1,2,3)` and columns `(0,1,2)` is

    [ a_1  a_0   0  ]
    [ a_2  a_1  a_0 ]
    [ a_3  a_2  a_1 ]

whose determinant expands to `a_1^3 - 2 a_0 a_1 a_2 + a_0^2 a_3`, i.e. to
`a_1^3 - 2 a_1 a_2 + a_3`.

**Step 2 — the three elementary functions in closed form.** For the centred spectrum,

    e_1 = n(n-1)(n-2) / 3,
    e_2 = n(n-1)(n-2)(5n^3 - 24n^2 + 28n + 12) / 90,
    e_3 = n(n-1)(n-2)(n-3)(n-4)(35n^4 - 154n^3 + 172n^2 + 292n + 120) / 5670.

Each is a polynomial identity in `n`, checked against the direct symmetric-function
computation at every `n` from 4 to 59.

**Step 3 — clear the denominators.** With `C(N,1) = N`, `C(N,2) = N(N-1)/2`,
`C(N,3) = N(N-1)(N-2)/6`,

    p_1^3 - 2 p_1 p_2 + p_3
        = e_1^3/N^3 - 4 e_1 e_2 / (N^2 (N-1)) + 6 e_3 / (N(N-1)(N-2)).

Multiplying by the positive quantity `N^3 (N-1)(N-2) = (n-1)^3 (n-2)(n-3)` gives the
polynomial

    Num(n) = e_1^3 (N-1)(N-2) - 4 e_1 e_2 N(N-2) + 6 e_3 N^2,

which factors completely:

    Num(n) = -(4/945) · n (n+1) (n-1)^3 (n-2)(n-3) (7n^3 - 43n^2 + 58n + 120).

**Step 4 — the cancellation.** The factor `(n-1)^3 (n-2)(n-3)` is exactly the
denominator cleared in Step 3, so it cancels and

    p_1^3 - 2 p_1 p_2 + p_3 = -(4/945) · n (n+1) (7n^3 - 43n^2 + 58n + 120),

a polynomial of degree five with no denominator left.

**Step 5 — the sign.** Substituting `n = m + 4` with `m >= 0`,

    7n^3 - 43n^2 + 58n + 120 = 7m^3 + 41m^2 + 50m + 112,

every coefficient of which is positive, so the cubic is at least `112 > 0` for all
`n >= 4`. Since `n(n+1) > 0` and the prefactor is negative, the minor is strictly
negative for every `n >= 4`. ∎

## Independent verification

Four separate paths, because a load-bearing identity gets checked by something other
than the code that produced it:

1. the closed forms of `e_1, e_2, e_3` against direct symmetric-function evaluation,
   `n = 4..59`, no mismatches;
2. the closed form of the minor against the determinant computed from the definition,
   `n = 4..60`, no mismatches;
3. the shift argument re-derived from scratch: `-Num(m+3)` also has all coefficients
   nonnegative, an independent route to the same sign;
4. spot values by hand: at `n = 4` the spectrum is `{4, 0, 4}`, giving
   `p_1 = 8/3`, `p_2 = 16/3`, `p_3 = 0` and a minor of `512/27 - 256/9 = -256/27`,
   which is what the formula returns.

## What it settles

**It closes a route.** Total positivity and the log-difference hierarchy
`Delta^r log p_t < 0` sit on opposite sides of the binomial normalisation: `e` is
totally positive and lacks the hierarchy, `p` has the hierarchy and — now provably —
is never totally positive. Any Lindström–Gessel–Viennot or planar-network argument
proves statements about the totally positive object, which is the wrong one. The route
was the leading surviving candidate after the moment representation died the same
night; it is dead too, and this time by a theorem rather than by a scan.

**It does not settle the main conjecture.** (B) and the hierarchy remain open. What the
theorem removes is a family of proof strategies, and it says why: the phenomenon
belongs to the *pairing* of a real-rooted spectrum with binomial weights, not to either
factor. Normalised elementary means are exactly the coordinates of the finite free
transforms, which is where to look next.

## Status

`CLAIM-NOPF` in the registry: **PROVED**. This is the first statement in the programme
proved with no certificate, no grid and no numerical step anywhere in the argument.
