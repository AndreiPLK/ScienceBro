"""The depth cutoff of the Hausdorff regime, mapped past the sample that defined it.

WHY.  results/asymptotic_regime_probe.json records the law "largest good
j == n/2 + 1" with matches_law true in every row, and
results/BFORM_POSITIVITY_THEOREM.md sec. 6 quotes it as an EXACT depth cutoff.
Every row of that measurement has EVEN n, from 12 to 44.  Two hypotheses,
n/2 + 1 and (n+3)/2, agree on even n, so that grid could not tell them apart --
and odd n was never computed.

This file computes the same predicate (`completely_monotone`, exact Hankel minors
via hankel_report -- no floating point anywhere) over n = 11..61 including every
odd n, and reports where the recorded law holds and where it does not.

Run: python lab/depth_boundary_map.py -> results/depth_boundary_map.json
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

from flint import fmpq

sys.set_int_max_str_digits(2_000_000)  # hankel_report stringifies exact minors; they get long

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asymptotic_regime_probe import completely_monotone  # noqa: E402
from moment_kernel_probe import shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def largest_odd_le(x: float) -> int:
    k = math.floor(x)
    return k if k % 2 == 1 else k - 1


def largest_good_j(n: int, lam: fmpq) -> int | None:
    Th = shore(lam)[0]
    best = None
    for j in range(3, n):
        if completely_monotone(n, j, lam, Th):
            best = j
        else:
            break
    return best


def main() -> int:
    t0 = time.time()
    lam = fmpq(10**4)
    n_max = int(os.environ.get("N_MAX", "140"))
    fit_upto = 61  # everything above is a HELD-OUT sample for the candidate law
    rows = []
    for n in range(11, n_max + 1):
        best = largest_good_j(n, lam)
        rows.append(
            {
                "n": n,
                "largest_good_j": best,
                "law_n_over_2_plus_1": n // 2 + 1,
                "matches_recorded_law": best == n // 2 + 1,
                "offset_from_half_n": (best - n / 2) if best is not None else None,
                "parity": "even" if n % 2 == 0 else "odd",
                "candidate_4n_plus_32_over_9": largest_odd_le((4 * n + 32) / 9),
                "sample": "fit" if n <= fit_upto else "held-out",
            }
        )
    bad = [r for r in rows if not r["matches_recorded_law"]]
    # stability of the two headline counterexamples across lam
    stability = []
    for n in (31, 47):
        stability.append(
            {
                "n": n,
                "law": n // 2 + 1,
                "largest_good_j_by_lam": {
                    f"1e{e}": largest_good_j(n, fmpq(10**e)) for e in (3, 4, 5, 6)
                },
            }
        )
    cand = {"fit": [0, 0], "held-out": [0, 0]}
    for r in rows:
        slot = cand[r["sample"]]
        slot[1] += 1
        slot[0] += r["largest_good_j"] == r["candidate_4n_plus_32_over_9"]
    out = {
        "what": "largest j for which the Hausdorff moment conditions hold, over n = 11..61",
        "reading": "the recorded law j <= n/2+1 was fitted on even n from 12 to 44; outside that "
        "sample it fails in BOTH directions",
        "lam": "1e4",
        "rows": rows,
        "mismatches": len(bad),
        "mismatching_n": [(r["n"], r["largest_good_j"], r["law_n_over_2_plus_1"]) for r in bad],
        "candidate_law": {
            "form": "largest odd j <= (4n+32)/9",
            "fitted_on": "n = 11..61",
            "hits_on_fit_sample": cand["fit"],
            "hits_on_held_out_sample": cand["held-out"],
        },
        "stability_of_counterexamples": stability,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "depth_boundary_map.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"rows {len(rows)}, mismatches with the recorded law: {len(bad)}")
    print("mismatching (n, measured, law):", out["mismatching_n"][:12])
    print(
        f"candidate 'largest odd <= (4n+32)/9': fit {cand['fit'][0]}/{cand['fit'][1]}, "
        f"HELD-OUT {cand['held-out'][0]}/{cand['held-out'][1]}"
    )
    for st in stability:
        print(f"   n={st['n']}: {st['largest_good_j_by_lam']}  (law says {st['law']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
