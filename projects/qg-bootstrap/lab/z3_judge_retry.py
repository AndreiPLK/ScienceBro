"""Retry the z3_judge 'unknown' cells: longer timeout + lam-interval splitting.

Reads results/z3_judge_j{J}.json, re-judges each unknown (k, m) with
Z3_TIMEOUT_MS (default 600000) and, if still unknown, splits the branch
lam-interval into 4 subintervals (unsat on all 4 = cell confirmed).
Artifact: results/z3_judge_j{J}_retry.json.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import Bj_coeffs
from z3_judge import judge_cell

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))


def branch_mu(kk):
    if kk == 3:
        return Fraction(1, 1000), Fraction(2, 3)
    lo = Fraction(3, 5) * (kk - Fraction(5, 2))
    if kk == 4:
        lo = Fraction(2, 3)
    return lo, Fraction(3, 5) * (kk - Fraction(3, 2))


def main() -> int:
    t0 = time.time()
    prev = json.loads((RES / f"z3_judge_j{J}.json").read_text())
    todo = [(c["k"], c["m"]) for c in prev["unknowns"]]
    confirmed, alarms, still = [], [], []
    for kk, mv in todo:
        lo, hi = branch_mu(kk)
        coeffs = Bj_coeffs(J, mv)
        verdict, model = judge_cell(coeffs, kk, lo, hi)
        if verdict == "unknown":
            parts, okp = 4, True
            for i in range(parts):
                a = lo + (hi - lo) * i / parts
                b = lo + (hi - lo) * (i + 1) / parts
                v2, m2 = judge_cell(coeffs, kk, a, b)
                if v2 == "SAT-ALARM":
                    alarms.append({"k": kk, "m": mv, "model": m2})
                    okp = False
                    break
                if v2 != "unsat":
                    okp = False
            (confirmed if okp else still).append({"k": kk, "m": mv})
        elif verdict == "SAT-ALARM":
            alarms.append({"k": kk, "m": mv, "model": model})
        else:
            confirmed.append({"k": kk, "m": mv})
        print(f"k={kk} m={mv}: "
              f"{'OK' if {'k': kk, 'm': mv} in confirmed else 'PENDING/ALARM'}"
              f" ({time.time()-t0:.0f}s)", flush=True)
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"j": J, "retried": len(todo), "confirmed": confirmed,
           "alarms": alarms, "still_unknown": still,
           "timeout_ms": int(os.environ.get("Z3_TIMEOUT_MS", "600000")),
           "command": f"KNIFE_J={J} Z3_TIMEOUT_MS=600000 "
                      "python lab/z3_judge_retry.py",
           "git": git, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"z3_judge_j{J}_retry.json").write_text(json.dumps(out, indent=1),
                                                   encoding="utf-8")
    print(f"RETRY: {len(confirmed)}/{len(todo)} confirmed, "
          f"{len(alarms)} alarms, {len(still)} still unknown", flush=True)
    return 0 if not alarms and not still else 1


if __name__ == "__main__":
    sys.exit(main())
