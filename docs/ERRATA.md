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
