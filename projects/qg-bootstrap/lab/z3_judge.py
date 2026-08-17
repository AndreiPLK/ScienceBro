"""Z3 independent judge for shallow knife cells.

Role: the FOREIGN engine (Microsoft Research SMT solver, not written by us)
independently confirms each shallow branch claim: no violation exists.
Satisfies the validator rule: imports only the exact integer coefficients of
B_j (numbers, not our certificate logic) and re-states the claim from scratch:

  exists? lam in [mu_lo, mu_hi], D in [4, T_k(lam)]:  P_j(lam, D) <= 0
  Z3 unsat  =>  no violation on the WHOLE branch cell (no bisection needed).

Usage: KNIFE_J=4 python lab/z3_judge.py
Artifact: results/z3_judge_j{J}.json; exit 0 iff every cell is unsat.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

from z3 import Q, Reals, Solver, unsat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import Bj_coeffs, j_min_m  # exact integers only

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))
MFIX = int(os.environ.get("MFIX", "40"))
TIMEOUT_MS = int(os.environ.get("Z3_TIMEOUT_MS", "120000"))


def judge_cell(coeffs, kk, mu_lo, mu_hi):
    lam, D = Reals("lam D")
    P = sum(c * lam**p * D**q for (p, q), c in coeffs.items())
    Tk = Q(3 * (2 * kk - 3), kk * (kk - 2)) * (lam**2 + (2 * kk - 2) * lam + 1) + 2 * kk
    s = Solver()
    s.set("timeout", TIMEOUT_MS)
    s.add(
        lam >= Q(mu_lo.numerator, mu_lo.denominator),
        lam <= Q(mu_hi.numerator, mu_hi.denominator),
        D >= 4,
        D <= Tk,
        P <= 0,
    )
    r = s.check()
    if r == unsat:
        return "unsat", None
    if str(r) == "sat":
        return "SAT-ALARM", str(s.model())
    return "unknown", None


def main() -> int:
    t0 = time.time()
    cells = 0
    alarms = []
    unknowns = []
    for kk in range(3, 46):
        if kk == 3:
            mu_lo, mu_hi = Fraction(1, 1000), Fraction(2, 3)
        else:
            mu_lo = Fraction(3, 5) * (kk - Fraction(5, 2))
            mu_hi = Fraction(3, 5) * (kk - Fraction(3, 2))
            if kk == 4:
                mu_lo = Fraction(2, 3)
        for mv in range(j_min_m(J), MFIX + 1):
            verdict, model = judge_cell(Bj_coeffs(J, mv), kk, mu_lo, mu_hi)
            cells += 1
            if verdict == "SAT-ALARM":
                alarms.append({"k": kk, "m": mv, "model": model})
                print(f"  ALARM j={J} k={kk} m={mv}: {model}", flush=True)
            elif verdict == "unknown":
                unknowns.append({"k": kk, "m": mv})
        print(f"branch k={kk}: judged ({time.time() - t0:.0f}s)", flush=True)
    ok = not alarms and not unknowns
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "j": J,
        "independent_engine": "z3 nlsat",
        "all_unsat": bool(ok),
        "cells": cells,
        "alarms": alarms,
        "unknowns": unknowns,
        "command": f"KNIFE_J={J} python lab/z3_judge.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / f"z3_judge_j{J}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(
        ("Z3 JUDGE: ALL CONFIRMED" if ok else "Z3 JUDGE: ISSUES")
        + f" (cells {cells}, alarms {len(alarms)},"
        f" unknown {len(unknowns)})",
        flush=True,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
