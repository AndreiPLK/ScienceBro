"""Bernstein certificate for the repaired odd-depth statement (ERR-0013).

Object: G = A(K,k,delta) + B(K,k,delta) * w from `odd_depth_kwindow.py`, with
w = sqrt(12k^2 - 36k + 9) >= 0 on the domain. Claim certified here:

    G >= 0  on  K in [3, inf) x k in [KMIN, inf) x delta in [-3/2, 3/2],

which is the depth-d knife's positivity at D = T_{k+delta}(lam*(k)) along the
critical curve -- the statement step (b)'s bracketing theorem actually needs
(the integer argmin is within 1 of k* for lam >= 7, and lam(KMIN) < 7 so the
curve coverage overlaps the fixed-k_s band below).

Per-box tests, together complete wherever G > 0 (C := A^2 - B^2 * w^2, a
polynomial since w^2 is one):
  (i)   minB A >= 0 and minB B >= 0          -> G >= 0  (w >= 0)
  (ii)  minB A >= 0 and minB C >= 0          -> |B| w <= A, so G >= 0
  (iii) minB B >= 0 and maxB C <= 0          -> B w >= |A|, so G >= 0
where minB/maxB are Bernstein coefficient bounds. All three polynomials are
carried as Bernstein grids from the root and split exactly by de Casteljau
(the keystone_unglued machinery, reused).

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
from keystone_unglued import (  # noqa: E402
    NPoly,
    bernstein_grid,
    compactify,
    split_grid,
)
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


def prove_G(A: NPoly, B: NPoly, C: NPoly, box, max_depth: int = 26):
    """Three-test Bernstein bisection for A + B*w >= 0, where C is any
    polynomial with sign(C) = sign(A^2 - B^2 w^2) on the box. Exact fmpq."""

    grids = []
    degs = []
    for poly in (A, B, C):
        g, dg = bernstein_grid(poly, box)
        grids.append(g)
        degs.append(dg)

    root_w = [box[s][1] - box[s][0] for s in range(3)]
    stack = [(grids, box, 0)]
    boxes = 0
    open_boxes = []
    t0 = time.time()
    while stack:
        gs, bx, depth = stack.pop()
        boxes += 1
        if boxes % 2000 == 0:
            print(f"    ... {boxes} boxes, {len(stack)} pending, {time.time()-t0:.0f}s", flush=True)
        minA = min(gs[0].values())
        minB = min(gs[1].values())
        if minA >= 0 and minB >= 0:
            continue
        minC = min(gs[2].values())
        if minA >= 0 and minC >= 0:
            continue
        maxC = max(gs[2].values())
        if minB >= 0 and maxC <= 0:
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
        lgs, rgs = [], []
        for g, dg in zip(gs, degs):
            lg, rg = split_grid(g, dg, axis)
            lgs.append(lg)
            rgs.append(rg)
        stack += [(lgs, lbx, depth + 1), (rgs, rbx, depth + 1)]
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
        # In the compactified k-coordinate y (k = KMIN/(1-y)),
        #   w^2 = [12 KMIN^2 - 36 KMIN (1-y) + 9 (1-y)^2] / (1-y)^2 = W2/(1-y)^2,
        # so  sign(A2^2 - B2^2 w^2) = sign( (A2 (1-y))^2 - B2^2 W2 )  since
        # (1-y)^2 > 0 on the box. That product is the C passed to prove_G.
        one_minus_y = NPoly.const(1) - NPoly.var(1)
        W2 = (
            NPoly.const(KMIN * KMIN * 12)
            - one_minus_y * (KMIN * 36)
            + one_minus_y * one_minus_y * fmpq(9)
        )
        C2 = (A2 * one_minus_y) * (A2 * one_minus_y) - B2 * B2 * W2
        box = [
            (fmpq(0), fmpq(999, 1000)),
            (fmpq(0), fmpq(999, 1000)),
            (-DELTA, DELTA),
        ]
        ok, boxes, open_boxes = prove_G(A2, B2, C2, box, max_depth=max_depth)
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
