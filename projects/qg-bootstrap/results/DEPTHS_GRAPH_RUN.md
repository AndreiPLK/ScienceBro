# Depths 3-6 of the unglued keystone: run status, honestly

Date: 2026-08-19. Repo HEAD at report time: `c31fa77`; the certificate runs
below were launched at `f5cf686`.
Prover under test: `lab/keystone_unglued.py` (four Bernstein pieces per parity:
`lo` 5/12 <= c <= 50, `hi` c >= 50, `wedge` c < 5/12, `small` lam <= 5/2).
Each depth was run by one agent and then independently checked by a second
agent that wrote its own reference engine and did **not** re-run the prover's
command.

## HEADLINE: the verifiers disagree with the prover, and they are right

**No depth is proved. Not 3, not 4, not 5, not 6 - and depth 2's "fully
proved" claim must be retracted too.**

Four independent verifications, written separately, all landed on the same
defect: **`build_wedge` (lab/keystone_unglued.py, lines ~497-531) builds the
wrong polynomial.** It is not the depth-d knife at `D = T_v(lam)`, and it is
not a positive rescaling of it either, at *any* depth 2-6. Therefore every
`wedge_proved: true, boxes: 1, open: 0` on disk - including depth 2's and
depth 4's - is a true Bernstein statement about an object that is not the
knife. The region `c < 5/12` (large N at moderate lambda) is **not covered at
any depth.**

Two named defects, agreed on by the verifiers independently:

1. Line 520, `lam = cN  # this is c*lam_true`. The comment is false: in wedge
   coordinates `K = 5/(4c) + z` we have `cN = c*N = lam_true` exactly, so `lam`
   carries **zero** extra powers of c. Lines 524-531 nevertheless homogenize
   `B`, `kk2`, `Qg`, `Pg` as if it carried one.
2. Line 530, `- kk2*fmpq(3)*c*c` carries two powers of c where Pg's degree-2
   term needs one. `L[i] = two_m_Qg + Pg + Qg*c*(1+i)` is inhomogeneous for the
   same reason (`Pg` needs the matching `c`).

Consequences measured, not inferred:

- The sign error is **parity-in-d**: it flips the overall sign at odd d and
  hides at even d. Measured sign(wedge) vs sign(branch) at identical physical
  points: d=2 agree, d=3 DISAGREE, d=4 agree, d=5 DISAGREE. Depth 2 - the depth
  declared closed - is one of the depths where the bug is invisible.
- At depth 3 the wedge polynomial is **uniformly negative** over its own
  certification box (125/125 sampled points negative, both parities), which is
  exactly why it never converged: `open == 2^max_depth` at max_depth 0/4/8/12
  (1/16/256/4096). Not one leaf ever turned positive. No amount of compute
  would have closed it.
- The **correctly** homogenized wedge is divisible by `c^(2d)`, so it vanishes
  identically on the `c = 0` face and cannot close as written either; the
  mis-homogenized version has min c-exponent 0, is positive on the root
  Bernstein grid, and hence looked *trivially easy* at "1 box". The bug is what
  made the piece look cheap.

**Why it survived:** `self_check` (line 272) builds and tests **only**
`build_branch`. `build_wedge` and `build_small_lam` are never compared against
the reference engine anywhere in the repo. `results/UNGLUED_KEYSTONE.md`
line ~112 claims "36 trials for the wedge"; `grep build_wedge` returns only its
definition and its single call site, so that claimed evidence does not exist in
the code. This is the third recurrence of the ERR-0010/ERR-0011 pattern.

**And the self-check itself is mis-specified.** It sets `lam = fmpq(c_num,
c_den)` (that is c), feeds it into `H.eval_at` as slot 1 = c correctly, and then
hands the *same* number to `jacobi_coeff_rec` as the physical lambda - while
`build_branch` internally uses `lam = c*N`. It compares the polynomial at
lam = c*N against the reference at lam = c. It reports 0 mismatches only
because both signs are +1 inside the window. Its trial count is also inflated:
the `k_s <= 3` guard silently skips part of the grid, so "320 trials" is
192 comparisons at depth 4 and 180 at depth 6 - of the wrong point. With the
correct lam = c*N the branch does pass (independently, 916-1561 trials, 0
mismatches, including genuinely negative reference points), so nothing is
currently hidden in the branch - but the repo's own check is not evidence of
that.

