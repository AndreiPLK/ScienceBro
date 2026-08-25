"""Bernstein certificate for the repaired odd-depth statement (ERR-0013).

Object: G = A(K,k,delta) + B(K,k,delta) * w from `odd_depth_kwindow.py`, with
w = sqrt(12k^2 - 36k + 9) >= 0 on the domain. Claim certified here:

    G >= 0  on  K in [3, inf) x k in [KMIN, inf) x delta in [-3/2, 3/2],

which is the depth-d knife's positivity at D = T_{k+delta}(lam*(k)) along the
critical curve -- the statement step (b)'s bracketing theorem actually needs
(the integer argmin is within 1 of k* for lam >= 7, and lam(KMIN) < 7 so the
curve coverage overlaps the fixed-k_s band below).

Per-box test: Bernstein lower bounds minA, minB of A and B, plus EXACT
rational brackets [w_lo, w_hi] of w on the box (w is increasing in k for
k >= 3/2, and integer-sqrt bracketing of a rational square root is exact),
give
    G = A + B w  >=  minA + (minB * w_lo  if minB >= 0 else  minB * w_hi),
and the box is proved when that bound is >= 0. No polynomial C = A^2-B^2w^2
is ever formed -- squaring the grids is what made the first version
intractable (killed at 50 minutes with the root grid still unfinished).
Grids are built once at the root by a fast per-axis dense transform (the
generic bernstein_grid is O(grid * monomials), hopeless at ~10^4 terms) and
split exactly by de Casteljau.

Infinite axes are compactified rationally: K = 3/(1-x), k = KMIN/(1-y). The
conic itself never needs a parametrization here, so the irrational point at
k = infinity of the line construction is never touched.

Run: python lab/odd_depth_kwindow_cert.py <d> [max_depth]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric  # noqa: E402
from keystone_unglued import NPoly, compactify, split_grid  # noqa: E402
from odd_depth_kwindow import build_kwindow, lam_of, line_point  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

KMIN = fmpq(12)  # lam*(12) < 7 (checked in main), so the curve piece overlaps
# the fixed-k_s = 8 band that covers lam in [5/2, 7].
DELTA = fmpq(3, 2)


def split_AB(G) -> tuple[NPoly, NPoly]:
    """P4(K,k,delta,w) with w-degree <= 1  ->  (A, B) as NPoly(K,k,delta)."""
    A: dict = {}
    B: dict = {}
    for e, c in G.d.items():
        key = (e[0], e[1], e[2])
        if e[3] == 0:
            A[key] = A.get(key, fmpq(0)) + c
        elif e[3] == 1:
            B[key] = B.get(key, fmpq(0)) + c
        else:
            raise ValueError("G not reduced mod conic")
    return NPoly(A), NPoly(B)


def fast_bernstein_grid(poly: NPoly, box):
    """Bernstein coefficients of poly on box, by per-axis dense transforms:
    O(sum_axis grid*deg_axis) instead of bernstein_grid's O(grid*monomials).
    Returns the same flat-dict format split_grid consumes."""
    from math import comb

    degs = [poly.max_deg(s) for s in range(3)]
    dims = [d + 1 for d in degs]

    # dense array, flat index i0*dims1*dims2 + i1*dims2 + i2
    arr = [fmpq(0)] * (dims[0] * dims[1] * dims[2])
    for (e0, e1, e2), c in poly.d.items():
        arr[(e0 * dims[1] + e1) * dims[2] + e2] = c

    def axis_lines(axis):
        """Yield (base_indices, stride) covering every 1D line along axis."""
        stride = {0: dims[1] * dims[2], 1: dims[2], 2: 1}[axis]
        others = [s for s in range(3) if s != axis]
        for a in range(dims[others[0]]):
            for b in range(dims[others[1]]):
                idx = [0, 0, 0]
                idx[others[0]], idx[others[1]] = a, b
                base = (idx[0] * dims[1] + idx[1]) * dims[2] + idx[2]
                yield base, stride

    for axis in range(3):
        n = degs[axis]
        lo, hi = box[axis]
        wdt = hi - lo
        # x = lo + wdt*t  (affine), then monomial-in-t -> Bernstein
        lo_pow = [fmpq(1)]
        w_pow = [fmpq(1)]
        for _ in range(n):
            lo_pow.append(lo_pow[-1] * lo)
            w_pow.append(w_pow[-1] * wdt)
        aff = [[fmpq(comb(p, m)) * lo_pow[p - m] * w_pow[m] for p in range(n + 1)] for m in range(n + 1)]
        ber = [
            [fmpq(comb(kk, p), comb(n, p)) if p <= kk else fmpq(0) for p in range(n + 1)]
            for kk in range(n + 1)
        ]
        for base, stride in axis_lines(axis):
            line = [arr[base + i * stride] for i in range(n + 1)]
            # affine: b_m = sum_p aff[m][p] * line[p]  (aff[m][p]=0 for p<m)
            tmp = [sum((aff[m][p] * line[p] for p in range(m, n + 1)), fmpq(0)) for m in range(n + 1)]
            # to Bernstein: c_k = sum_{p<=k} ber[k][p] * tmp[p]
            out = [sum((ber[kk][p] * tmp[p] for p in range(kk + 1)), fmpq(0)) for kk in range(n + 1)]
            for i in range(n + 1):
                arr[base + i * stride] = out[i]

    grid = {}
    for i0 in range(dims[0]):
        for i1 in range(dims[1]):
            for i2 in range(dims[2]):
                grid[(i0, i1, i2)] = arr[(i0 * dims[1] + i1) * dims[2] + i2]
    return grid, degs


def sqrt_bracket(x: fmpq) -> tuple[fmpq, fmpq]:
    """Exact rational lo <= sqrt(x) <= hi via integer sqrt (x >= 0)."""
    from math import isqrt

    p, q = int(x.p), int(x.q)
    r = isqrt(p * q)
    return fmpq(r, q), fmpq(r + 1, q)


def w_bracket_on(y_lo: fmpq, y_hi: fmpq) -> tuple[fmpq, fmpq]:
    """[w_lo, w_hi] on a y-box, y the compactified k (k = KMIN/(1-y)).
    w^2 = 12k^2-36k+9 is increasing in k for k >= 3/2, and k is increasing
    in y, so the bracket comes from the box endpoints."""
    k_lo = KMIN / (1 - y_lo)
    k_hi = KMIN / (1 - y_hi)
    w2_lo = k_lo * k_lo * 12 - k_lo * 36 + 9
    w2_hi = k_hi * k_hi * 12 - k_hi * 36 + 9
    lo, _ = sqrt_bracket(w2_lo)
    _, hi = sqrt_bracket(w2_hi)
    return lo, hi


def prove_G(A: NPoly, B: NPoly, box, max_depth: int = 26):
    """Bernstein bisection for A + B*w >= 0 with exact interval brackets on w
    (slot 1 is the compactified k). Exact fmpq throughout."""
    t0 = time.time()
    gA, dA = fast_bernstein_grid(A, box)
    gB, dB = fast_bernstein_grid(B, box)
    print(f"    root grids built ({time.time()-t0:.0f}s)", flush=True)

    root_w = [box[s][1] - box[s][0] for s in range(3)]
    stack = [((gA, gB), box, 0)]
    boxes = 0
    open_boxes = []
    while stack:
        (ga, gb), bx, depth = stack.pop()
        boxes += 1
        if boxes % 500 == 0:
            print(f"    ... {boxes} boxes, {len(stack)} pending, {time.time()-t0:.0f}s", flush=True)
        minA = min(ga.values())
        minB = min(gb.values())
        if minA >= 0 and minB >= 0:
            continue
        w_lo, w_hi = w_bracket_on(bx[1][0], bx[1][1])
        lb = minA + (minB * w_lo if minB >= 0 else minB * w_hi)
        if lb >= 0:
            continue
        if depth >= max_depth:
            open_boxes.append([(str(lo), str(hi)) for lo, hi in bx])
            continue
        rel = [(bx[s][1] - bx[s][0]) / root_w[s] for s in range(3)]
        axis = max(range(3), key=lambda s: rel[s])
        lo, hi = bx[axis]
        mid = (lo + hi) / 2
        lbx, rbx = list(bx), list(bx)
        lbx[axis], rbx[axis] = (lo, mid), (mid, hi)
        la, ra = split_grid(ga, dA, axis)
        lb2, rb2 = split_grid(gb, dB, axis)
        stack += [((la, lb2), lbx, depth + 1), ((ra, rb2), rbx, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def run_depth(d: int, max_depth: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    out: dict = {"depth": d, "KMIN": str(KMIN), "delta_window": [str(-DELTA), str(DELTA)], "branches": {}}
    for parity in ("even", "odd"):
        t1 = time.time()
        G = build_kwindow(parity, d, e_polys)
        A, B = split_AB(G)
        # compactify K in [3, inf) then k in [KMIN, inf); delta stays finite.
        A2 = compactify(compactify(A, 0, 3), 1, KMIN)
        B2 = compactify(compactify(B, 0, 3), 1, KMIN)
        # NOTE: compactify clears (1-t)^deg per polynomial. A and B may carry
        # DIFFERENT cleared powers, which would break the A/B/C sign relations.
        # Equalize: multiply each by the missing (1-t) powers of the other so
        # both carry the same positive factor.
        for slot in (0, 1):
            da, db = A.max_deg(slot), B.max_deg(slot)
            if da == db:
                continue
            one_minus = NPoly.const(1) - NPoly.var(slot)
            if da > db:
                B2 = B2 * one_minus ** (da - db)
            else:
                A2 = A2 * one_minus ** (db - da)
        box = [
            (fmpq(0), fmpq(999, 1000)),
            (fmpq(0), fmpq(999, 1000)),
            (-DELTA, DELTA),
        ]
        ok, boxes, open_boxes = prove_G(A2, B2, box, max_depth=max_depth)
        dt = time.time() - t1
        print(
            f"depth {d} [{parity}]: proved={ok} boxes={boxes} open={len(open_boxes)} ({dt:.0f}s)",
            flush=True,
        )
        out["branches"][parity] = {
            "proved": ok,
            "boxes": boxes,
            "open": len(open_boxes),
            "open_sample": open_boxes[:5],
            "seconds": round(dt, 1),
        }
    out["proved_both"] = all(out["branches"][p]["proved"] for p in ("even", "odd"))
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main() -> int:
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    # coverage check: lam at KMIN must be BELOW 7 so the curve piece overlaps
    # the fixed-k_s band. w(KMIN) is irrational, so bound lam via rational
    # bracketing of w: w^2 = 12*KMIN^2 - 36*KMIN + 9.
    w2 = KMIN * KMIN * 12 - KMIN * 36 + 9
    wlo, whi = fmpq(0), w2 + 1
    for _ in range(80):
        mid = (wlo + whi) / 2
        if mid * mid <= w2:
            wlo = mid
        else:
            whi = mid
    lam_hi = lam_of(KMIN, whi)
    print(f"lam*(KMIN={KMIN}) <= {float(lam_hi):.4f} (must be < 7: {lam_hi < 7})", flush=True)
    assert lam_hi < 7, "KMIN too large: curve piece would not overlap the lam<=7 band"

    # sanity of imported line construction (used only in self-checks elsewhere)
    kq, wq = line_point(fmpq(4))
    assert (kq, wq) == (fmpq(6), fmpq(15))

    res = run_depth(d, max_depth)
    path = RES / "odd_depth_kwindow_cert.json"
    prev = []
    if path.exists():
        try:
            prev = json.loads(path.read_text(encoding="utf-8")).get("runs", [])
        except (json.JSONDecodeError, OSError):
            prev = []
    keep = [r for r in prev if r.get("depth") != res["depth"]]
    path.write_text(
        json.dumps({"runs": sorted(keep + [res], key=lambda r: r["depth"]), **stamp()}, indent=1),
        encoding="utf-8",
    )
    print(f"written {path}", flush=True)
    return 0 if res["proved_both"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
