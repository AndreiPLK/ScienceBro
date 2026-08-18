# Depth 3, status

Same pipeline that closed depth 2 (docs: `D2_COMPLETE.md`), one level deeper.

## Proved (Bernstein certificates, both verified against the exact engine first)

* Elementary symmetric functions e_0..e_3(N) derived from power sums via
  Newton's identity, each power sum checked against direct summation on
  held-out points before being trusted. e_2 reproduces the hand-derived
  depth-2 E2 exactly.
* The depth-3 beta-mean formula (cubic in gamma) matches the exact reference
  engine (`jacobi_coeff_rec`) on 120 trials (n=8..30, various lam, D):
  0 mismatches (`lab/depth3_proof.py`).
* Parity-split, half-level-K argument (same fix as ERR-0008 for depth 2:
  `M=K` an actual integer, so `T_hat<=T_K` by definition) verified 70/70
  against the exact engine at concrete `(K,c)` points, THEN Bernstein-proved:

  ```
  [even] K>=3 (n>=6), 0<=c<=50:      proved, 1 box, 0 open
  [even] K>=3 (n>=6), c>=1:          proved, 1 box, 0 open   (compactified)
  [odd]  K>=3 (n>=7), 0<=c<=50:      proved, 1 box, 0 open
  [odd]  K>=3 (n>=7), c>=1:          proved, 1 box, 0 open   (compactified)
  ```

  The two pieces overlap on `[1,50]`, so together they cover **all c >= 0** --
  no separate "Half A" algebraic argument was needed (unlike depth 2): this
  Bernstein run reaches arbitrarily large lam directly. So **depth 3 is fully
  proved for n >= 6 (even) / n >= 7 (odd), every lam > 0.**

  `lab/depth3_parity_proof.py`

## Checked but NOT proved (dense grid, correct shore formula, zero failures)

* n = 6..40, lam = 5..500: zero failures (redundant with the proof above for
  n>=6/7, kept as an independent check).
* **n = 5, 6, 7** (below the K>=3 floor for at least one parity): dense grid,
  lam from 0.001 to 100, at the true shore and just below it (three fractions
  near 1): **zero failures.** This is evidence, not a continuum proof -- the
  fixed-N single-variable Bernstein extension (mirroring depth 2's direct
  n=3,4 treatment) was attempted and hit a bug in the verification script
  itself under time pressure; not resolved tonight, left for next session.
* n = 3, 4: depth-3 knife (j=4) does not exist for these n (`j <= n-1` fails).

## Honest gap

The rigorous, continuum-covering result is for **n >= 6 (even) / n >= 7
(odd)**. n = 5, 6, 7 have strong evidence (dense grid, zero failures) but not
a machine-checked proof for the full continuum of lam. Closing this is
mechanical (same method as depth 2's n=3,4 direct treatment) and is the next
concrete task.

## Lesson carried over from tonight (ERR-0009)

Every comparison against the exact engine in this file uses
`gamma = (D-3)/2` / `D = 2*gamma+3` applied consistently -- the exact
off-by-a-constant shape that produced ERR-0009's false alarm was checked for
explicitly before any result here was trusted.

## Small-n (n=5,6,7) closure attempted again, same failure mode found

Second attempt (fixed N, K forced to 3, single-variable-in-c polynomial)
disagrees with the exact engine at moderate-to-large c for all of n=5,6,7 --
same symptom as the first attempt earlier tonight.

FIRST HYPOTHESIS TESTED AND REFUTED: checked whether Qg or any cleared
denominator factor goes negative at the failing point (n=5, c=5) -- all of
them are positive (Qg=6, all den_cleared factors around 4356-4368). So the
sign-flip-from-clearing-a-negative-denominator theory is WRONG, at least at
this point. The actual cause is still unknown.

Not fixed tonight. Next session: since the K-parametrized (parity, N=2K or
N=2K+1) construction is independently verified correct (70/70 against the
exact engine, plus the depth_d_proof.py generic version also 56/56 for
d=2..5), while this SEPARATE "fixed N, independent K" construction fails --
the bug is likely in how this second, differently-structured construction
diverges from the first, not in the shared homogenization math. Compare the
two code paths term-by-term at the failing point rather than guessing again.
