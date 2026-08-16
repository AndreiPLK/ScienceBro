"""Below-diagonal band + K0 pieces on the v2 engine (flint port of
knife_belowdiag_shift.py pieces (ii)+(iii); far-below lives in farbelow2).

Region (deep water, m>=41): (ii) band v in [K-6, K+4], K=6+K2>=6 via
v = K2 + 10*sigma; (iii) explicit K0=0..5, v in [0, K0+4] via v=(K0+4)*sigma.
Certificate chain: Bernstein (thL, th) -> Bernstein sigma -> K2-univariate
nonneg (per sqrt3-part), exactly as v1. Denominators cleared uniformly by
den = kk(kk-2) > 0.

Usage: KNIFE_J=6 python lab/knife_belowdiag2.py
Artifact: results/knife{J}_belowdiag_shift.json (v1-compatible fields).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly  # noqa: E402
from knife_tail2 import (build_P, bern_axis_pair, collect_pairs,  # noqa: E402
                         univar_nonneg)

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "6"))
import knife_tail2 as _kt2
assert _kt2.J == J, (
    f"J mismatch: belowdiag2 J={J} but knife_tail2.build_P uses J={_kt2.J}; "
    "set KNIFE_J for both")
ELEV = int(os.environ.get("BERN_ELEV", "0"))

# vars: 0=thL, 1=th, 2=sigma, 3=K2
NV = 4
thL, th, sig, K2 = (Q3Poly.var(NV, i) for i in range(4))


def cert(P, has_K, tag, log, t0, strict_needed=True,
         strict_ok=None):
    if strict_ok is None:
        strict_ok = [True]
    A, B = bern_axis_pair(P.a.c, P.b.c, 0, ELEV)   # thL
    A, B = bern_axis_pair(A, B, 1, ELEV)           # th
    A, B = bern_axis_pair(A, B, 2, ELEV)           # sigma
    for kl, (ad, bd) in collect_pairs(A, B, (0, 1, 2)).items():
        afl = {e[0]: cv for e, cv in ad.items()}
        bfl = {e[0]: cv for e, cv in bd.items()}
        # S5-fix: единая проверка для обеих веток; спецслучай удалён
        if not (univar_nonneg(afl) and univar_nonneg(bfl)):
            log.append({"cell": tag, "ok": False})
            return False
        if strict_needed and not (any(cv > 0 for cv in afl.values())
                                  or any(cv > 0 for cv in bfl.values())):
            strict_ok[0] = False
    log.append({"cell": tag, "ok": True, "strict": bool(strict_ok[0])})
    return True


def bisect(builder, a, b, depth, has_K, tag, log, t0):
    if cert(builder(a, b), has_K, tag, log, t0):
        return True
    if depth == 0:
        return False
    mid = (a + b) / 2
    return (bisect(builder, a, mid, depth - 1, has_K, tag, log, t0)
            and bisect(builder, mid, b, depth - 1, has_K, tag, log, t0))


def main() -> int:
    t0 = time.time()
    log = []
    ok = True
    pieces = {}

    def build(K_expr, vsub, a, b):
        aq = fmpq(a.numerator, a.denominator)
        bq = fmpq(b.numerator, b.denominator)
        tL = aq + (bq - aq) * thL
        lam_c = (K_expr + 51 + tL) * Q3Poly.const(NV, 0, fmpq(1, 3))
        kk_c = K_expr + 53
        den = kk_c * (kk_c - 2)
        lam2 = lam_c * lam_c
        tk_num = ((3 * (2 * kk_c - 3))
                  * (lam2 + (2 * kk_c - 2) * lam_c + 1)
                  + (2 * kk_c) * kk_c * (kk_c - 2))
        D_num = 4 * den + (tk_num - 4 * den) * th
        return build_P(lam_c, D_num, den, vsub + 41)

    # (ii) band: K=6+K2 (K_expr=K2), v = K2 + 10*sigma
    got = bisect(lambda a, b: build(K2, K2 + 10 * sig, a, b),
                 Fraction(0), Fraction(1), 5, True, "band_K6plus", log, t0)
    ok &= got
    pieces["band"] = bool(got)
    print(f"(ii) band K>=6: {'OK' if got else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    # (iii) K0 = 0..5: K_expr = const K0-6... в v1: lam=(K0+45+tL)r3/3,
    # kk=K0+47 => K_expr тут = K0-6+... наш build использует +51/+53:
    # K_expr = K0 - 6 подставим константой
    for K0 in range(0, 6):
        got = bisect(lambda a, b, K0=K0: build(Q3Poly.const(NV, K0 - 6),
                                               (K0 + 4) * sig, a, b),
                     Fraction(0), Fraction(1), 5, False, f"K{K0}", log, t0)
        ok &= got
        pieces[f"K{K0}"] = bool(got)
        print(f"(iii) K={K0}: {'OK' if got else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    prov = stamp()
    out = {"all_certified": bool(ok), "cells": len(log), "elev": ELEV,
           "j": J, "pieces": pieces, "engine": "belowdiag2-flint",
           "env": {"KNIFE_J": J, "PIECES": "band,k0", "BERN_ELEV": ELEV},
           "scope_note": "pieces field lists exactly what was run; far-below "
                         "covered by knife{J}_farbelow_factored.json",
           "command": f"KNIFE_J={J} python lab/knife_belowdiag2.py",
           **prov, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"knife{J}_belowdiag_shift.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(("BELOW-DIAGONAL CLOSED" if ok else "INCOMPLETE"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
