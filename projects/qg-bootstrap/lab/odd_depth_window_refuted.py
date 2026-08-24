"""REFUTATION of the fixed-window step (a) at odd depths, with exact witnesses.

ODD_DEPTH_DIAGNOSIS.md attributed the odd-depth Bernstein failure to
near-total cancellation (conditioning). That diagnosis is WRONG. The truth is
simpler and harsher: the statement being certified is FALSE at odd depths.

The step-(a) claim quantifies over the fixed window v in [8/5, 2]. At odd
depth d (knife order j = d+1 even), the knife has a genuine threshold in D --
the margin law of 2026-08-17: even-j knives MUST have a threshold, odd-j
knives cannot. Away from the integer argmin of T_k, the evaluation point
T_{v*lam} overshoots that threshold once lam is large, and the knife is
LEGITIMATELY negative there. Even depths (odd j, thresholdless) are immune,
which is the entire even/odd split. This is the ERR-0010 mechanism a second
time: the method demanded strictly more than the physics.

Two independent checks per witness: `build_branch` (the certified
construction) and `jacobi_coeff_rec` (the exact reference engine). Both must
agree the knife is NEGATIVE at the window point, and POSITIVE at the true
integer argmin of T_k at the same (K, c) -- the physics is untouched.

The false region was missed by every earlier scan because it needs BOTH
c in a narrow band (~0.52..0.67) AND K large (>= 54 at v=2): all grids
used c in {5/12, 1, 5, 7, 50, 60, ...} and stepped straight over the band.
The ERR-0005 mechanism (a grid that looks wide can be systematically blind),
third occurrence.

Run: python lab/odd_depth_window_refuted.py
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

# (depth, parity, K, c, v) -- all inside the certified box K>=3, c in
# [5/12, 50], v in [8/5, 2]. Chosen small enough that the reference engine
# runs in seconds.
WITNESSES = [
    (3, "even", 54, fmpq(239, 400), fmpq(2)),
    (3, "even", 60, fmpq(3, 5), fmpq(2)),
    (3, "even", 226, fmpq(3, 5), fmpq(8, 5)),
    (3, "odd", 54, fmpq(71, 120), fmpq(2)),
    (5, "even", 111, fmpq(71, 120), fmpq(2)),
    (5, "odd", 111, fmpq(47, 80), fmpq(2)),
]


def shore_D(k_s: fmpq, lam: fmpq) -> fmpq:
    B = lam * lam + (k_s * 2 - 2) * lam + 1
    kk2 = k_s * (k_s - 2)
    Pg = (k_s * 2 - 3) * B * 3 + k_s * k_s * (k_s - 2) * 2 - kk2 * 3
    return (Pg / (kk2 * 2)) * 2 + 3


def ref_knife_sign(j: int, n: int, m: int, lam: fmpq, k_s: fmpq) -> int:
    D = shore_D(k_s, lam)
    knife = (-1) ** m * jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
    return (knife > 0) - (knife < 0)


def integer_argmin_T(lam: fmpq) -> int:
    lo = max(3, int(float(lam) * 3 / 2))
    hi = int(float(lam) * 21 / 10) + 2
    best, bk = None, None
    for k in range(lo, hi):
        kf = fmpq(k)
        T = fmpq(3) * (kf * 2 - 3) / (kf * (kf - 2)) * (lam * lam + (kf * 2 - 2) * lam + 1) + kf * 2
        if best is None or T < best:
            best, bk = T, k
    return bk


def main() -> int:
    t0 = time.time()
    rows = []
    built: dict = {}
    for d, parity, K, c, v in WITNESSES:
        if (d, parity) not in built:
            built[(d, parity)] = build_branch(parity, d, elementary_symmetric(d))
        H = built[(d, parity)]
        N = 2 * K if parity == "even" else 2 * K + 1
        n, j = N + 1, d + 1
        m = n - j
        lam = c * N
        k_s = v * lam

        val = H.eval_at((fmpq(K), c, v))
        s_branch = (val > 0) - (val < 0)
        s_ref = ref_knife_sign(j, n, m, lam, k_s)

        k_hat = integer_argmin_T(lam)
        s_argmin = ref_knife_sign(j, n, m, lam, fmpq(k_hat))

        row = {
            "depth": d,
            "parity": parity,
            "K": K,
            "n": n,
            "c": str(c),
            "lam": str(lam),
            "v": str(v),
            "k_s": str(k_s),
            "sign_build_branch": s_branch,
            "sign_reference_engine": s_ref,
            "engines_agree": s_branch == s_ref,
            "window_point_negative": s_ref < 0,
            "integer_argmin_k": k_hat,
            "sign_at_true_shore_T_hat": s_argmin,
        }
        rows.append(row)
        print(
            f"d={d} {parity} K={K} c={c} v={v}: window sign {s_ref} "
            f"(branch {s_branch}, agree {s_branch == s_ref}); "
            f"at argmin k={k_hat}: sign {s_argmin}",
            flush=True,
        )

    refuted = all(r["engines_agree"] and r["window_point_negative"] for r in rows)
    physics_intact = all(r["sign_at_true_shore_T_hat"] > 0 for r in rows)
    out = {
        "claim_refuted": (
            "Step (a) fixed-window statement -- knife_d >= 0 at D = T_{v*lam}(lam) for all "
            "v in [8/5, 2] on the lo box -- is FALSE for odd depths d = 3, 5. Witnesses "
            "below are exact, inside the certified box, and confirmed by two independent "
            "engines. Even depths are unaffected (their certificates certified true "
            "statements). The physical claim (positivity at the true shore T_hat and below) "
            "shows NO violation: the knife is positive at the integer argmin at every "
            "witness point."
        ),
        "all_witnesses_confirmed": refuted,
        "physics_intact_at_all_witnesses": physics_intact,
        "witnesses": rows,
        "command": "python lab/odd_depth_window_refuted.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "odd_depth_window_refuted.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"refuted={refuted} physics_intact={physics_intact}  written {path}", flush=True)
    return 0 if refuted else 1


if __name__ == "__main__":
    raise SystemExit(main())
