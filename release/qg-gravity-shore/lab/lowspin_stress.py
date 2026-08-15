"""Low-spin stress test at the conjectured boundary.

Standalone generator for results/lowspin_stress.json (first run 2026-08-15 via
the night queue wrote a bare []; this script recreates the identical test and
persists it WITH run metadata, per the experiment contract).

For each lambda in a spread of values: D in [min_n T_n - 2, min_n T_n], even
D only, full first_negative scan (ALL even l <= 2n-2) to depth 20; alarm = any
kill at a point the completeness conjecture calls alive. Zero alarms = no
low-spin wave cuts deeper than the conjectured envelope on this grid.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import first_negative  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def min_T(lamf: float) -> float:
    return min((3 * (2 * n - 3) / (n * (n - 2)))
               * (lamf * lamf + (2 * n - 2) * lamf + 1) + 2 * n
               for n in range(3, 400))


def main() -> int:
    t0 = time.time()
    alarms = []
    checks = 0
    for lam in (F(1), F(3, 2), F(2), F(3), F(5), F(8)):
        Dtop = int(min_T(float(lam)))
        for D in range(max(4, Dtop - 2), Dtop + 1):
            if D % 2:
                continue
            checks += 1
            fn = first_negative(lam, D, 20)
            if fn is not None:
                alarms.append({"lam": str(lam), "D": D, "first_neg": fn})
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"alarms": alarms, "lambdas": ["1", "3/2", "2", "3", "5", "8"],
           "depth": 20, "window": "[minT-2, minT] even D", "checks": checks,
           "command": "python lab/lowspin_stress.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "lowspin_stress.json").write_text(json.dumps(out, indent=1),
                                             encoding="utf-8")
    print(f"low-spin stress: {len(alarms)} alarms in {checks} checks"
          f" (depth 20, all even l), {time.time()-t0:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
