"""Is (B) one member of a hierarchy of higher-difference signs? And can that hierarchy
come from a Hausdorff moment sequence, as the anomaly-map brief proposes?

The brief (Downloads/Central_Factorial_Anomaly_Map.pdf, section 2) makes two claims:

  H1  `Delta^r log p_t < 0` for EVERY r >= 2 on the admissible first-half domain,
      so (B) -- which is exactly `Delta^3 log p_{t-1} <= 0` -- is the first
      nontrivial member of an infinite hierarchy;
  H2  the "potential jackpot": if `A_t = -Delta^2 log p_t` is a Hausdorff moment
      sequence, `A_t = integral_0^1 x^t dmu(x)` with `mu >= 0`, the whole hierarchy
      follows from one positive-measure representation.

**H2, taken literally, is inconsistent with (B) -- and that makes their own hedge
compulsory.** (B) says `A_t` is INCREASING: with `R_t = p_t^2/(p_{t-1} p_{t+1})` one
has `R_{t+1}/R_t = p_{t+1}^3 p_{t-1} / (p_t^3 p_{t+2})`, so (B) is exactly
`R_{t+1} >= R_t`, i.e. `A_t = log R_{t+1}` increasing. But a Hausdorff sequence
`A_t = int_0^1 x^t dmu` with `mu >= 0` is DECREASING, since `Delta A_t =
int x^t (x-1) dmu <= 0`. So the representation cannot hold for `A_t` as written.

The brief hedges with "or becomes one after reversing the index from the center",
and that hedge is not optional -- it is forced. Only the reversed sequence can carry
a positive-measure representation, and any attempt at this route must start from the
reversal.

H1 itself is a sign statement about exact rationals and is tested exactly here.
`Delta^r log p_t = SUM_j (-1)^{r-j} C(r,j) log p_{t+j}` is negative exactly when

    PROD_{j odd} p_{t+j}^{C(r,j)}   >   PROD_{j even} p_{t+j}^{C(r,j)}    (r odd)

and the other way for even r, so no logarithm is ever taken: the comparison is
between two integers. No float touches a sign.

Run: python lab/higher_difference_hierarchy.py -> results/higher_difference_hierarchy.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def p_list(n: int, upto: int) -> list[fmpq]:
    N = n - 1
    E = E2_list(n, upto)
    return [fmpq(E[t], comb(N, t)) for t in range(upto + 1)]


def sign_of_difference(p: list[fmpq], t: int, r: int) -> int:
    """Sign of Delta^r log p_t, computed by comparing two exact products."""
    lhs = fmpq(1)  # even j
    rhs = fmpq(1)  # odd j
    for j in range(r + 1):
        c = comb(r, j)
        if (r - j) % 2 == 0:
            lhs = lhs * p[t + j] ** c
        else:
            rhs = rhs * p[t + j] ** c
    if lhs == rhs:
        return 0
    return 1 if lhs > rhs else -1


def main() -> int:
    t0 = time.time()
    # Two readings of "the admissible first-half domain", because the first run used
    # the loose one and its 19 violations ALL had t + r running into the end of the
    # spectrum -- where, for even n, the multiset contains a zero and p_N = 0. A window
    # that leaves the first half is outside the claim, not a counterexample to it.
    RMAX = 8
    readings = {
        "window_inside_first_half": lambda t, r, N: t >= 1 and t + r <= N // 2,
        "index_in_first_half_window_free": lambda t, r, N: t >= 1 and t + r <= N - 1,
    }
    rows: list[dict] = []
    viol: dict[str, list] = {k: [] for k in readings}
    for n in range(9, 33):
        N = n - 1
        p = p_list(n, N)
        for r in range(2, RMAX + 1):
            for t in range(1, N):
                if t + r > N or (n % 2 == 0 and t + r >= N):
                    continue
                s = None
                for name, ok in readings.items():
                    if not ok(t, r, N):
                        continue
                    if s is None:
                        s = sign_of_difference(p, t, r)
                        rows.append({"n": n, "t": t, "r": r, "sign": s,
                                     "reading": name})
                    if s >= 0:
                        viol[name].append({"n": n, "t": t, "r": r, "sign": s})

    by_r: dict[int, dict[str, int]] = {}
    for row in rows:
        d = by_r.setdefault(row["r"], {"tested": 0, "negative": 0, "nonnegative": 0})
        d["tested"] += 1
        d["negative" if row["sign"] < 0 else "nonnegative"] += 1
    for r in sorted(by_r):
        d = by_r[r]
        print(f"  r={r}: {d['tested']:>5} cases, negative {d['negative']:>5}, "
              f"NOT negative {d['nonnegative']:>5}")
    for name, vs in viol.items():
        print(f"  reading '{name}': {len(vs)} violations")

    out = {
        "what": "H1 of the anomaly-map brief: is Delta^r log p_t < 0 for every r >= 2 on the "
        "first-half domain?",
        "method": "exact: the sign is decided by comparing two products of rationals; no "
        "logarithm and no float is used",
        "range": "n = 9..32, r = 2..8, t = 1..floor((n-1)/2)",
        "by_order": by_r,
        "violations_by_reading": {k: v[:40] for k, v in viol.items()},
        "violation_counts": {k: len(v) for k, v in viol.items()},
        "H1_holds_with_window_inside_first_half": not viol["window_inside_first_half"],
        "H2_verdict": "(B) says A_t = -Delta^2 log p_t is INCREASING, while a Hausdorff "
        "sequence int_0^1 x^t dmu with mu >= 0 is decreasing. So the representation cannot "
        "hold for A_t as written; the brief's own hedge -- reversing the index from the "
        "centre -- is not optional but forced, and any attempt at this route must start "
        "there. Argued on paper, no computation needed.",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "higher_difference_hierarchy.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    ok = not viol["window_inside_first_half"]
    print(f"H1 with the window inside the first half: {'HOLDS' if ok else 'FAILS'} "
          f"({out['runtime_s']}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
