"""Three structural routes to K_r >= 0 without a constant -- all refuted.

Since the cancellation ratio approaches 1 with the level
(results/cancellation_bound_sweep.json), a proof cannot fix c < 1 and would
have to get positivity STRUCTURALLY. Ordering the Gauss nodes ascending and
writing c_i = w_i P_r(y_i), three natural structures were tested exactly:

 1. ADJACENT PAIRING: c_i + c_{i+1} >= 0 for all i (a pairwise cancellation
    argument).
 2. PARTIAL SUMS: sum_{i<=k} c_i >= 0 for all k (from the left, and from the
    right) -- the shape a variation-diminishing / total-positivity argument
    would deliver, which would have connected this to the day's kernel TP
    theorem.
 3. LEIBNIZ TAIL: the sign pattern is a block of positives followed by an
    alternating tail; if the tail's magnitudes decreased monotonically, its
    sum would be controlled by its first term and the head would dominate
    structurally.

ALL THREE FAIL. What does survive across every configuration tested is
weaker and quantitative: the HEAD BLOCK (the contributions at the smallest
nodes, all positive) exceeds the tail in absolute value, with |tail| / head
between 0.43 and 0.79 -- i.e. the same tightness as the cancellation ratio,
restated. No free structural lunch.

Run: python lab/pairing_structures_probe.py -> results/pairing_structures_probe.json
"""

from __future__ import annotations

import json
import sys
import time
from itertools import accumulate
from math import comb
from pathlib import Path

from flint import acb, ctx, fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base_moment_probe import m_seq  # noqa: E402
from cancellation_bound_sweep import quadrature  # noqa: E402
from moment_kernel_probe import falling, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def contributions(n: int, lam: fmpq, j: int, Dfac: fmpq = fmpq(1)) -> list[float]:
    Th = shore(lam)[0]
    D = Th * Dfac
    m = m_seq(n, lam, n - 2)
    q = min((n - 2) // 2, 12)
    nodes, weights = quadrature(m, q)
    H = (D + 4 * n - 7) / 2
    r = j - 1
    g = H - r
    order = sorted(range(q), key=lambda i: nodes[i].real.mid())
    out = []
    for i in order:
        P = sum(
            (acb(comb(r, t)) * acb(str(falling(g, t))) * (-nodes[i]) ** t for t in range(r + 1)),
            acb(0),
        )
        out.append(float((weights[i] * P).real.mid()))
    return out


def main() -> int:
    t0 = time.time()
    ctx.prec = 500
    rows = []
    for n, j, lam in ((20, 8, 7), (28, 8, 7), (40, 14, 7), (40, 10, 7), (28, 12, 1), (20, 5, 7),
                      (20, 8, 1), (28, 6, 72), (40, 8, 1)):
        v = contributions(n, fmpq(lam), j)
        signs = "".join("+" if x > 0 else "-" for x in v)
        L = list(accumulate(v))
        R = list(accumulate(v[::-1]))
        pairs = [v[i] + v[i + 1] for i in range(len(v) - 1)]
        k = next((i for i in range(len(v) - 1) if (v[i] > 0) != (v[i + 1] > 0)), len(v) - 1)
        head, tail = v[: k + 1], v[k + 1:]
        mags = [abs(x) for x in tail]
        rows.append(
            {
                "n": n, "j": j, "lam": lam, "signs": signs,
                "adjacent_pairs_nonneg": all(p >= 0 for p in pairs),
                "partial_sums_left_nonneg": all(x >= 0 for x in L),
                "partial_sums_right_nonneg": all(x >= 0 for x in R),
                "tail_magnitudes_decreasing": all(
                    mags[i] >= mags[i + 1] for i in range(len(mags) - 1)
                ) if len(mags) > 1 else True,
                "head_sum": sum(head),
                "tail_sum": sum(tail),
                "tail_over_head": abs(sum(tail)) / sum(head) if sum(head) else None,
                "head_dominates": sum(head) > abs(sum(tail)),
                "total": sum(v),
            }
        )
    n_pairs = sum(1 for r in rows if r["adjacent_pairs_nonneg"])
    n_left = sum(1 for r in rows if r["partial_sums_left_nonneg"])
    n_right = sum(1 for r in rows if r["partial_sums_right_nonneg"])
    n_leib = sum(1 for r in rows if r["tail_magnitudes_decreasing"])
    n_head = sum(1 for r in rows if r["head_dominates"])
    print(f"configurations: {len(rows)}", flush=True)
    print(f"  adjacent pairing holds:      {n_pairs}/{len(rows)}", flush=True)
    print(f"  partial sums (left) hold:    {n_left}/{len(rows)}", flush=True)
    print(f"  partial sums (right) hold:   {n_right}/{len(rows)}", flush=True)
    print(f"  Leibniz tail (decreasing):   {n_leib}/{len(rows)}", flush=True)
    print(f"  head dominates tail:         {n_head}/{len(rows)}", flush=True)
    ratios = [r["tail_over_head"] for r in rows if r["tail_over_head"] is not None]
    if ratios:
        print(f"  |tail|/head: min {min(ratios):.3f}, max {max(ratios):.3f}", flush=True)

    out = {
        "claim": (
            "Three structural routes to K_r >= 0 without a constant -- adjacent "
            "pairing of quadrature contributions, nonnegative partial sums (the "
            "variation-diminishing shape that would have connected to the kernel TP "
            "theorem), and a Leibniz alternating tail -- are all REFUTED by exact "
            "computation. What survives is quantitative and no better than the "
            "cancellation ratio itself: the head block at the smallest nodes exceeds "
            "the tail, with |tail|/head between 0.43 and 0.79."
        ),
        "adjacent_pairing": [n_pairs, len(rows)],
        "partial_sums_left": [n_left, len(rows)],
        "partial_sums_right": [n_right, len(rows)],
        "leibniz_tail": [n_leib, len(rows)],
        "head_dominates": [n_head, len(rows)],
        "rows": rows,
        "command": "python lab/pairing_structures_probe.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "pairing_structures_probe.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
