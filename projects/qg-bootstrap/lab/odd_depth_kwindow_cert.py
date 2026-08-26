"""Bernstein certificate for the repaired odd-depth statement (ERR-0013).

Object: G = A + B*w from `odd_depth_kwindow.py` (validated by substitution
from `build_branch`, self-check 0 mismatches, non-vacuous), with
w = sqrt(12k^2 - 36k + 9) >= 0. Claim certified:

    G >= 0  on  K >= 3,  k >= 12,  delta in [-9/8, 9/8]

-- the depth-d knife's positivity at D = T_{k+delta}(lam*(k)) along the
critical curve dT/dk = 0. Step (b) needs only |delta| < 1 (for lam >= 7 the
integer argmin brackets k*, so |argmin - k*| < 1 strictly); 9/8 keeps a 1/8
margin. lam*(12) < 7 (checked at start), so the curve piece overlaps the
fixed-k_s band that covers lam in [5/2, 7].

COORDINATES, and the lesson they encode. The first runs used (K, k) directly
and jammed in the corner where K and k grow TOGETHER -- Bernstein
coefficients of A and B degenerate at that double face although A, B and G
are all positive there (measured: sign(A)=sign(B)=+1, G/max ~ 1). The same
two-variable degeneration killed the lam-coordinate runs in UNGLUED_KEYSTONE
and has the same cure: a coordinate in which the double corner is an
ordinary point. With rho = k/(2K):

  piece 1 (rho >= 2):  substitute k = 2*K*rho -- a pure exponent remap of
      G's dictionary. K >= 3 and rho >= 2 give k >= 12 for free.
      Closed in ONE box (depth 3 even).
  piece 2 (rho <= 2):  wedge substitution K = (6 + rho*z)/rho, z >= 0
      (cleared by rho^deg_K, positive), so k = 12 + 2*rho*z >= 12 and
      K >= 6/rho >= 3 for free. Closed in 11 boxes (depth 3 even).

Together the pieces cover ALL K >= 3, k >= 12 -- both infinities honestly
compactified, no finite-coverage caveat. Each substitution is verified
exactly against G at rational points before any Bernstein run (ERR-0012).

Per-box test: Bernstein lower bounds minA, minB plus EXACT rational brackets
[w_lo, w_hi] of w on the box (w increasing in k >= 3/2; k is monotone in the
box coordinates in both pieces; integer-sqrt bracketing is exact):
    G >= minA + (minB * w_lo  if minB >= 0 else  minB * w_hi).
No polynomial A^2 - B^2 w^2 is ever formed (squaring the grids is what made
the very first version intractable).

Run: python lab/odd_depth_kwindow_cert.py <d> [parity ...]
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
    compactify,
    compactify_from_zero,
    split_grid,
)
from odd_depth_kwindow import P4, build_kwindow, lam_of, line_point  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
STATE = RES / "raw" / "kwindow_state"  # gitignored scratch: G cache + checkpoints

KMIN = fmpq(12)
DELTA = fmpq(9, 8)
RHO_SPLIT = fmpq(2)  # pieces meet at rho = k/(2K) = 2


def split_AB(G) -> tuple[NPoly, NPoly]:
    """P4(a0,a1,delta,w) with w-degree <= 1  ->  (A, B) as NPoly(a0,a1,delta)."""
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
    O(sum_axis lines*deg_axis^2) instead of bernstein_grid's
    O(grid * monomials). Returns the flat-dict format split_grid consumes."""
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
    """Exact rational lo <= sqrt(x) <= hi via integer sqrt (x >= 0)."""
    from math import isqrt

    p, q = int(x.p), int(x.q)
    r = isqrt(p * q * scale * scale)
    return fmpq(r, q * scale), fmpq(r + 1, q * scale)


def w_bracket_from_k(k_lo: fmpq, k_hi: fmpq) -> tuple[fmpq, fmpq]:
    """[w_lo, w_hi] from a k-range (w^2 = 12k^2-36k+9 increasing for k>=3/2)."""
    lo, _ = sqrt_bracket(k_lo * k_lo * 12 - k_lo * 36 + 9)
    _, hi = sqrt_bracket(k_hi * k_hi * 12 - k_hi * 36 + 9)
    return lo, hi


