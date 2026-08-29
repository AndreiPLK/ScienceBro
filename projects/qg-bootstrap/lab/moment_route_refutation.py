"""The moment route is dead: A_t = -Delta^2 log p_t has a negative Hankel minor.

The anomaly-map brief proposed, as its "potential jackpot", that the whole
log-difference hierarchy would follow from a positive-measure representation of

    A_t = -Delta^2 log p_t = log( p_{t+1}^2 / (p_t p_{t+2}) ).

Two facts settle it, one on paper and one by computation.

**On paper.** The hierarchy `Delta^r log p < 0` for all `r >= 2` says exactly that `A`
is ABSOLUTELY monotone (`Delta^k A >= 0` for all k), which is a moment sequence of a
measure on `[1, infinity)` -- not on `[0,1]`. So the brief's un-reversed Hausdorff
form was ruled out before any computation, and its own hedge about reversing the
index was compulsory rather than optional.

**By computation, and this kills both orientations.** Any positive-measure
representation forces every Hankel matrix of the sequence to be positive
semidefinite. It is not: the forward sequence has a negative 4x4 minor at every `n`
tested, and the reversed sequence has one too, at order 5 to 9 depending on `n`.

`A` is transcendental, so the determinants are computed by rationalising `A` to 300
digits and then evaluating EXACTLY over `Q` with flint -- an independent code path
from the floating-point version, and one that comes with a rigorous error bound.
Every decisive minor exceeds its bound by more than 200 orders of magnitude, so the
signs are facts, not numerical noise.

Consequence: whatever produces the hierarchy, it is not a positive measure on the
second log-difference. Total positivity, an LGV path model, or a determinant identity
remain; the moment route does not.

Run: python lab/moment_route_refutation.py -> results/moment_route_refutation.json
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_mat
from mpmath import log, mp, mpf

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from provenance import stamp  # noqa: E402
from sciencebro_math.families import centered_squares, normalized_means  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
DIGITS = 300
mp.dps = 400


def A_rationalised(n: int) -> list[fmpq]:
    """A_t on the first half, as exact rationals within 10^-DIGITS of the true value."""
    p = normalized_means(centered_squares(n))
    half = (n - 1) // 2
    scale = 10**DIGITS
    out = []
    for t in range(half):
        r = p[t + 1] ** 2 / (p[t] * p[t + 2])
        v = log(mpf(int(r.numer())) / int(r.denom()))
        out.append(fmpq(int(mp.floor(v * scale)), scale))
    return out


def hankel_signs(seq: list[fmpq]) -> tuple[str, int | None, dict]:
    signs, first_neg, detail = [], None, {}
    for order in range(1, len(seq) // 2 + 2):
        if 2 * order - 2 >= len(seq):
            break
        d = fmpq_mat([[seq[i + j] for j in range(order)] for i in range(order)]).det()
        s = "+" if d > 0 else ("-" if d < 0 else "0")
        signs.append(s)
        if s == "-" and first_neg is None:
            first_neg = order
            mx = max(abs(float(x)) for x in seq)
            err = math.factorial(order) * (mx ** (order - 1)) * (10.0**-DIGITS)
            detail = {
                "order": order,
                "abs_det": f"{abs(float(d)):.4e}",
                "error_bound": f"{err:.4e}",
                "orders_of_magnitude_above_bound": round(
                    math.log10(abs(float(d)) / err), 1
                ),
            }
    return "".join(signs), first_neg, detail


def main() -> int:
    t0 = time.time()
    rows = []
    for n in (21, 31, 41, 61, 81, 101):
        A = A_rationalised(n)
        fwd_s, fwd_n, fwd_d = hankel_signs(A)
        rev_s, rev_n, rev_d = hankel_signs(list(reversed(A)))
        rows.append(
            {
                "n": n,
                "terms": len(A),
                "forward_sign_pattern": fwd_s,
                "forward_first_negative_order": fwd_n,
                "forward_decisive_minor": fwd_d,
                "reversed_sign_pattern": rev_s,
                "reversed_first_negative_order": rev_n,
                "reversed_decisive_minor": rev_d,
            }
        )
        print(
            f"  n={n:<4} forward {fwd_s:<14} first neg {fwd_n}   |   "
            f"reversed {rev_s:<26} first neg {rev_n}"
        )

    both_dead = all(r["forward_first_negative_order"] and r["reversed_first_negative_order"]
                    for r in rows)
    out = {
        "what": "does A_t = -Delta^2 log p_t admit a positive-measure representation?",
        "answer": "NO, in either orientation",
        "why_it_matters": "this was the proposed single mechanism behind the whole "
        "log-difference hierarchy; it is now excluded, and the hierarchy needs another cause",
        "paper_argument": "the hierarchy says A is ABSOLUTELY monotone, i.e. a moment "
        "sequence on [1, infinity), so the un-reversed Hausdorff form on [0,1] was ruled out "
        "before computing; the reversal was compulsory, and it does not save the route either",
        "method": "A rationalised to 300 digits, determinants evaluated EXACTLY over Q with "
        "flint -- an independent code path from the floating-point version -- with a rigorous "
        "error bound on each decisive minor",
        "rows": rows,
        "positive_measure_excluded_in_both_orientations": both_dead,
        "evidence_kind": "EXACT_FINITE on a rationalised transcendental sequence, with an "
        "explicit error bound; this REFUTES a representation and never proves one",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "moment_route_refutation.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\npositive measure excluded in both orientations: {both_dead}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
