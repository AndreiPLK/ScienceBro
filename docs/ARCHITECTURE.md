# Architecture

See roadmap §4 for the full diagram. Short map of the actual code:

| Layer | Location | Notes |
| --- | --- | --- |
| Schemas + claim gate | `sciencebro/schemas/core.py` | `allowed_claim_promotion` is the single deterministic gate |
| File store | `sciencebro/store.py` | YAML/JSONL are the only truth; malformed files raise actionable `StoreError` |
| Computed status | `sciencebro/status.py` | derives everything from files; no stored percentages |
| Evidence audit | `sciencebro/evidence/audit.py` | deterministic rule checks |
| Citation verification | `sciencebro/research/citations.py` | arXiv API; failure → `unverified`, never `verified` |
| Run capture | `sciencebro/experiments/runner.py` | commit, lock hash, hardware, timestamps |
| CLI | `sciencebro/cli.py` | Typer app `sb` |
| Dashboard | `apps/dashboard/` | Streamlit, read-only over files |
| Registry | `registry/topics.yaml` | 10 topics, explicit readiness states |
| Donor pins | `vendor/upstream-manifest.yaml` | 13 pinned repos |
| First project | `projects/ainstein-audit/` | evidence, claims, hypothesis, verifier, upstream |
| Independent verifier | `projects/ainstein-audit/verifier/` | finite-difference geometry; NEVER imports upstream |

Data flow: files → store → status/audit/gates → CLI + dashboard. Nothing writes
scientific state except explicit CLI commands and hand edits, both visible in git.
