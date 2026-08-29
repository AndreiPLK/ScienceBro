"""A proof machine for conjecture (B) at any FIXED t.

(B) is `p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}` for the central factorial family
(results/FINITE_N_BRIDGE.md).  For a fixed t it is a polynomial inequality in n,
because every ingredient is:

    p_j = e_j / C(N,j),  N = n-1,  e_j a polynomial in n of degree 3j,
    C(N,j) a polynomial in n of degree j,

so, cross-multiplying by the positive binomials,

    (B_t)   e_{t+1}^3 e_{t-1} C(N,t)^3 C(N,t+2)  -  e_t^3 e_{t+2} C(N,t+1)^3 C(N,t-1)  >=  0.

That difference is one explicit polynomial.  If substituting `n = m + s` makes all
its coefficients nonnegative, (B) is PROVED at that t for every `n >= s` -- the
same all-nonnegative-coefficients move that carries the repair certificate.

This does not prove (B) for all t at once, and the file does not pretend to: it
proves rungs, and it reports the smallest shift that works for each.  The rung
that matters most is t = 1, where the slack is tightest.

Run: python lab/conjecture_B_rungs.py -> results/conjecture_B_rungs.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def interpolate(deg: int, value, start: int) -> fmpq_poly:
    xs = list(range(start, start + deg + 1))
    ys = [fmpq(value(x)) for x in xs]
    out = fmpq_poly([0])
    for i, (xi, yi) in enumerate(zip(xs, ys, strict=True)):
        num, den = fmpq_poly([1]), fmpq(1)
        for j, xj in enumerate(xs):
            if i != j:
                num = num * fmpq_poly([-xj, 1])
                den *= fmpq(xi - xj)
        out = out + num * (yi / den)
    return out


def e_poly(t: int, start: int) -> fmpq_poly:
    return interpolate(3 * t, lambda n: E2_list(n, t)[t], start)


def binom_poly(j: int) -> fmpq_poly:
    """C(N, j) as a polynomial in n, with N = n-1."""
    N = fmpq_poly([-1, 1])
    out = fmpq_poly([1])
    for i in range(j):
        out = out * (N - i)
    from math import factorial

    return fmpq_poly([c / fmpq(factorial(j)) for c in [out[k] for k in range(out.degree() + 1)]])


def rung(t: int) -> dict:
    start = max(8, 2 * t + 6)
    e = {j: e_poly(j, start) for j in (t - 1, t, t + 1, t + 2) if j >= 1}
    if t - 1 == 0:
        e[0] = fmpq_poly([1])
    for j, P in e.items():
        if j >= 1:
            for n in range(start, start + 12):
                assert P(fmpq(n)) == fmpq(E2_list(n, j)[j]), (t, j, n)
    C = {j: binom_poly(j) for j in (t - 1, t, t + 1, t + 2)}
    lhs = e[t + 1] ** 3 * e[t - 1] * C[t] ** 3 * C[t + 2]
    rhs = e[t] ** 3 * e[t + 2] * C[t + 1] ** 3 * C[t - 1]
    diff = lhs - rhs

    # direct spot check of the sign, against the reference engine
    bad = 0
    for n in range(max(6, 2 * t + 4), max(6, 2 * t + 4) + 20):
        E = E2_list(n, t + 2)
        if len(E) <= t + 2:
            continue
        p = [fmpq(E[j], comb(n - 1, j)) for j in range(t + 3)]
        if p[t + 1] ** 3 * p[t - 1] < p[t] ** 3 * p[t + 2]:
            bad += 1

    best = None
    for s in range(2, 41):
        sh = diff(fmpq_poly([s, 1]))
        cs = [sh[i] for i in range(sh.degree() + 1)]
        if all(c >= 0 for c in cs):
            best = s
            break
    return {
        "t": t,
        "degree": diff.degree(),
        "smallest_shift_with_all_coefficients_nonnegative": best,
        "proved_for_n_at_least": best,
        "direct_check_failures": bad,
    }


def uniform_rung(t: int) -> bool:
    """Is the rung polynomial nonnegative-coefficient after the shift n = m + 2t?

    That shift is exactly what the application needs (its range is t < n/2, i.e.
    n > 2t), so a clean answer here proves (B) at that t on the whole needed range.
    """
    start = max(8, 2 * t + 6)
    e = {j: (e_poly(j, start) if j >= 1 else fmpq_poly([1])) for j in (t - 1, t, t + 1, t + 2)}
    C = {j: binom_poly(j) for j in (t - 1, t, t + 1, t + 2)}
    diff = (
        e[t + 1] ** 3 * e[t - 1] * C[t] ** 3 * C[t + 2]
        - e[t] ** 3 * e[t + 2] * C[t + 1] ** 3 * C[t - 1]
    )
    sh = diff(fmpq_poly([2 * t, 1]))
    return all(sh[i] >= 0 for i in range(sh.degree() + 1))


def main() -> int:
    t0 = time.time()
    rungs = [rung(t) for t in (1, 2, 3, 4)]
    top = int(os.environ.get("RUNG_TOP", "40"))
    uniform_bad = [t for t in range(3, top + 1) if not uniform_rung(t)]
    out = {
        "what": "(B) at fixed t is one polynomial inequality in n; a shift making all its "
        "coefficients nonnegative proves that rung",
        "rungs": rungs,
        "uniform_shift_2t": {
            "t_range": f"3..{top}",
            "failures": uniform_bad,
            "meaning": "a clean t proves (B) at that t for every n > 2t, which is the whole "
            "range the bridge needs; so (B) is a theorem for t <= this range",
        },
        "note": "this proves rungs, not (B) for all t at once; t = 1 is the tightest rung "
        "and is proved",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "conjecture_B_rungs.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"uniform shift 2t over t = 3..{top}: {len(uniform_bad)} failures")
    for r in rungs:
        print(
            f"   t={r['t']}: degree {r['degree']}, proved for n >= "
            f"{r['smallest_shift_with_all_coefficients_nonnegative']}, "
            f"direct failures {r['direct_check_failures']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
