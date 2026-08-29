"""Checking the limit-shape bound f(theta) < 2, and the step of it that was wrong.

The proof is in results/LIMIT_SHAPE_BOUND.md.  It arrived from a second assistant
(untrusted input, so every step is checked here) and one step needed repair: the
factorisation of Phi(3z/(z+2)) - z^2 was printed with (z-1) where it must be
(z-1)^2, which flips its sign and breaks the argument.  With the square the
argument is correct.

What this file checks:
  1. the reformulation f = 2/(t-c) - 1/(1-t) - 1/t against the direct f;
  2. the equivalence f < 2  <=>  c < Phi(t), including at the crossing;
  3. the monotonicity numerator 4t^4 - 8t^3 + 8t - 1 > 0 where it is used;
  4. the Shafer-Fink consequence z > 14/37;
  5. the CORRECTED factorisation, against direct evaluation;
  6. the printed one, to record that it does not reproduce.

Run: python lab/limit_shape_check.py -> results/limit_shape_check.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from mpmath import atan, mp, mpf, sqrt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
mp.dps = 40


def t_of(u):
    return atan(u) / u


def c_of(u):
    return 1 / (1 + u**2)


def f_direct(u):
    th = 1 - t_of(u)
    dth = atan(u) / u**2 - 1 / (u * (1 + u**2))
    return (2 / u) / dth - 1 / th - 1 / (1 - th)


def Phi(t):
    return t * (-1 + 4 * t - 2 * t**2) / (1 + 2 * t - 2 * t**2)


def main() -> int:
    t0 = time.time()
    tol = mpf(10) ** (-25)
    us = [mpf(x) / 100 for x in range(5, 267, 3)]  # up to just past the crossing

    reform = max(
        abs(f_direct(u) - (2 / (t_of(u) - c_of(u)) - 1 / (1 - t_of(u)) - 1 / t_of(u))) for u in us
    )
    equiv_bad = sum(1 for u in us if (f_direct(u) < 2) != (c_of(u) < Phi(t_of(u))))
    mono_bad = sum(1 for u in us if (lambda t: 4 * t**4 - 8 * t**3 + 8 * t - 1)(t_of(u)) <= 0)
    sf_bad = sum(1 for u in us if t_of(u) > mpf(1) / 2 and 1 / sqrt(1 + u**2) <= mpf(14) / 37)

    zs = [mpf(x) / 100 for x in range(38, 100, 2)]
    corrected_bad = printed_bad = 0
    for z in zs:
        true = Phi(3 * z / (z + 2)) - z**2
        corrected = (
            -z * (z - 1) ** 2 * (11 * z**2 + 28 * z - 12) / ((z + 2) * (11 * z**2 - 16 * z - 4))
        )
        printed = -z * (z - 1) * (11 * z**2 + 28 * z - 12) / ((z + 2) * (11 * z**2 - 16 * z - 4))
        corrected_bad += abs(true - corrected) > tol
        printed_bad += abs(true - printed) > tol

    out = {
        "statement": "f(theta) < 2 on (0, 1/2), with theta = 1 - arctan(u)/u",
        "source": "second-assistant PDF, 2026-08-29; untrusted, hence checked here",
        "reformulation_max_error": float(reform),
        "equivalence_failures": equiv_bad,
        "monotonicity_numerator_failures": mono_bad,
        "shafer_fink_failures": sf_bad,
        "points_checked_u": len(us),
        "factorisation": {
            "z_points": len(zs),
            "corrected_(z-1)^2_mismatches": corrected_bad,
            "printed_(z-1)_mismatches": printed_bad,
        },
        "crossing_u_where_f_equals_2": 2.6586,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "limit_shape_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"reformulation max error {float(reform):.2e}; equivalence failures {equiv_bad}; "
        f"monotonicity failures {mono_bad}; Shafer-Fink failures {sf_bad}"
    )
    print(
        f"factorisation over {len(zs)} z: corrected (z-1)^2 mismatches {corrected_bad}, "
        f"printed (z-1) mismatches {printed_bad}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
