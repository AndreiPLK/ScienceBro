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
