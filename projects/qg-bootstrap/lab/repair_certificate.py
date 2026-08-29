"""Turning the neighbour repair from a measurement into a certificate.

THE STATEMENT.  With the three relevant y-coefficients of the far-below
polynomial sharing den^{J-1} (see results/FARBELOW_NEGATIVE_PATTERN.md),

    c_{J-1} = den^{J-1} w,
    c_{J-2} = den^{J-1} (u - w e1),
    c_{J-3} = den^{J-1} (w e2 - u e1p + poch_2 s^4 E_{J-3}),

    w = E_{J-1},  u = poch_1 s^2 E_{J-2},  alpha_r = A_r/den,
    e1 = e_1(alpha_0..alpha_{J-2}),  e1p = e_1(alpha_1..),  e2 = e_2(alpha_0..),

the repair that absorbs the one negative coefficient into its neighbours is

    (R)   4 c_{J-1} c_{J-3} - c_{J-2}^2  >=  0.

Measured at 504 region points (117 of them with the coefficient actually dipping)
without a single failure -- and, importantly, it holds even where nothing dips, so
(R) is UNCONDITIONAL and needs no case split.

WHAT THIS FILE DOES.  Builds (R) exactly, as a polynomial over Q(sqrt3) in the
region variables (thL, v, K3), all of which are >= 0 on the far-below region.  If
every monomial of that polynomial is nonnegative, positivity on the whole region
follows immediately -- manifest positivity, the same certificate shape the
far-below criterion itself uses for j <= 8, and a proof rather than a sample.

Multiplied through by den^2 to clear the alphas:

    (R') 4 w [ w e2(A) - u den e1p(A) + poch_2 s^4 E_{J-3} den^2 ]
             - [ u den - w e1(A) ]^2   >=  0.

Run: KNIFE_J=9 python lab/repair_certificate.py -> results/repair_certificate_j<J>.json
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
J = int(os.environ.get("KNIFE_J", "9"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from knife_tail2 import E_at  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NAMES = ("thL", "y", "v", "K3")


def e_sym(items: list, t: int) -> Q3Poly:
    acc = [Q3Poly.const(NV, 1)] + [Q3Poly.const(NV, 0)] * t
    for it in items:
        for q in range(min(t, len(acc) - 1), 0, -1):
            acc[q] = acc[q] + acc[q - 1] * it
    return acc[t]


def build_R(v_offset: int = 0) -> tuple[Q3Poly, dict]:
    lam, D_num, den, m_expr = region(v_offset)
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, 1)
    tk_num = D_num + y * den  # undo D_num = tk_num - y den
    A = [tk_num + den * (c_const + 2 * r) for r in range(J - 1)]

    poch1 = (2 * n_expr - 2 * J + 1) * (2 * n_expr - 2 * J + 2)
    poch1 = Q3Poly(poch1.a * fmpq(1, 2), poch1.b * fmpq(1, 2))
    poch2 = Q3Poly.const(NV, 1)
    for q in range(1, 5):
        poch2 = poch2 * (2 * n_expr - 2 * J + q)
    poch2 = Q3Poly(
        poch2.a * fmpq(1, math.factorial(2) * 4), poch2.b * fmpq(1, math.factorial(2) * 4)
    )

    w = E_at(m_expr, J - 1)
    u = poch1 * s * s * E_at(m_expr, J - 2)
    e1 = e_sym(A, 1)
    e1p = e_sym(A[1:], 1)
    e2 = e_sym(A, 2)
    s4 = s * s * s * s

    inner = w * e2 - u * den * e1p + poch2 * s4 * E_at(m_expr, J - 3) * den * den
    outer = u * den - w * e1
    R = (w * inner) * 4 - outer * outer
    info = {"terms_w": len(w.a.c), "terms_u": len(u.a.c), "terms_inner": len(inner.a.c)}
    return R, info


def main() -> int:
    t0 = time.time()
    v_offset = int(os.environ.get("V_OFFSET", "0"))
    R, info = build_R(v_offset)
    mons = {}
    for part, store in ((R.a, "a"), (R.b, "b")):
        for e, cval in part.c.items():
            mons.setdefault(e, {"a": fmpq(0), "b": fmpq(0)})[store] = cval
    neg = []
    for e, ab in mons.items():
        if sign_q3(ab["a"], ab["b"]) < 0:
            neg.append(
                {"exponents": {NAMES[i]: int(e[i]) for i in range(NV)}, "total_degree": int(sum(e))}
            )
    neg.sort(key=lambda d: d["total_degree"])
    out = {
        "j": J,
        "v_offset": v_offset,
        "statement": "(R) 4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0 on the far-below region, "
        "cleared by den^2; every region variable is >= 0, so all-nonnegative monomials "
        "PROVE it there",
        "monomials": len(mons),
        "negative_monomials": len(neg),
        "manifestly_positive": len(neg) == 0,
        "sample_negatives": neg[:20],
        "sizes": info,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (
        RES
        / (
            f"repair_certificate_j{J}.json"
            if not v_offset
            else f"repair_certificate_j{J}_v{v_offset}.json"
        )
    ).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[j={J}, v>={v_offset}] (R): {len(mons)} monomials, {len(neg)} negative -> "
        f"{'MANIFESTLY POSITIVE (certificate)' if not neg else 'not manifest; needs Bernstein'}"
    )
    for d in neg[:8]:
        print(f"   {d['exponents']}  deg={d['total_degree']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
