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

## 3. What the pass produced instead: CRITERION S

Failing the real-rootedness route, the same reduced polynomial admits a
different exact test. Write the reduced composition as `P(x) = SUM_{t=0}^{r}
(-1)^t c_t e_t(b) x^{r-t}`, leading coefficient `+1`, and expand at `x = 1`:

    P(1+y) = SUM_{m=0}^{r} A_m y^m,   A_m = SUM_t (-1)^t C(r-t, m) c_t e_t(b),
    A_0 = K_r.

**CRITERION S: if every `A_m > 0` then `K_r > 0`.** Proof: all `A_m > 0` makes
`P(1+y) > 0` for `y >= 0`, so `P` has no real zero in `[1, inf)`; a real
polynomial with no zero on a ray keeps its sign there, and at `+inf` that sign
is `+`; hence `P(1) = K_r > 0`. (Descartes' rule of signs applied to the shift.
Everything is evaluated in exact `fmpq`.)

`S` is one-sided — sufficient, not necessary — and the technique is itself
classical (Descartes; Pólya's Positivstellensatz; certificates of positivity in
the Bernstein basis). Its interest is entirely empirical, and the measurement is
strong:

| | tested | criterion S fired |
|---|---|---|
| n = 6 | 102 | 102 |
| n = 12 | 306 | 306 |
| n = 20 | 578 | 578 |
| n = 28 | 850 | 850 |
| n = 40 | 1258 | 1258 |
| **total below the shore** | **3094** | **3094** |

over `lam` in {1/10, 1/2, 1, 5/2, 7, 30, 300}, `D/T_hat` in {1/4, 1/2, 9/10,
99/100, 1}, and **every** depth `3 <= j <= n-1`. Negative control, far above the
shore (`D = 40 T_hat`, `n` = 6, 12, 20): 26 negative knives seen, criterion
fired on **0** of them.

Put beside the two proved theorems, which are corners:

| route | status | region |
|---|---|---|
| Leibniz + Newton (Thm 6) | proved | `lam ~> 3 n^2` |
| J-form bound (Thm 9) | proved | `lam ~> 32 n` |
| Hausdorff corner | measured | `lam ~> 2n`, `j <= n/2+1` |
| **Criterion S** | **measured, no failure yet** | **every point tested below the shore** |

**This is a measurement and nothing more.** No `A_m > 0` has been proved for any
`m > 0`, `n <= 40` is not all `n`, and a criterion that has not failed on 3094
points is not a theorem — this repository has killed statements that survived
larger sweeps (ERR-0013 killed a statement that had certified at three depths).
What it is: the first candidate all-depths criterion in the programme whose
tested region is not a corner, and the obvious next target — prove `A_m > 0` by
downward induction from `A_r = 1`.

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
