"""The second-order shape g(theta): the one analytic ingredient the bridge still needs.

results/FINITE_N_BRIDGE.md reduces the finite-n half of the named lemma to an
effective expansion

    M_{n,t} = f(t/n) + g(t/n)/n + O(1/n^2),

with `f` already proved (< 2 on (0,1/2), results/LIMIT_SHAPE_BOUND.md).  Granting
such an expansion with a positive `g` and an explicit remainder, BOTH remaining
conjectures follow: the bound `M <= 2`, and (C), which is just the statement that
the central curvature descends monotonically -- its margin is of order 1/n^2,
which is what a positive `1/n` coefficient predicts.

This file measures `g` so that whoever proves the expansion has a target with
numbers.  At each theta it evaluates n(M - f) at several n and Richardson-
extrapolates in 1/n, which removes the leading O(1/n) contamination and gives a
value far closer to the limit than any single n.

Everything on the exact side is fmpq; `f` is evaluated by solving
theta = 1 - arctan(u)/u to 25 digits.

Run: python lab/second_order_shape.py -> results/second_order_shape.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq
from mpmath import atan, findroot, mp, mpf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
mp.dps = 30


def f_of(theta: float) -> float:
    th = mpf(theta)
    u = findroot(lambda z: 1 - atan(z) / z - th, mpf("1.0"))
    dth = atan(u) / u**2 - 1 / (u * (1 + u**2))
    return float((2 / u) / dth - 1 / th - 1 / (1 - th))


def M(n: int, t: int) -> float:
    N = n - 1
    E = E2_list(n, t + 1)
    p = [fmpq(E[j], comb(N, j)) for j in (t - 1, t, t + 1)]
    return float((p[1] * p[1] / (p[0] * p[2]) - 1) * n)


def main() -> int:
    t0 = time.time()
    rows = []
    for theta in (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49):
        fv = f_of(theta)
        raw = []
        for n in (120, 240):
            t = max(2, round(theta * n))
            raw.append((n, n * (M(n, t) - f_of(t / n))))
        (n1, a1), (n2, a2) = raw
        # Richardson in 1/n: a(n) = g + c/n  ->  g = (n2 a2 - n1 a1)/(n2 - n1)
        g = (n2 * a2 - n1 * a1) / (n2 - n1)
        rows.append(
            {
                "theta": theta,
                "f": round(fv, 6),
                "n_120": round(a1, 4),
                "n_240": round(a2, 4),
                "g_extrapolated": round(g, 4),
            }
        )
        print(
            f"   theta={theta:<5} f={fv:7.4f}   n(M-f) at 120: {a1:7.4f}, at 240: {a2:7.4f}"
            f"   ->  g ~ {g:7.4f}"
        )
    out = {
        "what": "the second-order coefficient g(theta) in M_{n,t} = f(t/n) + g(t/n)/n + O(1/n^2)",
        "why": "proving this expansion with explicit remainder closes BOTH remaining bridge "
        "conjectures at once -- the bound and (C)",
        "method": "n(M - f) evaluated at n = 120 and 240, Richardson-extrapolated in 1/n",
        "rows": rows,
        "max_g_on_the_needed_range": max(r["g_extrapolated"] for r in rows),
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "second_order_shape.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"  max g over theta <= 0.49: {out['max_g_on_the_needed_range']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
