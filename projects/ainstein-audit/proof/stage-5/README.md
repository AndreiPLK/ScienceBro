# Proof pack: Scientific verdict (stage-5)

**Status: IN PROGRESS**

**Question:** Is every claim mapped to evidence and independently validated, with exact allowed wording?

**Why it matters:** The verdict is only as strong as its weakest unsupported claim.

## What passed
- complete claim-to-evidence mapping: 2 promoted claims, all mapped to evidence/experiments
- independent validation decision recorded: VAL-0001:fail, VAL-0002:pass, VAL-0003:pass, VAL-0004:pass
- all contradictions and limitations recorded: 2 promoted claims record their own limitations openly
- exact allowed public wording fixed: 2/2 promoted claims carry exact allowed wording
- PASS / FAIL / INCONCLUSIVE recorded: 3 pass / 1 fail recorded

## What is not settled
- reviewed by a qualified external expert (missing): 

## How to reproduce
Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.
Compare outputs against `measurements.json`; verify file integrity against
`checksums.sha256`; check `attestation.json` for the exact git commit and
environment lock hash.

## What this does and does not prove
It proves: the declared deterministic checks ran with the recorded outcomes.
It does NOT prove: any claim about AInstein candidates beyond the allowed
public claim in `allowed-public-claim.md`.
