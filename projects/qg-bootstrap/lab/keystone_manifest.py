"""THE FINAL STEP: is J manifestly positive in the depth below the shore?

From keystone_shore.json we know the D-threshold never sits strictly below
the shore, and in the tangency cases it sits EXACTLY on it.  So substitute

        Q = Q_shore - z,        z = (T_hat(lam) - D)/2 >= 0

("z = how far below the shore we are") and ask the only question left:

        are ALL coefficients of J(Q_shore - z) in z NONNEGATIVE?

If yes, positivity below the shore is MANIFEST -- no root hunting, no
asymptotics, no Stokes topology: a sum of nonnegative terms in z, strictly
positive as soon as one coefficient is positive.  That is a Polya-type
certificate and it would be the keystone: one argument covering every
knife j at once.

This script tests it exactly (Fraction arithmetic) over a wide grid and
reports the first failures with full coordinates if it is false.

Run: python lab/keystone_manifest.py -> results/keystone_manifest.json
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

LAMS = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10), Fraction(1, 3),
        Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26), Fraction(150), Fraction(1000))


def shift_poly(poly: list[Fraction], q0: Fraction) -> list[Fraction]:
    """Coefficients (ascending in z) of poly(q0 - z)."""
    out = [Fraction(0)] * len(poly)
    # Horner in (q0 - z): iterate from the top coefficient down
    cur = [Fraction(0)]
    for c in reversed(poly):
        # cur <- cur * (q0 - z) + c
        new = [Fraction(0)] * (len(cur) + 1)
        for d, cd in enumerate(cur):
            new[d] += cd * q0
            new[d + 1] -= cd
        new[0] += c
        cur = new
    for d, cd in enumerate(cur):
        if d < len(out):
            out[d] = cd
        elif cd != 0:                       # degree guard
            out.append(cd)
    return cur


def main() -> int:
    t0 = time.time()
    cells = 0
    failures, tangency, examples = [], [], []
    for j in range(2, 41):
        for n in range(max(4, j + 1), max(4, j + 1) + 24, 2):
            for lam in LAMS:
                Th = T_hat(lam)
                if Th <= 4:
                    continue
                poly = J_poly_in_Q(j, n, lam)
                q_shore = Fraction(Th, 2) + n - j - 2
                zc = shift_poly(poly, q_shore)
                cells += 1
                neg = [(d, str(c)) for d, c in enumerate(zc) if c < 0]
                if neg:
                    if len(failures) < 25:
                        failures.append({"j": j, "n": n, "lam": str(lam),
                                         "negative_z_coeffs": neg[:6],
                                         "n_negative": len(neg),
                                         "degree": len(zc) - 1})
                if zc[0] == 0:
                    tangency.append({"j": j, "n": n, "lam": str(lam)})
                if len(examples) < 12 and j <= 4:
                    examples.append({"j": j, "n": n, "lam": str(lam),
                                     "z_coeffs_signs":
                                         "".join("+" if c > 0 else
                                                 ("0" if c == 0 else "-")
                                                 for c in zc)})
        print(f"  j={j}: cells {cells}, cells with a negative z-coeff "
              f"{len(failures)} ({time.time()-t0:.0f}s)", flush=True)

    out = {"question": "are all coefficients of J(Q_shore - z) in z >= 0?",
           "meaning": "if yes, positivity below the shore is manifest for"
                      " every knife at once (Polya-type certificate)",
           "cells": cells,
           "manifest_positive_everywhere": not failures,
           "failure_examples": failures,
           "tangency_cells_zero_constant_term": tangency[:40],
           "tangency_count": len(tangency),
           "sign_pattern_examples": examples,
           "command": "python lab/keystone_manifest.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_manifest.json").write_text(json.dumps(out, indent=1),
                                                encoding="utf-8")
    print(f"cells {cells}; cells with negative z-coefficients "
          f"{len(failures)}; tangency cells {len(tangency)}", flush=True)
    print("MANIFEST POSITIVITY " + ("HOLDS" if not failures else
                                    "FAILS (see artifact)"), flush=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
