# The literature pass on the B-form: the transform is classical, and what that leaves

2026-08-29. Requested because `BFORM_POSITIVITY_THEOREM.md` §7 said, in its own
words, that no literature pass had been done and that nothing there should be
called new until someone had actually looked. Someone has now looked.

Machine checks: `lab/ffp_convolution_check.py` -> `results/ffp_convolution_check.json`.
Sources: `evidence/keystone_prior_art.jsonl` (records `EV-KEYSTONE-2309.10970`,
`EV-KEYSTONE-2404.11479`), papers under `evidence/papers/`.

## 1. The finding: our transform is the Schur–Szegő composition

Martinez-Finkelshtein, Morales and Perales define, for two degree-`n`
polynomials written as `p(x) = SUM_i x^{n-i} (-1)^i e_i(p)`, the finite free
multiplicative convolution

    [p BOX_n q](x) := SUM_k x^{n-k} (-1)^k C(n,k)^{-1} e_k(p) e_k(q)

(arXiv:2309.10970, §1, the display defining `\boxplus_n` and `\boxtimes_n`;
LaTeX source line 272, sha256 `eb42ce…`). In the same paragraph, four lines
above, they record what it is classically called:

> "the multiplicative $\boxtimes_n$ (also known as Schur--Szegő composition)"

Our B-form (`BFORM_POSITIVITY_THEOREM.md` Thm 1) multiplies `e_t(b)` by the
Pochhammer ratio `c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t]`. Setting `N = n-1`,
`p = PROD_k (x - b_k)` and `e_t(q) := C(N,t) c_t = (r)_t (H-r)_t/[t! (n-3/2)_t]`,
the definition above gives `e_t(p BOX_N q) = c_t e_t(b)` and therefore

    K_r = (p BOX_N q)(1).                                                  (*)

So the knife is the value at `x = 1` of a Schur–Szegő composition of an
explicit real-rooted `p` with an explicit hypergeometric `q`. **Checked, not
assumed:** 336 cases (`n` = 4..20, `j` = 3..8, `lam` = 1, 5/2, 7, 30, four
values of `D` each), **0 sign mismatches** against the reference engine, of
which **65 points have a NEGATIVE reference knife**, so the check is not
vacuous.

**Consequence for the claim state.** The novelty wording in
`BFORM_POSITIVITY_THEOREM.md` §7 was POSSIBLY_KNOWN for the technique. That is
now too generous: the operation is classical, named, and a century old
(Schur–Szegő; the preservation results below are Szegő 1922 and Walsh 1922).
The correct status is **KNOWN for the transform**. Nothing in §1, §4 or §4b of
that file may be described as a new operation. What remains specific to this
project is the identification — that this particular physics object, the CHR
knife, is such a composition with these explicit `p` and `q` — and the two
region theorems proved for it.

## 2. The corollary we hoped for does not apply, and this is now measured

The reason to care about (*) was Proposition (Szegő, Walsh) in the same paper
(`\label{prop:realrootedness}`, source lines 711-719):

> "(ii) $p\in \P_n(\rr),\ q\in \P_n(\rr_{\geq 0}) \Rightarrow p\boxtimes_n q\in \P(\rr)$.
> (iii) $p,q\in \P_n(\rr_{\geq 0}) \Rightarrow p\boxtimes_n q\in \P(\rr_{\geq 0})$."

If `q` had only real nonnegative roots, then `p BOX_N q` would too, and knife
positivity would reduce to the single statement `theta_max(p BOX_N q) < 1` —
with nothing thrown away, unlike Theorem 9, whose loss §6c of that file proves
no constant can repair.

**It does not: `q` has genuinely complex zeros in 336 of 336 cases.** The
refutation is rigorous, not numerical: the `arb` enclosure of the imaginary
part excludes 0. At `n = 12`, `j = 6`, `lam = 7`, `D = 30` the five zeros of the
reduced `q` are

    3.7358,   3.2986 +/- 1.3805 i,   2.0954 +/- 2.2525 i.