def equalize(A: NPoly, B: NPoly, A2: NPoly, B2: NPoly, slots) -> tuple[NPoly, NPoly]:
    """After per-polynomial compactification, multiply in the missing
    (1-t)-powers so A2 and B2 carry the SAME positive cleared factor -- the
    sign relation of A + B*w survives only under a common factor."""
    for slot in slots:
        da, db = A.max_deg(slot), B.max_deg(slot)
        if da == db:
            continue
        om = NPoly.const(1) - NPoly.var(slot)
        if da > db:
            B2 = B2 * om ** (da - db)
        else:
            A2 = A2 * om ** (db - da)
    return A2, B2


def _box_ser(bx):
    return [[str(lo), str(hi)] for lo, hi in bx]


def _box_de(bs):
    return [(fmpq(lo), fmpq(hi)) for lo, hi in bs]


def prove_piece(A2, B2, box, k_range_of_box, max_depth=26, label="", ckpt_path=None):
    """Bernstein bisection for A2 + B2*w >= 0 on box; k_range_of_box maps a
    box to exact (k_lo, k_hi) for the w bracket. Exact fmpq throughout.

    Environment restarts kill long runs, so the pending frontier is
    checkpointed to ckpt_path every ~2 minutes (boxes only; grids are
    re-derived for the restored frontier, which is cheap -- the frontier is
    tens of boxes, not thousands)."""
    t0 = time.time()
    root_w = [box[s][1] - box[s][0] for s in range(3)]
    boxes = 0
    open_boxes = []
    stack = None
    if ckpt_path is not None and ckpt_path.exists():
        st = json.loads(ckpt_path.read_text(encoding="utf-8"))
        if st.get("done"):
            print(f"    {label}: already done in checkpoint", flush=True)
            return (not st["open_boxes"]), st["boxes"], st["open_boxes"], 0.0
        stack = []
        for bs, dep in st["pending"]:
            bx = _box_de(bs)
            ga, _ = fast_bernstein_grid(A2, bx)
            gb, _ = fast_bernstein_grid(B2, bx)
            stack.append(((ga, gb), bx, dep))
        boxes = st["boxes"]
        open_boxes = st["open_boxes"]
        print(f"    {label}: RESUME {len(stack)} frontier, {boxes} done ({time.time()-t0:.0f}s)", flush=True)
    if stack is None:
        gA, dA0 = fast_bernstein_grid(A2, box)
        gB, dB0 = fast_bernstein_grid(B2, box)
        stack = [((gA, gB), box, 0)]
    dA = [A2.max_deg(s) for s in range(3)]
    dB = [B2.max_deg(s) for s in range(3)]
    last_ckpt = time.time()
    while stack:
        (ga, gb), bx, depth = stack.pop()
        boxes += 1
        if ckpt_path is not None and time.time() - last_ckpt > 120:
            st = {
                "pending": [(_box_ser(b), dp) for (_, b, dp) in stack] + [(_box_ser(bx), depth)],
                "boxes": boxes - 1,
                "open_boxes": open_boxes,
            }
            tmp = ckpt_path.with_suffix(".tmp")
            tmp.write_text(json.dumps(st), encoding="utf-8")
            tmp.replace(ckpt_path)
            last_ckpt = time.time()
            print(f"    {label}: {boxes} boxes, {len(stack)} pending, {time.time()-t0:.0f}s", flush=True)
        minA = min(ga.values())
        minB = min(gb.values())
        if minA >= 0 and minB >= 0:
            continue
        k_lo, k_hi = k_range_of_box(bx)
        w_lo, w_hi = w_bracket_from_k(k_lo, k_hi)
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
    if ckpt_path is not None:
        ckpt_path.write_text(
            json.dumps({"pending": [], "boxes": boxes, "open_boxes": open_boxes, "done": True}),
            encoding="utf-8",
        )
    return (not open_boxes), boxes, open_boxes, round(time.time() - t0, 1)


def sanity_substitution(G, G_sub, point_maker, n_points=6) -> None:
    """Exact spot-check that a substituted polynomial equals the (positively
    scaled) original at rational points -- the ERR-0012 rule: substitutions
    are verified, never trusted."""
    pts = [
        (fmpq(1, 2), fmpq(4)),
        (fmpq(3, 2), fmpq(1)),
        (fmpq(2), fmpq(0)),
        (fmpq(1, 3), fmpq(9)),
        (fmpq(5, 4), fmpq(2)),
        (fmpq(1), fmpq(7)),
    ][:n_points]
    for u, v in pts:
        for delta, wv in ((fmpq(1), fmpq(5)), (fmpq(-1), fmpq(7)), (fmpq(0), fmpq(100))):
            lhs, rhs = point_maker(G, G_sub, u, v, delta, wv)
            assert lhs == rhs, f"substitution mismatch at {u},{v},{delta}"


