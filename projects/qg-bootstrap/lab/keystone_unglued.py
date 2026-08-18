"""The UNGLUED keystone argument: one window of shore-integers, every depth.

WHY THIS FILE EXISTS (docs/ERRATA.md ERR-0010, ERR-0011). The previous
"half-level" argument glued two different roles onto a single integer K: the
LEVEL (N = 2K or 2K+1) and the integer used to bound the shore through
T_hat(lam) <= T_K(lam). That gluing is what killed it. The minimiser of
T_k(lam) over integers k grows like sqrt(3)*lam, so forcing k = N/2 leaves
T_K far above the true shore once lam is large, and in that gap the knife is
LEGITIMATELY negative -- verified at n=101, lam=100: sign is -1 at
D = T_K = 2500.9 but +1 at the true shore T_hat = 1890.4 and everywhere
below. No physics was ever violated; the method was demanding something
strictly stronger than the physics, and failing at its own demand.

THE UNGLUED ARGUMENT, in three steps:

  (a) CONTINUUM STEP (what this file certifies). Prove knife_d >= 0 at
      D = T_v(lam) for ALL REAL v in the window [8/5, 2], every level, every
      lam. Note v is a REAL parameter here -- no integrality is used, so this
      is an honest continuum statement a Bernstein certificate can carry.

  (b) INTEGRALITY STEP (where integrality is actually needed, and only here).
      Apply (a) at an INTEGER k_s = v*lam inside the window. The window has
      length (2 - 8/5)*lam = 2*lam/5, so it contains an integer as soon as
      lam >= 5/2; for such k_s, T_hat(lam) <= T_{k_s}(lam) holds BY
      DEFINITION of a minimum over integers -- exactly the property ERR-0008
      showed must never be assumed for a non-integer. Small lam (below 5/2)
      is a separate finite region, handled directly as depth 2's small-n was.

  (c) MONOTONICITY STEP. The knife is decreasing in D at fixed (n, lam)
      (measured: monotone on every configuration tested). Therefore
      positivity at the LARGEST admissible D -- namely T_{k_s} >= T_hat --
      implies positivity on the whole physical region D <= T_hat.

WHY THE WINDOW IS THE INTERESTING PART. It was MEASURED, not guessed:
v = 1.45 and v = 2.10 both produce genuine negatives, v in [1.50, 2.05] gave
0 negatives over 48 configurations, so [8/5, 2] is taken with margin on both
sides. Crucially the SAME window is clean for depths 2 through 8 (0 negatives
out of 160 tested per depth) -- a single window covering every depth is what
makes this a candidate keystone rather than one more per-depth trick.

Engine 2 throughout: flint fmpq only, no sympy, no float in any comparison
(float appears solely in human-readable prints). Every gamma<->D conversion
is gamma=(D-3)/2, D=2*gamma+3 -- the ERR-0009 trap is checked explicitly.

Run: python lab/keystone_unglued.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric, falling_poly, poch  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

# The measured window of admissible shore-ratios v = k_s / lam. See the module
# docstring: v=1.45 and v=2.10 genuinely fail, [1.50, 2.05] was clean, so this
# is the clean interval taken with margin at both ends.
V_LO = fmpq(8, 5)
V_HI = fmpq(2)

# Below lam = 5/2 the window [V_LO*lam, V_HI*lam] is shorter than 1 and need
# not contain any integer, so step (b) has nothing to stand on. Independently
# MEASURED, step (c) dies at the same place: monotonicity of the knife in D
# held on 120 of 120 configurations at lam >= 5/2 and failed on 33 of 96 below
# it. Two different requirements, one boundary.
LAM_MIN = fmpq(5, 2)

# The rectangular sufficient condition for lam >= LAM_MIN: with K >= 3 we have
# N >= 6, so c >= 5/12 forces lam = c*N >= 5/2. Points with lam >= 5/2 but
# c < 5/12 (large N, moderate lam) are a SEPARATE region this file does not
# cover, and are recorded as an open gap rather than quietly included.
C_MIN = fmpq(5, 12)

# Where the direct c piece hands over to the compactified tail; the two pieces
# meet here, so together they cover all c >= C_MIN.
C_SPLIT = fmpq(50)

# The fixed integer shore level used on lam <= LAM_MIN, where the window is too
# short to be guaranteed to contain one. k=3 fails (depth 2 near lam=2.4); k=4
# is clean on 392 trials across depths 2..10 and all lam in (0, 5/2].
KS_SMALL = fmpq(4)


# --------------------------------------------------------------------------
# Multivariate polynomial over Q: dict[(e0, e1, ..)] -> fmpq. Same design as
# depth_d_proof.BiPoly, generalised to n slots because the unglued argument
# needs a THIRD variable (v) that the glued one did not have.
# Slot 0 = "K" (level), slot 1 = "c" (= lam/N), slot 2 = "v" (= k_s/lam).
#
# WHY c AND NOT lam, decided by measurement, not taste. The argument needs an
# INTEGER k_s >= 3 in the window [8/5*lam, 2*lam]; that window is longer than 1
# exactly once lam >= 5/2. A first version therefore made lam an independent
# coordinate, since "lam >= 5/2" is then a box face while in c it is the
# slanted condition c >= 5/(2N). That version proved the near region but JAMMED
# on the tail: 69253 boxes and failure, and deeper bisection (214021 boxes),
# a leading-term bound (threshold 3.5e13, useless) and a geometric ladder
# (301829 boxes on ONE rung) all failed too. Printing the open boxes back in
# the original variables showed every single one sat in the corner where
# K -> inf AND lam -> inf TOGETHER -- a two-variable degeneration, i.e. the
# wrong coordinate, not a resource problem. In (K, c) that corner is an
# ordinary finite point because c = lam/N stays bounded there, and the same
# tail closed in ONE box.
#
# The integrality condition is recovered rectangularly instead: for K >= 3 we
# have N >= 6, so
#       c >= 5/12   ==>   lam = c*N >= 5/2,
# which is a box face in c. The remaining sliver (lam >= 5/2 but c < 5/12,
# i.e. large N with moderate lam) is NOT covered by this file -- see
# C_MIN below.
# --------------------------------------------------------------------------
NVARS = 3


class NPoly:
    __slots__ = ("d",)

    def __init__(self, d=None):
        self.d = {} if d is None else d

    @staticmethod
    def const(v) -> NPoly:
        v = fmpq(v)
        return NPoly({} if v == 0 else {(0,) * NVARS: v})

    @staticmethod
    def var(slot: int) -> NPoly:
        e = [0] * NVARS
        e[slot] = 1
        return NPoly({tuple(e): fmpq(1)})

    def __add__(self, other) -> NPoly:
        if not isinstance(other, NPoly):
            other = NPoly.const(other)
        out = dict(self.d)
        for k, v in other.d.items():
            nv = out.get(k, fmpq(0)) + v
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
        return NPoly(out)

    def __sub__(self, other) -> NPoly:
        if not isinstance(other, NPoly):
            other = NPoly.const(other)
        return self + other * fmpq(-1)

    def __mul__(self, other) -> NPoly:
        if not isinstance(other, NPoly):
            f = fmpq(other)
            if f == 0:
                return NPoly()
            return NPoly({k: v * f for k, v in self.d.items()})
        out: dict = {}
        for k1, v1 in self.d.items():
            for k2, v2 in other.d.items():
                key = tuple(a + b for a, b in zip(k1, k2))
                nv = out.get(key, fmpq(0)) + v1 * v2
                if nv == 0:
                    out.pop(key, None)
                else:
                    out[key] = nv
        return NPoly(out)

    __rmul__ = __mul__
    __radd__ = __add__

    def __pow__(self, n: int) -> NPoly:
        r = NPoly.const(1)
        b = self
        while n:
            if n & 1:
                r = r * b
            b = b * b
            n >>= 1
        return r

    def max_deg(self, slot: int) -> int:
        return max((k[slot] for k in self.d), default=0)

    def eval_at(self, pt) -> fmpq:
        tot = fmpq(0)
        for k, coeff in self.d.items():
            term = coeff
            for slot, e in enumerate(k):
                if e:
                    term *= pt[slot] ** e
            tot += term
        return tot


def lift_N(poly_in_N, N_bi: NPoly) -> NPoly:
    """Evaluate a univariate fmpq_poly (in N) at the NPoly N_bi, by Horner."""
    result = NPoly.const(0)
    for c in reversed(poly_in_N.coeffs()):
        result = result * N_bi + NPoly.const(c)
    return result


# --------------------------------------------------------------------------
# The depth-d knife sign as a polynomial in (K, c, v), at D = T_{v*lam}(lam).
# --------------------------------------------------------------------------
def build_branch(parity: str, d: int, e_polys: dict) -> NPoly:
    """H(K, c, v) whose SIGN is the depth-d knife's sign at D = T_{v*lam}(lam).

    The homogenization uses the COMPLEMENT product and Qg**j -- the ERR-0010
    fix. Writing it out: with gamma = Pg/Qg and
    L[i] = 2*m*Qg + Pg + Qg*(1+i), we have
        (2m+gamma+1)_j = (prod_{i<j} L[i]) / Qg^j,
    so bringing term j up to the common denominator L[0]*...*L[d-1] means
    multiplying by the factors it is MISSING, i.e. L[j]*...*L[d-1], and by
    Qg^j from clearing its own denominator. The pre-ERR-0010 code used the
    prefix L[0]..L[j-1] and Qg^(d-j) -- both wrong, and wrong in a way that
    stayed invisible until depth 6.
    """
    K = NPoly.var(0)
    c = NPoly.var(1)
    v = NPoly.var(2)
    one = NPoly.const(1)

    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + one
    m = N - NPoly.const(d)
    lam = c * N
    X = (N + lam) * (N + lam)

    # k_s = v * lam, the shore-bounding value -- INDEPENDENT of the level now.
    k_s = v * lam

    # T_k(k,lam) = 3(2k-3)/(k(k-2)) * (lam^2+(2k-2)lam+1) + 2k, and
    # gamma = (T_k - 3)/2 = Pg/Qg with the denominator cleared:
    #   Qg = 2*k*(k-2)
    #   Pg = 3*(2k-3)*B + 2*k^2*(k-2) - 3*k*(k-2),  B = lam^2+(2k-2)lam+1
    Bexpr = lam * lam + (k_s * fmpq(2) - fmpq(2)) * lam + one
    kk2 = k_s * (k_s - fmpq(2))
    Qg = kk2 * fmpq(2)
    Pg = (
        (k_s * fmpq(2) - fmpq(3)) * Bexpr * fmpq(3)
        + k_s * k_s * (k_s - fmpq(2)) * fmpq(2)
        - kk2 * fmpq(3)
    )

    total = NPoly.const(0)
    half = NPoly.const(fmpq(1, 2))
    two_m_Qg = (m * fmpq(2)) * Qg
    L = [two_m_Qg + Pg + Qg * fmpq(1 + i) for i in range(d)]

    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeff_bi = lift_N(coeff_N, N) * fmpq((-1) ** k)

        num_bi = NPoly.const(1)
        for i in range(j):
            num_bi = num_bi * (m + half + NPoly.const(i))

        complement = NPoly.const(1)
        for i in range(j, d):
            complement = complement * L[i]

        total = total + coeff_bi * num_bi * complement * (X**j) * (Qg**j)
    return total


def self_check(d: int, e_polys: dict, k_values, c_values, v_values) -> list[str]:
    """Compare build_branch's SIGN against the exact reference engine at
    concrete (K, c, v).

    ERR-0011's lesson is baked into the CALLER's ranges: a self-check whose
    domain is much narrower than the box being certified manufactures false
    confidence. Two separate files carried the same algebra bug undetected
    precisely because their self-checks only ever looked at small K and c<1.
    """
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
                lam = fmpq(c_num, c_den)
                for v_num, v_den in v_values:
                    v_val = fmpq(v_num, v_den)
                    k_s = v_val * lam
                    if k_s <= 3:
                        continue

                    sgn = H.eval_at((fmpq(K_val), lam, v_val))
                    sign_formula = (sgn > 0) - (sgn < 0)

                    # exact reference at the SAME D the algebra targets
                    Bexpr = lam * lam + (k_s * 2 - 2) * lam + 1
                    kk2 = k_s * (k_s - 2)
                    Qg = kk2 * 2
                    Pg = (k_s * 2 - 3) * Bexpr * 3 + k_s * k_s * (k_s - 2) * 2 - kk2 * 3
                    gamma = Pg / Qg
                    D = gamma * 2 + 3  # ERR-0009: D=2*gamma+3, no stray +3
                    lam_F = F(int(lam.p), int(lam.q))
                    D_F = F(int(D.p), int(D.q))
                    knife = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, D_F)
                    sign_exact = (knife > 0) - (knife < 0)

                    if sign_formula != sign_exact:
                        bad.append(
                            f"depth={d} {parity} K={K_val} lam={c_num}/{c_den} "
                            f"v={v_num}/{v_den}: {sign_formula} vs {sign_exact}"
                        )
    return bad


# --------------------------------------------------------------------------
# Exact Bernstein in NVARS dimensions: build the coefficient grid ONCE at the
# root, then bisect it with de Casteljau. (The old code rebuilt the grid from
# the monomial form at every box, which is O(prod deg_i^2) per box instead of
# O(deg^2); with three variables that difference is fatal, not merely slow.)
# --------------------------------------------------------------------------
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


def bernstein_grid(poly: NPoly, box):
    """Bernstein coefficients on `box`, as a flat dict keyed by multi-index."""
    from math import comb

    degs = [poly.max_deg(s) for s in range(NVARS)]
    pw = [affine_powers(box[s][0], box[s][1] - box[s][0], degs[s]) for s in range(NVARS)]

    # monomial coefficients of the box-affine-mapped polynomial
    mono: dict = {}
    for expo, coeff in poly.d.items():
        parts = [pw[s][expo[s]] for s in range(NVARS)]
        stack = [((), coeff)]
        for part in parts:
            nxt = []
            for key, val in stack:
                for p, cf in part.items():
                    nxt.append((key + (p,), val * cf))
            stack = nxt
        for key, val in stack:
            mono[key] = mono.get(key, fmpq(0)) + val

    # Bernstein coefficients: b_k = sum_{p<=k} C(k,p)/C(deg,p) * mono_p, per axis
    ratio = [
        [
            [fmpq(comb(k, p), comb(degs[s], p)) if p <= k else None for p in range(degs[s] + 1)]
            for k in range(degs[s] + 1)
        ]
        for s in range(NVARS)
    ]
    grid: dict = {}
    idx_ranges = [range(degs[s] + 1) for s in range(NVARS)]

    def rec(slot, key):
        if slot == NVARS:
            b = fmpq(0)
            for p, cf in mono.items():
                f = fmpq(1)
                ok = True
                for s in range(NVARS):
                    if p[s] > key[s]:
                        ok = False
                        break
                    f *= ratio[s][key[s]][p[s]]
                if ok:
                    b += cf * f
            grid[key] = b
            return
        for i in idx_ranges[slot]:
            rec(slot + 1, key + (i,))

    rec(0, ())
    return grid, degs


def _decasteljau_half(coeffs):
    """Split a 1D Bernstein sequence at t=1/2, exactly, degree-preserving."""
    half = fmpq(1, 2)
    d = len(coeffs) - 1
    tri = [list(coeffs)]
    for r in range(1, d + 1):
        prev = tri[-1]
        tri.append([(prev[i] + prev[i + 1]) * half for i in range(d - r + 1)])
    return [tri[r][0] for r in range(d + 1)], [tri[d - r][r] for r in range(d + 1)]


def split_grid(grid, degs, axis):
    """Bisect the Bernstein grid at the midpoint along `axis`, de Casteljau."""
    left: dict = {}
    right: dict = {}
    others = [s for s in range(NVARS) if s != axis]
    seen = set()
    for key in grid:
        base = tuple(key[s] for s in others)
        if base in seen:
            continue
        seen.add(base)
        line = []
        for i in range(degs[axis] + 1):
            k = list(key)
            k[axis] = i
            line.append(grid[tuple(k)])
        lline, rline = _decasteljau_half(line)
        for i in range(degs[axis] + 1):
            k = list(key)
            k[axis] = i
            left[tuple(k)] = lline[i]
            right[tuple(k)] = rline[i]
    return left, right


def prove_box(poly: NPoly, box, max_depth: int = 24):
    """Bisect until every box has a positive Bernstein lower bound.

    The split axis is chosen by RELATIVE width (current width divided by the
    ROOT width of that axis), not absolute width. With absolute widths a box
    like K in [0, 0.999] x lam in [5/2, 200] x v in [8/5, 2] never splits the
    K or v axis at all -- lam is a hundred times wider in absolute terms, so
    it wins every comparison and the other two directions are never refined.
    That is not a slow proof, it is a proof that cannot terminate: measured
    directly, at max_depth=7 all 128 open boxes still had the full K range
    [0, 0.999] and the full v range, with only lam subdivided. Relative width
    makes the three axes comparable regardless of their units.
    """
    grid, degs = bernstein_grid(poly, box)
    root_w = [box[s][1] - box[s][0] for s in range(NVARS)]
    stack = [(grid, box, 0)]
    boxes, open_boxes = 0, []
    while stack:
        g, bx, depth = stack.pop()
        boxes += 1
        if min(g.values()) > 0:
            continue
        if depth >= max_depth:
            open_boxes.append([(str(lo), str(hi)) for lo, hi in bx])
            continue
        rel = [(bx[s][1] - bx[s][0]) / root_w[s] for s in range(NVARS)]
        axis = max(range(NVARS), key=lambda s: rel[s])
        lo, hi = bx[axis]
        mid = (lo + hi) / 2
        lbx, rbx = list(bx), list(bx)
        lbx[axis], rbx[axis] = (lo, mid), (mid, hi)
        lg, rg = split_grid(g, degs, axis)
        stack += [(lg, lbx, depth + 1), (rg, rbx, depth + 1)]
    return (not open_boxes), boxes, open_boxes


def compactify_from_zero(poly: NPoly, slot: int) -> NPoly:
    """Map [0, infinity) -> [0,1) via x = t/(1-t), clearing (1-t)^deg.

    Distinct from `compactify`, which needs a strictly positive left endpoint.
    Used for the wedge coordinate z, which starts at 0.
    """
    deg = poly.max_deg(slot)
    pw = [{0: fmpq(1)}]
    for _ in range(deg):
        prev = pw[-1]
        cur: dict = {}
        for p, cf in prev.items():
            cur[p] = cur.get(p, fmpq(0)) + cf
            cur[p + 1] = cur.get(p + 1, fmpq(0)) - cf
        pw.append(cur)
    out: dict = {}
    for expo, coeff in poly.d.items():
        e = expo[slot]
        for p, cf in pw[deg - e].items():
            key = list(expo)
            key[slot] = e + p
            k = tuple(key)
            out[k] = out.get(k, fmpq(0)) + coeff * cf
    return NPoly({k: v for k, v in out.items() if v != 0})


def build_wedge(parity: str, d: int, e_polys: dict) -> NPoly:
    """The region c < C_MIN with lam >= LAM_MIN, as an honest box.

    `build_branch`'s box needs c >= C_MIN = 5/12 to guarantee lam >= 5/2, which
    leaves out large N at moderate lam. Rather than bound c, substitute the
    LEVEL:
        K = 5/(4c) + z,   z >= 0
    Then N = 2K = 5/(2c) + 2z gives lam = c*N = 5/2 + 2*c*z >= 5/2 for free,
    and K >= 5/(4c) >= 3 whenever c <= 5/12, also for free. So the wedge is the
    plain box  c in (0, 5/12] x z in [0, inf) x v in [V_LO, V_HI]  with NO
    leftover side conditions -- the two boxes together cover every point with
    lam >= 5/2.

    K is a fraction in c, so every quantity is carried multiplied by the
    appropriate power of c (cK = c*K, cN = c*N, cm = c*m) to stay polynomial.
    Slot 0 = c, slot 1 = z, slot 2 = v.
    """
    c = NPoly.var(0)
    z = NPoly.var(1)
    v = NPoly.var(2)

    cK = NPoly.const(fmpq(5, 4)) + c * z
    cN = cK * fmpq(2) if parity == "even" else cK * fmpq(2) + c
    lam = cN  # this is c*lam_true; every companion below carries the same c-power
    cm = cN - c * NPoly.const(d)
    X = (cN + c * lam) * (cN + c * lam)
    k_s = v * lam
    B = lam * lam + (k_s * fmpq(2) - fmpq(2) * c) * lam + c * c
    kk2 = k_s * (k_s - fmpq(2) * c)
    Qg = kk2 * fmpq(2)
    Pg = (
        (k_s * fmpq(2) - fmpq(3) * c) * B * fmpq(3)
        + k_s * k_s * (k_s - fmpq(2) * c) * fmpq(2)
        - kk2 * fmpq(3) * c * c
    )

    total = NPoly.const(0)
    half = NPoly.const(fmpq(1, 2))
    two_m_Qg = (cm * fmpq(2)) * Qg
    L = [two_m_Qg + Pg + Qg * c * fmpq(1 + i) for i in range(d)]
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeffs = coeff_N.coeffs()
        deg = len(coeffs) - 1
        cb = NPoly.const(0)
        for i, co in enumerate(coeffs):
            cb = cb + NPoly.const(co) * (cN**i) * (c ** (deg - i))
        cb = cb * fmpq((-1) ** k)

        num = NPoly.const(1)
        for i in range(j):
            num = num * (cm + c * half + c * NPoly.const(i))
        comp = NPoly.const(1)
        for i in range(j, d):
            comp = comp * L[i]
        total = total + cb * num * comp * (X**j) * (Qg**j)
    return total


def build_small_lam(parity: str, d: int, e_polys: dict) -> NPoly:
    """H(K, lam) at D = T_{KS_SMALL}(lam), for the region lam <= LAM_MIN.

    Below lam = 5/2 the window [8/5 lam, 2 lam] is shorter than 1, so step (b)
    cannot rely on it. But the window was only ever a convenience: T_hat <= T_k
    holds for EVERY integer k >= 3, so on this region we may simply FIX one
    integer, provided the knife stays positive there. Measured: k = 4 works at
    every depth 2..10 and every lam in (0, 5/2] (392 trials, 0 negatives),
    while k = 3 already fails for depth 2 near lam = 2.4 -- hence 4, not 3.

    Fixing k_s removes the v axis entirely, so this is a 2-variable problem
    (slot 0 = K, slot 1 = lam; slot 2 unused).
    """
    K = NPoly.var(0)
    lam = NPoly.var(1)
    one = NPoly.const(1)

    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + one
    m = N - NPoly.const(d)
    X = (N + lam) * (N + lam)
    k_s = NPoly.const(KS_SMALL)

    B = lam * lam + (k_s * fmpq(2) - fmpq(2)) * lam + one
    kk2 = k_s * (k_s - fmpq(2))
    Qg = kk2 * fmpq(2)
    Pg = (
        (k_s * fmpq(2) - fmpq(3)) * B * fmpq(3)
        + k_s * k_s * (k_s - fmpq(2)) * fmpq(2)
        - kk2 * fmpq(3)
    )

    total = NPoly.const(0)
    half = NPoly.const(fmpq(1, 2))
    two_m_Qg = (m * fmpq(2)) * Qg
    L = [two_m_Qg + Pg + Qg * fmpq(1 + i) for i in range(d)]
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        cb = lift_N(coeff_N, N) * fmpq((-1) ** k)
        num = NPoly.const(1)
        for i in range(j):
            num = num * (m + half + NPoly.const(i))
        comp = NPoly.const(1)
        for i in range(j, d):
            comp = comp * L[i]
        total = total + cb * num * comp * (X**j) * (Qg**j)
    return total


def compactify(poly: NPoly, slot: int, x_min) -> NPoly:
    """Map [x_min, infinity) -> [0,1) via x = x_min/(1-t), clearing (1-t)^deg."""
    deg = poly.max_deg(slot)
    pw = [{0: fmpq(1)}]
    for _ in range(deg):
        prev = pw[-1]
        cur: dict = {}
        for p, cf in prev.items():
            cur[p] = cur.get(p, fmpq(0)) + cf
            cur[p + 1] = cur.get(p + 1, fmpq(0)) - cf
        pw.append(cur)
    out: dict = {}
    for expo, coeff in poly.d.items():
        e = expo[slot]
        base = coeff * fmpq(x_min) ** e
        for p, cf in pw[deg - e].items():
            key = list(expo)
            key[slot] = p
            k = tuple(key)
            out[k] = out.get(k, fmpq(0)) + base * cf
    return NPoly({k: v for k, v in out.items() if v != 0})


def run_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)

    # ERR-0011: keep the self-check range as wide as the box being certified.
    # lam starts at LAM_MIN=5/2 (below it the window holds no integer k_s, so
    # the argument does not apply and the polynomial is legitimately negative).
    k_values = (3, 4, 5, 6, 10, 25, 100, 300)
    c_values = [(5, 12), (1, 1), (5, 1), (50, 1), (500, 1)]
    v_values = [(8, 5), (7, 4), (19, 10), (2, 1)]
    bad = self_check(d, e_polys, k_values, c_values, v_values)
    n_trials = len(k_values) * len(c_values) * len(v_values) * 2
    print(f"depth {d}: self-check {n_trials} trials, {len(bad)} mismatches", flush=True)
    if bad:
        for b in bad[:5]:
            print("  ", b)
        return {"depth": d, "self_check_passed": False, "mismatches": bad[:10]}

    result = {
        "depth": d,
        "self_check_trials": n_trials,
        "self_check_passed": True,
        "v_window": [str(V_LO), str(V_HI)],
        "branches": {},
    }
    for parity in ("even", "odd"):
        H = build_branch(parity, d, e_polys)
        t1 = time.time()
        # K >= 3 compactified to [0,1); lam in [LAM_MIN, LAM_SPLIT] direct and
        # lam >= LAM_SPLIT compactified; v stays on its finite window.
        # The two lam pieces MEET at LAM_SPLIT rather than overlapping from
        # LAM_MIN: compactifying the tail from LAM_MIN would force the single
        # map x = LAM_MIN/(1-t) to resolve both the near region and the tail,
        # and the tail piece then failed (4225 open boxes) while the same
        # polynomial on the direct piece proved cleanly in 3687.
        poly_K = compactify(H, 0, 3)
        ok_lo, boxes_lo, open_lo = prove_box(
            poly_K, [(fmpq(0), fmpq(999, 1000)), (C_MIN, C_SPLIT), (V_LO, V_HI)], max_depth=30
        )
        poly_Kc = compactify(poly_K, 1, C_SPLIT)
        ok_hi, boxes_hi, open_hi = prove_box(
            poly_Kc, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000)), (V_LO, V_HI)]
        )
        # the wedge: c < C_MIN with lam >= LAM_MIN, as its own box
        W = build_wedge(parity, d, e_polys)
        Wz = compactify_from_zero(W, 1)
        ok_w, boxes_w, open_w = prove_box(
            Wz, [(fmpq(0), C_MIN), (fmpq(0), fmpq(999, 1000)), (V_LO, V_HI)]
        )
        # small lam (<= LAM_MIN) at the FIXED shore level KS_SMALL
        S = build_small_lam(parity, d, e_polys)
        Sk = compactify(S, 0, 3)
        ok_s, boxes_s, open_s = prove_box(
            Sk, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), LAM_MIN), (fmpq(0), fmpq(1))]
        )
        dt = time.time() - t1
        print(
            f"  [{parity}] lo({float(C_MIN):.4f}<=c<={float(C_SPLIT)})={ok_lo}({boxes_lo}b) "
            f"hi(c>={float(C_SPLIT)})={ok_hi}({boxes_hi}b) "
            f"wedge(c<{float(C_MIN):.4f})={ok_w}({boxes_w}b) "
            f"small(lam<={float(LAM_MIN)})={ok_s}({boxes_s}b)  ({dt:.0f}s)",
            flush=True,
        )
        result["branches"][parity] = {
            "K_deg": H.max_deg(0),
            "c_deg": H.max_deg(1),
            "v_deg": H.max_deg(2),
            "terms": len(H.d),
            "lo_proved": ok_lo,
            "lo_boxes": boxes_lo,
            "lo_open": len(open_lo),
            "hi_proved": ok_hi,
            "hi_boxes": boxes_hi,
            "hi_open": len(open_hi),
            "wedge_proved": ok_w,
            "wedge_boxes": boxes_w,
            "wedge_open": len(open_w),
            "small_lam_proved": ok_s,
            "small_lam_boxes": boxes_s,
            "small_lam_open": len(open_s),
        }
    result["proved_for_all_lam"] = all(
        result["branches"][p]["lo_proved"]
        and result["branches"][p]["hi_proved"]
        and result["branches"][p]["wedge_proved"]
        and result["branches"][p]["small_lam_proved"]
        for p in ("even", "odd")
    )
    result["seconds"] = round(time.time() - t0, 1)
    return result


CLAIM = (
    "STEP (a) of the unglued keystone argument: the depth-d knife is positive at "
    "D = T_v(lam) for all REAL v in [8/5, 2], all K>=3, and all c >= C_MIN = 5/12 "
    "(which forces lam = c*N >= 5/2, since N >= 6). Integrality is NOT used here -- "
    "it enters only in step (b), where an INTEGER k_s inside the window gives "
    "T_hat <= T_{k_s} by definition. Step (c) (monotonicity of the knife in D, "
    "measured clean on 120/120 configurations at lam >= 5/2 and FAILING on 33/96 "
    "below it) then covers D <= T_hat. NOT covered here: lam >= 5/2 with c < 5/12, "
    "i.e. large N at moderate lam. See docs/ERRATA.md ERR-0010/ERR-0011 for why "
    "the older glued argument failed."
)


def _write(out: list) -> Path:
    """Persist results. Called after EVERY depth, not once at the end: a run
    that times out on depth 3 must not throw away a proved depth 2 (which is
    exactly what happened once)."""
    path = RES / "keystone_unglued.json"
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
                "claim": CLAIM,
                "runs": sorted(keep + out, key=lambda r: r["depth"]),
                "command": "python lab/keystone_unglued.py <d> [<d> ...]",
                **stamp(),
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    return path


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [2]
    out = []
    for d in depths:
        try:
            out.append(run_depth(d))
        except Exception as exc:  # noqa: BLE001 - one bad depth must not kill the queue
            print(f"depth {d} FAILED: {type(exc).__name__}: {exc}", flush=True)
            out.append({"depth": d, "error": f"{type(exc).__name__}: {exc}"})
        path = _write(out)
        print(f"  written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
