"""Analytic test metrics for known-answer and negative-control checks.

Coordinates: (t, r, theta, phi) in Schwarzschild coordinates; G = c = 1.
"""

from __future__ import annotations

import numpy as np


def minkowski(x: np.ndarray) -> np.ndarray:
    """Flat spacetime, signature (-,+,+,+), spherical spatial part."""
    _, r, theta, _ = x
    return np.diag([-1.0, 1.0, r**2, (r * np.sin(theta)) ** 2])


def schwarzschild(x: np.ndarray, mass: float = 1.0) -> np.ndarray:
    """Schwarzschild exterior metric (r > 2M)."""
    _, r, theta, _ = x
    f = 1.0 - 2.0 * mass / r
    return np.diag([-f, 1.0 / f, r**2, (r * np.sin(theta)) ** 2])


def perturbed_schwarzschild(x: np.ndarray, mass: float = 1.0, eps: float = 1e-3) -> np.ndarray:
    """Deliberate NON-solution: Schwarzschild with a smooth non-vacuum perturbation.

    Negative control — the verifier MUST flag this as non-vacuum.
    """
    _, r, _, _ = x
    g = schwarzschild(x, mass)
    g[0, 0] *= 1.0 + eps * np.exp(-((r - 6.0) ** 2) / 4.0)
    return g


def invalid_signature(x: np.ndarray) -> np.ndarray:
    """Deliberately broken metric (two negative eigenvalues) — signature control."""
    _, r, theta, _ = x
    return np.diag([-1.0, -1.0, r**2, (r * np.sin(theta)) ** 2])


def kretschmann_schwarzschild_analytic(r: float, mass: float = 1.0) -> float:
    """Known answer: K = 48 M^2 / r^6 for Schwarzschild."""
    return 48.0 * mass**2 / r**6