Consistently, `p BOX_N q` itself is real-rooted in only 93 of the 336 cases.
That is exactly the *exclusion* direction the same authors use (their
contrapositive of (ii), source line 1759): a non-real-rooted composition with a
real-rooted factor proves the other factor is not real-rooted.

So the finite-free-probability route to knife positivity **closes**, and it
closes for a stated reason rather than for lack of effort. The critic's reading
in `BFORM_CRITIQUE.md` — that the genre is Pólya–Schur multiplier sequences — is
confirmed as the right genre by the paper's own remark that `BOX_n` "can also be
considered in the framework of finite multiplier sequences", and is confirmed as
insufficient here by the measurement: our multiplier is not one of the
zero-preserving ones.

## 3. What the pass produced instead: the diagonal identity

**Read the correction first: `docs/ERRATA.md` ERR-0015.** This section first
claimed a positivity CRITERION, and that claim was circular. What is true is an
identity, and it is more useful than the thing I thought I had.

Write the reduced composition as `P(x) = SUM_{t=0}^{r} (-1)^t c_t e_t(b) x^{r-t}`
and expand at `x = 1`:

    P(1+y) = SUM_{m=0}^{r} A_m y^m,   A_m = SUM_t (-1)^t C(r-t, m) c_t e_t(b).

**The identity.** Using `(r)_t (r-t)_m = (r)_m (r-m)_t`,

    A_m = C(r,m) * K_{r-m}  evaluated at  H -> H - m,  i.e. at  D -> D - 2m.

Verified exactly in the artefact: **1696 checks, 0 mismatches**. So the Taylor coefficients of
the knife polynomial at `x = 1` are themselves knives — of lower depth, at lower
dimension, walking the diagonal `(j, D) -> (j-m, D-2m)`.

**Why the criterion reading was worthless.** `A_0 = P(1) = K_r`. "All `A_m > 0`
implies `K_r > 0`" is true and empty: the hypothesis contains the conclusion.
ERR-0015.

**What the sweep therefore measured.** Not a criterion firing, but the whole
diagonal staircase being positive: 3094 of 3094 points below the shore
(`n` = 6, 12, 20, 28, 40, every depth `3 <= j <= n-1`, `lam` in {1/10, 1/2, 1,
5/2, 7, 30, 300}, `D/T_hat` in {1/4, 1/2, 9/10, 99/100, 1}), and, above the
shore at `D = 40 T_hat`, 26 negative knives with the staircase intact in 0 of
them. That is a real fact about the family; it is just not the fact I announced.

**The direction that is not circular.** By Descartes, all `A_m > 0` is
equivalent to `P` having no real zero in `[1, inf)`. Read forwards that is
circular; read backwards it is not:

    theta_max(p BOX_N q) < 1   ==>   K_{r-m}(D - 2m) > 0 for every m = 0..r,

i.e. a single root-location bound on a Schur–Szegő composition delivers the
entire diagonal at once, without knowing any knife value in advance. Bounding
the largest root of a finite free multiplicative convolution is a studied
problem — it is what Marcus, Spielman and Srivastava used the `S`-transform for.
That is the live route out of this pass.

## 3b. How much room a root bound has, and one dead end already measured

If the live route is `theta_max(p BOX_N q) < 1`, the first question is how sharp
such a bound must be. Measured exactly (`lab/root_margin_scan.py` ->
`results/root_margin_scan.json`): for each `(n, r, lam)` at the shore, the
smallest `c` for which the exact Descartes test certifies **no real zero in
[c, inf)** — so `c*` is a certified upper bound on the largest real root, and
`1 - c*` is the room a bound may waste.

| `lam` \ `n` | 6 | 12 | 20 | 28 | 40 | 60 | 80 |
|---|---|---|---|---|---|---|---|
| 1 | .111 | .061 | .053 | .045 | .036 | .031 | .029 |
| 5/2 | .034 | .048 | .051 | .049 | .062 | .044 | .032 |
| 7 | .110 | .012 | .040 | .045 | .065 | .055 | .042 |
| 30 | .580 | .317 | .142 | .061 | .012 | .005 | .025 |

