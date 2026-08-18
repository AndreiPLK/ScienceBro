"""FASTNUM: the flint engine with the conveniences I kept reaching Fraction for.

Reason this exists, stated plainly. The fast-engine law kept being broken not
because I disagreed with it but because the correct path had friction and the
wrong one had none: `from fractions import Fraction` is a reflex, while fmpq
lacks the small conveniences (constructing from a sympy Rational, from a string,
from a float ratio) that a prototype needs. A law that fights a reflex loses.

So the fix is to remove the friction: everything below returns flint types, and
the module is a one-line import at the top of any new computational file.

    from fastnum import Q, to_Q, poly_coeffs

`Q` is fmpq. Nothing here reimplements arithmetic -- it only makes the fast
engine as easy to reach as the slow one.
"""

from __future__ import annotations

from flint import fmpq, fmpq_poly, fmpz

Q = fmpq
Z = fmpz
QPoly = fmpq_poly


def to_Q(x) -> fmpq:
    """A rational from almost anything: int, Fraction, sympy Rational, 'p/q'."""
    if isinstance(x, fmpq):
        return x
    if isinstance(x, int):
        return fmpq(x)
    p, q = getattr(x, "p", None), getattr(x, "q", None)  # sympy Rational
    if p is not None and q is not None:
        return fmpq(int(p), int(q))
    num, den = getattr(x, "numerator", None), getattr(x, "denominator", None)
    if num is not None and den is not None:  # fractions.Fraction
        return fmpq(int(num), int(den))
    if isinstance(x, str):
        if "/" in x:
            a, b = x.split("/")
            return fmpq(int(a), int(b))
        return fmpq(int(x))
    raise TypeError(f"cannot convert {type(x).__name__} to an exact rational")


def poly_coeffs(expr, *gens) -> dict:
    """{exponent tuple: Q} from a sympy expression, on the fast engine."""
    import sympy as sp

    p = sp.Poly(sp.expand(expr), *gens)
    return {m: to_Q(sp.Rational(c)) for m, c in zip(p.monoms(), p.coeffs())}


def rising(a, k: int) -> fmpq:
    """Rising factorial (a)_k with exact rational a."""
    a = to_Q(a)
    v = fmpq(1)
    for i in range(k):
        v *= a + fmpq(i)
    return v
