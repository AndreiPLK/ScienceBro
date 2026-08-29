# ERRATA — реестр исправлений опубликованных материалов

Правило (основатель, 2026-08-16): любая найденная ошибка в уже
опубликованном исправляется ВЕЗДЕ (репозиторий, PDF, сайт, пакет) с записью
здесь: что, где, кем найдено, когда исправлено, в каких версиях.

| ID | Дата находки | Работа | Ошибка | Найдено кем | Исправлено | Версии |
|----|--------------|--------|--------|-------------|------------|--------|
| ERR-0001 | 2026-08-16 | Paper 3 (master formula, DOI 10.5281/zenodo.21947272) | ПОДОЗРЕНИЕ: край окна "(26.2, 30.3)" — усечение внутрь | я, по мотивам W2 из ревью paper 4 | ФАНТОМ: проверка опубликованной v1.0.1 показала, что 30.4 уже стояло (правка W2 внесена ДО публикации в раунде ревью paper 3). Ошибочно выпущенный erratum-релиз v1.0.2 ОТОЗВАН (release+tag удалены) в тот же час. Урок: перед erratum сначала проверять published-версию, не локальную память | — |

Примечания:
- Zenodo-версии: новый релиз создаёт новую версию записи; concept-DOI
  остаётся, версия с ошибкой сохраняется в истории (честная наука).
- Внутренние (неопубликованные) правки нот/черновиков в реестр не входят —
  они живут в DATA_LOG и git-истории.

## ERR-0002 (2026-08-17): knife-4/5 theorems prematurely marked COMPLETE
- What: results/knife{4,5}_theorem.json claimed "COMPLETE pending adversarial
  review" while cited artifacts recorded all_certified:false, knife-5 below-
  diagonal band had no certificate at all, and lam<1/1000 was uncovered.
- Caught by: our own adversarial fleet review (36 agents), same night.
- Fix: statuses downgraded immediately (commit with this entry); repair plan
  in DATA_LOG; re-promotion only after passing per-stage artifacts exist.
- Lesson: consolidation JSONs are claims too — they go through the same gate:
  no COMPLETE without every cited artifact recording a PASS.

## ERR-0003 (2026-08-17): the shore was computed with a hard-coded k cap

**What was wrong.** lab/keystone_hunt.T_hat computed the shore as
min(T_k(k, lam) for k in range(3, 61)). The minimising k grows like
sqrt(3)*lam, so the cap silently OVERESTIMATED the shore once lam was
large: by 1.06x at lam = 60, 1.47x at lam = 150, and 5.96x at lam = 1000.

**How it was found.** While measuring how close the knives come to the
shore, a cell appeared with threshold/shore = 0.79 -- a knife apparently
cutting BELOW the shore, i.e. a counterexample to the grand theorem. Both
the Beta reduction and the ORIGINAL master formula agreed that P_j < 0
there, so it was not a reduction bug. Checking the shore itself showed the
minimum was attained at k = 60, exactly the edge of the scan window. With
the correct shore (2836.81 instead of 4174.76) that point lies ABOVE the
shore, where knives are supposed to cut. No counterexample.

**Direction of the error.** The shore was too HIGH, so every positivity
test ran on a LARGER region than required. Conclusions of the form "no
violation below the shore" therefore remain valid -- they were tested on a
superset. What was wrong were the shore NUMBERS for lam above about 34.

**Published work: NOT affected.** The release scripts compute the shore
over range(3, 400) or range(3, 3000), and
release/qg-blade-theorem/lab/bruteforce_recheck.py already used an adaptive
window min(4000, 3*lam+50). The papers define the shore correctly as the
minimum over all n >= 3 with no cap. The regression was in NEW research
code only: the old code was more careful than the new code.

**Fixed.** T_hat now scans range(3, max(61, 3*lam+60)), verified to equal
the true minimum at lam = 1, 26, 150, 1000. All keystone artifacts of
2026-08-17 regenerated. With the corrected shore the interval certificate
became CLEANER: 5616/5616 cells at bisection depth 0, where before 21 cells
had needed a bisection.

**Lesson recorded in memory.** Any minimisation over an unbounded index
must use a window that grows with the parameters, and a minimum attained at
the edge of a scan window is not a minimum -- it is a bug report.

## ERR-0004 (2026-08-18 00:20) -- spin direction inverted in tonight's "weakest knife" result

WHAT I WROTE. That the weakest constraint is "the LOWEST spin, j = 2", in
article/DATA_LOG.md, article/visuals/the_weakest_knife.py and the figure
weakest-knife.png that was sent to the founder.

WHAT IS TRUE. In this programme the trajectory index is ell = 2n - 2j with
2 <= j <= n-1 (release/qg-master-formula/paper/main.tex, line 23 and 70), so
j = 2 is the LEADING trajectory ell = 2n-4, the HIGHEST spin of the level, and
large j is low spin. The weakest knife is therefore the LEADING, highest-spin
trajectory -- not the lowest.

CONSISTENT WITH. C4 in research/inventory-of-facts.md, "low spin dominance
FAILS here", which says exactly that the binding constraint is not at low spin.
I had that fact in the repository and still wrote the opposite.

SECOND CORRECTION IN THE SAME PLACE. I called the identity B(n,lam) = T_n(lam)
a discovery. It is not: the shore paper DEFINES T_n by
a_{n,2n-4} >= 0 <=> D <= T_n(lam) (release/qg-gravity-shore/paper/main.tex,
lines 26 and 55). So what I actually did is REDERIVE the published shore from a
completely different route (Jacobi normal form + Saalschutz summation) and get it
exactly. That is an end-to-end validation of tonight's machinery against
published work, which is worth having, but it is a check and not a new result.

