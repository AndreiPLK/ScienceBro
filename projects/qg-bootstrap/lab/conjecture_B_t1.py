"""Conjecture (B) at t = 1, PROVED -- and it is the tightest case.

(B) says `p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}` for the central factorial family
(results/FINITE_N_BRIDGE.md).  Measured, its slack shrinks with n and is smallest
at t = 1: the ratio p_2^3/(p_1^3 p_3) is 1.0195 at n = 10, 1.0033 at 20, 1.00059
at 44, 1.00023 at 69.  So t = 1 is the case a proof must survive -- and it is also
the case with closed forms.

    THEOREM.  For n >= 6,  p_2^3 p_0 >= p_1^3 p_3,  i.e. (B) holds at t = 1.

    PROOF.  With N = n-1 and p_t = e_t/C(N,t),
        p_2^3 = 8 e_2^3 / (N(N-1))^3,      p_1^3 p_3 = 6 e_1^3 e_3 / (N^4 (N-1)(N-2)),
    so over the common denominator (N(N-1))^3 N^4 (N-1)(N-2) > 0 the claim is
        P(n) := 8 e_2^3 N^4 (N-1)(N-2)  -  6 e_1^3 e_3 (N(N-1))^3  >=  0.
    e_1, e_2, e_3 are polynomials in n of degrees 3, 6, 9, so P has degree 22.
    Substituting n = m + 6 makes every one of its 23 coefficients nonnegative,
    hence P >= 0 for m >= 0.  QED

This file carries out the substitution exactly and reports the coefficient signs --
the proof is the argument above, this is the check on its one computation.  The
e_i are obtained by exact Lagrange interpolation and verified against the
reference `E2_list` before use, so the polynomials are not taken on trust either.

Run: python lab/conjecture_B_t1.py -> results/conjecture_B_t1.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def interpolate(deg: int, value) -> fmpq_poly:
    """Exact Lagrange interpolation of a polynomial of known degree."""
    xs = list(range(4, 4 + deg + 1))
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


def main() -> int:
    t0 = time.time()
    e1 = interpolate(3, lambda n: E2_list(n, 3)[1])
    e2 = interpolate(6, lambda n: E2_list(n, 3)[2])
    e3 = interpolate(9, lambda n: E2_list(n, 3)[3])

    checked = 0
    for n in range(5, 60):
        E = E2_list(n, 3)
        assert e1(fmpq(n)) == fmpq(E[1]) and e2(fmpq(n)) == fmpq(E[2]) and e3(fmpq(n)) == fmpq(E[3])
        checked += 1

    N = fmpq_poly([-1, 1])  # N = n - 1
    P = e2 * e2 * e2 * 8 * (N**4) * (N - 1) * (N - 2) - e1 * e1 * e1 * e3 * 6 * ((N * (N - 1)) ** 3)
    shifted = P(fmpq_poly([6, 1]))  # n = m + 6
    coeffs = [shifted[i] for i in range(shifted.degree() + 1)]
    negative = [i for i, c in enumerate(coeffs) if c < 0]

    direct_bad = 0
    for n in range(6, 70):
        E = E2_list(n, 3)
        from math import comb

        p1 = fmpq(E[1], comb(n - 1, 1))
        p2 = fmpq(E[2], comb(n - 1, 2))
        p3 = fmpq(E[3], comb(n - 1, 3))
        direct_bad += p2**3 < p1**3 * p3

    out = {
        "theorem": "(B) at t = 1: p_2^3 p_0 >= p_1^3 p_3 for n >= 6",
        "status": "PROVED; this file checks the computation the proof turns on",
        "e_polynomials_verified_against_reference_at_n": checked,
        "numerator_degree": P.degree(),
        "coefficients_after_n_eq_m_plus_6": len(coeffs),
        "negative_coefficients": len(negative),
        "direct_check_failures_n_6_to_69": direct_bad,
        "why_this_case": "the slack in (B) is smallest at t = 1 -- ratio 1.0195 at n = 10 "
        "down to 1.00023 at n = 69 -- so this is the case any proof must survive",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "conjecture_B_t1.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"numerator degree {P.degree()}, {len(coeffs)} coefficients after n = m+6, "
        f"{len(negative)} negative; direct check failures {direct_bad}"
    )
    return 0 if not negative and not direct_bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
