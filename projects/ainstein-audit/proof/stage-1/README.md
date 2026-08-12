# Proof pack: Research infrastructure (stage-1)

**Status: VERIFIED** (ENGINEERING, not scientific)

**Question:** Does a clean clone reproduce the environment, schemas, tests and provenance tracking?

**Why it matters:** Without reproducible engineering, no scientific number can be trusted.

## What passed
- uv.lock present: 11704d4fd8fa9376
- clean-clone reproduction log: C:\Users\user\ScienceBro\projects\ainstein-audit\proof\stage-01\clean-clone-2026-08-11.log
- schema/gate unit tests pass: ..................                                                       [100%]
- upstream manifest with pinned commits: C:\Users\user\ScienceBro\vendor\upstream-manifest.yaml

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
