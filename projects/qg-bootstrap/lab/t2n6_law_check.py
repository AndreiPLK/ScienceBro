"""Blind verification of the closed-form 2n-6 law against the exact evaluator.

Law (derived from symbolic brackets n=4..9, verified here also on UNSEEN
n=10..12): with m=n-3, s=lam+n-1, u=D+4m+1,
  G(m)     = 2(m+1)(m+3) / (3(2m+3))
  alpha(m) = (m+3)(5m^3+21m^2+19m+15) / (45(2m+1)(2m+3))
  Bhat     = alpha*u*(u-2) - G*u*s^2 + s^4
Claim: sign(a_{n,2n-6}) == sign(Bhat) for D>3 even, lam>0 (zero allowed both).
Exact rational arithmetic on both sides.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hunt_2n8 import a_l  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def bhat(n: int, lamv: F, Dv: int) -> F:
    m = n - 3
    s = lamv + n - 1
    u = F(Dv + 4 * m + 1)
    G = F(2 * (m + 1) * (m + 3), 3 * (2 * m + 3))
    alpha = F((m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15), 45 * (2 * m + 1) * (2 * m + 3))
    return alpha * u * (u - 2) - G * u * s**2 + s**4


def sgn(x) -> int:
    return (x > 0) - (x < 0)


def main() -> int:
    t0 = time.time()
    lams = [
        F(1, 10),
        F(1, 4),
        F(1, 2),
        F(3, 4),
        F(1),
        F(3, 2),
        F(2),
        F(3),
        F(5),
        F(7),
        F(10),
        F(20),
    ]
    mism = []
    checks = 0
    for n in range(4, 13):
        for Dv in range(4, 41, 2):
            for lamv in lams:
                checks += 1
                se = sgn(a_l(n, 2 * n - 6, lamv, Dv))
                sb = sgn(bhat(n, lamv, Dv))
                if se != sb:
                    mism.append({"n": n, "lam": str(lamv), "D": Dv, "exact": se, "law": sb})
        print(f"n={n} done ({time.time() - t0:.0f}s, mismatches so far: {len(mism)})", flush=True)
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "checks": checks,
        "mismatches": mism,
        "fitted_on": "n=4..9",
        "blind_levels": "n=10..12",
        "command": "python lab/t2n6_law_check.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "t2n6_law_check.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"TOTAL: {checks} checks, {len(mism)} mismatches", flush=True)
    return 1 if mism else 0


if __name__ == "__main__":
    sys.exit(main())
