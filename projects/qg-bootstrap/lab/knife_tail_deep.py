"""Knife-j theorem, stages 2+3: shallow m-tail and deep water. KNIFE_J=4.

P_j := (-1)^{j-1} B~_j where B~_j is the bracket with the i=0 factorial
divided out: weights become Pochhammer POLYNOMIALS in m:
  w~_i = prod_{q=1}^{2i} (2n-2j+q) / (i! 2^i),  n = m+3.
E_{2t}(n) enters as an exact polynomial in m (degree 3t), built by
interpolation and VERIFIED on extra points.

Stage SHALLOW-TAIL: branches k=3..45, m = 41+v (v>=0):
  P_j > 0 on D in [4, T_k(lam)] via 3-var certificates (v, u, w).
Stage DEEP-FIXED: m = j-2..40 fixed, lam = 26+x (x>=0 unbounded):
  P_j > 0 on D in [4, (12+4sqrt3)lam] via (x, u) certificates over Q(sqrt3).
Stage DEEP-TAIL: m = 41+v, lam = 26+x:
  P_j > 0 on same interval via (v, x, u) certificates over Q(sqrt3).
Combined with knife_proof.py stage 1 and Lemma L1 (envelope <= asymptote,
j-free, proven in blade_proof.py), exit 0 across all stages = the full
knife-j theorem: a_{n,2n-2j} >= 0 everywhere in D <= min_k T_k(lam).
Artifact: results/knife_tail_deep_j{J}.json
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))
m, v, w, u, x = sp.symbols('m v w u x', nonnegative=True)
r3 = sp.sqrt(3)


def e_doubled_int(n: int):
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


def E_poly_m(t: int):
    """E_{2t}(n=m+3) как точный полином от m (deg 3t) + верификация."""
    deg = 3 * t
    pts = [(mm, e_doubled_int(mm + 3)[t]) for mm in range(1, deg + 5)]
    poly = sp.expand(sp.interpolate(pts[:deg + 1], m))
    for mm, val in pts[deg + 1:]:
        assert poly.subs(m, mm) == val, f"E_poly_m fail t={t} m={mm}"
    return poly


EPOLY = {t: E_poly_m(t) for t in range(J)}


def P_sym(lam_expr, D_expr, m_expr):
    """(-1)^{j-1} B~_j с полиномиальными весами, символьный m."""
    n = m_expr + 3
    c = 4 * n - 4 * J - 1
    s = lam_expr + n - 1
    B = sp.Integer(0)
    for i in range(J):
        poch = sp.prod(2 * n - 2 * J + q for q in range(1, 2 * i + 1))
        wgt = poch / (sp.factorial(i) * 2 ** i)
        tail = sp.prod(D_expr + c + 2 * k for k in range(i, J - 1))
        Et = EPOLY[J - 1 - i].subs(m, m_expr)
        B += (-1) ** i * Et * wgt * s ** (2 * i) * tail
    return sp.expand(B * (-1) ** (J - 1))


def certify(expr, gens, tag, log):
    e2 = sp.expand(sp.fraction(sp.together(expr))[0])
    P = sp.Poly(e2, *gens)
    bad = 0
    for mon, cc in P.terms():
        cc = sp.expand(cc)
        if cc.has(r3):
            a = cc.coeff(r3, 0)
            b = cc.coeff(r3, 1)
            okc = (a >= 0 and b >= 0) or \
                  (a >= 0 and b < 0 and a ** 2 >= 3 * b ** 2) or \
                  (a < 0 and b >= 0 and 3 * b ** 2 >= a ** 2)
        else:
            okc = cc >= 0
        if not okc:
            bad += 1
    log.append({"cell": tag, "mono": len(P.terms()), "bad": bad})
    return bad == 0


def bernstein_in_D(P_of_D, D_var, lo, hi):
    """P (полином deg d по D) на [lo, hi]: коэффициенты Бернштейна.
    Положительность всех b_i => положительность P на интервале."""
    th = sp.Symbol('theta')
    p = sp.expand(P_of_D.subs(D_var, lo + (hi - lo) * th))
    pp = sp.Poly(p, th)
    d = pp.degree()
    cs = [pp.coeff_monomial(th ** q) for q in range(d + 1)]
    bs = []
    for i in range(d + 1):
        b = sp.Integer(0)
        for q in range(i + 1):
            b += sp.binomial(i, q) / sp.binomial(d, q) * cs[q]
        bs.append(sp.together(b))
    return bs


def bisect_t(builder, a, b, depth, gens, tag, log):
    """builder(a,b) -> список выражений (Бернштейн-коэффициенты);
    все должны быть положительны."""
    exprs = builder(a, b)
    if all(certify(e, gens, f"{tag}", log) for e in exprs):
        return True
    if depth == 0:
        return False
    mid = (a + b) / 2
    return (bisect_t(builder, a, mid, depth - 1, gens, tag, log) and
            bisect_t(builder, mid, b, depth - 1, gens, tag, log))


def main() -> int:
    t0 = time.time()
    log = []
    ok = True

    # ---- SHALLOW-TAIL: m = 41+v ----
    for kk in range(3, 46):
        if kk == 3:
            mu_lo, mu_hi = sp.Rational(1, 1000), sp.Rational(2, 3)
        else:
            mu_lo = sp.Rational(3, 5) * (kk - sp.Rational(5, 2))
            mu_hi = sp.Rational(3, 5) * (kk - sp.Rational(3, 2))
            if kk == 4:
                mu_lo = sp.Rational(2, 3)

        D0 = sp.Symbol('D0')

        def build(a, b, kk=kk):
            lam_e = a + (b - a) * (w / (1 + w))
            Tk = (sp.Rational(3 * (2 * kk - 3), kk * (kk - 2))
                  * (lam_e ** 2 + (2 * kk - 2) * lam_e + 1) + 2 * kk)
            P = P_sym(lam_e, D0, 41 + v)
            return bernstein_in_D(P, D0, sp.Integer(4), Tk)

        got = bisect_t(build, mu_lo, mu_hi, 4, (v, w),
                       f"stail_k{kk}", log)
        ok &= got
        print(f"shallow-tail k={kk}: {'OK' if got else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    # ---- DEEP-FIXED: m = J-2..40, lam = 26+x ----
    D_hi = (12 + 4 * r3) * (26 + x)
    D0 = sp.Symbol('D0')
    deep_fixed_ok = True
    for mv in range(max(1, J - 2), 41):
        P = P_sym(26 + x, D0, sp.Integer(mv))
        bs = bernstein_in_D(P, D0, sp.Integer(4), D_hi)
        got = all(certify(e, (x,), f"deep_m{mv}", log) for e in bs)
        deep_fixed_ok &= got
        if not got:
            print(f"  deep FAIL m={mv}", flush=True)
    ok &= deep_fixed_ok
    print(f"deep-fixed m<{41}: {'OK' if deep_fixed_ok else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    # ---- DEEP-TAIL: m = 41+v ----
    P = P_sym(26 + x, D0, 41 + v)
    bs = bernstein_in_D(P, D0, sp.Integer(4), D_hi)
    got = all(certify(e, (v, x), "deep_tail", log) for e in bs)
    ok &= got
    print(f"deep-tail: {'OK' if got else 'FAIL'} ({time.time()-t0:.0f}s)",
          flush=True)

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"j": J, "all_certified": bool(ok), "cells": len(log),
           "stages": "shallow-tail(m>=41) + deep-fixed + deep-tail",
           "command": f"KNIFE_J={J} python lab/knife_tail_deep.py",
           "git": git, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"knife_tail_deep_j{J}.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(("ALL CERTIFIED" if ok else "INCOMPLETE") + f" cells={len(log)}",
          flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
