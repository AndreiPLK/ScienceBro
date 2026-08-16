"""Far-below via factor-then-certify, v2 engine (flint) for the P build.

The sympy P_sym build was the bottleneck (hours for j>=6). Here the whole
polynomial N = (kk(kk-2))^{j-1} * P is built in exact flint arithmetic over
Q(sqrt3) in variables (thL, v, K3, y) — minutes, MB of RAM. Only the final
per-y-coefficient factorization uses sympy (sp.factor is irreplaceable),
fed with the exact expanded polynomial (no symbolic sqrt3: pairs a+b*r3).

Denominator clearing is sign-safe: kk = v + K3 + 53 >= 53 > 2, so
(kk(kk-2))^{j-1} > 0 and sign(N) = sign(P) on the region.

Usage: KNIFE_J=6 python lab/knife_farbelow2.py
Artifact: results/knife{J}_farbelow_factored.json (same contract as v1).
Validation contract: reproduce v1 verdicts for j=4 and j=5 first.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp
from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prover2_core import QPoly, Q3Poly  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "5"))

# variables: 0=thL, 1=v, 2=K3, 3=y
NV = 4
THL, V, K3, Y = range(NV)


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
    """E_{2t}(m) как список рациональных коэффициентов по степеням m
    (интерполяция с проверкой, как в v1)."""
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


def q3_const(a, b=0):
    return Q3Poly.const(NV, a, b)


def q3_var(idx):
    return Q3Poly.var(NV, idx)


def main() -> int:
    t0 = time.time()
    print(f"[farbelow2 j={J}] build start", flush=True)

    vv, k3, thl, y = q3_var(V), q3_var(K3), q3_var(THL), q3_var(Y)
    r3half = fmpq(1, 3)  # sqrt3/3 = (0 + 1/3*sqrt3)

    # lam = (Kc + 6 + 45 + thL) * sqrt3/3,  Kc = v + K3
    base = vv + k3 + 51 + thl
    lam = base * Q3Poly.const(NV, 0, fmpq(1, 3))
    _ = r3half  # (октава выше: sqrt3/3 = 0 + (1/3)*sqrt3)

    kk = vv + k3 + 53                     # rational polynomial
    m_expr = vv + 41                      # m = 41 + v
    n_expr = m_expr + 3
    s = lam + (n_expr - 1)                # s = lam + n - 1
    c_const = 4 * (m_expr + 3) - 4 * J - 1

    # Tk = 3(2kk-3)/(kk(kk-2)) * (lam^2+(2kk-2)lam+1) + 2kk
    # NUM(Tk) = 3(2kk-3)(lam^2+(2kk-2)lam+1) + 2kk*kk*(kk-2), DEN = kk(kk-2)
    lam2 = lam * lam
    tk_num = (3 * (2 * kk - 3)) * (lam2 + (2 * kk - 2) * lam + 1) \
        + (2 * kk) * kk * (kk - 2)
    den = kk * (kk - 2)                   # positive on region

    # D = Tk - y  =>  тейл-фактор (D + c + 2r) = (tk_num + (c+2r-y)*den)/den
    print(f"[farbelow2 j={J}] E-polys...", flush=True)
    EP = {t: E_poly_coeffs(t) for t in range(J)}

    def E_at_m(t):
        acc = Q3Poly.const(NV, 0)
        p = Q3Poly.const(NV, 1)
        for cf in EP[t]:
            acc = acc + p * cf
            p = p * m_expr
        return acc

    print(f"[farbelow2 j={J}] assembling N "
          f"({time.time()-t0:.0f}s)...", flush=True)
    s2 = s * s
    s2_pows = {0: Q3Poly.const(NV, 1)}
    for i in range(1, J):
        s2_pows[i] = s2_pows[i - 1] * s2

    # веса (2n-2J+2i)!/(i!2^i) с n = m+3 полиномом: используем отношение
    # Похгаммеров как в P_sym v1: wgt_i = prod_{q=1..2i} (2n-2J+q) / (i! 2^i)
    B = Q3Poly.const(NV, 0)
    two_n = 2 * (m_expr + 3)
    den_pows = {0: Q3Poly.const(NV, 1)}
    for i in range(1, J):
        den_pows[i] = den_pows[i - 1] * den
    for i in range(J):
        poch = Q3Poly.const(NV, 1)
        for q in range(1, 2 * i + 1):
            poch = poch * (two_n - 2 * J + q)
        wgt_den = fmpq(1)
        import math
        wgt_den = fmpq(math.factorial(i) * 2 ** i)
        tail = Q3Poly.const(NV, 1)
        for r in range(i, J - 1):
            tail = tail * (tk_num + (c_const + 2 * r) * den - y * den)
        # tail содержит den^{J-1-i}; домножаем на den^i => единый den^{J-1}
        term = E_at_m(J - 1 - i) * poch * s2_pows[i] * tail * den_pows[i]
        term = Q3Poly(term.a * (fmpq(1) / wgt_den), term.b * (fmpq(1) / wgt_den))
        B = B + term if i % 2 == 0 else B - term
    if J % 2 == 0:
        B = Q3Poly(QPoly(NV, {k: -c for k, c in B.a.c.items()}),
                   QPoly(NV, {k: -c for k, c in B.b.c.items()}))
    print(f"[farbelow2 j={J}] N built: {len(B.a.c)}+{len(B.b.c)} monomials "
          f"({time.time()-t0:.0f}s)", flush=True)

    # y-коэффициенты: собрать словари по степени y
    ycoeffs = {}
    for part, store in ((B.a, 'a'), (B.b, 'b')):
        for e, cval in part.c.items():
            d = ycoeffs.setdefault(e[Y], {'a': {}, 'b': {}})
            d[store][(e[THL], e[V], e[K3])] = cval
    print(f"[farbelow2 j={J}] y-coefficients: {len(ycoeffs)}", flush=True)

    # каждый y-коэффициент -> sympy -> factor -> знаки (как v1)
    thL_s, v_s, K3_s = sp.symbols('thL v K3', nonnegative=True)
    r3_s = sp.sqrt(3)

    def to_sympy(d):
        terms = []
        for (i1, i2, i3), cval in d['a'].items():
            terms.append(sp.Rational(int(cval.p), int(cval.q))
                         * thL_s**i1 * v_s**i2 * K3_s**i3)
        for (i1, i2, i3), cval in d['b'].items():
            terms.append(sp.Rational(int(cval.p), int(cval.q)) * r3_s
                         * thL_s**i1 * v_s**i2 * K3_s**i3)
        return sp.Add(*terms)

    def sign_q3(cc):
        a = cc.coeff(r3_s, 0)
        b = cc.coeff(r3_s, 1)
        if a >= 0 and b >= 0:
            return 1 if (a > 0 or b > 0) else 0
        if a <= 0 and b <= 0:
            return -1
        if a >= 0:
            return 1 if a**2 > 3*b**2 else (-1 if a**2 < 3*b**2 else 0)
        return -1 if a**2 > 3*b**2 else (1 if a**2 < 3*b**2 else 0)

    def factor_all_positive(expr, name):
        factors = sp.factor_list(sp.factor(expr))
        content = sp.expand(factors[0])
        cs = sign_q3(content) if content.has(r3_s) else (
            1 if content > 0 else (-1 if content < 0 else 0))
        total_neg = 0
        for f, ex in factors[1]:
            P = sp.Poly(sp.expand(f), thL_s, v_s, K3_s)
            neg = sum(1 for _, cc in P.terms()
                      if (sign_q3(sp.expand(cc)) if cc.has(r3_s)
                          else (1 if cc > 0 else -1)) < 0)
            if neg == len(P.terms()):
                total_neg += ex
            elif neg > 0:
                print(f"  {name}: MIXED ({neg}/{len(P.terms())})", flush=True)
                return False
        ok = cs * (-1) ** total_neg > 0
        print(f"  {name}: {'OK' if ok else 'BAD'} "
              f"({time.time()-t0:.0f}s)", flush=True)
        return ok

    allok = True
    for k2 in sorted(ycoeffs):
        allok &= factor_all_positive(to_sympy(ycoeffs[k2]), f"c{k2}")

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    json.dump({"j": J, "far_below_factored": bool(allok),
               "engine": "farbelow2-flint-build",
               "command": f"KNIFE_J={J} python lab/knife_farbelow2.py",
               "git": git, "runtime_s": round(time.time() - t0, 1)},
              open(RES / f"knife{J}_farbelow_factored.json", "w"), indent=1)
    print(f"FAR-BELOW(j={J}) " + ("CLOSED" if allok else "OPEN"), flush=True)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
