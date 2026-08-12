"""Known-answer tests for the Petrov and trapping diagnostics.

These lock in the two new instruments: analytic Schwarzschild must read as
algebraically special (S = 1) and, in Schwarzschild coordinates, as untrapped
outside the horizon and trapped inside it.
"""

from __future__ import annotations

import numpy as np

from verifier.horizon import trapping_diagnostics
from verifier.known_metrics import minkowski, schwarzschild
from verifier.petrov import petrov_invariants, weyl_operator


def test_schwarzschild_is_algebraically_special():
    """Type D => speciality index exactly 1 (measured to machine precision)."""
    for r in (8.0, 12.0, 20.0):
        inv = petrov_invariants(schwarzschild, np.array([0.0, r, 1.1, 0.3]))
        assert inv["abs_S_minus_1"] < 1e-8, (r, inv["S"])


def test_weyl_operator_is_traceless_and_symmetric():
    q = weyl_operator(schwarzschild, np.array([0.0, 10.0, 1.0, 0.4]))
    assert abs(np.trace(q)) < 1e-10
    assert np.allclose(q, q.T, atol=1e-12)


def test_minkowski_weyl_vanishes():
    """Flat space has zero Weyl tensor, so the operator scale must be at the floor."""
    inv = petrov_invariants(minkowski, np.array([0.0, 5.0, 1.0, 0.4]))
    assert inv["weyl_scale"] < 1e-8, inv["weyl_scale"]


def _schwarzschild_areal_metric(x: np.ndarray) -> np.ndarray:
    """Schwarzschild in (t, r, theta, phi) has areal radius r in the angular block,
    but verifier.horizon expects the stereographic convention g_qq = 4R^2/(1+|q|^2)^2.
    Wrap the analytic metric so the angular block carries R = r in that convention."""
    g = np.array(schwarzschild(x), dtype=np.float64)
    r = x[1]
    n = 1.0 + x[2] ** 2 + x[3] ** 2
    g[2, 2] = 4.0 * r**2 / n**2
    g[3, 3] = 4.0 * r**2 / n**2
    return g


def test_trapping_outside_and_inside_horizon():
    """Schwarzschild (m=1, horizon r=2): untrapped outside, trapped inside.

    Uses the standard (t, r) block where dR/dr = 1, so
    Xi = h^rr = 1 - 2m/r: positive outside, negative inside.
    """
    out = trapping_diagnostics(_schwarzschild_areal_metric, np.array([0.0, 8.0, 0.2, 0.1]))
    assert out["Xi"] > 0, out
    assert out["classification"] == "untrapped", out
    assert abs(out["areal_radius"] - 8.0) < 1e-6

    inside = trapping_diagnostics(_schwarzschild_areal_metric, np.array([0.0, 1.2, 0.2, 0.1]))
    assert inside["Xi"] < 0, inside
    # In Schwarzschild coordinates the coordinate time is spacelike inside the horizon,
    # so the diagnostic must report trapping WITHOUT guessing an orientation.
    assert inside["classification"].startswith("trapped"), inside
    assert inside["time_orientable"] is False, inside
