"""Exact positivity: Sturm sign counts, Bernstein certificates, and honest verdicts.

Three levels of answer, and the tool always says which one it reached:

* **manifest** — every monomial of the polynomial is nonnegative on the orthant, so
  positivity is immediate. Cheapest and strongest.
* **Bernstein** — after a change to the Bernstein basis on a box, every coefficient is
  nonnegative. A certificate on that box, and nothing outside it.
* **Sturm** — an exact root count on an interval. Decisive in one variable.

If none succeeds the answer is `inconclusive`, never `refuted`: failing to certify is
not the same as being false, and conflating the two is how a wall gets invented where
there is only a gap.
"""

from __future__ import annotations

from math import comb
from typing import Any

from flint import fmpq, fmpq_poly

from .core import Result, timed


def _poly(coeffs: Any) -> fmpq_poly:
    out = []
    for c in coeffs:
        if isinstance(c, fmpq):
            out.append(c)
        elif isinstance(c, str) and "/" in c:
            a, b = c.split("/")
            out.append(fmpq(int(a), int(b)))
        elif isinstance(c, float):
            raise TypeError("float coefficient given to an exact tool")
        else:
            out.append(fmpq(int(c)))
    return fmpq_poly(out)


def sturm_chain(p: fmpq_poly) -> list[fmpq_poly]:
    chain = [p, p.derivative()]
    while chain[-1].degree() > 0:
        r = chain[-2] % chain[-1]
        if r == 0:
            break
        chain.append(-r)
    return chain


def _sign_changes(chain: list[fmpq_poly], x: fmpq) -> int:
    vals = [q(x) for q in chain]
    vals = [v for v in vals if v != 0]
    return sum(1 for i in range(len(vals) - 1) if (vals[i] > 0) != (vals[i + 1] > 0))


def sturm_roots(coeffs: Any, lo: Any = 0, hi: Any = 1) -> Result:
    """Exact count of distinct real roots in (lo, hi]. No floating point anywhere."""
    tm = timed()
    p = _poly(coeffs)
    a = fmpq(lo) if not isinstance(lo, fmpq) else lo
    b = fmpq(hi) if not isinstance(hi, fmpq) else hi
    chain = sturm_chain(p)
    n = _sign_changes(chain, a) - _sign_changes(chain, b)
    return Result(
        tool="sturm_roots",
        inputs={"degree": p.degree(), "lo": str(a), "hi": str(b)},
        status="ok",
        evidence_kind="CERTIFICATE",
        data={"distinct_real_roots_in_interval": n, "chain_length": len(chain)},
        runtime_s=tm.stop(),
    )


def sturm_sign(coeffs: Any, lo: Any = 0, hi: Any = 1) -> Result:
    """Does the polynomial keep one sign on [lo, hi]? Exact, via a root count."""
    tm = timed()
    p = _poly(coeffs)
    a = fmpq(lo) if not isinstance(lo, fmpq) else lo
    b = fmpq(hi) if not isinstance(hi, fmpq) else hi
    roots = sturm_roots(coeffs, a, b)
    n = roots.data["distinct_real_roots_in_interval"]
    va, vb = p(a), p(b)
    same = (va > 0 and vb > 0) or (va < 0 and vb < 0)
    verdict = "constant sign" if (n == 0 and same) else "sign change or root inside"
    return Result(
        tool="sturm_sign",
        inputs={"degree": p.degree(), "lo": str(a), "hi": str(b)},
        status="ok" if n == 0 and same else "inconclusive",
        evidence_kind="CERTIFICATE",
        data={
            "roots_inside": n,
            "value_at_lo": str(va),
            "value_at_hi": str(vb),
            "verdict": verdict,
            "sign": 1 if va > 0 else (-1 if va < 0 else 0),
        },
        runtime_s=tm.stop(),
    )


