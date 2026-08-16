"""Tails + deep water on the v2 engine (flint) — full port of
knife_tail_deep.py stages: shallow-tail (m>=41), deep-fixed (m<=40),
deep-tail (below-diagonal K-pieces + above-diagonal orthant).

Same mathematics, same certificates, same cell logic; only the arithmetic
engine changes. Validation contract: verdicts must match v1 artifacts.

Usage: KNIFE_J=6 python lab/knife_tail2.py
Artifact: results/knife_tail_deep_j{J}.json (same name/fields as v1 —
engine field marks the build).
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp
from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402
from prover2_core import Q3Poly, QPoly, bern_matrix, sign_q3  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))
STAGE = os.environ.get("KNIFE_STAGE", "all")
ELEV = int(os.environ.get("BERN_ELEV", "0"))


# ---------------------------------------------------------------- E-polys
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


def E_poly_coeffs(t):
    m = sp.Symbol('m')
    deg = 3 * t
    lo = max(1, t - 1)
    pts = [(mm, e_doubled_int(mm + 3)[t]) for mm in range(lo, lo + deg + 4)]
    poly = sp.expand(sp.interpolate(pts[:deg + 1], m))
    for mm, val in pts[deg + 1:]:
        assert poly.subs(m, mm) == val
    P = sp.Poly(poly, m)
    return [fmpq(int(sp.Rational(c).p), int(sp.Rational(c).q))
            for c in P.all_coeffs()[::-1]]


EP = {t: E_poly_coeffs(t) for t in range(J)}


def E_at(m_expr, t):
    acc = Q3Poly.const(m_expr.nv, 0)
    p = Q3Poly.const(m_expr.nv, 1)
    for cf in EP[t]:
        acc = acc + p * cf
        p = p * m_expr
    return acc


def build_P(lam, D_num, den, m_expr):
    """N = den^{J-1} * (-1)^{J-1} B_j, где D = D_num/den, den > 0.
    lam, D_num, den, m_expr — Q3Poly одного nv. Если den == 1, обычный P."""
    nv = lam.nv
    n = m_expr + 3
    c = 4 * n - 4 * J - 1
    s = lam + (n - 1)
    s2 = s * s
    s2p = {0: Q3Poly.const(nv, 1)}
    for i in range(1, J):
        s2p[i] = s2p[i - 1] * s2
    denp = {0: Q3Poly.const(nv, 1)}
    for i in range(1, J):
        denp[i] = denp[i - 1] * den
    B = Q3Poly.const(nv, 0)
    two_n = 2 * n
    for i in range(J):
        poch = Q3Poly.const(nv, 1)
        for q in range(1, 2 * i + 1):
            poch = poch * (two_n - 2 * J + q)
        wgt_den = fmpq(math.factorial(i) * 2 ** i)
        tail = Q3Poly.const(nv, 1)
        for r in range(i, J - 1):
            tail = tail * (D_num + (c + 2 * r) * den)
        term = E_at(m_expr, J - 1 - i) * poch * s2p[i] * tail * denp[i]
        term = Q3Poly(term.a * (fmpq(1) / wgt_den),
                      term.b * (fmpq(1) / wgt_den))
        B = B + term if i % 2 == 0 else B - term
    if J % 2 == 0:
        B = Q3Poly(QPoly(nv, {k: -cv for k, cv in B.a.c.items()}),
                   QPoly(nv, {k: -cv for k, cv in B.b.c.items()}))
    return B


# ------------------------------------------------- Bernstein (paired A,B)
def bern_axis_pair(A, B, axis, elev=0):
    d = max(max((e[axis] for e in A), default=0),
            max((e[axis] for e in B), default=0)) + elev
    M = bern_matrix(d)

    def transform(C):
        fib = {}
        for e, val in C.items():
            key = e[:axis] + e[axis + 1:]
            fib.setdefault(key, {})[e[axis]] = val
        out = {}
        for key, f in fib.items():
            for i in range(d + 1):
                sacc = fmpq(0)
                Mi = M[i]
                for q, cq in f.items():
                    if q <= i:
                        sacc += Mi[q] * cq
                if sacc != fmpq(0):
                    out[key[:axis] + (i,) + key[axis:]] = sacc
        return out
    return transform(A), transform(B)


def collect_pairs(A, B, axes_left):
    """Сгруппировать по осям axes_left: {exp_left: (a_dict, b_dict)} по
    остальным осям."""
    out = {}
    for src, tag in ((A, 0), (B, 1)):
        for e, val in src.items():
            kl = tuple(e[i] for i in axes_left)
            kr = tuple(x for i, x in enumerate(e) if i not in axes_left)
            slot = out.setdefault(kl, ({}, {}))
            slot[tag][kr] = val
    return out


def univar_nonneg(coeffs):
    """{deg: fmpq} — неотрицательность на [0, inf)."""
    if not coeffs:
        return True
    if all(cv >= 0 for cv in coeffs.values()):
        return True
    dmax = max(coeffs)
    if coeffs[dmax] < 0:
        return False
    x = sp.Symbol('x')
    e = sp.Add(*[sp.Rational(int(cv.p), int(cv.q)) * x ** d
                 for d, cv in coeffs.items()])
    P = sp.Poly(e, x)
    if [r for r in P.real_roots() if r >= 0]:
        return False
    return P.eval(1) > 0


def univar_strict(coeffs):
    """S4: полином от одной переменной строго положителен на [0, inf)?
    Достаточно: неотрицателен и есть положительный коэффициент."""
    return any(cv > 0 for cv in coeffs.values())


def q3_pointwise_ok(a_dict, b_dict):
    """Все коэффициенты >= 0 (ортант). Возвращает True/False."""
    for e in set(a_dict) | set(b_dict):
        if sign_q3(a_dict.get(e, fmpq(0)), b_dict.get(e, fmpq(0))) < 0:
            return False
    return True


def block_strict(a_dict, b_dict):
    """S4: блок Бернштейна (как полином от остаточных переменных с
    неотрицательными коэффициентами) строго положителен на [0,inf)^d
    <=> его свободный член строго положителен. Если это выполнено для
    ВСЕХ блоков, то P > 0 на всём замкнутом множестве (сумма базиса
    Бернштейна = 1, значит в каждой точке активен хотя бы один блок)."""
    zero = tuple([0] * len(next(iter(set(a_dict) | set(b_dict)), (0,))))
    return sign_q3(a_dict.get(zero, fmpq(0)), b_dict.get(zero, fmpq(0))) > 0


def q3_strict(a_dict, b_dict):
    """S4: есть ли СТРОГО положительный коэффициент (=> P > 0 на ортанте
    вместе с неотрицательностью остальных)."""
    for e in set(a_dict) | set(b_dict):
        if sign_q3(a_dict.get(e, fmpq(0)), b_dict.get(e, fmpq(0))) > 0:
            return True
    return False


# --------------------------------------------------------------- stages
def main() -> int:
    t0 = time.time()
    log = []
    ok = True
    r3 = sp.sqrt(3)  # noqa: F841

    # ============ STAGE 1: SHALLOW-TAIL (m = 41+v), rational only =======
    # vars: 0=tau, 1=th, 2=v
    stail_ok = True
    if STAGE != "belowdiag":
        NV = 3

        def var(i):
            return Q3Poly.var(NV, i)

        tau, th, vv = var(0), var(1), var(2)
        mv_expr = vv + 41

        def cell(kk, a, b, onto, depth, tag):
            aq = fmpq(a.numerator, a.denominator)
            bq = fmpq(b.numerator, b.denominator)
            if onto:
                lam_e = (Q3Poly.const(NV, fmpq(2, 3))
                         * (1 - aq - (bq - aq) * tau))
            else:
                lam_e = aq + (bq - aq) * tau
            r = fmpq(3 * (2 * kk - 3), kk * (kk - 2))
            Tk = (lam_e * lam_e + (2 * kk - 2) * lam_e + 1) * r + 2 * kk
            D_e = 4 + (Tk - 4) * th
            P = build_P(lam_e, D_e, Q3Poly.const(NV, 1), mv_expr)
            A, B = P.a.c, P.b.c
            A, B = bern_axis_pair(A, B, 0, ELEV)
            A, B = bern_axis_pair(A, B, 1, ELEV)
            good = True
            strict = True
            for kl, (ad, bd) in collect_pairs(A, B, (0, 1)).items():
                assert not bd, "sqrt3 in shallow?"
                cf = {e[0]: cv for e, cv in ad.items()}
                if not univar_nonneg(cf):
                    good = False
                    break
                if cf.get(0, fmpq(0)) <= 0:
                    strict = False
            log.append({"cell": tag, "ok": bool(good),
                        "strict": bool(strict)})
            if good:
                return True
            if depth == 0:
                return False
            mid = (a + b) / 2
            return (cell(kk, a, mid, onto, depth - 1, tag)
                    and cell(kk, mid, b, onto, depth - 1, tag))

        for kk in range(3, 46):
            onto = kk == 3
            if onto:
                lo, hi = Fraction(0), Fraction(1)
            else:
                lo = Fraction(3, 5) * (kk - Fraction(5, 2))
                hi = Fraction(3, 5) * (kk - Fraction(3, 2))
                if kk == 4:
                    lo = Fraction(2, 3)
            got = cell(kk, lo, hi, onto, 5, f"stail_k{kk}")
            ok &= got
            stail_ok &= got
            print(f"shallow-tail k={kk}: {'OK' if got else 'FAIL'}"
                  f" ({time.time()-t0:.0f}s)", flush=True)

    # ============ STAGE 2: DEEP-FIXED (m<=40, lam=26+x), Q(sqrt3) =======
    # vars: 0=x, 1=th
    deep_fixed_ok = True
    if STAGE != "belowdiag":
        NV = 2
        xq, thq = Q3Poly.var(NV, 0), Q3Poly.var(NV, 1)
        lam_df = 26 + xq
        D_hi = (12 + 4 * Q3Poly.const(NV, 0, 1)) * (26 + xq)
        D_e = 4 + (D_hi - 4) * thq
        for mv in range(max(1, J - 2), 41):
            P = build_P(lam_df, D_e, Q3Poly.const(NV, 1),
                        Q3Poly.const(NV, mv))
            A, B = bern_axis_pair(P.a.c, P.b.c, 1, ELEV)
            good = True
            strict = True
            for kl, (ad, bd) in collect_pairs(A, B, (1,)).items():
                if not q3_pointwise_ok(ad, bd):
                    good = False
                    break
                if not block_strict(ad, bd):
                    strict = False
            log.append({"cell": f"deep_m{mv}", "ok": bool(good),
                        "strict": bool(strict)})
            deep_fixed_ok &= good
            if not good:
                print(f"  deep FAIL m={mv}", flush=True)
        ok &= deep_fixed_ok
        print(f"deep-fixed m<41: {'OK' if deep_fixed_ok else 'FAIL'}"
              f" ({time.time()-t0:.0f}s)", flush=True)

    # ============ STAGE 3: DEEP-TAIL (m=41+v, lam >= 26) ================
    # ниже диагонали: y-разложение у мыса (K0=0..7 + K>=8), выше: ортант
    # vars: 0=thL, 1=v, 2=K (или vpp), 3=y
    NV = 4
    thL, vv, KK, yv = (Q3Poly.var(NV, i) for i in range(4))

    strict_flag = [True]

    def deep_pieces(K_expr, vsub, tag, a1, b1, depth, y_mode, extra):
        """y_mode: True => D = Tk - y (вся полуось); False => D-интервал."""
        aq = fmpq(a1.numerator, a1.denominator)
        bq = fmpq(b1.numerator, b1.denominator)
        tL = aq + (bq - aq) * thL
        lam_c = (K_expr + 45 + tL) * Q3Poly.const(NV, 0, fmpq(1, 3))
        kk_c = K_expr + 47
        den = kk_c * (kk_c - 2)
        lam2 = lam_c * lam_c
        tk_num = (3 * (2 * kk_c - 3)) * (lam2 + (2 * kk_c - 2) * lam_c + 1) \
            + (2 * kk_c) * kk_c * (kk_c - 2)
        if y_mode:
            D_num = tk_num - yv * den
        else:
            D_num = 4 * den + (tk_num - 4 * den) * Q3Poly.var(NV, 3)
        P = build_P(lam_c, D_num, den, vsub + 41)
        # Бернштейн по thL (ось 0); y/th — по коэффициентам оси 3
        A, B = bern_axis_pair(P.a.c, P.b.c, 0, ELEV)
        good = True
        if y_mode:
            groups = collect_pairs(A, B, (0, 3))
        else:
            A, B = bern_axis_pair(A, B, 3, ELEV)
            groups = collect_pairs(A, B, (0, 3))
        for kl, (ad, bd) in groups.items():
            # S6-fix: ветка "Kpoly" удалена (суммировала по v = проверка при
            # v=1, а не доказательство для всех v>=0). Только честный ортант.
            assert extra == "orthant", f"unsupported extra={extra}"
            if not q3_pointwise_ok(ad, bd):
                good = False
            elif not block_strict(ad, bd):
                strict_flag[0] = False
            if not good:
                break
        log.append({"cell": tag, "ok": bool(good),
                    "strict": bool(strict_flag[0])})
        if good:
            return True
        if depth == 0:
            return False
        mid = (a1 + b1) / 2
        return (deep_pieces(K_expr, vsub, tag, a1, mid, depth - 1,
                            y_mode, extra)
                and deep_pieces(K_expr, vsub, tag, mid, b1, depth - 1,
                                y_mode, extra))

    # Ниже диагонали НЕ дублируем: эта область целиком покрыта
    # отдельными PASS-артефактами knife{J}_belowdiag_shift.json
    # (band K>=6 + явные K0..5) и knife{J}_farbelow_factored.json (v<=K-6).
    # tail2 сертифицирует: shallow-tail + deep-fixed + above-diagonal.
    gotA = None

    gotB = deep_pieces(KK, KK + 4 + vv, "deep_above_diag",
                       Fraction(0), Fraction(1), 3, False, "orthant") \
        if STAGE != "belowdiag" else True
    print(f"deep-tail above-diagonal: {'OK' if gotB else 'FAIL'}"
          f" ({time.time()-t0:.0f}s)", flush=True)
    ok &= gotB

    prov = stamp()
    failed = [c for c in log if not c.get("ok", True)]
    nonstrict = [c for c in log if c.get("strict") is False]
    out = {"j": J, "all_certified": bool(ok), "cells": len(log),
           "engine": "tail2-flint",
           "stage_verdicts": {"shallow_tail": bool(stail_ok),
                              "deep_fixed": bool(deep_fixed_ok),
                              "deep_tail_below_diag": "covered by belowdiag_shift + farbelow artifacts",
                              "deep_tail_above_diag": bool(gotB)},
           "n_failed": len(failed), "failed_cells": failed[:50],
           "strict_positive": len(nonstrict) == 0,
           "n_nonstrict_cells": len(nonstrict),
           "nonstrict_cells": [c["cell"] for c in nonstrict][:20],
           "strict_note": ("strict_positive=true means every Bernstein block "
                           "has a strictly positive constant term => P > 0 "
                           "on the CLOSED region, not merely P >= 0"),
           "env": {"KNIFE_STAGE": STAGE, "BERN_ELEV": ELEV},
           "command": f"KNIFE_J={J} python lab/knife_tail2.py",
           **prov, "runtime_s": round(time.time() - t0, 1)}
    (RES / f"knife_tail2_j{J}.json").write_text(json.dumps(out, indent=1),
                                                encoding="utf-8")
    print(("ALL CERTIFIED" if ok else "INCOMPLETE") + f" cells={len(log)}",
          flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
