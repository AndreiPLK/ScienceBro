# ScienceBro

ScienceBro helps an engineer do computational science without pretending that AI output is
evidence. It searches real papers, records claims, freezes experiments, attacks results with
an independent validator, and shows exactly what is ready to publish.

## Quick start

```
uv sync
uv run sb doctor
uv run sb dashboard
```

## What it does, in plain language

1. **Find what scientists actually know** — build a traceable literature corpus.
2. **Record exactly where each fact came from** — evidence records with exact locations.
3. **State what we think may be true and what would prove us wrong** — falsifiable hypotheses.
4. **Run the experiment** — frozen protocols, preserved raw outputs, full manifests.
5. **Make a separate validator attack the result** — independent implementations, hidden
   points, negative controls, convergence checks.
6. **Publish only what survives** — deterministic claim gates; a human always pushes the
   publish button.

## Current project

**Independent Invariant Stress Test of AI-Discovered Black-Hole Metrics** — an independent
audit of the AInstein project's reported non-Schwarzschild vacuum candidates
(paper: [arXiv:2607.05489](https://arxiv.org/abs/2607.05489), code:
[xand-stapleton/ainstein@blackhole](https://github.com/xand-stapleton/ainstein/tree/blackhole)).

State lives in `projects/ainstein-audit/` as plain YAML/JSONL/Markdown. The dashboard is a
read-only view over those files and never invents progress.

## Commands

```
uv run sb doctor                          # environment diagnosis
uv run sb topic list                      # research opportunity backlog
uv run sb project status ainstein-audit   # computed project status
uv run sb evidence audit ainstein-audit   # evidence/claim consistency audit
uv run sb claim list ainstein-audit       # claim ledger with promotion blockers
uv run sb release check ainstein-audit    # release gate dry run
uv run sb check                           # lint + types + tests + integrity
uv run sb dashboard                       # local Streamlit dashboard
```

## Honesty rules (non-negotiable)

- Every factual scientific claim needs a source with an exact location.
- A run completing without an exception is not scientific validation.
- Claims are promoted by deterministic gates, never because they sound plausible.
- Failed runs and contradictory evidence stay visible.
- No invented confidence percentages, anywhere.

See `SCIENCEBRO_MASTER_ROADMAP.md` for the full specification and
`docs/DECISIONS.md` for deviations.
