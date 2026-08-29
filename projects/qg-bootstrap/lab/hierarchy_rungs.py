"""Proving the log-difference hierarchy at FIXED (t, r), for every n at once.

`higher_difference_hierarchy.py` measures the hierarchy on a range of n. This proves it,
one rung at a time, by the move that has carried every other result in this programme:
write the statement as one polynomial in n, substitute n = m + s, and check that all
coefficients are nonnegative.

    Delta^r log p_t < 0
      <=>  PROD_{j : r-j even} p_{t+j}^{C(r,j)}  <  PROD_{j : r-j odd} p_{t+j}^{C(r,j)}

Each p is e/C(N,·) with e a polynomial in n of degree 3t and C(N,·) a polynomial in n,
so cross-multiplying gives a single polynomial inequality. If the shifted polynomial has
all nonnegative coefficients, the rung is PROVED for every n >= s -- an argument, not a
measurement, and it covers infinitely many n.

**What is new here is r >= 4.** The rung r = 3 is exactly conjecture (B), already proved
for t <= 100 by `conjecture_B_rungs.py`. If r = 4 and beyond also succumb, the hierarchy
is genuinely deeper than (B) rather than a restatement of it.

Degrees grow like 3(t+r)2^r, so this is run at small (t, r) by design; the point is to
learn whether the mechanism survives, not to sweep.

Run: python lab/hierarchy_rungs.py -> results/hierarchy_rungs.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from math import comb, factorial
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from provenance import stamp  # noqa: E402
from sciencebro_math.families import centered_squares, esym  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def e_poly(t: int, start: int | None = None) -> fmpq_poly:
    """e_t of the centred spectrum as an exact polynomial in n, by interpolation.

    `start` must be large enough that the spectrum has at least t entries, i.e. n-1 >= t;
    forgetting that raised an IndexError at t = 6 on the first run.
    """
    start = max(6, t + 2) if start is None else start
    deg = 3 * t + 2
    xs = list(range(start, start + deg + 1))
    ys = [fmpq(esym(centered_squares(x))[t]) for x in xs]
    out = fmpq_poly([0])
    for i, (xi, yi) in enumerate(zip(xs, ys, strict=True)):
        num, den = fmpq_poly([1]), fmpq(1)
        for j, xj in enumerate(xs):
            if i != j:
                num = num * fmpq_poly([-xj, 1])
                den *= fmpq(xi - xj)
        out = out + num * (yi / den)
    # never trust an interpolation: check it past the nodes it was built from
    for x in range(start + deg + 1, start + deg + 6):
        assert out(fmpq(x)) == fmpq(esym(centered_squares(x))[t]), (t, x)
    return out


def binom_poly(j: int) -> fmpq_poly:
    """C(N, j) as a polynomial in n, with N = n - 1."""
    N = fmpq_poly([-1, 1])
    out = fmpq_poly([1])
    for i in range(j):
        out = out * (N - i)
    return fmpq_poly([out[k] / fmpq(factorial(j)) for k in range(out.degree() + 1)])


def rung(t: int, r: int, cache: dict) -> dict:
    """Prove Delta^r log p_t < 0 for all n >= s, or report that no shift up to 60 works."""
    idx = range(t, t + r + 1)
    for j in idx:
        cache.setdefault(j, e_poly(j))
    E = {j: cache[j] for j in idx}
    C = {j: binom_poly(j) for j in idx}

    # p_j = E_j / C_j; the inequality is  PROD_{even side} p < PROD_{odd side} p
    lo = fmpq_poly([1])  # the side that must be SMALLER, numerators
    hi = fmpq_poly([1])
    lo_den = fmpq_poly([1])
    hi_den = fmpq_poly([1])
    for j in range(r + 1):
        c = comb(r, j)
        if (r - j) % 2 == 0:
            lo = lo * E[t + j] ** c
            lo_den = lo_den * C[t + j] ** c
        else:
            hi = hi * E[t + j] ** c
            hi_den = hi_den * C[t + j] ** c
    # cross-multiply: lo/lo_den < hi/hi_den  <=>  hi*lo_den - lo*hi_den > 0 (denominators > 0)
    diff = hi * lo_den - lo * hi_den

    # a direct spot check against the reference computation, so a sign slip cannot pass
    from sciencebro_math.families import normalized_means
    from sciencebro_math.sequences import sign_log_difference

    bad_spot = 0
    for n in range(max(8, 2 * (t + r) + 2), max(8, 2 * (t + r) + 2) + 6):
        p = normalized_means(centered_squares(n))
        if t + r >= len(p):
            continue
        want_neg = sign_log_difference(p, t, r) < 0
        got_pos = diff(fmpq(n)) > 0
        if want_neg != got_pos:
            bad_spot += 1

    best = None
    for s in range(2, 61):
        sh = diff(fmpq_poly([s, 1]))
        if all(sh[k] >= 0 for k in range(sh.degree() + 1)):
            best = s
            break
    return {
        "t": t,
        "r": r,
        "degree": diff.degree(),
        "smallest_shift_all_coefficients_nonnegative": best,
        "proved_for_all_n_at_least": best,
        "spot_check_mismatches": bad_spot,
    }


def main() -> int:
    t0 = time.time()
    rmax = int(os.environ.get("HIER_RMAX", "5"))
    tmax = int(os.environ.get("HIER_TMAX", "3"))
    cache: dict = {}
    rows = []
    for r in range(3, rmax + 1):
        for t in range(1, tmax + 1):
            row = rung(t, r, cache)
            rows.append(row)
            mark = (
                f"PROVED for n >= {row['proved_for_all_n_at_least']}"
                if row["smallest_shift_all_coefficients_nonnegative"]
                else "no shift <= 60 works"
            )
            print(
                f"  r={r} t={t}: degree {row['degree']:<5} {mark}"
                f"   (spot mismatches {row['spot_check_mismatches']})"
            )
    out = {
        "what": "the log-difference hierarchy proved at fixed (t, r) for every n >= s, by "
        "all-nonnegative coefficients after a shift",
        "why_r_ge_4_matters": "r = 3 IS conjecture (B), already proved per t; r >= 4 is new "
        "content and shows whether the hierarchy is deeper than (B)",
        "rows": rows,
        "all_proved": all(r["smallest_shift_all_coefficients_nonnegative"] for r in rows),
        "spot_mismatches_total": sum(r["spot_check_mismatches"] for r in rows),
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "hierarchy_rungs.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nall rungs proved: {out['all_proved']}  ({out['runtime_s']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
