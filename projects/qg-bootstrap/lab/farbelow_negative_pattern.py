"""The eleven exceptions: which monomials go negative when the far-below criterion breaks.

THE FACT THIS FILE CHASES.  The y-expansion criterion of `knife_farbelow2.py`
proves knife positivity in the far-below region by MANIFEST positivity: expand
N = (-1)^{J-1} B_j at D = T_cap - y, and check that every monomial of every
y-coefficient is nonnegative.  It works for j = 4..8 and breaks at j = 9.  But
look at how it breaks (`results/knife*_farbelow_factored.json`):

    j        9      10      11      12
    negative monomials   11      30      41      71
    total monomials  54331   84170  124881  178816

Two parts in ten thousand.  A criterion that fails on 0.02% of its terms is not a
wall, it is a list of exceptions -- and if that list has a shape in j, the
far-below region closes for EVERY depth at once, which is the uniformity the
programme is missing.

WHAT THIS FILE DOES.  Rebuilds N on the fast engine (Q3Poly over Q(sqrt3), via
`knife_tail2.build_P`, no new derivation), and for each j prints the actual
exponent tuples of the negative monomials, their y-degree, and their coefficient
sizes -- the data the existing artefacts summarise to a count.  Nothing is
concluded here; the point is to see the exceptions.

Region (identical to knife_farbelow2, deliberately): m = 41 + v, K = v + K3 + 6,
lam = (K + 51 + thL) sqrt3/3, D = T_cap - y, all of v, K3, thL, y >= 0.

Run: KNIFE_J=9 python lab/farbelow_negative_pattern.py
     -> results/farbelow_negative_pattern_j<J>.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
J = int(os.environ.get("KNIFE_J", "9"))
os.environ["KNIFE_J"] = str(J)
from knife_tail2 import build_P  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NV = 4
THL, Y, V, K3 = 0, 1, 2, 3
NAMES = ("thL", "y", "v", "K3")


def region(v_offset: int = 0):
    """The far-below parametrisation, as Q3Poly objects.

    v_offset shifts the origin of v, i.e. starts the region at n = 44 + v_offset
    instead of n = 44.  Used to test statements that only hold inside the regime
    n >= 2J-3, where the region's own corner lies outside it.
    """
    thl, y, vv, k3 = (Q3Poly.var(NV, i) for i in range(NV))
    vv = vv + v_offset
    lam = (vv + k3 + 51 + thl) * Q3Poly.const(NV, 0, fmpq(1, 3))  # (K+51+thL) sqrt3/3
    kk = vv + k3 + 53
    m_expr = vv + 41
    lam2 = lam * lam
    tk_num = (3 * (2 * kk - 3)) * (lam2 + (2 * kk - 2) * lam + 1) + (2 * kk) * kk * (kk - 2)
    den = kk * (kk - 2)
    return lam, tk_num - y * den, den, m_expr


def main() -> int:
    t0 = time.time()
    lam, D_num, den, m_expr = region()
    print(f"[j={J}] building N ...", flush=True)
    N = build_P(lam, D_num, den, m_expr)
    mons = {}
    for part, store in ((N.a, "a"), (N.b, "b")):
        for e, cval in part.c.items():
            mons.setdefault(e, {"a": fmpq(0), "b": fmpq(0)})[store] = cval
    neg = []
    for e, ab in mons.items():
        if sign_q3(ab["a"], ab["b"]) < 0:
            neg.append(
                {
                    "exponents": {NAMES[i]: int(e[i]) for i in range(NV)},
                    "y_degree": int(e[Y]),
                    "total_degree": int(sum(e)),
                    "a": str(ab["a"]),
                    "b": str(ab["b"]),
                }
            )
    neg.sort(key=lambda d: (d["y_degree"], d["total_degree"]))
    out = {
        "j": J,
        "region": "far-below: m = 41+v, K = v+K3+6, lam = (K+51+thL)sqrt3/3, D = T_cap - y",
        "total_monomials": len(mons),
        "negative_monomials": len(neg),
        "negatives": neg,
        "by_y_degree": {},
        "c_Jm2_closed_form_check": c_Jm2_closed_form(N),
        "newton_on_y_coefficients": newton_on_y_coefficients(N),
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    for d in neg:
        out["by_y_degree"].setdefault(str(d["y_degree"]), 0)
        out["by_y_degree"][str(d["y_degree"])] += 1
    (RES / f"farbelow_negative_pattern_j{J}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(f"[j={J}] monomials {len(mons)}, negative {len(neg)}, by y-degree {out['by_y_degree']}")
    for d in neg[:20]:
        print(f"   {d['exponents']}   deg={d['total_degree']}")
    return 0


def c_Jm2_closed_form(N=None) -> dict:
    """Why c_{J-2} is the exceptional coefficient: it is the first DIFFERENCE.

    With tail_i = PROD_{r=i}^{J-2} (A_r - y*den), A_r = tk_num + (c+2r) den, the
    y-expansion of N = (-1)^{J-1} B has

        [y^k] N = (-1)^{J-1+k} den^k SUM_{i<=J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                     den^i e_{J-1-i-k}(A),

    so the top coefficient k = J-1 has ONE term (manifestly positive), and
    k = J-2 has exactly TWO, of opposite sign:

        c_{J-2} = den^{J-2} [ poch_1 s^2 den E_{J-2} - E_{J-1} SUM_{r=0}^{J-2} A_r ],
        SUM_r A_r = (J-1) (tk_num + den (c + J - 2)),
        poch_1 = (2n-2J+1)(2n-2J+2)/2.

    Every other coefficient is a longer alternating sum whose expansion happens to
    come out with nonnegative monomials.  This function CHECKS the formula against
    the assembled polynomial rather than asserting it.
    """
    import math

    from knife_tail2 import E_at

    lam, D_num, den, m_expr = region()
    if N is None:
        N = build_P(lam, D_num, den, m_expr)
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    tk_num = D_num + Q3Poly.var(NV, Y) * den  # undo D_num = tk_num - y*den
    poch1 = (2 * n_expr - 2 * J + 1) * (2 * n_expr - 2 * J + 2)
    poch1 = Q3Poly(poch1.a * fmpq(1, 2), poch1.b * fmpq(1, 2))
    sum_A = (tk_num + den * (c_const + (J - 2))) * (J - 1)
    denp = Q3Poly.const(NV, 1)
    for _ in range(J - 2):
        denp = denp * den
    predicted = denp * (poch1 * s * s * den * E_at(m_expr, J - 2) - E_at(m_expr, J - 1) * sum_A)

    got = {}
    for part, store in ((N.a, "a"), (N.b, "b")):
        for e, cval in part.c.items():
            if e[Y] == J - 2:
                key = (e[THL], e[V], e[K3])
                got.setdefault(key, {"a": fmpq(0), "b": fmpq(0)})[store] = cval
    pred = {}
    for part, store in ((predicted.a, "a"), (predicted.b, "b")):
        for e, cval in part.c.items():
            if e[Y] != 0:
                continue
            key = (e[THL], e[V], e[K3])
            pred.setdefault(key, {"a": fmpq(0), "b": fmpq(0)})[store] = cval
    keys = set(got) | set(pred)
    bad = [
        k
        for k in keys
        if got.get(k, {"a": fmpq(0), "b": fmpq(0)})["a"]
        != pred.get(k, {"a": fmpq(0), "b": fmpq(0)})["a"]
        or got.get(k, {"a": fmpq(0), "b": fmpq(0)})["b"]
        != pred.get(k, {"a": fmpq(0), "b": fmpq(0)})["b"]
    ]
    _ = math
    return {
        "j": J,
        "monomials_in_c_Jm2": len(got),
        "monomials_in_formula": len(pred),
        "mismatches": len(bad),
        "sample_mismatch": sorted(bad)[:3],
    }


def _eval_q3(part_dicts, point):
    """Evaluate the (a, b) coefficient dicts of one y-coefficient at a point.

    point maps (thL, v, K3) exponents to values; returns (a, b) with the value
    a + b sqrt(3), exactly in fmpq.
    """
    out = [fmpq(0), fmpq(0)]
    for idx, d in enumerate(part_dicts):
        for (e_thl, e_v, e_k3), cval in d.items():
            out[idx] += cval * point[0] ** e_thl * point[1] ** e_v * point[2] ** e_k3
    return out[0], out[1]


def _q3_mul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def newton_on_y_coefficients(N=None) -> dict:
    """Test c_{J-2}^2 <= c_{J-1} c_{J-3} -- the repair the structure suggests.

    N(y) = SUM_k c_k y^k has every c_k manifestly nonnegative except c_{J-2}
    (results above).  A single negative coefficient in an otherwise nonnegative
    series is harmless exactly when its neighbours dominate it: pairing to the
    left covers y <= c_{J-3}/|c_{J-2}| and to the right y >= |c_{J-2}|/c_{J-1},
    and the two ranges meet iff

        c_{J-2}^2 <= c_{J-1} c_{J-3},

    a discrete Newton (log-concavity) inequality on the coefficient sequence.
    This function evaluates the three coefficients at points of the region and
    reports where it holds.  It is a MEASUREMENT: the inequality is checked, not
    derived.
    """
    lam, D_num, den, m_expr = region()
    if N is None:
        N = build_P(lam, D_num, den, m_expr)
    coeffs = {}
    for part, idx in ((N.a, 0), (N.b, 1)):
        for e, cval in part.c.items():
            slot = coeffs.setdefault(int(e[Y]), [{}, {}])
            slot[idx][(int(e[THL]), int(e[V]), int(e[K3]))] = cval
    grid = (0, 1, 2, 3, 6, 12, 40, 200)
    rows, fails = [], 0
    for thl in grid:
        for v in grid:
            for k3 in grid:
                pt = (fmpq(thl), fmpq(v), fmpq(k3))
                c1 = _eval_q3(coeffs[J - 1], pt)
                c2 = _eval_q3(coeffs[J - 2], pt)
                c3 = _eval_q3(coeffs[J - 3], pt)
                lhs = _q3_mul(c2, c2)
                rhs = _q3_mul(c1, c3)
                strict = sign_q3(rhs[0] - lhs[0], rhs[1] - lhs[1]) >= 0
                disc = sign_q3(4 * rhs[0] - lhs[0], 4 * rhs[1] - lhs[1]) >= 0
                neg = sign_q3(*c2) < 0
                fails += neg and not disc
                if neg or not strict:
                    rows.append(
                        {
                            "thL": thl,
                            "v": v,
                            "K3": k3,
                            "c_Jm2_negative": neg,
                            "newton_strict_ok": strict,
                            "discriminant_ok": disc,
                        }
                    )
    negs = [r for r in rows if r["c_Jm2_negative"]]
    return {
        "j": J,
        "criterion": "where c_{J-2} < 0, the quadratic c_{J-3} + c_{J-2} y + c_{J-1} y^2 must be "
        "nonnegative for y >= 0, i.e. c_{J-2}^2 <= 4 c_{J-1} c_{J-3} (discriminant); the stronger "
        "log-concave form c_{J-2}^2 <= c_{J-1} c_{J-3} is reported too",
        "points": len(grid) ** 3,
        "points_with_c_Jm2_negative": len(negs),
        "discriminant_failures_where_negative": fails,
        "strict_newton_failures_where_negative": sum(1 for r in negs if not r["newton_strict_ok"]),
        "rows_of_interest": rows[:80],
    }


def general_coefficient_formula(N=None, kmax: int | None = None) -> dict:
    """Check the closed form for EVERY y-coefficient, not just c_{J-2}.

        [y^k] N = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                        den^i e_{J-1-i-k}(A_i..A_{J-2}),

    with A_r = tk_num + (c+2r) den and poch_i = PROD_{q=1}^{2i}(2n-2J+q)/(i! 2^i).

    This is the foundation the uniformity argument would stand on: statement (1)
    of the repair -- "every c_k with k != J-2 is manifestly nonnegative" -- is a
    statement about THIS expression, so the expression itself must be verified
    against the assembled polynomial first.  Light enough to run at small j while
    the founder's machine is busy.
    """
    import math

    from knife_tail2 import E_at

    lam, D_num, den, m_expr = region()
    if N is None:
        N = build_P(lam, D_num, den, m_expr)
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    s2 = s * s
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, Y)
    tk_num = D_num + y * den
    A = [tk_num + den * (c_const + 2 * r) for r in range(J - 1)]

    def e_sym_of(items, t):
        acc = [Q3Poly.const(NV, 1)] + [Q3Poly.const(NV, 0)] * t
        for it in items:
            for q in range(min(t, len(acc) - 1), 0, -1):
                acc[q] = acc[q] + acc[q - 1] * it
        return acc[t]

    got = {}
    for part, idx in ((N.a, 0), (N.b, 1)):
        for e, cval in part.c.items():
            got.setdefault(int(e[Y]), [{}, {}])[idx][(int(e[THL]), int(e[V]), int(e[K3]))] = cval

    checked, bad = [], []
    top = J - 1 if kmax is None else min(J - 1, kmax)
    for k in range(top + 1):
        acc = Q3Poly.const(NV, 0)
        for i in range(J - k):
            poch = Q3Poly.const(NV, 1)
            for q in range(1, 2 * i + 1):
                poch = poch * (2 * n_expr - 2 * J + q)
            wgt = fmpq(1, math.factorial(i) * 2**i)
            s2i = Q3Poly.const(NV, 1)
            for _ in range(i):
                s2i = s2i * s2
            deni = Q3Poly.const(NV, 1)
            for _ in range(i):
                deni = deni * den
            term = E_at(m_expr, J - 1 - i) * poch * s2i * deni * e_sym_of(A[i:], J - 1 - i - k)
            term = Q3Poly(term.a * wgt, term.b * wgt)
            acc = acc + term if i % 2 == 0 else acc - term
        denk = Q3Poly.const(NV, 1)
        for _ in range(k):
            denk = denk * den
        pred = acc * denk
        if (J - 1 + k) % 2:
            pred = Q3Poly.const(NV, 0) - pred
        pd = {}
        for part, idx in ((pred.a, 0), (pred.b, 1)):
            for e, cval in part.c.items():
                if e[Y] != 0:
                    continue
                pd.setdefault((int(e[THL]), int(e[V]), int(e[K3])), [fmpq(0), fmpq(0)])[idx] = cval
        gd = got.get(k, [{}, {}])
        keys = set(pd) | set(gd[0]) | set(gd[1])
        mism = 0
        for key in keys:
            ga, gb = gd[0].get(key, fmpq(0)), gd[1].get(key, fmpq(0))
            pa, pb = (pd.get(key, [fmpq(0), fmpq(0)]))[0], (pd.get(key, [fmpq(0), fmpq(0)]))[1]
            if ga != pa or gb != pb:
                mism += 1
        checked.append({"k": k, "monomials": len(keys), "mismatches": mism})
        if mism:
            bad.append(k)
    return {"j": J, "coefficients_checked": checked, "coefficients_with_mismatch": bad}


if __name__ == "__main__":
    raise SystemExit(main())
