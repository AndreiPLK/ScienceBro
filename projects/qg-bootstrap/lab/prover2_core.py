"""Prover v2 core: exact certificates over Q(sqrt3) on the flint engine.

Replaces the sympy algebra layer of the knife provers:
  - Q3Poly: multivariate polynomial A + B*sqrt(3), A/B dense-dict fmpq coeffs
    backed by flint fmpq for all arithmetic (C-speed exact rationals).
  - bernstein_certify: per-variable Bernstein coefficients on [0,1]^d with
    optional degree elevation; positivity via the exact a+b*sqrt3 sign test.
  - from_sympy: one-time converter for polynomials built symbolically.

Design contract (validated against prover v1 artifacts cell-by-cell):
  same certificates, same cell logic, only the arithmetic engine changes.
"""

from __future__ import annotations

from flint import fmpq

QZERO = fmpq(0)
THREE = fmpq(3)


def _binom_table(nmax):
    C = [[fmpq(0)] * (nmax + 1) for _ in range(nmax + 1)]
    for i in range(nmax + 1):
        C[i][0] = fmpq(1)
        for q in range(1, i + 1):
            C[i][q] = C[i - 1][q - 1] + C[i - 1][q]
    return C


_BINOM = _binom_table(160)


def binom(i, q):
    return _BINOM[i][q]


