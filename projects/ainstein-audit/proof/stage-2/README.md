# Proof pack: Verifier calibration (stage-2)

**Status: VERIFIED**

**Question:** Does the independent verifier reproduce known analytical answers and reject corrupted input?

**Why it matters:** Every later verdict about AI-found metrics rests on this instrument being calibrated.

## What passed
- analytical Minkowski vacuum: 3 tests passed
- analytical Schwarzschild vacuum + Kretschmann known answer: 6 tests passed
- corrupted metric rejected: 2 tests passed
- invalid signature rejected: 4 tests passed
- 4D Penrose-route analytic floor within thresholds: max|Ricci|=1.49e-08 (tol 1e-07), K rel err=1.15e-08 (tol 1e-07)
- FD-step sweep stable on NN metric: max/min ratio = 1.0002 over 4 steps
- float32 vs float64 sensitivity measured: float32 inflates median residual 203x -> float64 mandatory
- upstream loss replicated with independent Ricci (factor < 3): replica=8.08e-11 vs upstream=1.57e-10 (factor 1.94); sqrt(loss)=1.253e-05

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