WHAT SURVIVES UNCHANGED. The measurements: the weakest coefficient of each level
is the one at m = n-2, and it falls exponentially with the level (2.3e-2 at
n = 10 to 2.2e-21 at n = 70, lam = 1, D = 6). Only the physical NAME of that
knife was wrong.

WHAT THIS REFRAMES. Since the j = 2 threshold IS the shore, and the j = 3 case is
the published blade theorem, the genuinely open part of the keystone is j >= 4.

## ERR-0005 (2026-08-18 11:49) -- the endpoint lemma is FALSE. Counterexample confirmed.

WHAT I CLAIMED (today, hours ago): that for n >= 14 the minimum of the sequence
C_m is always at an endpoint, so the whole knife family reduces to two cases; and
that log-concavity holds for n >= 24. I called it "the uniform statement" and
recorded it as the sharpest form of the problem.

IT IS FALSE. An outside check produced a counterexample and my own exact engine
reproduces it digit for digit:

    n = 24, lam = 10, D = 177   (the shore is 187.541, so this is admissible)
    C_m/C_0: 1.000000, 0.568188, 0.470609, ..., 0.308001, 0.305587, 0.312789, ...
    global minimum at m = 10, strictly interior
    log-concavity violated at m = 1..16, e.g. C_0 C_2 / C_1^2 = 1.4577

A second one also confirmed: n = 14, lam = 2, D = 39 (shore 39.4), interior local
minimum at m = 8.

WHY I MISSED IT -- the mechanism, which matters more than the fact. My D-grids
were ABSOLUTE: 4, 5, 7, 11, 19, 35, 70. At lam = 10 the shore is 187.5, so every
test I ran there sat below 40 percent of the shore, and the counterexample lives
at 94 percent of it. I varied D, so my own rule "vary every parameter" was
formally satisfied -- but the parameter that matters is D RELATIVE TO THE SHORE,
and on that scale I never left the deep interior at large lam. A grid that looks
wide in absolute terms can be systematically blind.

NEW RULE, added to the scientist skill: when a region has a moving boundary,
sample RELATIVE to that boundary (fractions of the shore), never on an absolute
grid.

WHAT DIES WITH IT:
* the endpoint-minimum lemma and everything built on it;
* log-concavity of C_m;
* today's saddle-point reduction "log-concavity <=> z' > 0". The machinery itself
  reproduces the exact ratios to 0.003 at n = 40, but at the counterexample it
  reports z' > 0 everywhere while log-concavity actually fails by 3 percent --
  i.e. the asymptotics does not resolve the term that decides the question. An
  asymptotic proof there would have been a proof of a false statement.

WHAT SURVIVES, and it is most of the work:
* every C_m in BOTH counterexamples is still POSITIVE -- the physics claim is
  untouched;
* the Jacobi normal form, the closed forms per knife, the Saalschutz moments, the
  scaling limit and the parity mechanism, the knife-4 box proof -- all of these
  are statements about SIGNS, and signs do not depend on the normalisation.

ALSO CORRECTED, from the same outside check:
* My C_m are RAW integrals, not Jacobi expansion coefficients: the true
  coefficient is I_m / h_m with an m-dependent h_m (DLMF 18.18.1). Signs are
  unaffected, but any statement about log-concavity or the location of the
  minimum is normalisation-dependent, and I had not said which normalisation I
  meant. That alone made the lemma ill-posed.
* Strict positivity ON the shore is impossible: at D = T_k(lam) with k the
  minimising level, that coefficient VANISHES (verified exactly: 0 at lam = 1 and
  lam = 2). The correct statement is D < shore implies C_m > 0, and D = shore
  implies C_m >= 0.

---

## ERR-0006 (18 August 2026) -- I measured a boundary claim OFF the boundary

**What I wrote, and committed:** "the closed-form condition on `a_{N-2}` IS the
binding coefficient for `lam >= 4`", supported by exact agreement to six figures
at `n = 13, lam = 8` and `n = 21, lam = 8`, and at `lam = 16`.

**What is true:** in the regime that actually decides Region A -- `lam ~ 4.72 n`
-- the binding coefficient is `a_1` (and `a_3` for some residues of n mod 4), not
`a_{N-2}`. Verified exactly on this claim's own terms:

| n | lam/n = 4.70 | lam/n = 4.72 |
|---|---|---|
| 20 | negative index [1] | clean |
| 24 | negative index [1] | clean |
| 28 | negative index [1] | negative index [1] |
| 40 | negative index [1] | negative index [1] |

`a_{N-2}` is positive with an enormous margin at every one of those points.

**The mechanism of the error, and it is a NEW one for me.** My checks at
`lam = 8, 16` were real and correct -- but they sit at `lam/n` of 0.6 and 0.38,
while the boundary lives at `lam/n = 4.72`. I verified the claim where it was
cheap to verify, and then stated it in a range (`lam >= 4`) that contains the
place I had never looked. This is not the ERR-0005 error (one value of a
parameter); it is subtler: I sampled the right parameter over the wrong RATIO.

**NEW RULE, added to the scientist skill:** a claim about a BOUNDARY must be
measured ON the boundary. If the boundary is a curve `lam = c(n)`, sample along
that curve, not at fixed convenient values of lam.

