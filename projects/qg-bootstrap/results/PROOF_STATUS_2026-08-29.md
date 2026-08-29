# The chain, and what each link is standing on

2026-08-29, end of day. One line per statement: what it says, what holds it up,
and what it still owes. Nothing here is a summary of intent — every row points at
an artefact.

## The far-below front

| # | statement | status | artefact |
|---|---|---|---|
| 1 | The far-below polynomial `N(y)` has exactly one negative `y`-coefficient, at degree `J-2` | **certified per depth**, `j = 9..16` | `farbelow_negative_pattern_j*.json` |
| 2 | That localisation holds iff `n >= 2J-3` | measured on a grid containing BOTH sides: 1376 points inside with 0 violations, 100 outside with 0 clean | `farbelow_regime_map.json` |
| 3 | `(R) 4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0` on the region | **certified** at `J` = 7, 9, 12, 16, 20, 25-32, 35, 40, 50 | `repair_certificate_j*.json` |
| 4 | (1) + (3) + one grouping ⇒ `N(y) > 0` on `y >= 0` | **proof** (quadratic with nonpositive discriminant) | `FARBELOW_NEGATIVE_PATTERN.md` |
| 5 | The conclusion, tested against the object rather than its parts | 252 points each at `j = 9, 11, 13`, 0 non-positive | `farbelow_endtoend_j*.json` |

**Net:** the far-below region is closed at `j = 9..16` by manifest positivity plus
one grouping — depths that previously needed the interval-Bernstein route.

## The road to depth-uniformity

| # | statement | status | artefact |
|---|---|---|---|
| 6 | leading obstruction of (R) is `J`-uniform ⟸ Newton-excess lemma + an elementary inequality | reduction, exact | `FARBELOW_NEGATIVE_PATTERN.md` |
| 7 | the elementary inequality | **PROVED**, two independent proofs | `elementary_half_check.json` |
| 8 | Newton-excess lemma, asymptotic half: `f(theta) < 2` on `(0,1/2)` | **PROVED** (external proof, one step repaired here) | `LIMIT_SHAPE_BOUND.md` |
| 9 | finite-`n` half reduces to (B) + (C) + two numbers | reduction, with the exact recursion `e_t(n+2) = e_t(n) + 2n^2 e_{t-1} + n^4 e_{t-2}` verified | `FINITE_N_BRIDGE.md` |
| 10 | (B) ratio-log-concavity | **PROVED for every `t <= 100`**, hence for the whole needed range at `n <= 200` | `conjecture_B_rungs.json` |
| 11 | (B) uniformly in `t` | **open** — one statement: `P_t(m + 2t)` has nonnegative coefficients for every `t >= 3` | same |
| 12 | (C) parity monotonicity | **open**, and shown NOT locally derivable (three synthetic tests) | `FINITE_N_BRIDGE.md` |

## Structure found along the way

| statement | status |
|---|---|
| the `b`-multiset is doubled: `prod (u - b_k)` is a perfect square, `E_{2t}` a self-convolution | **proved** (one line), and new to this repository |
| the transform of the B-form is the Schur–Szegő composition (Szegő 1922, Walsh 1922) | identified exactly, novelty of the technique KNOWN |
| squares of an AP have a Gamma-ratio generating function | verified exactly |

## What was withdrawn today

* the depth law `j <= n/2+1` — fitted on multiples of four, fails 70 of 90 (ERR-0017);
* "odd-`j` knives never dip" — they do, 72 cases (ERR-0016);
* "criterion S" — its hypothesis contained its conclusion (ERR-0015);
* my explanation of the half-depth boundaries by doubling — refuted by its own control;
* "the dominant term wins" — the rest exceeds it by 3 to 3.2e8;
* the claim that the in-regime certificate never fails — it fails from `J = 31`,
  where one Bernstein step is needed.

## Closed routes, with numbers

Fujiwara/Cauchy root bounds (2.8-49 against a needed `<1`); Grace–Szegő–Walsh
product of extreme zeros (2-7.7); the finite-free real-rootedness route
(`q` has complex zeros in 336 of 336 cases); the simple generalisation of the
repair past its regime (needs margin 4, has 1.96).
