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
