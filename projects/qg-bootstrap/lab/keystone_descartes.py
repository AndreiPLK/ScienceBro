"""How many sign changes does the D-free shape Hhat have on (0,1)?

Why this is the closing question.  From keystone_beta.json:

    sign P_j = sign of  INT_0^1 Hhat(u) u^p (1-u)^Q du,   Q = D/2 + n - j - 2.

Substituting v = -log(1-u) turns the kernel into exp(-Q v): a Laplace
kernel, hence STRICTLY TOTALLY POSITIVE.  Karlin's variation-diminishing
property then bounds the number of sign changes of the integral as a
function of Q by the number of sign changes of Hhat on (0,1).  So:

    Hhat has one sign change  =>  positivity in D is a single interval
                             =>  the theorem is the single inequality
                                 J(Q_shore) >= 0 (measured in
                                 keystone_shore.json, 5616 cells, 0 fails).

Method: Descartes after the Mobius map u = w/(1+w), which sends (0,1) onto
(0, inf).  With m = deg Hhat, the numerator

        Nw(w) = SUM_i h_i w^i (1+w)^{m-i}

has the same roots in (0, inf) as Hhat has in (0, 1).  Descartes' rule
bounds the count by the sign changes of Nw's coefficients and matches its
parity, so 0 changes => no roots and 1 change => EXACTLY one root.  This
replaces the Sturm chain that blew up in rational arithmetic (its
coefficients grew without bound; killed after 28 min with no output).

Run: python lab/keystone_descartes.py -> results/keystone_descartes.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import Hhat_coeffs  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

LAMS = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10), Fraction(1, 3),
        Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26), Fraction(150), Fraction(1000))


def mobius_numerator(h_asc: list[Fraction]) -> list[Fraction]:
    """Coefficients of Nw(w) = sum_i h_i w^i (1+w)^{m-i}, ascending."""
    m = len(h_asc) - 1
    out = [Fraction(0)] * (m + 1)
    for i, hi in enumerate(h_asc):
        if not hi:
            continue
        for k in range(m - i + 1):            # (1+w)^{m-i}
            out[i + k] += hi * comb(m - i, k)
    return out


def sign_changes(coeffs: list[Fraction]) -> int:
    sg = [1 if c > 0 else -1 for c in coeffs if c != 0]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)


def main() -> int:
    t0 = time.time()
    hist: dict[int, int] = {}
    cells, many = 0, []
    for j in range(2, 61):
        for n in range(max(4, j + 1), max(4, j + 1) + 30, 2):
            for lam in LAMS:
                if T_hat(lam) <= 4:
                    continue
                h_asc = list(reversed(Hhat_coeffs(j, n, lam)))
                sc = sign_changes(mobius_numerator(h_asc))
                hist[sc] = hist.get(sc, 0) + 1
                cells += 1
                if sc > 1 and len(many) < 25:
                    many.append({"j": j, "n": n, "lam": str(lam),
                                 "sign_changes": sc})
        if j % 5 == 0 or j < 6:
            print(f"  j={j}: cells {cells}, histogram "
                  f"{dict(sorted(hist.items()))} ({time.time()-t0:.0f}s)",
                  flush=True)

    ok = set(hist) <= {0, 1}
    out = {"question": "number of sign changes of the D-free shape Hhat on"
                       " (0,1), i.e. an exact upper bound on the number of"
                       " D-thresholds",
           "method": "Descartes' rule after the Mobius map u = w/(1+w)"
                     " (exact rational arithmetic; 0 changes => no root,"
                     " 1 change => exactly one root)",
           "why_it_matters": "the Beta kernel is a Laplace kernel in"
                             " v = -log(1-u) and therefore strictly totally"
                             " positive; by Karlin's variation-diminishing"
                             " property the number of sign changes of the"
                             " integral in Q is at most that of Hhat in u",
           "grid": {"j": "2..60", "n": "max(4,j+1)..+30 step 2",
                    "lam": [str(x) for x in LAMS]},
           "cells": cells,
           "sign_change_histogram": {str(k): v
                                     for k, v in sorted(hist.items())},
           "at_most_one_sign_change": ok,
           "cells_with_more_than_one": many,
           "note_on_method_change": "the Sturm-chain version"
                                    " (lab/keystone_sturm.py) blew up in"
                                    " rational arithmetic and was killed"
                                    " after 28 minutes with no output;"
                                    " recorded as a tool limitation, not a"
                                    " result",
           "command": "python lab/keystone_descartes.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_descartes.json").write_text(json.dumps(out, indent=1),
                                                 encoding="utf-8")
    print(f"cells {cells}; histogram {dict(sorted(hist.items()))}", flush=True)
    print("AT MOST ONE SIGN CHANGE: " + ("YES" if ok else "NO"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
