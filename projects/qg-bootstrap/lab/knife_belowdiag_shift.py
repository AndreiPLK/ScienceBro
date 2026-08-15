"""Knife-4 below-diagonal, THE SHIFT: give the tight sliver to the method
that already passed above the diagonal (interval 2D Bernstein), keep
Descartes-at-cap for the fat-margin far-below region.

Pieces:
 (ii)  band v in [K-6, K+4], K>=6 (K=6+K2): vsub = K2 + 10*sigma;
       interval Bernstein in (thL, th), then Bernstein in sigma,
       then exact root isolation in K2. All over Q(sqrt3).
 (iii) explicit K0=0..5: v in [0, K0+4]: vsub=(K0+4)*sigma; same chain,
       final coefficients rational numbers.
 (iv)  far below: v <= K-6 (K=6+K2, vsub = K2*sigma... covers [0, K2] =
       [0, K-6]): Descartes-at-cap (y-coefficients), margins are fat there.
Exit 0 iff all pieces certify. Artifact: results/knife4_belowdiag_shift.json
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
LAB = Path(__file__).resolve().parent
J = 4
ELEV = int(os.environ.get("BERN_ELEV", "6"))
m, v = sp.symbols('m v', nonnegative=True)
K2 = sp.Symbol('K2', nonnegative=True)
sig = sp.Symbol('sigma', nonnegative=True)
thL = sp.Symbol('thL', nonnegative=True)
th = sp.Symbol('theta', nonnegative=True)
yv = sp.Symbol('y', nonnegative=True)
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
    deg = 3 * t
    lo = max(1, t - 1)
    pts = [(mm, e_doubled_int(mm + 3)[t]) for mm in range(lo, lo + deg + 4)]
    poly = sp.expand(sp.interpolate(pts[:deg + 1], m))
    for mm, val in pts[deg + 1:]:
        assert poly.subs(m, mm) == val
    return poly


EPOLY = {t: E_poly_m(t) for t in range(J)}


def P_sym(lam_expr, D_expr, m_expr):
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


def bern1(expr, var, extra=0):
    pp = sp.Poly(sp.expand(expr), var)
    d0 = pp.degree()
    d = d0 + extra
    cs = [pp.coeff_monomial(var ** q) if q <= d0 else sp.Integer(0)
          for q in range(d + 1)]
    out = []
    for i2 in range(d + 1):
        b = sum(sp.binomial(i2, q) / sp.binomial(d, q) * cs[q]
                for q in range(min(i2, d0) + 1))
        out.append(sp.expand(b))
    return out


def bern2(expr, v1, v2, extra=0):
    out = []
    for b1_ in bern1(expr, v1, extra):
        out.extend(bern1(b1_, v2, extra))
    return out


def q3_parts_nonneg(cc):
    if not cc.has(r3):
        return cc >= 0 if not cc.free_symbols else None
    a = cc.coeff(r3, 0)
    b = cc.coeff(r3, 1)
    if not (a.free_symbols or b.free_symbols):
        if a >= 0 and b >= 0:
            return True
        if a >= 0 and b < 0:
            return bool(a ** 2 >= 3 * b ** 2)
        if a < 0 and b >= 0:
            return bool(3 * b ** 2 >= a ** 2)
        return False
    return None


def polyK_nonneg(c):
    """положительность на K2 >= 0: раздельно для рациональной и sqrt3-части"""
    def okpoly(e):
        e = sp.expand(e)
        if not e.free_symbols:
            return e >= 0
        P = sp.Poly(e, K2)
        if all(cc >= 0 for _, cc in P.terms()):
            return True
        if P.LC() < 0:
            return False
        return not [r for r in P.real_roots() if r >= 0]
    if c.has(r3):
        return okpoly(c.coeff(r3, 0)) and okpoly(c.coeff(r3, 1))
    return okpoly(c)


def cert_chain(P, has_K, tag, log):
    """P полином (thL, th, sigma[, K2]) над Q(sqrt3):
    Бернштейн (thL, th) с подъёмом -> Бернштейн sigma -> K2-изоляция."""
    for b2_ in bern2(P, thL, th, ELEV):
        for b3_ in bern1(b2_, sig, ELEV):
            if has_K:
                if not polyK_nonneg(b3_):
                    log.append({"cell": tag, "ok": False})
                    return False
            else:
                r = q3_parts_nonneg(sp.expand(b3_))
                if r is not True:
                    log.append({"cell": tag, "ok": False})
                    return False
    log.append({"cell": tag, "ok": True})
    return True


def bisect(builder, a, b, depth, has_K, tag, log):
    if cert_chain(builder(a, b), has_K, tag, log):
        return True
    if depth == 0:
        return False
    mid = (a + b) / 2
    return (bisect(builder, a, mid, depth - 1, has_K, tag, log) and
            bisect(builder, mid, b, depth - 1, has_K, tag, log))


def main() -> int:
    t0 = time.time()
    log = []
    ok = True

    # (ii) band: K = 6 + K2, v = K2 + 10*sigma  (v in [K-6, K+4])
    def build_band(a, b):
        tL = a + (b - a) * thL
        lam_c = (K2 + 6 + 45 + tL) * r3 / 3
        kk_c = K2 + 6 + 47
        Tk = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
              * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        D_c = 4 + (Tk - 4) * th
        P = P_sym(lam_c, D_c, 41 + K2 + 10 * sig)
        return sp.expand(sp.fraction(sp.together(P))[0])

    got = bisect(build_band, sp.Integer(0), sp.Integer(1), 5, True,
                 "band_K6plus", log)
    ok &= got
    print(f"(ii) band K>=6: {'OK' if got else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    # (iii) explicit K0 = 0..5: v = (K0+4)*sigma
    for K0 in range(0, 6):
        def build_k0(a, b, K0=K0):
            tL = a + (b - a) * thL
            lam_c = (sp.Integer(K0) + 45 + tL) * r3 / 3
            kk_c = sp.Integer(K0) + 47
            Tk = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                  * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
            D_c = 4 + (Tk - 4) * th
            P = P_sym(lam_c, D_c, 41 + (K0 + 4) * sig)
            return sp.expand(sp.fraction(sp.together(P))[0])

        got = bisect(build_k0, sp.Integer(0), sp.Integer(1), 5, False,
                     f"K{K0}", log)
        ok &= got
        print(f"(iii) K={K0}: {'OK' if got else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    # (iv) far below: K = 6 + K2, v = K2*sigma (v in [0, K-6]),
    #      Декарт у мыса: коэффициенты по y
    # (iv-v2) far below: v свободен, K2 = v + K3 (гарантирует v <= K-6),
    #          обе переменные по ортанту — как в победившем above-diagonal
    K3 = sp.Symbol('K3', nonnegative=True)

    def build_far(a, b):
        tL = a + (b - a) * thL
        Kc = v + K3
        lam_c = (Kc + 6 + 45 + tL) * r3 / 3
        kk_c = Kc + 6 + 47
        Tk = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
              * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        D_c = 4 + (Tk - 4) * th
        P = P_sym(lam_c, D_c, 41 + v)
        return sp.expand(sp.fraction(sp.together(P))[0])

    def cert_orthant2(P, tag):
        for b2_ in bern2(P, thL, th, ELEV):
            Pp = sp.Poly(sp.expand(b2_), v, K3)
            for _, cc in Pp.terms():
                r = q3_parts_nonneg(sp.expand(cc)) if cc.has(r3) else (cc >= 0)
                if r is not True:
                    log.append({"cell": tag, "ok": False})
                    return False
        log.append({"cell": tag, "ok": True})
        return True

    def bisect_far(a, b, depth):
        if cert_orthant2(build_far(a, b), "far_below_orthant"):
            return True
        if depth == 0:
            return False
        mid = (a + b) / 2
        return bisect_far(a, mid, depth - 1) and bisect_far(mid, b, depth - 1)

    MODE = os.environ.get("FAR_MODE", "orthant")
    if MODE == "compact4d":
        w1 = sp.Symbol('w1', nonnegative=True)
        w2 = sp.Symbol('w2', nonnegative=True)

        def build_far_c(a, b):
            tL = a + (b - a) * thL
            vv = 40 * w1 / (1 - w1 + sp.Rational(1, 1000))
            KK3 = 40 * w2 / (1 - w2 + sp.Rational(1, 1000))
            Kc = vv + KK3
            lam_c = (Kc + 6 + 45 + tL) * r3 / 3
            kk_c = Kc + 6 + 47
            Tk = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                  * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
            D_c = 4 + (Tk - 4) * th
            P = P_sym(lam_c, D_c, 41 + vv)
            return sp.expand(sp.fraction(sp.together(P))[0])

        def cert4(P, tag):
            for b1_ in bern2(P, thL, th, ELEV):
                for b2_ in bern2(b1_, w1, w2, ELEV):
                    rr = q3_parts_nonneg(sp.expand(b2_))
                    if rr is not True:
                        log.append({"cell": tag, "ok": False})
                        return False
            log.append({"cell": tag, "ok": True})
            return True

        def bisect_c(a, b, depth):
            if cert4(build_far_c(a, b), "far_compact4d"):
                return True
            if depth == 0:
                return False
            mid = (a + b) / 2
            return bisect_c(a, mid, depth-1) and bisect_c(mid, b, depth-1)

        got = bisect_c(sp.Integer(0), sp.Integer(1), 4)
    else:
        got = bisect_far(sp.Integer(0), sp.Integer(1), 5)
    ok &= got
    print(f"(iv) far below: {'OK' if got else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"all_certified": bool(ok), "cells": len(log), "elev": ELEV,
           "command": "python lab/knife_belowdiag_shift.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "knife4_belowdiag_shift.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(("BELOW-DIAGONAL CLOSED" if ok else "INCOMPLETE"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
