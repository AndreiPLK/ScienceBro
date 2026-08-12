# Proof pack: Independent candidate stress test (stage-4)

**Status: NOT STARTED**

**Question:** Does the candidate survive hidden-point, convergence, signature and boundary checks?

**Why it matters:** This is the scientific core: independent verification outside the training path.

## What passed

## What is not settled
- hidden-point residuals measured (median/p95/p99/max) (missing): 
- signature and determinant checks across domain (missing): 
- boundary and horizon failure maps (missing): 
- precision and convergence tests (missing): 
- negative controls fail as expected (missing): 
- independent implementation, no upstream loss imports (missing): 

## How to reproduce
Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.
Compare outputs against `measurements.json`; verify file integrity against
`checksums.sha256`; check `attestation.json` for the exact git commit and
environment lock hash.

## What this does and does not prove
It proves: the declared deterministic checks ran with the recorded outcomes.
It does NOT prove: any claim about AInstein candidates beyond the allowed
public claim in `allowed-public-claim.md`.
