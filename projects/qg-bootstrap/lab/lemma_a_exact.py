"""Lemma A, checked EXACTLY over Q(sqrt3) -- no floating point anywhere.

Every ingredient of

    phi_i = tau_i / C(L-1, i),
    tau_i = E_{J-1-i} * poch_i * s^{2i} * den^i * e_{J-1-i-k}(A_i .. A_{J-2})

lives in `Q(sqrt3)` when the region point is rational: `E` is an integer, `poch` and `den`
are rational, and `s^2` and the `A_r` are `a + b sqrt3`. So `phi` and all its finite
differences are exact, and their signs are decided by `sign_q3`, not by comparison of
floats.

This exists because double precision could not decide the high-order differences. On 30
August a thirteenth difference of doubles reported 75 violations that vanished entirely at
60, 200 and 250 digits, and a first attempt at a noise guard passed the same noise through
as "refuted" because it compared against the wrong scale. Exact arithmetic ends that whole
class of question.

The domain is the one Proposition 1 actually needs: `k` outside `{J-2, J-3}`. The
unrestricted statement is FALSE -- at `J = 16`, `k = 13 = J-3` the sequence fails at the
first difference.

Run: KNIFE_J=12 python lab/lemma_a_exact.py -> results/lemma_a_exact_j<J>.json
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
J = int(os.environ.get("KNIFE_J", "12"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from prover2_core import Q3Poly, sign_q3  # noqa: E402
from provenance import stamp  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from sciencebro_math.families import centered_squares, esym  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

Q3 = tuple[fmpq, fmpq]  # a + b sqrt3


def mul(x: Q3, y: Q3) -> Q3:
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def add(x: Q3, y: Q3) -> Q3:
    return (x[0] + y[0], x[1] + y[1])


def sub(x: Q3, y: Q3) -> Q3:
    return (x[0] - y[0], x[1] - y[1])


def scale(c: fmpq, x: Q3) -> Q3:
    return (c * x[0], c * x[1])


def sgn(x: Q3) -> int:
    return sign_q3(x[0], x[1])


def _ev(q, pt: tuple[fmpq, ...]) -> fmpq:
    tot = fmpq(0)
    for e, c in q.c.items():
        term = c
        for idx, power in enumerate(e):
            if power:
                term *= pt[idx] ** power
        tot += term
    return tot


def ev3(P, pt: tuple[fmpq, ...]) -> Q3:
    return (_ev(P.a, pt), _ev(P.b, pt))


def point_data(pt: tuple[fmpq, ...]) -> dict:
    lam, D_num, den, m_expr = region()
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, 1)
    tk = D_num + y * den
    A = [ev3(tk + den * (c_const + 2 * r), pt) for r in range(J - 1)]
    return {
        "den": _ev(den.a, pt),
        "n": int(_ev(n_expr.a, pt)),
        "m": int(_ev(m_expr.a, pt)),
        "s2": ev3(s * s, pt),
        "A": A,
    }


def phis_exact(P: dict, k: int) -> list[Q3]:
    L = J - k
    den, m, n = P["den"], P["m"], P["n"]
    Et = esym(centered_squares(m + 3))
    out: list[Q3] = []
    for i in range(L):
        mm = J - 1 - i - k
        items = P["A"][i:]
        if mm < 0 or mm > len(items):
            continue
        acc: list[Q3] = [(fmpq(1), fmpq(0))] + [(fmpq(0), fmpq(0))] * len(items)
        for it in items:
            for q in range(len(items), 0, -1):
                acc[q] = add(acc[q], mul(acc[q - 1], it))
        e_sym = acc[mm]
        poch = fmpq(1)
        for q in range(1, 2 * i + 1):
            poch *= 2 * n - 2 * J + q
        poch /= math.factorial(i) * 2**i
        s2p: Q3 = (fmpq(1), fmpq(0))
        for _ in range(i):
            s2p = mul(s2p, P["s2"])
        E = Et[J - 1 - i] if 0 <= J - 1 - i < len(Et) else fmpq(0)
        tau = scale(E * poch * den**i, mul(s2p, e_sym))
        out.append(scale(fmpq(1, comb(L - 1, i)), tau))
    return out


def first_negative_order(phi: list[Q3]) -> int | None:
    cur = list(phi)
    order = 0
    while len(cur) > 1:
        cur = [sub(cur[i + 1], cur[i]) for i in range(len(cur) - 1)]
        order += 1
        if any(sgn(x) < 0 for x in cur):
            return order
    return None


def main() -> int:
    t0 = time.time()
    pts = [
        (fmpq(a, 8), fmpq(b), fmpq(c), fmpq(d))
        for a in (0, 4, 8)
        for b in (0, 5, 10**4)
        for c in (0, 2, 3)
        for d in (0, 3, 50)
    ]
    rows, bad = [], []
    for pt in pts:
        P = point_data(pt)
        for k in range(J - 1):
            excluded = k in (J - 2, J - 3)
            phi = phis_exact(P, k)
            if len(phi) < 3:
                continue
            o = first_negative_order(phi)
            rows.append({"k": k, "excluded": excluded, "first_negative_order": o})
            if o is not None and not excluded:
                bad.append({"point": [str(x) for x in pt], "k": k, "order": o})
    on_domain = [r for r in rows if not r["excluded"]]
    excluded_rows = [r for r in rows if r["excluded"]]
    out = {
        "j": J,
        "statement": "Lemma A: phi_i = tau_i/C(L-1,i) is absolutely monotone, for k outside "
        "{J-2, J-3}",
        "arithmetic": "EXACT over Q(sqrt3); signs by sign_q3; no floating point anywhere",
        "region_points": len(pts),
        "checked_on_domain": len(on_domain),
        "violations_on_domain": len(bad),
        "examples": bad[:10],
        "excluded_indices_checked": len(excluded_rows),
        "excluded_indices_that_fail": sum(
            1 for r in excluded_rows if r["first_negative_order"] is not None
        ),
        "holds": not bad,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / f"lemma_a_exact_j{J}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[j={J}] EXACT: {len(on_domain)} checks on the domain, {len(bad)} violations; "
        f"excluded indices fail in {out['excluded_indices_that_fail']} of "
        f"{len(excluded_rows)}  ({out['runtime_s']}s)"
    )
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
