"""Where is the WORST relative margin of H over the lo box, per depth?

The factor probe broke the corner-cancellation diagnosis: the margin at the
hard corner (K=1000, c=5/12, v=2) decreases smoothly with depth -- 2.2e-3,
7.8e-5, 3.1e-6, 1.1e-7 for depths 2, 3, 4, 5 -- with NO parity structure,
while certification alternates: even closes, odd does not. So the corner
number cannot be what separates them, and the actual worst point of the odd
depths must sit somewhere the diagnosis never sampled (the ERR-0005 lesson:
an extremum quoted from a grid is only an extremum of the grid).

This scans the relative margin value/max|monomial| on a dense-ish grid over
the lo box K in [3, ~4000] x c in [5/12, 50] x v in [8/5, 2], refines around
the worst grid point by coordinate descent, and reports worst margin and its
location per depth/parity. Exact fmpq arithmetic; float for printing only.

Run: python lab/odd_depth_margin_scan.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric  # noqa: E402
from keystone_unglued import build_branch  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

K_GRID = [fmpq(x) for x in (3, 4, 5, 6, 8, 12, 20, 40, 100, 300, 1000, 4000)]
C_GRID = [fmpq(5, 12), fmpq(1, 2), fmpq(3, 4), fmpq(1), fmpq(2), fmpq(5), fmpq(15), fmpq(50)]
V_GRID = [fmpq(8, 5) + fmpq(i, 25) for i in range(11)]  # 1.6 .. 2.0 step 0.04


def rel_margin(H, pt) -> fmpq:
    biggest = fmpq(0)
    total = fmpq(0)
    for expo, coeff in H.d.items():
        term = coeff
        for slot, e in enumerate(expo):
            if e:
                term *= pt[slot] ** e
        total += term
        a = term if term >= 0 else -term
        if a > biggest:
            biggest = a
    return total / biggest if biggest != 0 else fmpq(0)


BOX_LO = (fmpq(3), fmpq(5, 12), fmpq(8, 5))
BOX_HI = (fmpq(4000), fmpq(50), fmpq(2))


def refine(H, pt: list, rounds: int = 6) -> tuple[list, fmpq]:
    """Coordinate descent on the margin around pt, exact arithmetic, clamped
    to the box. Purely a search for a bad point -- carries no proof weight."""
    best = rel_margin(H, pt)
    step = [(BOX_HI[s] - BOX_LO[s]) / 8 for s in range(3)]
    for _ in range(rounds):
        for s in range(3):
            for sgn in (1, -1):
                cand = list(pt)
                cand[s] = cand[s] + step[s] * sgn
                if cand[s] < BOX_LO[s] or cand[s] > BOX_HI[s]:
                    continue
                m = rel_margin(H, cand)
                if m < best:
                    best, pt = m, cand
        step = [w / 2 for w in step]
    return pt, best


def scan_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    out: dict = {"depth": d, "branches": {}}
    for parity in ("even", "odd"):
        H = build_branch(parity, d, e_polys)
        worst = None
        worst_pt = None
        for K in K_GRID:
            for c in C_GRID:
                for v in V_GRID:
                    m = rel_margin(H, (K, c, v))
                    if worst is None or m < worst:
                        worst, worst_pt = m, [K, c, v]
        worst_pt, worst = refine(H, worst_pt)
        sign_worst = (worst > 0) - (worst < 0)
        print(
            f"  d={d} [{parity}] worst margin {float(worst):.3e} (sign {sign_worst}) at "
            f"K={float(worst_pt[0]):.6g} c={float(worst_pt[1]):.6g} v={float(worst_pt[2]):.6g}"
            f"  ({time.time() - t0:.0f}s)",
            flush=True,
        )
        out["branches"][parity] = {
            "worst_margin": float(worst),
            "worst_margin_exact": str(worst),
            "sign_at_worst": sign_worst,
            "at": [str(x) for x in worst_pt],
            "grid": f"{len(K_GRID)}x{len(C_GRID)}x{len(V_GRID)} + 6 refine rounds",
        }
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [2, 3, 4, 5]
    out = []
    for d in depths:
        out.append(scan_depth(d))
        path = RES / "odd_depth_margin_scan.json"
        path.write_text(json.dumps({"runs": out, **stamp()}, indent=1), encoding="utf-8")
    print(f"written {RES / 'odd_depth_margin_scan.json'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
