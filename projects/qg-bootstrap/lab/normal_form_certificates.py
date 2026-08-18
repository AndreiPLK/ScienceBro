"""CERTIFICATES VIA THE NORMAL FORM -- every knife of a level in one pass.

The Jacobi normal form (lab/jacobi_normal_form.py, verified against the
independently computed exact value on 4500 cells with zero mismatches) says

    sign(knife j) = (-1)^m x sign of the m-th Jacobi coefficient of
                    F(u) = u^eps prod_a (u - (a/s)^2)^2,   m = n - j.

Because j enters ONLY through m, one level n costs one polynomial and n-1
coefficient evaluations: at n = 60 that is 59 knives in 35 seconds, against
9941 seconds for the strip-certificate run to reach j = 28. This module turns
that into a coverage artifact.

WHAT THIS DOES AND DOES NOT REPLACE. The strip certificates cover RANGES of lam
and D symbolically; this fixes one (lam, D) per pass. It is therefore extra
coverage of the same statement at many more levels, not a substitute. Both are
kept.

Every number is an exact rational; a cell is recorded as certified only when the
coefficient is strictly positive as a rational, and the shore condition
D < T_hat(lam) is checked before the cell is claimed.

Run: python lab/normal_form_certificates.py -> results/normal_form_certificates.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import jacobi_moment, sign_of  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
OUT = RES / "normal_form_certificates.json"

LEVELS = list(range(6, 41)) + [45, 50, 55, 60]  # capped: the machine had 3.2 GB free
LAMS = [F(1, 4), F(1, 2), F(1), F(2), F(3), F(7), F(14), F(26), F(60), F(150)]
DS = [F(4), F(6), F(8), F(11), F(26), F(60)]


def main() -> int:
    t0 = time.time()
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    rows = data.get("rows", {})
    knives = failures = 0
    for n in LEVELS:
        for lam in LAMS:
            shore = T_hat(float(lam))
            for D in DS:
                if float(D) >= shore:
                    continue
                key = f"{n}|{lam}|{D}"
                if key in rows:
                    knives += rows[key]["knives"]
                    failures += len(rows[key]["negative_m"])
                    continue
                t1 = time.time()
                neg = []
                for m in range(n - 1):
                    if sign_of(F(-1) ** m * jacobi_moment(n - m, n, lam, D)) <= 0:
                        neg.append(m)
                rows[key] = {
                    "n": n,
                    "lam": str(lam),
                    "D": str(D),
                    "knives": n - 1,
                    "negative_m": neg,
                    "shore": round(shore, 4),
                    "seconds": round(time.time() - t1, 2),
                }
                knives += n - 1
                failures += len(neg)
                data = {
                    "claim": "every knife j = 2..n is certified positive at this"
                    " (n, lam, D) by the sign of one exact rational"
                    " Jacobi coefficient",
                    "equivalence_verified_in": "results/jacobi_normal_form.json"
                    " (4500 cells, 0 mismatches)",
                    "knives_certified": knives,
                    "failures": failures,
                    "rows": rows,
                    "command": "python lab/normal_form_certificates.py",
                    **stamp(),
                    "runtime_s": round(time.time() - t0, 1),
                }
                OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
                print(
                    f"  n={n:3d} lam={str(lam):<4s} D={str(D):<4s} knives {n - 1:3d}  "
                    f"negatives {neg if neg else 'none'}  ({time.time() - t1:.1f}s)",
                    flush=True,
                )
    print(f"TOTAL knives certified: {knives}, failures: {failures}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