def bernstein_coefficients(coeffs: Any, lo: Any = 0, hi: Any = 1) -> list[fmpq]:
    """Coefficients in the Bernstein basis of [lo, hi]; nonnegativity certifies the box."""
    p = _poly(coeffs)
    a = fmpq(lo) if not isinstance(lo, fmpq) else lo
    b = fmpq(hi) if not isinstance(hi, fmpq) else hi
    n = p.degree()
    # p(a + (b-a) u) as a polynomial in u
    shifted = fmpq_poly([a, b - a])
    q = fmpq_poly([0])
    pw = fmpq_poly([1])
    for k in range(n + 1):
        q = q + pw * p[k]
        pw = pw * shifted
    c = [q[k] for k in range(n + 1)]
    # b_i = SUM_{j<=i} C(i,j)/C(n,j) c_j -- the standard power-to-Bernstein change of
    # basis. Writing C(j,i)/C(n,i) here instead is a silent no-op for j < i and was
    # caught only because a test demanded that x^2 - x + 1 be certified on [0,1].
    return [sum(fmpq(comb(i, j), comb(n, j)) * c[j] for j in range(0, i + 1)) for i in range(n + 1)]


def bernstein_certificate(coeffs: Any, lo: Any = 0, hi: Any = 1) -> Result:
    """Nonnegative Bernstein coefficients on [lo, hi] certify nonnegativity there."""
    tm = timed()
    bc = bernstein_coefficients(coeffs, lo, hi)
    neg = [i for i, v in enumerate(bc) if v < 0]
    return Result(
        tool="bernstein_certificate",
        inputs={"lo": str(lo), "hi": str(hi), "degree": len(bc) - 1},
        status="ok" if not neg else "inconclusive",
        evidence_kind="CERTIFICATE",
        data={
            "coefficients": [str(v) for v in bc],
            "negative_indices": neg,
            "certified_nonnegative_on_box": not neg,
            "note": "negative Bernstein coefficients do NOT refute positivity; subdivide",
        },
        runtime_s=tm.stop(),
    )


def verify_polynomial_positive(
    coeffs: Any, lo: Any = 0, hi: Any = 1, subdivisions: int = 4
) -> Result:
    """Escalate: manifest monomial signs, then Bernstein, then Bernstein on subdivisions.

    Returns the cheapest level that succeeded, and `inconclusive` if none did.
    """
    tm = timed()
    p = _poly(coeffs)
    mono_neg = [k for k in range(p.degree() + 1) if p[k] < 0]
    if not mono_neg:
        return Result(
            tool="verify_polynomial_positive",
            inputs={"lo": str(lo), "hi": str(hi)},
            status="ok",
            evidence_kind="CERTIFICATE",
            data={"level": "manifest", "note": "all monomials nonnegative on the orthant"},
            runtime_s=tm.stop(),
        )
    b = bernstein_certificate(coeffs, lo, hi)
    if b.status == "ok":
        return Result(
            tool="verify_polynomial_positive",
            inputs={"lo": str(lo), "hi": str(hi)},
            status="ok",
            evidence_kind="CERTIFICATE",
            data={"level": "bernstein", "negative_monomials": len(mono_neg)},
            runtime_s=tm.stop(),
        )
    a0 = fmpq(lo) if not isinstance(lo, fmpq) else lo
    b0 = fmpq(hi) if not isinstance(hi, fmpq) else hi
    pieces, ok = [], True
    for i in range(subdivisions):
        left = a0 + (b0 - a0) * fmpq(i, subdivisions)
        right = a0 + (b0 - a0) * fmpq(i + 1, subdivisions)
        r = bernstein_certificate(coeffs, left, right)
        pieces.append({"box": [str(left), str(right)], "certified": r.status == "ok"})
        ok = ok and r.status == "ok"
    return Result(
        tool="verify_polynomial_positive",
        inputs={"lo": str(lo), "hi": str(hi), "subdivisions": subdivisions},
        status="ok" if ok else "inconclusive",
        evidence_kind="CERTIFICATE",
        data={"level": "bernstein_subdivided" if ok else "none", "pieces": pieces},
        warnings=[]
        if ok
        else ["not certified; this is NOT a refutation -- subdivide further or look for a root"],
        runtime_s=tm.stop(),
    )
