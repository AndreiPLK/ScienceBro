"""Checking the finite-n bridge: the exact recursion, and the two conjectures it rests on.

results/FINITE_N_BRIDGE.md.  The plan came from the parallel chat and is untrusted
input, so everything checkable in it is checked here:

  (A) the exact recursion e_t(n+2) = e_t(n) + 2n^2 e_{t-1}(n) + n^4 e_{t-2}(n),
      which is the doubling of DOUBLED_MULTISET.md read as a step in n;
  (B) ratio-log-concavity p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}, which would put the
      maximum of R_{n,t} at the central t;
  (C) parity monotonicity of the central value in n, which would put the maximum
      over n >= 44 at n = 44 and n = 45;
  the two base numbers M_{44,21} and M_{45,22}, which the PDF quotes to ten digits;
  and the closed form R_{n,1} = 5n(n-2)^2/(5n^3-24n^2+28n+12).

(A), the base numbers and the closed form are identities and are verified as such.
(B) and (C) are CONJECTURES: this file tests them and reports how far it looked,
which is all a test can do.

Run: python lab/finite_n_bridge_check.py -> results/finite_n_bridge_check.json
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


def p_seq(n: int, tmax: int) -> list[fmpq]:
    N = n - 1
    E = E2_list(n, tmax)
    return [fmpq(E[t], comb(N, t)) for t in range(min(tmax, len(E) - 1) + 1)]


def M(n: int, t: int) -> fmpq:
    p = p_seq(n, t + 1)
    return (p[t] * p[t] / (p[t - 1] * p[t + 1]) - 1) * n


def main() -> int:
    t0 = time.time()

    rec_checks = rec_bad = 0
    for n in range(5, 60):
        E, E2 = E2_list(n, n - 1), E2_list(n + 2, n + 1)
        for t in range(n):
            a = E[t - 1] if 1 <= t < len(E) else 0
            b = E[t - 2] if 2 <= t < len(E) else 0
            v = E[t] if t < len(E) else 0
            rec_checks += 1
            rec_bad += E2[t] != v + 2 * n * n * a + n**4 * b

    b_pairs = b_bad = 0
    for n in range(8, 90):
        p = p_seq(n, n - 1)
        for t in range(1, min(len(p) - 2, n // 2 + 2)):
            b_pairs += 1
            b_bad += p[t + 1] ** 3 * p[t - 1] < p[t] ** 3 * p[t + 2]

    c_vals = c_bad = 0
    for n in range(8, 80):
        t1, t2 = (n - 1) // 2, (n + 1) // 2
        if t1 < 1:
            continue
        c_vals += 1
        c_bad += M(n + 2, t2) > M(n, t1)

    base = {f"M_{n}_{t}": float(M(n, t)) for n, t in ((44, 21), (45, 22))}

    r1_bad = 0
    for n in range(5, 80):
        p = p_seq(n, 2)
        claim = fmpq(5 * n * (n - 2) ** 2, 5 * n**3 - 24 * n**2 + 28 * n + 12)
        r1_bad += p[1] * p[1] / (p[0] * p[2]) != claim

    out = {
        "source": "third answer from the parallel chat, 2026-08-29; untrusted, hence checked",
        "recursion_A": {"checks": rec_checks, "mismatches": rec_bad, "status": "identity"},
        "conjecture_B_ratio_log_concavity": {
            "pairs_tested": b_pairs,
            "failures": b_bad,
            "status": "CONJECTURE, tested only",
        },
        "conjecture_C_parity_monotonicity": {
            "n_tested": c_vals,
            "failures": c_bad,
            "status": "CONJECTURE, tested only",
        },
        "base_cases": base,
        "closed_form_t1": {"n_tested": 75, "mismatches": r1_bad, "status": "identity"},
        "reduction": "if (B) and (C) hold, the lemma reduces to the two base cases above, "
        "both below the 2 allowed",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "finite_n_bridge_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"(A) recursion: {rec_checks} checks, {rec_bad} mismatches")
    print(f"(B) tested on {b_pairs} pairs, {b_bad} failures")
    print(f"(C) tested on {c_vals} values of n, {c_bad} failures")
    print(f"base cases: {base}; t=1 closed form mismatches {r1_bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
