---
id: CLAIM-HIER-RUNGS
statement: For every t in 1..4 and r in 3..8, Delta^r log p_t < 0 for every n in the domain of the claim (n >= 2(t+r)+1).
domain: t = 1..4, r = 3..8, all n with the difference window inside the first half
status: PROVED
proof_artifact: projects/qg-bootstrap/results/THEOREM_HIERARCHY_RUNGS.md
last_verified: 2026-08-30
dependencies:
evidence:
  - 24 polynomial inequalities, degrees 38 to 4089, each with all coefficients nonnegative after an explicit shift
  - every shift is smaller than the domain requirement 2(t+r)+1, so each rung is complete rather than partial
  - e_t interpolations verified at five nodes beyond those they were built from
  - each rung spot-checked against the reference sign computation at six n; 0 mismatches
references:
---

An all-nonnegative-coefficients argument is a proof, not a measurement, and each rung
covers infinitely many n.

r = 3 IS conjecture (B); the eighteen rungs with r >= 4 are new and do not follow from
it, which settles that the hierarchy is genuinely deeper than (B) rather than a
restatement of it.

Uniformity in (t, r) is open: degrees grow like 3(t+r)2^r so no computation reaches all
rungs. The shifts depend on the PARITIES of t and r, not only their sizes, and explaining
that parity is the likely way in.