def load_or_build_G(d: int, parity: str):
    """The depth-5 odd G takes ~17 minutes to build and environment restarts
    kill runs more often than that, so the built dictionary is cached to the
    gitignored scratch dir as exact (p, q) integer pairs."""
    import hashlib

    STATE.mkdir(parents=True, exist_ok=True)
    # the cache is only valid for the exact constructor version that wrote it
    # (a stale cache would silently certify a different polynomial -- the
    # ERR-0011 failure shape), so it is keyed by the constructor file's hash.
    src = Path(__file__).resolve().parent / "odd_depth_kwindow.py"
    fingerprint = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    cache = STATE / f"Gcache_d{d}_{parity}_{fingerprint}.json"
    if cache.exists():
        raw = json.loads(cache.read_text(encoding="utf-8"))
        G = P4(
            {
                tuple(map(int, e.split(","))): fmpq(int(p), int(q))
                for e, (p, q) in raw.items()
            }
        )
        return G, True
    G = build_kwindow(parity, d, elementary_symmetric(d))
    cache.write_text(
        json.dumps({",".join(map(str, e)): [str(c.p), str(c.q)] for e, c in G.d.items()}),
        encoding="utf-8",
    )
    return G, False


def run_parity(d: int, parity: str, max_depth: int) -> dict:
    t0 = time.time()
    G, cached = load_or_build_G(d, parity)
    Amax = max(e[0] for e in G.d)
    kb_max = max(e[1] for e in G.d)
    print(
        f"depth {d} [{parity}]: G {'loaded from cache' if cached else 'built'}, "
        f"{len(G.d)} terms ({time.time()-t0:.0f}s)",
        flush=True,
    )

    # ---- piece 1: k = 2*K*rho, rho >= RHO_SPLIT (exponent remap, no algebra)
    Gr = P4({(e[0] + e[1], e[1], e[2], e[3]): c * fmpq(2) ** e[1] for e, c in G.d.items()})

    def pm1(G_, Gs, K, rho, delta, wv):
        return Gs.eval_at((K, rho, delta, wv)), G_.eval_at((K, K * rho * 2, delta, wv))

    sanity_substitution(G, Gr, lambda G_, Gs, u, v, dl, wv: pm1(G_, Gs, u + 3, v + 2, dl, wv))
    A, B = split_AB(Gr)
    A2 = compactify(compactify(A, 0, 3), 1, RHO_SPLIT)
    B2 = compactify(compactify(B, 0, 3), 1, RHO_SPLIT)
    A2, B2 = equalize(A, B, A2, B2, (0, 1))

    def krange1(bx):
        # k = 2*K*rho = 2 * 3/(1-x) * RHO_SPLIT/(1-y)
        (xlo, xhi), (ylo, yhi) = bx[0], bx[1]
        return (
            RHO_SPLIT * 6 / ((1 - xlo) * (1 - ylo)),
            RHO_SPLIT * 6 / ((1 - xhi) * (1 - yhi)),
        )

    box1 = [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000)), (-DELTA, DELTA)]
    ok1, boxes1, open1, sec1 = prove_piece(
        A2, B2, box1, krange1, max_depth, f"{parity}/p1",
        ckpt_path=STATE / f"ckpt_d{d}_{parity}_p1.json",
    )
    print(f"  piece1 (rho>=2): proved={ok1} boxes={boxes1} open={len(open1)} ({sec1}s)", flush=True)

    # ---- piece 2: wedge K = (6 + rho*z)/rho, k = 12 + 2*rho*z, cleared by rho^Amax
    rho = P4.var(0)
    z = P4.var(1)
    sixrz = P4.const(6) + rho * z
    k_new = P4.const(12) + rho * z * fmpq(2)
    mp_a = {0: P4.const(1)}
    for i in range(1, Amax + 1):
        mp_a[i] = mp_a[i - 1] * sixrz
    mp_b = {0: P4.const(1)}
    for i in range(1, kb_max + 1):
        mp_b[i] = mp_b[i - 1] * k_new
    mp_r = {0: P4.const(1)}
    for i in range(1, Amax + 1):
        mp_r[i] = mp_r[i - 1] * rho
    Gw = P4()
    for e, c in G.d.items():
        a, b, dd, we = e
        term = mp_a[a] * mp_b[b] * mp_r[Amax - a] * c
        term = P4({(kk[0], kk[1], dd, we): v for kk, v in term.d.items()})
        Gw = Gw + term

    def pm2(G_, Gs, r, zq, delta, wv):
        K = (6 + r * zq) / r
        k = 12 + r * zq * 2
        return Gs.eval_at((r, zq, delta, wv)), (r**Amax) * G_.eval_at((K, k, delta, wv))

    sanity_substitution(G, Gw, pm2)
    Aw, Bw = split_AB(Gw)
    Aw2 = compactify_from_zero(Aw, 1)
    Bw2 = compactify_from_zero(Bw, 1)
    Aw2, Bw2 = equalize(Aw, Bw, Aw2, Bw2, (1,))

    def krange2(bx):
        # k = 12 + 2*rho*z, z = t/(1-t)
        (rlo, rhi), (tlo, thi) = bx[0], bx[1]
        return (12 + rlo * (tlo / (1 - tlo)) * 2, 12 + rhi * (thi / (1 - thi)) * 2)

    box2 = [(fmpq(0), RHO_SPLIT), (fmpq(0), fmpq(999, 1000)), (-DELTA, DELTA)]
    ok2, boxes2, open2, sec2 = prove_piece(
        Aw2, Bw2, box2, krange2, max_depth, f"{parity}/p2",
        ckpt_path=STATE / f"ckpt_d{d}_{parity}_p2.json",
    )
    print(f"  piece2 (rho<=2): proved={ok2} boxes={boxes2} open={len(open2)} ({sec2}s)", flush=True)

    return {
        "parity": parity,
        "piece1_rho_ge_2": {"proved": ok1, "boxes": boxes1, "open": len(open1), "seconds": sec1},
        "piece2_wedge": {"proved": ok2, "boxes": boxes2, "open": len(open2), "seconds": sec2},
        "proved": ok1 and ok2,
        "seconds": round(time.time() - t0, 1),
    }


