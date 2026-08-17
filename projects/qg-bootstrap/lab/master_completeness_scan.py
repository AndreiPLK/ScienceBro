"""THE completeness test: does ANY knife j>=3 cut into conjectured-alive land?

Alive (conjecture 1, paper 2): D <= min_n T_n(lam). Using the MASTER FORMULA,
evaluate the sign of EVERY trajectory a_{n,2n-2j} (j=2..n-1) at every even D
inside the conjectured-alive region on a lambda grid. Any negative sign at an
alive point falsifies the conjecture (and maps the true boundary).
Exact rational arithmetic.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from math import factorial
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = 40


def e_doubled(n: int):
    poly = [1]
    for k in range(1, n):
        r = n - 2 * k
        for _ in range(2):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] += c * r
            poly = new
    return [abs(poly[2 * t]) for t in range(len(poly) // 2 + 1)]


E = {n: e_doubled(n) for n in range(3, NMAX + 1)}


def ensure_E(nmax):
    for n in range(3, nmax + 1):
        if n not in E:
            E[n] = e_doubled(n)


W = {}


def master_sign(n: int, j: int, lamv: F, Dv: int) -> int:
    c = 4 * n - 4 * j - 1
    e = E[n]
    s = lamv + n - 1
    s2 = s * s
    B = F(0)
    spow = F(1)
    for i in range(j):
        key = (n, j, i)
        if key not in W:
            W[key] = F(factorial(2 * n - 2 * j + 2 * i), factorial(i) * 2**i)
        tail = 1
        for k in range(i, j - 1):
            tail *= Dv + c + 2 * k
        B += (-1) ** i * e[j - 1 - i] * W[key] * spow * tail
        spow *= s2
    if j % 2 == 0:
        B = -B
    return (B > 0) - (B < 0)


def min_T_exact(lam: F) -> F:
    """min_n T_n как точная дробь (критик: float-граница зоны недопустима)."""
    return min(
        F(3 * (2 * n - 3), n * (n - 2)) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n
        for n in range(3, 400)
    )


def main() -> int:
    t0 = time.time()
    lams = [F(i, 20) for i in range(1, 61)] + [F(4), F(5), F(7), F(10), F(15), F(20), F(30), F(50)]
    alarms = []
    checks = 0
    for lam in lams:
        mt = min_T_exact(lam)
        Dtop = int(mt) if mt.denominator > 1 else int(mt)  # точный floor
        Dtop = mt.numerator // mt.denominator
        for Dv in range(4, Dtop + 1):  # критик: и чётные, и нечётные D
            for n in range(4, NMAX + 1):
                for j in range(3, n):
                    if 2 * n - 2 * j < 0:
                        continue
                    checks += 1
                    if master_sign(n, j, lam, Dv) < 0:
                        alarms.append({"lam": str(lam), "D": Dv, "n": n, "j": j})
        print(
            f"lam={lam}: cum checks {checks}, alarms {len(alarms)} ({time.time() - t0:.0f}s)",
            flush=True,
        )
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "checks": checks,
        "alarms": alarms,
        "nmax": NMAX,
        "region": "ALL integer D (even+odd) <= exact floor(min_n T_n), all j=3..n-1",
        "command": "python lab/master_completeness_scan.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "master_completeness_scan.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"TOTAL {checks} checks, {len(alarms)} alarms", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
