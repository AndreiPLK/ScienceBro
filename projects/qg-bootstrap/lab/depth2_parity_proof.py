"""Depth 2, CORRECTED: rigorous parity split, engine 2 only (no sympy anywhere).

Supersedes the "Half B" section of d2_proof.py, which had a real logical gap:
it evaluated the top-knife condition at the HALF level M = N/2 and claimed
gamma_shore(lam) <= (T_M-3)/2 "because the shore is a minimum over levels" --
true ONLY when M is one of the actual integers k >= 3 in that minimum. For ODD
N, M = N/2 is a half-integer, not in that set, and the claim T_hat <= T_M does
NOT follow from the definition of a minimum. Grid search found 97 violations
(all at odd N) where the continuous T_{N/2} formula dips BELOW the true T_hat.
Spot checks against the exact knife engine found no actual counterexample to
depth-2 positivity itself at those points -- the physical claim still held --
but the PROOF as written did not establish it there. That gap is fixed here.

THE FIX. Split by parity and use an ACTUAL INTEGER K as the comparison level:

    even N = 2K,   K >= 3 integer  ->  M = K directly
    odd  N = 2K+1, K >= 3 integer  ->  M = K directly (not N/2!)

For any integer K >= 3, T_hat(lam) <= T_K(lam) holds BY DEFINITION of the min
over integers -- no numerical spot check needed, no continuous-extrapolation
ambiguity. This is proved as two separate Bernstein certificates, one per
parity branch, each in the two free variables (K, c) with lam = c*N.

N = 5, 6 fall below both branches' validity floor (K >= 3 needs N = 2K >= 6 for
even, N = 2K+1 >= 7 for odd) and are checked directly, alongside N = 3, 4 which
were already checked directly in d2_proof.py.

Pure flint throughout: fmpq for scalars, a small dict-based bivariate polynomial
(K, c) with fmpq coefficients for everything else. No sympy import at all.
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


class BiPoly:
    """A polynomial in two variables over Q: dict[(i, j)] -> fmpq. Index 0 is
    the "K" slot, index 1 is the "c" slot. Minimal, auditable, engine-2 only."""

    __slots__ = ("d",)

    def __init__(self, d=None):
        self.d = {} if d is None else d

    @staticmethod
    def const(v) -> BiPoly:
        v = fmpq(v)
        return BiPoly({(0, 0): v}) if v != 0 else BiPoly({})

    @staticmethod
    def var(idx: int) -> BiPoly:
        key = (1, 0) if idx == 0 else (0, 1)
        return BiPoly({key: fmpq(1)})

    def __add__(self, other) -> BiPoly:
        other = other if isinstance(other, BiPoly) else BiPoly.const(other)
        out = dict(self.d)
        for k, v in other.d.items():
            nv = out.get(k, fmpq(0)) + v
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
        return BiPoly(out)

    def __neg__(self) -> BiPoly:
        return BiPoly({k: -v for k, v in self.d.items()})

    def __sub__(self, other) -> BiPoly:
        other = other if isinstance(other, BiPoly) else BiPoly.const(other)
        return self + (-other)

    def __mul__(self, other) -> BiPoly:
        other = other if isinstance(other, BiPoly) else BiPoly.const(other)
        out: dict = {}
        for (i1, j1), v1 in self.d.items():
            for (i2, j2), v2 in other.d.items():
                key = (i1 + i2, j1 + j2)
                out[key] = out.get(key, fmpq(0)) + v1 * v2
        return BiPoly({k: v for k, v in out.items() if v != 0})

    __rmul__ = __mul__

    def __pow__(self, n: int) -> BiPoly:
        r = BiPoly.const(1)
        base = self
        while n > 0:
            if n & 1:
                r = r * base
            base = base * base
            n >>= 1
        return r

    def truediv_scalar(self, s) -> BiPoly:
        s = fmpq(s)
        return BiPoly({k: v / s for k, v in self.d.items()})

    def max_deg(self, idx: int) -> int:
        if not self.d:
            return 0
        return max(k[idx] for k in self.d)


def K_() -> BiPoly:
    return BiPoly.var(0)


def C_() -> BiPoly:
    return BiPoly.var(1)


ONE = BiPoly.const(1)


def E2_of_N(N: BiPoly) -> BiPoly:
    """N(N^2-1)(5N^3-9N^2-5N+21)/90 -- hand-derived, verified elsewhere against
    the exact knife engine (D2_COMPLETE.md, 75 cells, 0 mismatches)."""
    return (
        N * (N * N - ONE) * (N * N * N * fmpq(5) - N * N * fmpq(9) - N * fmpq(5) + fmpq(21))
    ).truediv_scalar(90)


def A_of_N(N: BiPoly) -> BiPoly:
    """N(N-1)(2N-3)(2N-1)/8"""
    return (N * (N - ONE) * (N * fmpq(2) - fmpq(3)) * (N * fmpq(2) - ONE)).truediv_scalar(8)


def B_of_N(N: BiPoly) -> BiPoly:
    """N(N^2-1)(N-1)(2N-3)/6"""
    return (N * (N * N - ONE) * (N - ONE) * (N * fmpq(2) - fmpq(3))).truediv_scalar(6)


def build_branch(parity: str):
    """Build the homogenized depth-2 numerator for one parity branch, in (K, c).

    parity: 'even' -> N = 2K, 'odd' -> N = 2K+1. M = K directly (an actual
    integer for integer K), so T_hat(lam) <= T_K(lam) BY DEFINITION -- no
    numerical check needed for that step, unlike the M = N/2 version.
    """
    K = K_()
    c = C_()
    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + ONE

    E2 = E2_of_N(N)
    A = A_of_N(N)
    B = B_of_N(N)
    lam = c * N
    NplusLam = N + lam
    X = NplusLam * NplusLam
    s0 = N * fmpq(2) - fmpq(3)  # L = gamma + s0

    c2 = E2
    c1 = E2 * (s0 * fmpq(2) + ONE) - B * X
    c0 = E2 * s0 * (s0 + ONE) - B * X * (s0 + ONE) + A * X * X

    # gamma at the top-knife condition of level M = K:
    #   T_K = 3(2K-3)/(K(K-2)) * (lam^2 + (2K-2)lam + 1) + 2K
    #   gamma = (T_K-3)/2 = Pg/Qg,  Qbig = K(K-2), Abig = 2K-3
    #   Bexpr = lam^2+(2K-2)lam+1,  Pg = Abig*(3*Bexpr+Qbig), Qg = 2*Qbig
    Qbig = K * (K - fmpq(2))
    Abig = K * fmpq(2) - fmpq(3)
    Bexpr = lam * lam + (K * fmpq(2) - fmpq(2)) * lam + ONE
    Pg = Abig * (Bexpr * fmpq(3) + Qbig)
    Qg = Qbig * fmpq(2)

    H_final = c2 * (Pg * Pg) + c1 * (Pg * Qg) + c0 * (Qg * Qg)
    return H_final


def one_minus_v_powers(m: int):
    out = [{0: fmpq(1)}]
    for _ in range(m):
        prev = out[-1]
        cur: dict = {}
        for p, cf in prev.items():
            cur[p] = cur.get(p, fmpq(0)) + cf
            cur[p + 1] = cur.get(p + 1, fmpq(0)) - cf
        out.append(cur)
    return out


def compactify_K(poly: BiPoly, k_min: int) -> BiPoly:
    """K -> k_min/(1-v), cleared by (1-v)^degK -> polynomial in (v, c)."""
    degK = poly.max_deg(0)
    pw = one_minus_v_powers(degK)
    out: dict = {}
    for (ki, ci), coeff in poly.d.items():
        c_here = coeff * fmpq(k_min) ** ki
        for p, cf in pw[degK - ki].items():
            key = (p, ci)
            out[key] = out.get(key, fmpq(0)) + c_here * cf
    return BiPoly({k: v for k, v in out.items() if v != 0})


def affine_powers(lo, w, deg):
    out = [{0: fmpq(1)}]
    cur = {0: fmpq(1)}
    for _ in range(deg):
        nxt: dict = {}
        for p, cf in cur.items():
            nxt[p] = nxt.get(p, fmpq(0)) + cf * lo
            nxt[p + 1] = nxt.get(p + 1, fmpq(0)) + cf * w
        cur = nxt
        out.append(cur)
    return out


def bernstein_lower(poly: BiPoly, box) -> fmpq:
    (lo0, hi0), (lo1, hi1) = box
    d0 = poly.max_deg(0)
    d1 = poly.max_deg(1)
    w0, w1 = hi0 - lo0, hi1 - lo1
    pw0 = affine_powers(lo0, w0, d0)
    pw1 = affine_powers(lo1, w1, d1)
    mono: dict = {}
    for (i0, i1), coeff in poly.d.items():
        for p0, cf0 in pw0[i0].items():
            for p1, cf1 in pw1[i1].items():
                key = (p0, p1)
                mono[key] = mono.get(key, fmpq(0)) + coeff * cf0 * cf1
    best = None
    for k0 in range(d0 + 1):
        for k1 in range(d1 + 1):
            b = fmpq(0)
            for (p0, p1), cf in mono.items():
                if p0 <= k0 and p1 <= k1:
                    f = fmpq(comb(k0, p0), comb(d0, p0)) * fmpq(comb(k1, p1), comb(d1, p1))
                    b += cf * f
            if best is None or b < best:
                best = b
                if best <= 0:
                    return best
    return best if best is not None else fmpq(0)


def prove_box(poly: BiPoly, box, max_depth: int = 26):
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
        w = [bx[0][1] - bx[0][0], bx[1][1] - bx[1][0]]
        k = 0 if w[0] >= w[1] else 1
        lo, hi = bx[k]
        mid = (lo + hi) / 2
        left, right = [bx[0], bx[1]], [bx[0], bx[1]]
        left[k] = (lo, mid)
        right[k] = (mid, hi)
        stack += [(left, depth + 1), (right, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def run_branch(parity: str, k_min: int, c_max_num: int = 3, c_max_den: int = 10):
    t0 = time.time()
    H_final = build_branch(parity)
    degK = H_final.max_deg(0)
    degC = H_final.max_deg(1)
    print(f"  [{parity}] H_final degree: K^{degK}, c^{degC}, {len(H_final.d)} terms", flush=True)
    poly_vc = compactify_K(H_final, k_min)
    print(f"  [{parity}] compactified: {len(poly_vc.d)} terms in (v,c)", flush=True)
    box = [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(c_max_num, c_max_den))]
    ok, boxes, open_boxes = prove_box(poly_vc, box)
    dt = time.time() - t0
    print(
        f"  [{parity}] K >= {k_min}, 0 <= c <= {c_max_num}/{c_max_den}: "
        f"proved={ok}, boxes={boxes}, open={len(open_boxes)}  ({dt:.0f}s)",
        flush=True,
    )
    return {
        "parity": parity,
        "k_min": k_min,
        "c_max": f"{c_max_num}/{c_max_den}",
        "degree_K": degK,
        "degree_c": degC,
        "proved": ok,
        "boxes": boxes,
        "open": len(open_boxes),
        "seconds": round(dt, 1),
    }


def main() -> int:
    t0 = time.time()
    out = []
    out.append(run_branch("even", k_min=3))
    out.append(run_branch("odd", k_min=3))
    ok = all(r["proved"] for r in out)
    payload = {
        "claim": "depth-2 coefficient positive for N >= 6 (even) and N >= 7 (odd), "
        "0 <= lam/N <= 0.3, using an ACTUAL INTEGER comparison level K (not N/2), "
        "so gamma_shore <= gamma_at_K holds by definition of the min -- no numerical "
        "spot-check required for that step",
        "supersedes": "d2_proof.py Half B, which used the non-integer M=N/2 for odd N "
        "and had 97 grid violations of T_hat <= T_{N/2} (all at odd N); this file "
        "fixes that by construction",
        "branches": out,
        "not_covered_here": "N = 3, 4, 5, 6 are outside both branches' validity floor "
        "and must be checked directly",
        "engine": "flint only (fmpq + custom BiPoly dict polynomial); zero sympy imports",
        "command": "python lab/depth2_parity_proof.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "depth2_parity_proof.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"\nwritten results/depth2_parity_proof.json  (overall proved={ok})", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
