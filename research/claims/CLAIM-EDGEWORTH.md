---
id: CLAIM-EDGEWORTH
statement: log rho = 1/K'' + K''''/(2 K''^3) - K'''^2/K''^4 up to O(1/n^3), in the tilted cumulants.
domain: n = 41..201, theta = 0.2..0.45
status: MEASURED
last_verified: 2026-08-29
dependencies:
  - CLAIM-POISSON
evidence:
  - residual falls like 1/n^3, scaled column flat to about 5 percent (edgeworth_prediction.json)
  - the Gaussian term alone leaves O(1/n^2)
references:
---

The SHAPE of the expansion, verified as a rate. MEASURED and not PROVED because it carries no
remainder bound; supplying one is exactly Gap 2.
