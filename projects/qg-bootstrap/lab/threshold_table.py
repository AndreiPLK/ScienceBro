"""Exact table of n*(lam): the level above which q is clean at the shore.

Why this and not something else. The outside memorandum offers a coarse endpoint
model, n* ~ exp(2 gamma_shore/(lam+1)), and a sharper four-lobe model. Both are
asymptotic. What neither side has is a TABLE of exact thresholds to test them
against -- and exact thresholds are the one thing this side can produce and the
analysis cannot. First data point already: at lam = 1/8 the coarse formula says
819 and the true threshold is 744, an overshoot of 10 percent.

Each threshold is bisected to a single level and both sides are recorded, so the
entry is falsifiable: `dirty` at n*-1 and `clean` at n*.

Writes incrementally after every lam, so a kill at any point leaves valid data.

Run: python lab/threshold_table.py
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import machine_guard  # noqa: E402
from gegenbauer_flint import T_hat, q_poly, to_gegenbauer  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
OUT = RES / "threshold_table.json"

# cheapest first, so an interruption still leaves a useful table
# lam = 1/3 predicts n* ~ 2300 and is what exhausted memory on 18 Aug; excluded
# until the guard has been exercised on something smaller.
LAMS = [fmpq(1, 40), fmpq(1, 16), fmpq(1, 8), fmpq(1, 6), fmpq(1, 4), fmpq(1, 5)]
KNOWN = {"1/20": 516, "1/10": 660, "1/5": 1056, "1/8": 744}


def clean(n: int, lam: fmpq, g: fmpq) -> bool:
    # The appetite grows with n, so the check belongs HERE, not before the loop.
    # On 18 August the lam = 1/3 case walked to degree ~2300 and took the machine
    # from 31 GB free to 0.3 GB while a pre-flight check had happily passed.
    # Floor 4 GB, not the module default of 6: this job is the only heavy thing
    # running, and 4 GB still leaves the founder room to start a game -- at which
    # point free memory drops, the guard fires, and this job yields to him.
    machine_guard.check(machine_guard.floor_for(n), what=f"n={n}, lam={lam}")
    a = to_gegenbauer(q_poly(n, lam), g)
    return not any(c < 0 for c in a)


def bracket(lam: fmpq, g: fmpq, guess: int) -> tuple[int, int]:
    """Find lo dirty < hi clean around a predicted threshold, doubling outward."""
    lo = max(20, int(guess * 0.5))
    hi = max(lo + 20, int(guess * 1.6))
    while clean(lo, lam, g) and lo > 25:
        hi, lo = lo, max(20, lo // 2)
    while not clean(hi, lam, g):
        lo, hi = hi, hi * 2
        if hi > 20000:
            raise RuntimeError("threshold beyond 20000")
    return lo, hi


def main() -> int:
    rows = []
    if OUT.exists():
        try:
            rows = json.loads(OUT.read_text(encoding="utf-8")).get("rows", [])
        except (json.JSONDecodeError, OSError):
            rows = []
    done = {r["lam"] for r in rows}
    for lam in LAMS:
        key = str(lam)
        if key in done:
            continue
        t0 = time.time()
        g = T_hat(lam) / fmpq(2) - fmpq(3, 2)
        coarse = math.exp(2 * float(g) / (float(lam) + 1))
        print(f"lam={key}: shore={float(g):.5f}, coarse prediction {coarse:.0f}", flush=True)
        print("   " + machine_guard.note("this lam"), flush=True)
        try:
            lo, hi = bracket(lam, g, int(coarse))
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if clean(mid, lam, g):
                    hi = mid
                else:
                    lo = mid
                print(f"   {lo} .. {hi}   ({time.time() - t0:.0f}s)", flush=True)
        except machine_guard.MachineBusy as e:
            # Stop the whole run, not just this lam: memory does not come back on
            # its own, and the next lam is always more expensive than this one.
            print(f"   STOPPING: {e}", flush=True)
            print(f"   table kept with {len(rows)} rows at {OUT}", flush=True)
            return 0
        row = {
            "lam": key,
            "shore_gamma": str(g),
            "n_star": hi,
            "verified_dirty_at": lo,
            "coarse_prediction": round(coarse, 1),
            "coarse_error_pct": round(100 * (coarse - hi) / hi, 1),
            "seconds": round(time.time() - t0, 1),
        }
        rows.append(row)
        print(
            f"   -> n*({key}) = {hi}, coarse off by {row['coarse_error_pct']:+.1f}%\n", flush=True
        )
        OUT.write_text(
            json.dumps(
                {
                    "claim": "exact thresholds n*(lam): q is dirty at n*-1 and clean at n*, "
                    "every Gegenbauer coefficient checked in exact rational arithmetic",
                    "tests": "the outside memorandum's coarse endpoint model "
                    "n* ~ exp(2 gamma_shore/(lam+1))",
                    "independently_known": KNOWN,
                    "rows": rows,
                    "command": "python lab/threshold_table.py",
                    **stamp(),
                },
                indent=1,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
