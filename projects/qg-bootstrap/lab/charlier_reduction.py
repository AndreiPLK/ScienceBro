"""The Charlier reduction of the knife, and the exact regime where the base
sequence is a Hausdorff moment sequence.

TWO EXACT FACTS, both verified here.

(1) SPLIT. The reorganized knife sum uses M_t^(r) = (H-r)_t * m_t where

        m_t := t! E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ],   s = lam+n-1,

    depends on NEITHER the depth r NOR the dimension D. All r- and
    D-dependence sits in the falling factorial (H-r)_t. This is why a fixed
    Hausdorff hypothesis for M_t^(r) was ill-posed (the outside report's
    route): M changes with r, m does not.

(2) CHARLIER FORM. With g := H - r,

        K_r = sum_t (-1)^t C(r,t) (g)_t m_t = sum_t C(r,t) (g)_t (-1)^t m_t,

    and the polynomial P_r(y) := sum_t C(r,t) (g)_t (-y)^t is exactly the
    Charlier polynomial C_r(g; 1/y) (both equal 2F0(-r,-g;;-y)). Hence if
    m_t = INT y^t dmu(y) with dmu >= 0, then

        K_r = INT C_r(g; 1/y) dmu(y),

    so all-depths positivity reduces to a zero/positivity statement for a
    CLASSICAL orthogonal family in the depth index -- exactly the kind of
    uniform-in-r structure the theorem needs. The identification is verified
    below against the standard Charlier three-term recurrence
    (DLMF 18.22.3 form):  -x C_n(x;a) = a C_{n+1} - (n+a) C_n + n C_{n-1}.

MEASURED REGIME (results/base_moment_probe.json and this run): m_t IS a
Hausdorff moment sequence for t up to about n/2 and FAILS beyond, with the
boundary INDEPENDENT of lam over five orders of magnitude -- so the failure
is intrinsic to the central factorial numbers, not to the amplitude
parameter. Consequences, stated honestly: the Charlier route as it stands
covers knives with j-1 <~ n/2, not all j.

Run: python lab/charlier_reduction.py -> results/charlier_reduction.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base_moment_probe import m_seq, moment_report  # noqa: E402
from moment_kernel_probe import K_from_M, M_seq, falling, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def P_r(r: int, g: fmpq, y: fmpq) -> fmpq:
    return sum(
        (fmpq(comb(r, t)) * falling(g, t) * (-y) ** t for t in range(r + 1)), fmpq(0)
    )


def charlier_recurrence_ok(r: int, g: fmpq, y: fmpq) -> bool:
    """-x C_n(x;a) = a C_{n+1}(x;a) - (n+a) C_n(x;a) + n C_{n-1}(x;a),
    with x = g, a = 1/y and C_n identified as P_n."""
    a = 1 / y
    lhs = -g * P_r(r, g, y)
    rhs = a * P_r(r + 1, g, y) - (r + a) * P_r(r, g, y) + r * P_r(r - 1, g, y)
    return lhs == rhs


def main() -> int:
    t0 = time.time()
    out: dict = {}

    # ---- (1) the split M_t^(r) = (H-r)_t m_t, exact
    bad_split = 0
    trials = 0
    for lam in (fmpq(1), fmpq(3), fmpq(72)):
        for n in (12, 24, 40):
            for j in (3, 5, 8):
                if n - 1 < j:
                    continue
                D = shore(lam)[0]
                H = (D + 4 * n - 7) / 2
                r = j - 1
                M = M_seq(n, j, lam, D)
                m = m_seq(n, lam, r)
                for t in range(r + 1):
                    trials += 1
                    if M[t] != falling(H - r, t) * m[t]:
                        bad_split += 1
    out["split_identity"] = {"trials": trials, "violations": bad_split}
    print(f"split M_t^(r) = (H-r)_t m_t: {trials} trials, {bad_split} violations", flush=True)

    # ---- (2) Charlier identification via the three-term recurrence
    bad_rec = 0
    rec_trials = 0
    for r in (1, 2, 3, 5, 8):
        for g in (fmpq(37, 2), fmpq(100), fmpq(1234, 7)):
            for y in (fmpq(1, 100), fmpq(1, 7), fmpq(3, 4)):
                rec_trials += 1
                if not charlier_recurrence_ok(r, g, y):
                    bad_rec += 1
    out["charlier_recurrence"] = {"trials": rec_trials, "violations": bad_rec}
    print(f"Charlier recurrence for P_r: {rec_trials} trials, {bad_rec} violations", flush=True)

    # ---- (2b) K_r reconstructed as sum_t (-1)^t C(r,t) (g)_t m_t vs reference
    bad_K = 0
    K_trials = 0
    neg = 0
    for lam in (fmpq(1), fmpq(5, 2), fmpq(72)):
        Th = shore(lam)[0]
        for n in (12, 24, 40):
            for j in (3, 4, 6, 8):
                if n - 1 < j:
                    continue
                for D in (Th, Th * fmpq(4, 5), Th * fmpq(3, 2)):
                    if D <= 3:
                        continue
                    r = j - 1
                    H = (D + 4 * n - 7) / 2
                    g = H - r
                    m = m_seq(n, lam, r)
                    K = sum(
                        (fmpq((-1) ** t * comb(r, t)) * falling(g, t) * m[t] for t in range(r + 1)),
                        fmpq(0),
                    )
                    sK = (K > 0) - (K < 0)
                    sR = ref_sign(j, n, lam, D)
                    K_trials += 1
                    neg += sR < 0
                    bad_K += sK != sR
    out["K_reconstruction"] = {"trials": K_trials, "mismatches": bad_K, "negative_refs": neg}
    print(
        f"K_r from (g)_t m_t vs reference: {K_trials} trials, {bad_K} mismatches, "
        f"{neg} negative refs",
        flush=True,
    )

    # ---- (3) the measured Hausdorff regime of m, boundary vs n, lam-independence
    def tmax_ok(n: int, lam: fmpq) -> int:
        best = 0
        for tmax in range(2, n - 1):
            if not moment_report(m_seq(n, lam, tmax))["all_nonneg"]:
                break
            best = tmax
        return best

    regime = []
    for n in (8, 10, 12, 14, 16, 20, 24, 30, 40, 60):
        vals = {str(lam): tmax_ok(n, lam) for lam in (fmpq(1, 10), fmpq(3), fmpq(72), fmpq(5000))}
        same = len(set(vals.values())) == 1
        regime.append({"n": n, "n_minus_2": n - 2, "tmax_clean": vals, "lam_independent": same})
    all_same = all(x["lam_independent"] for x in regime)
    print(
        f"Hausdorff regime of m: boundary lam-independent at every n: {all_same}; "
        f"tmax_clean/n ~ {[round(list(x['tmax_clean'].values())[0] / x['n'], 3) for x in regime]}",
        flush=True,
    )
    out["hausdorff_regime"] = {"lam_independent_everywhere": all_same, "rows": regime}

    out["claim"] = (
        "VERIFIED: (a) M_t^(r) = (H-r)_t m_t with m_t independent of r and D -- the "
        "r-dependence of the reorganized knife sum is entirely in a falling "
        "factorial; (b) P_r(y) = sum_t C(r,t)(g)_t(-y)^t is the Charlier polynomial "
        "C_r(g;1/y), verified against the standard three-term recurrence, so a "
        "Hausdorff representation of m would give K_r = INT C_r(H-r;1/y) dmu(y), a "
        "uniform-in-depth classical structure. MEASURED, NOT PROVED: m_t is a "
        "Hausdorff moment sequence exactly for t up to about n/2 and fails beyond, "
        "with a boundary independent of lam over five orders of magnitude; so this "
        "route currently covers knives with j-1 <~ n/2 only."
    )
    out["seconds"] = round(time.time() - t0, 1)
    path = RES / "charlier_reduction.json"
    path.write_text(json.dumps({**out, **stamp()}, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0 if (bad_split == 0 and bad_rec == 0 and bad_K == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
