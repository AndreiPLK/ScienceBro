# Proof pack: Public release (stage-6)

**Status: IN PROGRESS**

**Question:** Can an independent person reproduce everything from a clean clone with verified citations and licenses?

**Why it matters:** A release that cannot be reproduced is marketing, not science.

## What passed
- clean-clone reproduction: C:\Users\user\ScienceBro\projects\ainstein-audit\proof\stage-01\clean-clone-2026-08-11.log
- CI pass: 2 workflow(s) defined
- license audit: upstream licenses recorded incl. the GPL-2.0 / MIT conflict
- AI-use disclosure: C:\Users\user\ScienceBro\AI_DISCLOSURE.md

## What is not settled
- citation verification (missing): CITATION.cff present, 0 corpus entries content-verified
- complete proof packs for all stages (missing): 5 of 6 stages have a full proof pack
- GitHub release + Zenodo DOI (missing): 

## How to reproduce
Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.
Compare outputs against `measurements.json`; verify file integrity against
`checksums.sha256`; check `attestation.json` for the exact git commit and
environment lock hash.

## What this does and does not prove
It proves: the declared deterministic checks ran with the recorded outcomes.
It does NOT prove: any claim about AInstein candidates beyond the allowed
public claim in `allowed-public-claim.md`.
