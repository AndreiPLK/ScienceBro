---
id: CLAIM-PROP1
statement: If every y-coefficient outside degrees J-2 and J-3 is nonnegative and (R) holds, then the far-below polynomial N(y) > 0 for y >= 0.
domain: every depth J
status: PROVED
proof_artifact: projects/qg-bootstrap/results/THEOREM_STATE.md
last_verified: 2026-08-29
dependencies:
  - CLAIM-TOPCOEF
evidence:
  - grouping argument: a quadratic with positive leading coefficient and nonpositive discriminant
references:
---

Group the three middle terms as `y^(J-3) (c_(J-1) y^2 + c_(J-2) y + c_(J-3))`. (R) makes the
discriminant nonpositive and CLAIM-TOPCOEF makes the leading coefficient positive, so the
quadratic is nonnegative; the remaining terms are nonnegative by hypothesis.

`c_(J-3) >= 0` is NOT a hypothesis: (R) bounds it below by a square over a positive number.