class QPoly:
    """Dense-dict multivariate polynomial: {exponent-tuple: fmpq}."""

    __slots__ = ("nv", "c")

    def __init__(self, nv, c=None):
        self.nv = nv
        self.c = c if c is not None else {}

    @classmethod
    def const(cls, nv, val):
        v = fmpq(val)
        return cls(nv, {} if v == QZERO else {(0,) * nv: v})

    @classmethod
    def var(cls, nv, idx):
        e = [0] * nv
        e[idx] = 1
        return cls(nv, {tuple(e): fmpq(1)})

    def copy(self):
        return QPoly(self.nv, dict(self.c))

    def __add__(self, o):
        r = dict(self.c)
        for e, v in o.c.items():
            s = r.get(e, QZERO) + v
            if s == QZERO:
                r.pop(e, None)
            else:
                r[e] = s
        return QPoly(self.nv, r)

    def __sub__(self, o):
        r = dict(self.c)
        for e, v in o.c.items():
            s = r.get(e, QZERO) - v
            if s == QZERO:
                r.pop(e, None)
            else:
                r[e] = s
        return QPoly(self.nv, r)

    def __neg__(self):
        return QPoly(self.nv, {e: -v for e, v in self.c.items()})

    def __mul__(self, o):
        if isinstance(o, fmpq) or isinstance(o, int):
            v0 = fmpq(o)
            if v0 == QZERO:
                return QPoly(self.nv)
            return QPoly(self.nv, {e: v * v0 for e, v in self.c.items()})
        r = {}
        for e1, v1 in self.c.items():
            for e2, v2 in o.c.items():
                e = tuple(a + b for a, b in zip(e1, e2))
                s = r.get(e, QZERO) + v1 * v2
                if s == QZERO:
                    r.pop(e, None)
                else:
                    r[e] = s
        return QPoly(self.nv, r)

    __rmul__ = __mul__

    def pow(self, k, cache=None):
        if k == 0:
            return QPoly.const(self.nv, 1)
        if cache is not None and k in cache:
            return cache[k]
        half = self.pow(k // 2, cache)
        r = half * half
        if k % 2:
            r = r * self
        if cache is not None:
            cache[k] = r
        return r

    def degree(self, idx):
        return max((e[idx] for e in self.c), default=0)

    def scale_denominators(self):
        """Multiply by the LCM of denominators (positive) — sign-preserving."""
        if not self.c:
            return self
        from math import lcm

        L = 1
        for v in self.c.values():
            L = lcm(L, int(v.q))
        if L == 1:
            return self
        return self * fmpq(L)


class Q3Poly:
    """A + B*sqrt(3) with A, B QPoly."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=None):
        self.a = a
        self.b = b if b is not None else QPoly(a.nv)

    @classmethod
    def const(cls, nv, val, val3=0):
        return cls(QPoly.const(nv, val), QPoly.const(nv, val3))

    @classmethod
    def var(cls, nv, idx):
        return cls(QPoly.var(nv, idx))

    @property
    def nv(self):
        return self.a.nv

    def __add__(self, o):
        if isinstance(o, (int, fmpq)):
            o = Q3Poly.const(self.nv, o)
        return Q3Poly(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        if isinstance(o, (int, fmpq)):
            o = Q3Poly.const(self.nv, o)
        return Q3Poly(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return (-self) + o

    def __neg__(self):
        return Q3Poly(-self.a, -self.b)

    def __mul__(self, o):
        if isinstance(o, (int, fmpq)):
            return Q3Poly(self.a * o, self.b * o)
        return Q3Poly(self.a * o.a + THREE * (self.b * o.b), self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def pow(self, k, cache=None):
        if k == 0:
            return Q3Poly.const(self.nv, 1)
        if cache is not None and k in cache:
            return cache[k]
        half = self.pow(k // 2, cache)
        r = half * half
        if k % 2:
            r = r * self
        if cache is not None:
            cache[k] = r
        return r

    def is_rational(self):
        return not self.b.c


def sign_q3(a, b):
    """Exact sign of a + b*sqrt(3), a,b fmpq. Returns -1/0/1."""
    if a >= 0 and b >= 0:
        return 0 if (a == 0 and b == 0) else 1
    if a <= 0 and b <= 0:
        return -1
    aa, bb = a * a, THREE * b * b
    if a >= 0:  # b < 0
        return 1 if aa > bb else (-1 if aa < bb else 0)
    return -1 if aa > bb else (1 if aa < bb else 0)


def _bern_matrix(d):
    """Lower-triangular M[i][q] = C(i,q)/C(d,q); b = M c (per variable)."""
    return [[binom(i, q) / binom(d, q) for q in range(i + 1)] for i in range(d + 1)]


_BM_CACHE = {}


def bern_matrix(d):
    M = _BM_CACHE.get(d)
    if M is None:
        M = _bern_matrix(d)
        _BM_CACHE[d] = M
    return M


def _bern_axis(coeffs, axis, deg):
    """Bernstein transform along one axis of a dense-dict poly {exp: fmpq}."""
    M = bern_matrix(deg)
    fibers = {}
    for e, val in coeffs.items():
        key = e[:axis] + e[axis + 1 :]
        fibers.setdefault(key, {})[e[axis]] = val
    out = {}
    for key, fib in fibers.items():
        for i in range(deg + 1):
            s = QZERO
            Mi = M[i]
            for q, cq in fib.items():
                if q <= i:
                    s += Mi[q] * cq
            if s != QZERO:
                e = key[:axis] + (i,) + key[axis:]
                out[e] = s
    return out


def bernstein_certify(p3, elev=0):
    """All Bernstein coefficients of A + B*sqrt3 on [0,1]^nv nonnegative?

    Transforms A and B jointly (paired axis transform) so the exact
    sign test sees matching (a, b) pairs. Returns (ok, n_neg_checked).
    """
    nv = p3.nv
    A, B = dict(p3.a.c), dict(p3.b.c)
    for axis in range(nv):
        d = max(max((e[axis] for e in A), default=0), max((e[axis] for e in B), default=0)) + elev
        A = _bern_axis(A, axis, d)
        B = _bern_axis(B, axis, d)
    ok = True
    for e in set(A) | set(B):
        if sign_q3(A.get(e, QZERO), B.get(e, QZERO)) < 0:
            ok = False
            break
    return ok


def orthant_certify(p3):
    """All raw coefficients nonnegative (positivity on the whole orthant)."""
    A, B = p3.a.c, p3.b.c
    for e in set(A) | set(B):
        if sign_q3(A.get(e, QZERO), B.get(e, QZERO)) < 0:
            return False
    return True


def from_sympy(expr, gens):
    """Convert an expanded sympy expression to Q3Poly (gens -> var order).

    # ENGINE-OK: this is the ONE-TIME boundary the fast-engine law allows --
    a polynomial built symbolically ELSEWHERE (by hand, once, not in a loop)
    is parsed here exactly once and handed off to flint (Q3Poly/fmpq) for all
    subsequent bulk work (bernstein_certify etc). sympy never touches a
    growing object and never runs more than once per polynomial.
    """
    import sympy as sp

    r3 = sp.sqrt(3)
    e2 = sp.expand(expr)
    a_part = e2.coeff(r3, 0)
    b_part = e2.coeff(r3, 1)
    nv = len(gens)

    def build(part):
        if part == 0:
            return QPoly(nv)
        P = sp.Poly(part, *gens)
        c = {}
        for mon, cc in P.terms():
            c[tuple(mon)] = (
                fmpq(int(sp.nsimplify(cc).p), int(sp.nsimplify(cc).q)) if cc.is_Rational else None
            )
            if c[tuple(mon)] is None:
                raise ValueError(f"non-rational coeff {cc}")
        return QPoly(nv, c)

    return Q3Poly(build(a_part), build(b_part))
