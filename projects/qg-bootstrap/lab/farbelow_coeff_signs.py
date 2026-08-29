"""Leg (a) without assembling the whole polynomial: coefficient signs, straight from the formula.

`farbelow_negative_pattern.py` answers "which y-coefficients have a negative
monomial" by building all of N and splitting it -- 77 minutes at j = 16, and worse
above.  But the verified general formula gives each coefficient on its own:

    c_k = (-1)^{J-1+k} den^k SUM_{i<=J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i} den^i
                                            e_{J-1-i-k}(A_i..A_{J-2}),

so leg (a) -- every c_k with k != J-2 nonnegative monomial by monomial -- can be
checked coefficient by coefficient, reusing the elementary symmetric functions of
the A's across k.  Same statement, far less work, and it lets the proved depths
go further.

The formula itself is not taken on trust: it was verified against the assembled
polynomial at every k for j = 6 and j = 9 (0 mismatches), and this file re-checks
its own output against `farbelow_negative_pattern`'s artefact wherever one exists.

V_OFFSET shifts v so the run sits inside the regime n >= 2J-3, exactly as the repair
certificate does; without it the criterion is being asked to hold where it is known
not to, and a negative there says nothing.

Run: KNIFE_J=18 [V_OFFSET=k] python lab/farbelow_coeff_signs.py
     -> results/farbelow_coeff_signs_j<J>[_v<k>].json
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
J = int(os.environ.get("KNIFE_J", "12"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from knife_tail2 import E_at  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NAMES = ("thL", "y", "v", "K3")


def negatives_of(P: Q3Poly) -> list[tuple[int, ...]]:
    mons: dict[tuple[int, ...], list[fmpq]] = {}
    for idx, part in enumerate((P.a, P.b)):
        for e, c in part.c.items():
            mons.setdefault(e, [fmpq(0), fmpq(0)])[idx] = c
    return [e for e, ab in mons.items() if sign_q3(ab[0], ab[1]) < 0]


def main() -> int:
    t0 = time.time()
    v_offset = int(os.environ.get("V_OFFSET", "0"))
    lam, D_num, den, m_expr = region(v_offset=v_offset)
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, 1)
    tk_num = D_num + y * den
    A = [tk_num + den * (c_const + 2 * r) for r in range(J - 1)]

    # elementary symmetric functions of A_i.. A_{J-2}, for every i, computed once
    esym: dict[int, list[Q3Poly]] = {}
    for i in range(J):
        items = A[i:]
        acc = [Q3Poly.const(NV, 1)] + [Q3Poly.const(NV, 0)] * len(items)
        for it in items:
            for q in range(len(items), 0, -1):
                acc[q] = acc[q] + acc[q - 1] * it
        esym[i] = acc

    s2 = s * s
    s2p = {0: Q3Poly.const(NV, 1)}
    denp = {0: Q3Poly.const(NV, 1)}
    for i in range(1, J):
        s2p[i] = s2p[i - 1] * s2
        denp[i] = denp[i - 1] * den
    poch = {}
    for i in range(J):
        acc = Q3Poly.const(NV, 1)
        for q in range(1, 2 * i + 1):
            acc = acc * (2 * n_expr - 2 * J + q)
        w = fmpq(1, math.factorial(i) * 2**i)
        poch[i] = Q3Poly(acc.a * w, acc.b * w)

    rows = []
    for k in range(J):
        acc = Q3Poly.const(NV, 0)
        for i in range(J - k):
            m = J - 1 - i - k
            if m >= len(esym[i]):
                continue
            term = E_at(m_expr, J - 1 - i) * poch[i] * s2p[i] * denp[i] * esym[i][m]
            acc = acc + term if i % 2 == 0 else acc - term
        if (J - 1 + k) % 2:
            acc = Q3Poly.const(NV, 0) - acc
        acc = acc * denp[k] if k < J else acc
        neg = negatives_of(acc)
        rows.append({"k": k, "monomials": len(acc.a.c) + len(acc.b.c), "negative": len(neg)})

    off = [r for r in rows if r["negative"] and r["k"] != J - 2]
    out = {
        "j": J,
        "what": "leg (a): sign of every y-coefficient, from the verified formula rather than "
        "from assembling the whole polynomial",
        "coefficients": rows,
        "negatives_outside_k_eq_J_minus_2": off,
        "leg_a_holds": not off,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    out["v_offset"] = v_offset
    name = f"farbelow_coeff_signs_j{J}" + (f"_v{v_offset}" if v_offset else "") + ".json"
    (RES / name).write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    negs = {r["k"]: r["negative"] for r in rows if r["negative"]}
    print(f"[j={J}] negatives by k: {negs}   leg (a) holds: {not off}   ({out['runtime_s']}s)")
    return 0 if not off else 1


if __name__ == "__main__":
    raise SystemExit(main())