**Also corrected, same source -- and this one is strategic.** I wrote that the
unproved band is finite in n for each lam, and added "and finitely many levels is
exactly what certificates are for". The first half stands; **the second half was
unsupported**. The endpoint model gives `n*(lam) ~ exp(2 gamma_shore/(lam+1))`,
which tends to `exp(12 + 4 sqrt 3) ~ 1.66e8` as lam grows. "Finite" here may mean
1e8, not 1e3, and our certificates reach 1e3. Region A only overtakes that scale
around `lam ~ 7.9e8`. So the band is finite and STILL out of computational reach,
and saying otherwise was rhetoric, not a result.

**What survives and is confirmed by the same outside check:**
* the exact transitions, reproduced digit for digit by our engine:
  `lam = 1/20`: n = 515 has `a_0 < 0`, n = 516 clean; `lam = 1/10`: n = 659 has
  `a_0 < 0`, n = 660 clean (our own bisection had bracketed it to (656, 662]);
* the Gamma coordinate, verified exactly as a polynomial identity:
  `q(1 - 2u/s) = (2/s)^N * Gamma(d+N-u)/Gamma(d-u)` with `d = (lam+1)/2`
  (0 mismatches, 18 rational test points). This is the right coordinate: the
  zeros become `u = d, d+1, d+2, ...` and the oscillation splits into explicit
  Gamma lobes;
* the reason positivity RETURNS at large n -- the negative lobes all begin at a
  FIXED `u = d`, while the factor `N^{-u}` pulls the effective mass left of that
  barrier. That is a mechanism, not a coincidence.

**Where the open problem actually is, corrected.** Not `a_0` reopening -- that is
excludable for fixed low m from the Gamma integral. The gap is a late negative
BULK coefficient `a_m` with `m ~ rho N`. That is now the statement to attack.

## ERR-0008 (2026-08-18): sympy engine ban violation, PLUS a real logic gap it exposed

**What was wrong, part 1 (engine).** `lab/depth_proof.py` imported sympy with a
comment claiming "symbolic setup only; bounds are computed on flint" -- false.
sympy did the actual polynomial expansion/factoring on a two-variable degree-40
polynomial before flint ever touched it. This is exactly the uncontrolled memory
growth that took the founder's machine down. Founder's rule, now absolute: **no
sympy anywhere there is another way.** Fixed by rewriting the depth-2 proof
(`lab/depth2_parity_proof.py`) entirely on flint `fmpq` plus a small in-house
`BiPoly` dict-polynomial class -- zero sympy imports, verified against the exact
knife engine (70/70 match) before trusting any Bernstein output.

**What was wrong, part 2 (logic, found while fixing part 1).** The committed
`d2_proof.py` "Half B" step evaluated the top-knife condition at `M = N/2` and
claimed `gamma_shore <= (T_M-3)/2` "because the shore is a minimum over
levels" -- true only when `M` is an actual integer `k >= 3` in that minimum.
For ODD `N`, `M = N/2` is a half-integer, outside that set; grid search found
97 violations (all odd `N`) where the continuous formula dips below the true
`T_hat`. **Fixed** in `depth2_parity_proof.py` by splitting into two parity
branches with an ACTUAL INTEGER comparison level `K` (`N=2K` even, `N=2K+1`
odd), so `T_hat <= T_K` holds by definition, no numerical check needed. Both
branches now proved by Bernstein in under a second (7 and 11 boxes, 0 open).

**What this exposed, and it is the important part.** Checking positivity at
ONE point (`gamma = gamma_at_K`) only implies positivity at the TRUE shore
`gamma_hat` if the coefficient does not dip negative somewhere in between --
an assumption neither the old nor the new proof actually established. Testing
it directly against the exact engine found it is FALSE for two small levels:

* `n = 6`: depth-2 knife negative for `lam` roughly in `(0, 0.56)`, **strictly
  below the true shore**, not just at it.
* `n = 7`: depth-2 knife negative for `lam` roughly in `(0.15, 1.0)`, same.
* `n = 8` through `n = 40` (dense scan): **clean, zero failures.**

So "DEPTH 2 CLOSED" (`D2_COMPLETE.md`) is **withdrawn to "in progress"**: the
argument is correct and complete for `n >= 8`; `n = 6, 7` are confirmed finite
exceptions where the published depth-1 shore `T_hat` is NOT sufficient to
guarantee depth-2 positivity, and need either a refined (tighter) shore for
those two levels specifically, or a separate argument. `n = 3, 4, 5` remain
clean (checked directly).

**NEW RULE, added to the scientist skill:** a "prove at one boundary-adjacent
point implies the whole interval" argument is not valid without either (a) a
discriminant/no-root argument covering the WHOLE interval (as depth-2's Half A
already correctly does), or (b) an explicit monotonicity proof. Checking a
single endpoint is not the same as checking the interval, and small n is where
this kind of gap actually bites -- check small n directly, at fine grain, near
the true (not proxy) boundary, before calling anything closed.

## ERR-0009 (2026-08-18): ERR-0008's "n=6,7 exceptions" was MY OWN bug, not physics

**Retracting part of ERR-0008.** The claim "depth-2 negative strictly below
the true shore at n=6,7" was built on a bug in the exploratory test script,
not a property of the object. The script computed

    D_shore = T_hat(lam) + 3

