"""THE KEYSTONE, closing argument: variation diminishing + one inequality.

Setting (verified in keystone_beta.json, 6720 exact checks):

    sign P_j(n, lam, D) = sign I(Q),
    I(Q) = INT_0^1 Hhat(u) u^p (1-u)^Q du,   Q = D/2 + n - j - 2,
    Hhat  D-free polynomial of degree j-1,   p = n - j - 1/2.

Substituting v = -log(1-u) turns the kernel into exp(-Q v): a Laplace
kernel, which is STRICTLY TOTALLY POSITIVE.  Karlin's variation-
diminishing property then gives, for the number S of sign changes,

    S_Q( I )  <=  S_u( Hhat ) .

So if Hhat has exactly ONE sign change on (0, 1), then I(Q) has AT MOST
ONE sign change in Q: the positivity region in D is a single interval and
the whole "no knife cuts below the shore" theorem collapses to ONE
inequality, J(Q_shore) >= 0, which keystone_shore.json already measured
(5616 cells, zero violations, exact tangency in 3 cells).

This script computes the EXACT number of sign changes of Hhat on (0, 1)
by a Sturm chain in rational arithmetic -- no floating point anywhere.

Run: python lab/keystone_sturm.py -> results/keystone_sturm.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import Hhat_coeffs  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

LAMS = (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10), Fraction(1, 3),
        Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(7),
        Fraction(26), Fraction(150), Fraction(1000))


def trim(p: list[Fraction]) -> list[Fraction]:
    while p and p[-1] == 0:
        p.pop()
    return p


def pmul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for k, bk in enumerate(b):
                out[i + k] += ai * bk
    return trim(out)


def prem(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    """Remainder of a mod b (ascending coefficient lists)."""
    a = a[:]
    db, lb = len(b) - 1, b[-1]
    while len(a) - 1 >= db and trim(a):
        shift = len(a) - 1 - db
        f = a[-1] / lb
        for i, bi in enumerate(b):
            a[i + shift] -= f * bi
        trim(a)
        if not a:
            break
    return trim(a)


def deriv(p: list[Fraction]) -> list[Fraction]:
    return trim([p[i] * i for i in range(1, len(p))])


def sturm_chain(p: list[Fraction]) -> list[list[Fraction]]:
    chain = [p[:], deriv(p)]
    while len(chain[-1]) > 1:
        r = prem(chain[-2], chain[-1])
        if not r:
            break
        chain.append([-c for c in r])
    return [c for c in chain if c]


def peval(p: list[Fraction], x: Fraction) -> Fraction:
    v = Fraction(0)
    for c in reversed(p):
        v = v * x + c
    return v


def sign_var(chain, x: Fraction) -> int:
    sg = []
    for c in chain:
        v = peval(c, x)
        if v:
            sg.append(1 if v > 0 else -1)
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)


def roots_in_open_interval(p: list[Fraction], a: Fraction,
                           b: Fraction) -> int:
    """Number of DISTINCT real roots of p in (a, b) via Sturm."""
    p = trim(p[:])
    if len(p) <= 1:
        return 0
    g = p
    d = deriv(p)
    while d:                                  # strip repeated factors
        r = prem(g, d)
        if not r:
            g = d
            d = deriv(g)
            continue
        g, d = d, r
    # g is (up to scale) gcd(p, p'); divide it out for a squarefree part
    chain = sturm_chain(p)
    return sign_var(chain, a) - sign_var(chain, b)


def main() -> int:
    t0 = time.time()
    counts: dict[int, int] = {}
    cells, worst = 0, []
    for j in range(2, 41):
        for n in range(max(4, j + 1), max(4, j + 1) + 24, 2):
            for lam in LAMS:
                if T_hat(lam) <= 4:
                    continue
                desc = Hhat_coeffs(j, n, lam)     # descending u^{j-1}..u^0
                asc = list(reversed(desc))        # ascending for Sturm
                r = roots_in_open_interval(asc, Fraction(0), Fraction(1))
                counts[r] = counts.get(r, 0) + 1
                cells += 1
                if r > 1 and len(worst) < 20:
                    worst.append({"j": j, "n": n, "lam": str(lam),
                                  "roots_in_0_1": r})
        print(f"  j={j}: cells {cells}, root-count histogram "
              f"{dict(sorted(counts.items()))} ({time.time()-t0:.0f}s)",
              flush=True)

    out = {"question": "how many sign changes does the D-free polynomial"
                       " Hhat have on (0,1)?",
           "why_it_matters": "the Beta kernel (1-u)^Q is a Laplace kernel"
                             " after v=-log(1-u), hence strictly totally"
                             " positive; Karlin's variation-diminishing"
                             " property bounds the number of sign changes of"
                             " I(Q) in Q by the number of sign changes of"
                             " Hhat in u. One sign change => a single"
                             " positivity interval in D => the theorem"
                             " reduces to J(Q_shore) >= 0.",
           "method": "exact Sturm chain in Fraction arithmetic",
           "cells": cells,
           "root_count_histogram": {str(k): v
                                    for k, v in sorted(counts.items())},
           "at_most_one_sign_change": set(counts) <= {0, 1},
           "cells_with_more_than_one": worst,
           "command": "python lab/keystone_sturm.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_sturm.json").write_text(json.dumps(out, indent=1),
                                             encoding="utf-8")
    print(f"cells {cells}; histogram {dict(sorted(counts.items()))}",
          flush=True)
    print("SINGLE SIGN CHANGE " + ("CONFIRMED" if set(counts) <= {0, 1}
                                   else "NOT universal (see artifact)"),
          flush=True)
    return 0 if set(counts) <= {0, 1} else 1


if __name__ == "__main__":
    sys.exit(main())
