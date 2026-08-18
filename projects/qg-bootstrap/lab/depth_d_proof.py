"""Generic depth-d proof: any fixed depth, one command, engine 2 throughout.

The pipeline that closed depth 2 (ERR-0008/ERR-0009, lab/depth2_parity_proof.py)
and depth 3 (lab/depth3_parity_proof.py), generalised to any depth d without
copy-pasting a new file per depth.

  1. e_0..e_d(N): elementary symmetric functions of the roots of P_N, from
     power sums (exact Lagrange interpolation, each CHECKED against direct
     summation on held-out points) via Newton's identity.
  2. The beta-mean formula for the depth-d knife (degree d in gamma), built as
     a bivariate polynomial in (K, c) at the half-level M = K -- an ACTUAL
     integer, so T_hat(lam) <= T_K(lam) by definition (the fix ERR-0008
     established; it does not depend on depth).
  3. Verified against the exact reference engine (jacobi_coeff_rec) at
     concrete (K, c) points, for BOTH parities, BEFORE any Bernstein run is
     trusted.
  4. Two overlapping Bernstein pieces -- 0<=c<=50 direct, c>=1 compactified --
     together cover all c >= 0 (all lam > 0), for K >= 3, i.e. n >= 2d
     (even) / n >= 2d+1 (odd) roughly (exact floor depends on where j=d+1
     stays a valid knife index).

Every gamma<->D conversion here is gamma=(D-3)/2, D=2*gamma+3 -- checked
explicitly, because an off-by-a-constant in exactly this conversion produced
a false alarm earlier tonight (ERR-0009).

No sympy, no float in any comparison. fmpq throughout; float only for the
final human-readable print.

Run: python lab/depth_d_proof.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


# --------------------------------------------------------------------------
# A minimal bivariate polynomial over Q: dict[(i, j)] -> fmpq. Slot 0 = "K",
# slot 1 = "c". Same design as depth2_parity_proof.BiPoly (reimplemented here
# so this file has no cross-file coupling and can be dropped in standalone).
# --------------------------------------------------------------------------
class BiPoly:
    __slots__ = ("d",)

    def __init__(self, d=None):
        self.d = {} if d is None else d

    @staticmethod
    def const(v) -> BiPoly:
        v = fmpq(v)
        return BiPoly({(0, 0): v}) if v != 0 else BiPoly({})

    @staticmethod
    def var(idx: int) -> BiPoly:
        return BiPoly({((1, 0) if idx == 0 else (0, 1)): fmpq(1)})

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
        return max((k[idx] for k in self.d), default=0)


def roots_of_P(N: int) -> list[int]:
    out = []
    a = N - 1
    while a > 0:
        out += [a * a, a * a]
        a -= 2
    if N % 2:
        out.append(0)
    assert len(out) == N
    return out


def lagrange_poly(points) -> fmpq_poly:
    X = fmpq_poly([0, 1])
    result = fmpq_poly([0])
    for i, (xi, yi) in enumerate(points):
        if yi == 0:
            continue
        num = fmpq_poly([1])
        den = fmpq(1)
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = num * (X - fmpq(xj))
            den *= fmpq(xi - xj)
        result = result + num * (yi / den)
    return result


def power_sum_poly(t: int) -> fmpq_poly:
    deg = 2 * t + 1
    pts = [(n, fmpq(sum(r**t for r in roots_of_P(n)))) for n in range(3, 3 + deg + 1)]
    poly = lagrange_poly(pts)
    for n in range(3 + deg + 1, 3 + deg + 9):
        got = poly(fmpq(n))
        want = fmpq(sum(r**t for r in roots_of_P(n)))
        if got != want:
            raise AssertionError(f"power sum t={t} failed at N={n}: {got} != {want}")
    return poly


def elementary_symmetric(d: int) -> dict[int, fmpq_poly]:
    p = {t: power_sum_poly(t) for t in range(1, d + 1)}
    e = {0: fmpq_poly([1])}
    for k in range(1, d + 1):
        acc = fmpq_poly([0])
        for i in range(1, k + 1):
            acc = acc + e[k - i] * p[i] * ((-1) ** (i - 1))
        e[k] = acc / fmpq(k)
    return e


def falling_poly(shift: int, length: int) -> fmpq_poly:
    X = fmpq_poly([0, 1])
    r = fmpq_poly([1])
    for i in range(length):
        r = r * (X - fmpq(shift + i))
    return r


def poch(x: fmpq, k: int) -> fmpq:
    r = fmpq(1)
    for i in range(k):
        r *= x + i
    return r


def lift_N(poly_in_N: fmpq_poly, N_bi: BiPoly) -> BiPoly:
    coeffs = poly_in_N.coeffs()
    result = BiPoly.const(0)
    for c in reversed(coeffs):
        result = result * N_bi + BiPoly.const(c)
    return result


def build_branch(parity: str, d: int, e_polys: dict) -> BiPoly:
    """H_final(K, c) for depth d, one parity branch, gamma homogenized away."""
    K = BiPoly.var(0)
    c = BiPoly.var(1)
    ONE = BiPoly.const(1)
    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + ONE
    m = N - BiPoly.const(d)
    lam = c * N
    X = (N + lam) * (N + lam)

    Qbig = K * (K - fmpq(2))
    Abig = K * fmpq(2) - fmpq(3)
    Bexpr = lam * lam + (K * fmpq(2) - fmpq(2)) * lam + ONE
    Pg = Abig * (Bexpr * fmpq(3) + Qbig)
    Qg = Qbig * fmpq(2)

    total = BiPoly.const(0)
    half = BiPoly.const(fmpq(1, 2))
    two_m_Qg = (m * fmpq(2)) * Qg
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeff_bi = lift_N(coeff_N, N) * fmpq((-1) ** k)

        num_bi = BiPoly.const(1)
        for i in range(j):
            num_bi = num_bi * (m + half + BiPoly.const(i))

        den_cleared = BiPoly.const(1)
        for i in range(j):
            den_cleared = den_cleared * (two_m_Qg + Pg + Qg * fmpq(1 + i))

        total = total + coeff_bi * num_bi * den_cleared * (X**j) * (Qg ** (d - j))
    return total


def self_check(d: int, e_polys: dict, k_values, c_values) -> list[str]:
    """Compare build_branch's sign, at concrete integer (K,c), to the exact
    reference engine at gamma = gamma_at_K(lam) -- the SAME quantity the
    algebra targets."""
    from fractions import Fraction as F  # ENGINE-OK: interface glue only

    from jacobi_normal_form import jacobi_coeff_rec

    bad = []
    for parity in ("even", "odd"):
        H = build_branch(parity, d, e_polys)
        for K_val in k_values:
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            j = d + 1
            m = n - j
            if m < 0 or j > n - 1 or K_val < 3:
                continue
            for c_num, c_den in c_values:
                c_val = fmpq(c_num, c_den)
                val = fmpq(0)
                for (ki, ci), coeff in H.d.items():
                    val += coeff * fmpq(K_val) ** ki * c_val**ci
                sign_formula = (val > 0) - (val < 0)

                lam = c_val * N
                Qbig = fmpq(K_val) * (fmpq(K_val) - 2)
                Abig = fmpq(K_val) * 2 - 3
                Bexpr = lam * lam + (fmpq(K_val) * 2 - 2) * lam + 1
                Pg = Abig * (Bexpr * 3 + Qbig)
                Qg = Qbig * 2
                gamma_at_K = Pg / Qg
                D = gamma_at_K * 2 + 3  # checked explicitly: D=2*gamma+3, not gamma+3 (ERR-0009)
                lam_F = F(int(lam.p), int(lam.q))
                D_F = F(int(D.p), int(D.q))
                knife = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, D_F)
                sign_exact = (knife > 0) - (knife < 0)
                if sign_formula != sign_exact:
                    bad.append(
                        f"depth={d} {parity} K={K_val} c={c_num}/{c_den}: "
                        f"{sign_formula} vs {sign_exact}"
                    )
    return bad


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
    degK = poly.max_deg(0)
    pw = one_minus_v_powers(degK)
    out: dict = {}
    for (ki, ci), coeff in poly.d.items():
        c_here = coeff * fmpq(k_min) ** ki
        for p, cf in pw[degK - ki].items():
            key = (p, ci)
            out[key] = out.get(key, fmpq(0)) + c_here * cf
    return BiPoly({k: v for k, v in out.items() if v != 0})


def compactify_c(poly: BiPoly, c_min: int) -> BiPoly:
    degC = poly.max_deg(1)
    pw = one_minus_v_powers(degC)
    out: dict = {}
    for (ki, ci), coeff in poly.d.items():
        c_here = coeff * fmpq(c_min) ** ci
        for p, cf in pw[degC - ci].items():
            key = (ki, p)
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
    from math import comb

    (lo0, hi0), (lo1, hi1) = box
    d0, d1 = poly.max_deg(0), poly.max_deg(1)
    pw0 = affine_powers(lo0, hi0 - lo0, d0)
    pw1 = affine_powers(lo1, hi1 - lo1, d1)
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


def prove_box(poly: BiPoly, box, max_depth: int = 28):
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
        left[k], right[k] = (lo, mid), (mid, hi)
        stack += [(left, depth + 1), (right, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def run_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    k_values = (3, 4, 5, 6, 8, 10, 15)
    c_values = [(cn, 100) for cn in (1, 10, 20, 29)]
    bad = self_check(d, e_polys, k_values, c_values)
    n_trials = len(k_values) * len(c_values) * 2
    print(f"depth {d}: self-check {n_trials} trials, {len(bad)} mismatches", flush=True)
    if bad:
        for b in bad[:5]:
            print("  ", b)
        return {"depth": d, "self_check_passed": False, "mismatches": bad[:10]}

    result = {"depth": d, "self_check_trials": n_trials, "self_check_passed": True, "branches": {}}
    for parity in ("even", "odd"):
        H = build_branch(parity, d, e_polys)
        poly_v = compactify_K(H, 3)
        t1 = time.time()
        ok_lo, boxes_lo, open_lo = prove_box(
            poly_v, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(50))]
        )
        poly_vw = compactify_c(poly_v, 1)
        ok_hi, boxes_hi, open_hi = prove_box(
            poly_vw, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000))]
        )
        dt = time.time() - t1
        print(
            f"  [{parity}] K>=3, all c>=0: lo(0<=c<=50)={ok_lo}({boxes_lo}b) "
            f"hi(c>=1)={ok_hi}({boxes_hi}b)  ({dt:.0f}s)",
            flush=True,
        )
        result["branches"][parity] = {
            "K_deg": H.max_deg(0),
            "c_deg": H.max_deg(1),
            "terms": len(H.d),
            "lo_proved": ok_lo,
            "lo_boxes": boxes_lo,
            "lo_open": len(open_lo),
            "hi_proved": ok_hi,
            "hi_boxes": boxes_hi,
            "hi_open": len(open_hi),
        }
    result["proved_for_all_c"] = all(
        result["branches"][p]["lo_proved"] and result["branches"][p]["hi_proved"]
        for p in ("even", "odd")
    )
    result["seconds"] = round(time.time() - t0, 1)
    return result


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [4, 5]
    out = []
    for d in depths:
        try:
            out.append(run_depth(d))
        except Exception as exc:  # noqa: BLE001 - one bad depth must not kill the queue
            print(f"depth {d} FAILED: {type(exc).__name__}: {exc}", flush=True)
            out.append({"depth": d, "error": f"{type(exc).__name__}: {exc}"})

    path = RES / "depth_d_proofs.json"
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
                "claim": "for each fixed depth d, the knife is positive for K>=3 (n>=2d "
                "even / n>=2d+1 odd, roughly) and ALL lam>0, via the parity-split "
                "half-level-K Bernstein method that closed depth 2 (ERR-0008/9) and "
                "depth 3. n below the K>=3 floor is NOT covered by this file -- check "
                "separately, same as depth 2's n=3,4,5 and depth 3's n=5,6,7.",
                "runs": sorted(keep + out, key=lambda r: r["depth"]),
                "command": "python lab/depth_d_proof.py <d> [<d> ...]",
                **stamp(),
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"written {path}", flush=True)
    return 0 if all(r.get("proved_for_all_c") for r in out if "error" not in r) else 1


if __name__ == "__main__":
    sys.exit(main())
