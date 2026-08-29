# The moment route is closed: no positive measure explains the hierarchy

*2026-08-29 night. Artefact: `results/moment_route_refutation.json`, module
`lab/moment_route_refutation.py`.*

## What was proposed

The anomaly-map brief's "potential jackpot": if

    A_t = -Delta^2 log p_t = log( p_{t+1}^2 / (p_t p_{t+2}) )

is a moment sequence of a positive measure, then the entire observed hierarchy
`Delta^r log p_t < 0` for all `r >= 2` would follow from that one representation, and
with it our conjecture (B), which is the member `r = 3`.

It would have been the single mechanism behind everything. It does not exist.

## Step 1, on paper: the un-reversed form was excluded before computing

The hierarchy says exactly that `A` is **absolutely** monotone — every forward
difference `Delta^k A >= 0` — because `Delta^r log p = -Delta^{r-2} A`. An absolutely
monotone sequence is a moment sequence of a measure on `[1, infinity)`, whereas a
Hausdorff (completely monotone) sequence lives on `[0,1]` and DECREASES. So the
brief's Hausdorff form applied to `A` as written contradicts (B) outright, and its own
hedge — "or becomes one after reversing the index from the center" — was compulsory
rather than a fallback.

## Step 2, by computation: both orientations die

Any positive-measure representation forces every Hankel matrix of the sequence to be
positive semidefinite. Leading-minor sign patterns:

| `n` | terms | forward `A` | first negative | reversed `A` | first negative |
|---|---|---|---|---|---|
| 21 | 10 | `+++--` | 4 | `++++-` | 5 |
| 31 | 15 | `+++--++-` | 4 | `+++++-+-` | 6 |
| 41 | 20 | `+++---++--` | 4 | `+++++---+-` | 6 |
| 61 | 30 | `++++---++--++--` | 5 | `+++++++--++--++` | 8 |
| 81 | 40 | `++++---+++--++---++-` | 5 | `++++++++---++--++--+` | 9 |
| 101 | 50 | `+++++---++---++--+++--++-` | 6 | `++++++++----+++--++--++--` | 9 |

**A positive measure is excluded in both orientations, at every `n` tested.**

## Why the numbers are trustworthy

`A` is transcendental, so this cannot be done in exact arithmetic directly. Instead
`A` is rationalised to 300 digits and the determinants are evaluated **exactly over
`Q`** with flint — a genuinely independent code path from the floating-point version,
which agrees with it. Each decisive minor comes with a rigorous error bound
`k! * max|A|^(k-1) * 10^-300`, and every one of them clears its bound by more than
**200 orders of magnitude**:

| case | order | `|det|` | error bound |
|---|---|---|---|
| `n = 21`, forward | 4 | 1.86e-17 | 1.78e-302 |
| `n = 41`, forward | 4 | 1.30e-24 | 2.21e-303 |
| `n = 101`, reversed | 9 | 5.48e-114 | 4.09e-309 |

These signs are facts about the sequence, not numerical noise.

## What survives, and what this costs the programme

The hierarchy is real — it was confirmed exactly earlier the same night, 0 violations
for `r = 2..8` with the window inside the first half. What is now excluded is its most
attractive explanation.

Still open as mechanisms:

* total positivity of the Toeplitz array (Polya frequency), which the battery finds
  consistent so far;
* an LGV / planar-network model producing the signs combinatorially;
* a determinant or minor identity for `H_{N,t}` directly;
* a recurrence carrying the sign.

Worth noting for whoever picks this up: the first negative order **grows with `n`**
(4, 4, 4, 5, 5, 6 forward; 5, 6, 6, 8, 9, 9 reversed). The sequence is becoming
smoother, so the obstruction retreats — but it never leaves. An argument that only
inspects low orders at large `n` would miss it, which is exactly the shape of mistake
this lab has made before.
