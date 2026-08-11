"""Independent curvature computation from metric components via finite differences.

Route: metric g(x) -> central-difference derivatives -> Christoffel -> Riemann ->
Ricci -> scalar -> vacuum residual. No autodiff, no upstream code.

All computations are float64 (or longdouble where requested). Step sizes are
explicit arguments so convergence studies can sweep them.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

# A MetricFunction maps coordinates x (shape (4,)) to metric components (4, 4).
MetricFunction = Callable[[np.ndarray], np.ndarray]

DIM = 4


def _d1(g: MetricFunction, x: np.ndarray, h: float) -> np.ndarray:
    """First derivatives d_c g_ab, shape (c, a, b), 4th-order central differences."""
    out = np.empty((DIM, DIM, DIM))
    for c in range(DIM):
        e = np.zeros(DIM)
        e[c] = h
        out[c] = (
            -g(x + 2 * e) + 8 * g(x + e) - 8 * g(x - e) + g(x - 2 * e)
        ) / (12 * h)
    return out


def christoffel(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Christoffel symbols of the second kind, shape (a, b, c) = Gamma^a_{bc}."""
    gx = g(x)
    ginv = np.linalg.inv(gx)
    dg = _d1(g, x, h)  # dg[c, a, b] = d_c g_ab
    # Gamma^a_{bc} = 1/2 g^{ad} (d_b g_dc + d_c g_db - d_d g_bc)
    term = np.einsum("bdc->dbc", dg) + np.einsum("cdb->dbc", dg) - dg
    return 0.5 * np.einsum("ad,dbc->abc", ginv, term)


def riemann_tensor(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Riemann tensor R^a_{bcd} via finite differences of Christoffel symbols."""
    gamma = christoffel(g, x, h)
    dgamma = np.empty((DIM, DIM, DIM, DIM))  # dgamma[c, a, b, d] = d_c Gamma^a_{bd}
    for c in range(DIM):
        e = np.zeros(DIM)
        e[c] = h
        dgamma[c] = (
            -christoffel(g, x + 2 * e, h)
            + 8 * christoffel(g, x + e, h)
            - 8 * christoffel(g, x - e, h)
            + christoffel(g, x - 2 * e, h)
        ) / (12 * h)
    # R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb}
    #           + Gamma^a_{ce} Gamma^e_{db} - Gamma^a_{de} Gamma^e_{cb}
    r = (
        np.einsum("cadb->abcd", dgamma)
        - np.einsum("dacb->abcd", dgamma)
        + np.einsum("ace,edb->abcd", gamma, gamma)
        - np.einsum("ade,ecb->abcd", gamma, gamma)
    )
    return r


def ricci_tensor(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Ricci tensor R_bd = R^a_{bad}."""
    return np.einsum("abad->bd", riemann_tensor(g, x, h))


def ricci_scalar(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> float:
    ginv = np.linalg.inv(g(x))
    return float(np.einsum("bd,bd->", ginv, ricci_tensor(g, x, h)))


def kretschmann_scalar(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> float:
    """K = R_abcd R^abcd."""
    gx = g(x)
    ginv = np.linalg.inv(gx)
    r_up = riemann_tensor(g, x, h)  # R^a_{bcd}
    r_low = np.einsum("ae,ebcd->abcd", gx, r_up)          # R_abcd
    r_upup = np.einsum("bf,cg,dh,afgh->abcd", ginv, ginv, ginv, r_up)  # R^{abcd}
    return float(np.einsum("abcd,abcd->", r_low, r_upup))


def einstein_residual(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Vacuum Einstein residual G_ab = R_ab - 1/2 R g_ab (zero for vacuum, Lambda=0).

    For vacuum, R_ab = 0 alone is equivalent; we return the full Einstein tensor so
    trace effects are visible too.
    """
    gx = g(x)
    ric = ricci_tensor(g, x, h)
    rs = float(np.einsum("bd,bd->", np.linalg.inv(gx), ric))
    return ric - 0.5 * rs * gx


def normalized_vacuum_residual(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> float:
    """Primary metric (predeclared in H-0001): Frobenius norm of Ricci normalized by
    a characteristic curvature scale sqrt(K) (Kretschmann), avoiding division blowup
    where K ~ 0 by flooring with 1.

    normalized_independent_einstein_residual = |Ricci|_F / max(sqrt(K), 1)
    """
    ric = ricci_tensor(g, x, h)
    k = abs(kretschmann_scalar(g, x, h))
    return float(np.linalg.norm(ric) / max(np.sqrt(k), 1.0))


def lorentzian_signature_ok(g: MetricFunction, x: np.ndarray) -> bool:
    """True when the metric has signature (-,+,+,+) (one negative eigenvalue) and
    negative determinant."""
    gx = g(x)
    if not np.allclose(gx, gx.T, atol=1e-12):
        return False
    eig = np.linalg.eigvalsh(gx)
    return bool(np.linalg.det(gx) < 0 and np.sum(eig < 0) == 1)
