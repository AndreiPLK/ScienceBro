"""Knife-5 far-below via FACTOR-THEN-CERTIFY (the knife-4 winning method).

P_5(T_cap - y): all 5 y-coefficients factored over Q(sqrt3); each factor's
monomials sign-checked exactly. All manifestly positive => P > 0 on the
whole ray D <= T_cap in the far-below region (v free, K = v + K3 + 6).
Artifact: results/knife_farbelow_factored.json
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

RES = Path(__file__).resolve().parents[1] / "results"
import os

J = int(os.environ.get("KNIFE_J", "5"))
m, v = sp.symbols("m v", nonnegative=True)
K3 = sp.Symbol("K3", nonnegative=True)
thL = sp.Symbol("thL", nonnegative=True)
yv = sp.Symbol("y", nonnegative=True)
r3 = sp.sqrt(3)


def e_doubled_int(n):
    poly = [1]
    for k in range(1, n):
        r = n - 2 * k
        for _ in range(2):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] += c * r
            poly = new
    return [abs(poly[2 * t]) for t in range(len(poly) // 2 + 1)]


def E_poly_m(t):
    deg = 3 * t
    lo = max(1, t - 1)
    pts = [(mm, e_doubled_int(mm + 3)[t]) for mm in range(lo, lo + deg + 4)]
    poly = sp.expand(sp.interpolate(pts[: deg + 1], m))
    for mm, val in pts[deg + 1 :]:
        assert poly.subs(m, mm) == val
    return poly


print(f"[farbelow j={J}] building E-polynomials...", flush=True)
EPOLY = {t: E_poly_m(t) for t in range(J)}
print(f"[farbelow j={J}] E done; building P (long, silent)...", flush=True)


def P_sym(lam_expr, D_expr, m_expr):
    n = m_expr + 3
    c = 4 * n - 4 * J - 1
    s = lam_expr + n - 1
    B = sp.Integer(0)
    for i in range(J):
        poch = sp.prod(2 * n - 2 * J + q for q in range(1, 2 * i + 1))
        wgt = poch / (sp.factorial(i) * 2**i)
        tail = sp.prod(D_expr + c + 2 * k for k in range(i, J - 1))
        Et = EPOLY[J - 1 - i].subs(m, m_expr)
        B += (-1) ** i * Et * wgt * s ** (2 * i) * tail
    return sp.expand(B * (-1) ** (J - 1))


def sign_q3(cc):
    a = cc.coeff(r3, 0)
    b = cc.coeff(r3, 1)
    if a >= 0 and b >= 0:
        return 1 if (a > 0 or b > 0) else 0
    if a <= 0 and b <= 0:
        return -1
    if a >= 0:
        return 1 if a**2 > 3 * b**2 else (-1 if a**2 < 3 * b**2 else 0)
    return -1 if a**2 > 3 * b**2 else (1 if a**2 < 3 * b**2 else 0)


def factor_all_positive(expr, gens, name, t0):
    factors = sp.factor_list(sp.factor(expr))
    content = sp.expand(factors[0])
    cs = sign_q3(content) if content.has(r3) else (1 if content > 0 else (-1 if content < 0 else 0))
    total_neg = 0
    for f, e in factors[1]:
        P = sp.Poly(sp.expand(f), *gens)
        neg = sum(
            1
            for _, cc in P.terms()
            if (sign_q3(sp.expand(cc)) if cc.has(r3) else (1 if cc > 0 else -1)) < 0
        )
        if neg == len(P.terms()):
            total_neg += e
        elif neg > 0:
            print(f"  {name}: MIXED factor (neg {neg}/{len(P.terms())})", flush=True)
            return False
    ok = cs * (-1) ** total_neg > 0
    print(f"  {name}: {'OK' if ok else 'BAD SIGN'} ({time.time() - t0:.0f}s)", flush=True)
    return ok


def main() -> int:
    t0 = time.time()
    Kc = v + K3
    lam_c = (Kc + 6 + 45 + thL) * r3 / 3
    kk_c = Kc + 6 + 47
    Tk = (
        3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2)) * (lam_c**2 + (2 * kk_c - 2) * lam_c + 1)
        + 2 * kk_c
    )
    P = P_sym(lam_c, Tk - yv, 41 + v)
    P = sp.expand(sp.fraction(sp.together(P))[0])
    coeffs = sp.Poly(P, yv).all_coeffs()[::-1]
    print(f"y-coefficients: {len(coeffs)}", flush=True)
    allok = True
    for k2, c_ in enumerate(coeffs):
        allok &= factor_all_positive(sp.expand(c_), (thL, v, K3), f"c{k2}", t0)
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    json.dump(
        {
            "j": J,
            "far_below_factored": bool(allok),
            "command": f"KNIFE_J={J} python lab/knife_farbelow_factored.py",
            "git": git,
            "runtime_s": round(time.time() - t0, 1),
        },
        open(RES / f"knife{J}_farbelow_factored.json", "w"),
        indent=1,
    )
    print(f"FAR-BELOW(j={J}) " + ("CLOSED" if allok else "OPEN"), flush=True)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
