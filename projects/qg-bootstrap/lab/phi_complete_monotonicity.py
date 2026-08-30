"""Leg (a) is the sign of a top finite difference. Is the sequence behind it completely monotone?

The verified coefficient formula makes `c_k` an alternating sum,

    c_k = (-1)^{J-1+k} den^k SUM_{i=0}^{L-1} (-1)^i tau_i,    L = J - k,

and measurement showed the `tau_i` sit almost exactly on a BINOMIAL profile:
`tau_i / tau_0` came out as `1, 8.07, 28.6, 57.8, 73.2, 59.5` against
`C(8,i) = 1, 8, 28, 56, 70, 56`. A pure binomial profile makes the alternating sum vanish
identically, so `c_k` is a small residual of an exact cancellation — the relative size fell
from `1e-3` to `1e-9` as the number of terms grew.

That identifies the mechanism. Put

    phi_i = tau_i / C(L-1, i).

Then, by the classical identity `SUM_i (-1)^i C(m,i) f(i) = (-1)^m Delta^m f(0)`,

    SUM_i (-1)^i tau_i = (-1)^{L-1} Delta^{L-1} phi (0),

so **leg (a) is exactly a statement about the sign of the top finite difference of phi**.

And that sign is automatic if `phi` is COMPLETELY MONOTONE: `(-1)^j Delta^j phi >= 0` for
every `j`. By Hausdorff that is the same as `phi` being the moment sequence of a positive
measure on `[0,1]`. If it holds, leg (a) follows at EVERY depth at once, which is the
uniformity the programme is missing.

This file tests complete monotonicity of `phi` at exact rational region points. It is a
shape test, not a proof: a positive answer says the mechanism is right and names the lemma
to prove; a negative answer kills it, as it killed the previous guess (that the `tau_i`
merely decrease) within the hour.

Run: KNIFE_J=9 python lab/phi_complete_monotonicity.py -> results/phi_complete_monotonicity_j<J>.json
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
J = int(os.environ.get("KNIFE_J", "9"))
os.environ["KNIFE_J"] = str(J)
from farbelow_negative_pattern import NV, region  # noqa: E402
from knife_tail2 import E_at  # noqa: E402
from prover2_core import Q3Poly  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def _ev(q, pt: tuple[fmpq, ...]) -> fmpq:
    tot = fmpq(0)
    for e, c in q.c.items():
        term = c
        for idx, power in enumerate(e):
            if power:
                term *= pt[idx] ** power
        tot += term
    return tot


def ev3(P, pt: tuple[fmpq, ...]) -> tuple[fmpq, fmpq]:
    return (_ev(P.a, pt), _ev(P.b, pt))


def build_terms() -> dict:
    """The symbolic tau-factors, built by the verified construction, once."""
    lam, D_num, den, m_expr = region()
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    s2 = s * s
    c_const = 4 * n_expr - 4 * J - 1
    y = Q3Poly.var(NV, 1)
    tk_num = D_num + y * den
    A = [tk_num + den * (c_const + 2 * r) for r in range(J - 1)]
    esym = {}
    for i in range(J):
        items = A[i:]
        acc = [Q3Poly.const(NV, 1)] + [Q3Poly.const(NV, 0)] * len(items)
        for it in items:
            for q in range(len(items), 0, -1):
                acc[q] = acc[q] + acc[q - 1] * it
        esym[i] = acc
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
    return {"esym": esym, "s2p": s2p, "denp": denp, "poch": poch, "m_expr": m_expr}


def phis(T: dict, k: int, pt: tuple[fmpq, ...]) -> list[float]:
    """phi_i = tau_i / C(L-1, i) at an exact region point."""
    L = J - k
    out = []
    for i in range(L):
        m = J - 1 - i - k
        if m >= len(T["esym"][i]) or m < 0:
            continue
        term = (
            E_at(T["m_expr"], J - 1 - i)
            * T["poch"][i]
            * T["s2p"][i]
            * T["denp"][i]
            * T["esym"][i][m]
        )
        a, b = ev3(term, pt)
        tau = float(a) + float(b) * math.sqrt(3.0)
        out.append(tau / comb(L - 1, i))
    return out


def cm_violations(phi: list[float]) -> list[tuple[int, int]]:
    """Indices where (-1)^j Delta^j phi < 0, i.e. complete monotonicity fails."""
    bad = []
    cur = phi[:]
    for j in range(len(phi)):
        for t, v in enumerate(cur):
            if ((-1) ** j) * v < 0:
                bad.append((j, t))
        cur = [cur[t + 1] - cur[t] for t in range(len(cur) - 1)]
        if not cur:
            break
    return bad


def main() -> int:
    t0 = time.time()
    T = build_terms()
    pts = [
        (fmpq(a, 4), fmpq(b), fmpq(c), fmpq(d))
        for a in (0, 2, 4)
        for b in (0, 3, 17)
        for c in (0, 9, 40)
        for d in (0, 2)
    ]
    rows = []
    for k in range(J - 1):
        L = J - k
        if L < 3:
            continue
        cm = viol = 0
        sample = None
        for pt in pts:
            phi = phis(T, k, pt)
            if len(phi) < 3:
                continue
            bad = cm_violations(phi)
            if bad:
                viol += 1
                if sample is None:
                    sample = {"point": [str(x) for x in pt], "first_violation": bad[0],
                              "phi": [f"{x:.6e}" for x in phi]}
            else:
                cm += 1
        rows.append({"k": k, "terms": L, "completely_monotone": cm,
                     "violations": viol, "sample": sample})
        print(f"   k={k:<3} terms {L:<3} completely monotone {cm:<4} violations {viol}")
    bad_rows = [r for r in rows if r["violations"]]
    out = {
        "j": J,
        "identity": "SUM_i (-1)^i tau_i = (-1)^{L-1} Delta^{L-1} phi(0), phi_i = tau_i/C(L-1,i)",
        "question": "is phi completely monotone in i? that would fix the sign of the top "
        "difference and give leg (a) at every depth at once",
        "region_points": len(pts),
        "rows": rows,
        "completely_monotone_everywhere": not bad_rows,
        "status": "shape test at exact region points; floats compare magnitudes of "
        "quantities that are positive by construction. Not a proof either way.",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / f"phi_complete_monotonicity_j{J}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(f"\nphi completely monotone at every k and point: {not bad_rows}  "
          f"({out['runtime_s']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
