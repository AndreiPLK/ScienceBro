"""Z3 independent judge aimed at the TIGHTEST zone of the whole project.

Why here. Measurement (results/keystone_lowspin.json, keystone_margin_law.json)
puts the smallest margin of the entire programme at

        branch k = 45  (lam in [25.5, 26.1]),  levels n around 44,
        even knives, margin about ONE PERCENT of the shore.

That is where a wrong claim would hide, and it is also where our own tools
were weakest: the old counterexample hunt swept only spins 0,2,4,6 (this zone
has spin ~80), and the level n = 44 sits just past the m <= 40 cut-off of the
earlier Z3 run.

Role of this script: the FOREIGN engine (Z3, Microsoft Research; not our
code) re-states the claim from scratch, using only the exact INTEGER
coefficients of B_j -- numbers, never our certificate logic:

        exists? lam in [a, b], D in [4, T_k(lam)] with P_j(lam, D) <= 0

unsat  =>  no violation anywhere in that continuous cell, no bisection and no
sampling involved. sat => a counterexample candidate, which would freeze the
claim immediately. unknown is reported honestly as unknown, never as pass.

Run: python lab/z3_judge_tight.py -> results/z3_judge_tight.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from z3 import Q, Reals, Solver, sat, unsat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import Bj_coeffs  # exact integers only
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
TIMEOUT_MS = 180000

# the tight zone: branch k = 45 and its neighbours
CELLS = [
    (k, Fraction(3, 5) * (k - Fraction(5, 2)), Fraction(3, 5) * (k - Fraction(3, 2)))
    for k in (44, 45, 46)
]
JS = (4, 6, 8)
LEVELS = range(38, 53)


def judge(coeffs, kk, lo: Fraction, hi: Fraction):
    lam, D = Reals("lam D")
    P = sum(c * lam**p * D**q for (p, q), c in coeffs.items())
    Tk = Q(3 * (2 * kk - 3), kk * (kk - 2)) * (lam**2 + (2 * kk - 2) * lam + 1) + 2 * kk
    s = Solver()
    s.set("timeout", TIMEOUT_MS)
    s.add(
        lam >= Q(lo.numerator, lo.denominator),
        lam <= Q(hi.numerator, hi.denominator),
        D >= 4,
        D <= Tk,
        P <= 0,
    )
    r = s.check()
    return "unsat" if r == unsat else "SAT_COUNTEREXAMPLE" if r == sat else "unknown"


def main() -> int:
    t0 = time.time()
    rows, alarms, unknowns = [], [], 0
    for j in JS:
        for n in LEVELS:
            mv = n - 3
            if mv < max(1, j - 2):
                continue
            coeffs = Bj_coeffs(j, mv)
            for kk, lo, hi in CELLS:
                verdict = judge(coeffs, kk, lo, hi)
                rows.append(
                    {
                        "j": j,
                        "n": n,
                        "spin": 2 * (n - j),
                        "k": kk,
                        "lam_range": [str(lo), str(hi)],
                        "verdict": verdict,
                    }
                )
                if verdict == "SAT_COUNTEREXAMPLE":
                    alarms.append(rows[-1])
                elif verdict == "unknown":
                    unknowns += 1
        print(
            f"  j={j}: cells {len(rows)}, alarms {len(alarms)}, "
            f"unknown {unknowns} ({time.time() - t0:.0f}s)",
            flush=True,
        )

    out = {
        "role": "foreign-engine confirmation of the tightest zone of the"
        " programme (branch k=44..46, lam about 26, levels 38..52,"
        " even knives, margin about one percent)",
        "why_here": "smallest measured margin in the whole project; also"
        " the zone our own earlier tools covered worst (old"
        " hunt swept only spins 0,2,4,6; this zone has spin"
        " about 80, and n=44 sits past the old m<=40 cut-off)",
        "claim_restated": "exists lam in branch, D in [4, T_k(lam)] with"
        " P_j <= 0 ?  unsat means no violation in the"
        " whole continuous cell",
        "independence": "imports only exact integer coefficients of B_j;"
        " no certificate logic of ours is shared",
        "cells": len(rows),
        "alarms": alarms,
        "unknown_count": unknowns,
        "all_unsat": not alarms and unknowns == 0,
        "rows": rows,
        "command": "python lab/z3_judge_tight.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "z3_judge_tight.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells {len(rows)}, alarms {len(alarms)}, unknown {unknowns}", flush=True)
    print(
        "FOREIGN JUDGE: "
        + ("CONFIRMS (all unsat)" if not alarms and unknowns == 0 else "SEE ARTIFACT"),
        flush=True,
    )
    return 1 if alarms else 0


if __name__ == "__main__":
    sys.exit(main())
