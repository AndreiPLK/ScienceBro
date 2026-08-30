"""Leg (a) certificates on flint's native multivariate type.

Same mathematics as `farbelow_coeff_signs.py`, same verified coefficient formula, same
exact `Q(sqrt3)` arithmetic — but the polynomials are `fmpq_mpoly` in C instead of Python
dicts. Measured on this programme's own products, that is a 500x to 1200x difference, and
leg (a) at `j = 18` took 3.7 hours under the old representation.

The two structural facts found on 30 August are used as well: the `A_r` form an arithmetic
progression, so every elementary symmetric function of a tail comes from shared powers of
`A_0` and `2 den` weighted by integer coefficients; and the factors depending only on `i`
are hoisted out of the `(k, i)` loop.

Validation is against the old module's published artefacts, not against itself.

Run: KNIFE_J=20 [V_OFFSET=k] python lab/leg_a_flint.py
     -> results/leg_a_flint_j<J>[_v<k>].json
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import q3_mpoly as Q  # noqa: E402
from provenance import stamp  # noqa: E402
from sciencebro_math.families import centered_squares, esym  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J = int(os.environ.get("KNIFE_J", "12"))


def E_poly_in_n(t: int) -> fmpq_poly:
    """E_t = e_t of the centred spectrum, as an exact polynomial in n, by interpolation.

    Verified past its own nodes, so an interpolation that had gone wrong cannot pass.
    """
    start = max(6, t + 2)
    deg = 3 * t + 2
    xs = list(range(start, start + deg + 1))
    ys = [fmpq(esym(centered_squares(x))[t]) for x in xs]
    out = fmpq_poly([0])
    for i, (xi, yi) in enumerate(zip(xs, ys, strict=True)):
        num, den = fmpq_poly([1]), fmpq(1)
        for j2, xj in enumerate(xs):
            if i != j2:
                num = num * fmpq_poly([-xj, 1])
                den *= fmpq(xi - xj)
        out = out + num * (yi / den)
    for x in range(start + deg + 1, start + deg + 5):
        assert out(fmpq(x)) == fmpq(esym(centered_squares(x))[t]), (t, x)
    return out


def subst(p: fmpq_poly, arg: Q.Q3) -> Q.Q3:
    """Evaluate a univariate polynomial at a Q3 argument, by Horner."""
    acc = Q.const(0)
    for k in range(p.degree(), -1, -1):
        acc = acc * arg + Q.const(p[k])
    return acc


def region(v_offset: int = 0):
    thL, y, v, K3 = (Q.var(i) for i in range(4))
    v = v + v_offset
    kk = v + K3 + 53
    m = v + 41
    n = m + 3
    den = kk * (kk - 2)
    lam = Q.Q3(Q.CTX.from_dict({}), ((v + K3 + 51 + thL) * fmpq(1, 3)).a)
    lam2 = lam * lam
    tk = (kk * 2 - 3) * 3 * (lam2 + (kk * 2 - 2) * lam + 1) + (kk * 2) * kk * (kk - 2)
    return lam, tk - y * den, den, m, n, y


def bernstein_in_thL(terms: dict) -> dict:
    """Change to the Bernstein basis along thL, which lives on [0, 1].

    b_i = SUM_{q<=i} C(i,q)/C(d,q) c_q, applied fibre by fibre in the other three
    variables. This is the escalation the repair certificate already uses, and the only
    variable it can be applied to, the rest being unbounded.
    """
    from math import comb

    d = max((e[0] for e in terms), default=0)
    fib: dict[tuple[int, ...], dict[int, tuple[fmpq, fmpq]]] = {}
    for e, ab in terms.items():
        fib.setdefault(e[1:], {})[e[0]] = ab
    out: dict[tuple[int, ...], tuple[fmpq, fmpq]] = {}
    for rest, col in fib.items():
        for i in range(d + 1):
            sa = sb = fmpq(0)
            for q, (a, b) in col.items():
                if q <= i:
                    w = fmpq(comb(i, q), comb(d, q))
                    sa += w * a
                    sb += w * b
            if sa != 0 or sb != 0:
                out[(i,) + rest] = (sa, sb)
    return out


def main() -> int:
    t0 = time.time()
    v_offset = int(os.environ.get("V_OFFSET", "0"))
    lam, D_num, den, m_expr, n_expr, y = region(v_offset)
    s = lam + (n_expr - 1)
    c_const = (n_expr * 4) - 4 * J - 1
    tk = D_num + y * den
    A0 = tk + den * c_const
    d = den * 2
    M = J - 2

    A0p, dp = [Q.const(1)], [Q.const(1)]
    for _ in range(M + 2):
        A0p.append(A0p[-1] * A0)
        dp.append(dp[-1] * d)
    denp, s2p = [Q.const(1)], [Q.const(1)]
    s2 = s * s
    for _ in range(J + 1):
        denp.append(denp[-1] * den)
        s2p.append(s2p[-1] * s2)

    ST: dict[int, list[fmpq_poly]] = {}
    for i in range(M + 1):
        acc = [fmpq_poly([1])] + [fmpq_poly([0])] * (M - i + 1)
        for r in range(i, M + 1):
            term = fmpq_poly([r, 1])
            for q in range(M - i + 1, 0, -1):
                acc[q] = acc[q] + acc[q - 1] * term
        ST[i] = acc

    def esym_tail(i: int, m: int) -> Q.Q3:
        if i > M:
            return Q.const(1) if m == 0 else Q.const(0)
        if m < 0 or m > M - i + 1:
            return Q.const(0)
        S = ST[i][m]
        acc = Q.const(0)
        for jj in range(S.degree() + 1):
            cj = S[jj]
            if cj != 0:
                acc = acc + (dp[m - jj] * A0p[jj]) * cj
        return acc

    poch = []
    for i in range(J):
        acc = Q.const(1)
        for q in range(1, 2 * i + 1):
            acc = acc * (n_expr * 2 - 2 * J + q)
        poch.append(acc * fmpq(1, math.factorial(i) * 2**i))

    Ev = [subst(E_poly_in_n(t), n_expr) for t in range(J)]
    W = [Ev[J - 1 - i] * poch[i] * s2p[i] * denp[i] for i in range(J)]

    rows = []
    for k in range(J):
        acc = Q.const(0)
        for i in range(J - k):
            m = J - 1 - i - k
            if m < 0 or (i <= M and m > M - i + 1):
                continue
            term = W[i] * esym_tail(i, m)
            acc = acc + term if i % 2 == 0 else acc - term
        if (J - 1 + k) % 2:
            acc = Q.const(0) - acc
        acc = acc * denp[k]
        terms = acc.terms()
        neg = sum(1 for a, b in terms.values() if Q.sign_q3(a, b) < 0)
        row = {"k": k, "monomials": len(terms), "negative": neg}
        # Same escalation the repair certificate uses: when monomial signs are not enough,
        # change to the Bernstein basis in thL, which is the only bounded variable.
        if neg and k not in (J - 2,):
            bt = bernstein_in_thL(terms)
            bneg = sum(1 for a, b in bt.values() if Q.sign_q3(a, b) < 0)
            row["bernstein_thL"] = {"coefficients": len(bt), "negative": bneg,
                                    "certified": bneg == 0}
        rows.append(row)

    def still_bad(r: dict) -> bool:
        if not r["negative"] or r["k"] in (J - 2, J - 3):
            return False
        b = r.get("bernstein_thL")
        return not (b and b["certified"])

    off = [r for r in rows if still_bad(r)]
    out = {
        "j": J,
        "v_offset": v_offset,
        "engine": "flint fmpq_mpoly over Q(sqrt3); the dict-based QPoly is 500-1200x slower",
        "coefficients": rows,
        "negatives_outside_excluded_indices": off,
        "leg_a_holds": not off,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    name = f"leg_a_flint_j{J}" + (f"_v{v_offset}" if v_offset else "") + ".json"
    (RES / name).write_text(json.dumps(out, indent=2), encoding="utf-8")
    negs = {r["k"]: r["negative"] for r in rows if r["negative"]}
    print(f"[j={J}] negatives by k: {negs}   leg (a) holds: {not off}   ({out['runtime_s']}s)")
    return 0 if not off else 1


if __name__ == "__main__":
    raise SystemExit(main())
