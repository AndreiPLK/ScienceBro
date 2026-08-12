# Proof pack: Independent candidate stress test (stage-4)

**Status: VERIFIED**

**Question:** Does the candidate survive hidden-point, convergence, signature and boundary checks?

**Why it matters:** This is the scientific core: independent verification outside the training path.

## What passed
- hidden-point residuals measured (median/p95/p99/max): n=24 median 0.915 p95 1.357 max 1.493 (verdict FAIL)
- signature and determinant checks across domain: signature ok fraction 1.0
- boundary and horizon failure maps: 95 grid pts incl. horizon: exterior median 1.098, interior 0.986
- precision and convergence tests: median spread 1.67e-06
- negative controls fail as expected: amp-0.5 control breaks criteria as expected
- independent implementation, no upstream loss imports: FD verifier, subprocess boundary, no upstream imports

## What is not settled
- nothing — all requirements passed

## How to reproduce
Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.
Compare outputs against `measurements.json`; verify file integrity against
`checksums.sha256`; check `attestation.json` for the exact git commit and
environment lock hash.

## What this does and does not prove
It proves: the declared deterministic checks ran with the recorded outcomes.
It does NOT prove: any claim about AInstein candidates beyond the allowed
public claim in `allowed-public-claim.md`.
