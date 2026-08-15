"""Gravity slice 4: the exclusion map lambda_min/max(D) from the derived brackets.

For each even D and each level n<=NMAX, the bracket q_hat_n(lam)*D+p_hat_n(lam)
(near-leading even trajectory, positive prefactors removed) excludes the lambda
interval where it is negative. Union over n = the excluded region at depth NMAX.
Exact rational endpoints via sympy solve on the stored symbolic brackets.

Output: results/grav_lambda_map.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import sympy as sp

RES = Path(__file__).resolve().parents[1] / "results"
lam, x, D = sp.symbols("lambda x D", positive=True)
NMAX = 16


def hat_bracket(n):
    mu = (n + lam - 1) / lam
    t = -mu * (1 - x) / 2
    Q = sp.prod([sp.Rational(1, 2) * (1 + lam) + lam * t + lam * (k - 1)
                 for k in range(1, n)])
    P = sp.expand(Q ** 2)
    co = sp.Poly(P, x).all_coeffs()[::-1]
    l = 2 * n - 4
    rho = sp.Rational((l + 1) * (l + 2), 2) / (D + 2 * l - 1)
    S = sp.simplify((co[2 * n - 4] + co[2 * n - 2] * rho) * (D + 2 * l - 1))
    return sp.expand(sp.cancel(S / (lam + n - 1) ** (2 * n - 4)))


def main() -> int:
    t0 = time.time()
    brackets = {n: hat_bracket(n) for n in range(3, NMAX + 1)}
    print(f"brackets built ({time.time()-t0:.0f}s)", flush=True)
    out = []
    for Dv in range(10, 41, 2):
        intervals = []
        for n, S in brackets.items():
            S4 = sp.expand(S.subs(D, Dv))
            roots = sp.solve(S4, lam)
            reals = sorted([sp.nsimplify(r) for r in roots if sp.im(r) == 0],
                           key=lambda r: float(r))
            if len(reals) == 2 and float(reals[0]) > 0:
                intervals.append({"n": n, "lo": str(reals[0]), "hi": str(reals[1]),
                                  "lo_f": float(reals[0]), "hi_f": float(reals[1])})
        if intervals:
            lo = min(i["lo_f"] for i in intervals)
            hi = max(i["hi_f"] for i in intervals)
        else:
            lo = hi = None
        out.append({"D": Dv, "excluded_union_approx": [lo, hi],
                    "per_level": intervals})
        print(f"D={Dv}: excluded lambda union ~ [{lo}, {hi}] "
              f"({len(intervals)} active levels)", flush=True)
    (RES / "grav_lambda_map.json").write_text(json.dumps(out, indent=1),
                                              encoding="utf-8")
    print("written grav_lambda_map.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
