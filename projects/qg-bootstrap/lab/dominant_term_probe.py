"""Does the dominant term of each y-coefficient beat the rest?  Numbers only.

THE STRATEGY THIS TESTS.  results/FARBELOW_NEGATIVE_PATTERN.md derives

    [y^k] N / den^k = SUM_{i=0}^{J-1-k} (-1)^{J-1+k+i} T_i,
    T_i = E_{J-1-i} poch_i s^{2i} den^i e_{J-1-i-k}(A_i..A_{J-2}) >= 0,

and observes that the term with the highest power of s, i = J-1-k, always carries
sign +1.  Manifest positivity of c_k is then implied by the crude but uniform

    T_{J-1-k}  >=  SUM_{i < J-1-k} T_i,                                     (DOM)

which, unlike monomial-by-monomial positivity, is a chain of RATIOS -- each factor
of T_i/T_{i+1} is separately boundable (E-ratios by Newton, poch explicitly, the
e-ratio by count times max A).  If (DOM) holds with a geometric margin, the
uniform proof for k <= J-3 is a decay estimate rather than a search.

This file evaluates T_i as NUMBERS at points of the far-below region -- no
polynomial is assembled, so it runs in seconds and does not compete with the
founder's machine.  Every comparison is a certified `arb` interval; a comparison
the enclosure cannot decide is reported as undecided, never guessed.

Run: python lab/dominant_term_probe.py -> results/dominant_term_probe.json
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from flint import arb, ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
ctx.prec = 300


def region_point(v: int, k3: int, thl: int, J: int):
    """The far-below parametrisation, evaluated as arb numbers."""
    m = 41 + v
    n = m + 3
    kk = arb(v + k3 + 53)
    lam = arb(v + k3 + 51 + thl) * arb(3).sqrt() / 3
    s = lam + (n - 1)
    den = kk * (kk - 2)
    T_cap = arb(3) * (2 * kk - 3) / (kk * (kk - 2)) * (lam * lam + (2 * kk - 2) * lam + 1) + 2 * kk
    tk_num = T_cap * den
    c_const = 4 * n - 4 * J - 1
    A = [tk_num + den * (c_const + 2 * r) for r in range(J - 1)]
    return n, s, den, A


def e_sym(items, t):
    acc = [arb(1)] + [arb(0)] * t
    for it in items:
        for q in range(min(t, len(acc) - 1), 0, -1):
            acc[q] = acc[q] + acc[q - 1] * it
    return acc[t]


def terms(J: int, k: int, v: int, k3: int, thl: int):
    n, s, den, A = region_point(v, k3, thl, J)
    E = E2_list(n, J)
    out = []
    for i in range(J - k):
        poch = arb(1)
        for q in range(1, 2 * i + 1):
            poch *= arb(2 * n - 2 * J + q)
        poch /= arb(math.factorial(i) * 2**i)
        out.append(arb(E[J - 1 - i]) * poch * s ** (2 * i) * den**i * e_sym(A[i:], J - 1 - i - k))
    return out


def main() -> int:
    t0 = time.time()
    rows, undecided, fails = [], 0, 0
    for J in (6, 9, 12, 16, 20, 30):
        for k in range(0, J - 1):
            worst_ratio, worst_pt = None, None
            for v in (0, 3, 40):
                for k3 in (0, 5, 60):
                    for thl in (0, 2, 30):
                        T = terms(J, k, v, k3, thl)
                        dom = T[J - 1 - k]
                        rest = sum(T[: J - 1 - k], arb(0))
                        diff = dom - rest
                        if not (diff > 0 or diff < 0):
                            undecided += 1
                            continue
                        ratio = float(rest / dom)
                        if worst_ratio is None or ratio > worst_ratio:
                            worst_ratio, worst_pt = ratio, (v, k3, thl)
                        if diff < 0:
                            fails += 1
            rows.append(
                {
                    "J": J,
                    "k": k,
                    "is_the_weak_link": k == J - 2,
                    "worst_rest_over_dominant": worst_ratio,
                    "worst_point_v_K3_thL": worst_pt,
                    "dominance_holds": worst_ratio is not None and worst_ratio < 1,
                }
            )
    by_k = {}
    for r in rows:
        if r["worst_rest_over_dominant"] is None:
            continue
        key = "k = J-2 (the weak link)" if r["is_the_weak_link"] else "k <= J-3"
        by_k.setdefault(key, []).append(r["worst_rest_over_dominant"])
    out = {
        "what": "(DOM): does the dominant term T_{J-1-k} exceed the sum of the others?",
        "reading": "rest/dominant < 1 means the crude uniform criterion suffices at that (J,k); "
        "the k = J-2 row is the known weak link",
        "rows": rows,
        "worst_by_class": {kk: max(vv) for kk, vv in by_k.items()},
        "failures": fails,
        "undecided_enclosures": undecided,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "dominant_term_probe.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"failures {fails}, undecided {undecided}")
    for kk, vv in out["worst_by_class"].items():
        print(f"   {kk}: worst rest/dominant = {vv:.4f}")
    bad = [r for r in rows if r["worst_rest_over_dominant"] and r["worst_rest_over_dominant"] > 0.5]
    for r in bad[:12]:
        print(
            f"   J={r['J']:3d} k={r['k']:3d} weak_link={r['is_the_weak_link']} "
            f"rest/dom={r['worst_rest_over_dominant']:.4f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
