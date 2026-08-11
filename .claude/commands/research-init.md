---
description: Initialize a research project from a registry topic (creates projects/<id>/ structure)
---

Initialize a ScienceBro research project for topic: $ARGUMENTS

1. Read `registry/topics.yaml` and find the topic.
2. Create `projects/<topic-id>/` with the structure from roadmap §8 (project.yaml,
   QUESTION.md, STATUS.md, research/, evidence/, hypotheses/, experiments/,
   validations/, results/{raw,processed,figures,tables}/, reports/, release/).
3. Fill project.yaml per the schema in `sciencebro/schemas/core.py` (Project).
4. Delegate QUESTION.md drafting to the research-director agent.
5. Run `uv run sb project status <topic-id>` and report the computed status.

Do not invent evidence or claims — the project starts empty and honest.
