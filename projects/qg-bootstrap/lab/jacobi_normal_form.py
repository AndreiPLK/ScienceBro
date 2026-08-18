"""THE JACOBI NORMAL FORM: the whole theorem reduced to the sign of ONE number.

Route (each step exact, and the module CHECKS itself against the already
verified value rather than trusting the derivation):

1. Hhat is an m-th derivative. With m = n - j and
       F(u) = u^{n-1} G2(1/(s^2 u)) = SUM_t (-1)^t E_2t(n) s^{-2t} u^{n-1-t},
   differentiating m times multiplies term t by the falling factorial
   (n-1-t)(n-2-t)...(n-m-t) = prod_{i=j}^{n-1} (i-t) = Q(t), so

       Hhat(u) = d^m/du^m F(u)                                   (identity 1)

   -- one line of term-by-term differentiation, no numerics needed.

2. F is NONNEGATIVE on u > 0. G2(x) = prod_a (1 - a^2 x)^2 is a square, so
   F(u) = u^{n-1-2K} prod_a (s^2 u - a^2)^2 / s^{4K} >= 0 with K = |S_n|, and
   F is a genuine polynomial because deg G2 = 2*floor((n-1)/2) <= n-1.

3. Integrating by parts m times and using Rodrigues,
       d^m/du^m [ u^{p} (1-u)^{Q} ] = c_m u^{alpha}(1-u)^{beta}
                                      P_m^{(alpha,beta)}(1-2u),
   with alpha = p - m = -1/2 and beta = Q - m = D/2 - 2 -- exactly the two
   exponents of the problem. So

       I = (-1)^m c_m INT_0^1 F(u) u^{-1/2}(1-u)^{D/2-2}
                              P_m^{(-1/2, D/2-2)}(1-2u) du .        (form 3)

4. THE STEP THAT MAKES IT ONE NUMBER. F is a polynomial of degree n-1, so
   expand it in the Jacobi basis: orthogonality kills every term except k = m,
   and the sign of I is the sign of the SINGLE Jacobi coefficient f_m:

       sign I = (-1)^m * sign f_m .

   The grand theorem "every knife is positive" therefore becomes: the m-th
   Jacobi coefficient of an explicit nonnegative polynomial alternates in sign
   with m. One rational number per (j, n, lam, D).

Everything is computed with Fractions through Pochhammer ratios, so the only
transcendental factor is the common B(alpha+1, beta+1) > 0, which cannot change
a sign.

VALIDATION (this is the point of the module): the sign produced here is compared
against keystone_beta.J_exact, whose sign is already known to equal sign I. A
single mismatch means the derivation above is wrong, and the module says so.

Run: python lab/jacobi_normal_form.py
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_exact  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def poch(a: F, k: int) -> F:
    """Rising factorial (a)_k, exact."""
    v = F(1)
    for i in range(k):
        v *= a + i
    return v


def F_coeffs(n: int, lam: F) -> list[F]:
    """Ascending coefficients of F(u) = u^{n-1} G2(1/(s^2 u)), s = lam + n - 1.

    F_l = (-1)^{n-1-l} E_{2(n-1-l)} s^{-2(n-1-l)}.
    """
    e = e_doubled_int(n)
    s = F(lam) + n - 1
    out = [F(0)] * n
    for t in range(min(len(e), n)):
        out[n - 1 - t] = F((-1) ** t) * F(e[t]) / s ** (2 * t)
    return out


def jacobi_moment(j: int, n: int, lam: F, D: F) -> F:
    """INT_0^1 F(u) u^alpha (1-u)^beta P_m^{(alpha,beta)}(1-2u) du,
    divided by the positive constant B(alpha+1, beta+1). Exact rational.

    Uses P_m^{(a,b)}(1-2u) = ((a+1)_m/m!) * 2F1(-m, m+a+b+1; a+1; u) and
    INT_0^1 u^{a+q}(1-u)^b du / B(a+1,b+1) = (a+1)_q / (a+b+2)_q.
    """
    m = n - j
    a, b = F(-1, 2), F(D, 2) - 2
    Fc = F_coeffs(n, lam)
    pref = poch(a + 1, m) / F(_fact(m))
    tot = F(0)
    for k in range(m + 1):
        ck = poch(F(-m), k) * poch(F(m) + a + b + 1, k) / (poch(a + 1, k) * F(_fact(k)))
        if ck == 0:
            continue
        inner = F(0)
        for lpow, fl in enumerate(Fc):
            if fl == 0:
                continue
            q = k + lpow
            inner += fl * poch(a + 1, q) / poch(a + b + 2, q)
        tot += ck * inner
    return pref * tot


def _fact(k: int) -> int:
    v = 1
    for i in range(2, k + 1):
        v *= i
    return v


def sign_of(x: F) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def main() -> int:
    t0 = time.time()
    checks, bad = 0, []
    rows = []
    for n in range(6, 21):
        for j in range(2, n + 1):
            m = n - j
            for lam in (F(1, 2), F(1), F(3), F(7), F(26)):
                for D in (F(5), F(6), F(8), F(11), F(26)):
                    jm = jacobi_moment(j, n, lam, D)
                    got = sign_of(F(-1) ** m * jm)
                    want = sign_of(J_exact(j, n, lam, D))
                    checks += 1
                    if got != want:
                        bad.append(
                            {
                                "j": j,
                                "n": n,
                                "lam": str(lam),
                                "D": str(D),
                                "m": m,
                                "normal_form_sign": got,
                                "exact_sign": want,
                            }
                        )
                    if j in (2, n // 2, n) and lam == F(1) and D == F(6):
                        rows.append(
                            {
                                "j": j,
                                "n": n,
                                "m": m,
                                "sign_jacobi_coefficient": sign_of(jm),
                                "expected_(-1)^m": (-1) ** m,
                                "sign_I": want,
                            }
                        )
    print(f"  checks: {checks}, mismatches: {len(bad)}", flush=True)
    for r in bad[:8]:
        print("   MISMATCH", r, flush=True)
    out = {
        "claim": "sign I = (-1)^m * sign of the m-th Jacobi coefficient of the"
        " nonnegative polynomial F(u) = u^{n-1} G2(1/(s^2 u)),"
        " alpha = -1/2, beta = D/2 - 2, m = n - j",
        "why_it_matters": "F is a polynomial of degree n-1, so orthogonality"
        " leaves exactly ONE coefficient: the whole"
        " four-parameter positivity question becomes the sign"
        " of a single rational number per cell",
        "checks": checks,
        "mismatches": bad,
        "sample_rows": rows[:40],
        "command": "python lab/jacobi_normal_form.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "jacobi_normal_form.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/jacobi_normal_form.json", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())


def M_closed(q: int, m: int, D: F) -> F:
    """INT u^q w P_m du / B(alpha+1, beta+1), in CLOSED FORM.

    The k-sum in `jacobi_moment` is a terminating 3F2 at unit argument whose
    parameters are Saalschutzian (1 + sum of numerator parameters = sum of
    denominator parameters -- checked by hand and then on 432 exact cells), so
    Saalschutz's theorem collapses it to a product. Orthogonality falls out for
    free: the factor (-q)_m vanishes whenever m > q.
    """
    a, b = F(-1, 2), F(D, 2) - 2
    den = poch(a + 1, m) * poch(F(-m) - b - a - q - 1, m)
    if den == 0:
        return F(0)
    return (
        (poch(a + 1, m) / F(_fact(m)))
        * (poch(a + 1, q) / poch(a + b + 2, q))
        * poch(F(-m) - b, m)
        * poch(F(-q), m)
        / den
    )


def jacobi_coeff_fast(j: int, n: int, lam: F, D: F) -> F:
    """The m-th Jacobi coefficient (m = n - j) as a sum of exactly j terms.

    Orthogonality kills every power below m, so knife j costs j terms rather
    than the m-term k-sum of `jacobi_moment`. For a whole level that is O(n^2)
    products instead of O(n^3), which is what makes level-wide sweeps possible.
    Verified against `jacobi_moment` in `self_check_fast`.
    """
    m = n - j
    Fc = F_coeffs(n, lam)
    tot = F(0)
    for q in range(m, len(Fc)):
        if Fc[q]:
            tot += Fc[q] * M_closed(q, m, D)
    return tot


def self_check_fast(verbose: bool = True) -> int:
    """The fast path must agree EXACTLY with the slow one, or it is worthless."""
    bad = 0
    checked = 0
    for n in range(5, 16):
        for j in range(2, n + 1):
            for lam in (F(1, 2), F(1), F(7)):
                for D in (F(4), F(6), F(11)):
                    checked += 1
                    if jacobi_coeff_fast(j, n, lam, D) != jacobi_moment(j, n, lam, D):
                        bad += 1
                        if verbose and bad <= 5:
                            print(f"   MISMATCH j={j} n={n} lam={lam} D={D}")
    if verbose:
        print(f"  fast vs slow: {checked} exact comparisons, {bad} mismatches")
    return bad
