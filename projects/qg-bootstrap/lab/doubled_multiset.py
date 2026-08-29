"""The b-multiset is doubled: pairing, square factorisation, self-convolution.

The B-form runs over b_k = (n-2k)^2, k = 1..n-1.  Those are pairwise equal --
b_{n-k} = (2k-n)^2 = b_k -- so the multiset is a doubled copy of the half-set
beta = {(n-2k)^2 : k = 1..ceil(n/2)-1}, plus the single 0 when n is even.  Hence

    PROD_k (u - b_k) = [PROD_beta (u - b)]^2 * u^{[n even]},
    E_{2t}(n) = e_t(b) = SUM_i e_i(beta) e_{t-i}(beta).

Both follow in a line from the pairing, so this file is not evidence for them --
it is the machine check that the line is right, and the artefact the write-up
(results/DOUBLED_MULTISET.md) quotes its numbers from.

Run: python lab/doubled_multiset.py -> results/doubled_multiset.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpz_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def half_set(n: int) -> list[int]:
    return [(n - 2 * k) ** 2 for k in range(1, (n + 1) // 2)]


def e_of(vals: list[int], tmax: int) -> list[int]:
    e = [0] * (tmax + 1)
    e[0] = 1
    for a in vals:
        for t in range(min(tmax, len(vals)), 0, -1):
            e[t] += a * e[t - 1]
    return e


def main() -> int:
    t0 = time.time()
    pairing = []
    for n in (7, 8, 12, 13, 20, 41, 60):
        vals = [(n - 2 * k) ** 2 for k in range(1, n)]
        pairing.append(
            {
                "n": n,
                "doubled": all(vals[k - 1] == vals[n - k - 1] for k in range(1, n)),
                "distinct_values": len(set(vals)),
                "of": len(vals),
            }
        )

    squares = []
    for n in (7, 8, 12, 13, 20):
        p = fmpz_poly([1])
        for k in range(1, n):
            p = p * fmpz_poly([-((n - 2 * k) ** 2), 1])
        h = fmpz_poly([1])
        for b in half_set(n):
            h = h * fmpz_poly([-b, 1])
        pred = h * h * (fmpz_poly([0, 1]) if n % 2 == 0 else fmpz_poly([1]))
        squares.append({"n": n, "is_square_times_u": p == pred})

    conv_checks = conv_bad = 0
    for n in (7, 8, 9, 11, 12, 13, 20, 21, 40, 41):
        beta = half_set(n)
        tmax = n - 1
        E = E2_list(n, tmax)
        eb = e_of(beta, tmax)
        for t in range(tmax + 1):
            pred = sum(
                eb[i] * eb[t - i] for i in range(max(0, t - len(beta)), min(t, len(beta)) + 1)
            )
            conv_checks += 1
            conv_bad += E[t] != pred

    out = {
        "what": "b_k = (n-2k)^2 is a doubled multiset: pairing, square factorisation, "
        "and E_{2t} as the self-convolution of the half-set",
        "proof": "b_{n-k} = (2k-n)^2 = b_k -- one line; the rest follows, and is checked here",
        "pairing": pairing,
        "square_factorisation": squares,
        "self_convolution": {"checks": conv_checks, "mismatches": conv_bad},
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "doubled_multiset.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"pairing holds at {sum(p['doubled'] for p in pairing)}/{len(pairing)} n; "
        f"square factorisation {sum(s['is_square_times_u'] for s in squares)}/{len(squares)}; "
        f"self-convolution {conv_checks} checks, {conv_bad} mismatches"
    )
    for p in pairing:
        print(
            f"   n={p['n']:3d}: {p['distinct_values']} distinct of {p['of']}  (n/2 = {p['n'] / 2})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
