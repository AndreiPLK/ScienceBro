"""Certify unimodality of dT/dk on the window: T is strictly CONVEX in k.

Step (b)'s bracketing theorem (UNGLUED_KEYSTONE.md) concluded "the integer
argmin is one of the two integers bracketing k*" from a MEASURED unimodality
of dT/dk on the window (400-point sweeps). This certifies the stronger and
simpler fact d^2T/dk^2 > 0 on k in [8/5 lam, 2 lam], lam >= 7 -- convexity
makes dT/dk strictly increasing, so it changes sign exactly once and the
bracketing conclusion needs no sweep.

Derivation, exact and mechanical. With U = k(k-2), B = lam^2+(2k-2)lam+1,
N1 = 3(2k-3)B + 2kU, we have T = N1/U and

    T'' * U^3 = U*(N1''*U - N1*U'') - 2*U'*(N1'*U - N1*U')   (' = d/dk)

U^3 > 0 for k > 2, so sign(T'') = sign of that polynomial in (k, lam).
Substituting k = sigma*lam maps the window to the box
sigma in [8/5, 2] x lam in [7, inf) (compactified); the substitution is an
exponent remap exactly like the certifier's rho trick.

Self-check (non-vacuous): the polynomial's value is compared against an
INDEPENDENT computation of T'' via flint fmpq_poly quotient-rule derivatives
at fixed rational lam -- exact equality of values, not just signs -- and
sign probes are taken outside k > 2 ... including k < 2 where U^3 < 0 flips
the relation, and small-k regions where T is genuinely concave, so the
reference goes negative.

Run: python lab/unimodality_cert.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_unglued import NPoly, compactify, prove_box  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

SIG_LO = fmpq(8, 5)
SIG_HI = fmpq(2)
LAM_MIN = fmpq(7)


def dk(p: NPoly) -> NPoly:
    """d/dk on NPoly slot 0."""
    out: dict = {}
    for e, c in p.d.items():
        if e[0] == 0:
            continue
        key = (e[0] - 1, e[1], e[2])
        out[key] = out.get(key, fmpq(0)) + c * e[0]
    return NPoly(out)


def build_conv() -> NPoly:
    """T'' * U^3 as an NPoly in (k, lam); slot 2 unused."""
    k = NPoly.var(0)
    lam = NPoly.var(1)
    one = NPoly.const(1)
    U = k * (k - NPoly.const(2))
    B = lam * lam + (k * fmpq(2) - NPoly.const(2)) * lam + one
    N1 = (k * fmpq(2) - NPoly.const(3)) * B * fmpq(3) + k * U * fmpq(2)
    Up, N1p = dk(U), dk(N1)
    Upp, N1pp = dk(Up), dk(N1p)
    return U * (N1pp * U - N1 * Upp) - Up * (N1p * U - N1 * Up) * fmpq(2)


def tpp_reference(k0: fmpq, lam0: fmpq) -> fmpq:
    """T''(k0) at fixed lam0 via fmpq_poly quotient-rule derivatives --
    an independent route sharing no code with build_conv."""
    lam = lam0
    U = fmpq_poly([0, -2, 1])  # k^2 - 2k
    B0 = lam * lam + 1
    # N1(k) = 3(2k-3)(lam^2 + (2k-2)lam + 1) + 2k(k^2-2k)
    N1 = (
        fmpq_poly([-3, 2]) * fmpq_poly([B0 - lam * 2, lam * 2]) * 3
        + fmpq_poly([0, 0, -4, 2])
    )
    Up, N1p = U.derivative(), N1.derivative()
    # T' = (N1' U - N1 U')/U^2 ; T'' = d/dk of that, quotient rule again
    num1 = N1p * U - N1 * Up
    num2 = num1.derivative() * U * U - num1 * (U * U).derivative()
    # T'' = num2 / U^4
    return num2(k0) / (U(k0) ** 4)


def self_check(C: NPoly) -> dict:
    rep = {"trials": 0, "mismatches": 0, "negative_refs": 0}
    pts = [
        (fmpq(12), fmpq(7)), (fmpq(14), fmpq(7)), (fmpq(56, 5), fmpq(7)),
        (fmpq(120), fmpq(70)), (fmpq(173), fmpq(100)), (fmpq(346), fmpq(200)),
        # outside the window: k > 2 stays convex in every probe, so honest
        # negative references need k in (0, 2) where U = k(k-2) < 0 and T''
        # genuinely changes sign; the identity C = T'' U^3 is still exact.
        (fmpq(3), fmpq(7)), (fmpq(5, 2), fmpq(1)), (fmpq(4), fmpq(50)),
        (fmpq(3), fmpq(100)), (fmpq(7, 2), fmpq(30)),
        (fmpq(1), fmpq(1)), (fmpq(3, 2), fmpq(5)), (fmpq(1, 2), fmpq(2)),
        (fmpq(1), fmpq(10)), (fmpq(7, 4), fmpq(3)),
    ]
    for k0, lam0 in pts:
        val = C.eval_at((k0, lam0, fmpq(0)))
        ref = tpp_reference(k0, lam0)
        u3 = (k0 * (k0 - 2)) ** 3
        rep["trials"] += 1
        rep["negative_refs"] += ref < 0
        if val != ref * u3:
            rep["mismatches"] += 1
            print(f"  MISMATCH at k={k0} lam={lam0}: {val} vs {ref * u3}", flush=True)
    return rep


def main() -> int:
    t0 = time.time()
    C = build_conv()
    rep = self_check(C)
    vac = " VACUOUS" if rep["negative_refs"] == 0 else ""
    print(
        f"self-check {rep['trials']} exact-value trials, {rep['mismatches']} mismatches, "
        f"{rep['negative_refs']} negative refs{vac}",
        flush=True,
    )
    if rep["mismatches"] or rep["negative_refs"] == 0:
        return 1

    # substitute k = sigma*lam (exponent remap), box sigma x lam-compactified
    Csub = NPoly({(e[0], e[0] + e[1], e[2]): c for e, c in C.d.items()})
    # slot 0 = sigma exponent, slot 1 = total lam exponent
    Ck = compactify(Csub, 1, LAM_MIN)
    ok, boxes, open_boxes = prove_box(
        Ck, [(SIG_LO, SIG_HI), (fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(1))]
    )
    print(f"convexity on window: proved={ok} boxes={boxes} open={len(open_boxes)}", flush=True)

    out = {
        "claim": (
            "d^2T/dk^2 > 0 on k in [8/5 lam, 2 lam] for all lam >= 7 (lam compactified): "
            "T_k(lam) is strictly convex in k on the step-(b) window, so dT/dk is strictly "
            "increasing there, has exactly one sign change, and the integer argmin is one of "
            "the two integers bracketing k* -- the unimodality premise of the bracketing "
            "theorem in UNGLUED_KEYSTONE.md, previously a 400-point measurement, is now "
            "certified. Verified by exact-value comparison against an independent "
            "fmpq_poly quotient-rule computation of T'' (non-vacuous: T is genuinely "
            "concave at small k, and those probes go negative)."
        ),
        "self_check_trials": rep["trials"],
        "negative_reference_signs": rep["negative_refs"],
        "proved": ok,
        "boxes": boxes,
        "open": len(open_boxes),
        "command": "python lab/unimodality_cert.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "unimodality_cert.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
