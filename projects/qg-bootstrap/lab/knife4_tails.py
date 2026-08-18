"""THE TAILS: closing knife 4 outside the compact box, by compactification.

The box proof (lab/knife4_proof.py) covers 4 <= n <= 400, 1/10 <= lam <= 60,
4 <= D <= shore. What is left is unbounded in n or in lam, and the two crude
tools both failed on it:

  * a Cauchy-type bound in n gives n0 = 1.6e6 at lam = 1 and 3.8e15 at lam = 120,
    because bounding each coefficient separately throws away the cancellation;
  * the same in lam is no better.

The tools that works is compactification: an unbounded direction is mapped to a
half-open interval by a Moebius substitution, and the polynomial is restored by
multiplying with a positive power of the denominator, which cannot change a sign.

    n-tail :  n = 400/(1-v),  v in [0,1),  multiply by (1-v)^9
    lam-tail: lam = 60/(1-w), w in [0,1),  D = d lam,  multiply by (1-v)^9 (1-w)^9

After that it is the same exact Bernstein subdivision as the box. The n-tail
closes in a SINGLE box for lam <= 30 (Bernstein minimum 2.0e24).

Legitimacy of the D range in the lam-tail: for lam >= 5 the shore satisfies
T_hat(lam)/lam < 18.93, so d = D/lam in [4/lam, 1893/100] contains the whole
admissible slab, and 4/lam <= 1/15 there.

Run: python lab/knife4_tails.py -> results/knife4_tails.json
"""

from __future__ import annotations

import json
import sys
import time
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp
from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife4_proof import shore_upper  # noqa: E402
from knife_closed_form import D as Dsym  # noqa: E402
from knife_closed_form import knife_polynomial  # noqa: E402
from knife_closed_form import lam as lamsym
from knife_closed_form import n as nsym
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
v, w, dsym = sp.symbols("v w d", nonnegative=True)


def build_n_tail(j: int, n0: int):
    """P(j) with n = n0/(1-v), cleared: a polynomial in (v, D, lam)."""
    P = knife_polynomial(j)
    deg = int(sp.degree(sp.expand(P), nsym))
    Q = sp.expand(sp.simplify(P.subs(nsym, sp.Rational(n0) / (1 - v)) * (1 - v) ** deg))
    return sp.Poly(Q, v, Dsym, lamsym)


def build_lam_tail(j: int, n0: int, l0: int):
    """P(j) with n = n0/(1-v), lam = l0/(1-w), D = d lam; cleared."""
    P = knife_polynomial(j)
    dn = int(sp.degree(sp.expand(P), nsym))
    Q = P.subs(
        {
            nsym: sp.Rational(n0) / (1 - v),
            lamsym: sp.Rational(l0) / (1 - w),
            Dsym: dsym * sp.Rational(l0) / (1 - w),
        }
    )
    Q = sp.expand(sp.simplify(sp.together(Q) * (1 - v) ** dn * (1 - w) ** dn))
    num, den = sp.fraction(sp.together(Q))
    assert den.is_number, "clearing failed"
    return sp.Poly(sp.expand(num / den), v, w, dsym)


def bernstein_min(poly: sp.Poly, box: list):
    """Exact Bernstein lower bound of `poly` on the box (its own variables)."""
    gens = poly.gens
    ts = [sp.Symbol(f"_t{k}") for k in range(len(gens))]
    subm = {
        g: sp.Rational(int(lo.p), int(lo.q))
        + (sp.Rational(int(hi.p), int(hi.q)) - sp.Rational(int(lo.p), int(lo.q))) * t
        for g, (lo, hi), t in zip(gens, box, ts)
    }
    p = sp.Poly(sp.expand(poly.as_expr().subs(subm)), *ts)
    md = [p.degree(t) for t in ts]
    a = {
        m: fmpq(int(sp.Rational(c).p), int(sp.Rational(c).q))
        for m, c in zip(p.monoms(), p.coeffs())
    }
    best = None
    for idx in product(*[range(m + 1) for m in md]):
        b = fmpq(0)
        for key, c in a.items():
            if all(key[i] <= idx[i] for i in range(len(idx))):
                f = fmpq(1)
                for i in range(len(idx)):
                    f *= fmpq(comb(idx[i], key[i]), comb(md[i], key[i]))
                b += c * f
        if best is None or b < best:
            best = b
            if best <= 0:
                return best
    return best


def subdivide(poly: sp.Poly, box, max_depth: int = 20):
    stack = [(box, 0)]
    boxes, open_boxes = 0, []
    while stack:
        bx, depth = stack.pop()
        boxes += 1
        if bernstein_min(poly, bx) > 0:
            continue
        if depth >= max_depth:
            open_boxes.append(bx)
            continue
        widths = [hi - lo for lo, hi in bx]
        k = widths.index(max(widths))
        lo, hi = bx[k]
        mid = (lo + hi) / 2
        left = list(bx)
        right = list(bx)
        left[k] = (lo, mid)
        right[k] = (mid, hi)
        stack += [(left, depth + 1), (right, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def main() -> int:
    t0 = time.time()
    out = {}
    # --- n tail: n >= 400, lam in [1/10, 60], D in [4, shore]
    Pn = build_n_tail(4, 400)
    ok_n, boxes_n, open_n = subdivide(
        Pn, [(fmpq(0), fmpq(999, 1000)), (fmpq(4), shore_upper(fmpq(60))), (fmpq(1, 10), fmpq(60))]
    )
    print(
        f"  n-tail  (n >= 400, lam <= 60): proved={ok_n}, boxes={boxes_n}, "
        f"open={len(open_n)}  ({time.time() - t0:.0f}s)",
        flush=True,
    )
    out["n_tail"] = {"proved": ok_n, "boxes": boxes_n, "open": len(open_n)}
    # --- lam tail: lam >= 60, n >= 4, D = d lam with d in [1/15, 18.93]
    Pl = build_lam_tail(4, 4, 60)
    ok_l, boxes_l, open_l = subdivide(
        Pl, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000)), (fmpq(1, 15), fmpq(1893, 100))]
    )
    print(
        f"  lam-tail (lam >= 60): proved={ok_l}, boxes={boxes_l}, "
        f"open={len(open_l)}  ({time.time() - t0:.0f}s)",
        flush=True,
    )
    out["lam_tail"] = {"proved": ok_l, "boxes": boxes_l, "open": len(open_l)}
    out.update(
        {
            "claim": "knife 4 positive on the two unbounded tails, by Moebius"
            " compactification plus exact Bernstein subdivision",
            "command": "python lab/knife4_tails.py",
            **stamp(),
            "runtime_s": round(time.time() - t0, 1),
        }
    )
    (RES / "knife4_tails.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/knife4_tails.json", flush=True)
    return 0 if (ok_n and ok_l) else 1


if __name__ == "__main__":
    sys.exit(main())
