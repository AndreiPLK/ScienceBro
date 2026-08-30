# The Jensen polynomials are hyperbolic — and that is why they cannot explain the hierarchy

*2026-08-30. Artefact: `results/jensen_polynomials.json`, module `lab/jensen_polynomials.py`.*

## The positive fact

For the centred family, every Jensen polynomial

    J^{d,t}(X) = SUM_{j=0}^{d} C(d,j) p_{t+j} X^j

tested is hyperbolic — all roots real. **332 of 332**, degrees `d = 2..8`, at
`n = 11, 15, 21, 27, 33, 41`, with the window inside the first half. Coefficients are exact
rationals and roots are isolated by flint in certified boxes, so "real" means the imaginary
interval provably contains zero.

That is a real structural fact: it delivers the whole family of higher-order Turán
inequalities for `p` at once.

## Why it is nevertheless the wrong tool for our problem

The log-difference hierarchy has two sharp signatures, and Jensen hyperbolicity has
neither.

**It does not stop at the midpoint.** The hierarchy fails once the difference window
crosses the midpoint — that is where the reciprocal spectrum takes over. Hyperbolicity does
not care:

| `n` | first half | past the midpoint |
|---|---|---|
| 21 | 29/29 | 40/40 |
| 27 | 41/41 | 52/52 |
| 33 | 53/53 | 64/64 |

**It does not distinguish `e` from `p`.** The hierarchy holds for the normalised `p` and
fails for the raw `e`; total positivity does the opposite (`THEOREM_NO_POLYA_FREQUENCY.md`).
Jensen hyperbolicity holds for both, at every degree tested.

So hyperbolicity is a coarser property than the phenomenon we are chasing: it survives both
transitions that the hierarchy detects. A theorem built on it would prove something true
but weaker, and could not produce a statement that is false for `e` or false past the
midpoint — which (B) and the hierarchy both are.

Note also that `e`'s hyperbolicity is expected rather than surprising: `e` is the
coefficient sequence of a real-rooted polynomial with nonnegative coefficients, hence a
Pólya frequency sequence, and those have hyperbolic Jensen polynomials classically. The
content of the measurement is that the binomial normalisation **preserves** it — the same
normalisation that destroys total positivity.

## Status

Recorded as a structural fact about the family, and as a closed route for explaining the
hierarchy. The higher-order Turán inequalities that follow are a genuine by-product and are
available if ever needed.
