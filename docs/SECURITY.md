# Security

Binding rules: roadmap §22 and `.claude/rules/security.md`.

Environment-specific notes (this machine, 2026-08-11):

- Docker is NOT installed → isolation fallback: separate uv venvs per untrusted
  codebase (`projects/ainstein-audit/upstream/.venv-upstream`), inspected before run.
- Secrets: `.env` (gitignored) only; `.env.example` documents variables without values.
- Downloaded PDFs are treated as untrusted input and are NOT committed
  (license + size); hashes recorded in corpus.jsonl.
- Upstream checkout is gitignored; the pinned SHA + re-clone command live in
  `projects/ainstein-audit/upstream/INSPECTION.md`.
- Before any public release: run secret scanning and the license audit
  (AInstein license conflict GPL-2 vs MIT is an open blocker recorded in the manifest).