(worst over the depths tested; 36 rows, **0 depths left uncertified**.)

The room is small but it does **not** close: log-log slopes in `n` are `-0.44`
at `lam = 1` and essentially flat (`-0.04`, `+0.04`) at `lam = 5/2` and `7`. So a
bound has a few percent of slack, roughly uniformly in `n` — a far better
situation than Theorem 9, where §6c of `BFORM_POSITIVITY_THEOREM.md` proves no
constant can help at all. Caveat stated rather than buried: for `n > 28` only
five depths per `(n, lam)` are tested, so these worst-case margins may be
optimistic.

**Dead end, measured, do not retry.** Classical coefficient-magnitude root
bounds cannot deliver this. At the shore, Fujiwara `2 max_t (c_t e_t)^{1/t}` and
Cauchy `1 + max_t c_t e_t` — both need to be `< 1` — come out at 2.8 to 49 and
up to `1.4e7` respectively (`n` = 6..40, `lam` = 1, 7, 300). They ignore the
cancellation, and the cancellation IS the phenomenon: the same reason the
Bernstein route jammed at odd depth (`ODD_DEPTH_DIAGNOSIS.md`) and the same
reason Theorem 5's Newton step cannot be sharpened. Any usable bound must use the
structure of the composition, not the sizes of its coefficients.

## 3c. The reformulation, and how tight it is

`lab/root_crossing_probe.py` -> `results/root_crossing_probe.json`.

Since `A_m = C(r,m) K_{r-m}(D-2m)` and every knife decreases in `D` (the
programme's step (c)), the staircase can only switch off once as `D` grows:
measured, **0 monotonicity violations in 1920 steps**. So there is a single
crossing `D_cross(n, r, lam)` where the composition's largest real zero passes 1,
and the physical statement becomes one scalar inequality:

    every knife positive below the shore   <==>   D_cross >= T_hat.

**Measured: `D_cross / T_hat >= 1` in 120 of 120 rows** (`n` = 6..60, three
depths each, `lam` = 1, 5/2, 7, 30, 300), and the worst case is **1.008** at
`n = 60`, `r = 2`, `lam = 30`. Descartes is sufficient-only, so each ratio is a
LOWER bound on the truth — the safe direction.

**What that costs any future proof.** The reformulation is exact and it is
*tight*: at the worst tested point the crossing sits 0.8% above the shore. Any
argument that gives away a constant factor — the Grace–Szegő–Walsh product of
extreme zeros gives 2 to 7.7 where under 1 is needed, Fujiwara and Cauchy give
2.8 to 49 — cannot close it, and those three are now measured dead ends rather
than guesses. This is the same shape as §6c of `BFORM_POSITIVITY_THEOREM.md`, and
knowing it *before* spending a week on a bound is the point of measuring it
first.

## 4. Claim-state changes this pass forces

- `BFORM_POSITIVITY_THEOREM.md` §7: novelty of the transform
  POSSIBLY_KNOWN -> **KNOWN** (Schur–Szegő composition; Szegő 1922, Walsh 1922
  for the preservation theorems). Done in that file.
- The mathematics of Theorems 1-9 is unaffected: the validator pass
  (`validation/VAL-BFORM-0001.yaml`) checked identities and inequalities, none of
  which this pass touches.
- The framing appears absent from the HEP literature: INSPIRE title searches for
  `Schur-Szego composition` and for `finite free convolution` return **0**
  records (2026-08-29), while the control query `t unitarity of string
  amplitudes` returns the expected 2, including Arkani-Hamed–Eberhardt–Huang et
  al., arXiv:2201.11575, which is already in our evidence ledger. A title search
  is weak evidence of absence and is recorded as such.
- Still NOT searched: whether the *region* results (Thm 6 / Thm 9 thresholds for
  this family) have an analogue in the amplitude literature — that needs a
  full-text pass over the partial-wave-positivity papers, not a title query.
