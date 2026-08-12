"""Independent trapped-surface / horizon diagnostics.

Third and last leg of the black-hole claim (vacuum + type I + trapped interior).
Implemented from the standard 2+2 split, NOT from upstream code.

The metric family is block diagonal: a 2D Lorentzian block in (T, X) times a
2-sphere written in stereographic coordinates, so the angular block carries the
areal radius R:

    g_q1q1 = g_q2q2 = 4 R^2 / (1 + q1^2 + q2^2)^2
    =>  R(T, X, q) = sqrt( g_q1q1 * (1 + |q|^2)^2 / 4 )

With h_ab the 2D block metric (a, b in {T, X}) the standard quantity is

    Xi = h^ab (d_a R)(d_b R)

    Xi > 0 : R has a spacelike gradient -> untrapped (normal) region
    Xi < 0 : R has a timelike gradient -> trapped OR anti-trapped region
    Xi = 0 : marginally trapped surface (apparent horizon)

The orientation is fixed by the two future-directed null normals l, n of the block
(h_ab l^a l^b = 0, l^T > 0). Their expansions satisfy theta_l ∝ (2/R) l^a d_a R and
theta_n ∝ (2/R) n^a d_a R, so

    theta_l < 0 AND theta_n < 0  ->  future-trapped (black-hole interior)
    theta_l > 0 AND theta_n > 0  ->  past-trapped (white-hole / anti-trapped)

Known answers used as controls (analytic Schwarzschild in the same coordinates):
exterior region gives Xi > 0, interior (r < 2m) gives Xi < 0 with both expansions
negative, and R must agree with the independent Lambert-W r(T, X).
"""

from __future__ import annotations

import numpy as np

from verifier.geometry import MetricFunction


def areal_radius(g: MetricFunction, x: np.ndarray) -> float:
    """R from the angular block; also usable as a consistency check (q1 vs q2)."""
    gx = g(x)
    n = 1.0 + x[2] ** 2 + x[3] ** 2
    r_sq_1 = gx[2, 2] * n**2 / 4.0
    r_sq_2 = gx[3, 3] * n**2 / 4.0
    if r_sq_1 <= 0 or r_sq_2 <= 0:
        raise ValueError(f"non-positive angular block: {r_sq_1}, {r_sq_2}")
    return float(np.sqrt(0.5 * (r_sq_1 + r_sq_2)))


def angular_isotropy(g: MetricFunction, x: np.ndarray) -> float:
    """Relative difference between the two angular diagonal entries (0 if isotropic)."""
    gx = g(x)
    a, b = gx[2, 2], gx[3, 3]
    return float(abs(a - b) / max(abs(a) + abs(b), 1e-300) * 2.0)


def trapping_diagnostics(g: MetricFunction, x: np.ndarray, h: float = 3e-3) -> dict:
    """Return Xi, the null expansions' signs and the trapping classification."""
    r0 = areal_radius(g, x)

    # gradient of R in the 2D block (T, X), angular coordinates held fixed
    grad = np.zeros(2, dtype=np.float64)
    for a in range(2):
        xp, xm = x.copy(), x.copy()
        xp[a] += h
        xm[a] -= h
        grad[a] = (areal_radius(g, xp) - areal_radius(g, xm)) / (2.0 * h)

    hh = np.array(g(x))[:2, :2]
    if np.linalg.det(hh) >= 0:
        raise ValueError(f"2D block is not Lorentzian: det={np.linalg.det(hh):.3e}")
    hinv = np.linalg.inv(hh)
    xi = float(grad @ hinv @ grad)

    # future-directed null directions of the block: h_ab l^a l^b = 0, l^T > 0
    a_, b_, c_ = hh[1, 1], 2.0 * hh[0, 1], hh[0, 0]      # for l = (1, s)
    disc = b_**2 - 4.0 * a_ * c_
    if disc < 0:
        raise ValueError("no real null directions in the block")
    s1 = (-b_ + np.sqrt(disc)) / (2.0 * a_)
    s2 = (-b_ - np.sqrt(disc)) / (2.0 * a_)
    l_vec = np.array([1.0, s1])
    n_vec = np.array([1.0, s2])

    dr_l = float(l_vec @ grad)
    dr_n = float(n_vec @ grad)

    # Time orientation: "future = increasing x^0" is only meaningful where the first
    # coordinate is timelike (h_00 < 0). Inside a Schwarzschild-coordinate horizon the
    # roles of t and r swap, so the orientation must be reported as ambiguous instead
    # of guessed. In the Penrose coordinates used for the models h_00 = -F < 0 holds.
    time_orientable = bool(hh[0, 0] < 0)
    if xi > 0:
        cls = "untrapped"
    elif not time_orientable:
        cls = "trapped (orientation ambiguous: x^0 is spacelike here)"
    elif dr_l < 0 and dr_n < 0:
        cls = "future-trapped"
    elif dr_l > 0 and dr_n > 0:
        cls = "past-trapped (anti-trapped)"
    else:
        cls = "trapped (mixed null signs — inspect numerically)"

    return {
        "areal_radius": r0,
        "angular_isotropy_rel": angular_isotropy(g, x),
        "grad_R_T": float(grad[0]),
        "grad_R_X": float(grad[1]),
        "Xi": xi,
        "theta_l_sign_proxy": dr_l,
        "theta_n_sign_proxy": dr_n,
        "time_orientable": time_orientable,
        "classification": cls,
    }
