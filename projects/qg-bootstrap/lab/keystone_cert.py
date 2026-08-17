"""KEYSTONE CERTIFICATE: J(Q) > 0 on the whole stretch below the shore.

State of the reduction (all machine-verified):
  * keystone_beta.json   -- sign P_j = sign J(Q), J a polynomial of degree
                            j-1 in Q = D/2 + n - j - 2, coefficients
                            rational in (n, lam), D-free shape (6720 checks)
  * keystone_shore.json  -- the D-threshold never falls strictly below the
                            shore on 5616 cells; exact tangency in 3
  * keystone_descartes.json -- Hhat has ALL j-1 sign changes inside (0,1),
                            so Karlin's variation-diminishing bound is
                            j-1, not 1: the "single threshold" route via
                            total positivity does NOT close the argument

So the honest remaining task is a positivity certificate for J on the
closed stretch Q in [Q_low, Q_shore], with

        Q_low = n - j          (this is D = 4)
        Q_shore = T_hat(lam)/2 + n - j - 2 .

Certificate used (the same architecture as the twelve proven knives, now
in ONE variable): map the stretch onto (0, inf) by

        Q = Q_low + (Q_shore - Q_low) * w/(1+w),   w >= 0,

clear the denominator (multiply by (1+w)^{j-1}) and test whether every
coefficient of the resulting integer/rational polynomial in w is
nonnegative.  All coefficients nonnegative  =>  no root for w >= 0  =>
J > 0 on the whole stretch, strictly if the constant term is positive.
That is a Polya-type certificate: finite, exact, and independent of any
asymptotics.

Where a cell fails the plain test, we bisect the stretch (the standard
repair) and report how deep the bisection had to go.

Run: python lab/keystone_cert.py -> results/keystone_cert.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_poly_in_Q  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

LAMS = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10), Fraction(1, 3),
        Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26), Fraction(150), Fraction(1000))
MAX_DEPTH = 6


def affine_then_mobius(poly: list[Fraction], a: Fraction,
                       b: Fraction) -> list[Fraction]:
    """Coefficients (ascending in w) of (1+w)^m * poly(a + (b-a) w/(1+w)).

    Nonnegative coefficients  <=>  poly has no root on [a, b) and is
    positive there (Polya / Descartes on the mapped ray).
    """
    m = len(poly) - 1
    d = b - a
    # poly(a + d*w/(1+w)) * (1+w)^m = sum_k c_k (d w)^k (1+w)^{m-k}
    # after re-expanding poly around a first:
    shifted = [Fraction(0)] * (m + 1)          # poly(a + x) in powers of x
    for i, ci in enumerate(poly):
        if not ci:
            continue
        for k in range(i + 1):
            shifted[k] += ci * comb(i, k) * a ** (i - k)
    out = [Fraction(0)] * (m + 1)
    for k, ck in enumerate(shifted):
        if not ck:
            continue
        term = ck * d ** k
        for r in range(m - k + 1):             # (1+w)^{m-k}
            out[k + r] += term * comb(m - k, r)
    return out


def certify(poly: list[Fraction], a: Fraction, b: Fraction,
            depth: int = 0) -> tuple[bool, int]:
    """Nonnegative-coefficient certificate on [a, b], with bisection."""
    co = affine_then_mobius(poly, a, b)
    if all(c >= 0 for c in co) and any(c > 0 for c in co):
        return True, depth
    if depth >= MAX_DEPTH:
        return False, depth
    mid = (a + b) / 2
    ok1, d1 = certify(poly, a, mid, depth + 1)
    if not ok1:
        return False, d1
    ok2, d2 = certify(poly, mid, b, depth + 1)
    return ok2, max(d1, d2)


def main() -> int:
    t0 = time.time()
    cells = certified = 0
    depth_hist: dict[int, int] = {}
    failures = []
    for j in range(2, 41):
        for n in range(max(4, j + 1), max(4, j + 1) + 24, 2):
            for lam in LAMS:
                Th = T_hat(lam)
                if Th <= 4:
                    continue
                poly = J_poly_in_Q(j, n, lam)
                q_low = Fraction(n - j)                     # D = 4
                q_shore = Fraction(Th, 2) + n - j - 2
                if q_shore <= q_low:
                    continue
                cells += 1
                ok, d = certify(poly, q_low, q_shore)
                if ok:
                    certified += 1
                    depth_hist[d] = depth_hist.get(d, 0) + 1
                elif len(failures) < 25:
                    failures.append({"j": j, "n": n, "lam": str(lam),
                                     "depth_reached": d})
        print(f"  j={j}: cells {cells}, certified {certified}, "
              f"failures {len(failures)}, depth histogram "
              f"{dict(sorted(depth_hist.items()))} ({time.time()-t0:.0f}s)",
              flush=True)

    out = {"claim": "J(Q) > 0 for every Q in [Q_low, Q_shore], i.e. every"
                    " knife stays positive everywhere strictly below the"
                    " shore -- certified, not sampled",
           "certificate": "nonnegative coefficients after Q = Q_low +"
                          " (Q_shore-Q_low) w/(1+w) and clearing (1+w)^{j-1};"
                          " bisection of the stretch where needed",
           "stretch": {"Q_low": "n - j  (this is D = 4)",
                       "Q_shore": "T_hat(lam)/2 + n - j - 2"},
           "grid": {"j": "2..40", "n": "max(4,j+1)..+24 step 2",
                    "lam": [str(x) for x in LAMS]},
           "cells": cells, "certified": certified,
           "all_certified": certified == cells,
           "bisection_depth_histogram": {str(k): v for k, v
                                         in sorted(depth_hist.items())},
           "failures": failures,
           "max_depth_allowed": MAX_DEPTH,
           "command": "python lab/keystone_cert.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_cert.json").write_text(json.dumps(out, indent=1),
                                            encoding="utf-8")
    print(f"cells {cells}, certified {certified}, "
          f"depths {dict(sorted(depth_hist.items()))}", flush=True)
    print("KEYSTONE CERTIFICATE " + ("HOLDS on the whole grid"
                                     if certified == cells else
                                     "INCOMPLETE (see artifact)"), flush=True)
    return 0 if certified == cells else 1


if __name__ == "__main__":
    sys.exit(main())
