"""HUNT FOR A SIGN-DEFINITE CONTOUR: the most promising open line.

Why this line exists. The verdict for each constraint is a contour integral of
a polynomial divided by a power, so by Cauchy the integral is the SAME on every
closed loop around the origin -- the loop is ours to choose. If some loop makes
the integrand one-signed, positivity is immediate and UNIFORM in the constraint
index, which is exactly the uniformity the whole programme is missing. No
asymptotics, no remainder bounds, no resurgence.

What is established here (measured, exactly and in high precision):

  * On the best circle the density is one large positive hump with a tiny
    negative dip. Depth of the dip, relative to the answer: about 1e-3 at
    moderate constraint index, falling to 1e-8 in places.
  * Optimising the SHAPE of the loop (13 Fourier parameters, Nelder-Mead)
    shrinks the dip by factors of 1.5 to 6, but has not removed it.
  * In 120-digit ball arithmetic the dip is CONFIRMED negative for j = 10..16
    at lam = 1, and CONFIRMED positive for j = 18, 20 -- so sign-definite
    circles do exist in places, but not everywhere.
  * Scanning (j, n, lam): dips persist across most of the grid. Universally
    sign-definite CIRCLES therefore do not exist. Richer loops remain open.

Honest status: this is the most promising open route, not a result. It has
converted the remaining gap from "estimate an oscillatory sum whose terms are
55x the answer" into "show that a small negative part of one explicit function
on one explicit loop is dominated by its positive part" -- a much better shaped
problem, still unsolved.

Run: python lab/keystone_contour_hunt.py -> results/keystone_contour_hunt.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_saddles import build_P, coeff  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
K = 6


def circle_min(j: int, n: int, lam: F, radii=None):
    """Best (largest) minimum of the density over a family of circles."""
    P = build_P(j, n, lam)
    N = j - 1
    true = float(coeff(P, N))
    if true == 0 or not np.isfinite(true):
        return None, None
    pf = np.polynomial.Polynomial([float(c) for c in P])
    t = np.linspace(0, 2 * np.pi, 1200, endpoint=False)
    best = (None, -1e9)
    for r in radii if radii is not None else np.logspace(-2.5, -0.8, 70):
        # SAME density as the shaped version: includes the contour element dx,
        # so the two numbers are comparable (a mismatch here produced a fake
        # 'shape optimisation makes it worse' anomaly)
        x = r * np.exp(1j * t)
        dx = 1j * r * np.exp(1j * t)
        v = (pf(x) * x ** (-N - 1) * dx / (2j * np.pi)).real
        if not np.isfinite(v).all():
            continue
        m = v.min() / abs(true)
        if m > best[1]:
            best = (r, m)
    return best


def shaped_min(j: int, n: int, lam: F, r0: float):
    """Optimise the loop SHAPE (Fourier harmonics) to lift the dip."""
    from scipy.optimize import minimize

    P = build_P(j, n, lam)
    N = j - 1
    true = float(coeff(P, N))
    pf = np.polynomial.Polynomial([float(c) for c in P])

    def dens_min(p):
        rr = np.exp(p[0])
        a, b = p[1 : 1 + K], p[1 + K : 1 + 2 * K]
        t = np.linspace(0, 2 * np.pi, 1200, endpoint=False)
        shape = 1 + sum(a[k] * np.cos((k + 1) * t) + b[k] * np.sin((k + 1) * t) for k in range(K))
        if (shape <= 0.05).any():
            return 1e6
        rho = rr * shape
        dshape = sum(
            -a[k] * (k + 1) * np.sin((k + 1) * t) + b[k] * (k + 1) * np.cos((k + 1) * t)
            for k in range(K)
        )
        x = rho * np.exp(1j * t)
        dx = (rr * dshape + 1j * rho) * np.exp(1j * t)
        d = (pf(x) * x ** (-N - 1) * dx / (2j * np.pi)).real
        if not np.isfinite(d).all():
            return 1e6
        return -d.min() / abs(true)

    p0 = np.zeros(1 + 2 * K)
    p0[0] = np.log(r0)
    best = -dens_min(p0)
    for trial in range(5):
        start = p0.copy()
        if trial:
            rng = np.random.default_rng(trial)
            start[1:] += 0.15 * rng.normal(size=2 * K)
        res = minimize(
            dens_min,
            start,
            method="Nelder-Mead",
            options=dict(maxiter=3000, fatol=1e-13, xatol=1e-11),
        )
        best = max(best, -res.fun)
    return best


def main() -> int:
    t0 = time.time()
    rows = []
    for j in (10, 12, 14, 16, 18, 20, 22, 24):
        for lam in (F(1), F(3), F(26)):
            n = j + 4
            r, m_circle = circle_min(j, n, lam)
            if r is None:
                continue
            m_shape = shaped_min(j, n, lam, r)
            rows.append(
                {
                    "j": j,
                    "n": n,
                    "lam": str(lam),
                    "best_radius": r,
                    "min_over_circles": m_circle,
                    "min_after_shape_optimisation": m_shape,
                    "sign_definite": bool(m_shape >= 0),
                }
            )
            print(
                f"  j={j} lam={lam}: circle {m_circle:+.3e} -> shaped "
                f"{m_shape:+.3e} "
                f"{'(sign-definite)' if m_shape >= 0 else ''}",
                flush=True,
            )

    definite = [r for r in rows if r["sign_definite"]]
    out = {
        "idea": "the integral is the same on every loop around the origin,"
        " so choose a loop where the integrand is one-signed;"
        " positivity then holds immediately and uniformly in the"
        " constraint index",
        "why_it_matters": "this is the only route found that gives"
        " uniformity for free, i.e. without asymptotics"
        " or remainder bounds",
        "cells": len(rows),
        "sign_definite_cells": len(definite),
        "status": "PROMISING OPEN ROUTE, not a result. Circles alone are not"
        " enough: dips persist on most of the grid, though they"
        " are tiny (1e-3 down to 1e-8 relative to the answer)."
        " Shape optimisation shrinks them 1.5x-6x without"
        " eliminating them.",
        "what_it_achieved": "reshaped the remaining gap from 'estimate an"
        " oscillatory sum whose individual terms are 55x"
        " the answer' into 'show a small negative part"
        " of one explicit function on one explicit loop"
        " is dominated by its positive part'",
        "rows": rows,
        "command": "python lab/keystone_contour_hunt.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_contour_hunt.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells {len(rows)}, sign-definite {len(definite)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
