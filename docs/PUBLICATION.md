# Publication pipeline

Full spec: roadmap §18. Short version:

1. GitHub release (tagged, immutable commit) + environment lock + reproduction command.
2. Technical report (Markdown/PDF) with limitations and AI-use disclosure.
3. Zenodo archive with DOI.
4. arXiv preprint ONLY when a defensible contribution exists and all gates pass
   (gr-qc for the AInstein audit). Moderation/endorsement may apply.
5. Journal routing per roadmap table (CQG/PRD for GR results; JOSS for tooling).
6. Upstream-author contact package: result summary, reproduction command, key figure,
   pass/fail table, limitations, questions. Reproducible evidence first, never accusations.

Every step above the line "create the package" is executed by the human, not by agents.

## AI disclosure (living record)

- Models: Claude Opus 5 (implementation, tests, docs), via Claude Code.
- Human decisions: research question approval, claim promotion approval, all publishing.
- The model is not allowed to decide scientific truth; deterministic checks are.
