"""Far-below, third-generation certificate: INTERVAL Bernstein in D.

Why: the y-expansion criterion (farbelow2) is sufficient but stops holding
at j >= 9 (documented boundary, DATA_LOG 2026-08-17). Here we instead map
the D-range to a FINITE interval, D = 4 + (T_cap - 4)*th with th in [0,1],
and certify with Bernstein in th x thL plus orthant positivity in (v, K3) —
the same chain that already closes the below-diagonal band.

Region: deep water far below the diagonal, m = 41 + v (v >= 0),
K = v + K3 + 6 (so v <= K-6), lam = (K + 51 + thL)*sqrt3/3, D <= T_cap.

Usage: KNIFE_J=9 python lab/knife_farbelow3.py
Artifact: results/knife{J}_farbelow_interval.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_tail2 import bern_axis_pair, build_P, collect_pairs  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "9"))
ELEV = int(os.environ.get("BERN_ELEV", "0"))
DEPTH = int(os.environ.get("DEPTH", "5"))

# vars: 0=thL, 1=th, 2=v, 3=K3
NV = 4
thL, th, vv, K3 = (Q3Poly.var(NV, i) for i in range(4))


def build(a, b):
    aq = fmpq(a.numerator, a.denominator)
    bq = fmpq(b.numerator, b.denominator)
    tL = aq + (bq - aq) * thL
    Kc = vv + K3
    lam = (Kc + 51 + tL) * Q3Poly.const(NV, 0, fmpq(1, 3))
    kk = Kc + 53
    den = kk * (kk - 2)
    tk_num = (3 * (2 * kk - 3)) * (lam * lam + (2 * kk - 2) * lam + 1) + (2 * kk) * kk * (kk - 2)
    D_num = 4 * den + (tk_num - 4 * den) * th
    return build_P(lam, D_num, den, vv + 41)


def cert(P, tag, log):
    A, B = bern_axis_pair(P.a.c, P.b.c, 0, ELEV)  # thL on [0,1]
    A, B = bern_axis_pair(A, B, 1, ELEV)  # th on [0,1]
    strict = True
    for _kl, (ad, bd) in collect_pairs(A, B, (0, 1)).items():
        for e in set(ad) | set(bd):
            if sign_q3(ad.get(e, fmpq(0)), bd.get(e, fmpq(0))) < 0:
                log.append({"cell": tag, "ok": False})
                return False, False
        zero = (0, 0)
        if sign_q3(ad.get(zero, fmpq(0)), bd.get(zero, fmpq(0))) <= 0:
            strict = False
    log.append({"cell": tag, "ok": True, "strict": bool(strict)})
    return True, strict


def bisect(a, b, depth, log, strict_flag):
    ok, st = cert(build(a, b), f"far_thL[{a},{b}]", log)
    if ok:
        strict_flag[0] &= st
        return True
    if depth == 0:
        return False
    mid = (a + b) / 2
    return bisect(a, mid, depth - 1, log, strict_flag) and bisect(
        mid, b, depth - 1, log, strict_flag
    )


def main() -> int:
    t0 = time.time()
    log = []
    strict_flag = [True]
    ok = bisect(Fraction(0), Fraction(1), DEPTH, log, strict_flag)
    out = {
        "j": J,
        "far_below_interval": bool(ok),
        "cells": len(log),
        "strict_positive": bool(strict_flag[0]) if ok else None,
        "method": "interval Bernstein in (thL, th) + orthant in (v, K3)",
        "scope": (
            "far-below deep water: m=41+v (v>=0), K=v+K3+6 "
            "(=> v<=K-6), lam=(K+51+thL)sqrt3/3, D in [4, T_cap]"
        ),
        "elev": ELEV,
        "depth": DEPTH,
        "failed_cells": [c for c in log if not c.get("ok", True)][:20],
        "command": f"KNIFE_J={J} python lab/knife_farbelow3.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / f"knife{J}_farbelow_interval.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print(
        f"FAR-BELOW-INTERVAL(j={J}) "
        + ("CLOSED" if ok else "OPEN")
        + f"  cells={len(log)} ({time.time() - t0:.0f}s)",
        flush=True,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