and then read off `gamma = (D-3)/2` from that -- but `T_hat(lam)` **already
equals** the shore's `D` value (since `gamma_shore = (T_hat-3)/2` by
definition, so `D_shore = 2*gamma_shore+3 = T_hat`, no extra `+3`). Adding it
anyway shifted every tested gamma up by 1.5, so the script was testing
`gamma_shore_true + 1.5`, never the actual shore.

**Rechecked with the correct formula** (`gamma_shore = T_hat(lam)/2 - 3/2`,
no extra offset), dense grid, n = 4..40, lam from 0.001 to 5, at the true
shore and just below it: **zero failures.** n=6 and n=7 are clean, exactly
like every other level tested. There is no exception.

**So `D2_COMPLETE.md`'s correction header is itself partly wrong and is now
corrected again:** the sympy-ban fix and the odd-N parity fix (both real,
both still stand, `depth2_parity_proof.py` verified 70/70 against the exact
engine) are unaffected. But depth 2 is **NOT** limited to `n >= 8` -- it holds
for every `n >= 4` tested, and the Bernstein certificates (parity-split,
`K >= 3`) plus the direct checks (n = 3, 4, 5, and now 6, 7 too) leave no
known gap.

**Lesson, added to the scientist skill:** when a "shock finding" contradicts
hundreds of thousands of prior zero-failure certificates, check the
EXPLORATORY script's own arithmetic against the DEFINITION line by line
before trusting the finding -- especially the `D <-> gamma` conversion
(`D = 2*gamma+3`), which has exactly the kind of `+3`-shaped trap that bit me
here. A surprising result is more likely to be a bug in new code than a
40-year-old shore formula being wrong.

## ERR-0010 (2026-08-18): `depth_d_proof.py`'s generic `build_branch` had a wrong
homogenization -- invisible for d<=5, wrong for d>=6

