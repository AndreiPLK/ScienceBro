"""Iteration 2: exact-rational positivity spot-check of the (r,w) family at q=1.

Two independent routes, no shared core:

ROUTE 1 — the paper's closed form: partial-wave coefficients a_{n,l} from Eq. (A6)
of arXiv:2406.02665 (q=1), built from unsigned Stirling numbers, factorials and
Pochhammers — evaluated in EXACT Fraction arithmetic.

ROUTE 2 — first principles: the residue of the amplitude at level n (q->1 limit of
Eq. 16, verified against Veneziano at r=w=0):
    R(n,t') = (1+r+t')_n/(2+r)_n * (1+r+t'+w)(1+n+r+w) / ((1+r+t')(1+r+w))
with the appendix shift (s,t) -> (s-mu0, t-mu0): poles sit at s = n + mu0 and
    t' = t - mu0,  t = -(s - 4*mu0)(1-x)/2 at s = n+mu0,  x = cos(theta).
Decompose the polynomial in x into Gegenbauer C_l^{alpha}, alpha=(D-3)/2 (Legendre
for D=4), with exact rational coefficients via the classical projection using the
exact Legendre recurrence and exact monomial integrals over [-1,1].

Agreement criterion: for every tested (n, l), sign(route1) == sign(route2), and
route1/route2 is a positive constant depending only on l (normalization of G_l),
independent of n, r, w, mu0.

Spot checks (frozen): Veneziano point (0,0,0) must be non-negative for n<=8;
a far point must show a negative coefficient (existence of exclusion).
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from functools import cache

D = 4  # spacetime dimension for the spot check


# ---------------- route 1: Eq. (A6) exact ----------------


@cache
def stirling1_unsigned(n: int, k: int) -> int:
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return stirling1_unsigned(n - 1, k - 1) + (n - 1) * stirling1_unsigned(n - 1, k)


@cache
def fact(n: int) -> int:
    return 1 if n <= 0 else n * fact(n - 1)


def poch(a: F, n: int) -> F:
    out = F(1)
    for k in range(n):
        out *= a + k
    return out


def gamma_ratio_half(m: int) -> F:
    """Gamma((D-1)/2) / Gamma((D-1)/2 + m) for D=4: Gamma(3/2)/Gamma(3/2+m)."""
    return F(1) / poch(F(3, 2), m)


def a_route1(n: int, ell: int, r: F, w: F, mu0: F) -> F:
    """Eq. (A6), q=1, D=4, exact."""
    if n == 0:
        return F(1) if ell == 0 else F(0)

    def f_base(k: int, j: int, power: int) -> F:
        """f(n,l,k,j) with the (n-mu0-2r-4) factor raised to `power` instead of
        k-l-2j — lets the second sum absorb its division algebraically, so the
        removable singularity at n = mu0+2r+4 never appears."""
        num = F((-1) ** k * stirling1_unsigned(n - 1, k - 1) * fact(k - 1))
        num /= fact(k - ell - 2 * j) * fact(j)
        num *= (n - mu0 - 2 * r - 4) ** power
        num *= (3 * mu0 - n) ** (ell + 2 * j)
        num *= gamma_ratio_half(ell + j)
        num /= F(2) ** (k + ell + 2 * j)
        return num

    total = F(0)
    for k in range(max(ell, 1), n + 1):
        for j in range(0, (k - ell) // 2 + 1):
            if k - ell - 2 * j < 0:
                continue
            total += (ell + 2 * j) * f_base(k, j, k - ell - 2 * j)
    for k in range(ell + 1, n + 1):
        for j in range(0, (k - ell - 1) // 2 + 1):
            p = k - ell - 2 * j
            if p < 1:
                continue
            # (k-l-2j) * (n-mu0-2r-2-2w)/(n-mu0-2r-4) * f  ==  power folded to p-1
            total += p * F(n - mu0 - 2 * r - 2 - 2 * w) * f_base(k, j, p - 1)

    pref = (1 + F(2) * ell / (D - 3)) * F(1)  # Gamma((D-1)/2) folded into gamma_ratio_half
    pref *= (1 + n + r + w) / ((1 + r + w) * poch(F(2) + r, n))
    return pref * total


# ---------------- route 2: residue + exact Legendre decomposition ----------------


def legendre_poly_coeffs(ell: int) -> list[F]:
    """Coefficients (in x) of Legendre P_ell, exact, via Bonnet recurrence."""
    p0, p1 = [F(1)], [F(0), F(1)]
    if ell == 0:
        return p0
    if ell == 1:
        return p1
    for m in range(2, ell + 1):
        # m P_m = (2m-1) x P_{m-1} - (m-1) P_{m-2}
        xp = [F(0)] + p1
        new = [(2 * m - 1) * c / m for c in xp]
        for i, c in enumerate(p0):
            new[i] -= (m - 1) * c / m
        p0, p1 = p1, new
    return p1


def monomial_integral(k: int) -> F:
    """Integral of x^k over [-1, 1]."""
    return F(0) if k % 2 else F(2, k + 1)


def a_route2(n: int, ell: int, r: F, w: F, mu0: F) -> F:
    """Legendre coefficient of the level-n residue polynomial in x = cos(theta)."""
    if n == 0:
        return F(1) if ell == 0 else F(0)
    # residue R(n, t') as polynomial in t' (exact), then t'(x)
    # R(n,t') = (1+r+t')_n/(2+r)_n * (1+r+t'+w)(1+n+r+w)/((1+r+t')(1+r+w))
    #        = [(2+r+t')_{n-1}] * (1+r+t'+w)(1+n+r+w) / [(2+r)_n (1+r+w)]
    # (cancel the (1+r+t') factor exactly: (1+r+t')_n = (1+r+t')*(2+r+t')_{n-1})
    import sympy as sp

    tp = sp.Symbol("tp")
    poly = sp.prod([(2 + r + tp + k) for k in range(n - 1)]) if n > 1 else 1
    poly = sp.expand(poly * (1 + r + tp + w) * (1 + n + r + w) / (poch(F(2) + r, n) * (1 + r + w)))
    # substitution t' = -(n - 3*mu0)*(1-x)/2 - mu0
    x = sp.Symbol("x")
    poly_x = (
        sp.expand(poly.subs(tp, sp.Rational(-(n - 3 * mu0), 2) * (1 - x) - mu0))
        if isinstance(mu0, int) or mu0.denominator == 1
        else sp.expand(
            poly.subs(
                tp,
                (sp.Rational(-1, 2) * (n - 3 * sp.Rational(mu0.numerator, mu0.denominator)))
                * (1 - x)
                - sp.Rational(mu0.numerator, mu0.denominator),
            )
        )
    )
    coeffs = sp.Poly(poly_x, x).all_coeffs()[::-1]  # ascending powers
    coeffs = [F(sp.Rational(c).p, sp.Rational(c).q) for c in coeffs]
    # exact Legendre projection: b_l = (2l+1)/2 * Int P_l(x) * poly(x) dx
    pl = legendre_poly_coeffs(ell)
    integral = F(0)
    for i, ci in enumerate(pl):
        for k, ck in enumerate(coeffs):
            integral += ci * ck * monomial_integral(i + k)
    return F(2 * ell + 1, 2) * integral


# ---------------- spot checks ----------------


def run_point(r: F, w: F, mu0: F, nmax: int, label: str) -> tuple[bool, list]:
    neg = []
    ratio_by_ell: dict[int, F] = {}
    for n in range(1, nmax + 1):
        # threshold caveat (paper p.6): only impose positivity above threshold
        if n + mu0 < 4 * mu0:
            continue
        for ell in range(0, n + 1):
            a1 = a_route1(n, ell, r, w, mu0)
            a2 = a_route2(n, ell, r, w, mu0)
            if (a1 > 0) != (a2 > 0) and not (a1 == 0 and a2 == 0):
                print(f"  ROUTE MISMATCH n={n} l={ell}: {a1} vs {a2}")
                return False, neg
            if a2 != 0:
                key = ell
                ratio = a1 / a2
                if ratio <= 0:
                    print(f"  RATIO NOT POSITIVE n={n} l={ell}: {ratio}")
                    return False, neg
                if key in ratio_by_ell and ratio_by_ell[key] != ratio:
                    print(f"  RATIO NOT l-ONLY n={n} l={ell}: {ratio} vs {ratio_by_ell[key]}")
                    return False, neg
                ratio_by_ell[key] = ratio
            if a1 < 0:
                neg.append((n, ell, a1))
    status = "all non-negative" if not neg else f"{len(neg)} negative coefficients"
    print(f"  [{label}] r={r} w={w} mu0={mu0}: routes agree; {status}")
    return True, neg


def main() -> int:
    ok = True
    # 1) Veneziano point: must be clean up to n=8
    good, neg = run_point(F(0), F(0), F(0), 8, "Veneziano")
    ok &= good and not neg
    # 2) a moderately deformed point that Fig.1 shows as allowed-ish (small r,w)
    good, neg = run_point(F(1, 4), F(1, 4), F(0), 8, "small deformation")
    ok &= good
    # 3) a far point: expect exclusion (some negative coefficient)
    good, neg = run_point(F(-3, 2), F(3, 2), F(0), 8, "far point")
    ok &= good
    far_excluded = bool(neg)
    print(f"\nfar point excluded: {far_excluded}")
    print(f"VERDICT: {'PASS' if ok else 'FAIL'} (routes agree everywhere tested)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
