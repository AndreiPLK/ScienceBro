---
id: CLAIM-HIER-RUNGS
statement: For every t in 1..14 and r in 3..9, Delta^r log p_t < 0 for every n in the domain of the claim (n >= 2(t+r)+1).
domain: t = 1..14, r = 3..9, all n with the difference window inside the first half
status: PROVED
proof_artifact: projects/qg-bootstrap/results/THEOREM_HIERARCHY_RUNGS.md
last_verified: 2026-08-30
dependencies:
evidence:
  - 98 polynomial inequalities, degrees 38 to 18936, each with all coefficients nonnegative after an explicit shift
  - every shift is smaller than the domain requirement 2(t+r)+1, so each rung is complete rather than partial
  - e_t interpolations verified at five nodes beyond those they were built from
  - each rung spot-checked against the reference sign computation at six n each; 0 mismatches in 98 rungs
references:
---

An all-nonnegative-coefficients argument is a proof, not a measurement, and each rung
covers infinitely many n.

r = 3 IS conjecture (B); the eighteen rungs with r >= 4 are new and do not follow from
it, which settles that the hierarchy is genuinely deeper than (B) rather than a
restatement of it.

Uniformity in (t, r) is open: degrees grow like 3(t+r)2^r so no computation reaches all
rungs. The shift excess obeys an EXACT parity law -- 0 when t and r have opposite parity, 2 or 3
when the same -- which yields CLAIM-U2: the single statement that would prove the whole
hierarchy. CLAIM-U, the first and stronger form, is DISPROVED.