**What was wrong.** `build_branch(parity, d, e_polys)` clears the denominators
`(2m+gamma+1)_j` (for `j = 0..d`) to bring all `d+1` terms of the beta-mean sum
to one common polynomial. With `gamma = Pg/Qg` and `L[i] = two_m_Qg + Pg +
Qg*(1+i)`, the identity is `(2m+gamma+1)_j = (prod_{i=0}^{j-1} L[i]) / Qg^j`.
To bring term `j` up to the FULL common denominator `L[0]*...*L[d-1]`, it must
be multiplied by the factors it is MISSING -- the COMPLEMENT product
`L[j]*L[j+1]*...*L[d-1]` -- and by `Qg^j` (from clearing its own denominator).
The committed code instead multiplied by the PREFIX product `L[0]*...*L[j-1]`
(factors the term already effectively has, not the ones it's missing) and by
`Qg^(d-j)` (the wrong power). Both are wrong in the same place, and they
happened to cancel out enough to give the right SIGN for depths 2 through 5 in
every tested case -- pure luck of small degree, not a validity argument.

**How it was found.** Generic self-check (`self_check`, comparing
`build_branch`'s sign against `jacobi_coeff_rec`, the exact reference) started
failing at depth 6 (2/56 mismatches, K=8/10, tiny c) and depth 7 (24/56,
wider K range, even at c=1) -- see the depth-6/7 debugging trail already
recorded in `results/DEPTHS_2_TO_5_PROVED.md`. Depths 2-5 showed 0 mismatches
throughout, which is why the bug shipped quietly in the first generic run.
Triangulated with a THIRD, independently-coded evaluator
(`depth3_proof.knife_sign_via_beta_formula`, direct evaluation at concrete
integer N, no K-parametrization) at the exact failing point (K=8, N=16,
n=17, j=7, c=1/100): independent method and the exact engine both gave sign
-1; `build_branch` gave +1. This isolated the bug to `build_branch`'s own
arithmetic, not the underlying beta-mean formula (confirmed correct a third
time). A tested hypothesis (denominator sign flip) was checked and REFUTED
(all cleared factors positive at the failing point). A term-by-term ratio
comparison (`homog_term / raw_term` for each `j = 0..d` at depth 6, K=9,
N=18, c=1/100) showed only the `j=0` term had the expected ratio `Qg^d`; every
other term's ratio was inconsistent -- proof the homogenization formula
itself was structurally wrong, not a numerical fluke.

**Fixed.** Complement product + `Qg^j` (both shown above), applied in
`lab/depth_d_proof.py`'s `build_branch`. Verified: the corrected
`fixed_term/raw_term` ratio is now constant and positive across all `j` at
the original failing point, and `sign(fixed_tot) == sign(raw_tot)` (both -1,
matching the exact engine). Re-ran `self_check` for depths 2 through 10 (K in
3,4,5,6,7,8,9,10,12,15; c in 1/100,1/10,1/2,1,29/100): **0 mismatches for
every depth**, including the two that previously failed.

**Status of the Bernstein certificates.** Because the OLD, buggy `build_branch`
was used to produce the depths-2-5 Bernstein certificates recorded in
`results/DEPTHS_2_TO_5_PROVED.md` (1 box each, suspiciously fast), those
certificates technically certify the WRONG polynomial, even though the
self-check now confirms the underlying claim is still true for those depths.
**They must be regenerated with the corrected `build_branch` before being
trusted as rigorous positivity proofs** -- the sign-match self-check alone is
a strong but not sufficient substitute for an actual Bernstein certificate on
the corrected polynomial. Regeneration in progress; depth 2 done post-fix (45
even-parity boxes, 59 odd, both `proved=True` -- up from 1 each, i.e. the
corrected polynomial is genuinely harder to certify, consistent with the fix
being real). Depths 3+ pending as of this entry.

**NEW RULE, added to `prover-v2` skill:** when homogenizing a sum of terms
`coeff_j * num_j / (2m+gamma+1)_j` (denominators growing with `j`, one nested
factor at a time) to one common denominator, the multiplier for term `j` is
always the COMPLEMENT of what it already has relative to the full product,
never the prefix. A generic self-check across MANY depths/degrees is what
caught this -- a single hand-checked depth (as depth2/3's own hand-derived
closed-form provers did, sidestepping the general loop entirely) would not
have exercised the bug at all. Always self-check a generic d-parametrized
construction at several different `d`, not just the smallest one.

## ERR-0011 (2026-08-18): the SAME ERR-0010 bug was already sitting, undetected,
in the PREVIOUSLY-TRUSTED `depth3_parity_proof.py` -- and its own self-check
never had a wide enough range to catch it

**What was wrong.** `depth3_parity_proof.py:74` (`term = coeff_bi * num_bi *
den_cleared * (X**j) * (Qg ** (d - j))`) uses the exact same wrong
homogenization as ERR-0010: prefix product (`den_cleared`, built as
`prod_{i=0}^{j-1}(...)`) times `Qg**(d-j)`, instead of the correct complement
product times `Qg**j`. This is a SEPARATE, independently hand-written file
(not generated from `depth_d_proof.py`) that shares the same bug because the
underlying algebra mistake is the same one a human made twice.

**Why its own self-check never caught it.** `main()`'s `trials` (line 124) use
only `c_num in (1, 5, 10, 20, 29)` with `c_den = 100` -- i.e. `c` from 0.01 to
0.29, NEVER `c >= 1`. Checked directly against the exact reference
(`jacobi_coeff_rec`) at `c = 1`, EVERY tested `K` from 15 up to 200 (even
parity) MISMATCHES: `build_branch` gives `+1`, the true sign is `-1`. This
means `depth3_parity_proof.py`'s Bernstein certificate -- "0 open boxes,
proved for K>=3, ALL c>=0" -- certified the WRONG polynomial. It never was a
proof of the physical depth-3 claim.

**How it was found.** While regenerating depth 2's Bernstein certificate with
the ERR-0010 fix (using the new, faster de Casteljau `prove_box`, see the
speed lesson above), a spot check of `depth_d_proof.py`'s own corrected
`build_branch` at unusually large `K` (300, 1000, c=1 -- far outside any
self-check ever run before tonight) turned up a genuinely negative value.
Cross-checked against `jacobi_coeff_rec` directly: the true sign IS negative
there, so `depth_d_proof.py`'s fixed formula was CORRECT (verified at K up to
1000, both parities, several c). But the SAME point evaluated through the
OLDER, previously-"proved" `depth3_parity_proof.py` gave the WRONG (positive)
sign -- a second, independent confirmation that a bug exists specifically in
that older file, not in the corrected generic one.

**Status, honestly.** `results/D3_STATUS.md`'s claim "depth 3 is fully proved
for n>=6 (even) / n>=7 (odd), every lam>0" is **RETRACTED** effective this
entry. It was never true; the certificate backing it certified a different
polynomial than the physical claim. The dense-grid "checked but not proved"
evidence for small n in the same file is unaffected (it goes through
`jacobi_coeff_rec` directly, not through the buggy `build_branch`). The
CORRECT depth-3 result, once re-certified, will come from `depth_d_proof.py`
(the generic, ERR-0010-fixed, wide-range-verified implementation) -- see the
in-progress Bernstein regeneration referenced in ERR-0010.

**NEW RULE, added to `prover-v2` skill and now MECHANICAL going forward:**
any `self_check`/`self_check_concrete` in this family must test `c` across
at least a couple orders of magnitude including `c >= 1` (not just tiny
`c < 0.3`), and `K` should include at least one value in the hundreds, not
only single/double digits -- a self-check whose domain is much narrower than
the Bernstein box it is meant to validate is not actually validating the
whole box. Two independent files carried the identical algebra mistake
undetected specifically because both self-checks used a narrow, small-value
range. A narrow self-check is worse than no self-check: it manufactures
false confidence.

## ERR-0012 (2026-08-19): `build_wedge` certified the WRONG polynomial, and the
self-check could not have caught it -- found by four independent verifier agents

**What was wrong.** `keystone_unglued.build_wedge` re-derived the whole beta-mean
construction from scratch in wedge coordinates, carrying each quantity at "the
appropriate power of c". Those powers were wrong. Consequence: every
`wedge proved, 1 box, 0 open` written to `results/keystone_unglued.json` at
depths 2 and 4 certified an object that is not the knife.

**This retracted "depth 2 fully proved".** Its `lo`, `hi` and `small` pieces
verify clean, but the wedge is one of the four pieces, so the region `c < 5/12`
was uncovered at every depth. Depth 2 was downgraded the moment this was found,
not after the fix.

**How it was found, and this is the part worth keeping.** A Workflow graph ran
four depths in parallel, each with an INDEPENDENT verifier agent instructed not
to trust the prover and to write its own harness. All four, separately, landed on
the same function. Their decisive test was one I had not thought to run: the
wedge and the branch must agree in SIGN on their shared boundary `c = C_MIN`,
where the wedge's `K = 5/(4c)+z = 3+z`. They disagreed 9 of 9 points at depth 3
(branch +, wedge -), and since `build_branch` is the construction validated
against the exact engine, the wedge was the wrong one. Mismatch counts against
the reference: 770/3145 at d=3, 30/5367 at d=4, 148/502 at d=5, 256/4639 at d=6.

**Why my own self-check was blind, in two separate ways.**
1. `self_check` built and tested ONLY `build_branch`. `build_wedge` and
   `build_small_lam` had no self-check at all. Third occurrence of the ERR-0010
   pattern: the bug lives exactly where the check does not reach.
2. Subtler, and the more useful lesson: inside the window `v in [8/5, 2]` the
   reference sign is ALWAYS +1. A sign comparison there cannot distinguish the
   intended polynomial from ANY other positive function. So even a self-check
   that HAD covered the wedge would have passed while the wedge was wrong. The
   check was close to vacuous and reported "0 mismatches" all the same.

**Fixed, two ways, cross-validated.** The wedge is no longer re-derived. It is
obtained by SUBSTITUTION into the already-validated branch: with
`H(K,c,v) = sum_a K^a P_a(c,v)` and `A = deg_K H`,
`W = sum_a (5+4cz)^a (4c)^(A-a) P_a(c,v)`, which is `(4c)^A * H(K -> 5/(4c)+z)`.
Since `(4c)^A > 0` on the domain the sign is preserved, and nothing is
re-derived, so nothing new can be mis-derived. The verifiers independently
confirmed the equivalent algebraic route (removing the spurious c's from
`B`, `kk2`, `Qg`, `Pg`) gives the identical coefficient dict. Boundary agreement
after the fix: 9/9 at every depth 2-6, both parities.

**And the check is fixed too, not just the code.** `self_check_all` now covers
all THREE constructions, probes `v` well OUTSIDE the window (v = 1, 5/4, 3, 4) so
the reference actually goes negative, and REPORTS the number of negative
reference signs -- printing `VACUOUS` when that count is 0, i.e. saying out loud
when it has proved nothing. A check that cannot fail is not a check.

**Physics is untouched, again.** 1196 in-window trials found 0 negative knives;
every sign failure sits at `v` outside `[8/5, 2]`. What was broken was the
certificate, not the claim.

**NEW RULE:** an independent verifier that does not share the prover's code is
worth more than any amount of self-checking. This bug had survived my own
review, two commits and a night of work; it did not survive one pass of four
agents told to disbelieve me.

## ERR-0013 (2026-08-24): the odd-depth "cancellation" diagnosis was wrong -- the
fixed-window step (a) statement is FALSE at odd depths, and the Bernstein runs
were failing because they were asked to prove a false claim

**What was wrong, twice.**
1. `ODD_DEPTH_DIAGNOSIS.md` concluded the odd-depth `lo` piece fails through
   near-total cancellation (relative margin `7.8e-05` at the corner), i.e. a
   conditioning problem, and recommended an SOS basis change. The mechanism is
   refuted by its own measure: the corner margin decreases SMOOTHLY with depth
   (2.2e-3, 7.8e-5, 3.1e-6, 1.1e-7 for depths 2, 3, 4, 5) with NO parity
   structure, while certification alternates by parity. Depth 4's margin is 25x
   WORSE than depth 3's, and depth 4 certifies in 1369 boxes.
2. The actual reason: **the statement is false.** The step-(a) claim "knife_d
   positive at `D = T_{v*lam}` for ALL v in `[8/5, 2]`" fails at odd depths.
   Exact witnesses, confirmed independently by `build_branch` AND the exact
   reference engine `jacobi_coeff_rec` (`results/odd_depth_window_refuted.json`):
   depth 3 even parity `K=54, c=239/400, v=2` (n=109, lam=64.53); depth 3 odd
   `K=54, c=71/120, v=2`; depth 5 both parities at `K=111, c~0.59, v=2`; also
   `v=8/5` at `K=226, c=3/5`. All inside the certified box.

**The structural mechanism, which was on the wall the whole time.** The margin
law of 2026-08-17: knives of even order `j` MUST have a threshold in `D`, odd-j
knives cannot. Odd depth d means even `j = d+1`. Away from the integer argmin
of `T_k`, the evaluation point `T_{v*lam}` exceeds the true shore by an amount
growing with `lam`, overshoots the threshold, and the knife is LEGITIMATELY
negative. Even depths are thresholdless, which is the entire even/odd split in
the certification record. This is the ERR-0010 mechanism a second time: the
method demanded strictly more than the physics. The physics shows no violation:
at every witness point the knife is POSITIVE at the true shore `T_hat` (integer
argmin), both engines agreeing.

**Why every earlier scan missed it (ERR-0005, third occurrence).** The negative
region needs BOTH `c` in a narrow band (~0.52..0.67) AND `K` large (>= 54).
Every window-cleanliness scan used `c` grids like {5/12, 1, 5, 7, 50, 60} --
stepping straight over the band -- and the ERR-0012 note "1196 in-window trials,
0 negative knives" inherited the same blindness. A 2D-conjunctive feature needs
BOTH axes sampled inside it; the existing rule "sample relative to moving
boundaries" now extends to: when a region is suspected clean, hunt its
COMPLEMENT with an optimizer (bisection on sign along rays), not only grids.

**What dies:**
* the fixed-window form of step (a) for ALL odd depths -- unprovable, being false;
* the SOS/Jacobi-basis route AS AIMED AT THAT STATEMENT (you cannot certify a
  false inequality; the basis was never the problem);
* the "same window clean at every depth" keystone property claimed in
  `UNGLUED_KEYSTONE.md` (its "0 negatives out of 160 per depth" was grid
  blindness);
* the cancellation diagnosis in `ODD_DEPTH_DIAGNOSIS.md` (correction appended
  in place).

**What survives:**
* even-depth certificates (2, 4, 6): their statements are about thresholdless
  knives, are true as far as anything now shows, and were honestly certified;
* step (b) (PROVED for lam >= 7) and step (c) -- unaffected;
* the physical claim itself: positivity at and below `T_hat`. No witness
  violates it.

**The repaired route, made concrete the same day.** What the argument actually
needs at odd depths is positivity in a window of FIXED width in k-units around
the critical level `k*(lam)` (the measured room is ~sqrt(lam) k-units, ample).
The critical curve `dT/dk = 0` is quadratic in `lam` with discriminant
`3 k^2 (k-2)^2 (4k^2-12k+3)`: the non-square part is a QUADRATIC, so the curve
is a conic, has the rational point `(k, w) = (3, 3)`, and admits an explicit
rational parametrization. Substituting `lam = lam(t)`, `k = k(t) + delta` with
`delta in [-3/2, 3/2]` turns the odd-depth claim into a polynomial positivity
problem in `(t, delta, K)` -- certifiable by the existing Bernstein pipeline.

## ERR-0014 (2026-08-28) — two arithmetic slips in the positivity write-ups, both conservative

Found by the domain-critic pass on the same day the theorems were written, not by
me. Both are wrong as stated; neither breaks a conclusion, because both err in
the safe direction.

**(a) The lower bound in Lemma 3 (`results/BFORM_POSITIVITY_THEOREM.md`), and
the same expression duplicated in `results/KERNEL_TP_THEOREM.md`'s corollary.**
I wrote `H - 2r + 1 = (D-1)/2 + 2(n-2-r)`. The identity is
`H - 2r + 1 = (D-1)/2 + 2(n-1-r)`, with `H = (D+4n-7)/2`. Checked exactly: my
form fails in 27/27 test cases, the correct form in 0/27. My version understates
the quantity by 2, so every positivity conclusion drawn from it still holds.
Both files corrected.

**(b) Theorem 6's parenthetical.** I wrote that `H/2 > n-2` holds "exactly when
`D > 3`". It reduces to `D > -1`. The physical domain has `D > 3`, so the
theorem's proof is unaffected — but the stated equivalence is false. Corrected to
`D > -1`, with the note that this holds throughout the physical domain a
fortiori.

**The lesson is the one the repository already encodes and I did not apply.** I
derived both expressions by hand and then machine-verified the THEOREMS built on
them — the identity checks, the implications, the region — all of which passed,
because both slips are conservative and therefore invisible to any check that
only asks whether the conclusion holds. A check that cannot fail is not a check
(ERR-0012). Every hand-derived intermediate identity must be machine-verified as
an identity, separately from the result it feeds. `lab/bform_gap_diagnosis.py`
now does this for the pieces it uses; the earlier modules did not.

**Both review passes found (a) independently, in different but algebraically
identical forms** — the domain-critic wrote `(D-1)/2 + 2(n-1-r)`, the
independent-validator wrote `(D+3)/2 + 2(n-2-r)`; both equal `(D+4n-5-4r)/2`,
and both differ from what I wrote. Two reviewers converging on the same line is
the strongest signal available here that the slip was real and mine.

## ERR-0015 — "Criterion S" contains its own conclusion (2026-08-29, mine, same day)

**What I claimed.** In `results/FFP_LITERATURE_PASS.md` §3 and in the commit
`c50b146` I presented CRITERION S — every Taylor coefficient `A_m` of the
reduced composition at `x = 1` strictly positive — as a *criterion* sufficient
for `K_r > 0`, and called it "the first candidate all-depths criterion whose
tested region is the physical domain rather than a corner".

**Why that is wrong.** `A_0 = P(1) = K_r`. The hypothesis contains the
conclusion. The Descartes argument is valid but useless: `K_r > 0 and (stuff)`
implies `K_r > 0`. As a criterion S is trivial, and the 3094/3094 measurement,
while true, does not measure what I said it measured.

**How it was caught.** Not by a check — by asking, an hour later, what `A_m`
actually *is*. The answer is an exact identity, verified first in 1236 ad-hoc cases and then
in the artefact itself (`results/ffp_convolution_check.json`, 1696 checks), 0
mismatches either time:

    A_m = C(r,m) * K_{r-m} evaluated at H -> H - m,   i.e. at D -> D - 2m.

Reading `A_0` in that identity, with `m = 0`, is what exposed the circularity.

**What survives, and it is worth more than the false criterion.** The Taylor
coefficients of the knife polynomial at `x = 1` ARE knives — of lower depth, at
lower dimension, along the diagonal `(j, D) -> (j-m, D-2m)`. So

  * the measurement says the whole diagonal staircase is positive below the
    shore (3094 points) and breaks above it (0 of 26 negative knives);
  * the useful implication runs the OTHER way from what I wrote: a bound
    `theta_max(p BOX q) < 1` — a root-location statement about a Schur-Szegő
    composition, which is a studied problem — would give the entire diagonal at
    once, without knowing any knife value in advance. That direction is not
    circular, and it is now the live route.

**The lesson, which this repository already had.** ERR-0012: a check that cannot
fail is not a check. I built the sweep to test S before asking what S's own
first term was. The rule to add: before measuring a criterion, expand its
hypothesis at the trivial index and check that the conclusion is not sitting
inside it.

## ERR-0016 — "odd-j knives never turn negative" is false (2026-08-29, mine)

**What the file said.** `results/BFORM_POSITIVITY_THEOREM.md` §6b, from the Beta
representation: as `D -> inf` the weight's mass goes to 0, so
`sign(K_r) -> (-1)^r = (-1)^{j-1}`, and I concluded — quoting myself — "Odd `j`
never turns negative; even `j` must. ... That is the programme's long-measured
parity asymmetry ... derived rather than observed."

**Why it is wrong.** The limit constrains the sign at infinity. It forbids an
odd-`j` knife from ENDING negative; it says nothing about a dip at finite `D`.
Half the sentence was derived, the other half was assumed.

**The counterexample, on both engines.** `n = 6`, `j = 3` (odd), `lam = 1/10`:

| D | 10 | 12 | **13** | 20 | 100 | 1e4 | 1e6 |
|---|---|---|---|---|---|---|---|
| sign | + | + | **-** | + | + | + | + |

The composition engine and the independent reference engine
(`jacobi_normal_form` via `moment_kernel_probe.ref_sign`) agree at every point.
A wider scan (`results/shore_gap_scan.json`, 928 rows) finds **72 odd-`j` knives
with a zero**, concentrated at small `lam` (22 at `lam = 1/10`, 19 at `1/2`, 19
at `1`, 11 at `5/2`, 1 at `7`, none above) and spread over `j` = 3, 5, 7, ..., 17.

**What is unaffected.** Every one of those dips is ABOVE the shore: the closest
odd-`j` approach is `D0/T_hat = 1.146` (`n = 8`, `j = 3`, `lam = 1`), and over all
928 rows no ratio falls below 1. The physical claim — positivity below the shore
— is untouched, and so are Theorems 1-9, which never used the parity sentence.

**Corrected statement.** The `D -> inf` limit proves: every EVEN-`j` knife is
negative for all sufficiently large `D`. For odd `j` it proves only that the
knife returns to positive; a finite-`D` dip is possible and does occur at small
`lam`.

**How it was caught, and the lesson.** By a scan that treated the parity claim as
a hypothesis to be tested rather than a fact to be assumed — it reported odd-`j`
zeros instead of skipping them. My first version of that scan skipped odd `j`
"because §6b says so", and would have found nothing. When a derivation is used to
prune a search, the pruned branch must still be sampled: a claim that removes
work is exactly the claim that never gets checked.

## ERR-0017 — the depth law "exactly j <= n/2 + 1" was measured on even n only (2026-08-29)

**What the repository says.** `results/asymptotic_regime_probe.json` records
`depth_law_j_le_half_n_plus_1` with `matches_law: true` in every row, and
`results/BFORM_POSITIVITY_THEOREM.md` §6 quotes it as "an exact depth cutoff
`j <= n/2 + 1`".

**Every row of that measurement has EVEN n** — 12, 16, 20, 24, 28, 36, 44. At even
`n` the two candidate forms `n/2 + 1` and `(n+3)/2` coincide, so the run could not
distinguish them, and odd `n` was never probed at all.

**Mapped over every n from 11 to 61** (`lab/depth_boundary_map.py` ->
`results/depth_boundary_map.json`, same exact predicate, no floating point):
**the law fails in 31 of 51 cases**, in both directions. The two headline
counterexamples are stable across `lam = 10^3 .. 10^6`:

| n | largest good j | law says |
|---|---|---|
| 31 | **17** | 16 |
| 47 | **23** | 24 |

And the original sample explains itself: 12, 16, 20, 24, 28, 36, 44 are **all
multiples of 4**, which is exactly where the formula happens to be right.

The measured boundary is always ODD, rises in runs of 4 or 5 consecutive `n`, and
drifts steadily below `n/2`: `j - n/2` goes from `+2` at `n = 14` to `-1.5` at
`n = 61`. So the cutoff is near `n/2` but is not `n/2 + 1`, and its true form is
open — this file does not guess one from 51 points.

**What is affected.** Nothing proved: the Hausdorff corner was always recorded as
MEASURED, not proved, and the exact cutoff was descriptive. What must change is
the wording — "exact depth cutoff" becomes "cutoff close to `n/2+1`, exact form
unknown, and not `n/2+1` at `n = 31` or `n = 47`" — and the artefact's
`matches_law` flag, which is true only because of the even-`n` sample.

**How it was caught.** By a different question entirely: the far-below
localisation has its own boundary at `n = 2J-3`, whose points are all at ODD `n`,
so comparing the two lines forced the odd case to be computed for the first time.

**The lesson, and it is the third instance today** (ERR-0015, ERR-0016). A law
measured on a sample that cannot separate two hypotheses is not a law, it is one
hypothesis with a flattering sample. Before recording "exactly", check that the
grid can distinguish the stated formula from its nearest rival.

**And it is the second time this exact mistake has been paid for.** The manifest
already carries `FROZEN_PREDICTION_blocks.md`, retracted on 18 August with the
note: "the block-width step law was an artefact of scanning only even j; refuted
by the full integer grid." Even `j` then, multiples of four now. The lesson was
recorded as a fact about that one artefact rather than as a rule about sampling,
so it did not transfer. It is now a rule, in memory as
`law-needs-a-sample-that-can-refute-it`.
