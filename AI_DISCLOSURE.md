# AI use disclosure

Required by the project's own release gate (roadmap §18) and stated here in full.

## What the AI did

Essentially all code, documentation and experiment execution in this repository was
written by an AI agent (Claude, Anthropic) operating in Claude Code, under the
direction of the human author. This includes:

- the independent verifier (`projects/ainstein-audit/verifier/`),
- the workbench, schemas, CLI and dashboard (`sciencebro/`, `apps/`),
- the experiment manifests, validation records and reports,
- the text of the reports, press material and this file.

## What the human did

- Set the research question and the priorities, and re-set them when the work drifted.
- Imposed the binding constraint that the AI may never mark its own scientific work as
  verified: stage statuses are computed by deterministic checks against hashed artifacts
  (`sciencebro/proofgate.py`), not asserted in prose.
- Required that discrepancies be resolved by measurement rather than explanation, which
  is how the loss-scale discrepancy was settled.
- Approved or rejected infrastructure decisions on evidence (for example, GPU execution
  was abandoned after it measured ten times slower than CPU on float64).
- Sent all external communication personally. No email, publication or repository
  release was performed by the AI.
- Owns every scientific claim and the decision to publish it.

## Why this is stated plainly

The audit's value depends on the reader being able to check it rather than trust it.
Every number in the reports traces to a file with a recorded SHA-256 checksum, every
threshold was frozen and version-tagged before the results it judges existed, and failed
runs are preserved alongside successful ones. An AI wrote the code; the deterministic
gates and the preserved artifacts are what make the result checkable regardless of who
or what typed it.

## Known limitation of this arrangement

AI-written code can contain errors that AI-written tests do not catch. The mitigations
used here are known-answer tests against analytic solutions (Minkowski, Schwarzschild),
negative controls with deliberately corrupted input, cross-checks between independent
formulations (for example, the areal radius read from the metric versus an independent
Lambert-W computation of r(T, X)), and convergence checks. None of this substitutes for
review by a qualified relativist, which has not yet happened.
