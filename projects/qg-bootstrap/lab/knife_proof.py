"""General-knife prover: (-1)^{j-1} B_j > 0 on the allowed region, per knife j.

Usage: KNIFE_J=4 python lab/knife_proof.py
Architecture (generalizes the blade theorem, j=3 -> any fixed j):
  SHALLOW (lam <= 26.1), branches k=3..45 with the blade-proof breakpoints:
    per-cell claim: P_j := (-1)^{j-1} B_j > 0 for ALL D in [4, T_k(lam)]
    (interval positivity - no window bookkeeping needed). Certificates:
    D = 4 + (T_k - 4) * u/(1+u), lam-branch t = w/(1+w); fixed m univariate
    in (u) per t-subcell... implemented as positive-coefficient checks in
    (u, w) for fixed m and (v, u, w) for the m-tail, with adaptive t-bisection.
  DEEP (lam >= 26): reuse L1 (envelope <= (12+4sqrt3)lam, proven j-free);
    prove P_j > 0 for D in [4, (12+4sqrt3)lam] on {m >= M0} u {small m}:
    small m: per-m certificates in (x=lam-26, u); tail m: (v, z, u) over
    Q(sqrt3) on the containment region s <= (4/3)(m+3) plus the outside
    region via... outside the belt negativity may still exist for higher j
    (containment was j=3-specific), so deep tail here certifies the FULL
    D-interval directly without containment.
Artifact: results/knife_proof_j{J}.json; exit 0 iff every cell certifies.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from math import factorial
from pathlib import Path

import sympy as sp

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "4"))

m, lam, v, w, u, z, x = sp.symbols("m lam v w u z x", nonnegative=True)
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


def Esym(t):
    """E_{2t} для символьного m: элементарные симметрические от
    {(m+3-2k)^2, k=1..m+2} удвоенного — вычислить нельзя символически в
    общем виде; для ячеек с фиксированным m используем e_doubled_int, для
    m-хвоста строим E_{2t}(m0+v) интерполяцией по v (полином степени 3t)."""
    raise NotImplementedError


def E_poly_in_v(t, m0, deg_extra=1):
    """E_{2t}(n) как полином от v (m = m0+v): степень 3t; строим по 3t+1+deg_extra
    точкам точной интерполяцией и ПРОВЕРЯЕМ на 2 контрольных точках."""
    deg = 3 * t
    pts = []
    for vv in range(deg + 1 + deg_extra + 2):
        n = m0 + vv + 3
        pts.append((vv, e_doubled_int(n)[t]))
    poly = sp.interpolate(pts[: deg + 1], v)
    for vv, val in pts[deg + 1 :]:
        assert sp.expand(poly.subs(v, vv) - val) == 0, f"E interp fail t={t}"
    return sp.expand(poly)


def bracket_sym(j, m_expr, lam_expr, D_expr, e_vals):
    """(-1)^{j-1} B_j с подстановками; e_vals: список E_{2t} выражений."""
    c = 4 * m_expr - 4 * j + 12 - 1  # 4n-4j-1, n = m+3
    s = lam_expr + m_expr + 2
    B = sp.Integer(0)
    for i in range(j):
        wgt = sp.Rational(factorial(0))  # placeholder
        # (2n-2j+2i)! нельзя символически по m; для фиксированного m числа,
        # для хвоста факториалы входят как отношения — здесь используем
        # ТОЛЬКО фиксированные m (см. main), хвост через отношение к i=0.
        raise NotImplementedError
    return B


def certify_pos(expr, gens, tag, log):
    e2 = sp.expand(sp.fraction(sp.together(expr))[0])
    P = sp.Poly(e2, *gens)
    bad = 0
    for mon, c in P.terms():
        c = sp.expand(c)
        if c.has(r3):
            a = c.coeff(r3, 0)
            b = c.coeff(r3, 1)
            okc = (
                (a >= 0 and b >= 0)
                or (a >= 0 and b < 0 and a**2 >= 3 * b**2)
                or (a < 0 and b >= 0 and 3 * b**2 >= a**2)
            )
        else:
            okc = c >= 0
        if not okc:
            bad += 1
    log.append({"cell": tag, "monomials": len(P.terms()), "bad": bad})
    return bad == 0


def Bj_fixed_m(j, mv, lam_expr, D_expr):
    n = mv + 3
    e = e_doubled_int(n)
    c = 4 * n - 4 * j - 1
    s = lam_expr + n - 1
    B = sp.Integer(0)
    for i in range(j):
        wgt = sp.Integer(factorial(2 * n - 2 * j + 2 * i)) / (factorial(i) * 2**i)
        tail = sp.prod(D_expr + c + 2 * k for k in range(i, j - 1))
        B += (-1) ** i * e[j - 1 - i] * wgt * s ** (2 * i) * tail
    if j % 2 == 0:
        B = -B
    return B


def cell_shallow(j, mv, kk, mu_lo, mu_hi, depth, log):
    """P_j > 0 на D in [4, T_k(lam)], lam in [mu_lo, mu_hi], m=mv фиксирован.
    t-бисекция; на каждом под-отрезке: 2-вар сертификат (u, w)."""
    t = sp.Symbol("t", nonnegative=True)

    def try_cell(a, b, d):
        lam_e = a + (b - a) * (w / (1 + w))
        Tk = (
            sp.Rational(3 * (2 * kk - 3), kk * (kk - 2)) * (lam_e**2 + (2 * kk - 2) * lam_e + 1)
            + 2 * kk
        )
        D_e = 4 + (Tk - 4) * (u / (1 + u))
        B = Bj_fixed_m(j, mv, lam_e, D_e)
        if certify_pos(B, (u, w), f"j{j}_k{kk}_m{mv}", log):
            return True
        if d == 0:
            return False
        mid = (a + b) / 2
        return try_cell(a, mid, d - 1) and try_cell(mid, b, d - 1)

    return try_cell(mu_lo, mu_hi, depth)


def main() -> int:
    t0 = time.time()
    log = []
    ok = True
    summary = {}
    # SHALLOW: branches (как в blade_proof), фиксированные m до MFIX,
    # m-хвост: пока фиксированные до 60 + отчёт о хвосте отдельным этапом
    MFIX = 40
    for kk in range(3, 46):
        if kk == 3:
            mu_lo, mu_hi = sp.Rational(1, 1000), sp.Rational(2, 3)
        else:
            mu_lo = sp.Rational(3, 5) * (kk - sp.Rational(5, 2))
            mu_hi = sp.Rational(3, 5) * (kk - sp.Rational(3, 2))
            if kk == 4:
                mu_lo = sp.Rational(2, 3)
        branch_ok = True
        for mv in range(max(1, j_min_m(J)), MFIX + 1):
            got = cell_shallow(J, mv, kk, mu_lo, mu_hi, 4, log)
            branch_ok &= got
            if not got:
                print(f"  FAIL j={J} k={kk} m={mv}", flush=True)
        ok &= branch_ok
        print(
            f"branch k={kk}: {'OK' if branch_ok else 'FAIL'} ({time.time() - t0:.0f}s)", flush=True
        )
    summary["shallow_mfix"] = MFIX
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "j": J,
        "ok_so_far": bool(ok),
        "scope": f"shallow branches k=3..45, m={j_min_m(J)}..{MFIX} (m-tail and"
        f" deep water: next stage)",
        "cells": len(log),
        "command": f"KNIFE_J={J} python lab/knife_proof.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / f"knife_proof_j{J}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(("SHALLOW CERTIFIED" if ok else "INCOMPLETE") + f" (cells {len(log)})", flush=True)
    return 0 if ok else 1


def j_min_m(j):
    return max(1, j - 2)  # нужен l=2n-2j>=2 -> n>=j+1 -> m>=j-2


if __name__ == "__main__":
    sys.exit(main())
