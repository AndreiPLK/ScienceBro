---
description: Dry-run the release gate and list exact blockers
---

Run the release gate for project: $ARGUMENTS

1. `uv run sb release check <project-id>` — report output verbatim.
2. Delegate final wording review to the release-reviewer agent.
3. Verify: clean-clone command documented, citations verified, licenses recorded,
   AI-use disclosure present, no secrets committed.
4. Publication remains a human action — produce the package, never push/submit.