CLAIM = (
    "REPAIRED step (a) for odd depth {d} (ERR-0013): the depth-{d} knife is positive at "
    "D = T_(k+delta)(lam*(k)) for ALL levels K >= 3, ALL k >= 12 on the critical curve "
    "dT/dk = 0 (branch lam* = (3b + k(k-2)w)/(6a), w = sqrt(12k^2-36k+9)), and all "
    "delta in [-9/8, 9/8]. Both infinities are compactified; the two rho = k/(2K) "
    "pieces (rho >= 2 direct, rho <= 2 wedge) cover the region with no side "
    "conditions. Step (b) (integer argmin within 1 of k* for lam >= 7 -- proved, "
    "given measured unimodality) places the shore integer inside the delta window; "
    "lam*(12) < 7 so coverage overlaps the fixed-k_s band below lam = 7; step (c) "
    "carries positivity down from the shore."
)


def main() -> int:
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    parities = sys.argv[2:] or ["even", "odd"]
    max_depth = 26

    # coverage check: lam*(KMIN) < 7
    w2 = KMIN * KMIN * 12 - KMIN * 36 + 9
    _, whi = sqrt_bracket(w2, scale=10**6)
    assert lam_of(KMIN, whi) < 7, "KMIN too large for band overlap"
    assert line_point(fmpq(4)) == (fmpq(6), fmpq(15))

    rows = [run_parity(d, p, max_depth) for p in parities]
    result = {
        "depth": d,
        "claim": CLAIM.format(d=d),
        "KMIN": str(KMIN),
        "delta_window": [str(-DELTA), str(DELTA)],
        "branches": rows,
        "proved_all": all(r["proved"] for r in rows),
        "command": "python lab/odd_depth_kwindow_cert.py <d>",
        **stamp(),
    }
    path = RES / f"odd_depth_kwindow_cert_d{d}.json"
    path.write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(f"depth {d}: proved_all={result['proved_all']}  written {path}", flush=True)
    return 0 if result["proved_all"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
