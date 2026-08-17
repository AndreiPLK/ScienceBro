"""Independent validation of numerical claims in projects/qg-bootstrap/paper/main.tex.

FRESH implementation written by the independent validator from the formulas
stated in the paper (Eq. (1) residue, angle substitution, Gegenbauer/Legendre
projection) and in the validation task. It deliberately imports NOTHING from
projects/qg-bootstrap/lab.

All arithmetic is exact (fractions.Fraction). Signs of partial-wave
coefficients are computed up to positive normalization only (l-dependent
positive constants of the orthogonal-polynomial expansion are irrelevant for
sign statements and exact zeros).

Conventions used (from paper Sec. 2):
  R(n,t) = (2+r+t)_{n-1} (1+r+t+w)(1+n+r+w) / ((2+r)_n (1+r+w))
  t = alpha(x-1) - mu0,  alpha = (n-3*mu0)/2      (mu0 = 0 everywhere below)
  a_{n,l}  propto  Integral_{-1}^{1} R(x) G_l(x) (1-x^2)^{(D-4)/2} dx
      with G_l = Legendre P_l for D=4, Gegenbauer C_l^{(D-3)/2} for D=6.

q-clock (task item 4, CHR Eq. 16 at r=w=0):
  roots xi = [-1]_q and [-1-k]_q for k=1..n-1, with [m]_q = (q^m-1)/(q-1)
  R_q(n,t) = prod (t - xi)   (monic; positive prefactor assumed)
  t = [n]_q (x-1)/2
"""

import random
import sys
from fractions import Fraction as F

# ----------------------------------------------------------------------
# polynomial helpers: a polynomial is a list of Fractions, index = power of x
# ----------------------------------------------------------------------


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
    return out


def pmul_many(factors):
    out = [F(1)]
    for f in factors:
        out = pmul(out, f)
    return out


def pscale(a, c):
    return [c * ai for ai in a]


# ----------------------------------------------------------------------
# orthogonal polynomials (rational coefficients)
# ----------------------------------------------------------------------


def legendre(l):
    """Legendre P_l as coefficient list, exact."""
    if l == 0:
        return [F(1)]
    pm, p = [F(1)], [F(0), F(1)]
    for k in range(1, l):
        # (k+1) P_{k+1} = (2k+1) x P_k - k P_{k-1}
        xp = [F(0)] + p
        nxt = [F(0)] * (len(xp))
        for i, c in enumerate(xp):
            nxt[i] += F(2 * k + 1, k + 1) * c
        for i, c in enumerate(pm):
            nxt[i] -= F(k, k + 1) * c
        pm, p = p, nxt
    return p


def gegenbauer(l, alpha):
    """Gegenbauer C_l^{(alpha)} as coefficient list, exact (alpha Fraction)."""
    if l == 0:
        return [F(1)]
    cm, c = [F(1)], [F(0), 2 * alpha]
    for k in range(1, l):
        # (k+1) C_{k+1} = 2(k+alpha) x C_k - (k+2alpha-1) C_{k-1}
        xp = [F(0)] + c
        nxt = [F(0)] * (len(xp))
        A = F(2) * (k + alpha) / (k + 1)
        B = (k + 2 * alpha - 1) / F(k + 1)
        for i, ci in enumerate(xp):
            nxt[i] += A * ci
        for i, ci in enumerate(cm):
            nxt[i] -= B * ci
        cm, c = c, nxt
    return c


# ----------------------------------------------------------------------
# exact monomial integrals with weight (1-x^2)^p on [-1,1], integer p >= 0
# ----------------------------------------------------------------------


def mono_int(m, p):
    if m % 2 == 1:
        return F(0)
    # binomial expansion of (1-x^2)^p, exact
    total = F(0)
    binom = 1
    for j in range(p + 1):
        total += F((-1) ** j * binom * 2, m + 2 * j + 1)
        binom = binom * (p - j) // (j + 1)
    return total


def project(poly, l, D):
    """sign-faithful partial-wave coefficient: int R * G_l * (1-x^2)^{(D-4)/2}."""
    assert (D - 4) % 2 == 0 and D >= 4
    p = (D - 4) // 2
    G = legendre(l) if D == 4 else gegenbauer(l, F(D - 3, 2))
    prod = pmul(poly, G)
    return sum(c * mono_int(m, p) for m, c in enumerate(prod))


# ----------------------------------------------------------------------
# residue polynomials
# ----------------------------------------------------------------------


def residue_q1(n, r, w, mu0=F(0)):
    """R(n,t(x)) as polynomial in x, q=1, paper Eq. (1); includes prefactor."""
    alpha = (F(n) - 3 * mu0) / 2
    # t(x) = alpha*x + (-alpha - mu0)
    t0, t1 = -alpha - mu0, alpha
    factors = []
    for j in range(n - 1):  # (2+r+t)_{n-1}
        factors.append([t0 + 2 + r + j, t1])
    factors.append([t0 + 1 + r + w, t1])  # (1+r+t+w)
    poly = pmul_many(factors)
    poch = F(1)
    for j in range(n):  # (2+r)_n
        poch *= 2 + r + j
    pref = (1 + n + r + w) / (poch * (1 + r + w))
    return pscale(poly, pref)


