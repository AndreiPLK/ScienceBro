---
description: Freeze a hypothesis + experiment protocol before the confirmatory run
---

Freeze the experiment protocol for: $ARGUMENTS (project-id experiment-id)

1. Load the experiment YAML; call `Experiment.freeze_blockers()` logic: command,
   code_commit, analysis_plan, primary_metric must be set.
2. Confirm the linked hypothesis is complete (statement, null, falsification,
   primary_metric) and freeze it: `uv run sb hypothesis freeze <project> <H-id>`.
3. Verify thresholds are predeclared (calibrated on baselines is OK; candidate results
   must NOT have been inspected yet — §15 residual normalization).
4. Set experiment status to `frozen` and record git commit + uv.lock hash.
5. Print every changed file.

After freezing, the primary metric and thresholds may not change; a change requires a
new experiment version with a recorded reason.
