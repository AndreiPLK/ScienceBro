"""The normalized depth-kernel sequence M_t^(r): exact tests of the
outside report's programme (research/reading-notes/keystone-outside-2026-08-28).

The report reorganizes the repository's exact closed sum
(lab/knife_closed_form.py):

    sign(knife_j) = sign( K_r ),   r = j - 1,
    K_r = SUM_{t=0}^{r} (-1)^t E_{2t}(n) s^{-2t} R_t,
    R_t = [prod (j-i)] [prod (D+4n-2j-5-2(i-1))] / [prod (n-i)][prod (2n-1-2i)]

into an alternating binomial transform. With H = (D+4n-7)/2 and falling
factorials (a)_t = a(a-1)...(a-t+1):

    prod_{i<=t} (j-i)                 = (r)_t * r/(r-t+1)... = r!/(r-t)! = C(r,t) t!
    prod_{i<=t} (D+4n-2j-5-2(i-1))    = 2^t (H-r)_t
    prod_{i<=t} (n-i)                 = (n-1)_t
    prod_{i<=t} (2n-1-2i)             = 2^t (n-3/2)_t

so K_r = SUM_t (-1)^t C(r,t) M_t^(r) with

    M_t^(r) = t! (H-r)_t E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ].

NOTE the report's own page-7 display writes R_t inverted relative to the
repository's; the derivation here follows the REPOSITORY formula and is
verified against the exact reference engine before anything else is trusted.

Tests, all exact fmpq (floats only in prints):
  1. RECONSTRUCTION: sign(K_r) vs the reference engine at positive, ZERO and
     negative knife points (non-vacuous by construction).
  2. DEPTH RECURSION: M_t^(r+1) = (1 - t/(H-r)) M_t^(r) exactly.
  3. HAUSDORFF-MOMENT EVIDENCE: leading principal minors of the truncated
     Hankel matrices [M_{a+b}], [M_{a+b+1}] and the [0,1]-localizer
     [M_{a+b} - M_{a+b+1}], at the shore, below it, and above it -- the
     report predicts the [0,1] support condition should FAIL above the
     even-knife threshold and the structure should persist for odd knives.
  4. DEPTH-KERNEL MINORS: the report proves adjacent 2x2 minors of
     B_{r,t} = C(r,t)(H-r)_t t! factor as B*B*(H-2r-1); test solid 3x3 and
     4x4 minors symbolically in H for a uniform factorization.

Run: python lab/moment_kernel_probe.py -> results/moment_kernel_probe.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F  # ENGINE-OK: interface glue for the reference engine
from math import comb
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def E2_list(n: int, tmax: int) -> list[int]:
    """E_{2t}(n) = e_t({(n-2k)^2 : k=1..n-1}), exact integers."""
    vals = [(n - 2 * k) ** 2 for k in range(1, n)]
    tmax = min(tmax, len(vals))
    e = [0] * (tmax + 1)
    e[0] = 1
    for cnt, a in enumerate(vals, 1):
        for t in range(min(cnt, tmax), 0, -1):
            e[t] += a * e[t - 1]
    return e


def falling(a: fmpq, t: int) -> fmpq:
    out = fmpq(1)
    for i in range(t):
        out *= a - i
    return out


def M_seq(n: int, j: int, lam: fmpq, D: fmpq) -> list[fmpq]:
    """M_t^(r) for t = 0..r, r = j-1, from the repository closed form."""
    r = j - 1
    H = (D + 4 * n - 7) / 2
    s = lam + n - 1
    E = E2_list(n, r)
    out = []
    for t in range(r + 1):
        num = falling(fmpq(1) * 1, 0)  # placeholder, replaced below
        num = fmpq(1)
        for i in range(1, t + 1):
            num *= i  # t!
        num *= falling(H - r, t) * E[t]
        den = (s ** (2 * t)) * falling(fmpq(n - 1), t) * falling(fmpq(2 * n - 3, 2), t)
        out.append(num / den)
    return out


def K_from_M(M: list[fmpq]) -> fmpq:
    r = len(M) - 1
    return sum((fmpq((-1) ** t * comb(r, t)) * M[t] for t in range(r + 1)), fmpq(0))


def ref_sign(j: int, n: int, lam: fmpq, D: fmpq) -> int:
    m = n - j
    knife = (-1) ** m * jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
    return (knife > 0) - (knife < 0)


def T_k(k: fmpq, lam: fmpq) -> fmpq:
    return fmpq(3) * (k * 2 - 3) / (k * (k - 2)) * (lam * lam + (k * 2 - 2) * lam + 1) + k * 2


def shore(lam: fmpq) -> tuple[fmpq, int]:
    lo = max(3, int(float(lam) * 12 // 10))
    hi = int(float(lam) * 25 // 10) + 4
    best, bk = None, None
    for k in range(lo, hi):
        T = T_k(fmpq(k), lam)
        if best is None or T < best:
            best, bk = T, k
    return best, bk


def leading_minors(mat: list[list[fmpq]]) -> list[fmpq]:
    """Leading principal minors, exact (fraction-free Gaussian via fmpq)."""
    from copy import deepcopy

    n = len(mat)
    out = []
    a = deepcopy(mat)

    # simple exact determinant per leading size (sizes are tiny: <= 5)
    def det(sz: int) -> fmpq:
        m = [row[:sz] for row in a[:sz]]
        d = fmpq(1)
        for c in range(sz):
            piv = None
            for rr in range(c, sz):
                if m[rr][c] != 0:
                    piv = rr
                    break
            if piv is None:
                return fmpq(0)
            if piv != c:
                m[c], m[piv] = m[piv], m[c]
                d = -d
            d *= m[c][c]
            inv = 1 / m[c][c]
            for rr in range(c + 1, sz):
                f = m[rr][c] * inv
                if f != 0:
                    for cc in range(c, sz):
                        m[rr][cc] -= f * m[c][cc]
        return d

    for sz in range(1, n + 1):
        out.append(det(sz))
    return out


# hankel_report round-trips exact minors through str(), and CPython caps
# int->str at 4300 digits by default.  Those minors pass 4300 digits somewhere
# around n = 100, so the cap turns into a ValueError in every consumer of this
# module at large n -- which is exactly where one wants to look.  Raised once,
# here, rather than in each caller.
sys.set_int_max_str_digits(2_000_000)


def hankel_report(M: list[fmpq]) -> dict:
    """Truncated Hankel + localizer minors from moments M_0..M_r."""
    r = len(M) - 1
    q0 = r // 2  # [M_{a+b}] needs a+b <= r
    q1 = (r - 1) // 2
    H0 = [[M[a + b] for b in range(q0 + 1)] for a in range(q0 + 1)]
    rep = {"H0_minors": [str(x) for x in leading_minors(H0)]}
    if q1 >= 0:
        H1 = [[M[a + b + 1] for b in range(q1 + 1)] for a in range(q1 + 1)]
        L01 = [[M[a + b] - M[a + b + 1] for b in range(q1 + 1)] for a in range(q1 + 1)]
        rep["H1_minors"] = [str(x) for x in leading_minors(H1)]
        rep["L01_minors"] = [str(x) for x in leading_minors(L01)]
    rep["all_nonneg"] = all(
        fmpq(x) >= 0 for key in rep for x in (rep[key] if isinstance(rep[key], list) else [])
    )
    return rep


def main() -> int:
    t0 = time.time()
    out: dict = {"reconstruction": [], "recursion_ok": True, "hankel": [], "kernel_minors": {}}

    # ---- 1. reconstruction vs reference, incl. zero and negative points
    mismatches = 0
    neg_refs = 0
    zero_refs = 0
    cases = []
    for lam in (fmpq(1), fmpq(5, 2), fmpq(7), fmpq(72), fmpq(650, 3)):
        Th, kh = shore(lam)
        for j in (3, 4, 5, 6, 7, 8):
            n_min = j + 1
            for n in (max(8, n_min), 15, 40):
                if n - 1 < j:
                    continue
                for D in (Th, Th * fmpq(9, 10), Th + 4, Th * fmpq(3, 2), fmpq(4)):
                    if D <= 3:
                        continue
                    M = M_seq(n, j, lam, D)
                    sK = (K_from_M(M) > 0) - (K_from_M(M) < 0)
                    sR = ref_sign(j, n, lam, D)
                    mismatches += sK != sR
                    neg_refs += sR < 0
                    zero_refs += sR == 0
                    cases.append((str(lam), j, n, str(D), sK, sR))
    out["reconstruction"] = {
        "trials": len(cases),
        "mismatches": mismatches,
        "negative_refs": neg_refs,
        "zero_refs": zero_refs,
        "sample_fail": [c for c in cases if c[4] != c[5]][:5],
    }
    print(
        f"reconstruction: {len(cases)} trials, {mismatches} mismatches, "
        f"{neg_refs} negative refs, {zero_refs} zero refs",
        flush=True,
    )
    if mismatches:
        return 1

    # ---- 2. exact depth recursion
    bad_rec = 0
    for lam in (fmpq(3), fmpq(50)):
        for n in (12, 30):
            for j in (3, 4, 5, 6, 7):
                D = shore(lam)[0]
                H = (D + 4 * n - 7) / 2
                r = j - 1
                M_r = M_seq(n, j, lam, D)
                M_r1 = M_seq(n, j + 1, lam, D)  # r+1 = j
                for t in range(r + 1):
                    lhs = M_r1[t]
                    rhs = (1 - fmpq(t) / (H - r)) * M_r[t]
                    if lhs != rhs:
                        bad_rec += 1
    out["recursion_ok"] = bad_rec == 0
    print(f"depth recursion M_t^(r+1) = (1 - t/(H-r)) M_t^(r): {bad_rec} violations", flush=True)

    # ---- 3. Hankel / [0,1]-localizer evidence
    for lam in (fmpq(3), fmpq(72), fmpq(650, 3)):
        Th, kh = shore(lam)
        for j in (6, 7, 8):  # need r >= 5 for informative minors
            for n in (max(12, j + 2), 40):
                for tag, D in (
                    ("shore", Th),
                    ("below", Th * fmpq(4, 5)),
                    ("above", Th + 8),
                    ("far_above", Th * fmpq(3, 2)),
                ):
                    M = M_seq(n, j, lam, D)
                    rep = hankel_report(M)
                    sK = (K_from_M(M) > 0) - (K_from_M(M) < 0)
                    out["hankel"].append(
                        {
                            "lam": str(lam),
                            "j": j,
                            "n": n,
                            "where": tag,
                            "knife_sign": sK,
                            **rep,
                        }
                    )
    ok_shore = sum(1 for h in out["hankel"] if h["where"] in ("shore", "below") and h["all_nonneg"])
    tot_shore = sum(1 for h in out["hankel"] if h["where"] in ("shore", "below"))
    fail_above = sum(
        1 for h in out["hankel"] if h["where"] in ("above", "far_above") and not h["all_nonneg"]
    )
    tot_above = sum(1 for h in out["hankel"] if h["where"] in ("above", "far_above"))
    print(
        f"hankel/[0,1]-localizer: at/below shore nonneg {ok_shore}/{tot_shore}; "
        f"above shore FAILS {fail_above}/{tot_above}",
        flush=True,
    )

    # ---- 4. depth-kernel solid minors, symbolic in H
    # B_{r,t} = C(r,t) (H-r)_t t! ; minors of [B_{r+a, t+b}] as polys in H
    def B_poly(rr: int, tt: int) -> fmpq_poly:
        p = fmpq_poly([1])
        x = fmpq_poly([0, 1])  # H
        for i in range(tt):
            p = p * (x - rr - i)
        from math import factorial

        return p * fmpq(comb(rr, tt) * factorial(tt))

    def kernel_minor(r0: int, t0: int, q: int) -> fmpq_poly:
        rows = [[B_poly(r0 + a, t0 + b) for b in range(q)] for a in range(q)]

        # Laplace by first column (q <= 4, tiny)
        def det(mat):
            sz = len(mat)
            if sz == 1:
                return mat[0][0]
            tot = fmpq_poly([0])
            for i in range(sz):
                sub = [row[1:] for k2, row in enumerate(mat) if k2 != i]
                term = mat[i][0] * det(sub)
                tot = tot + term if i % 2 == 0 else tot - term
            return tot

        return det(rows)

    minors = {}
    for q in (2, 3, 4):
        for r0 in (5, 6, 8):
            for t0 in (0, 1, 2):
                if t0 + q - 1 > r0:
                    continue
                mp = kernel_minor(r0, t0, q)
                fac = mp.factor()
                minors[f"q{q}_r{r0}_t{t0}"] = str(fac)
    out["kernel_minors"] = minors
    print(f"kernel minors factored: {len(minors)} cases (see artifact)", flush=True)

    out["seconds"] = round(time.time() - t0, 1)
    path = RES / "moment_kernel_probe.json"
    path.write_text(json.dumps({**out, **stamp()}, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
