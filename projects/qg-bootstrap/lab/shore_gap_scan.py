"""Where the first knife zero comes closest to the shore -- locating the extremal point.

WHY.  results/FFP_LITERATURE_PASS.md sec. 3c reformulated the keystone as one
scalar inequality: the first zero of the knife in D must not fall below the
shore.  The same section measured that the room is a few percent at worst, so any
proof must handle the EXTREMAL configuration exactly.  This file finds it.

WHAT IS MEASURED.  For each (n, j, lam), the first zero D0 of K_{j-1} in D, by
exact bisection (every evaluation is exact fmpq; the bisection only chooses which
exact evaluation to run), and the ratio D0 / T_hat.  ALL knife orders are scanned
and the parity is recorded, not assumed: the first version of this file skipped
odd j because sec. 6b of BFORM_POSITIVITY_THEOREM.md said odd knives never turn
negative.  They do -- 72 of them in the first run -- and both engines agree
(ERR-0016).  The D -> infinity limit forces EVEN j to end up negative; it says
nothing about a finite-D dip, and odd j dips.

READING THE RESULT.  inf over the grid of D0/T_hat is the margin the keystone
has.  If it drifts toward 1 in some corner, that corner is where the theorem
lives or dies; if it stays bounded away, the shore has room and the difficulty is
elsewhere.

Run: python lab/shore_gap_scan.py -> results/shore_gap_scan.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ffp_convolution_check import K_from_conv, conv_e  # noqa: E402
from moment_kernel_probe import shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
CAP = fmpq(10) ** 9


def K_at(n: int, r: int, lam: fmpq, D: fmpq) -> fmpq:
    return K_from_conv(conv_e(n, r, lam, (D + 4 * n - 7) / 2))


def first_zero(n: int, r: int, lam: fmpq, steps: int = 60) -> fmpq | None:
    """First D > 3 where K_r changes sign; None if it stays positive up to the cap."""
    lo = fmpq(7, 2)
    if K_at(n, r, lam, lo) <= 0:
        return lo
    hi = fmpq(4)
    while K_at(n, r, lam, hi) > 0:
        hi *= 2
        if hi > CAP:
            return None
    for _ in range(steps):
        mid = (lo + hi) / 2
        if K_at(n, r, lam, mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> int:
    t0 = time.time()
    ns = (6, 8, 10, 12, 16, 20, 28, 40)
    lams = (fmpq(1, 10), fmpq(1, 2), fmpq(1), fmpq(5, 2), fmpq(7), fmpq(30), fmpq(100), fmpq(300))
    rows, odd_with_zero = [], []
    best = None
    for lam in lams:
        T_hat = shore(lam)[0]
        for n in ns:
            for j in range(3, n):
                r = j - 1
                z = first_zero(n, r, lam)
                if z is None:
                    rows.append(
                        {
                            "n": n,
                            "j": j,
                            "lam": str(lam),
                            "D0": None,
                            "ratio": None,
                            "odd_j": j % 2 == 1,
                        }
                    )
                    continue
                ratio = float(z / T_hat)
                if j % 2 == 1:
                    odd_with_zero.append(
                        {"n": n, "j": j, "lam": str(lam), "D0": float(z), "ratio": ratio}
                    )
                rows.append(
                    {
                        "n": n,
                        "j": j,
                        "lam": str(lam),
                        "T_hat": float(T_hat),
                        "D0": float(z),
                        "ratio": ratio,
                        "odd_j": j % 2 == 1,
                    }
                )
                if best is None or ratio < best["ratio"]:
                    best = {"ratio": ratio, "n": n, "j": j, "lam": str(lam), "D0": float(z)}
    below = [x for x in rows if x["ratio"] is not None and x["ratio"] < 1]
    out = {
        "what": "first knife zero in D against the shore: D0 / T_hat over a wide grid",
        "reading": "the infimum is the room the keystone has; a ratio below 1 would refute "
        "the physical claim outright",
        "rows": rows,
        "rows_below_one": below,
        "n_rows_below_one": len(below),
        "closest_approach": best,
        "odd_knife_orders_with_a_zero": odd_with_zero,
        "n_odd_with_zero": len(odd_with_zero),
        "closest_approach_odd_j": min(odd_with_zero, key=lambda x: x["ratio"])
        if odd_with_zero
        else None,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "shore_gap_scan.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"rows {len(rows)}   below 1: {len(below)}   odd-j zeros (should be 0): {len(odd_with_zero)}"
    )
    print(f"closest approach: {best}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
