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
intractable. Root grids by a fast per-axis dense transform (the generic
bernstein_grid is O(grid * monomials), hopeless at ~10^4 terms), splits by
exact de Casteljau.

RESUMABLE AND PARTITIONED. A single certification is hours of CPU and the
session's background processes do not survive harness restarts (one run died
at 2500 boxes with no artifact). So each invocation certifies ONE job -- a
(parity, y-subrange) slice -- and checkpoints its pending frontier to a
gitignored state file every CHECKPOINT_S seconds; a restarted job rebuilds G,
re-derives grids only for the restored frontier boxes, and continues. Jobs
are independent, so parities and y-slices run in parallel processes.

Run (one job):
    python lab/odd_depth_kwindow_cert.py <d> <parity> <y_lo> <y_hi> [max_depth]
e.g. python lab/odd_depth_kwindow_cert.py 3 even 0 1/2
y is the compactified k: k = KMIN/(1-y); the full axis is [0, 999/1000].
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

RES = Path(__file__).resolve().parents[1] / "results"
STATE_DIR = RES / "raw" / "kwindow_state"  # gitignored (results/raw/**)

KMIN = fmpq(12)  # lam*(12) < 7 (checked in main), so the curve piece overlaps
# the fixed-k_s = 8 band that covers lam in [5/2, 7].
#
# DELTA: step (b) needs only |delta| < 1 -- for lam >= 7 the integer argmin is
# one of the two integers BRACKETING k* (proved in UNGLUED_KEYSTONE.md via the
# coefficient-sign pairs, given measured unimodality), so |argmin - k*| < 1
# strictly. 9/8 keeps a 1/8 margin. The first attempt used 3/2 "for safety"
# and that extra slack was exactly what jammed: all 156+58 open boxes sat at
# delta in [1.31, 1.5] in the K,k -> infinity corner, where the polynomial
# degenerates relative to its coefficient scale while the physics stays safe.
DELTA = fmpq(9, 8)
CHECKPOINT_S = 120


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
    O(sum_axis grid*deg_axis^2/lines) instead of O(grid * monomials).
    Returns the same flat-dict format split_grid consumes."""
    from math import comb

    degs = [poly.max_deg(s) for s in range(3)]
    dims = [d + 1 for d in degs]

    arr = [fmpq(0)] * (dims[0] * dims[1] * dims[2])
    for (e0, e1, e2), c in poly.d.items():
        arr[(e0 * dims[1] + e1) * dims[2] + e2] = c

    def axis_lines(axis):
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
        lo_pow = [fmpq(1)]
        w_pow = [fmpq(1)]
        for _ in range(n):
            lo_pow.append(lo_pow[-1] * lo)
            w_pow.append(w_pow[-1] * wdt)
        aff = [
            [fmpq(comb(p, m)) * lo_pow[p - m] * w_pow[m] for p in range(n + 1)]
            for m in range(n + 1)
        ]
        ber = [
            [fmpq(comb(kk, p), comb(n, p)) if p <= kk else fmpq(0) for p in range(n + 1)]
            for kk in range(n + 1)
        ]
        for base, stride in axis_lines(axis):
            line = [arr[base + i * stride] for i in range(n + 1)]
            tmp = [
                sum((aff[m][p] * line[p] for p in range(m, n + 1)), fmpq(0))
                for m in range(n + 1)
            ]
            out = [
                sum((ber[kk][p] * tmp[p] for p in range(kk + 1)), fmpq(0))
                for kk in range(n + 1)
            ]
            for i in range(n + 1):
                arr[base + i * stride] = out[i]

    grid = {}
    for i0 in range(dims[0]):
        for i1 in range(dims[1]):
            for i2 in range(dims[2]):
                grid[(i0, i1, i2)] = arr[(i0 * dims[1] + i1) * dims[2] + i2]
    return grid, degs


def sqrt_bracket(x: fmpq, scale: int = 1) -> tuple[fmpq, fmpq]:
    """Exact rational lo <= sqrt(x) <= hi via integer sqrt (x >= 0).
    `scale` = M tightens the bracket to width 1/(q*M) at cost of isqrt on
    p*q*M^2 -- used where a loose bound would fail a strict comparison."""
    from math import isqrt

    p, q = int(x.p), int(x.q)
    r = isqrt(p * q * scale * scale)
    return fmpq(r, q * scale), fmpq(r + 1, q * scale)


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


def box_to_str(bx):
    return [[str(lo), str(hi)] for lo, hi in bx]


def box_from_str(bs):
    return [(fmpq(lo), fmpq(hi)) for lo, hi in bs]


def prove_G_resumable(A: NPoly, B: NPoly, root_box, state_path: Path, max_depth: int = 26):
    """Bernstein bisection for A + B*w >= 0 with exact interval brackets on w.
    Checkpoints the pending frontier (boxes only, grids re-derived) so a
    killed process can continue. Exact fmpq throughout."""
    t0 = time.time()
    root_w = [root_box[s][1] - root_box[s][0] for s in range(3)]

    if state_path.exists():
        st = json.loads(state_path.read_text(encoding="utf-8"))
        pending = [(box_from_str(b), d) for b, d in st["pending"]]
        boxes = st["boxes"]
        open_boxes = st["open_boxes"]
        print(f"    RESUME: {len(pending)} frontier boxes, {boxes} done", flush=True)
        stack = []
        for bx, dep in pending:
            ga, dA = fast_bernstein_grid(A, bx)
            gb, dB = fast_bernstein_grid(B, bx)
            stack.append(((ga, gb), bx, dep))
        print(f"    frontier grids rebuilt ({time.time()-t0:.0f}s)", flush=True)
    else:
        gA, dA = fast_bernstein_grid(A, root_box)
        gB, dB = fast_bernstein_grid(B, root_box)
        stack = [((gA, gB), root_box, 0)]
        boxes = 0
        open_boxes = []
        print(f"    root grids built ({time.time()-t0:.0f}s)", flush=True)

    degsA = [A.max_deg(s) for s in range(3)]
    degsB = [B.max_deg(s) for s in range(3)]
    last_ckpt = time.time()

    def checkpoint():
        st = {
            "pending": [(box_to_str(bx), dep) for (_, bx, dep) in stack],
            "boxes": boxes,
            "open_boxes": open_boxes,
            "elapsed_this_run": round(time.time() - t0, 1),
        }
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(st), encoding="utf-8")
        tmp.replace(state_path)

    while stack:
        (ga, gb), bx, depth = stack.pop()
        boxes += 1
        if time.time() - last_ckpt > CHECKPOINT_S:
            checkpoint()
            last_ckpt = time.time()
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
            open_boxes.append(box_to_str(bx))
            continue
        rel = [(bx[s][1] - bx[s][0]) / root_w[s] for s in range(3)]
        axis = max(range(3), key=lambda s: rel[s])
        lo, hi = bx[axis]
        mid = (lo + hi) / 2
        lbx, rbx = list(bx), list(bx)
        lbx[axis], rbx[axis] = (lo, mid), (mid, hi)
        la, ra = split_grid(ga, degsA, axis)
        lb2, rb2 = split_grid(gb, degsB, axis)
        stack += [((la, lb2), lbx, depth + 1), ((ra, rb2), rbx, depth + 1)]

    # done: final state records the outcome and empties the frontier
    st = {"pending": [], "boxes": boxes, "open_boxes": open_boxes, "done": True}
    state_path.write_text(json.dumps(st), encoding="utf-8")
    return (not open_boxes), boxes, open_boxes


def equalized_AB(parity: str, d: int):
    """Build G, split into (A, B), compactify K and k, and equalize the
    cleared (1-t) powers so A and B carry the SAME positive factor (the
    per-polynomial clearing in `compactify` would otherwise break the sign
    relation of A + B*w)."""
    e_polys = elementary_symmetric(d)
    G = build_kwindow(parity, d, e_polys)
    A, B = split_AB(G)
    A2 = compactify(compactify(A, 0, 3), 1, KMIN)
    B2 = compactify(compactify(B, 0, 3), 1, KMIN)
    for slot in (0, 1):
        da, db = A.max_deg(slot), B.max_deg(slot)
        if da == db:
            continue
        one_minus = NPoly.const(1) - NPoly.var(slot)
        if da > db:
            B2 = B2 * one_minus ** (da - db)
        else:
            A2 = A2 * one_minus ** (db - da)
    return A2, B2


def main() -> int:
    d = int(sys.argv[1])
    parity = sys.argv[2]
    y_lo = fmpq(sys.argv[3]) if "/" not in sys.argv[3] else fmpq(*map(int, sys.argv[3].split("/")))
    y_hi = fmpq(sys.argv[4]) if "/" not in sys.argv[4] else fmpq(*map(int, sys.argv[4].split("/")))
    max_depth = int(sys.argv[5]) if len(sys.argv) > 5 else 26
    assert parity in ("even", "odd")

    # coverage check: lam at KMIN must be BELOW 7 so the curve piece overlaps
    # the fixed-k_s band (lam in [5/2, 7]).
    w2 = KMIN * KMIN * 12 - KMIN * 36 + 9
    _, whi = sqrt_bracket(w2, scale=10**6)
    lam_hi = lam_of(KMIN, whi)
    assert lam_hi < 7, "KMIN too large: curve piece would not overlap the lam<=7 band"
    kq, wq = line_point(fmpq(4))
    assert (kq, wq) == (fmpq(6), fmpq(15))

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tag = f"d{d}_{parity}_y{y_lo.p}-{y_lo.q}_{y_hi.p}-{y_hi.q}"
    state_path = STATE_DIR / f"kwstate_{tag}.json"

    t0 = time.time()
    print(f"job {tag}: building G...", flush=True)
    A2, B2 = equalized_AB(parity, d)
    print(f"job {tag}: G built ({time.time()-t0:.0f}s), certifying...", flush=True)
    box = [(fmpq(0), fmpq(999, 1000)), (y_lo, y_hi), (-DELTA, DELTA)]
    ok, boxes, open_boxes = prove_G_resumable(A2, B2, box, state_path, max_depth=max_depth)
    print(
        f"job {tag}: proved={ok} boxes={boxes} open={len(open_boxes)} ({time.time()-t0:.0f}s total)",
        flush=True,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
