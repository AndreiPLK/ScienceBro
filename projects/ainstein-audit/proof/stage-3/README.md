# Proof pack: Candidate generation (stage-3)

**Status: IN PROGRESS**

**Question:** Was a Petrov-I candidate trained under a frozen configuration with holdout points?

**Why it matters:** Unfrozen configs or leaked holdout points would invalidate the audit.

## What passed
- checkpoint sha256 recorded: fd56f1709961f3e3
- immutable training log preserved: epoch 500/500 complete
- holdout points excluded from training: hidden seed derived from checkpoint hash (candidate_stress.json)
- validation thresholds frozen before candidate inspection: THRESHOLDS_FROZEN.md + git tag thresholds-frozen

## What is not settled
- training config frozen before run (missing): 
- exact seed recorded (missing): 

## How to reproduce
Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.
Compare outputs against `measurements.json`; verify file integrity against
`checksums.sha256`; check `attestation.json` for the exact git commit and
environment lock hash.

## What this does and does not prove
It proves: the declared deterministic checks ran with the recorded outcomes.
It does NOT prove: any claim about AInstein candidates beyond the allowed
public claim in `allowed-public-claim.md`.
