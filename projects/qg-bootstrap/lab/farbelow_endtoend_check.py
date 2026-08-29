"""End-to-end check of the far-below conclusion, not of its ingredients.

The proof closed today has two legs (every y-coefficient nonnegative except the one
at degree J-2, and the certified repair (R)) plus a grouping argument that puts
them together.  Each leg is checked in its own artefact, and the grouping is
algebra -- which means nothing so far has tested the CONCLUSION against the object.

This file does that: it assembles N(y) for a depth, evaluates it EXACTLY at points
of the far-below region crossed with a spread of y >= 0, and checks the sign.  A
negative value would mean the grouping argument is wrong even though its pieces
check out, which is exactly the failure mode a separated check cannot see.

Run: KNIFE_J=11 python lab/farbelow_endtoend_check.py
     -> results/farbelow_endtoend_j<J>.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
J = int(os.environ.get("KNIFE_J", "11"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from knife_tail2 import build_P  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def evaluate(P, point: tuple[fmpq, ...]) -> tuple[fmpq, fmpq]:
    """Exact value of a Q3Poly at a rational point, as (a, b) with a + b sqrt3."""
    out = [fmpq(0), fmpq(0)]
    for idx, part in enumerate((P.a, P.b)):
        acc = fmpq(0)
        for e, c in part.c.items():
            term = c
            for i in range(NV):
                if e[i]:
                    term *= point[i] ** e[i]
            acc += term
        out[idx] = acc
    return out[0], out[1]


def main() -> int:
    t0 = time.time()
    lam, D_num, den, m_expr = region()
    N = build_P(lam, D_num, den, m_expr)
    thls = (fmpq(0), fmpq(1, 2), fmpq(1))
    vs = (fmpq(0), fmpq(3), fmpq(40), fmpq(400))
    k3s = (fmpq(0), fmpq(5), fmpq(60))
    ys = (fmpq(0), fmpq(1, 10), fmpq(1), fmpq(10), fmpq(100), fmpq(1000), fmpq(10) ** 5)
    bad, tot = [], 0
    for thl in thls:
        for v in vs:
            for k3 in k3s:
                for y in ys:
                    a, b = evaluate(N, (thl, y, v, k3))
                    tot += 1
                    if sign_q3(a, b) <= 0:
                        bad.append({"thL": str(thl), "y": str(y), "v": str(v), "K3": str(k3)})
    out = {
        "j": J,
        "what": "N(y) evaluated exactly on the far-below region; the conclusion of the "
        "two-leg proof, tested against the object rather than against its pieces",
        "points": tot,
        "non_positive": len(bad),
        "failures": bad[:20],
        "grid": {
            "thL": [str(x) for x in thls],
            "v": [str(x) for x in vs],
            "K3": [str(x) for x in k3s],
            "y": [str(x) for x in ys],
        },
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / f"farbelow_endtoend_j{J}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[j={J}] end-to-end: {tot} points, {len(bad)} non-positive")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
