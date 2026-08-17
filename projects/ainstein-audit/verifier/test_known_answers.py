"""Known-answer scientific tests for the independent verifier (roadmap §15 baseline).

Tolerances below were calibrated on analytic cases on 2026-08-11 (see
verifier/CALIBRATION.md) BEFORE any candidate metric was inspected.
Run:  uv run pytest projects/ainstein-audit/verifier/ -v
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.geometry import (  # noqa: E402
    kretschmann_scalar,
    lorentzian_signature_ok,
    normalized_vacuum_residual,
    ricci_tensor,
)
from verifier.known_metrics import (  # noqa: E402
    invalid_signature,
    kretschmann_schwarzschild_analytic,
    minkowski,
    perturbed_schwarzschild,
    schwarzschild,
)

# Predeclared tolerances (calibrated on analytic baselines 2026-08-11 at h=3e-3,
# see CALIBRATION.md; candidates were NOT inspected before fixing these):
RICCI_VACUUM_TOL = 1e-7  # max |R_ab| for exact vacuum solutions at test points
KRETSCHMANN_REL_TOL = 1e-7  # relative error vs analytic K = 48 M^2/r^6
PERTURBED_MIN_RESIDUAL = 1e-5  # negative control must exceed this

TEST_POINTS = [
    np.array([0.0, 6.0, 1.2, 0.7]),
    np.array([1.0, 10.0, 0.9, 2.1]),
    np.array([-2.0, 25.0, 2.0, 4.0]),
]


@pytest.mark.parametrize("x", TEST_POINTS)
def test_minkowski_is_vacuum(x):
    ric = ricci_tensor(minkowski, x)
    assert np.max(np.abs(ric)) < RICCI_VACUUM_TOL


@pytest.mark.parametrize("x", TEST_POINTS)
def test_schwarzschild_is_vacuum(x):
    ric = ricci_tensor(schwarzschild, x)
    assert np.max(np.abs(ric)) < RICCI_VACUUM_TOL


@pytest.mark.parametrize("x", TEST_POINTS)
def test_schwarzschild_kretschmann_known_answer(x):
    k = kretschmann_scalar(schwarzschild, x)
    k_true = kretschmann_schwarzschild_analytic(x[1])
    assert abs(k - k_true) / k_true < KRETSCHMANN_REL_TOL


@pytest.mark.parametrize("x", [TEST_POINTS[0], TEST_POINTS[1]])
def test_perturbed_schwarzschild_detected(x):
    """Negative control: deliberately non-vacuum metric must NOT pass.

    Checked only inside the perturbation's support (Gaussian centered at r=6,
    width 2): at r=25 the perturbation is exp(-90) ~ 0 and the metric is honestly
    vacuum there — see test below.
    """
    res = normalized_vacuum_residual(perturbed_schwarzschild, x)
    assert res > PERTURBED_MIN_RESIDUAL


def test_perturbation_is_local():
    """Far outside the perturbation support the control correctly returns to vacuum —
    demonstrates the verifier distinguishes regions, not just whole metrics."""
    x = np.array([-2.0, 25.0, 2.0, 4.0])
    assert normalized_vacuum_residual(perturbed_schwarzschild, x) < 1e-7


@pytest.mark.parametrize("x", TEST_POINTS)
def test_signature_checks(x):
    assert lorentzian_signature_ok(schwarzschild, x)
    assert lorentzian_signature_ok(minkowski, x)
    assert not lorentzian_signature_ok(invalid_signature, x)


def test_residual_converges_with_step():
    """Convergence sanity: smaller FD step should not increase Schwarzschild residual
    by orders of magnitude (guards against using a step in the noise-dominated regime)."""
    x = np.array([0.0, 8.0, 1.1, 0.3])
    r_coarse = np.max(np.abs(ricci_tensor(schwarzschild, x, h=3e-2)))
    r_fine = np.max(np.abs(ricci_tensor(schwarzschild, x, h=3e-3)))
    assert r_fine < r_coarse  # truncation-dominated regime: finer step must improve
    assert r_fine < RICCI_VACUUM_TOL
