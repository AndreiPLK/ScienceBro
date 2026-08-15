"""AUTO-PROVER: the j=3 blades never cut the shore (theorem candidate, paper 4).

Claim: for every level n>=4 and every lambda>0, the negativity window of the
j=3 ladder (if any) lies strictly above the envelope min_k T_k(lambda).

Proof architecture (all certificates = polynomial identities with nonnegative
coefficients after affine-rational substitutions; checked in exact rational
arithmetic by sympy):

BRANCH k=3, lambda in (0, 2/3]:
  (a) n=4,5: no window at all (disc<0; univariate root isolation);
  (b) n>=6: Bhat(T_3)>0 AND T_3 left of the vertex - both by direct
      positive-coefficient certificates after m=v+3, lam=(2/3)(1-w/(1+w)).
BRANCHES k=4..45, lambda in [3(2k-5)/10, 3(2k-3)/10] (k=4 starts at 2/3):
  For each pair of inequalities (Bhat(T_k)>0; vertex OR no-window) run an
  ADAPTIVE certifier: substitute lam=(2/3)(kap+1+t), t in [a,b] subinterval,
  t = a+(b-a)*w/(1+w); m=v+m0 (small m handled per-value); kap=K+k0; check
  all coefficients >=0; bisect [a,b] / split small m, kap on failure.
Every branch's certificate list is persisted to results/blade_proof.json;
exit 0 only if every cell certifies.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

RES = Path(__file__).resolve().parents[1] / "results"
m, lam, v, w, kap = sp.symbols('m lam v w kappa', nonnegative=True)

s_ = lam + m + 2
G = 2*(m+1)*(m+3)/(3*(2*m+3))
al = (m+3)*(5*m**3+21*m**2+19*m+15)/(45*(2*m+1)*(2*m+3))


def Tk_of(k_expr):
    return (3*(2*k_expr-3)/(k_expr*(k_expr-2))
            * (lam**2 + (2*k_expr-2)*lam + 1) + 2*k_expr)


def bhat_at_T(k_expr):
    u_at = Tk_of(k_expr) + 4*m + 1
    F = sp.together(sp.expand(al*u_at*(u_at-2) - G*u_at*s_**2 + s_**4))
    return sp.expand(sp.fraction(F)[0])


def vertex_gap(k_expr):
    """G s^2 - (T_k + 4m) * 2 al > 0  <=>  T_k left of the window vertex."""
    V = sp.together(sp.expand(G*s_**2 - (Tk_of(k_expr) + 4*m)*2*al))
    return sp.expand(sp.fraction(V)[0])


def univar_ok_on01(expr_t):
    """expr(t) > 0 на [0,1]: изоляция корней + положительная выборка. Строго."""
    t = sp.Symbol('t', nonnegative=True)
    e = sp.expand(expr_t)
    if e.is_number:
        return e > 0
    roots = sp.Poly(e, t).real_roots()
    if any(0 <= r <= 1 for r in roots):
        return False
    return e.subs(t, sp.Rational(1, 2)) > 0


def cell_fixed_m(Bk, Vk, disc, mv, lam_sub, log, tag):
    """Ячейка с фиксированным m: (нет окна) ИЛИ (B>0 И V>0), одномерно по t."""
    t = sp.Symbol('t', nonnegative=True)
    d = sp.expand(disc.subs(m, mv).subs(lam, lam_sub))
    if univar_ok_on01(-d):
        log.append({"cell": tag, "via": "no-window"})
        return True
    Bv = sp.expand(sp.fraction(sp.together(Bk.subs(m, mv).subs(lam, lam_sub)))[0])
    Vv = sp.expand(sp.fraction(sp.together(Vk.subs(m, mv).subs(lam, lam_sub)))[0])
    if univar_ok_on01(Bv) and univar_ok_on01(Vv):
        log.append({"cell": tag, "via": "B&V"})
        return True
    # окно умирает внутри диапазона: делим t на подотрезки по корням disc
    roots = sorted([sp.nsimplify(r) for r in sp.Poly(d, t).real_roots()
                    if 0 <= r <= 1])
    pts = [sp.Integer(0)] + roots + [sp.Integer(1)]
    for i in range(len(pts) - 1):
        a2, b2 = pts[i], pts[i + 1]
        if b2 == a2:
            continue
        tt = a2 + (b2 - a2) * t
        dd = sp.expand(d.subs(t, tt))
        if univar_ok_on01(-dd):
            continue
        Bv2 = sp.expand(Bv.subs(t, tt))
        Vv2 = sp.expand(Vv.subs(t, tt))
        if univar_ok_on01(Bv2) and univar_ok_on01(Vv2):
            continue
        log.append({"cell": tag, "sub": [str(a2), str(b2)], "cert": "FAILED"})
        return False
    log.append({"cell": tag, "via": "split-at-disc-roots"})
    return True


def certify_cell(expr, mvar, kapvar, a, b, depth, log, tag):
    """Positivity of expr(m=mvar+m0 handled by caller) for t in [a,b] via
    t = a+(b-a)w/(1+w); bisect on failure."""
    t = sp.Symbol('t', nonnegative=True)
    e = expr.subs(t, a + (b - a) * w / (1 + w))
    e = sp.expand(sp.fraction(sp.together(e))[0])
    gens = [g for g in (mvar, kapvar, w) if g is not None]
    P = sp.Poly(e, *gens)
    neg = [c for _, c in P.terms() if c < 0]
    if not neg:
        log.append({"cell": tag, "t": [str(a), str(b)], "cert": "N=0"})
        return True
    if depth == 0:
        log.append({"cell": tag, "t": [str(a), str(b)], "cert": "FAILED"})
        return False
    mid = (a + b) / 2
    return (certify_cell(expr, mvar, kapvar, a, mid, depth-1, log, tag) and
            certify_cell(expr, mvar, kapvar, mid, b, depth-1, log, tag))


def univar_positive(expr_lam, lo, hi):
    """expr(lam) > 0 on (lo, hi]: no roots in interval + positive sample."""
    roots = sp.Poly(sp.expand(expr_lam), lam).real_roots()
    if any(lo < r <= hi for r in roots):
        return False
    return sp.expand(expr_lam).subs(lam, (lo + hi)/2) > 0


def main() -> int:
    t0 = time.time()
    log = []
    ok = True

    # ---------- BRANCH k=3 ----------
    B3 = bhat_at_T(sp.Integer(3))
    V3 = vertex_gap(sp.Integer(3))
    for mv in (1, 2):
        Gm, alm, sm = (G.subs(m, mv), al.subs(m, mv), s_.subs(m, mv))
        disc = sp.expand((2*alm + Gm*sm**2)**2 - 4*alm*sm**4)
        nowin = univar_positive(-disc, 0, sp.Rational(2, 3))
        log.append({"cell": f"k3_m{mv}_nowindow", "ok": bool(nowin)})
        ok &= nowin
    r_ = sp.Symbol('t', nonnegative=True)
    for name, E in (("k3_B", B3), ("k3_V", V3)):
        e = E.subs([(m, v + 3), (lam, sp.Rational(2, 3)*(1 - r_))])
        got = certify_cell(sp.expand(e * 81), v, None, sp.Integer(0),
                           sp.Integer(1), 4, log, name)
        ok &= got

    # ---------- EXPLICIT BRANCHES k = 4..45 ----------
    # branch k covers lam in [mu_k, mu_{k+1}], rational breakpoints near the
    # true argmin switches: mu_k = (k - 5/2) * 3/5  (3/5 ~ 1/sqrt(3) is NOT
    # used; spacing per k is 3/5=0.6, drift over 42 branches ~1.0 in k units,
    # tolerated because certificates verify each branch INDIVIDUALLY).
    t = sp.Symbol('t', nonnegative=True)
    KMAX = 45
    for kk in range(4, KMAX + 1):
        mu_lo = sp.Rational(3, 5) * (kk - sp.Rational(5, 2))
        mu_hi = sp.Rational(3, 5) * (kk - sp.Rational(3, 2))
        if kk == 4:
            mu_lo = sp.Rational(2, 3)   # стык с веткой k=3
        lam_sub = mu_lo + (mu_hi - mu_lo) * t
        Bk = bhat_at_T(sp.Integer(kk))
        Vk = vertex_gap(sp.Integer(kk))
        disc = sp.expand((2*al + G*s_**2)**2 - 4*al*s_**4)
        branch_ok = True
        # фиксированные m: одномерные строгие проверки; поднимаем стартовый m
        # хвоста, пока 2-переменный сертификат не сойдётся
        m_start = 4
        tail_done = False
        while m_start <= 120 and not tail_done:
            for m0 in range(1 if m_start == 4 else m_start - 6, m_start):
                branch_ok &= cell_fixed_m(Bk, Vk, disc, m0, lam_sub, log,
                                          f"k{kk}_m{m0}")
            # хвост m >= m_start: 2-var Пойя для B и V
            okB = okV = True
            for name, E in ((f"k{kk}_Btail", Bk), (f"k{kk}_Vtail", Vk)):
                e = sp.expand(E.subs(m, v + m_start).subs(lam, lam_sub))
                e = sp.expand(sp.fraction(sp.together(e))[0])
                got = certify_cell(e, v, None, sp.Integer(0), sp.Integer(1),
                                   3, [], f"{name}_m{m_start}")
                if name.endswith('Btail'):
                    okB = got
                else:
                    okV = got
            if okB and okV:
                log.append({"cell": f"k{kk}_tail", "m_start": m_start,
                            "cert": "OK"})
                tail_done = True
            else:
                m_start += 6
        branch_ok &= tail_done
        ok &= branch_ok
        print(f"branch k={kk} [{mu_lo},{mu_hi}]:"
              f" {'OK' if branch_ok else 'FAIL'} ({time.time()-t0:.0f}s)",
              flush=True)

    # ---------- TAIL lam >= 26 ----------
    x, z, r3 = sp.Symbol('x', nonnegative=True), sp.Symbol('z', nonnegative=True), sp.sqrt(3)
    disc_g = sp.expand((2*al + G*s_**2)**2 - 4*al*s_**4)
    # Part T0: m <= 78 -> no window at lam >= 26 (univariate certificates)
    t0fails = []
    for mv in range(1, 79):
        d = sp.expand(-disc_g.subs([(m, mv), (lam, 26 + x)]))
        num = sp.expand(sp.fraction(sp.together(d))[0])
        P = sp.Poly(num, x)
        if any(c < 0 for _, c in P.terms()):
            roots = [r for r in P.real_roots() if r >= 0]
            if roots or num.subs(x, 1) <= 0:
                t0fails.append(mv)
    ok &= not t0fails
    log.append({"cell": "tail_T0_nowindow_m1..78", "fails": t0fails})

    def q3_nonneg(c):
        c = sp.expand(c)
        a, b = c.coeff(r3, 0), c.coeff(r3, 1)
        if a >= 0 and b >= 0:
            return True
        if a >= 0 and b < 0:
            return bool(a**2 >= 3*b**2)
        if a < 0 and b >= 0:
            return bool(3*b**2 >= a**2)
        return False

    def cert_q3(E, gens_and_ranges, tag):
        num = sp.expand(sp.fraction(sp.together(E))[0])
        for gvar in gens_and_ranges:
            deg = sp.Poly(num, gvar).degree()
            num = sp.expand(sp.fraction(sp.together(
                num.subs(gvar, w/(1+w)) * (1+w)**deg))[0])
        P = sp.Poly(num, v, w)
        bad = sum(0 if q3_nonneg(c) else 1 for _, c in P.terms())
        log.append({"cell": tag, "monomials": len(P.terms()), "bad": bad})
        return bad == 0

    # Part T1 (L2): no window when s > (4/3)(m+3), for m >= 79
    beta = sp.together(4*al - G**2)
    RHS = sp.together(sp.Rational(16, 9)*(m+3)**2*beta - 2*al*G)
    e1 = sp.expand(sp.fraction(RHS)[0].subs(m, v + 79))
    e2 = sp.expand(sp.fraction(sp.together(RHS**2 - 16*al**3))[0].subs(m, v + 79))
    okL2 = (all(c >= 0 for _, c in sp.Poly(e1, v).terms()) and
            all(c >= 0 for _, c in sp.Poly(e2, v).terms()))
    ok &= okL2
    log.append({"cell": "tail_L2_window_containment", "ok": bool(okL2)})

    # Part T2 (L1): envelope <= (12+4*sqrt3)*lam for lam >= 26
    K, th = sp.symbols('K theta', nonnegative=True)
    lamK = (K + th)*r3/3
    kk_ = K + 2
    TkK = 3*(2*kk_-3)/(kk_*(kk_-2))*(lamK**2 + (2*kk_-2)*lamK + 1) + 2*kk_
    Delta = sp.together(sp.radsimp(sp.expand((12+4*r3)*lamK - TkK)))
    numD = sp.expand(sp.fraction(Delta)[0]).subs([(K, v + 45), (th, z)])
    okL1 = cert_q3(numD, [z], "tail_L1_envelope_below_asymptote")
    ok &= okL1

    # Part T3 (L3): deep water m>=79, 26<=lam<=26+(v+7)/3 (s <= 4(m+3)/3)
    mdeep = v + 79
    lamdeep = 26 + z*(v + 7)/3
    sdeep = lamdeep + mdeep + 2
    Gd = G.subs(m, mdeep)
    ald = al.subs(m, mdeep)
    uA = (12 + 4*r3)*lamdeep + 4*mdeep + 1
    Bd = sp.together(sp.expand(ald*uA*(uA-2) - Gd*uA*sdeep**2 + sdeep**4))
    Vd = sp.together(sp.expand(Gd*sdeep**2 - ((12+4*r3)*lamdeep + 4*mdeep)*2*ald))
    okL3 = (cert_q3(Bd, [z], "tail_L3a_B_at_asymptote") and
            cert_q3(Vd, [z], "tail_L3b_vertex"))
    ok &= okL3
    print(f"TAIL lam>=26: T0={not t0fails} L2={okL2} L1={okL1} L3={okL3}"
          f" ({time.time()-t0:.0f}s)", flush=True)

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"theorem": "j=3 blades never cut the shore - COMPLETE: branches k=3..45 (lam<=26.1) + tail lam>=26 (T0/L2/L1/L3)",
           "branches": "k=3 on (0,2/3]; k>=4 on [(2/3)(k-3),(2/3)(k-2)]",
           "all_certified": bool(ok), "cells": log,
           "command": "python lab/blade_proof.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "blade_proof.json").write_text(json.dumps(out, indent=1),
                                          encoding="utf-8")
    print("ALL CERTIFIED" if ok else "CERTIFICATION INCOMPLETE", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
