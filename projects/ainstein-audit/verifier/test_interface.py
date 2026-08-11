"""End-to-end interface test: exported NN metric → independent verifier.

Skipped when the isolated upstream environment or the smoke checkpoint is absent
(e.g. in CI) — the interface is machine-local by design.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.interface import CHECKOUT, UPSTREAM_PY, export_points  # noqa: E402

SMOKE_MODEL = "runs/dummy-kjjf3e3e_2026-08-11_13-51-44/final_model.keras"

pytestmark = pytest.mark.skipif(
    not UPSTREAM_PY.exists() or not (CHECKOUT / SMOKE_MODEL).exists(),
    reason="isolated upstream env / smoke checkpoint not present",
)


def test_export_shape_symmetry_signature():
    pts = np.array([[0.1, 0.2], [0.0, 0.0], [-0.2, 0.4]], dtype=np.float64)
    g, meta = export_points(SMOKE_MODEL, pts)
    assert g.shape == (3, 2, 2)
    assert meta["metric_dim"] == 2
    assert np.allclose(g, np.swapaxes(g, 1, 2))
    for i in range(len(g)):
        eig = np.linalg.eigvalsh(g[i])
        assert np.linalg.det(g[i]) < 0 and (eig < 0).sum() == 1  # 2D Lorentzian
