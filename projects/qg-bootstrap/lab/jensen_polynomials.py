"""Are the Jensen polynomials of t -> p_t hyperbolic?

Suggested by the new-literature brief (Ono-style Hermite-Jensen limits, Mukherjee on
signs of higher log-differences). The Jensen polynomial of degree `d` at shift `t` is

    J^{d,t}(X) = SUM_{j=0}^{d} C(d,j) p_{t+j} X^j.

If every one of them is hyperbolic -- all roots real -- then the whole family of
higher-order Turan inequalities holds at once, rather than being proved one at a time.
`d = 2` is ordinary log-concavity; `d = 3` is the first genuinely new member.

Two disciplines matter here.

**Roots are isolated, not estimated.** flint's certified complex root isolation returns
boxes; a root counts as real only when its imaginary part interval contains zero, so a
verdict is a statement about isolating boxes rather than about float noise. And `p_t` are
exact rationals, so the polynomial itself is exact.

**The domain is stated, not assumed.** As everywhere in this programme, the window
`t..t+d` must lie inside the first half. Letting it run past the midpoint reports failures
that are outside any claim, which is a mistake already paid for once.

Run: python lab/jensen_polynomials.py -> results/jensen_polynomials.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from sciencebro_math.families import centered_squares, normalized_means  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def jensen(p: list[fmpq], d: int, t: int) -> fmpq_poly:
    return fmpq_poly([fmpq(comb(d, j)) * p[t + j] for j in range(d + 1)])


def non_real_roots(P: fmpq_poly) -> int:
    return sum(1 for r, _m in P.complex_roots() if not r.imag.contains(0))


def main() -> int:
    t0 = time.time()
    dmax = int(os.environ.get("JENSEN_DMAX", "8"))
    rows, failures = [], []
    for n in (11, 15, 21, 27, 33, 41):
        p = normalized_means(centered_squares(n))
        N = n - 1
        half = N // 2
        for d in range(2, dmax + 1):
            tested = bad = 0
            for t in range(0, half - d + 1):
                J = jensen(p, d, t)
                tested += 1
                nr = non_real_roots(J)
                if nr:
                    bad += 1
                    if len(failures) < 20:
                        failures.append({"n": n, "d": d, "t": t, "non_real_roots": nr})
            rows.append({"n": n, "d": d, "tested": tested, "not_hyperbolic": bad})
        line = " ".join(
            f"d={r['d']}:{r['tested'] - r['not_hyperbolic']}/{r['tested']}"
            for r in rows
            if r["n"] == n
        )
        print(f"  n={n:<3} hyperbolic  {line}")

    total = sum(r["tested"] for r in rows)
    bad_total = sum(r["not_hyperbolic"] for r in rows)
    by_d: dict[int, dict[str, int]] = {}
    for r in rows:
        s = by_d.setdefault(r["d"], {"tested": 0, "not_hyperbolic": 0})
        s["tested"] += r["tested"]
        s["not_hyperbolic"] += r["not_hyperbolic"]

    out = {
        "question": "are the Jensen polynomials of t -> p_t hyperbolic on the first half?",
        "why_it_matters": "hyperbolicity for every d gives the whole family of higher-order "
        "Turan inequalities at once, instead of one rung at a time",
        "method": "exact rational coefficients; roots isolated by flint with certified boxes, "
        "so 'real' means the imaginary interval contains zero",
        "domain": "window t..t+d inside the first half",
        "rows": rows,
        "by_degree": by_d,
        "tested": total,
        "not_hyperbolic": bad_total,
        "all_hyperbolic": bad_total == 0,
        "failures": failures,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "jensen_polynomials.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\ntested {total}, NOT hyperbolic {bad_total}")
    for d in sorted(by_d):
        s = by_d[d]
        print(f"   d={d}: {s['tested'] - s['not_hyperbolic']}/{s['tested']} hyperbolic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
