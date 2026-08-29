"""The elementary half of the J-uniform chain: the identity, and the proved bound.

results/FARBELOW_NEGATIVE_PATTERN.md reduces a J-uniform (R) to two statements.
The second one is elementary and now PROVED:

    LEMMA.  For integers J >= 4, n >= 6, M = n - J >= 2,
        (J-1)(n-J+2)/[(J-2)(n-J+1)] * (1 + 2/n)
             <= 2(2n-2J+3)(2n-2J+4)/[(2n-2J+1)(2n-2J+2)].

    PROOF.  Both sides carry the factor (M+2)/(M+1): the left is
    [(J-1)/(J-2)][(M+2)/(M+1)](1 + 2/n), the right is
    2(2M+3)(M+2)/[(2M+1)(M+1)].  Cancelling it leaves
        (J-1)/(J-2) * (1 + 2/n)  <=  2(2M+3)/(2M+1).
    The right side exceeds 2.  On the left, (J-1)/(J-2) <= 3/2 for J >= 4 and
    1 + 2/n <= 4/3 for n >= 6, so the product is at most 2.  QED

This file is not the evidence -- the proof above is -- but a proof written by hand
deserves a machine check of the step it turns on.  Two things are verified: the
CANCELLATION is an exact identity, and the bound holds where the lemma claims it,
including the extreme corners.

Run: python lab/elementary_half_check.py -> results/elementary_half_check.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def sides(n: int, J: int) -> tuple[fmpq, fmpq, fmpq, fmpq]:
    M = n - J
    lhs = fmpq((J - 1) * (n - J + 2), (J - 2) * (n - J + 1)) * (1 + fmpq(2, n))
    rhs = fmpq(
        2 * (2 * n - 2 * J + 3) * (2 * n - 2 * J + 4), (2 * n - 2 * J + 1) * (2 * n - 2 * J + 2)
    )
    lhs_red = fmpq(J - 1, J - 2) * (1 + fmpq(2, n))
    rhs_red = fmpq(2 * (2 * M + 3), 2 * M + 1)
    return lhs, rhs, lhs_red, rhs_red


def main() -> int:
    t0 = time.time()
    ident = failures = pairs = 0
    worst = None
    for n in range(6, 401):
        for J in range(4, n - 1):
            M = n - J
            if M < 2:
                continue
            lhs, rhs, lhs_red, rhs_red = sides(n, J)
            pairs += 1
            f = fmpq(M + 2, M + 1)
            if lhs != lhs_red * f or rhs != rhs_red * f:
                ident += 1
            if lhs > rhs:
                failures += 1
            slack = float(rhs / lhs)
            if worst is None or slack < worst[0]:
                worst = (slack, n, J)
    out = {
        "lemma": "(J-1)(n-J+2)/[(J-2)(n-J+1)] (1+2/n) <= 2(2n-2J+3)(2n-2J+4)/[(2n-2J+1)(2n-2J+2)] "
        "for J >= 4, n >= 6",
        "status": "PROVED by hand; this file checks the cancellation step and the range",
        "pairs_checked": pairs,
        "cancellation_identity_mismatches": ident,
        "inequality_failures": failures,
        "tightest_slack": {"slack": worst[0], "n": worst[1], "J": worst[2]},
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "elementary_half_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"{pairs} pairs: cancellation mismatches {ident}, inequality failures {failures}, "
        f"tightest slack {worst[0]:.4f} at n={worst[1]}, J={worst[2]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