## Status table

| depth | prover verdict | prover seconds | verifier | trials | mismatches | FINAL status | precisely why |
|---|---|---|---|---|---|---|---|
| 2 | (earlier run) PROVED, 2211/1/1/3 boxes, 0 open | 21.1 | disagrees (found by the d3/d4/d5/d6 verifiers) | see note | wedge invalid at d=2 | **not proved** | `lo`/`hi`/`small` verified clean; the `wedge` quarter certifies the wrong polynomial, so `c < 5/12` is uncovered. The "closed for every lam > 0" claim is **retracted**. |
| 3 | **TIMEOUT** (killed at the 2400 s cap, exit 124) | 2403 | disagrees | 3145 | 770 | **not proved** | Two independent failures: (a) `lo` genuinely did not finish - only the self-check line ever printed, zero of 8 piece verdicts; (b) `wedge` is uniformly negative (770 mismatches, 432/432 in-window = 100%), so it could never have closed. Nothing persisted to `keystone_unglued.json`. |
| 4 | PROVED, 8/8 pieces True, 0 open, exit 0 | 313.3 | disagrees | 5367 | 30 | **not proved** | `lo` (1369b), `hi` (1b), `small` (3b/1b) verified clean (916 branch + 420 small trials, 0 mismatches, negative controls tracked). The `wedge` "1 box, 0 open" certifies the wrong polynomial. Witness: K=25, c=1/4, z=20, v=5 -> repo wedge sign +1, exact knife -1. All 30 mismatches lie outside v in [8/5,2], so no counterexample to the physics; the certificate, not the statement, is broken. |
| 5 | **TIMEOUT** (2400 s cap, exit 124) | 2400 | disagrees | 502 | 148 | **not proved** | Only the self-check line printed. Zero of 8 piece verdicts; still inside even parity, had not finished `lo`. Ran at ~0.48 core under 5 sibling jobs, so the 2400 s wall is not 2400 s of dedicated CPU. Also `wedge` 148/152 mismatches - it would have proved the wrong statement even had it finished. |
| 6 | **TIMEOUT** (2400 s cap, exit 124) | 2400 | disagrees | 4639 | 256 | **not proved** | Even parity printed True for all four pieces (lo 937b, hi 1b, wedge 1b, small 3b, 1140 s) but **odd parity produced no output at all** - 0 of 4 odd pieces certified. `_write()` runs only after `run_depth` returns, so **nothing for depth 6 is persisted**; the even numbers exist only as console text and the per-piece open-box counts were never written anywhere. Also `wedge` invalid: its internal gamma differs from the true gamma at 128/128 points. |

