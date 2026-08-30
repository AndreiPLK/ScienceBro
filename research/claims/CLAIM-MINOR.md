---
id: CLAIM-MINOR
statement: H_{N,t} = p_{t+1}^3 p_{t-1} - p_t^3 p_{t+2} equals det[[p_t^2, p_{t+1}^2],[T_t, T_{t+1}]] with T_t = p_t^2 - p_{t-1}p_{t+1}.
domain: any positive sequence p; verified for the centred family at 860 (n,t) pairs
status: PROVED
proof_artifact: projects/qg-bootstrap/results/MINOR_REPRESENTATION.md
last_verified: 2026-08-30
dependencies:
evidence:
  - three-line derivation from the definition of the Turan determinant
  - verified against the direct expression at 860 (n,t) pairs over n = 6..45, 0 mismatches
  - all 2x2 minors of the 2xN matrix [p^2 ; T] on the first half are nonnegative, 274 tested, 0 negative
references:
---

A reformulation, not a decision: that the determinant is NONNEGATIVE is exactly (B), which
remains open in general.

Its value is that (B) now has the shape total-positivity machinery expects -- a 2xN matrix
whose 2x2 minors are the quantity to be signed. That is what two routes in the recent
literature were trying to construct.

No conflict with CLAIM-NOPF: that concerns the Toeplitz array of p, a different matrix.
