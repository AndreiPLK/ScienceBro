"""Where the largest real root crosses 1, against where the shore is.

THE REFORMULATION.  results/FFP_LITERATURE_PASS.md sec. 3 gives
A_m = C(r,m) K_{r-m}(D-2m), so "no real zero of the reduced Schur-Szego
composition in [1, inf)" is the positivity of the whole diagonal staircase.  Two
measurements turn that into a one-parameter picture:

  (i) the certified bound c*(D) on the largest real root is NON-DECREASING in D
      -- which is the programme's step (c) monotonicity seen in root-location
      coordinates, since each A_m is a knife and each knife decreases in D;
  (ii) therefore there is a single crossing point D_cross(n, r, lam) where c*
      passes 1, and the physical claim "every knife positive below the shore"
      becomes "D_cross >= T_hat".

WHAT THIS FILE MEASURES.  D_cross by exact bisection (the Descartes test is
exact; the bisection only picks which exact test to run), the ratio
D_cross / T_hat, and the monotonicity of c* in D as a check that the bisection
is meaningful.  A ratio below 1 anywhere would REFUTE the reformulation; the
worst ratio is therefore the number to watch, not the average.

NOTE ON WHAT c* IS.  Descartes is sufficient, not necessary, so c* over-estimates
the largest real root and D_cross UNDER-estimates the true crossing.  Every ratio
reported here is therefore a lower bound on the truth -- the safe direction.

Run: python lab/root_crossing_probe.py -> results/root_crossing_probe.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ffp_convolution_check import conv_e, no_real_root_above, reduced_poly  # noqa: E402
from moment_kernel_probe import shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def staircase_holds(n: int, r: int, lam: fmpq, D: fmpq) -> bool:
    """No real zero in [1, inf) -- equivalently every A_m > 0, exactly."""
    H = (D + 4 * n - 7) / 2
    return no_real_root_above(reduced_poly(conv_e(n, r, lam, H)), fmpq(1))


def crossing(n: int, r: int, lam: fmpq, T_hat: fmpq, steps: int = 30) -> fmpq | None:
    """Largest D (bisected) at which the staircase still holds; None if it fails low."""
    lo = fmpq(7, 2)
    if not staircase_holds(n, r, lam, lo):
        return None
    hi = T_hat * 8
    if staircase_holds(n, r, lam, hi):
        return hi
    for _ in range(steps):
        mid = (lo + hi) / 2
        if staircase_holds(n, r, lam, mid):
            lo = mid
        else:
            hi = mid
    return lo


def monotone_steps(n: int, r: int, lam: fmpq, T_hat: fmpq) -> tuple[int, int]:
    """Once the staircase fails at some D it must never hold again, if c* rises with D."""
    seen_fail = False
    steps = viol = 0
    for num in range(1, 17):
        D = T_hat * fmpq(num, 4)
        if D <= 3:
            continue
        ok = staircase_holds(n, r, lam, D)
        steps += 1
        if seen_fail and ok:
            viol += 1
        seen_fail = seen_fail or not ok
    return steps, viol


def main() -> int:
    t0 = time.time()
    rows = []
    worst = None
    tot_steps = tot_viol = 0
    for n in (6, 8, 12, 16, 20, 28, 40, 60):
        for lam in (fmpq(1), fmpq(5, 2), fmpq(7), fmpq(30), fmpq(300)):
            T_hat = shore(lam)[0]
            for r in sorted({2, n // 2, n - 2}):
                Dc = crossing(n, r, lam, T_hat)
                st, vi = monotone_steps(n, r, lam, T_hat)
                tot_steps += st
                tot_viol += vi
                ratio = float(Dc / T_hat) if Dc is not None else None
                rows.append(
                    {
                        "n": n,
                        "r": r,
                        "lam": str(lam),
                        "T_hat": float(T_hat),
                        "D_cross": float(Dc) if Dc is not None else None,
                        "D_cross_over_T_hat": ratio,
                        "monotone_steps": st,
                        "monotone_violations": vi,
                    }
                )
                if ratio is not None and (worst is None or ratio < worst[0]):
                    worst = (ratio, n, r, str(lam))
    below_one = [
        x for x in rows if x["D_cross_over_T_hat"] is not None and x["D_cross_over_T_hat"] < 1
    ]
    out = {
        "what": "D_cross (largest D where the diagonal staircase still holds) against the shore T_hat",
        "reading": "D_cross/T_hat >= 1 everywhere means the root-location reformulation covers the "
        "whole physical interval; Descartes makes every ratio a LOWER bound on the truth",
        "rows": rows,
        "rows_with_ratio_below_1": len(below_one),
        "worst_ratio": {"ratio": worst[0], "n": worst[1], "r": worst[2], "lam": worst[3]}
        if worst
        else None,
        "monotonicity": {"steps": tot_steps, "violations": tot_viol},
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "root_crossing_probe.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"rows {len(rows)}   ratios below 1: {len(below_one)}")
    print(f"worst D_cross/T_hat = {worst[0]:.3f} at n={worst[1]}, r={worst[2]}, lam={worst[3]}")
    print(f"monotonicity in D: {tot_viol} violations in {tot_steps} steps")
    for x in rows[:: max(1, len(rows) // 12)]:
        print(
            f"   n={x['n']:3d} r={x['r']:3d} lam={x['lam']:>4}  "
            f"D_cross/T_hat = {x['D_cross_over_T_hat']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
