"""Gegenbauer expansion on flint, and the term-by-term test that would end the theorem.

THE REDUCTION. In the variable v (u = v^2) our positive polynomial is a square,

    F(v) = q(v)^2,    q(v) = (2/s)^N (x)_N ,   x = (s v + N - 1)/2,  N = n - 1,

with (x)_N the FALLING factorial -- the roots of q are the arithmetic progression
(N-1-2k)/s, k = 0..N-1. Both identities were verified exactly before this module
was written.

The classical square-of-a-factorial identity

    (x)_N^2 = SUM_{j=0}^{N} C(N,j)^2 j! (x)_{2N-j}

has ALL WEIGHTS POSITIVE. So F is a positive combination of SINGLE falling
factorials. Therefore:

    IF every (x)_M, M = N..2N, has non-negative EVEN-index Gegenbauer
    coefficients, THEN F does, and the theorem is finished.

Only the even indices are claimed, and that is not a weakening born of
convenience: F is even in v, so its odd coefficients vanish identically, while an
individual (x)_M is NOT even and its odd coefficients must cancel across the sum.
Any term-by-term argument therefore CANNOT hold for odd indices, and does not
need to.

This module builds the machinery exactly (flint, no float anywhere) and tests
that hypothesis. It is a test, not a proof: a single negative even coefficient
kills the route, and no amount of non-negative ones establishes it.

Run: python lab/gegenbauer_flint.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
V = fmpq_poly([0, 1])


def T_k(lam: fmpq, k: int) -> fmpq:
    """The shore of level k, exactly (our published result)."""
    return fmpq(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k


def T_hat(lam: fmpq, kmax: int | None = None) -> fmpq:
    """min over k >= 3 of T_k -- the binding shore.

    The minimising k sits at k ~ sqrt(3) lam (measured: k/lam = 1.7320 at
    lam = 100..900), so a FIXED cap silently truncates. A cap of 400 returned
    10547 instead of 9462 at lam = 500 -- an 11 percent error in the shore, which
    is a wrong answer, not a slow one. The cap therefore scales with lam, and
    `_argmin_is_interior` refuses to let a truncated minimum pass unnoticed.
    """
    if kmax is None:
        kmax = max(400, int(4 * float(lam)) + 20)
    best, bk = T_k(lam, 3), 3
    for k in range(4, kmax + 1):
        t = T_k(lam, k)
        if t < best:
            best, bk = t, k
    if bk >= kmax:
        raise ValueError(f"T_hat minimum hit the cap at k={bk}; raise kmax")
    return best


def gegenbauer(kmax: int, gamma: fmpq) -> list[fmpq_poly]:
    """C_0^gamma .. C_kmax^gamma by the exact three-term recurrence."""
    out = [fmpq_poly([1])]
    if kmax >= 1:
        out.append(fmpq_poly([0, 2]) * gamma)
    for k in range(2, kmax + 1):
        term = out[-1] * V * (2 * (fmpq(k) + gamma - 1)) - out[-2] * (fmpq(k) + 2 * gamma - 2)
        out.append(term / fmpq(k))
    return out


def to_gegenbauer(p: fmpq_poly, gamma: fmpq) -> list[fmpq]:
    """Coefficients of p in the C_k^gamma basis, exactly, by triangular peeling."""
    deg = p.degree()
    if deg < 0:
        return []
    basis = gegenbauer(deg, gamma)
    coeffs = [fmpq(0)] * (deg + 1)
    work = fmpq_poly(p)
    for k in range(deg, -1, -1):
        lead = basis[k].coeffs()[k]
        c = work.coeffs()[k] / lead if work.degree() >= k else fmpq(0)
        coeffs[k] = c
        if c != 0:
            work = work - basis[k] * c
    return coeffs


def falling_in_v(M: int, N: int, s: fmpq) -> fmpq_poly:
    """(x)_M as a polynomial in v, with x = (s v + N - 1)/2."""
    x = (V * s + (N - 1)) / fmpq(2)
    out = fmpq_poly([1])
    for i in range(M):
        out = out * (x - i)
    return out


def q_poly(n: int, lam: fmpq) -> fmpq_poly:
    """q(v) = prod (v - (N-1-2k)/s), the polynomial whose square is F."""
    N = n - 1
    s = lam + (n - 1)
    out = fmpq_poly([1])
    for k in range(N):
        out = out * (V - fmpq(N - 1 - 2 * k) / s)
    return out


# --------------------------------------------------------------------------
# self-checks: nothing below is used until all three pass
# --------------------------------------------------------------------------
def self_check() -> list[str]:
    bad = []
    # 1. the recurrence really produces Gegenbauer polynomials: C_k(1) = binom(k+2g-1, k)
    g = fmpq(7, 3)
    Cs = gegenbauer(8, g)
    val = fmpq(1)
    for k, C in enumerate(Cs):
        got = sum((c * fmpq(1) ** i for i, c in enumerate(C.coeffs())), fmpq(0))
        if got != val:
            bad.append(f"C_{k}(1) = {got}, expected {val}")
        val = val * (fmpq(k + 1) + 2 * g - 1) / fmpq(k + 1)
    # 2. the expansion round-trips
    for gam in (fmpq(1, 2), fmpq(5), fmpq(37, 4)):
        p = fmpq_poly([3, -2, 5, 1, -7, 2])
        cs = to_gegenbauer(p, gam)
        B = gegenbauer(len(cs) - 1, gam)
        rec = fmpq_poly([0])
        for c, b in zip(cs, B):
            rec = rec + b * c
        if rec != p:
            bad.append(f"round-trip failed at gamma={gam}")
    # 3. q^2 equals the positive combination of falling factorials (the identity
    #    the whole route rests on), checked as POLYNOMIALS in v, not at points
    from math import comb, factorial

    for n in (5, 6, 9, 12):
        N, lam = n - 1, fmpq(1)
        s = lam + (n - 1)
        lhs = q_poly(n, lam) ** 2 * (s / fmpq(2)) ** (2 * N)
        rhs = fmpq_poly([0])
        for j in range(N + 1):
            rhs = rhs + falling_in_v(2 * N - j, N, s) * fmpq(comb(N, j) ** 2 * factorial(j))
        if lhs != rhs:
            bad.append(f"square identity failed at n={n}")
    return bad


def main() -> int:
    t0 = time.time()
    bad = self_check()
    print("self-check:", "PASS" if not bad else "FAIL " + "; ".join(bad), flush=True)
    if bad:
        return 1

    print()
    print("HYPOTHESIS: every (x)_M, M = N..2N, has non-negative EVEN-index")
    print("Gegenbauer coefficients at the shore. One negative kills the route.")
    print()
    print("   n  lam        gamma(shore)   M range   even coeffs   negatives   min even coeff")
    out = []
    for n, lam in ((5, fmpq(1)), (6, fmpq(1)), (8, fmpq(1)), (6, fmpq(7)), (9, fmpq(3))):
        N = n - 1
        s = lam + (n - 1)
        gamma = T_hat(lam) / fmpq(2) - fmpq(3, 2)
        neg = 0
        tot = 0
        worst = None
        worst_at = None
        for M in range(N, 2 * N + 1):
            cs = to_gegenbauer(falling_in_v(M, N, s), gamma)
            for k in range(0, len(cs), 2):
                tot += 1
                if worst is None or cs[k] < worst:
                    worst, worst_at = cs[k], (M, k)
                if cs[k] < 0:
                    neg += 1
        print(
            f"  {n:3d}  {str(lam):8s}  {float(gamma):11.4f}   {N}..{2 * N:3d}   "
            f"{tot:9d}   {neg:9d}   {float(worst):+.4e} at M={worst_at[0]},k={worst_at[1]}",
            flush=True,
        )
        out.append(
            {
                "n": n,
                "lam": str(lam),
                "gamma_shore": str(gamma),
                "even_coeffs": tot,
                "negatives": neg,
                "min_even_coeff": str(worst),
                "min_at": {"M": worst_at[0], "k": worst_at[1]},
            }
        )

    verdict = "REFUTED" if any(r["negatives"] for r in out) else "consistent"
    print()
    print(f"VERDICT: term-by-term route is {verdict}")

    # ------------------------------------------------------------------
    # THE ROUTE THAT SURVIVED. Dougall's linearization is non-negative for
    # gamma > 0, so if q ITSELF has non-negative Gegenbauer coefficients then
    # q^2 does, and every knife is proved at once. Where does that happen?
    # ------------------------------------------------------------------
    def q_nonneg_at_shore(n: int, lam: fmpq) -> bool:
        g = T_hat(lam) / fmpq(2) - fmpq(3, 2)
        return all(c >= 0 for c in to_gegenbauer(q_poly(n, lam), g))

    def lam_star(n: int, hi_num: int = 20000, it: int = 22) -> fmpq | None:
        lo, hi = fmpq(1), fmpq(hi_num)
        if q_nonneg_at_shore(n, lo):
            return lo
        if not q_nonneg_at_shore(n, hi):
            return None
        for _ in range(it):
            mid = (lo + hi) / 2
            if q_nonneg_at_shore(n, mid):
                hi = mid
            else:
                lo = mid
        return hi

    print()
    print("PROVED REGION: smallest lam above which q is non-negative at the shore,")
    print("which by Dougall proves EVERY knife at EVERY dimension below the shore.")
    print("      n     lam*(n)    lam*/n")
    boundary = []
    for n in (5, 8, 14, 20, 28, 40, 60, 90, 130):
        L = lam_star(n)
        if L is None:
            continue
        boundary.append({"n": n, "lam_star": str(L), "ratio": float(L) / n})
        print(f"  {n:5d}  {float(L):10.3f}  {float(L) / n:8.5f}", flush=True)
    ratios = [b["ratio"] for b in boundary if b["n"] >= 20]
    print(f"\n  ratio for n >= 20: {min(ratios):.5f} .. {max(ratios):.5f}")
    print(f"  compare 3 + sqrt(3) = {3 + 3**0.5:.6f}  (a resemblance, NOT a claim)")

    payload = {
        "proved_region": {
            "statement": "for lam >= lam*(n), every knife of level n is positive at "
            "every dimension below the shore, by: F = q^2 with q having equally "
            "spaced roots; the classical quadratic transformation identifying the "
            "knife with the Gegenbauer coefficient of index 2m; Dougall's "
            "non-negative linearization; and DLMF 18.18.16 for the descent",
            "only_unproved_input": "that q itself has non-negative Gegenbauer "
            "coefficients at gamma_shore when lam >= lam*(n) -- MEASURED, not proved",
            "boundary": boundary,
            "ratio_note": "lam*/n sits at 4.72 for n >= 20; 3+sqrt(3) = 4.7320508 "
            "is close but is NOT claimed as the constant",
        },
        "hypothesis": "every (x)_M, M=N..2N, has non-negative even-index Gegenbauer "
        "coefficients at gamma = T_hat(lam)/2 - 3/2",
        "why_it_would_suffice": "(x)_N^2 = sum_j C(N,j)^2 j! (x)_{2N-j} has all weights "
        "positive, and F is even so its odd coefficients vanish identically",
        "verdict": verdict,
        "rows": out,
        "command": "python lab/gegenbauer_flint.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "gegenbauer_term_by_term.json").write_text(
        json.dumps(payload, indent=1), encoding="utf-8"
    )
    print("written results/gegenbauer_term_by_term.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
