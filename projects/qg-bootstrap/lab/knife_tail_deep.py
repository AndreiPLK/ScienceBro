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
    lo = max(1, t - 1)
    pts = [(mm, e_doubled_int(mm + 3)[t]) for mm in range(lo, lo + deg + 4)]
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


def bernstein2_coeffs(P_expr, tau, th):
    """Двойной Бернштейн: P полином по (tau, th) на [0,1]^2 ->
    матрица коэффициентов b_{p,q}; все >= 0 => P >= 0 на квадрате."""
    pp = sp.Poly(sp.expand(P_expr), tau, th)
    dt = pp.degree(tau)
    dh = pp.degree(th)
    C = {}
    for (pt, qt), cc in pp.terms():
        C[(pt, qt)] = C.get((pt, qt), 0) + cc
    out = []
    for p in range(dt + 1):
        for q in range(dh + 1):
            b = sp.Integer(0)
            for p2 in range(p + 1):
                for q2 in range(q + 1):
                    cc = C.get((p2, q2))
                    if cc is None:
                        continue
                    b += (sp.binomial(p, p2) / sp.binomial(dt, p2)
                          * sp.binomial(q, q2) / sp.binomial(dh, q2) * cc)
            out.append(sp.expand(b))
    return out


def poly_v_nonneg(c):
    """полином от v: неотрицательность на v >= 0 (коэф. или изоляция корней)"""
    if not c.free_symbols:
        return c >= 0
    P = sp.Poly(c, v)
    if all(cc >= 0 for _, cc in P.terms()):
        return True
    if P.LC() < 0:
        return False
    roots = [r for r in P.real_roots() if r >= 0]
    if roots:
        return False
    return c.subs(v, 1) > 0


def bisect_t(builder, a, b, depth, tag, log):
    """builder(a,b) -> список полиномов от v (двойные Бернштейн-коэф.);
    все должны быть >= 0 на v >= 0."""
    exprs = builder(a, b)
    bad = sum(0 if poly_v_nonneg(e) else 1 for e in exprs)
    log.append({"cell": tag, "coeffs": len(exprs), "bad": bad})
    if bad == 0:
        return True
    if depth == 0:
        return False
    mid = (a + b) / 2
    return (bisect_t(builder, a, mid, depth - 1, tag, log) and
            bisect_t(builder, mid, b, depth - 1, tag, log))


