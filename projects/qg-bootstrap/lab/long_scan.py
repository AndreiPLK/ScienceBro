"""LONG SCAN through contour_lib only -- the previous version crashed.

The earlier scan computed the loop minimum inline and died with
OverflowError at large j (coefficients exceed 1e308 and float(c) overflows).
contour_lib.density already scales the polynomial by its largest coefficient,
which is exactly the fix; the inline copy did not have it. This version calls
the library and nothing else, so the class of bug cannot come back.

Purpose: get the block boundaries out to j = 160 for two families, so the
widths of the failing blocks form a long enough sequence to test
  (a) whether the +6 step in the measured widths (8, 14, 20) continues,
  (b) whether the boundaries carry one period or several (the founder's
      several-sources question) -- 27 sample points was too short to tell.

Writes incrementally so a crash costs nothing.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contour_lib import best_circle, self_test  # noqa: E402

OUT = Path("/tmp/long_scan2.json")
JS = list(range(8, 161, 2))
LAMS = [F(1), F(7)]


def main() -> int:
    bad = self_test()
    if bad:
        print("SELF-TEST FAILED, refusing to produce data:")
        for b in bad:
            print("  -", b)
        return 1
    print("contour_lib self-test: PASSED", flush=True)

    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for lam in LAMS:
        for j in JS:
            key = f"{j}|{lam}"
            if key in data:
                continue
            t0 = time.time()
            try:
                r, m = best_circle(j, j + 4, lam)
            except OverflowError as exc:      # must not happen; report loudly
                print(f"  j={j} lam={lam}: OVERFLOW {exc}", flush=True)
                data[key] = None
                OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
                continue
            data[key] = None if m is None else float(m)
            OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
            print(f"  j={j} lam={lam}: {'unstable' if m is None else f'{m:+.3e}'}"
                  f"  ({time.time() - t0:.1f}s)", flush=True)
    print("done:", len(data), "cells ->", OUT, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