Verifier trial/mismatch columns are that verifier's own harness against its own
reference `D = T_k(lam)`, not the prover's `self_check`. Every verifier ran the
ERR-0009 cross-check (`T` against the repo's `Pg/Qg` route) and it was clean;
flint `fmpq` only, no float in any exact comparison. Each harness was validated
at depth 2 first, so "0 mismatches" on the good pieces is not vacuous - the
branch checks tracked 9 to 83 genuinely **negative** reference signs.

`results/keystone_unglued.json` contains records for depths **[2, 4] only**. No
depth 3, 5 or 6 record exists. The depth-4 record was written under a
read-modify-write race between four concurrent runs of the same script and is
not durable.

## The good news, also measured

The knife itself is not in trouble. Inside the certified window
(v in [8/5,2], c <= 5/12, K >= 3) a 1196-trial wedge scan found **0 negative
knives and 0 mismatches**; an 88074-point scan of the wedge box found the
buggy gamma *larger* than the true gamma at 88071 points. All 30/148/256
sign failures sit at v outside [8/5,2]. What is broken is the certificate.

And the fix is written and already validated by two verifiers independently:

- **Route A** (algebraic): remove the spurious c's from `B`, `kk2`, `Qg`, `Pg`
  and give `L[i]` the matching single c. Then, as dicts of `fmpq` coefficients,
  `c^(degK-4d) * W_fixed == c^degK * build_branch(K -> 5/(4c)+z, c, v)`
  **exactly** (checked True for both parities at d=2 and d=6; the same identity
  is False for the current wedge). 0 mismatches at depths 2, 3, 4, 5.
- **Route B** (substitution): `Wcorrect = SUM_a (5+4cz)^a (4c)^(A-a) P_a(c,v)`
  where `H = SUM_a K^a P_a(c,v)`, `A = deg_K H`. 0 mismatches at depths 2-5.
- With the positive factor `c^(2d)` divided out, the corrected wedge **actually
  certifies**: d=2 even/odd proved=True, 1 box, 0 open (4 s each);
  d=4 even True 1 box 0 open (125 s), d=4 odd True 1 box 0 open (159 s).
  Both measured, not estimated.

## What remains open

1. `build_wedge` must be fixed and depths 2 and 4 **re-run** before either can
   be called proved. The fix closes the wedge at d=2 and d=4 as measured above,
   but the *other three* pieces at those depths must be re-certified in the same
   run for the record to be a certificate rather than four separate claims.
2. `self_check` must be corrected (lam = c*N, k_s = v*c*N), extended to cover
   `build_wedge` and `build_small_lam`, made to report its **actual** number of
   comparisons, and pushed **outside** v in [8/5,2] - where every reference sign
   is +1, a sign check cannot distinguish the intended polynomial from any other
   positive one.
3. Depth 3's `lo` is a genuine open timeout. Its polynomial is positive at all
   455 swept points per parity and its sign matches the engine, so there is no
   known obstruction - but that is not a proof. Depths 5 and 6 `lo` likewise.
   Depth 6 needs roughly 2x the wall it was given, or a solo run.
4. **Coverage is overstated.** Every compactified axis stops at t = 999/1000,
   not 1: `K = 3/(1-t)` covers K <= 3000 (N <= 6000), not "all K >= 3";
   `c = 50/(1-t)` covers c <= 50000; `z = t/(1-t)` covers z <= 999. Pushing the
   `lo` box to t = 1 does not close (d=2: 9807 boxes, 1813 open at max_depth 30,
   both parities), although the K = infinity face is positive on an 861-point
   grid. So this looks like a Bernstein resolution issue rather than a sign
   change - and it is still uncovered.
5. Cost is **not monotone in d**: depth 4 closed in 313 s while depth 3 did not
   finish in 2400 s, and depth 4's `lo` needed 1369 boxes against depth 2's
   2211. Polynomial size grows smoothly ((K,c,v) degrees exactly (6d,4d,3d)),
   so the depth-3 stall is a pathology of depth 3's `lo` geometry, not a scaling
   wall. Unexplained.
6. Engineering: move `_write()` inside `run_depth` and print each piece as it
   completes. Depth 6 threw away 19 minutes of successful even-parity
   certification because a timeout in the second parity discards everything.
   Serialize the runs - every timing above was measured under roughly 4-6x
   contention on 16 cores, so none of them is a clean cost measurement.

## Scope caveat that applies even to a future "proved" row

All of this is **step (a)** of the unglued keystone argument: positivity of the
depth-d knife at `D = T_v(lam)`. Step (b) (integrality) and **step (c)
(monotonicity in D) are NOT certified.** Step (c) is *measured*, not proved:
0 non-monotone configurations out of 120 for lam >= 5/2, but **33 out of 96**
for lam < 5/2 (`results/UNGLUED_KEYSTONE.md`). So any row that ever reads
"proved" is proved **modulo an unproved monotonicity step** - and that matters
directly here, because the wedge's inflated gamma would only be "conservative"
if step (c) were granted, and at 3 of 88074 scanned points the wedge's gamma is
strictly *smaller* than the true one (worst shortfall 0.7003% at c=5/12, K=3,
v=8/5, lam=5/2), where no monotonicity argument could rescue it anyway.

## Provenance

Runs: `PYTHONIOENCODING=utf-8 timeout 2400 .venv/Scripts/python.exe
lab/keystone_unglued.py <d>` from `projects/qg-bootstrap`, git `f5cf686`,
python 3.12.10, flint 0.9.0, Windows-11-10.0.22631-SP0, 16 logical cores,
31.1 GB RAM (~13 GB free). 4-6 concurrent jobs throughout.
Audited: `lab/keystone_unglued.py` (`build_wedge` line 497; suspect lines 520,
524, 525, 530, 531; `self_check` line 272) and `lab/jacobi_normal_form.py`
(`jacobi_coeff_rec`, the reference). Verifier scripts live in the session
scratchpad; **nothing in the repo was modified by any of the eight agents.**