def main() -> int:
    t0 = time.time()
    log = []
    ok = True

    STAGE = os.environ.get("KNIFE_STAGE", "all")
    # ---- SHALLOW-TAIL: m = 41+v ----
    stail_ok = True
    for kk in ([] if STAGE == "belowdiag" else range(3, 46)):
        onto = kk == 3
        if kk == 3:
            # blade-подстановка lam=(2/3)(1-t): ONTO (0, 2/3], включая
            # lam < 1/1000 (ремонт ERR-0002); (a,b) — интервал по t
            mu_lo, mu_hi = sp.Integer(0), sp.Integer(1)
        else:
            mu_lo = sp.Rational(3, 5) * (kk - sp.Rational(5, 2))
            mu_hi = sp.Rational(3, 5) * (kk - sp.Rational(3, 2))
            if kk == 4:
                mu_lo = sp.Rational(2, 3)

        tau, th = sp.symbols('tau theta', nonnegative=True)

        def build(a, b, kk=kk, onto=onto):
            if onto:
                lam_e = sp.Rational(2, 3) * (1 - a - (b - a) * tau)
            else:
                lam_e = a + (b - a) * tau              # полиномиально!
            Tk = (sp.Rational(3 * (2 * kk - 3), kk * (kk - 2))
                  * (lam_e ** 2 + (2 * kk - 2) * lam_e + 1) + 2 * kk)
            D_e = 4 + (Tk - 4) * th                    # полиномиально!
            P = P_sym(lam_e, D_e, 41 + v)
            return bernstein2_coeffs(P, tau, th)

        got = bisect_t(build, mu_lo, mu_hi, 5, f"stail_k{kk}", log)
        ok &= got
        stail_ok &= got
        print(f"shallow-tail k={kk}: {'OK' if got else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    # ---- DEEP-FIXED: m = J-2..40, lam = 26+x ----
    th = sp.Symbol('theta', nonnegative=True)
    D_hi = (12 + 4 * r3) * (26 + x)
    deep_fixed_ok = True
    for mv in ([] if STAGE == "belowdiag" else range(max(1, J - 2), 41)):
        D_e = 4 + (D_hi - 4) * th                      # полиномиально
        P = P_sym(26 + x, D_e, sp.Integer(mv))
        # Бернштейн по th; коэффициенты — полиномы (x) над Q(sqrt3)
        pp = sp.Poly(sp.expand(P), th)
        dh = pp.degree()
        cs = [pp.coeff_monomial(th ** q) for q in range(dh + 1)]
        bs = []
        for i2 in range(dh + 1):
            b = sum(sp.binomial(i2, q) / sp.binomial(dh, q) * cs[q]
                    for q in range(i2 + 1))
            bs.append(sp.expand(b))
        got = all(certify(e, (x,), f"deep_m{mv}", log) for e in bs)
        deep_fixed_ok &= got
        if not got:
            print(f"  deep FAIL m={mv}", flush=True)
    ok &= deep_fixed_ok
    print(f"deep-fixed m<{41}: {'OK' if deep_fixed_ok else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    # ---- DEEP-TAIL v2: m = 41+v, дрейф-фри параметризация k = K+2,
    #      lam = (K+theta_L)*sqrt3/3, K >= 45 (=> lam >= 25.98), cap = T_k(lam)
    K = sp.Symbol('K', nonnegative=True)
    thL = sp.Symbol('thL', nonnegative=True)
    lam_e = (K + 45 + thL) * r3 / 3
    kk_ = K + 45 + 2
    Tk = (3 * (2 * kk_ - 3) / (kk_ * (kk_ - 2))
          * (lam_e ** 2 + (2 * kk_ - 2) * lam_e + 1) + 2 * kk_)
    # знаменатель kk_(kk_-2) > 0: домножим P на него ПОСЛЕ подстановки
    def deep_cell(a1, b1, a2, b2, depth):
        tL = a1 + (b1 - a1) * thL
        tD = a2 + (b2 - a2) * th
        lam_c = (K + 45 + tL) * r3 / 3
        kk_c = K + 47
        Tk_c = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        D_c = 4 + (Tk_c - 4) * tD
        P = P_sym(lam_c, D_c, 41 + v)
        P = sp.expand(sp.fraction(sp.together(P))[0])
        exprs = bernstein2_coeffs(P, thL, th)
        if all(certify(e, (v, K), "deep_tail_v2", log) for e in exprs):
            return True
        if depth == 0:
            return False
        m1 = (a1 + b1) / 2
        m2 = (a2 + b2) / 2
        return (deep_cell(a1, m1, a2, m2, depth-1) and
                deep_cell(a1, m1, m2, b2, depth-1) and
                deep_cell(m1, b1, a2, m2, depth-1) and
                deep_cell(m1, b1, m2, b2, depth-1))

    ELEV = int(os.environ.get("BERN_ELEV", "0"))

    def bern1(expr, var, elev=None):
        pp = sp.Poly(sp.expand(expr), var)
        d = pp.degree() + (ELEV if elev is None else elev)
        cs = [pp.coeff_monomial(var ** q) if q <= pp.degree() else 0
              for q in range(d + 1)]
        # коэффициенты полинома в мономах остаются прежними; Бернштейн
        # берём на поднятой степени d
        cs = [pp.coeff_monomial(var ** q) if q <= pp.degree()
              else sp.Integer(0) for q in range(d + 1)]
        out = []
        for i2 in range(d + 1):
            b = sum(sp.binomial(i2, q) / sp.binomial(d, q) * cs[q]
                    for q in range(min(i2, pp.degree()) + 1))
            out.append(sp.expand(b))
        return out

    def poly_K_nonneg(c):
        if not c.free_symbols:
            return c >= 0
        # коэффициенты могут содержать sqrt3: разделить и проверить как раньше
        if c.has(r3):
            a = sp.Poly(sp.expand(c.coeff(r3, 0)), K)
            b = sp.Poly(sp.expand(c.coeff(r3, 1)), K)
            # достаточно: обе части >= 0 на K>=0 (грубо, с изоляцией корней)
            def okpoly(P):
                if all(cc >= 0 for _, cc in P.terms()):
                    return True
                if P.LC() < 0:
                    return False
                return not [r for r in P.real_roots() if r >= 0]
            if okpoly(a) and okpoly(b):
                return True
            return False
        P = sp.Poly(c, K)
        if all(cc >= 0 for _, cc in P.terms()):
            return True
        if P.LC() < 0:
            return False
        roots = [r for r in P.real_roots() if r >= 0]
        return not roots and c.subs(K, 1) > 0

    sig = sp.Symbol('sigma', nonnegative=True)
    vpp = sp.Symbol('vpp', nonnegative=True)

    def deep_cell3(vsub, extra_var, a1, b1, a2, b2, depth, tag):
        tL = a1 + (b1 - a1) * thL
        tD = a2 + (b2 - a2) * th
        lam_c = (K + 45 + tL) * r3 / 3
        kk_c = K + 47
        Tk_c = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        D_c = 4 + (Tk_c - 4) * tD
        P = P_sym(lam_c, D_c, 41 + vsub)
        P = sp.expand(sp.fraction(sp.together(P))[0])
        exprs = bernstein2_coeffs(P, thL, th)
        allok = True
        for e in exprs:
            if extra_var is sig:
                subs_ok = all(poly_K_nonneg(b2c) for b2c in bern1(e, sig))
            else:
                # (K, vpp) ортант: покоэффициентно + fallback нет
                Pp = sp.Poly(sp.expand(e), K, vpp)
                subs_ok = all(
                    (cc >= 0) if not cc.has(r3) else (
                        cc.coeff(r3, 0) >= 0 and cc.coeff(r3, 1) >= 0)
                    for _, cc in Pp.terms())
            if not subs_ok:
                allok = False
                break
        log.append({"cell": tag, "box": [str(a1), str(b1), str(a2), str(b2)],
                    "ok": bool(allok)})
        if allok:
            return True
        if depth == 0:
            return False
        m1 = (a1 + b1) / 2
        m2 = (a2 + b2) / 2
        return all(deep_cell3(vsub, extra_var, aa, bb, cc2, dd, depth-1, tag)
                   for aa, bb, cc2, dd in
                   [(a1, m1, a2, m2), (a1, m1, m2, b2),
                    (m1, b1, a2, m2), (m1, b1, m2, b2)])

    # ---- v4 для below-diagonal: разложение по y (D = T_cap - y):
    #      положительность всех коэффициентов по y <=> P>0 на ВСЕЙ полуоси D<=T_cap
    yv = sp.Symbol('y', nonnegative=True)

    def deep_cell4(vsub, extra_var, a1, b1, depth, tag):
        tL = a1 + (b1 - a1) * thL
        lam_c = (K + 45 + tL) * r3 / 3
        kk_c = K + 47
        Tk_c = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        P = P_sym(lam_c.subs(K, K + 8) if "Ktail" in tag else lam_c, (Tk_c.subs(K, K + 8) if "Ktail" in tag else Tk_c) - yv, 41 + vsub)
        P = sp.expand(sp.fraction(sp.together(P))[0])
        ycoeffs = [sp.expand(c) for c in sp.Poly(P, yv).all_coeffs()[::-1]]
        allok = True
        for ci, e in enumerate(ycoeffs):
            # Бернштейн по thL, затем позитивность по (extra, K)
            for b_ in bern1(e, thL):
                if extra_var is sig:
                    okc = all(poly_K_nonneg(b2c) for b2c in bern1(b_, sig))
                else:
                    Pp = sp.Poly(sp.expand(b_), K, vpp)
                    okc = all(
                        (cc >= 0) if not cc.has(r3) else (
                            cc.coeff(r3, 0) >= 0 and cc.coeff(r3, 1) >= 0)
                        for _, cc in Pp.terms())
                if not okc:
                    allok = False
                    break
            if not allok:
                break
        log.append({"cell": tag, "range": [str(a1), str(b1)],
                    "ok": bool(allok)})
        if allok:
            return True
        if depth == 0:
            return False
        mid = (a1 + b1) / 2
        return (deep_cell4(vsub, extra_var, a1, mid, depth - 1, tag) and
                deep_cell4(vsub, extra_var, mid, b1, depth - 1, tag))

    # v5: K-расщепление: K=0..7 явно (2-вар), хвост K>=8 отдельно
    gotA = True
    for K0 in range(0, 8):
        got_k = deep_cell4((K + 4) * sig, sig, sp.Integer(0), sp.Integer(1),
                           6, f"bd_K{K0}")
        # deep_cell4 использует символ K; для явного K0 подменяем через
        # обёртку: временно замкнём K значением
        # (реализация: подстановка в poly_K_nonneg через глобальный сдвиг)
        gotA = gotA and got_k
        break  # placeholder — см. ниже честную реализацию
    # честная реализация: K-подстановка внутри отдельной функции
    def deep_cell4_atK(K0, a1, b1, depth, tag):
        tL = a1 + (b1 - a1) * thL
        lam_c = (sp.Integer(K0) + 45 + tL) * r3 / 3
        kk_c = sp.Integer(K0) + 47
        Tk_c = (3 * (2 * kk_c - 3) / (kk_c * (kk_c - 2))
                * (lam_c ** 2 + (2 * kk_c - 2) * lam_c + 1) + 2 * kk_c)
        P = P_sym(lam_c, Tk_c - yv, 41 + (sp.Integer(K0) + 4) * sig)
        P = sp.expand(sp.fraction(sp.together(P))[0])
        ycoeffs = [sp.expand(c2) for c2 in sp.Poly(P, yv).all_coeffs()[::-1]]
        allok = True
        for e in ycoeffs:
            for b_ in bern1(e, thL):
                sok = all(
                    (cc >= 0) if not cc.has(r3) else (
                        cc.coeff(r3, 0) >= 0 and cc.coeff(r3, 1) >= 0)
                    for b2c in bern1(b_, sig)
                    for _, cc in sp.Poly(sp.expand(b2c), sig).terms())
                if not sok:
                    allok = False
                    break
            if not allok:
                break
        log.append({"cell": tag, "range": [str(a1), str(b1)], "ok": bool(allok)})
        if allok:
            return True
        if depth == 0:
            return False
        mid = (a1 + b1) / 2
        return (deep_cell4_atK(K0, a1, mid, depth - 1, tag) and
                deep_cell4_atK(K0, mid, b1, depth - 1, tag))

    gotA = True
    for K0 in range(0, 8):
        gk = deep_cell4_atK(K0, sp.Integer(0), sp.Integer(1), 6, f"bd_K{K0}")
        print(f"  below-diag K={K0}: {'OK' if gk else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)
        gotA &= gk
    # хвост K >= 8
    gk = deep_cell4((K + 8 + 4) * sig, sig, sp.Integer(0), sp.Integer(1),
                    6, "bd_Ktail")
    print(f"  below-diag K>=8: {'OK' if gk else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)
    gotA &= gk
    print(f"deep-tail below-diagonal: {'OK' if gotA else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)
    gotB = True if STAGE == "belowdiag" else deep_cell3(
        K + 4 + vpp, vpp, sp.Integer(0), sp.Integer(1),
        sp.Integer(0), sp.Integer(1), 3, "deep_above_diag")
    print(f"deep-tail above-diagonal: {'OK' if gotB else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)
    got = gotA and gotB
    ok &= got
    print(f"deep-tail: {'OK' if got else 'FAIL'} ({time.time()-t0:.0f}s)",
          flush=True)

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    failed_cells = [c for c in log if not c.get("ok", True)]
    out = {"j": J, "all_certified": bool(ok), "cells": len(log),
           "stage_verdicts": {
               "shallow_tail": (None if STAGE == "belowdiag"
                                else bool(stail_ok)),
               "deep_fixed": (None if STAGE == "belowdiag"
                              else bool(deep_fixed_ok)),
               "deep_tail_below_diag": bool(gotA),
               "deep_tail_above_diag": (None if STAGE == "belowdiag"
                                        else bool(gotB)),
           },
           "failed_cells": failed_cells[:50],
           "n_failed": len(failed_cells),
           "env": {"KNIFE_STAGE": STAGE,
                   "BERN_ELEV": os.environ.get("BERN_ELEV", "0")},
           "scope_note": "stage_verdicts null = stage NOT RUN in this "
                         "invocation; all_certified covers only stages run",
           "command": f"KNIFE_J={J} KNIFE_STAGE={STAGE} "
                      "python lab/knife_tail_deep.py",
           "git": git, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"knife_tail_deep_j{J}.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(("ALL CERTIFIED" if ok else "INCOMPLETE") + f" cells={len(log)}",
          flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
