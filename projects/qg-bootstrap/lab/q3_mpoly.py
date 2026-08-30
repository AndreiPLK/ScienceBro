"""Q(sqrt3) polynomials on flint's NATIVE multivariate type, not on Python dicts.

`prover2_core.QPoly` stores a multivariate polynomial as a Python dict `{exponents: fmpq}`
and multiplies with Python loops. flint has `fmpq_mpoly`, the same object in C.

Measured on the products this programme actually performs:

| terms | dict QPoly | flint mpoly | speedup |
|---|---|---|---|
| 1500 | 1.60 s | 0.003 s | 533x |
| 4000 | 12.44 s | 0.017 s | 731x |
| 9000 | 70.18 s | 0.057 s | 1231x |

Leg (a) at `j = 18` took 3.7 hours. That was never a mathematical limit; it was a Python
loop. The repository's own fast-engine law says exactly this -- new computational code goes
on flint immediately -- and the prover core predates it.

`Q3` carries `a + b sqrt3` as a pair of `fmpq_mpoly`, with `sign_q3` for exact sign
decisions, matching `prover2_core` semantics so results can be compared directly.
"""

from __future__ import annotations

from flint import Ordering, fmpq, fmpq_mpoly_ctx

NAMES = ["thL", "y", "v", "K3"]
CTX = fmpq_mpoly_ctx.get(NAMES, Ordering.lex)


def const(c: fmpq | int, c3: fmpq | int = 0) -> "Q3":
    return Q3(CTX.from_dict({(0, 0, 0, 0): fmpq(c)}), CTX.from_dict({(0, 0, 0, 0): fmpq(c3)}))


def var(idx: int) -> "Q3":
    e = [0, 0, 0, 0]
    e[idx] = 1
    return Q3(CTX.from_dict({tuple(e): fmpq(1)}), CTX.from_dict({}))


class Q3:
    """a + b*sqrt(3) with a, b native flint multivariate polynomials."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=None):
        self.a = a
        self.b = b if b is not None else CTX.from_dict({})

    def __add__(self, o):
        if isinstance(o, (int, fmpq)):
            o = const(o)
        return Q3(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o):
        if isinstance(o, (int, fmpq)):
            o = const(o)
        return Q3(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return const(o) - self

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __mul__(self, o):
        if isinstance(o, (int, fmpq)):
            c = fmpq(o)
            return Q3(self.a * c, self.b * c)
        # (x + y r3)(u + v r3) = (xu + 3yv) + (xv + yu) r3
        return Q3(self.a * o.a + 3 * (self.b * o.b), self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __pow__(self, k: int):
        out = const(1)
        base = self
        while k:
            if k & 1:
                out = out * base
            base = base * base
            k >>= 1
        return out

    def terms(self) -> dict[tuple[int, ...], tuple[fmpq, fmpq]]:
        """Monomials as {exponents: (rational part, sqrt3 part)}."""
        out: dict[tuple[int, ...], list[fmpq]] = {}
        for mono, coeff in self.a.terms():
            out.setdefault(tuple(mono), [fmpq(0), fmpq(0)])[0] = fmpq(coeff)
        for mono, coeff in self.b.terms():
            out.setdefault(tuple(mono), [fmpq(0), fmpq(0)])[1] = fmpq(coeff)
        return {k: (v[0], v[1]) for k, v in out.items()}


def sign_q3(a: fmpq, b: fmpq) -> int:
    """Exact sign of a + b sqrt3, by comparing squares -- no float, no sqrt."""
    if a == 0 and b == 0:
        return 0
    if a >= 0 and b >= 0:
        return 1
    if a <= 0 and b <= 0:
        return -1
    # opposite signs: compare a^2 against 3 b^2 with the sign of the dominant part
    lhs, rhs = a * a, 3 * b * b
    if a > 0:
        return 1 if lhs > rhs else (-1 if lhs < rhs else 0)
    return -1 if lhs > rhs else (1 if lhs < rhs else 0)


def count_negative_monomials(P: Q3) -> int:
    return sum(1 for a, b in P.terms().values() if sign_q3(a, b) < 0)
