# AI disclosure

This research was conducted by the author (Andrei Pluzhnik) working with an AI
research assistant (Claude, Anthropic), which performed derivations, wrote the
computational code, and drafted the text under the author's direction.

Safeguards applied:

- **Exact arithmetic only.** Every certificate is checked over the rationals
  or over Q(sqrt3); no floating point enters any claim-bearing verdict.
- **Independent adversarial review with a real catch.** The reviewer audited
  the full logical chain and found one genuine defect: a coverage gap in the
  prover's escalation loop that silently skipped 740 cells while reporting
  success. The gap was fixed; the reviewer's own battery
  (`lab/attack_blade_theorem.py`, sharing no code with the prover)
  re-certified every cell including the formerly uncovered ones: exit 0,
  no counterexample. The episode is preserved in the public log as a lesson:
  an exit code proves what a script checked, not what it covered.
- **Two failed prover architectures preserved.** A symbolic-branch version
  (drifts from the argmin at large k) and a version missing the no-window
  alternative both failed honestly and are recorded in the log.
- **Persisted batteries.** The 60,000-point stress test, the exact
  closest-approach scan (24,375 checks), and both provers ship with run
  metadata (command, git commit) and per-cell logs.
- **Human gate for publication.** No agent published, pushed, or submitted
  anything; every public step is a deliberate human action by the author.
