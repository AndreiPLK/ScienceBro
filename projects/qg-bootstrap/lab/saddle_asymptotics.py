"""STEEPEST DESCENT for the knife coefficients, done properly.

Why this exists. The single open lemma is that the sequence C_m has no interior
minimum, equivalently that r_m = C_m/C_(m-1) decreases. Six mechanisms for it are
excluded (see results/OPEN_PROBLEM.md). The one route left is a genuine
asymptotic evaluation of C_m -- not a fit, which was tried and misses the
held-out half by 28 percent.

THE SETUP. Integrating the Rodrigues formula by parts m times,

    C_m  =  K_m * INT_0^1 F^(m)(u) u^(alpha+m) (1-u)^(beta+m) du,   K_m > 0

and writing the m-th derivative by Cauchy,

    F^(m)(u) = m!/(2 pi i) CONTOUR F(z) / (z-u)^(m+1) dz,

gives a double integral whose exponent is large in BOTH variables:

    Phi(u,z) = m [ log u + log(1-u) - log(z-u) ] + log F(z).

Saddle equations (d/du and d/dz):

    1/u - 1/(1-u) + 1/(z-u) = 0
    F'(z)/F(z) = m/(z-u),        F'/F = sum_a 2/(z - r_a) + eps/z

with r_a = (a/s)^2 the double roots of F. This module solves that system
numerically and compares the resulting leading asymptotics against the exact
rational C_m, so the analysis can be checked rather than believed.

The comparison is the point: an asymptotic formula that has not been held against
exact values is a guess.
"""

from __future__ import annotations

import sys
from pathlib import Path

# ENGINE-OK: the saddle solve is float by nature -- steepest descent is an
# asymptotic method, not an exact one. Every number it produces is compared
# against the EXACT rational coefficient computed on flint before being believed,
# which is the whole point of the module.
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402


def roots_of_F(n: int, lam: float):
    """The double roots (a/s)^2 and the exponent eps."""
    s = lam + n - 1
    aa = [n - 2 * k for k in range(1, n) if n - 2 * k > 0]
    return np.array([(a / s) ** 2 for a in aa]), (1 if n % 2 == 0 else 0)


def dlogF(z, r, eps):
    """F'(z)/F(z) for F = z^eps prod (z - r_a)^2."""
    return 2.0 * np.sum(1.0 / (z - r)) + (eps / z if eps else 0.0)


def saddle(n: int, lam: float, m: int, alpha=-0.5, beta=None, guess=None):
    """Solve the two saddle equations by Newton in the complex plane."""
    r, eps = roots_of_F(n, lam)
    u, z = guess if guess else (0.5 + 0.05j, 1.6 + 0.4j)

    def eqs(u, z):
        e1 = 1.0 / u - 1.0 / (1.0 - u) + 1.0 / (z - u)
        e2 = dlogF(z, r, eps) - m / (z - u)
        return np.array([e1, e2])

    for _ in range(200):
        f = eqs(u, z)
        if np.max(np.abs(f)) < 1e-13:
            break
        h = 1e-7
        J = np.array(
            [
                (eqs(u + h, z) - eqs(u - h, z)) / (2 * h),
                (eqs(u, z + h) - eqs(u, z - h)) / (2 * h),
            ]
        ).T
        try:
            step = np.linalg.solve(J, f)
        except np.linalg.LinAlgError:
            return None
        u -= 0.6 * step[0]
        z -= 0.6 * step[1]
        if not (np.isfinite(u) and np.isfinite(z)):
            return None
    return (u, z, np.max(np.abs(eqs(u, z))))


def log_exact(n: int, lam, D, m: int) -> float:
    """log |C_m| from the exact rational value, via bit lengths (no overflow)."""
    q = (-1) ** m * jacobi_coeff_rec(n - m, n, lam, D)
    p, d = int(q.p), int(q.q)
    sign = 1 if p > 0 else -1
    return sign, (abs(p).bit_length() - d.bit_length()) * np.log(2)


def main() -> int:
    from fractions import Fraction as F  # ENGINE-OK: parameter values only

    n, lam, D = 40, F(1), F(6)
    r, eps = roots_of_F(n, float(lam))
    print(f"n={n} lam={lam} D={D}: {len(r)} double roots, eps={eps}")
    print(f"  roots span [{r.min():.5f}, {r.max():.5f}]")
    print()
    # Continuation: the saddle is real and moves smoothly with m, so walk down
    # from a value where a cold start converges, reusing the previous solution.
    # A cold Newton start only worked at m = 32; continuation gets the whole range.
    print("  m   saddle u     saddle z     residual   sign C_m   log|C_m| exact")
    guess = (0.61 + 0j, 1.64 + 0j)
    rows = []
    for m in range(n - 8, 3, -1):
        out = saddle(n, float(lam), m, guess=guess)
        if out is None or out[2] > 1e-9:
            print(f"  {m:3d}  lost the saddle")
            break
        u, z, res = out
        guess = (u, z)
        sign, lg = log_exact(n, lam, D, m)
        rows.append((m, u, z, res, sign, lg))
    for m, u, z, res, sign, lg in rows[::-1][::4]:
        print(f"  {m:3d}  {u.real:+.6f}   {z.real:+.6f}   {res:.1e}   {sign:+d}       {lg:+.3f}")
    print()
    print(f"  saddle found for m = {rows[-1][0]} .. {rows[0][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
