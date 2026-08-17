"""360-analysis: does LOW SPIN DOMINANCE hold for the CHR graviton family?

Prior art. Bo Wang (arXiv:2403.00906, JHEP) studies positivity of the
hypergeometric Coon amplitude with harmonic numbers as a basis and
hypothesises "partial-wave low spin dominance": that the unitarity bounds
are controlled by the LOW-spin partial-wave coefficients. He supports it
numerically for m^2 = 0 (his fig. 1: bounds from spin-0 data align with
bounds from all data) and calls for stronger evidence. Read in full text,
sections 3.3 and 4.1.2.

Our setting is different (CHR graviton family with the deformation lam,
arXiv:2408.03362) and our reduction makes the question cheap to test
exactly: the D-threshold of knife j at level n is the smallest root of the
univariate polynomial J(Q) built in keystone_beta.py, and the spin on that
trajectory is l = 2n - 2j.

Frozen question (before looking): for fixed (j, lam), which level n gives
the SMALLEST D-threshold, and what spin l does it correspond to? If the
minimum always sat at l = 0 or 2, low spin dominance would hold here too.

Exact rational bisection, no floats in the decision.

Run: python lab/keystone_lowspin.py -> results/keystone_lowspin.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_poly_in_Q  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

LAMS = (Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26))


def peval(p, x: Fraction) -> Fraction:
    v = Fraction(0)
    for c in reversed(p):
        v = v * x + c
    return v


def threshold_D(j: int, n: int, lam: Fraction, hi_mult: int = 40):
    """Smallest D >= 4 where J turns non-positive; None if never."""
    pol = J_poly_in_Q(j, n, lam)
    off = Fraction(n - j - 2)

    def val(D):
        return peval(pol, Fraction(D, 2) + off)

    lo = Fraction(4)
    hi = Fraction(hi_mult) * T_hat(lam)
    if val(lo) <= 0:
        return lo
    if val(hi) > 0:
        return None
    for _ in range(70):
        mid = (lo + hi) / 2
        if val(mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> int:
    t0 = time.time()
    rows, spins = [], {}
    for j in range(3, 15):
        for lam in LAMS:
            best = None
            for n in range(max(4, j + 1), j + 46):
                thr = threshold_D(j, n, lam)
                if thr is None:
                    continue
                if best is None or thr < best[1]:
                    best = (n, thr)
            if best is None:
                continue
            n_star, thr = best
            l_star = 2 * n_star - 2 * j
            shore = T_hat(lam)
            spins[l_star] = spins.get(l_star, 0) + 1
            rows.append({"j": j, "lam": str(lam), "n_star": n_star,
                         "spin_l_star": l_star,
                         "D_threshold": float(thr),
                         "shore": float(shore),
                         "ratio_threshold_over_shore": float(thr / shore)})
        print(f"  j={j} done ({time.time()-t0:.0f}s)", flush=True)

    low = sum(v for k, v in spins.items() if k <= 2)
    out = {"question": "for fixed (j, lam), which level n minimises the"
                       " D-threshold, and what spin l = 2n - 2j is that?",
           "prior_art": "Bo Wang arXiv:2403.00906 hypothesises partial-wave"
                        " LOW SPIN DOMINANCE for the hypergeometric Coon"
                        " amplitude (numerical support at m^2 = 0, his fig."
                        " 1); we test the analogous statement in the CHR"
                        " graviton family (arXiv:2408.03362)",
           "method": "exact rational bisection on the smallest root of the"
                     " univariate J(Q) from keystone_beta.py",
           "cells": len(rows),
           "spin_histogram_of_minimisers": {str(k): v for k, v
                                            in sorted(spins.items())},
           "fraction_at_low_spin_l_le_2": (low / len(rows)) if rows else None,
           "low_spin_dominance_holds_here": low == len(rows) if rows else None,
           "min_ratio_threshold_over_shore":
               min((r["ratio_threshold_over_shore"] for r in rows),
                   default=None),
           "rows": rows,
           "command": "python lab/keystone_lowspin.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_lowspin.json").write_text(json.dumps(out, indent=1),
                                               encoding="utf-8")
    print(f"cells {len(rows)}; spin histogram of minimisers "
          f"{dict(sorted(spins.items()))}", flush=True)
    print(f"low spin (l<=2) share: {out['fraction_at_low_spin_l_le_2']}",
          flush=True)
    print(f"tightest ratio threshold/shore: "
          f"{out['min_ratio_threshold_over_shore']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
