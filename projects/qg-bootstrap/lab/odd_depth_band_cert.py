"""Certificate for the odd-depth lam in [5/2, 7] band at fixed k_s = 8.

The k-window certificate (odd_depth_kwindow_cert.py) covers lam >= 7, where
step (b)'s bracketing theorem places the integer argmin inside the delta
window. Below lam = 7 the chain uses fixed shore integers instead:
k_s = 4 on lam <= 5/2 (certified inside keystone_unglued's small piece) and
k_s = 8 on [5/2, 7] -- which until now rested on 1085 measured trials.
This certifies the k_s = 8 band for the odd depths 3 and 5.

Construction by SUBSTITUTION (ERR-0012): `build_small_lam` from the
validated keystone_unglued, with its module constant KS_SMALL set to 8 for
the call -- the identical code path that already certified the k_s = 4
piece, evaluated at a different fixed integer. Self-checked against the
exact reference engine on the band AND outside it (so the reference sign
actually goes negative and the check is non-vacuous; VACUOUS is printed
otherwise).

Region: K in [3, inf) compactified, lam in [5/2, 7]. 2-variable, tiny.

Run: python lab/odd_depth_band_cert.py [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F  # ENGINE-OK: interface glue for the reference engine
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keystone_unglued  # noqa: E402
from depth_d_proof import elementary_symmetric  # noqa: E402
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402
from keystone_unglued import compactify, prove_box  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

KS_BAND = fmpq(8)
LAM_LO = fmpq(5, 2)
LAM_HI = fmpq(7)


def build_band(parity: str, d: int, e_polys: dict):
    """build_small_lam at KS_SMALL = 8, by swapping the module constant for
    the duration of the call (same validated code path, different integer)."""
    saved = keystone_unglued.KS_SMALL
    try:
        keystone_unglued.KS_SMALL = KS_BAND
        return keystone_unglued.build_small_lam(parity, d, e_polys)
    finally:
        keystone_unglued.KS_SMALL = saved


def ref_sign(j: int, n: int, m: int, lam: fmpq, k_s: fmpq) -> int:
    B = lam * lam + (k_s * 2 - 2) * lam + 1
    kk2 = k_s * (k_s - 2)
    Pg = (k_s * 2 - 3) * B * 3 + k_s * k_s * (k_s - 2) * 2 - kk2 * 3
    D = (Pg / (kk2 * 2)) * 2 + 3
    knife = (-1) ** m * jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
    return (knife > 0) - (knife < 0)


def self_check(d: int, S_even, S_odd) -> dict:
    j = d + 1
    rep = {"trials": 0, "mismatches": [], "negative_refs": 0}
    # lam probes: inside the band, plus far outside where the odd-depth knife
    # at T_8 must eventually go negative (large lam overshoots the threshold).
    lam_probes = [
        fmpq(5, 2), fmpq(3), fmpq(7, 2), fmpq(9, 2), fmpq(6), fmpq(7),
        fmpq(30), fmpq(100), fmpq(300),
    ]
    for parity, S in (("even", S_even), ("odd", S_odd)):
        for K_val in (3, 5, 11, 40, 200):
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            m = n - j
            if m < 0:
                continue
            for lam in lam_probes:
                got = S.eval_at((fmpq(K_val), lam, fmpq(0)))
                sg = (got > 0) - (got < 0)
                se = ref_sign(j, n, m, lam, KS_BAND)
                rep["trials"] += 1
                rep["negative_refs"] += se < 0
                if sg != se:
                    rep["mismatches"].append(f"{parity} K={K_val} lam={lam}: {sg} vs {se}")
    return rep


def run_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    S = {p: build_band(p, d, e_polys) for p in ("even", "odd")}
    rep = self_check(d, S["even"], S["odd"])
    vac = " VACUOUS" if rep["negative_refs"] == 0 else ""
    print(
        f"depth {d}: self-check {rep['trials']} trials, {len(rep['mismatches'])} mismatches, "
        f"{rep['negative_refs']} negative refs{vac}",
        flush=True,
    )
    if rep["mismatches"]:
        for msg in rep["mismatches"][:5]:
            print("  MISMATCH", msg, flush=True)
        return {"depth": d, "self_check_passed": False, "mismatches": rep["mismatches"][:10]}

    out = {
        "depth": d,
        "self_check_trials": rep["trials"],
        "self_check_passed": True,
        "negative_reference_signs": rep["negative_refs"],
        "k_s": str(KS_BAND),
        "lam_band": [str(LAM_LO), str(LAM_HI)],
        "branches": {},
    }
    for parity in ("even", "odd"):
        Sk = compactify(S[parity], 0, 3)
        ok, boxes, open_boxes = prove_box(
            Sk, [(fmpq(0), fmpq(999, 1000)), (LAM_LO, LAM_HI), (fmpq(0), fmpq(1))]
        )
        print(f"  [{parity}] proved={ok} boxes={boxes} open={len(open_boxes)}", flush=True)
        out["branches"][parity] = {"proved": ok, "boxes": boxes, "open": len(open_boxes)}
    out["proved_both"] = all(out["branches"][p]["proved"] for p in ("even", "odd"))
    out["seconds"] = round(time.time() - t0, 1)
    return out


CLAIM = (
    "The lam in [5/2, 7] band of the odd-depth chain (ERR-0013 repair): the depth-d "
    "knife is positive at D = T_8(lam) for all lam in [5/2, 7] and all levels K >= 3 "
    "(compactified), both parities. T_hat <= T_8 holds by definition of the integer "
    "minimum, and step (c) monotonicity carries positivity down. Replaces the "
    "1085-trial measurement of UNGLUED_KEYSTONE.md's k_s = 8 band for depths 3, 5."
)


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [3, 5]
    out = []
    for d in depths:
        out.append(run_depth(d))
        path = RES / "odd_depth_band_cert.json"
        path.write_text(
            json.dumps({"claim": CLAIM, "runs": out, **stamp()}, indent=1), encoding="utf-8"
        )
        print(f"  written {path}", flush=True)
    return 0 if all(r.get("proved_both") for r in out) else 1


if __name__ == "__main__":
    raise SystemExit(main())
