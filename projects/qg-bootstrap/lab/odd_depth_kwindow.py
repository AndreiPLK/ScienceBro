"""The repaired odd-depth statement, in critical-curve coordinates (ERR-0013).

The fixed v-window form of step (a) is FALSE at odd depths
(results/odd_depth_window_refuted.json): even-order knives have thresholds,
and away from the argmin of T_k the window point overshoots them. What the
argument actually needs is positivity in a window of FIXED width in k-units
around the CONTINUOUS minimiser k*(lam) -- the integer argmin is within 1 of
k* (unimodality + bracketing, proved for lam >= 7 in UNGLUED_KEYSTONE.md), so
|delta| <= 3/2 suffices with margin.

COORDINATES. The critical curve dT/dk = 0 is
    P(k, lam) = -3 a(k) lam^2 + 3 b(k) lam + c0(k) = 0,
    a = k^2-3k+3,  b = k^2-6k+6,  c0 = k^4-4k^3+k^2+9k-9,
quadratic in lam with discriminant 9b^2 + 12 a c0 = 3 k^2 (k-2)^2 (4k^2-12k+3).
Writing w = sqrt(3(4k^2-12k+3)) >= 0 (a CONIC in (k, w), rational point
(3, 3)), the physical branch is
    lam*(k) = (3 b + k(k-2) w) / (6 a),
positive and ~ k/sqrt(3) for large k. Every quantity in the knife then
becomes polynomial in (K, k, delta, w) after clearing the POSITIVE
denominators N^*, lam^*, (6a)^*, and reducing w^2 -> 3(4k^2-12k+3):
    G = A(K, k, delta) + B(K, k, delta) * w,   sign(G) = sign(knife)
at level N (= 2K or 2K+1), lam = lam*(k), shore integer k_s = k + delta.

BUILT BY SUBSTITUTION, NOT RE-DERIVED (the ERR-0012 rule). The validated
`build_branch` H(K, c, v) is substituted with c = lam/N, v = k_s/lam:
    G0 = N^deg_c(H) * lam^deg_v(H) * H  is polynomial in (K, lam, k_s),
then lam -> (3b + k(k-2)w)/(6a) cleared by (6a)^deg_lam(G0), k_s -> k+delta,
and w^2 reduced. Nothing is re-derived, so nothing new can be mis-derived.

SELF-CHECK (ERR-0011/0012 rules: wide ranges, and reference signs that
actually go negative). Rational points on the conic come from the line
through (3,3):  k(t) = 3t(t-2)/(t^2-12),  w(t) = -3(t^2-12t+12)/(t^2-12),
with t in (2*sqrt(3), 6) giving k > 3. For rational t everything (k, w, lam,
D = T_{k+delta}(lam)) is rational and the exact engine `jacobi_coeff_rec`
can be consulted directly. delta is probed far OUTSIDE [-3/2, 3/2] as well,
where the knife must go negative -- the count of negative reference signs is
reported, and VACUOUS is printed if it is zero.

Run: python lab/odd_depth_kwindow.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F  # ENGINE-OK: interface glue for the reference engine
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric  # noqa: E402
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402
from keystone_unglued import build_branch  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

# 4-variable dict polynomial: slot 0 = K, 1 = k, 2 = delta, 3 = w.
NV = 4


class P4:
    __slots__ = ("d",)

    def __init__(self, d=None):
        self.d = {} if d is None else d

    @staticmethod
    def const(v) -> P4:
        v = fmpq(v)
        return P4({} if v == 0 else {(0,) * NV: v})

    @staticmethod
    def var(slot: int) -> P4:
        e = [0] * NV
        e[slot] = 1
        return P4({tuple(e): fmpq(1)})

    def __add__(self, other) -> P4:
        if not isinstance(other, P4):
            other = P4.const(other)
        out = dict(self.d)
        for kk, v in other.d.items():
            nv = out.get(kk, fmpq(0)) + v
            if nv == 0:
                out.pop(kk, None)
            else:
                out[kk] = nv
        return P4(out)

    def __sub__(self, other) -> P4:
        if not isinstance(other, P4):
            other = P4.const(other)
        return self + other * fmpq(-1)

    def __mul__(self, other) -> P4:
        if not isinstance(other, P4):
            f = fmpq(other)
            if f == 0:
                return P4()
            return P4({kk: v * f for kk, v in self.d.items()})
        out: dict = {}
        for k1, v1 in self.d.items():
            for k2, v2 in other.d.items():
                key = tuple(x + y for x, y in zip(k1, k2))
                nv = out.get(key, fmpq(0)) + v1 * v2
                if nv == 0:
                    out.pop(key, None)
                else:
                    out[key] = nv
        return P4(out)

    __rmul__ = __mul__
    __radd__ = __add__

    def __pow__(self, n: int) -> P4:
        r = P4.const(1)
        b = self
        while n:
            if n & 1:
                r = r * b
            b = b * b
            n >>= 1
        return r

    def eval_at(self, pt) -> fmpq:
        tot = fmpq(0)
        for kk, coeff in self.d.items():
            term = coeff
            for slot, e in enumerate(kk):
                if e:
                    term *= pt[slot] ** e
            tot += term
        return tot


def reduce_w(p: P4) -> P4:
    """Reduce modulo w^2 = 3(4k^2 - 12k + 3): every w-exponent ends 0 or 1."""
    # w^2 -> conic RHS, as a P4 in k alone
    k = P4.var(1)
    rhs = (k * k * fmpq(12)) + (k * fmpq(-36)) + P4.const(9)
    out = p
    while True:
        high = {e: c for e, c in out.d.items() if e[3] >= 2}
        if not high:
            return out
        keep = P4({e: c for e, c in out.d.items() if e[3] < 2})
        add = P4()
        for e, c in high.items():
            base = P4({(e[0], e[1], e[2], e[3] - 2): c})
            add = add + base * rhs
        out = keep + add


def build_kwindow(parity: str, d: int, e_polys: dict) -> P4:
    """G(K, k, delta, w) = A + B*w with sign(G) = sign of the depth-d knife at
    level N, lam = lam*(k), D = T_{k+delta}(lam*). Pure substitution from the
    validated build_branch; cleared factors N^*, lam^*, (6a)^* are positive on
    the domain (k > 2, lam > 0), so the sign is untouched."""
    H = build_branch(parity, d, e_polys)
    Ic = H.max_deg(1)  # c-degree
    Jv = H.max_deg(2)  # v-degree

    K = P4.var(0)
    k = P4.var(1)
    delta = P4.var(2)
    w = P4.var(3)
    one = P4.const(1)

    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + one
    k_s = k + delta
    a_pol = k * k - k * fmpq(3) + P4.const(3)
    b_pol = k * k - k * fmpq(6) + P4.const(6)
    Lnum = b_pol * fmpq(3) + k * (k - P4.const(2)) * w  # lam = Lnum / (6a)
    Lden = a_pol * fmpq(6)

    # G0 = N^Ic * lam^Jv * H, term by term:  h K^a c^i v^j ->
    #      h K^a N^(Ic-i) lam^(Jv+i-j) k_s^j
    # then lam^e -> Lnum^e * Lden^(Elam - e), with Elam = max over terms of e.
    Elam = 0
    for (aa, i, j) in H.d:
        Elam = max(Elam, Jv + i - j)

    # memoized powers
    Npow = [one]
    for _ in range(Ic):
        Npow.append(Npow[-1] * N)
    kspow = [one]
    for _ in range(Jv):
        kspow.append(kspow[-1] * k_s)
    Lnpow = [one]
    for _ in range(Elam):
        Lnpow.append(reduce_w(Lnpow[-1] * Lnum))
    Ldpow = [one]
    for _ in range(Elam):
        Ldpow.append(Ldpow[-1] * Lden)
    Kv = P4.var(0)
    Kpow_cache: dict[int, P4] = {0: one, 1: Kv}

    def Kpow(n: int) -> P4:
        if n not in Kpow_cache:
            Kpow_cache[n] = Kpow_cache[n - 1] * Kv if n - 1 in Kpow_cache else Kv**n
        return Kpow_cache[n]

    # Accumulate into one dict in place: `total = total + term` copies the
    # growing total dict on every one of the |H| additions (P4.__add__ starts
    # from dict(self.d)), which is quadratic -- measured 996 s at depth 5 odd
    # while every prepared power table takes under a second. Same algebra,
    # incremental merge.
    acc: dict = {}
    for (aa, i, j), h in H.d.items():
        e = Jv + i - j
        term = (
            Kpow(aa)
            * Npow[Ic - i]
            * kspow[j]
            * Lnpow[e]
            * Ldpow[Elam - e]
            * h
        )
        for key, v in term.d.items():
            nv = acc.get(key, fmpq(0)) + v
            if nv == 0:
                acc.pop(key, None)
            else:
                acc[key] = nv
    return reduce_w(P4(acc))


def line_point(t: fmpq) -> tuple[fmpq, fmpq]:
    """Rational point on the conic from the line through (3,3) with slope t."""
    den = t * t - 12
    k = (t * (t - 2) * 3) / den
    w = (t * t - t * 12 + 12) * fmpq(-3) / den
    return k, w


def lam_of(k: fmpq, w: fmpq) -> fmpq:
    a = k * k - k * 3 + 3
    b = k * k - k * 6 + 6
    return (b * 3 + k * (k - 2) * w) / (a * 6)


def T_of(k_s: fmpq, lam: fmpq) -> fmpq:
    return fmpq(3) * (k_s * 2 - 3) / (k_s * (k_s - 2)) * (lam * lam + (k_s * 2 - 2) * lam + 1) + k_s * 2


def ref_sign(j: int, n: int, m: int, lam: fmpq, k_s: fmpq) -> int:
    D = T_of(k_s, lam)  # T is D directly (gamma_shore = (T-3)/2, D = 2*gamma+3 = T)
    knife = (-1) ** m * jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
    return (knife > 0) - (knife < 0)


# rational t values on (2*sqrt(3), 6): the smaller t, the larger k
T_PROBE = [fmpq(87, 25), fmpq(7, 2), fmpq(18, 5), fmpq(4), fmpq(9, 2)]
DELTA_PROBE = [fmpq(0), fmpq(1), fmpq(-1), fmpq(3, 2), fmpq(-3, 2), fmpq(8), fmpq(-8), fmpq(30)]


def self_check(d: int, G_even: P4, G_odd: P4) -> dict:
    j = d + 1
    report = {"trials": 0, "mismatches": [], "negative_refs": 0, "in_window_negatives": []}
    for parity, G in (("even", G_even), ("odd", G_odd)):
        for K_val in (4, 7, 15, 40):
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            m = n - j
            if m < 0:
                continue
            for t in T_PROBE:
                k, w = line_point(t)
                # sanity: (k, w) really on the conic, and lam on the critical curve
                assert w * w == (k * k * 4 - k * 12 + 3) * 3
                lam = lam_of(k, w)
                assert lam > 0
                a = k * k - k * 3 + 3
                b = k * k - k * 6 + 6
                c0 = k**4 - k**3 * 4 + k * k + k * 9 - 9
                assert a * lam * lam * (-3) + b * lam * 3 + c0 == 0
                for delta in DELTA_PROBE:
                    k_s = k + delta
                    if k_s <= 3:
                        continue
                    got = G.eval_at((fmpq(K_val), k, delta, w))
                    sg = (got > 0) - (got < 0)
                    se = ref_sign(j, n, m, lam, k_s)
                    report["trials"] += 1
                    report["negative_refs"] += se < 0
                    if sg != se:
                        report["mismatches"].append(
                            f"{parity} K={K_val} t={t} delta={delta}: G={sg} ref={se}"
                        )
                    if se < 0 and abs(delta) <= fmpq(3, 2):
                        report["in_window_negatives"].append(
                            f"{parity} K={K_val} t={t} (k={float(k):.3f}, lam={float(lam):.3f}) delta={delta}"
                        )
    return report


def run_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    G = {}
    for parity in ("even", "odd"):
        t1 = time.time()
        G[parity] = build_kwindow(parity, d, e_polys)
        print(
            f"depth {d} [{parity}]: G built, {len(G[parity].d)} terms, "
            f"degs K={max(e[0] for e in G[parity].d)} k={max(e[1] for e in G[parity].d)} "
            f"delta={max(e[2] for e in G[parity].d)} w={max(e[3] for e in G[parity].d)} "
            f"({time.time() - t1:.0f}s)",
            flush=True,
        )
    rep = self_check(d, G["even"], G["odd"])
    vac = " VACUOUS" if rep["negative_refs"] == 0 else ""
    print(
        f"depth {d}: self-check {rep['trials']} trials, {len(rep['mismatches'])} mismatches, "
        f"{rep['negative_refs']} negative reference signs{vac}, "
        f"{len(rep['in_window_negatives'])} in-window negatives",
        flush=True,
    )
    for msg in rep["mismatches"][:5]:
        print("  MISMATCH", msg, flush=True)
    for msg in rep["in_window_negatives"][:5]:
        print("  IN-WINDOW NEGATIVE", msg, flush=True)
    return {
        "depth": d,
        "terms": {p: len(G[p].d) for p in G},
        "self_check_trials": rep["trials"],
        "mismatches": rep["mismatches"][:10],
        "self_check_passed": not rep["mismatches"],
        "negative_reference_signs": rep["negative_refs"],
        "vacuous": rep["negative_refs"] == 0,
        "in_window_negatives": rep["in_window_negatives"][:10],
        "delta_window": ["-3/2", "3/2"],
        "seconds": round(time.time() - t0, 1),
    }


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [3]
    out = []
    for d in depths:
        out.append(run_depth(d))
        path = RES / "odd_depth_kwindow_selfcheck.json"
        path.write_text(json.dumps({"runs": out, **stamp()}, indent=1), encoding="utf-8")
        print(f"  written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
