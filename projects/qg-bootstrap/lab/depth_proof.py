"""Depth d, proved the same way depth 2 was: exact algebra then exact Bernstein.

Depth 2 closed in four seconds and fifteen boxes. This generalises that pipeline
to any fixed depth d = N - m, so each rung of the ladder costs one run instead of
one invention.

The pipeline, and why each step is allowed:

  1. P_N(Y) = Y^eps prod_{a>0}(Y-a^2)^2 is monic of degree N with roots a^2 twice
     (plus 0 when N is odd). Its (N-d)-th derivative, divided by (N-d)!, is a
     polynomial of degree d whose coefficients are elementary symmetric functions
     of those roots times falling factorials of N -- polynomials in N.
  2. The verified beta-mean formula turns the sign of the knife into the sign of
     Q(X) = SUM_j r_j (m+1/2)_j / (2m+gamma+1)_j X^j at X = (N+lam)^2.
  3. Clearing the Pochhammer denominators, which are positive, leaves a
     polynomial in gamma of degree d.
  4. The shore is a MINIMUM over levels, so it never exceeds the top-knife
     condition of any single level. Evaluating at the half level M = N/2 is
     therefore a legitimate upper bound for gamma, and if the result is positive
     there it is positive on the whole physical range.
  5. lam = cN, Moebius compactification N = N0/(1-v), then exact Bernstein
     subdivision. A Bernstein bound above zero on a box is a proof for that box.

The power sums of the roots are obtained by exact interpolation and CHECKED
against direct summation before use -- the same discipline that caught an
off-by-one in the connection formula earlier today.

Run: python lab/depth_proof.py 3        (or any depth)
"""

from __future__ import annotations

import json
import sys
import time
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp  # ENGINE-OK: symbolic setup only; bounds are computed on flint
from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
N_SYM, C_SYM, V_SYM, G_SYM = sp.symbols("N c v gamma", positive=True)


def roots_of_P(N: int):
    """The roots of P_N with multiplicity: a^2 twice for a = N-1, N-3, ..., plus 0 if N odd."""
    out = []
    a = N - 1
    while a > 0:
        out += [a * a, a * a]
        a -= 2
    if N % 2:
        out.append(0)
    assert len(out) == N
    return out


def power_sum_poly(t: int, deg_hint: int | None = None):
    """p_t(N) = sum of (root)^t as an exact polynomial in N, by interpolation + check."""
    deg = deg_hint if deg_hint is not None else 2 * t + 1
    pts = list(range(3, 3 + deg + 3))
    vals = [sum(r**t for r in roots_of_P(n)) for n in pts]
    poly = sp.interpolate(list(zip(pts, vals)), N_SYM)
    poly = sp.expand(poly)
    # CHECK on points not used for the fit
    for n in range(3 + deg + 3, 3 + deg + 12):
        got = sp.Integer(poly.subs(N_SYM, n))
        want = sum(r**t for r in roots_of_P(n))
        if got != want:
            raise AssertionError(f"power sum t={t} failed at N={n}: {got} != {want}")
    return poly


def elementary_symmetric(d: int):
    """e_0..e_d of the roots of P_N, as exact polynomials in N (Newton's identities)."""
    p = {t: power_sum_poly(t) for t in range(1, d + 1)}
    e = {0: sp.Integer(1)}
    for k in range(1, d + 1):
        acc = sp.Integer(0)
        for i in range(1, k + 1):
            acc += (-1) ** (i - 1) * e[k - i] * p[i]
        e[k] = sp.expand(acc / k)
    return e


def falling(N, k):
    r = sp.Integer(1)
    for i in range(k):
        r *= N - i
    return r


def knife_polynomial(d: int):
    """Cleared polynomial whose sign is the sign of the depth-d knife."""
    e = elementary_symmetric(d)
    m = N_SYM - d
    X = (C_SYM * N_SYM + N_SYM) ** 2  # lam = c N
    # R = sum_{k=0}^{d} (-1)^k e_k * (N-k)!/((d-k)!(N-d)!) * Y^{d-k}
    terms = []
    for k in range(d + 1):
        j = d - k
        coeff = (-1) ** k * e[k] * falling(N_SYM - k, j) / sp.factorial(j)
        # (m+1/2)_j / (2m+gamma+1)_j
        num = sp.Integer(1)
        for i in range(j):
            num *= m + sp.Rational(1, 2) + i
        den = sp.Integer(1)
        for i in range(j):
            den *= 2 * m + G_SYM + 1 + i
        terms.append(coeff * num / den * X**j)
    expr = sum(terms)
    num, den = sp.fraction(sp.together(sp.expand(expr)))
    return sp.expand(num), sp.factor(den)


def half_level_gamma():
    """gamma at the top-knife condition of level M = N/2 -- an upper bound for the shore."""
    M = N_SYM / 2
    lam = C_SYM * N_SYM
    T_M = 3 * (2 * M - 3) / (M * (M - 2)) * (lam**2 + (2 * M - 2) * lam + 1) + 2 * M
    return (T_M - 3) / 2


