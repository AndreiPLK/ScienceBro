"""Independent Petrov-type diagnostics (stage-4 requirement).

Implemented from the standard definitions, NOT from upstream code:

  1. Weyl tensor in 4D from our own finite-difference Riemann/Ricci:
       C_abcd = R_abcd + (1/2)(g_ad R_bc + g_bc R_ad - g_ac R_bd - g_bd R_ac)
                + (1/6) R (g_ac g_bd - g_ad g_bc)
  2. An orthonormal Lorentzian tetrad at the point (eigen-decomposition of g;
     the single negative-eigenvalue direction becomes e_0).
  3. Electric/magnetic parts in that frame:
       E_ij = C_{0i0j},   B_ij = (1/2) eps_ikl C^{kl}_{ 0j}  (frame indices)
     and the complex traceless 3x3 Weyl operator Q = E + iB.
  4. Its eigenvalues l1,l2,l3 (sum ~ 0) give the two algebraic invariants
       I = (l1^2 + l2^2 + l3^2)/2 = -e2,      J = l1 l2 l3 = e3
     and the speciality index in the discriminant normalisation
       S = 27 J^2 / (4 I^3),
     which equals 1 exactly for algebraically special geometries (types D, N, II,
     III) and differs from 1 for algebraically general type I.

Known-answer validation (run as a test, not asserted here): analytic Schwarzschild
is type D, so S must come out 1 within the finite-difference floor, and Minkowski is
degenerate (I = J = 0) so S is undefined and reported as such.

Note on conventions: the paper uses S = 27J^2/I^3 with its own I, J normalisation and
also quotes S = 1 for type D. Both conventions agree on the S = 1 boundary, which is
the only thing used for a type-D/type-I decision here.
"""

from __future__ import annotations

import numpy as np

from verifier.geometry import (
    MetricFunction,
    ricci_scalar,
    ricci_tensor,
    riemann_tensor,
)


def weyl_tensor(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Fully covariant Weyl tensor C_abcd (4D)."""
    gx = g(x)
    r_up = riemann_tensor(g, x, h)  # R^a_bcd
    r_low = np.einsum("ae,ebcd->abcd", gx, r_up)  # R_abcd
    ric = ricci_tensor(g, x, h)
    rs = ricci_scalar(g, x, h)
    term = 0.5 * (
        np.einsum("ad,bc->abcd", gx, ric)
        + np.einsum("bc,ad->abcd", gx, ric)
        - np.einsum("ac,bd->abcd", gx, ric)
        - np.einsum("bd,ac->abcd", gx, ric)
    )
    scal = (rs / 6.0) * (np.einsum("ac,bd->abcd", gx, gx) - np.einsum("ad,bc->abcd", gx, gx))
    return r_low + term + scal


def orthonormal_tetrad(gx: np.ndarray) -> np.ndarray:
    """Return e[a, mu]: frame vectors with g(e_a, e_b) = diag(-1, 1, 1, 1).

    Uses the eigen-decomposition of the symmetric metric; the unique negative
    eigenvalue direction becomes the timelike leg.
    """
    vals, vecs = np.linalg.eigh(gx)
    order = np.argsort(vals)  # most negative first
    vals, vecs = vals[order], vecs[:, order]
    if vals[0] >= 0 or np.any(vals[1:] <= 0):
        raise ValueError(f"not a Lorentzian metric: eigenvalues {vals}")
    e = np.zeros((4, 4), dtype=np.float64)
    for a in range(4):
        e[a] = vecs[:, a] / np.sqrt(abs(vals[a]))
    return e


def weyl_operator(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> np.ndarray:
    """Complex traceless 3x3 Weyl operator Q = E + iB in an orthonormal frame."""
    gx = g(x)
    e = orthonormal_tetrad(gx)
    c = weyl_tensor(g, x, h)
    # frame components C_abcd (all indices frame indices, lowered)
    cf = np.einsum("am,bn,cp,dq,mnpq->abcd", e, e, e, e, c)
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])

    e_part = np.zeros((3, 3), dtype=np.float64)
    for i in range(3):
        for j in range(3):
            e_part[i, j] = cf[0, i + 1, 0, j + 1]

    # C^{kl}_{0j} in the frame: raise the first two indices with eta
    c_up2 = np.einsum("km,ln,mnpq->klpq", eta, eta, cf)
    eps = np.zeros((3, 3, 3), dtype=np.float64)
    for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        eps[i, j, k] = 1.0
        eps[i, k, j] = -1.0
    b_part = np.zeros((3, 3), dtype=np.float64)
    for i in range(3):
        for j in range(3):
            s = 0.0
            for k in range(3):
                for m in range(3):
                    s += eps[i, k, m] * c_up2[k + 1, m + 1, 0, j + 1]
            b_part[i, j] = 0.5 * s

    q = e_part + 1j * b_part
    # enforce the algebraic properties the definition guarantees
    q = 0.5 * (q + q.T)
    q = q - np.trace(q) / 3.0 * np.eye(3)
    return q


def petrov_invariants(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> dict:
    """Return I, J, speciality index S and the eigenvalues (as measured)."""
    q = weyl_operator(g, x, h)
    lam = np.linalg.eigvals(q)
    i_inv = float(np.real(np.sum(lam**2) / 2.0)) + 1j * float(np.imag(np.sum(lam**2) / 2.0))
    j_inv = complex(np.prod(lam))
    denom = 4.0 * i_inv**3
    s = complex(27.0 * j_inv**2 / denom) if abs(denom) > 0 else complex("nan")
    return {
        "eigenvalues": [complex(v) for v in lam],
        "trace_abs": float(abs(np.trace(q))),
        "I": complex(i_inv),
        "J": j_inv,
        "S": s,
        "abs_S_minus_1": float(abs(s - 1.0)) if np.isfinite(abs(s)) else float("nan"),
        "weyl_scale": float(np.linalg.norm(q)),
    }
