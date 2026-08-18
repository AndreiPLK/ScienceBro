"""KNIFE 4 ON A COMPACT REGION: a machine proof by exact Bernstein subdivision.

Not a scan. On each box the polynomial is re-expanded in the Bernstein basis with
EXACT rational arithmetic; the minimum of the Bernstein coefficients is a rigorous
lower bound for the polynomial on that box (the convex-hull property). A box is
accepted only when that bound is strictly positive, otherwise it is split. If the
recursion ends with no open box, positivity on the region is proved.

Two earlier attempts are recorded because they were wrong, not because they were
slow:
  * naive interval arithmetic per monomial -- the dependency problem makes the
    enclosure hopeless here (103 monomials with heavy cancellation);
  * "all coefficients non-negative after shifting to the corner" -- far too
    strong a test; it fails even on tiny boxes where the polynomial is clearly
    positive. The correct crude bound is c_0 plus the sum of negative
    coefficients, and Bernstein is sharper still: it closed
    n in [4,12], D in [4,24], lam in [1,2] in a SINGLE box.

DOMAIN, written before computing (the rule paid for twice this night):
    n >= 4          knife 4 does not exist below its own index
    D >= 4          physical; the weight needs D > 3
    D <= min_k T_k(lam_hi)
                    the shore itself, bounded exactly per box: T_hat <= T_k for
                    every k, and each T_k increases in lam, so evaluating at the
                    box's largest lam and minimising over k is a rigorous rational
                    majorant. (The first version used 18.93 lam + 5, which
                    over-included a slab above the shore -- D = 191 at lam = 10
                    where the shore is 187.5 -- and left 739 boxes open there.)
    lam in [1, LAM_MAX], n in [4, N_MAX]

Outside this compact region the two tails are separate statements (see
results/SCALING_LIMIT_THEOREM.md): n -> infinity at fixed (lam, D) has leading
coefficient +280, and lam -> infinity gives the scaling form with the tangency
approached from the safe side.

Run: python lab/knife4_proof.py -> results/knife4_box_proof.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_closed_form import D as Dsym  # noqa: E402
from knife_closed_form import knife_polynomial  # noqa: E402
from knife_closed_form import lam as lamsym
from knife_closed_form import n as nsym
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def shore_upper(lam_hi: F) -> F:
    """Exact rational upper bound for T_hat on a box, using T_hat <= min_k T_k.

    T_k(lam) = 3(2k-3)/(k(k-2)) (lam^2 + (2k-2) lam + 1) + 2k is increasing in lam
    for lam > 0, so evaluating at the box's largest lam and minimising over k gives
    a bound valid on the whole box. An earlier version used the crude
    18.93 lam + 5, which over-included a slab ABOVE the shore (D = 191 at lam = 10,
    where the shore is 187.5) and left 739 boxes open there for no reason.
    """
    best = None
    kmax = max(61, int(3 * float(lam_hi)) + 60)
    for k in range(3, kmax):
        v = F(3 * (2 * k - 3), k * (k - 2)) * (lam_hi * lam_hi + (2 * k - 2) * lam_hi + 1) + 2 * k
        if best is None or v < best:
            best = v
    return best


_P = sp.expand(knife_polynomial(4))
MD = (int(sp.degree(_P, nsym)), int(sp.degree(_P, Dsym)), int(sp.degree(_P, lamsym)))
_poly = sp.Poly(_P, nsym, Dsym, lamsym)
COEFFS = {
    m: F(int(sp.Rational(c).p), int(sp.Rational(c).q))
    for m, c in zip(_poly.monoms(), _poly.coeffs())
}


def shifted_coeffs(box):
    """Coefficients of P4(box(s)) in the powers of s on [0,1]^3, exact."""
    (n0, n1), (d0, d1), (l0, l1) = box
    m1, m2, m3 = MD
    # expand each variable as v0 + w*s and multiply out, binomially
    out: dict[tuple[int, int, int], F] = {}
    wn, wd, wl = n1 - n0, d1 - d0, l1 - l0
    for (a, b, c), coeff in COEFFS.items():
        for i in range(a + 1):
            ci = coeff * comb(a, i) * n0 ** (a - i) * wn**i
            if ci == 0:
                continue
            for j in range(b + 1):
                cj = ci * comb(b, j) * d0 ** (b - j) * wd**j
                if cj == 0:
                    continue
                for k in range(c + 1):
                    ck = cj * comb(c, k) * l0 ** (c - k) * wl**k
                    if ck == 0:
                        continue
                    key = (i, j, k)
                    out[key] = out.get(key, F(0)) + ck
    return out


def bernstein_lower(box):
    """min of the Bernstein coefficients: a rigorous lower bound on the box."""
    a = shifted_coeffs(box)
    m1, m2, m3 = MD
    best = None
    for i, j, k in product(range(m1 + 1), range(m2 + 1), range(m3 + 1)):
        b = F(0)
        for p in range(i + 1):
            cp = F(comb(i, p), comb(m1, p))
            for q in range(j + 1):
                cq = cp * F(comb(j, q), comb(m2, q))
                for r in range(k + 1):
                    c = a.get((p, q, r))
                    if c:
                        b += c * cq * F(comb(k, r), comb(m3, r))
        if best is None or b < best:
            best = b
            if best <= 0:
                return best  # early exit: this box will be split anyway
    return best


def prove(n_max: float, lam_max: float, max_depth: int = 30):
    lam_hi = F(lam_max).limit_denominator(10**6)
    stack = [
        ((F(4), F(n_max).limit_denominator(10**6)), (F(4), shore_upper(lam_hi)), (F(1), lam_hi), 0)
    ]
    boxes = 0
    open_boxes = []
    while stack:
        nb, db, lb, depth = stack.pop()
        top = shore_upper(lb[1])
        db = (db[0], min(db[1], top))
        if db[0] >= db[1]:
            continue
        boxes += 1
        if bernstein_lower((nb, db, lb)) > 0:
            continue
        if depth >= max_depth:
            open_boxes.append((nb, db, lb))
            continue
        widths = [
            (nb[1] - nb[0]) / max(F(1), nb[0]),
            (db[1] - db[0]) / max(F(1), db[0]),
            (lb[1] - lb[0]) / max(F(1), lb[0]),
        ]
        k = widths.index(max(widths))
        if k == 0:
            m = (nb[0] + nb[1]) / 2
            stack += [((nb[0], m), db, lb, depth + 1), ((m, nb[1]), db, lb, depth + 1)]
        elif k == 1:
            m = (db[0] + db[1]) / 2
            stack += [(nb, (db[0], m), lb, depth + 1), (nb, (m, db[1]), lb, depth + 1)]
        else:
            m = (lb[0] + lb[1]) / 2
            stack += [(nb, db, (lb[0], m), depth + 1), (nb, db, (m, lb[1]), depth + 1)]
    return (not open_boxes), boxes, open_boxes


def main() -> int:
    t0 = time.time()
    rows = []
    for n_max, lam_max in ((200, 30), (400, 60), (1000, 120)):
        ok, boxes, open_boxes = prove(n_max, lam_max)
        rows.append(
            {
                "n_max": n_max,
                "lam_max": lam_max,
                "proved": ok,
                "boxes": boxes,
                "open": len(open_boxes),
            }
        )
        print(
            f"  n <= {n_max}, lam <= {lam_max}: proved={ok}, boxes={boxes}, "
            f"open={len(open_boxes)}  ({time.time() - t0:.0f}s)",
            flush=True,
        )
        if not ok:
            print("     first open box:", open_boxes[0], flush=True)
    out = {
        "claim": "P4 > 0 on {4 <= n <= n_max, 4 <= D <= shore(lam), 1 <= lam <= lam_max},"
        " proved by exact Bernstein subdivision (convex-hull bound)",
        "why_the_D_bound_is_legitimate": "T_hat <= T_k for every k and each T_k is increasing in lam, so"
        " min_k T_k(lam_hi) is a rigorous rational majorant of the shore on the box",
        "regions": rows,
        "command": "python lab/knife4_proof.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "knife4_box_proof.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/knife4_box_proof.json", flush=True)
    return 0 if all(r["proved"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