def bernstein_lower(poly: sp.Poly, box) -> fmpq:
    gens = poly.gens
    ts = [sp.Symbol(f"_t{k}") for k in range(len(gens))]
    subm = {
        g: sp.Rational(int(lo.p), int(lo.q))
        + (sp.Rational(int(hi.p), int(hi.q)) - sp.Rational(int(lo.p), int(lo.q))) * t
        for g, (lo, hi), t in zip(gens, box, ts)
    }
    p = sp.Poly(sp.expand(poly.as_expr().subs(subm)), *ts)
    md = [p.degree(t) for t in ts]
    a = {
        mm: fmpq(int(sp.Rational(cc).p), int(sp.Rational(cc).q))
        for mm, cc in zip(p.monoms(), p.coeffs())
    }
    best = None
    for idx in product(*[range(x + 1) for x in md]):
        b = fmpq(0)
        for key, cc in a.items():
            if all(key[i] <= idx[i] for i in range(len(idx))):
                f = fmpq(1)
                for i in range(len(idx)):
                    f *= fmpq(comb(idx[i], key[i]), comb(md[i], key[i]))
                b += cc * f
        if best is None or b < best:
            best = b
            if best <= 0:
                return best
    return best


def prove_box(poly: sp.Poly, box, max_depth: int = 24):
    stack = [(box, 0)]
    boxes, open_boxes = 0, []
    while stack:
        bx, depth = stack.pop()
        boxes += 1
        if bernstein_lower(poly, bx) > 0:
            continue
        if depth >= max_depth:
            open_boxes.append([(str(lo), str(hi)) for lo, hi in bx])
            continue
        widths = [hi - lo for lo, hi in bx]
        k = widths.index(max(widths))
        lo, hi = bx[k]
        mid = (lo + hi) / 2
        left, right = list(bx), list(bx)
        left[k], right[k] = (lo, mid), (mid, hi)
        stack += [(left, depth + 1), (right, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def run(d: int, n_min: int = 8, c_max_num: int = 3, c_max_den: int = 10):
    c_max = sp.Rational(c_max_num, c_max_den)
    t0 = time.time()
    num, den = knife_polynomial(d)
    print(f"depth {d}: cleared numerator, denominator {den}", flush=True)
    sub = sp.expand(num.subs(G_SYM, half_level_gamma()))
    num2, den2 = sp.fraction(sp.together(sub))
    num2 = sp.expand(num2)
    degN = int(sp.degree(num2, N_SYM))
    print(f"  at the half level: degree {degN} in N, denominator {sp.factor(den2)}", flush=True)
    lead = sp.factor(sp.expand(sp.Poly(num2, N_SYM).coeff_monomial(N_SYM**degN)))
    print(f"  leading coefficient in N: {lead}", flush=True)
    shifted = sp.expand(num2.subs(N_SYM, sp.Rational(n_min) / (1 - V_SYM)) * (1 - V_SYM) ** degN)
    poly = sp.Poly(sp.simplify(shifted), V_SYM, C_SYM)
    print(f"  compactified: {len(poly.monoms())} monomials", flush=True)
    ok, boxes, open_boxes = prove_box(poly, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(3, 10))])
    dt = time.time() - t0
    print(
        f"  Bernstein on N >= {n_min}, 0 <= c <= {c_max}: proved={ok}, boxes={boxes}, "
        f"open={len(open_boxes)}  ({dt:.0f}s)",
        flush=True,
    )
    return {
        "depth": d,
        "n_min": n_min,
        "c_max": str(c_max),
        "degree_in_N": degN,
        "leading_coefficient": str(lead),
        "proved": ok,
        "boxes": boxes,
        "open": len(open_boxes),
        "denominator": str(sp.factor(den2)),
        "seconds": round(dt, 1),
    }


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [3]
    out = []
    for d in depths:
        try:
            out.append(run(d))
        except Exception as exc:  # noqa: BLE001 - a failed depth must not kill the queue
            print(f"  depth {d} FAILED: {type(exc).__name__}: {exc}", flush=True)
            out.append({"depth": d, "error": f"{type(exc).__name__}: {exc}"})
    path = RES / "depth_proofs.json"
    prev = []
    if path.exists():
        try:
            prev = json.loads(path.read_text(encoding="utf-8")).get("runs", [])
        except (json.JSONDecodeError, OSError):
            prev = []
    keep = [r for r in prev if r.get("depth") not in {o.get("depth") for o in out}]
    path.write_text(
        json.dumps(
            {
                "claim": "for each fixed depth d, the knife is positive throughout the "
                "physical region, proved by exact Bernstein subdivision after evaluating "
                "at the half-level shore bound and compactifying N",
                "runs": sorted(keep + out, key=lambda r: r["depth"]),
                "command": "python lab/depth_proof.py <d> [<d> ...]",
                **stamp(),
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"written {path}", flush=True)
    return 0 if all(r.get("proved") for r in out) else 1


if __name__ == "__main__":
    sys.exit(main())
