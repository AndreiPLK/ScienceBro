"""Is leg (a) an alternating series with decreasing terms? A route to uniformity in J.

The verified coefficient formula is an ALTERNATING sum,

    c_k = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i tau_i,
    tau_i = E_{J-1-i} * poch_i * s^{2i} * den^i * e_{J-1-i-k}(A_i .. A_{J-2}),

with every `tau_i > 0` on the region. An alternating sum whose terms DECREASE is
nonnegative, term by term, with no computation at all. So if

    tau_0 >= tau_1 >= tau_2 >= ...    for every k != J-2,

then leg (a) holds at EVERY depth at once -- which is exactly the uniformity the
programme is missing. And the exceptional coefficient would be explained rather than
observed: `c_{J-2}` is negative precisely because there the sequence is NOT decreasing,
`tau_1 > tau_0`.

This file tests that shape. It evaluates the `tau_i` at exact rational region points --
no polynomial is assembled, so it runs in seconds where building `N` takes hours -- and
reports, for each `k`, whether the sequence decreases.

What it can settle: whether the mechanism is right. What it cannot: uniformity itself,
which needs the ratio `tau_{i+1}/tau_i <= 1` proved, not measured. That ratio is a product
of three explicit factors, one of which is `E_{J-2-i}/E_{J-1-i}` -- the same central
factorial ratio the Newton-excess lemma controls. If the shape holds, both legs of the
programme reduce to one lemma.

Run: KNIFE_J=12 python lab/tau_monotonicity.py -> results/tau_monotonicity_j<J>.json
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
from prover2_core import Q3Poly  # noqa: E402
from provenance import stamp  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from sciencebro_math.families import centered_squares, esym  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
SQ3 = None  # sqrt(3) is never needed numerically: lam enters only through s^2 and A


def _ev(q, pt: tuple[fmpq, ...]) -> fmpq:
    """Evaluate a QPoly {exponent tuple: coeff} at an exact rational point."""
    tot = fmpq(0)
    for e, c in q.c.items():
        term = c
        for idx, power in enumerate(e):
            if power:
                term *= pt[idx] ** power
        tot += term
    return tot


def ev3(P, pt: tuple[fmpq, ...]) -> tuple[fmpq, fmpq]:
    """Evaluate a Q3Poly at a point, as the pair (rational part, sqrt3 part)."""
    return (_ev(P.a, pt), _ev(P.b, pt))


def region_point(thL: fmpq, y: fmpq, v: fmpq, K3: fmpq) -> dict:
    """The far-below region at an exact rational point.

    The region polynomials come from `farbelow_negative_pattern.region()` and are merely
    EVALUATED here. An earlier version of this file re-derived them by hand and got the
    A_r wrong; re-deriving what a verified module already computes is how that happened.
    """
    pt = (thL, y, v, K3)
    lam, D_num, den, m_expr = region()
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)
    c_const = 4 * n_expr - 4 * J - 1
    yv = Q3Poly.var(NV, 1)
    tk_num = D_num + yv * den
    A = [ev3(tk_num + den * (c_const + 2 * r), pt) for r in range(J - 1)]
    return {
        "den": _ev(den.a, pt),
        "n": int(_ev(n_expr.a, pt)),
        "m": int(_ev(m_expr.a, pt)),
        "s2": ev3(s * s, pt),
        "A": A,
    }


def mul(a: tuple[fmpq, fmpq], b: tuple[fmpq, fmpq]) -> tuple[fmpq, fmpq]:
    """(x + y sqrt3)(u + v sqrt3) = (xu + 3yv) + (xv + yu) sqrt3."""
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def val(a: tuple[fmpq, fmpq]) -> float:
    return float(a[0]) + float(a[1]) * math.sqrt(3.0)


def taus(P: dict, k: int) -> list[float]:
    """tau_i for i = 0 .. J-1-k, as floats -- only their ORDER is being inspected."""
    den, m = P["den"], P["m"]
    # the central factorial numbers at this point, computed once: n = m + 3 is an integer
    # here because v is. The local name must NOT shadow the imported esym -- it did, and
    # the run died with "tuple object is not callable".
    Etab = esym(centered_squares(int(m) + 3))
    A = P["A"]
    out = []
    for i in range(J - k):
        mm = J - 1 - i - k
        items = A[i:]
        if mm > len(items) or mm < 0:
            continue
        acc = [(fmpq(1), fmpq(0))] + [(fmpq(0), fmpq(0))] * len(items)
        for it in items:
            for q in range(len(items), 0, -1):
                pr = mul(acc[q - 1], it)
                acc[q] = (acc[q][0] + pr[0], acc[q][1] + pr[1])
        esym_A = acc[mm]
        poch = fmpq(1)
        for q in range(1, 2 * i + 1):
            poch *= 2 * P["n"] - 2 * J + q
        poch /= math.factorial(i) * 2**i
        s2p = (fmpq(1), fmpq(0))
        for _ in range(i):
            s2p = mul(s2p, P["s2"])
        idx = J - 1 - i
        E = Etab[idx] if 0 <= idx < len(Etab) else fmpq(0)
        term = mul(esym_A, s2p)
        out.append(float(E) * float(poch) * (float(den) ** i) * val(term))
    return out


def main() -> int:
    t0 = time.time()
    pts = [
        (fmpq(a, 4), fmpq(b), fmpq(c), fmpq(d))
        for a in (0, 2, 4)
        for b in (0, 1, 17)
        for c in (0, 5, 40)
        for d in (0, 7)
    ]
    rows = []
    for k in range(J):
        dec = nondec = 0
        for thL, y, v, K3 in pts:
            P = region_point(thL, y, v, K3)
            t = taus(P, k)
            if len(t) < 2:
                continue
            if all(t[i] >= t[i + 1] for i in range(len(t) - 1)):
                dec += 1
            else:
                nondec += 1
        rows.append({"k": k, "terms": J - k, "decreasing": dec, "not_decreasing": nondec})
    # SELF-CHECK: reconstruct the sign of c_k from the taus and compare with the known
    # pattern -- negative only at k = J-2. A verdict from an instrument that cannot
    # reproduce the known answer is worthless.
    P0 = region_point(fmpq(1, 2), fmpq(3), fmpq(9), fmpq(2))
    recon = {}
    for k in range(J):
        t = taus(P0, k)
        acc = sum((-1) ** i * x for i, x in enumerate(t))
        if (J - 1 + k) % 2:
            acc = -acc
        recon[k] = acc
    neg = sorted(k for k, x in recon.items() if x < 0)
    print(f"   self-check: reconstructed negative coefficients at k = {neg} "
          f"(expected only {J - 2})")
    instrument_ok = neg == [J - 2]

    bad = [r for r in rows if r["k"] != J - 2 and r["not_decreasing"]]
    print(f"[j={J}] tau_i decreasing, by coefficient index k  ({len(pts)} region points)")
    for r in rows:
        mark = "  <- the exceptional coefficient" if r["k"] == J - 2 else ""
        print(f"   k={r['k']:<3} terms {r['terms']:<3} decreasing {r['decreasing']:<4} "
              f"NOT {r['not_decreasing']:<4}{mark}")
    out = {
        "j": J,
        "question": "is c_k an alternating sum with DECREASING terms for every k != J-2?",
        "why": "an alternating sum with decreasing terms is nonnegative with no computation, "
        "so this shape would give leg (a) at every depth at once",
        "region_points": len(pts),
        "rows": rows,
        "instrument_self_check": {"reconstructed_negative_k": neg,
                                  "expected": [J - 2], "passes": instrument_ok},
        "shape_holds_away_from_J_minus_2": not bad,
        "exceptional_k": J - 2,
        "status": "EXACT region points, floats used ONLY to compare magnitudes of positive "
        "quantities; a verdict here is a shape check, not a proof",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / f"tau_monotonicity_j{J}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nshape holds away from k = J-2: {not bad}   ({out['runtime_s']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
