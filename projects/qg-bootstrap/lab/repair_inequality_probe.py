"""The neighbour repair, reduced to one explicit inequality, and measured.

WHERE THIS COMES FROM.  results/FARBELOW_NEGATIVE_PATTERN.md gives the verified
general y-coefficient.  Writing alpha_r = A_r/den = T_cap + c + 2r and

    w = E_{J-1},   u = poch_1 s^2 E_{J-2},
    e1  = e_1(alpha_0..alpha_{J-2}),   e1p = e_1(alpha_1..alpha_{J-2}),
    e2  = e_2(alpha_0..alpha_{J-2}),

the three coefficients that matter share the same power of den:

    c_{J-1} = den^{J-1} w,
    c_{J-2} = den^{J-1} (u - w e1),
    c_{J-3} = den^{J-1} (w e2 - u e1p + poch_2 s^4 E_{J-3}).

So the repair c_{J-2}^2 <= 4 c_{J-1} c_{J-3} is a QUADRATIC in u opening upward:

    u^2 - 2 u w (alpha_0 - e1p) + w^2 (e1^2 - 4 e2) - 4 w poch_2 s^4 E_{J-3} <= 0.

Evaluated at the boundary u = w e1 -- exactly where c_{J-2} changes sign -- it
collapses, using e1 - alpha_0 = e1p, to

    (BOUNDARY)   E_{J-1} [ e1p^2 - e_2(alpha_1..alpha_{J-2}) ]  <=  poch_2 s^4 E_{J-3},

whose left side is a Newton-positive quantity of the alphas.  That is one
explicit inequality in (n, J, s, T_cap) with no free variables left, and it is
the natural target for a proof uniform in depth.

THIS FILE MEASURES IT.  Numbers only (certified `arb`), so it is light.  It
reports (BOUNDARY) and the full quadratic at the actual u, over the far-below
region and over a wider (n, J, lam) grid, and it reports where each fails --
a failure being far more informative than another confirmation.

Run: python lab/repair_inequality_probe.py -> results/repair_inequality_probe.json
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from flint import arb, ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dominant_term_probe import region_point  # noqa: E402
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
ctx.prec = 300


def pieces(J: int, v: int, k3: int, thl: int):
    n, s, den, A = region_point(v, k3, thl, J)
    E = E2_list(n, J)
    alpha = [a / den for a in A]  # alpha_r = T_cap + c + 2r
    e1 = sum(alpha, arb(0))
    e1p = sum(alpha[1:], arb(0))
    e2 = arb(0)
    for i in range(len(alpha)):
        for jj in range(i + 1, len(alpha)):
            e2 += alpha[i] * alpha[jj]
    e2p = arb(0)
    for i in range(1, len(alpha)):
        for jj in range(i + 1, len(alpha)):
            e2p += alpha[i] * alpha[jj]
    poch1 = arb(2 * n - 2 * J + 1) * arb(2 * n - 2 * J + 2) / 2
    poch2 = arb(1)
    for q in range(1, 5):
        poch2 *= arb(2 * n - 2 * J + q)
    poch2 /= arb(math.factorial(2) * 4)
    w = arb(E[J - 1])
    u = poch1 * s * s * arb(E[J - 2])
    return {
        "n": n,
        "s": s,
        "w": w,
        "u": u,
        "e1": e1,
        "e1p": e1p,
        "e2": e2,
        "e2p": e2p,
        "alpha0": alpha[0],
        "poch2_s4_EJm3": poch2 * s**4 * arb(E[J - 3]),
    }


def main() -> int:
    t0 = time.time()
    rows, bnd_fail, quad_fail, undecided, dips = [], 0, 0, 0, 0
    for J in (5, 9, 12, 16, 20, 30, 40):
        for v in (0, 1, 5, 40, 400):
            for k3 in (0, 3, 60):
                for thl in (0, 2, 50):
                    P = pieces(J, v, k3, thl)
                    lhs_b = P["w"] * (P["e1p"] * P["e1p"] - P["e2p"])
                    rhs_b = P["poch2_s4_EJm3"]
                    d_b = rhs_b - lhs_b
                    u, w = P["u"], P["w"]
                    quad = (
                        u * u
                        - 2 * u * w * (P["alpha0"] - P["e1p"])
                        + w * w * (P["e1"] * P["e1"] - 4 * P["e2"])
                        - 4 * w * P["poch2_s4_EJm3"]
                    )
                    dip = u - w * P["e1"] < 0
                    dips += bool(dip)
                    if not (d_b > 0 or d_b < 0) or not (quad > 0 or quad < 0):
                        undecided += 1
                        continue
                    okb = d_b > 0
                    okq = quad < 0
                    bnd_fail += not okb
                    quad_fail += dip and not okq
                    if not okb or (dip and not okq):
                        rows.append(
                            {
                                "J": J,
                                "v": v,
                                "K3": k3,
                                "thL": thl,
                                "c_Jm2_dips": bool(dip),
                                "boundary_ok": bool(okb),
                                "quadratic_ok": bool(okq),
                                "boundary_ratio": float(lhs_b / rhs_b),
                            }
                        )
    out = {
        "what": "(BOUNDARY) E_{J-1}[e1p^2 - e2(alpha_1..)] <= poch_2 s^4 E_{J-3}, and the full "
        "quadratic form of the neighbour repair, over the far-below region",
        "points": 7 * 5 * 3 * 3,
        "points_where_c_Jm2_dips": dips,
        "boundary_failures": bnd_fail,
        "quadratic_failures_where_it_dips": quad_fail,
        "undecided_enclosures": undecided,
        "failing_rows": rows[:60],
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "repair_inequality_probe.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"points {out['points']}, dips {dips}, boundary failures {bnd_fail}, "
        f"quadratic failures where it dips {quad_fail}, undecided {undecided}"
    )
    for r in rows[:10]:
        print(
            f"   J={r['J']:3d} v={r['v']:4d} K3={r['K3']:3d} thL={r['thL']:3d} "
            f"dip={r['c_Jm2_dips']} boundary_ok={r['boundary_ok']} ratio={r['boundary_ratio']:.4f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def all_coefficients_signs(J: int, v: int, k3: int, thl: int) -> dict:
    """Sign of EVERY y-coefficient at one region point, from the verified formula.

    The claim the whole picture rests on is "only c_{J-2} ever dips".  Full
    polynomial expansion can test it to j = 12 at best; evaluating the verified
    closed form as numbers tests it wherever we like.  A dip at some k != J-2
    would refute the picture, so this is the check that can actually fail.
    """
    n, s, den, A = region_point(v, k3, thl, J)
    E = E2_list(n, J)
    alpha = [a / den for a in A]

    def e_sym_alpha(items, t):
        acc = [arb(1)] + [arb(0)] * t
        for it in items:
            for q in range(min(t, len(acc) - 1), 0, -1):
                acc[q] = acc[q] + acc[q - 1] * it
        return acc[t]

    negatives = []
    for k in range(J):
        tot = arb(0)
        for i in range(J - k):
            poch = arb(1)
            for q in range(1, 2 * i + 1):
                poch *= arb(2 * n - 2 * J + q)
            poch /= arb(math.factorial(i) * 2**i)
            term = arb(E[J - 1 - i]) * poch * s ** (2 * i) * e_sym_alpha(alpha[i:], J - 1 - i - k)
            tot = tot + term if i % 2 == 0 else tot - term
        if (J - 1 + k) % 2:
            tot = -tot
        if tot < 0:
            negatives.append(k)
        elif not (tot > 0):
            negatives.append(f"undecided_{k}")
    return {"J": J, "v": v, "K3": k3, "thL": thl, "negative_k": negatives}
