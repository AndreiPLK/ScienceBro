# Scientific method rules

The binding rule set lives in roadmap §6 and `.claude/rules/`. This file is the
plain-language summary.

1. **Evidence**: every factual claim links to a source with an exact location.
   Abstract-only reading is second-class and marked. Contradictions stay visible.
2. **Hypotheses**: stated with a null, predictions, falsification criteria, and one
   primary metric — then frozen before the confirmatory run.
3. **Experiments**: frozen manifests, preserved raw outputs, recorded seeds/precision/
   hardware, negative controls and known-answer baselines always included.
4. **Validation**: an independent implementation attacks the result on hidden points
   with convergence and signature checks. Pass/fail is deterministic.
5. **Claims**: promoted only through the gate; downgraded automatically when support
   is invalidated. Public wording is fixed at the gate, not improvised.
6. **Release**: a human presses every publish button.

For the AInstein audit specifically: upstream training loss is never evidence of
correctness; only the independent verifier's checks count (roadmap §15).
