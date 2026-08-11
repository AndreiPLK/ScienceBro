# ScienceBro — Implementation Plan (adapted to the real environment)

Date: 2026-08-11
Environment inspected: Windows 11, Git Bash + PowerShell, Python 3.12.10, uv 0.11.7,
git 2.53.0, Node 24.14.1, **no Docker**, GPU: NVIDIA RTX 4070 SUPER 12 GB.

## Environment decisions

- Native execution (no Docker on this machine). Untrusted upstream code runs in a
  **separate uv environment** under `projects/ainstein-audit/upstream/` and is inspected
  before execution. Documented as the fallback per roadmap §9 (Isolation).
- Python 3.12 via uv-managed venv. `uv sync` is the single environment command.
- GPU available for upstream PyTorch runs if needed; validator core is CPU-first (float64).

## Sequence (from roadmap §20 / §25)

1. **Phase 0 — preservation** (done): git init, doctor report, docs, .env.example.
   Existing work preserved: only `SCIENCEBRO_MASTER_ROADMAP.md` existed; nothing overwritten.
2. **Phase 1 — core scaffold**: pyproject + uv, Pydantic schemas (project, evidence,
   claim, hypothesis, experiment, validation), `sb` CLI (doctor, project status, check),
   unit tests, ruff, mypy, CI.
3. **Phase 2 — donor harvest**: `vendor/upstream-manifest.yaml` with pinned SHAs and
   licenses; project-scoped `.claude/` agents, commands, rules. No global installs.
   Donor code is NOT vendored in V1 — ideas and pinned references only; adapters have
   filesystem fallbacks.
4. **Phase 3 (minimum) — evidence engine**: corpus/evidence/claims JSONL+YAML storage,
   citation verification against arXiv/Crossref (network optional, fail-visible).
5. **Phase 4 (minimum) — experiment engine**: manifests, freeze gate, run capture.
6. **Phase 5 (minimum) — claim gates**: promotion blocked without evidence+validation.
7. **Phase 6 — dashboard**: Streamlit, 7 pages, read-only over repo files.
8. **Phase 7 — AInstein bootstrap**: pin blackhole @ `54736e466e54d948bd509b072e4047cf98405064`,
   project records, evidence, hypotheses, smallest safe baseline attempt.
9. Report honestly: what works, commands, tests, blockers, next experiment.

## Non-goals honored (roadmap §3)

No chatbot, no cloud platform, no vector DB, no auto-publication, no fake confidence.

## Verification loop

```
uv sync
uv run ruff check .
uv run mypy sciencebro
uv run pytest
uv run sb doctor
uv run sb check
uv run sb project status ainstein-audit
uv run sb dashboard
```
