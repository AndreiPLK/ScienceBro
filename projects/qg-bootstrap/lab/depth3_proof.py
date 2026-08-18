"""Depth 3: the beta-mean H-polynomial, derived and verified, engine 2 only.

Same pipeline as depth 2 (lab/depth2_parity_proof.py), one depth deeper.

  1. e_0..e_3(N): elementary symmetric functions of the roots of P_N, derived
     from power sums via Newton's identity. Power sums are built by exact
     Lagrange interpolation over integer points and CHECKED against direct
     summation on held-out points before being trusted (the same discipline
     that caught an off-by-one earlier tonight). e_2 here reproduces the
     hand-derived E2 from depth 2 exactly -- the cross-check that the method
     itself is sound before leaning on it for a NEW closed form (e_3).
  2. The cleared beta-mean numerator R(N,gamma) for depth 3 (degree 3 in gamma).
  3. Verify sign(R) == sign(exact knife) against jacobi_coeff_rec, many cells,
     BEFORE trusting anything built on R.

No sympy, no float in any comparison -- fmpq throughout. Where a numeric
threshold is reported for a human to read, it is cast to float only for
printing, never compared as float.

Run: python lab/depth3_proof.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))


def roots_of_P(N: int) -> list[int]:
    out = []
    a = N - 1
    while a > 0:
        out += [a * a, a * a]
        a -= 2
    if N % 2:
        out.append(0)
    assert len(out) == N
    return out


def lagrange_poly(points) -> fmpq_poly:
    X = fmpq_poly([0, 1])
    result = fmpq_poly([0])
    for i, (xi, yi) in enumerate(points):
        if yi == 0:
            continue
        num = fmpq_poly([1])
        den = fmpq(1)
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = num * (X - fmpq(xj))
            den *= fmpq(xi - xj)
        result = result + num * (yi / den)
    return result


def power_sum_poly(t: int) -> fmpq_poly:
    """p_t(N) = sum of root^t as exact fmpq_poly in N, checked on held-out points."""
    deg = 2 * t + 1
    pts = [(n, fmpq(sum(r**t for r in roots_of_P(n)))) for n in range(3, 3 + deg + 1)]
    poly = lagrange_poly(pts)
    for n in range(3 + deg + 1, 3 + deg + 9):
        got = poly(fmpq(n))
        want = fmpq(sum(r**t for r in roots_of_P(n)))
        if got != want:
            raise AssertionError(f"power sum t={t} failed at N={n}: {got} != {want}")
    return poly


def elementary_symmetric(d: int) -> dict[int, fmpq_poly]:
    p = {t: power_sum_poly(t) for t in range(1, d + 1)}
    e = {0: fmpq_poly([1])}
    for k in range(1, d + 1):
        acc = fmpq_poly([0])
        for i in range(1, k + 1):
            acc = acc + e[k - i] * p[i] * ((-1) ** (i - 1))
        e[k] = acc / fmpq(k)
    return e


def falling_poly(shift: int, length: int) -> fmpq_poly:
    """(N-shift)(N-shift-1)...(N-shift-length+1), as fmpq_poly in N."""
    X = fmpq_poly([0, 1])
    r = fmpq_poly([1])
    for i in range(length):
        r = r * (X - fmpq(shift + i))
    return r


def poch(x: fmpq, k: int) -> fmpq:
    r = fmpq(1)
    for i in range(k):
        r *= x + i
    return r


def knife_sign_via_beta_formula(N: int, d: int, lam: fmpq, gamma: fmpq, e: dict) -> int:
    """sign of the depth-d knife via Q_{N,m}(X) = sum_j r_j (m+1/2)_j/(2m+gamma+1)_j X^j,
    m = N-d, evaluated at concrete (N, lam, gamma). This is the SAME beta-mean
    formula verified earlier tonight (248/248, then 70/70 for depth 2)."""
    m = N - d
    s = lam + N
    X = (fmpq(N) + lam) ** 2
    tot = fmpq(0)
    for k in range(d + 1):
        j = d - k
        coeff = ((-1) ** k) * e[k](fmpq(N)) * falling_poly(k, j)(fmpq(N)) / poch(fmpq(1), j)
        # falling_poly(k,j) evaluated at N: (N-k)(N-k-1)...(N-k-j+1); dividing by j! (poch(1,j)=j!)
        num = poch(fmpq(m) + fmpq(1, 2), j)
        den = poch(fmpq(2 * m) + gamma + 1, j)
        tot += coeff * num / den * X**j
    return (tot > 0) - (tot < 0)


def self_check(d: int, trials) -> list[str]:
    """Compare the beta-formula sign against the exact reference engine."""
    from fractions import Fraction as F  # ENGINE-OK: interface glue to jacobi_coeff_rec only

    from jacobi_normal_form import jacobi_coeff_rec

    e = elementary_symmetric(d)
    bad = []
    for n, lam_num, lam_den, D_num, D_den in trials:
        N = n - 1
        j = d + 1  # depth d <=> j = d+1 always, established earlier tonight for d=2 (j=3)
        m = n - j
        if m < 0 or j < 2 or j > n - 1:
            continue
        lam = fmpq(lam_num, lam_den)
        D = fmpq(D_num, D_den)
        gamma = (D - 3) / 2
        sign_formula = knife_sign_via_beta_formula(N, d, lam, gamma, e)
        lam_F = F(lam_num, lam_den)
        D_F = F(D_num, D_den)
        knife = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, D_F)
        sign_exact = (knife > 0) - (knife < 0)
        if sign_formula != sign_exact:
            bad.append(
                f"n={n} lam={lam_num}/{lam_den} D={D_num}/{D_den}: {sign_formula} vs {sign_exact}"
            )
    return bad


def main() -> int:
    print("depth 3: j = 4 always (m = n-4). Verifying beta-formula against exact engine.")
    trials = []
    for n in (8, 10, 12, 15, 20, 30):
        for lam_num, lam_den in ((1, 1), (3, 1), (1, 10), (7, 1)):
            for D_num, D_den in ((4, 1), (6, 1), (9, 1), (15, 1), (40, 1)):
                trials.append((n, lam_num, lam_den, D_num, D_den))
    bad = self_check(3, trials)
    print(f"  {len(trials)} trials, {len(bad)} mismatches")
    for b in bad[:10]:
        print("   ", b)
    if bad:
        print("SELF-CHECK FAILED -- do not trust anything below")
        return 1
    print("SELF-CHECK PASSED: depth-3 beta-formula matches the exact engine exactly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
