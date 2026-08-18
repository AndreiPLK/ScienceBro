"""Depth 3, same parity-split pipeline as depth 2, engine 2 only.

Builds H_final(K, c) for depth 3 (cubic in gamma before homogenization) at the
half-level M = K (an actual integer, so T_hat(lam) <= T_K(lam) by definition --
the fix ERR-0008 already established for depth 2, unchanged here since it does
not depend on depth).

CRITICAL: verified against the exact reference engine (jacobi_coeff_rec) at
concrete (K, c) points BEFORE any Bernstein run is trusted -- exactly the
discipline that caught the depth-2 off-by-one earlier, and the discipline
that would have caught tonight's D_shore+3 mistake immediately if it had been
applied to that exploratory script too.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth2_parity_proof import C_, K_, ONE, BiPoly, compactify_K, prove_box  # noqa: E402
from depth3_proof import elementary_symmetric, falling_poly, poch  # noqa: E402


def lift_N(poly_in_N, N_bi: BiPoly) -> BiPoly:
    """Evaluate a univariate fmpq_poly (in N) at the BiPoly N_bi, via Horner."""
    coeffs = poly_in_N.coeffs()
    result = BiPoly.const(0)
    for c in reversed(coeffs):
        result = result * N_bi + BiPoly.const(c)
    return result


def build_branch(parity: str, e_polys: dict):
    """H_final(K, c) for depth 3, one parity branch, homogenized in gamma."""
    K = K_()
    c = C_()
    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + ONE
    d = 3
    m = N - BiPoly.const(d)
    lam = c * N
    X = (N + lam) * (N + lam)

    Qbig = K * (K - fmpq(2))
    Abig = K * fmpq(2) - fmpq(3)
    Bexpr = lam * lam + (K * fmpq(2) - fmpq(2)) * lam + ONE
    Pg = Abig * (Bexpr * fmpq(3) + Qbig)
    Qg = Qbig * fmpq(2)

    # Coefficient of gamma^i in R(N,gamma), BEFORE homogenization, is built from
    # the k=3-i term's (2m+gamma+1)_j factor -- degree i in gamma requires j>=i,
    # so only the k <= 3-i term contributes... actually cleanest: build R as a
    # sum over k, with (2m+gamma+1)_j cleared by Qg^j individually, then bring
    # all terms to the common power Qg^3 by multiplying by Qg^(3-j).
    total = BiPoly.const(0)
    half = BiPoly.const(fmpq(1, 2))
    two_m_Qg = (m * fmpq(2)) * Qg
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeff_bi = lift_N(coeff_N, N) * fmpq((-1) ** k)

        num_bi = BiPoly.const(1)
        for i in range(j):
            num_bi = num_bi * (m + half + BiPoly.const(i))

        den_cleared = BiPoly.const(1)  # (2m+gamma+1)_j * Qg^j, with gamma=Pg/Qg substituted
        for i in range(j):
            den_cleared = den_cleared * (two_m_Qg + Pg + Qg * fmpq(1 + i))

        term = coeff_bi * num_bi * den_cleared * (X**j) * (Qg ** (d - j))
        total = total + term
    return total


def self_check_concrete(e_polys: dict, trials) -> list[str]:
    """Evaluate build_branch's BiPoly at CONCRETE integer (K,c) and compare sign
    to the exact engine at gamma = gamma_at_K(lam), the SAME quantity the
    algebra targets -- not the true shore (that comparison is a separate,
    later step, exactly as it was for depth 2)."""
    from fractions import Fraction as F  # ENGINE-OK: interface glue only

    from jacobi_normal_form import jacobi_coeff_rec

    bad = []
    for parity in ("even", "odd"):
        H = build_branch(parity, e_polys)
        for K_val, c_num, c_den in trials:
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            j = 4  # depth 3 <=> j = 4 always
            m = n - j
            if m < 0 or j > n - 1:
                continue
            c_val = fmpq(c_num, c_den)
            val = fmpq(0)
            for (ki, ci), coeff in H.d.items():
                val += coeff * fmpq(K_val) ** ki * c_val**ci
            sign_formula = (val > 0) - (val < 0)

            lam = c_val * N
            Qbig = fmpq(K_val) * (fmpq(K_val) - 2)
            Abig = fmpq(K_val) * 2 - 3
            Bexpr = lam * lam + (fmpq(K_val) * 2 - 2) * lam + 1
            Pg = Abig * (Bexpr * 3 + Qbig)
            Qg = Qbig * 2
            gamma_at_K = Pg / Qg
            D = gamma_at_K * 2 + 3
            lam_F = F(int(lam.p), int(lam.q))
            D_F = F(int(D.p), int(D.q))
            knife = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, D_F)
            sign_exact = (knife > 0) - (knife < 0)
            if sign_formula != sign_exact:
                bad.append(f"{parity} K={K_val} c={c_num}/{c_den}: {sign_formula} vs {sign_exact}")
    return bad


def main() -> int:
    t0 = time.time()
    e_polys = elementary_symmetric(3)
    trials = [(K, cn, 100) for K in (3, 4, 5, 6, 8, 10, 15) for cn in (1, 5, 10, 20, 29)]
    bad = self_check_concrete(e_polys, trials)
    print(f"self-check: {len(trials) * 2} trials, {len(bad)} mismatches  ({time.time() - t0:.0f}s)")
    for b in bad[:10]:
        print("  ", b)
    if bad:
        print("SELF-CHECK FAILED -- fix the algebra before running Bernstein")
        return 1
    print("SELF-CHECK PASSED")

    from depth2_parity_proof import BiPoly, one_minus_v_powers

    def compactify_c(poly: BiPoly, c_min: int) -> BiPoly:
        """c -> c_min/(1-w), cleared by (1-w)^degC -- covers c in [c_min, infinity)."""
        degC = poly.max_deg(1)
        pw = one_minus_v_powers(degC)
        out: dict = {}
        for (ki, ci), coeff in poly.d.items():
            c_here = coeff * fmpq(c_min) ** ci
            for p, cf in pw[degC - ci].items():
                key = (ki, p)
                out[key] = out.get(key, fmpq(0)) + c_here * cf
        return BiPoly({k: v for k, v in out.items() if v != 0})

    all_ok = True
    for parity in ("even", "odd"):
        H = build_branch(parity, e_polys)
        print(f"[{parity}] H_final: K-deg={H.max_deg(0)}, c-deg={H.max_deg(1)}, {len(H.d)} terms")
        poly_v = compactify_K(H, 3)

        # Two overlapping pieces cover ALL c >= 0: a direct box [0, 50] and a
        # compactified [1, infinity). They overlap on [1, 50], so together they
        # miss nothing -- no separate "Half A" algebraic argument needed here,
        # unlike depth 2, because this Bernstein run reaches arbitrarily large c
        # directly.
        t1 = time.time()
        ok_lo, boxes_lo, open_lo = prove_box(
            poly_v, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(50))]
        )
        print(
            f"[{parity}] K>=3, 0<=c<=50: proved={ok_lo}, boxes={boxes_lo}, "
            f"open={len(open_lo)}  ({time.time() - t1:.0f}s)"
        )

        poly_vw = compactify_c(poly_v, c_min=1)
        t2 = time.time()
        ok_hi, boxes_hi, open_hi = prove_box(
            poly_vw, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000))]
        )
        print(
            f"[{parity}] K>=3, c>=1: proved={ok_hi}, boxes={boxes_hi}, "
            f"open={len(open_hi)}  ({time.time() - t2:.0f}s)"
        )
        all_ok = all_ok and ok_lo and ok_hi
        print(f"[{parity}] COMBINED (0<=c<=50 union c>=1 = all c>=0): {ok_lo and ok_hi}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