def qbracket(m, q):
    """[m]_q = (q^m - 1)/(q - 1), exact for rational q != 1; m may be negative."""
    if q == 1:
        return F(m)
    return (q**m - 1) / (q - 1)


def residue_qclock(n, q):
    """Monic q-residue at r=w=0: prod over roots (t - xi), t = [n]_q (x-1)/2."""
    h = qbracket(n, q) / 2
    t0, t1 = -h, h  # t(x) = h*x - h
    roots = [qbracket(-1, q)] + [qbracket(-1 - k, q) for k in range(1, n)]
    factors = [[t0 - xi, t1] for xi in roots]
    return pmul_many(factors)


def sgn(x):
    return (x > 0) - (x < 0)


# ----------------------------------------------------------------------
# checks
# ----------------------------------------------------------------------
results = []


def record(item, name, ok, detail):
    results.append((item, name, ok, detail))
    print(f"[item {item}] {'PASS' if ok else 'FAIL'}  {name}: {detail}")


def check1():
    r, w = F(-13, 25), F(1, 2)
    vals = {}
    for n in (24, 25, 26):
        vals[n] = project(residue_q1(n, r, w), n - 1, 4)
    ok = vals[24] > 0 and vals[25] == 0 and vals[26] < 0
    detail = (
        f"a_24,23={vals[24]} (>0? {vals[24] > 0}); "
        f"a_25,24={vals[25]} (==0? {vals[25] == 0}); "
        f"a_26,25={vals[26]} (<0? {vals[26] < 0})"
    )
    record(1, "edge razor (r,w)=(-13/25,1/2)", ok, detail)


def check2():
    rng = random.Random(20260814)  # frozen seed, declared before running
    n_pts, ok_all, details = 10, True, []
    got = 0
    while got < n_pts:
        r = F(rng.randint(-60, 60), rng.randint(1, 30))
        w = F(rng.randint(-60, 60), rng.randint(1, 30))
        if not (2 + r > 0 and 1 + r + w > 0):
            continue
        got += 1
        a20 = project(residue_q1(2, r, w), 0, 4)
        law = 3 * (1 + r) * (r + w) + 1
        agree = sgn(a20) == sgn(law)
        ok_all &= agree
        details.append(
            f"(r={r},w={w}): sgn a20={sgn(a20)}, sgn law={sgn(law)} {'OK' if agree else 'MISMATCH'}"
        )
    record(2, "a_{2,0} sign law at 10 random rational points", ok_all, "; ".join(details))


def check3():
    r = F(-3, 5)
    ok_all, details = True, []
    for i in range(9):
        w = F(10 + i, 10)  # w = 1, 11/10, ..., 9/5
        nstar = 10 + i  # n = 10w  (integer by construction)
        first_neg = None
        marginal_zero = None
        pos_before = True
        for n in range(1, nstar + 2):
            a = project(residue_q1(n, r, w), n - 1, 4)
            if n < nstar and a <= 0:
                pos_before = False
            if n == nstar:
                marginal_zero = a == 0
            if a < 0 and first_neg is None:
                first_neg = n
        ok = pos_before and marginal_zero and first_neg == nstar + 1
        ok_all &= ok
        details.append(
            f"w={w}: pos n<{nstar}:{pos_before}, "
            f"a_{{{nstar},{nstar - 1}}}==0:{marginal_zero}, "
            f"first neg n={first_neg} (expect {nstar + 1})"
            f" {'OK' if ok else 'MISMATCH'}"
        )
    record(3, "nine casualties at r=-3/5, first negative at n=10w+1", ok_all, "; ".join(details))


def first_negative_qclock(q, nmax):
    for n in range(1, nmax + 1):
        poly = residue_qclock(n, q)
        for l in range(0, n + 1):
            if project(poly, l, 4) < 0:
                return (n, l)
    return None


def check4():
    fn65 = first_negative_qclock(F(6, 5), 6)
    fn1110 = first_negative_qclock(F(11, 10), 8)
    fn1 = first_negative_qclock(F(1), 15)
    ok = (fn65 == (3, 0)) and (fn1110 == (4, 1)) and (fn1 is None)
    detail = (
        f"q=6/5 first neg {fn65} (expect (3,0)); "
        f"q=11/10 first neg {fn1110} (expect (4,1)); "
        f"q=1 first neg up to n=15: {fn1} (expect None)"
    )
    record(4, "q-clock spot checks", ok, detail)


def check5():
    a = project(residue_q1(10, F(-3, 5), F(1)), 9, 6)
    ok = a == 0
    record(
        5,
        "D=6 exact zero a_{10,9} at (r,w)=(-3/5,1)",
        ok,
        f"a_10,9 (D=6, Gegenbauer alpha=3/2) = {a} (==0? {ok})",
    )


if __name__ == "__main__":
    check1()
    check2()
    check3()
    check4()
    check5()
    n_fail = sum(1 for _, _, ok, _ in results if not ok)
    print()
    print(f"TOTAL: {len(results)} items, {len(results) - n_fail} pass, {n_fail} fail")
    sys.exit(1 if n_fail else 0)
