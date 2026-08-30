# The central diagonal is holonomic in principle, and out of reach of brute force

*2026-08-30. Artefact: `results/central_diagonal_holonomy.json`, tool
`tools/sciencebro_math/recurrence.py`.*

## The route

The brief proposed route (8) for conjecture (C): if the central diagonal
`e_{floor(N/2)}(n)` is P-recursive, then existing algorithmic machinery computes a finite
threshold beyond which higher Turán / Laguerre inequalities hold, and the finite remainder
closes by exact arithmetic. That would turn (C) — parity monotonicity `M_{n+2} <= M_n` —
from monstrous direct algebra into a recurrence plus a bounded check.

## The search, and what it actually settles

Fitting a P-recurrence is linear algebra, and the trap is that with more unknowns than
data a nullspace vector always exists and means nothing. The tool therefore **fits on part
of the data and verifies on held-out terms**; a candidate that fails the held-out
equations is reported as an artefact, not a recurrence. It was validated on controls
first: Catalan numbers found at order 1, degree 1; a random sequence correctly rejected.

On 46 terms of the central diagonal, split by parity, **52 (order, degree) pairs were
genuinely tested** — up to order 5 and degree 14 in combination — and none survived
held-out verification, on either the odd or the even branch. The same for the two
neighbouring diagonals.

## But the route is not dead, and the reason matters

The array is holonomic. The exact two-dimensional recursion

    e_t(n+2) = e_t(n) + 2 n^2 e_{t-1}(n) + n^4 e_{t-2}(n)

is verified here at **1767 `(n,t)` pairs over `n = 3..59`, zero mismatches**. It is a
recurrence in `n` with polynomial coefficients and finite support in `t`, so the array is
P-recursive in both indices. By Lipshitz's theorem the diagonal of a holonomic
two-dimensional sequence is itself holonomic.

**So the recurrence exists; our search simply did not reach it.** That is the useful
outcome: the negative result is about the search window, not about the mathematics, and it
says what the next step must be. Diagonal recurrences are routinely of much higher order
than the array they come from, and brute-force fitting scales as `(L+1)(D+1)` unknowns
against `terms - L` equations, so it loses quickly. Obtaining this one needs **creative
telescoping** (Zeilberger-style) applied to the 2D recursion, not a larger fit.

## Honest statement of what is and is not known

* The 2D recursion: verified exactly, 1767 pairs.
* Holonomy of the diagonal: **follows from a published theorem**, given that recursion —
  it is not something this repository has verified computationally, and the theorem's
  hypotheses should be checked against our setting before it is leaned on.
* Non-existence of a small recurrence: exact, on the stated window, and it is a statement
  about that window only.

## Status

Route (8) is **open and viable**, with an explicit next step. It is not recorded as a dead
route, because nothing about it failed — only a brute-force search that was never the
right instrument.
