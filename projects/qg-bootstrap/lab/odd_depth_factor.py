"""Factorisation probe for the odd-depth jam (ODD_DEPTH_DIAGNOSIS.md).

Odd depths 3 and 5 fail the Bernstein certificate through near-total
cancellation (relative margin 7.8e-05 at the hard corner), while even depths
2, 4, 6 close. The diagnosis names two candidate fixes; the CHEAPER one is an
explicit factorisation of H: if a factor carries the cancellation, certifying
factors separately avoids it entirely.

This probe answers one question: does H(K, c, v) factor nontrivially over Q,
and if so, do the factors have better relative margin at the hard corner
K = 1000, c = 5/12, v = 2 than H itself?

Engine 2: flint throughout. H comes from the validated `build_branch`
(self-checked against the exact engine before factoring anything), converted
to fmpz_mpoly by clearing the common denominator (a positive integer, so signs
are untouched), then factored with FLINT's multivariate factorisation.

Run: python lab/odd_depth_factor.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpz, fmpz_mpoly_ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric  # noqa: E402
from keystone_unglued import NPoly, build_branch, self_check  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

# The hard corner from ODD_DEPTH_DIAGNOSIS.md: worst relative margin of the
# depth-3 even branch sits here.
HARD_POINT = (fmpq(1000), fmpq(5, 12), fmpq(2))


def npoly_to_mpoly(H: NPoly, ctx) -> tuple:
    """Clear denominators: return (P, den) with P integer and H = P / den.

    den is the positive lcm of all coefficient denominators, so sign(P) =
    sign(H) everywhere.
    """
    den = fmpz(1)
    for coeff in H.d.values():
        q = coeff.q
        den = den * q // den.gcd(q)
    terms = {expo: (coeff * den).p for expo, coeff in H.d.items()}
    return ctx.from_dict(terms), den


def relative_margin(H: NPoly, pt) -> tuple[fmpq, float]:
    """value / max |single monomial| at pt -- the cancellation measure used in
    the diagnosis. Exact fmpq; float only for printing."""
    biggest = fmpq(0)
    total = fmpq(0)
    for expo, coeff in H.d.items():
        term = coeff
        for slot, e in enumerate(expo):
            if e:
                term *= pt[slot] ** e
        total += term
        a = term if term >= 0 else -term
        if a > biggest:
            biggest = a
    rel = total / biggest if biggest != 0 else fmpq(0)
    return rel, float(rel)


def probe_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)

    # ERR-0011: self-check with wide ranges BEFORE trusting the construction.
    bad = self_check(
        d,
        e_polys,
        k_values=(3, 4, 6, 25, 300),
        c_values=[(5, 12), (1, 1), (50, 1)],
        v_values=[(8, 5), (2, 1)],
    )
    print(f"depth {d}: self-check {len(bad)} mismatches", flush=True)
    if bad:
        return {"depth": d, "self_check_passed": False, "mismatches": bad[:5]}

    out: dict = {"depth": d, "self_check_passed": True, "branches": {}}
    ctx = fmpz_mpoly_ctx.get(("K", "c", "v"))
    for parity in ("even", "odd"):
        H = build_branch(parity, d, e_polys)
        P, den = npoly_to_mpoly(H, ctx)
        _, mH = relative_margin(H, HARD_POINT)

        t1 = time.time()
        content, factors = P.factor()
        dt = time.time() - t1

        # verify the factorisation exactly before reporting anything
        recon = ctx.from_dict({(0, 0, 0): int(content)})
        for f, mult in factors:
            recon = recon * f**mult
        assert recon == P, f"factorisation does not reproduce P (depth {d} {parity})"

        finfo = []
        for f, mult in factors:
            fd = f.to_dict()
            Hf = NPoly({tuple(int(x) for x in e): fmpq(c) for e, c in fd.items()})
            _, mf = relative_margin(Hf, HARD_POINT)
            val = Hf.eval_at(HARD_POINT)
            finfo.append(
                {
                    "terms": len(fd),
                    "mult": mult,
                    "deg": [int(f.degrees()[i]) for i in range(3)],
                    "rel_margin_hard_corner": mf,
                    "sign_hard_corner": (val > 0) - (val < 0),
                }
            )
        print(
            f"  [{parity}] {len(H.d)} terms, content={content}, "
            f"{len(factors)} factor(s) {[fi['terms'] for fi in finfo]} "
            f"H-margin {mH:.2e} -> factor margins "
            f"{[f'{fi['rel_margin_hard_corner']:.2e}' for fi in finfo]}  ({dt:.0f}s)",
            flush=True,
        )
        out["branches"][parity] = {
            "terms": len(H.d),
            "content": str(content),
            "denominator_cleared": str(den),
            "rel_margin_H": mH,
            "n_factors": len(factors),
            "factors": finfo,
            "factor_seconds": round(dt, 1),
        }
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [3]
    out = []
    for d in depths:
        out.append(probe_depth(d))
        path = RES / "odd_depth_factor.json"
        path.write_text(
            json.dumps({"runs": out, **stamp()}, indent=1), encoding="utf-8"
        )
        print(f"  written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
