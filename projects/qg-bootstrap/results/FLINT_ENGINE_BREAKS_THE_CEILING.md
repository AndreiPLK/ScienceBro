# The depth ceiling was a Python loop, and it is gone

*2026-08-30 evening. Module: `lab/leg_a_flint.py`, engine: `lab/q3_mpoly.py`.*

## What was actually limiting the theorem

Leg (a) is certified per depth, and the depth reached was `j = 18` at 3.7 hours per depth.
That was never a mathematical limit. `prover2_core.QPoly` stores a multivariate polynomial
as a Python dict and multiplies it with Python loops; flint has the same object in C.

Measured on the products this programme performs:

| terms | dict `QPoly` | flint `fmpq_mpoly` | speedup |
|---|---|---|---|
| 1500 | 1.60 s | 0.003 s | 533x |
| 4000 | 12.44 s | 0.017 s | 731x |
| 9000 | 70.18 s | 0.057 s | 1231x |

The repository's own fast-engine law says exactly this — new computational code goes on
flint immediately. The prover core predates the law.

## The rebuild, and its validation

`q3_mpoly.py` carries `a + b sqrt3` as a pair of native `fmpq_mpoly`. Its `sign_q3` agrees
with `prover2_core` on 20000 random pairs, including the delicate opposite-sign case.

`leg_a_flint.py` recomputes leg (a) with the same verified formula, plus the two structural
facts found earlier today (the `A_r` arithmetic progression, and hoisting the `i`-only
factors). Validated against the **published artefacts of the old engine**, not against
itself:

| `j` | old result | old time | new result | new time | speedup |
|---|---|---|---|---|---|
| 9 | `{7: 11}` | 64 s | `{7: 11}` | 0.9 s | 71x |
| 12 | `{10: 71}` | 428 s | `{10: 71}` | 6.6 s | 65x |
| 14 | `{12: 130}` | — | `{12: 130}` | 17 s | — |
| 16 | `{14: 205}` | — | `{14: 205}` | 39 s | — |
| 18 | `{16: 351}` | 13287 s | `{16: 351}` | 79 s | **168x** |

Identical numbers everywhere.

## What the new reach found

**`j = 20`: leg (a) holds**, negatives only at `k = J-2 = 18`, 526 of them. A new depth.

**`j = 22`: the monomial certificate FAILS** — negatives appear at `k = 18 = J-4`, 85 of
them, outside the excluded set `{J-2, J-3}`. A shift into the regime helps only slowly
(85 at offset 0, 83 at offset 4).

## Why that is a certificate failure and not a mathematical one

The exact point evaluation over `Q(sqrt3)` (`lemma_a_exact.py`) shows `c_k >= 0` for every
`k` outside `{J-2, J-3}` at **every point tested up to `J = 36`**, 15876 checks, zero
failures. So at `j = 22` the coefficient `c_{J-4}` is nonnegative in value while some of its
MONOMIALS are negative.

That is exactly the situation that produced the repair (R) at `k = J-2`: manifest positivity
stops being available before positivity stops being true. The same three remedies apply — a
larger shift, a Bernstein step, or a grouping with neighbours.

## Status

* **Leg (a) certified**: `j = 9..20`, up from 18, and now minutes per depth instead of hours.
* **Open at `j >= 22`**: the certificate needs the same kind of repair at `k = J-4` that (R)
  supplies at `k = J-2`. Large shifts are being tried.
* **Not in doubt**: the coefficient itself, which is nonnegative at every point tested to
  `j = 36`.


## And the `j = 22` failure is repaired by the established remedy

The monomial certificate fails at `j = 22`, `k = J-4`, with 85 negative monomials. A shift
into the regime removes them only slowly: 85, 83, 74, 64, 42 at offsets 0, 4, 24, 48, 96 —
converging, but expensively.

**One Bernstein step in `thL` certifies it outright**: 29099 coefficients, zero negative.
That is exactly the escalation the repair certificate already uses for `(R)` from `J = 31`,
and the same variable — `thL` is the only bounded one.

So the pattern for leg (a) matches the pattern for `(R)`: manifest monomial signs suffice up
to some depth, and beyond it one change of basis does. **Leg (a) is certified at `j = 22`.**

| depth | how leg (a) is certified |
|---|---|
| 9 – 20 | monomial signs |
| 22 | one Bernstein step in `thL` at `k = J-4` |

## Status after the evening

* **Leg (a) certified `j = 9..22`**, up from 18 this morning.
* **Time per depth**: 79 s at `j = 18` against 3.7 hours, 310 s at `j = 22`.
* The remedy is not new machinery; it is the one `(R)` already uses.


## A trap that caught four runs today, now closed in the module

Pushing to `j = 24, 26, 28` produced a new-looking failure family: negative monomials at the
LOW ODD indices `k = 1, 3, 5, 7`, growing with the depth, and Bernstein did not clear them.

Every one of those runs had `v_offset = 0`, so `n` started at 44 — while the regime
`n >= 2J-3` needs 45, 49 and 53 respectively. **They were computed outside the region where
leg (a) is claimed at all.**

That is the fourth time today a result came from outside the stated domain: the difference
window past the midpoint, `k = J-3` in Lemma A, `n < 2J-3` in the exact point check, and now
this. Three of the four looked like refutations.

The module now **defaults `V_OFFSET` to the regime edge** `max(0, 2J-3-44)` and records both
the offset used and whether it is inside the regime, so the mistake cannot be made silently
again. Passing `V_OFFSET` still overrides, deliberately.

The two families of failure remain worth separating:

* **near `J-2`** — `k = J-4`, `J-6`, `J-8` — cleared by one Bernstein step in `thL`
  (certified at `j = 22, 24, 26, 28`);
* **low odd `k`** — appeared only outside the regime, and is being rechecked inside it.
