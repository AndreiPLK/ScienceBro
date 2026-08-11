---
description: Run independent validation for a claim/experiment via the independent-validator agent
---

Validate: $ARGUMENTS (project-id claim-or-experiment-id)

1. Delegate to the independent-validator agent. It must use a separate formulation and
   must not import upstream losses or the implementation under test.
2. Required checks (roadmap §15): known-answer baseline, negative control, hidden
   points, precision convergence, boundary map, signature.
3. Write the result to `projects/<id>/validations/VAL-*.yaml` with decision
   pass/fail/inconclusive and explicit reasons.
4. Then run `uv run sb claim list <project-id>` to show what the gate now allows.

The implementing role never validates its own claim (§6 rule 22).
