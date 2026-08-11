---
description: Audit evidence/claims consistency for a project and verify citations
---

Run the evidence audit for project: $ARGUMENTS

1. `uv run sb evidence audit <project-id>` — report all findings and warnings verbatim.
2. For each evidence record with `verified_by.metadata: false`, verify the identifier
   against arXiv/Crossref (sciencebro.research.citations for arXiv ids). Update records
   only when verification actually succeeds.
3. List claims whose cited location has NOT been checked against the claim text
   (citation existence is insufficient — §6 rule 6).
4. Report blockers first. Never mark verified what you did not verify.
