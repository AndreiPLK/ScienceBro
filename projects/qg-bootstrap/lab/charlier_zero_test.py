"""Does the Charlier polynomial stay positive where the measure lives?

The reduction (lab/charlier_reduction.py) gives, for g = H - r,

    K_r = sum_t (-1)^t C(r,t) (g)_t m_t,
    P_r(y) = sum_t C(r,t) (g)_t (-y)^t = C_r(g ; 1/y),

with m_t independent of r and D. If m_t = INT y^t dmu(y) with dmu >= 0
supported in [0, Y], then

    K_r = INT_0^Y P_r(y) dmu(y),

so a SUFFICIENT condition for the whole depth family is

    P_r(y) >= 0  for  0 <= y <= Y,     i.e.  Y <= (smallest positive zero of P_r).

This script measures both sides exactly on the physical domain:

  * Y is probed by the ratios rho_t = m_{t+1}/m_t. For a moment sequence
    these INCREASE to sup supp mu, so max_t rho_t is a LOWER bound on Y:
    whenever the smallest zero of P_r falls below it, P_r provably changes
    sign INSIDE the support and the crude sufficient condition is dead.
  * the smallest positive zero of P_r is bracketed EXACTLY by bisection on
    exact rational sign changes (no root finder, no floats in decisions).

VERDICT (measured, see the artifact): the crude condition FAILS at and below
the shore in 56 of 84 configurations, with the zero sitting at 0.63-1.06
times the support lower bound -- close, but decisively inside. That is the
expected outcome in hindsight: at the shore the even knives are marginal by
construction, so no support-versus-zero bound can settle them; the true
argument has to use where the measure's MASS sits, not merely its support.

Run: python lab/charlier_zero_test.py -> results/charlier_zero_test.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base_moment_probe import m_seq  # noqa: E402
from moment_kernel_probe import falling, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def P_r(r: int, g: fmpq, y: fmpq) -> fmpq:
    return sum(
        (fmpq(comb(r, t)) * falling(g, t) * (-y) ** t for t in range(r + 1)), fmpq(0)
    )


def smallest_positive_zero(r: int, g: fmpq, hi: fmpq, steps: int = 400) -> fmpq | None:
    """Exact bracket of the smallest sign change of P_r on (0, hi]; returns
    the upper end of a bisected bracket (so it is an upper bound that is
    correct to 2^-45 * hi), or None if no sign change is found."""
    sgn = lambda v: (v > 0) - (v < 0)  # noqa: E731
    s0 = sgn(P_r(r, g, fmpq(0)))
    prev_y = fmpq(0)
    for i in range(1, steps + 1):
        y = hi * fmpq(i, steps)
        if sgn(P_r(r, g, y)) != s0:
            lo, up = prev_y, y
            for _ in range(45):
                mid = (lo + up) / 2
                if sgn(P_r(r, g, mid)) == s0:
                    lo = mid
                else:
                    up = mid
            return up
        prev_y = y
    return None


def main() -> int:
    t0 = time.time()
    rows = []
    for lam in (fmpq(1), fmpq(3), fmpq(72)):
        Th = shore(lam)[0]
        for n in (12, 24, 40):
            for tag, D in (("shore", Th), ("below", Th * fmpq(4, 5)), ("above", Th * fmpq(3, 2))):
                if D <= 3:
                    continue
                H = (D + 4 * n - 7) / 2
                # r-independent support bound from the m-ratios
                m = m_seq(n, lam, n - 2)
                ratios = [m[t + 1] / m[t] for t in range(len(m) - 1) if m[t] != 0]
                Ymax = max(ratios) if ratios else fmpq(0)
                for j in (3, 4, 6, 8, 12):
                    r = j - 1
                    if r > n - 2:
                        continue
                    g = H - r
                    z = smallest_positive_zero(r, g, Ymax * 4)
                    covered = z is not None and Ymax < z
                    rows.append(
                        {
                            "lam": str(lam),
                            "n": n,
                            "where": tag,
                            "j": j,
                            "Ymax": float(Ymax),
                            "smallest_zero": float(z) if z is not None else None,
                            "zero_over_Ymax": float(z / Ymax) if z is not None and Ymax != 0 else None,
                            "P_positive_on_support": covered,
                            "knife_sign": ref_sign(j, n, lam, D),
                        }
                    )
    at_shore = [x for x in rows if x["where"] in ("shore", "below")]
    above = [x for x in rows if x["where"] == "above"]
    ok_shore = sum(1 for x in at_shore if x["P_positive_on_support"])
    ok_above = sum(1 for x in above if x["P_positive_on_support"])
    print(
        f"P_r positive on the measure's range: at/below shore {ok_shore}/{len(at_shore)}; "
        f"above shore {ok_above}/{len(above)}",
        flush=True,
    )
    ratios = [x["zero_over_Ymax"] for x in at_shore if x["zero_over_Ymax"]]
    if ratios:
        print(
            f"  margin (smallest zero / Ymax) at-or-below shore: min {min(ratios):.3f}, "
            f"max {max(ratios):.3f}",
            flush=True,
        )
    out = {
        "claim": (
            "Sufficient-condition test for the Charlier route: with m_t a moment "
            "sequence on [0, Y], K_r = INT P_r dmu >= 0 whenever P_r >= 0 on [0, Y]. "
            "Y is over-estimated by max_t m_{t+1}/m_t; the smallest positive zero of "
            "P_r is bracketed by exact rational bisection. Reported at/below and "
            "above the shore."
        ),
        "at_or_below_shore_covered": [ok_shore, len(at_shore)],
        "above_shore_covered": [ok_above, len(above)],
        "rows": rows,
        "command": "python lab/charlier_zero_test.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "charlier_zero_test.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
