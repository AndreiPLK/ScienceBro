---
id: CLAIM-LEGA-REDUCTION
statement: c_k = den^k * Delta^{L-1} phi(0) exactly, where phi_i = tau_i/C(L-1,i) and L = J-k; the sign factors cancel identically.
domain: every depth J, every coefficient index k, the whole far-below region
status: PROVED
proof_artifact: projects/qg-bootstrap/results/LEG_A_REDUCED_TO_ONE_LEMMA.md
last_verified: 2026-08-30
dependencies:
evidence:
  - the classical identity sum_i (-1)^i C(m,i) f(i) = (-1)^m Delta^m f(0)
  - the sign product (-1)^{J-1+k} (-1)^{L-1} = (-1)^{2J-2} = +1 since L = J-k
  - den = kk(kk-2) >= 53*51 > 0 on the region
references:
---

Turns leg (a) from a per-depth certificate into a single statement about one finite
difference: c_k >= 0 for all k at all depths follows if phi is absolutely monotone
(CLAIM-LEGA-LEMMA).

Two exact simplifications make phi explicit: the A_r are an arithmetic progression with
difference 2 den, and the reciprocal identity e_{N-k}(x) = (prod x) e_k(1/x) removes the
growing elementary function in favour of a FIXED one of order k.
