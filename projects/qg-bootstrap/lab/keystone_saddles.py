"""ACTIVE SADDLES: finishing the one line we own and never completed.

The inventory (research/inventory-of-facts.md) showed that every unused asset
of this programme sits in one place -- the contour / saddle material we
abandoned in the morning when a naive sum over ALL saddles missed by 250 orders
of magnitude. The failure was not the method; it was that the Stokes topology
was never determined, i.e. we summed every critical point instead of only the
ACTIVE ones.

The setup simplifies more than we realised. The bracket is a COEFFICIENT OF A
PRODUCT OF TWO POLYNOMIALS:

    SUM_t (-1)^t E_2t(n) A_t  =  [x^{j-1}]  G2(x) * Psi_rev(x) ,

    G2(x)      = SUM_t (-1)^t E_2t(n) x^t     (the perfect square)
    Psi_rev(x) = x^{j-1} SUM_t A_t x^{-t}     (the reversed weight polynomial)

so with P = G2 * Psi_rev and N = j-1,

    bracket = (1/2 pi i) INT P(x) / x^{N+1} dx .

Saddle points therefore solve a POLYNOMIAL equation, not a transcendental one:

    d/dx [ log P(x) - (N+1) log x ] = 0   <=>   x P'(x) = (N+1) P(x) .

That is the whole point of this module: the critical points are computable
exactly, and then we can ask empirically WHICH SUBSET reproduces the true
coefficient -- reading off the Stokes topology from data instead of guessing it.

Method:
  1. build P exactly (rational arithmetic);
  2. solve x P' - (N+1) P = 0 for all critical points;
  3. evaluate the standard saddle contribution of each;
  4. compare the true coefficient with (a) the sum over all saddles and
     (b) the best-matching subsets, smallest first.

Run: python lab/keystone_saddles.py -> results/keystone_saddles.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import Hhat_coeffs  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def build_P(j: int, n: int, lam: F) -> list[F]:
    """P = G2 * Psi_rev, ascending coefficients, exact."""
    e = e_doubled_int(n)
    g2 = [F((-1) ** t) * F(e[t]) for t in range(min(len(e), j))]
    # Hhat_coeffs returns the weight polynomial already reversed in u:
    # entry k is the coefficient of u^{j-1-k}, i.e. exactly Psi_rev.
    psi_rev = list(Hhat_coeffs(j, n, lam))[::-1]
    out = [F(0)] * (len(g2) + len(psi_rev) - 1)
    for i, a in enumerate(g2):
        if a == 0:
            continue
        for k, b in enumerate(psi_rev):
            out[i + k] += a * b
    return out


def coeff(P: list[F], N: int) -> F:
    return P[N] if N < len(P) else F(0)


def saddle_points(P: list[F], N: int) -> list[complex]:
    """Roots of x P'(x) - (N+1) P(x) = 0."""
    dP = [P[i] * i for i in range(1, len(P))]
    # x*P' has coefficients dP shifted up by one
    lhs = [F(0)] * (len(P) + 1)
    for i, c in enumerate(dP):
        lhs[i + 1] += c
    for i, c in enumerate(P):
        lhs[i] -= (N + 1) * c
    while lhs and lhs[-1] == 0:
        lhs.pop()
    if len(lhs) <= 1:
        return []
    co = [float(c) for c in lhs][::-1]
    return list(np.roots(co))


def contribution(P: list[F], N: int, xs: complex) -> complex:
    """Standard saddle contribution to (1/2 pi i) INT P/x^{N+1} dx."""
    pf = np.polynomial.Polynomial([float(c) for c in P])
    phi = lambda z: np.log(pf(z) + 0j) - (N + 1) * np.log(z + 0j)  # noqa: E731
    h = 1e-5 * max(1.0, abs(xs))
    d2 = (phi(xs + h) - 2 * phi(xs) + phi(xs - h)) / h**2
    if d2 == 0 or not np.isfinite(d2):
        return 0j
    return np.exp(phi(xs)) / np.sqrt(2 * np.pi * d2)


def main() -> int:
    t0 = time.time()
    rows = []
    for j, n, lam in ((6, 10, F(1)), (8, 12, F(1)), (8, 12, F(3)), (10, 14, F(1))):
        P = build_P(j, n, lam)
        N = j - 1
        true = coeff(P, N)
        sads = saddle_points(P, N)
        contrib = [(s, contribution(P, N, s)) for s in sads]
        contrib = [(s, c) for s, c in contrib if np.isfinite(c)]
        all_sum = sum(c for _, c in contrib)
        tv = float(true)
        # find the smallest subset whose sum matches the true coefficient
        best = None
        idx = range(len(contrib))
        for size in range(1, min(4, len(contrib)) + 1):
            for combo in combinations(idx, size):
                s = sum(contrib[i][1] for i in combo)
                if tv != 0 and abs(s.real - tv) / abs(tv) < 0.25:
                    best = (size, [i for i in combo], float(abs(s.real - tv) / abs(tv)))
                    break
            if best:
                break
        rows.append(
            {
                "j": j,
                "n": n,
                "lam": str(lam),
                "true_coefficient": tv,
                "n_saddles": len(contrib),
                "sum_over_ALL_saddles": float(all_sum.real),
                "ratio_all_over_true": (float(all_sum.real) / tv) if tv else None,
                "smallest_matching_subset_size": best[0] if best else None,
                "matching_subset_indices": best[1] if best else None,
                "relative_error_of_that_subset": best[2] if best else None,
                "saddle_moduli": [float(abs(s)) for s, _ in contrib],
            }
        )
        print(
            f"  j={j} n={n} lam={lam}: {len(contrib)} saddles, "
            f"all-sum/true = "
            f"{(float(all_sum.real) / tv if tv else float('nan')):.3e}, "
            f"best subset "
            f"{best[0] if best else None} "
            f"(rel.err {best[2]:.3f})"
            if best
            else "no subset matched",
            flush=True,
        )

    out = {
        "purpose": "determine WHICH saddles are active, empirically, by"
        " finding the smallest subset that reproduces the exact"
        " coefficient -- the Stokes question that stopped the"
        " asymptotic route this morning",
        "key_simplification": "the bracket is [x^{j-1}] of a PRODUCT of two"
        " polynomials, so saddles solve the polynomial"
        " equation x P'(x) = (N+1) P(x)",
        "rows": rows,
        "command": "python lab/keystone_saddles.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_saddles.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("saddle analysis written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
