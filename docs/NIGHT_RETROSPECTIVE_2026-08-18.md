# Retrospective, night of 17-18 August 2026

Not the results (those are in `article/NIGHT_REPORT_2026-08-17_to_18.md`) but the
WAY OF WORKING. Only what the events of that night actually demonstrated.

---

## 1. What worked

### 1.1. Every new result was checked against an already verified one

This is the only reason the night produced results rather than confident text.
The pattern is always the same: a new fast path must reproduce the slow one
EXACTLY on a grid before it is used for anything.

| new thing | checked against | cells | mismatches |
|---|---|---|---|
| Jacobi normal form | independently computed exact value | 4500 | 0 |
| Saalschutz closed form | the long sum | 432 | 0 |
| fast path (j terms) | the slow one | 891 | 0 |
| flint port | the Fraction path | 891 | 0 |
| recursive moments | the Fraction path | 891 | 0 |
| closed form per knife | the exact engine | 24 each, j = 2..6 | 0 |

Twice this caught an algebra error of mine BEFORE anything was concluded from
it: an off-by-one in two factors of `R_t`, and a stray factor `(2n-3)/(2n-5)` in
a hand simplification.

### 1.2. Predictions were stated before computing

The parity mechanism predicted that knife 6 must carry an ODD power of the
bracket. The prediction was written down, then `E_10` was derived, then the
computation ran. It matched. Without that order, an explanation is
indistinguishable from a fit to what was already seen.

### 1.3. Hypotheses were frozen to a file before the data was examined

`results/FROZEN_PREDICTION_blocks.md` was time-stamped before the block
boundaries were looked at. It was REFUTED, and that is exactly why writing it
first had value: after the fact I would have adjusted it.

### 1.4. Changing the object beat improving the instrument

Half the night went into the contour method: faster, sharper radii, better
certificates. The result did not move. The breakthrough came from changing the
OBJECT -- from the minimum on a loop to a coefficient of an expansion. The sign
that it is time to switch: the instrument keeps improving and the answer does
not.

### 1.5. The algorithm mattered more than the engine

Porting to flint gave 3x. Removing a recomputation of Pochhammer symbols gave
another 7x. Saalschutz before that gave 11.8x. Most of the ~80x total was
algorithmic. First question to ask: what am I recomputing inside a loop?

---

## 2. Errors, with their mechanism

Seven. None came from hard mathematics; all came from procedure.

| # | error | why | what now catches it |
|---|---|---|---|
| 1 | "block widths step by 6" | scanned only even j and took a grid artefact for a law | check a finer grid before the word "law" |
| 2 | claimed the ceiling interlaces with Jacobi zeros | measured at ONE value of D | vary every parameter first |
| 3 | wrote that the margin GROWS with the level | measured at ONE n; it shrinks | same |
| 4 | inverted the spin direction (ERR-0004) | did not open the definition in our own published paper | check provenance before interpreting |
| 5 | called a rederivation of our published shore a discovery | provenance not checked before the claim | same |
| 6 | off-by-one in `R_t`, stray factor in a ratio | simplified by hand and did not verify the simplification | verify each simplification step |
| 7 | domain errors: allowed D < 3, then n = 3 for a knife that needs n >= 4 | domain of definition not written down before scanning | write the domain first |

Two near-misses: almost concluded a sign from a single monomial of `A_1` (the
full coefficient has the opposite sign), and almost built on a float comparison
that died with OverflowError at n = 70.

**The common mechanism: a conclusion drawn before its basis was checked.** Not a
gap in knowledge, a gap in order.

---

## 3. What was added to the machinery, not to the promises

1. `tests/test_fast_engine.py` fails `sb check` if a new computational module
   uses the slow engine. The debt register `tests/fast_engine_debt.txt` may
   shrink, never grow.
2. `CLAUDE.md` carries the fast-engine law: what to compute with, what not to,
   and no float comparisons of exact quantities.
3. `lab/contour_lib.py` has an 8-point self-test; the scanning scripts refuse to
   run if it fails.
4. `lab/jacobi_normal_form.py` has `self_check_fast`, `self_check_flint`,
   `self_check_rec`: every fast path must equal the slow one exactly.
5. `docs/ERRATA.md` records mechanisms, not just facts.
6. `results/OPEN_PROBLEM.md` states the open problem precisely and lists the
   CLOSED routes so the next session does not walk them again.

---

## 4. The method worth repeating: compress, do not assault

```
four parameters, infinitely many constraints
  -> one polynomial per level      (normal form)
  -> one number per constraint     (orthogonality)
  -> j terms per constraint        (Saalschutz: a balanced 3F2)
  -> one bracket to the power j-1  (Newton's binomial in the scaling limit)
```

At no step was the problem solved; at every step it was made SMALLER. The
solution appeared when the object was small enough.

---

## 5. Added the next morning, and it is the most important entry

An outside reader refuted, in one minute, a lemma I had "verified" on 966
configurations (`docs/ERRATA.md`, ERR-0005). The difference was not compute:

> I searched where my grid already was. He searched where the claim was most
> likely to fail -- hard against the boundary.

My D-grid was ABSOLUTE (4 to 70) while the boundary at that lam sits at 187.5,
so every test I ran there was below 40 percent of the boundary and the
counterexample lives at 94 percent of it. Hence the standing rule now: under a
MOVING boundary, sample in fractions of that boundary and include 0.99.

And the corollary that cost the least and returned the most: **an outside check
is cheaper than a week of my own work.** Write the self-contained brief early.
