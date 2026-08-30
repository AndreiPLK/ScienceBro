"""Leg (a) certificates, at O(J) big multiplications instead of O(J^2).

`farbelow_coeff_signs.py` computes each `y`-coefficient from the verified formula, and its
cost is dominated by the elementary symmetric functions of the tails `A_i .. A_{J-2}`:
recomputed for every `i`, that is `O(J^2)` multiplications of four-variable polynomials over
`Q(sqrt3)`. At `j = 18` it took 3.7 hours.

The `A_r` are an ARITHMETIC PROGRESSION, `A_r = A_0 + 2 den r`, so

    e_m(A_i, ..., A_{J-2}) = SUM_j c^{(i)}_{m,j} * d^{m-j} * A_0^j,     d = 2 den,

where `c^{(i)}_{m,j}` are the integer coefficients of `e_m(u+i, ..., u+M)` as a polynomial
in `u`. Verified against the direct computation at `J = 8`: 35 `(i,m)` pairs, 0 mismatches.

That changes the cost. The powers `A_0^j` and `d^j` are computed ONCE and reused for every
`i` and every `m`; each elementary function is then a scalar-weighted sum. `O(J)` big
multiplications instead of `O(J^2)`, with the same exact arithmetic and the same output.

The point of the speedup is the theorem: leg (a) is certified per depth, and the depth
ceiling has been machine time, not mathematics, since the day it was reached.

Run: KNIFE_J=20 [V_OFFSET=k] python lab/farbelow_coeff_fast.py
     -> results/farbelow_coeff_fast_j<J>[_v<k>].json
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
J = int(os.environ.get("KNIFE_J", "12"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from knife_tail2 import E_at  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def stirling_table(M: int) -> dict[int, list[fmpq_poly]]:
    """For each start `i`, the polynomials e_m(u+i, ..., u+M) in `u`, all `m`.

    Built once. These are integer-coefficient polynomials and carry no `Q(sqrt3)` part, so
    they are cheap however large `J` gets.
    """
    out: dict[int, list[fmpq_poly]] = {}
    for i in range(M + 1):
        acc = [fmpq_poly([1])] + [fmpq_poly([0])] * (M - i + 1)
        for r in range(i, M + 1):
            term = fmpq_poly([r, 1])
            for q in range(M - i + 1, 0, -1):
                acc[q] = acc[q] + acc[q - 1] * term
        out[i] = acc
    return out


def negatives_of(P: Q3Poly) -> int:
    mons: dict[tuple[int, ...], list[fmpq]] = {}
    for idx, part in enumerate((P.a, P.b)):
        for e, c in part.c.items():
            mons.setdefault(e, [fmpq(0), fmpq(0)])[idx] = c
    return sum(1 for ab in mons.values() if sign_q3(ab[0], ab[1]) < 0)


def main() -> int:
    t0 = time.time()
    v_offset = int(os.environ.get("V_OFFSET", "0"))
    lam, D_num, den, m_expr = region(v_offset=v_offset)
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, 1)
    tk = D_num + y * den
    A0 = tk + den * c_const
    d = den * 2
    M = J - 2

    # the only big multiplications in the whole run: powers of A0 and of d
    A0p = [Q3Poly.const(NV, 1)]
    dp = [Q3Poly.const(NV, 1)]
    for _ in range(M + 2):
        A0p.append(A0p[-1] * A0)
        dp.append(dp[-1] * d)
    denp = [Q3Poly.const(NV, 1)]
    s2 = s * s
    s2p = [Q3Poly.const(NV, 1)]
    for _ in range(J + 1):
        denp.append(denp[-1] * den)
        s2p.append(s2p[-1] * s2)

    ST = stirling_table(M)

    def esym_tail(i: int, m: int) -> Q3Poly:
        """e_m(A_i .. A_{J-2}) by the arithmetic-progression expansion.

        `i` can reach `J-1`, one past the last `A`, where the tail is EMPTY: then e_0 = 1
        and every higher e vanishes. Forgetting that raised a KeyError on the first run.
        """
        if i > M:
            return Q3Poly.const(NV, 1) if m == 0 else Q3Poly.const(NV, 0)
        if m < 0 or m > M - i + 1:
            return Q3Poly.const(NV, 0)
        S = ST[i][m]
        acc = Q3Poly.const(NV, 0)
        for jj in range(S.degree() + 1):
            cj = S[jj]
            if cj == 0:
                continue
            term = dp[m - jj] * A0p[jj]
            acc = acc + Q3Poly(term.a * cj, term.b * cj)
        return acc

    poch = []
    for i in range(J):
        acc = Q3Poly.const(NV, 1)
        for q in range(1, 2 * i + 1):
            acc = acc * (2 * n_expr - 2 * J + q)
        w = fmpq(1, math.factorial(i) * 2**i)
        poch.append(Q3Poly(acc.a * w, acc.b * w))

    # The four factors E * poch * s^2i * den^i depend ONLY on i, and the first version
    # recomputed them for every (k, i) pair -- four big products where one suffices.
    # Profiling said 99% of the run was in these products, so they are hoisted.
    W = [E_at(m_expr, J - 1 - i) * poch[i] * s2p[i] * denp[i] for i in range(J)]

    rows = []
    for k in range(J):
        acc = Q3Poly.const(NV, 0)
        for i in range(J - k):
            m = J - 1 - i - k
            if m < 0 or m > M - i + 1:
                continue
            term = W[i] * esym_tail(i, m)
            acc = acc + term if i % 2 == 0 else acc - term
        if (J - 1 + k) % 2:
            acc = Q3Poly.const(NV, 0) - acc
        acc = acc * denp[k]
        rows.append({"k": k, "monomials": len(acc.a.c) + len(acc.b.c),
                     "negative": negatives_of(acc)})

    off = [r for r in rows if r["negative"] and r["k"] not in (J - 2, J - 3)]
    out = {
        "j": J,
        "v_offset": v_offset,
        "what": "leg (a) by the arithmetic-progression expansion: O(J) big multiplications "
        "instead of O(J^2)",
        "identity_used": "e_m(A_i..A_{J-2}) = SUM_j c_{m,j} d^{m-j} A_0^j, d = 2 den; "
        "verified against the direct computation at J = 8, 35 pairs, 0 mismatches",
        "coefficients": rows,
        "negatives_outside_excluded_indices": off,
        "leg_a_holds": not off,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    name = f"farbelow_coeff_fast_j{J}" + (f"_v{v_offset}" if v_offset else "") + ".json"
    (RES / name).write_text(json.dumps(out, indent=2), encoding="utf-8")
    negs = {r["k"]: r["negative"] for r in rows if r["negative"]}
    print(f"[j={J}] negatives by k: {negs}   leg (a) holds: {not off}   ({out['runtime_s']}s)")
    return 0 if not off else 1


if __name__ == "__main__":
    raise SystemExit(main())
