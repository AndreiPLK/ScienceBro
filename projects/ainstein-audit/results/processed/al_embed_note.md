# Side observation: supervised seed vs unsupervised interim (2026-08-11)

Data: `al_embed_seed_check.json` (AL_embed supervised seed) vs `known_answer_4d.json`
nn_interim (unsupervised, 31/500 epochs). Same 4 exterior probe points, same
independent FD route, h=3e-3, float64.

| Model | max\|Ricci\| range | Kretschmann rel. err range | Signature |
| --- | --- | --- | --- |
| AL_embed (supervised on analytic metric components) | 0.064 – 0.149 | 1.5% – 8.2% | Lorentzian ✓ |
| Unsupervised interim (31/500 epochs, from this seed family) | 0.092 – 0.178 | 0.4% – 1.7% | Lorentzian ✓ |

## Measured observation (no claim beyond these numbers)

Componentwise-supervised metric fitting does not deliver curvature accuracy: the
supervised seed's Kretschmann error (1.5–8.2%) is worse than a 6%-trained unsupervised
PINN's (0.4–1.7%), consistent with second-derivative error amplification. Curvature
must be checked directly — pointwise metric closeness is not evidence of geometric
closeness.

## Consequence for the audit protocol

- The NN-metric residual floor for frozen thresholds must come from the FULLY TRAINED
  unsupervised Schwarzschild baseline, not from supervised seeds.
- `seed_models/old/` (11 architecture variants) remains useful for §15 check 19
  (parameter/checkpoint perturbation tests), not for floor calibration.
