"""HIGH-PRECISION block scan -- the only scan whose large-j numbers mean anything.

Paid for tonight: the float scan reported dips of -1e-16 for j = 80..92 and
exactly 0.0 from j = 94 at lam = 1. Both are artefacts. Worse, `best_circle`
then picks the radius from that noise, and a rigorous check at that radius
returned -3.75e+12 -- twelve orders of magnitude wrong, the same failure mode
as bug 3 in contour_lib's header, arriving by a new route.

Everything here goes through contour_lib.verdict_hp: ball arithmetic from the
radius search to the final sign, so a reported `dip` or `dip_free` is a proven
statement about the sampled points.

Tests the frozen closed form (results/FROZEN_PREDICTION_blocks.md):
    block k at lam = 1 occupies j = 2k(2k+3) .. 4k(k+3)
    -> block 4 = 88..112, block 5 = 130..160
and asks whether lam = 7 obeys the same form with different coefficients.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contour_lib import self_test, verdict_hp  # noqa: E402

OUT = Path("/tmp/hp_scan.json")
JOBS = [
    (F(1), list(range(76, 125, 2))),  # the predicted block 4 and its gaps
    (F(7), list(range(8, 125, 2))),
]  # independent family, whole range


def main() -> int:
    bad = self_test()
    if bad:
        print("SELF-TEST FAILED, refusing to produce data:", *bad, sep="\n  - ")
        return 1
    print("contour_lib self-test: PASSED", flush=True)
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for lam, js in JOBS:
        for j in js:
            key = f"{j}|{lam}"
            if key in data:
                continue
            t0 = time.time()
            v = verdict_hp(j, j + 4, lam)
            data[key] = v
            OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
            print(
                f"  j={j:3d} lam={str(lam):<3s} {v['status']:<9s} "
                f"mid={v.get('mid', 0.0):+.3e} rad={v.get('rad', 0.0):.1e} "
                f" ({time.time() - t0:.0f}s)",
                flush=True,
            )
    print("done:", len(data), "cells ->", OUT, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
