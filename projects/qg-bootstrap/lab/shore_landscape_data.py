"""Export the shore landscape as data for visualisation (outreach artifact).

This is NOT a new result. It renders objects that are already established in
this project, so that the picture shows the real thing rather than a drawing:

  1. THE MOUNTAIN RANGE.  T_k(lam) = 3(2k-3)/(k(k-2)) * (lam^2 + (2k-2)lam + 1)
     + 2k, evaluated on a continuous (k, lam) grid.  Each integer k is one
     spin level; the surface is the union of their constraints.

  2. THE SHORE.  T_hat(lam) = min over integers k >= 3 of T_k(lam) -- the
     valley floor of that range, and the largest spacetime dimension D the
     CHR graviton family can have at coupling lam.  The winning k jumps by one
     at discrete points; those jumps are recorded so the picture can show them.

  3. THE SEA (the physical statement).  For a fixed depth the exact reference
     engine (lab/jacobi_normal_form.py, the same one the certificates use)
     gives sign(knife_j) on a (lam, D) grid.  Positive = the theory survives,
     negative = it is excluded.  The measured sign field is exported as is,
     including any point that disagrees with the shore -- nothing is smoothed
     and nothing is dropped.

Exact arithmetic throughout (flint fmpq); floats appear only in the exported
JSON, which is a picture, not evidence.

Run: python lab/shore_landscape_data.py -> results/shore_landscape_data.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import T_k, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

K_LO, K_HI, K_STEPS = fmpq(5, 2), fmpq(26), 72
LAM_LO, LAM_HI, LAM_STEPS = fmpq(1, 5), fmpq(12), 72
CEIL = fmpq(140)  # display clamp: the range is unbounded near k -> 2


def grid(lo: fmpq, hi: fmpq, steps: int) -> list[fmpq]:
    return [lo + (hi - lo) * fmpq(i, steps) for i in range(steps + 1)]


def mountain_surface() -> dict:
    ks = grid(K_LO, K_HI, K_STEPS)
    lams = grid(LAM_LO, LAM_HI, LAM_STEPS)
    z = []
    for lam in lams:
        row = []
        for k in ks:
            T = T_k(k, lam)
            row.append(float(T if T < CEIL else CEIL))
        z.append(row)
    return {
        "k": [float(k) for k in ks],
        "lam": [float(x) for x in lams],
        "T": z,
        "clamp": float(CEIL),
    }


def shore_curve() -> dict:
    lams = grid(LAM_LO, LAM_HI, 240)
    pts, jumps = [], []
    prev_k = None
    for lam in lams:
        T, k = shore(lam)
        pts.append({"lam": float(lam), "T": float(T), "k": k})
        if prev_k is not None and k != prev_k:
            jumps.append({"lam": float(lam), "T": float(T), "from_k": prev_k, "to_k": k})
        prev_k = k
    return {"points": pts, "level_jumps": jumps}


def sign_field(n: int, j: int) -> dict:
    """Exact knife sign on a (lam, D) grid, with the shore for reference."""
    lams = grid(fmpq(1, 2), fmpq(12), 40)
    rows = []
    disagreements = 0
    for lam in lams:
        Th = shore(lam)[0]
        Ds = grid(fmpq(4), CEIL, 40)
        col = []
        for D in Ds:
            s = ref_sign(j, n, lam, D)
            col.append(s)
            if D <= Th and s < 0:
                disagreements += 1
        rows.append({"lam": float(lam), "D": [float(x) for x in Ds], "sign": col})
    return {"n": n, "j": j, "rows": rows, "negative_below_shore": disagreements}


def main() -> int:
    t0 = time.time()
    mountains = mountain_surface()
    curve = shore_curve()
    fields = [sign_field(12, 4), sign_field(12, 5)]
    bad = sum(f["negative_below_shore"] for f in fields)
    print(f"mountain grid: {len(mountains['lam'])} x {len(mountains['k'])}", flush=True)
    print(f"shore curve: {len(curve['points'])} points, "
          f"{len(curve['level_jumps'])} level jumps", flush=True)
    for f in fields:
        neg = sum(1 for r in f["rows"] for s in r["sign"] if s < 0)
        tot = sum(len(r["sign"]) for r in f["rows"])
        print(f"sign field n={f['n']} j={f['j']}: {neg}/{tot} negative, "
              f"{f['negative_below_shore']} of them below the shore", flush=True)
    print(f"knife negative below the shore anywhere: {bad}", flush=True)

    out = {
        "claim": (
            "Visualisation data only -- no new scientific content. Exports three "
            "already-established objects on a display grid: the level surface "
            "T_k(lam), the shore T_hat(lam) = min_k T_k(lam) with its integer-level "
            "jumps, and the exact knife sign field on a (lam, D) grid from the same "
            "reference engine the certificates use. The sign field is exported "
            "unsmoothed; the count of points where the knife is negative BELOW the "
            "shore is reported as a self-check and is "
            f"{bad} in this run."
        ),
        "mountains": mountains,
        "shore": curve,
        "sign_fields": fields,
        "negative_below_shore_total": bad,
        "command": "python lab/shore_landscape_data.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "shore_landscape_data.json"
    path.write_text(json.dumps(out), encoding="utf-8")
    print(f"written {path} ({path.stat().st_size // 1024} KB)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
