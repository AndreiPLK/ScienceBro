"""Independent r(T,X) for the upstream Penrose-diagram convention.

Reimplemented from the documented formula (upstream geometry/schwarzschild.py
PenroseRadiusWeighting) using scipy — NOT by importing upstream code. Exterior
region BI (X > |T|):

  arccoth(z) = 0.5 ln((z+1)/(z-1)),  z = cos(2T)/cos(2X)
  r = 2m (1 + W(exp(-2 arccoth(z) - 1)))

Interior regions BII/BIV use arctanh and W(-exp(-2 arctanh(z) - 1)).
"""

from __future__ import annotations

import numpy as np
from scipy.special import lambertw


def r_of_TX(T: float, X: float, m: float = 1.0) -> float:
    z = np.cos(2.0 * T) / np.cos(2.0 * X)
    if abs(z) > 1.0:  # exterior BI/BIII
        arccoth = 0.5 * np.log((z + 1.0) / (z - 1.0))
        w = lambertw(np.exp(-2.0 * arccoth - 1.0)).real
    else:  # interior BII/BIV
        arctanh = np.arctanh(z)
        w = lambertw(-np.exp(-2.0 * arctanh - 1.0)).real
    return 2.0 * m * (1.0 + w)


def kretschmann_analytic(T: float, X: float, m: float = 1.0) -> float:
    """K = 48 m^2 / r^6 with the independent r(T,X)."""
    r = r_of_TX(T, X, m)
    return 48.0 * m**2 / r**6
