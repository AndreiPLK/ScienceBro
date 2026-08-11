"""Independent metric verifier for the AInstein audit.

INDEPENDENCE CONTRACT (roadmap §15):
- This package must NEVER import anything from the upstream checkout
  (projects/ainstein-audit/upstream/checkout) or its loss functions.
- It consumes metric values only through the MetricFunction interface:
  a callable mapping coordinates (4,) -> metric components (4, 4).
- It uses plain NumPy float64+ finite differences — a different mathematical
  route than upstream's TensorFlow autodiff, giving a genuine cross-check.
"""

from verifier.geometry import (
    christoffel,
    einstein_residual,
    kretschmann_scalar,
    lorentzian_signature_ok,
    ricci_scalar,
    ricci_tensor,
    riemann_tensor,
)
from verifier.known_metrics import minkowski, perturbed_schwarzschild, schwarzschild

__all__ = [
    "christoffel",
    "einstein_residual",
    "kretschmann_scalar",
    "lorentzian_signature_ok",
    "ricci_scalar",
    "ricci_tensor",
    "riemann_tensor",
    "minkowski",
    "perturbed_schwarzschild",
    "schwarzschild",
]
