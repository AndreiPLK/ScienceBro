# Evidence contract (binding)

- Every externally factual scientific claim must reference an evidence record id.
- Evidence records must contain: stable identifier, exact location, paraphrase,
  evidence type, limitations, acquisition date; local PDFs get a sha256.
- Prefer primary papers, official datasets/docs, original repositories.
- Search results, blog summaries, LLM answers, abstract-only readings are NOT full
  evidence; mark `abstract_only: true` where applicable.
- Citations must be verified against arXiv/Crossref/OpenAlex/publisher before
  `verified_by.metadata: true`. Existence is insufficient — the cited location must
  actually support the claim (`verified_by.content: true` only after checking).
- Contradictory evidence is preserved and linked, never summarized away.
- Missing evidence stays visible as a blocker.
