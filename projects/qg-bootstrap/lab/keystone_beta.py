"""KEYSTONE CANDIDATE: the bracket as a single Beta-weighted integral.

Chain (each step exact algebra, verified numerically below):

1. Closed form (already verified, chr_closed_form.json):
       P_j = c0 * SUM_{t=0}^{j-1} (-1)^t E_2t(n) * M1_t * M2_t
       M1_t = (1-j)_t/(1-n)_t = C(j-1,t)/C(n-1,t)
       M2_t = (1-R)_t/((3/2-n)_t s^{2t})

2. M1 IS A POLYNOMIAL IN t (this is the new observation):
       M1_t = (j-1)!/(n-1)! * Q(t),   Q(t) = prod_{i=j}^{n-1} (i - t)
   so the j-truncation of the sum is NOT a separate condition: Q vanishes
   at t = j..n-1, and the kernel's degree is 2*floor((n-1)/2) <= n-1, so
   every surviving t is automatically < j.

3. M2 IS A STIELTJES MOMENT SEQUENCE with an explicit Beta density.
   With alpha = R-1, beta = n-3/2 (alpha > beta > 0 in the whole canyon):
       M2_t * s^{2t} = Gamma(a+1)Gamma(b+1-t)/(Gamma(a+1-t)Gamma(b+1))
                     = Cst * INT_0^1 u^{beta-t} (1-u)^{alpha-beta-1} du
   valid for t < beta+1 = n-1/2, i.e. for every t <= j-1 (since j <= n).

=> P_j = (positive prefactor) * I,

       I(n, j, lam; D) = INT_0^1 Hhat(u) u^p (1-u)^Q du
       Hhat(u)  = SUM_{t=0}^{j-1} (-1)^t E_2t(n) Q(t) s^{-2t} u^{j-1-t}
       p        = n - j - 1/2                    (D-free)
       Q        = D/2 + n - j - 2                (the ONLY place D enters)

THE POINT: Hhat is D-FREE. The dimension D only slides the exponent of
(1-u), i.e. it only moves where the positive weight sits. Large D pushes
the weight to u -> 0 (where Hhat has the sign of its lowest coefficient);
small D spreads it over (0,1). That is exactly the mechanism behind the
kill windows, and it turns the grand theorem into ONE univariate question.

Run: python lab/keystone_beta.py -> results/keystone_beta.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chr_closed_form import P_closed, poch  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def Qpoly_val(j: int, n: int, t: int) -> int:
    """Q(t) = prod_{i=j}^{n-1} (i - t), exact integer."""
    v = 1
    for i in range(j, n):
        v *= (i - t)
    return v


def Hhat_coeffs(j: int, n: int, lam: Fraction) -> list[Fraction]:
    """Coefficients of Hhat(u) by DESCENDING power u^{j-1} ... u^0.

    Hhat(u) = sum_t (-1)^t E_2t(n) Q(t) s^{-2t} u^{j-1-t}; entry k is the
    coefficient of u^{j-1-k} (k = t).  D-free by construction.
    """
    e = e_doubled_int(n)
    s = Fraction(lam) + n - 1
    out = []
    for t in range(j):
        et = Fraction(e[t]) if t < len(e) else Fraction(0)
        out.append((-1) ** t * et * Qpoly_val(j, n, t) / s ** (2 * t))
    return out


def J_exact(j: int, n: int, lam: Fraction, D: Fraction) -> Fraction:
    """EXACT rational value of I / B(p+1, Q+1) * prod_{i=0}^{j-2}(p+Q+2+i).

    Every Beta ratio is rational:
        B(p+1+m, Q+1)/B(p+1, Q+1) = prod_{i=0}^{m-1} (p+1+i)/(p+Q+2+i),
    so after clearing the common positive denominator the whole integral
    becomes a POLYNOMIAL in Q of degree j-1 with rational coefficients in
    (n, lam).  sign I = sign J because every cleared factor is positive.
    """
    coeffs = Hhat_coeffs(j, n, lam)
    p = Fraction(2 * (n - j) - 1, 2)           # n - j - 1/2
    Q = Fraction(D, 2) + n - j - 2
    tot = Fraction(0)
    for t, ct in enumerate(coeffs):            # power u^{j-1-t}
        m = j - 1 - t
        term = ct
        for i in range(m):                     # numerator of the Beta ratio
            term *= (p + 1 + i)
        for i in range(m, j - 1):              # cleared denominator factors
            term *= (p + Q + 2 + i)
        tot += term
    return tot


def J_poly_in_Q(j: int, n: int, lam: Fraction) -> list[Fraction]:
    """Coefficients of J as a polynomial in Q, ascending (degree j-1)."""
    coeffs = Hhat_coeffs(j, n, lam)
    p = Fraction(2 * (n - j) - 1, 2)
    poly = [Fraction(0)] * j
    for t, ct in enumerate(coeffs):
        m = j - 1 - t
        term = ct
        for i in range(m):
            term *= (p + 1 + i)
        cur = [term]                            # polynomial in Q
        for i in range(m, j - 1):               # multiply by (Q + p + 2 + i)
            shift = p + 2 + i
            new = [Fraction(0)] * (len(cur) + 1)
            for d, cd in enumerate(cur):
                new[d] += cd * shift
                new[d + 1] += cd
            cur = new
        for d, cd in enumerate(cur):
            poly[d] += cd
    return poly


def sign_changes(coeffs_desc: list[Fraction]) -> int:
    """Sign changes in the coefficient list (Descartes bound on (0, inf))."""
    sg = [1 if c > 0 else (-1 if c < 0 else 0) for c in coeffs_desc]
    sg = [x for x in sg if x]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)


def main() -> int:
    t0 = time.time()
    checks, mism, rows = 0, [], []
    for j in range(2, 22):
        for n in range(j + 1, j + 20, 3):
            for lam in (Fraction(1, 100), Fraction(1, 2), Fraction(3),
                        Fraction(26)):
                Th = T_hat(lam)
                s = Fraction(lam) + n - 1
                for f in (Fraction(0), Fraction(1, 2), Fraction(1),
                          Fraction(3)):
                    D = 4 + (Th - 4) * f
                    # --- exact algebra check: closed form == Q-form -------
                    e = e_doubled_int(n)
                    R = (D + Fraction(4 * n - 4 * j - 1)) / 2 + j - 1
                    c0 = (Fraction(factorial(2 * n - 2),
                                   factorial(j - 1) * 2 ** (j - 1))
                          * s ** (2 * (j - 1)))
                    tot = Fraction(0)
                    for t in range(j):
                        m2 = (poch(1 - R, t)
                              / (poch(Fraction(3, 2) - n, t) * s ** (2 * t)))
                        tot += ((-1) ** t * Fraction(e[t])
                                * Qpoly_val(j, n, t) * m2)
                    qform = c0 * Fraction(factorial(j - 1),
                                          factorial(n - 1)) * tot
                    ref = P_closed(j, n, lam, D)
                    checks += 1
                    if qform != ref:
                        mism.append({"kind": "Q-form", "j": j, "n": n,
                                     "lam": str(lam), "f": str(f)})
                    # --- integral representation: EXACT sign must agree ---
                    Jv = J_exact(j, n, lam, D)
                    checks += 1
                    if (Jv > 0) != (ref > 0):
                        mism.append({"kind": "sign", "j": j, "n": n,
                                     "lam": str(lam), "f": str(f),
                                     "J_pos": Jv > 0, "P_pos": ref > 0})
                    # J evaluated from its Q-polynomial must match J_exact
                    Qv = Fraction(D, 2) + n - j - 2
                    pol = J_poly_in_Q(j, n, lam)
                    val = sum(c * Qv ** d for d, c in enumerate(pol))
                    checks += 1
                    if val != Jv:
                        mism.append({"kind": "Qpoly", "j": j, "n": n,
                                     "lam": str(lam), "f": str(f)})
                    if f in (Fraction(0), Fraction(1)):
                        rows.append({
                            "j": j, "n": n, "lam": str(lam), "f": str(f),
                            "P_pos": ref > 0, "J_pos": Jv > 0,
                            "sign_changes_Hhat":
                                sign_changes(Hhat_coeffs(j, n, lam)),
                            "sign_changes_J_in_Q":
                                sign_changes(list(reversed(pol)))})
        print(f"  j={j} done ({time.time()-t0:.0f}s), "
              f"mismatches so far {len(mism)}", flush=True)

    sc = sorted({r["sign_changes_Hhat"] for r in rows})
    out = {"claim": "sign P_j = sign of a single Beta-weighted integral of a"
                    " D-FREE polynomial Hhat of degree j-1",
           "formula": {"I": "int_0^1 Hhat(u) u^p (1-u)^Q du",
                       "Hhat": "sum_t (-1)^t E_2t(n) Q(t) s^{-2t} u^{j-1-t}",
                       "Q_of_t": "prod_{i=j}^{n-1} (i-t)",
                       "p": "n - j - 1/2  (D-free)",
                       "Q_exp": "D/2 + n - j - 2  (only D-dependence)"},
           "exact_checks": checks, "mismatches": mism,
           "verified": not mism,
           "sign_changes_observed": sc,
           "rows": rows[:80],
           "command": "python lab/keystone_beta.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_beta.json").write_text(json.dumps(out, indent=1),
                                            encoding="utf-8")
    print(f"checks {checks}, mismatches {len(mism)}", flush=True)
    print(f"sign changes of Hhat observed: {sc}", flush=True)
    print("BETA REPRESENTATION " + ("VERIFIED" if not mism else "FAILED"),
          flush=True)
    return 0 if not mism else 1


if __name__ == "__main__":
    sys.exit(main())
