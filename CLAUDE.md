# ScienceBro — Claude Code project instructions

## MANDATORY: North Star check
Before selecting, starting or closing ANY task, reread `NORTH_STAR.md`. Every experiment
and mission must carry `north_star_relevance`. Infrastructure budget: ≤20% of effort;
≥80% goes to physics. The active program is the quantum-gravity S-matrix bootstrap
(`docs/QG_BOOTSTRAP_PLAN.md`); the AInstein audit is COMPLETE and archived in place
(`projects/ainstein-audit/`, published as github.com/AndreiPLK/spacetime-verifier,
DOI 10.5281/zenodo.21915627).

Authoritative spec: `SCIENCEBRO_MASTER_ROADMAP.md`. Deviations: `docs/DECISIONS.md`.

## Non-negotiable scientific rules (short form; full list in roadmap §6)

- Every factual scientific claim needs a source with an exact location; abstract-only
  evidence is marked `abstract_only: true`.
- Freeze hypothesis and primary metric BEFORE looking at final results.
- A run completing without an exception is NOT scientific validation.
- The independent validator must not import the implementation it validates
  (for AInstein: never import upstream loss functions).
- Claim promotion goes through `allowed_claim_promotion` — deterministic, no LLM judgment.
- Never use "discovered / proved / novel / confirmed / refuted" without the matching gate.
- Failed runs and contradictory evidence stay visible. Never delete raw results.
- No invented confidence percentages anywhere, including the dashboard.

## Engineering rules

- Everything project-scoped. Never modify global Claude settings or other repos.
- Source of truth = YAML/JSONL/Markdown files in this repo. Dashboard is read-only.
- Dev loop: `uv sync && uv run sb check` (ruff + mypy + pytest + integrity).
- Upstream AInstein code lives ONLY under `projects/ainstein-audit/upstream/` in its own
  uv environment; treat as untrusted (inspect before running).
- Pin third-party repos in `vendor/upstream-manifest.yaml`; verify license before copying code.
- Never commit secrets, proprietary PDFs, or restricted datasets.

## Roles

Specialist agent definitions are in `.claude/agents/` (research-director,
literature-reviewer, domain-critic, experiment-engineer, independent-validator,
release-reviewer). A claim is never self-approved by the role that implemented it.

## Commands

`sb doctor | sb check | sb topic list | sb project status <id> | sb evidence audit <id> |
sb claim list <id> | sb claim promote <id> <claim> <state> | sb release check <id> |
sb dashboard`
