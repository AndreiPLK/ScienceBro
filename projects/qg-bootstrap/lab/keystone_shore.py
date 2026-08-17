"""THE KEYSTONE, one inequality: does the D-threshold sit above the shore?

Given the verified Beta representation (results/keystone_beta.json),

    sign P_j(n, lam, D) = sign J(Q),   Q = D/2 + n - j - 2,

with J a polynomial in Q of degree j-1 whose coefficients are rational in
(n, lam) and COMPLETELY D-FREE.  Descartes on the coefficient list of J
bounds the number of positive roots; the observed count is 1-2, so the
positivity region in D is an interval [4, D*) and the whole "blades never
cut below the shore" statement becomes

        J(Q) > 0   for every Q in [Q(4), Q(T_hat(lam)) ),

i.e. ONE univariate polynomial inequality per (n, j, lam) instead of a
four-dimensional region.  This script measures it exactly:

  * sign of J at f = 0, 1/2, 9/10, 99/100 of the way to the shore
    (f = 1 is the shore itself, where the fleet is known to be tangent);
  * the exact threshold Q* by rational bisection on the sign of J;
  * the margin  (Q* - Q_shore)  -- positive means the kill window opens
    strictly ABOVE the shore, which is the theorem.

Run: python lab/keystone_shore.py -> results/keystone_shore.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_poly_in_Q, sign_changes  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

LAMS = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10), Fraction(1, 3),
        Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26), Fraction(150), Fraction(1000))
FRACS = (Fraction(0), Fraction(1, 2), Fraction(9, 10), Fraction(99, 100),
         Fraction(1))


def peval(poly: list[Fraction], x: Fraction) -> Fraction:
    v = Fraction(0)
    for c in reversed(poly):
        v = v * x + c
    return v


def threshold_Q(poly: list[Fraction], q_lo: Fraction, q_hi: Fraction,
                iters: int = 60):
    """Bisect for the sign change of J on [q_lo, q_hi]; None if no change."""
    a, b = peval(poly, q_lo), peval(poly, q_hi)
    if a <= 0:
        return "already_nonpositive_at_low_end"
    if b > 0:
        return None                      # positive on the whole stretch
    lo, hi = q_lo, q_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if peval(poly, mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> int:
    t0 = time.time()
    rows, violations, below_shore = [], [], []
    for j in range(2, 41):
        for n in range(max(4, j + 1), max(4, j + 1) + 24, 2):
            for lam in LAMS:
                Th = T_hat(lam)
                if Th <= 4:
                    continue
                poly = J_poly_in_Q(j, n, lam)
                Q_of = lambda D: Fraction(D, 2) + n - j - 2   # noqa: E731
                signs = {}
                for f in FRACS:
                    D = 4 + (Th - 4) * f
                    v = peval(poly, Q_of(D))
                    signs[str(f)] = int((v > 0) - (v < 0))
                    if f < 1 and v <= 0:
                        violations.append({"j": j, "n": n, "lam": str(lam),
                                           "f": str(f), "sign": signs[str(f)]})
                q_shore = Q_of(Th)
                thr = threshold_Q(poly, Q_of(Fraction(4)), q_shore)
                margin = None
                if isinstance(thr, Fraction):
                    margin = float(thr - q_shore)     # < 0 => cuts below
                    below_shore.append({"j": j, "n": n, "lam": str(lam),
                                        "Q_star": float(thr),
                                        "Q_shore": float(q_shore),
                                        "margin": margin})
                rows.append({"j": j, "n": n, "lam": str(lam),
                             "signs_by_f": signs,
                             "sign_changes_J": sign_changes(
                                 list(reversed(poly))),
                             "threshold": (str(thr) if not isinstance(
                                 thr, Fraction) else float(thr)),
                             "Q_shore": float(q_shore),
                             "margin_vs_shore": margin})
        print(f"  j={j}: rows {len(rows)}, strict-interior violations "
              f"{len(violations)} ({time.time()-t0:.0f}s)", flush=True)

    out = {"claim": "P_j > 0 strictly below the shore, for every knife j,"
                    " every n and every lam -- tested through the exact"
                    " one-variable polynomial J(Q)",
           "grid": {"j": "2..40", "n": "max(4,j+1) .. +24 step 2",
                    "lam": [str(x) for x in LAMS],
                    "f": [str(x) for x in FRACS]},
           "cells": len(rows),
           "strict_interior_violations": violations,
           "all_positive_strictly_below_shore": not violations,
           "threshold_inside_shore_cases": below_shore[:40],
           "threshold_inside_shore_count": len(below_shore),
           "sign_changes_seen": sorted({r["sign_changes_J"] for r in rows}),
           "rows": rows[:60],
           "command": "python lab/keystone_shore.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_shore.json").write_text(json.dumps(out, indent=1),
                                             encoding="utf-8")
    print(f"cells {len(rows)}; violations strictly below shore: "
          f"{len(violations)}; thresholds found inside [4, shore]: "
          f"{len(below_shore)}", flush=True)
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
