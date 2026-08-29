"""Does hypergeometric self-convolution preserve ratio log-concavity? A control test.

The AP-square brief reduces the physical conjecture (B) to a preservation question
(`AP_BRIEF_VERIFICATION.md`, their Sections 9 and 16): the physical `p_t` is

    p_t = SUM_i [C(m,i) C(m,t-i) / C(2m,t)] q_i q_{t-i},

`q` the normalized elementary means of the half spectrum, and their Problem 2 asks
for a proof that this preserves ratio log-concavity (RLC).

Before spending effort on that route, it is worth knowing whether the preservation
is TRUE IN GENERAL or only for this `q`. If a general RLC input can be mapped to a
non-RLC output, no general preservation theorem exists, and the route must use the
specific structure of the half spectrum -- which is exactly the kind of thing that
is cheap to learn now and expensive to learn after a week of work.

Two families of input, both exact:

  A. general RLC sequences, constructed rather than filtered. A positive `q` is RLC
     iff `r_t = q_t/q_{t-1}` is log-concave, so a DECREASING positive `d_t =
     r_t/r_{t-1}` gives one directly, and every RLC sequence arises this way.
  B. structured ones: normalized elementary means of random positive multisets,
     kept only when they happen to be RLC.

Family A is the real test; B is there because a failure only in A would leave open
whether real-rooted inputs behave better.

Deterministic: a fixed seed, recorded in the artefact, and every number exact.

Run: python lab/selfconv_preservation.py -> results/selfconv_preservation.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 20260829


def is_rlc(q: list[fmpq], top: int | None = None) -> list[int]:
    """Indices t where q_{t+1}^3 q_{t-1} >= q_t^3 q_{t+2} FAILS."""
    hi = len(q) - 3 if top is None else min(top, len(q) - 3)
    return [t for t in range(1, hi + 1) if q[t + 1] ** 3 * q[t - 1] < q[t] ** 3 * q[t + 2]]


def selfconv(q: list[fmpq], m: int) -> list[fmpq]:
    return [
        sum(
            fmpq(comb(m, i) * comb(m, t - i), comb(2 * m, t)) * q[i] * q[t - i]
            for i in range(max(0, t - m), min(m, t) + 1)
        )
        for t in range(2 * m + 1)
    ]


def esym(vals: list[fmpq]) -> list[fmpq]:
    acc = [fmpq(1)] + [fmpq(0)] * len(vals)
    for v in vals:
        for w in range(len(vals), 0, -1):
            acc[w] = acc[w] + acc[w - 1] * v
    return acc


def family_a(rng: random.Random, m: int) -> list[fmpq]:
    """A general RLC sequence: d decreasing -> r log-concave -> q ratio log-concave."""
    d = sorted((fmpq(rng.randint(1, 60), rng.randint(1, 60)) for _ in range(m)), reverse=True)
    r, q = [fmpq(1)], [fmpq(1)]
    for i in range(m):
        r.append(r[-1] * d[i])
        q.append(q[-1] * r[-1])
    return q


def family_b(rng: random.Random, m: int) -> list[fmpq]:
    x = [fmpq(rng.randint(1, 400), rng.randint(1, 20)) for _ in range(m)]
    e = esym(x)
    return [e[i] / fmpq(comb(m, i)) for i in range(m + 1)]


def main() -> int:
    t0 = time.time()
    rng = random.Random(SEED)
    out_rows = []
    for fam, gen in (("A_general_RLC", family_a), ("B_real_rooted", family_b)):
        tried = kept = broke = 0
        examples = []
        for m in range(4, 11):
            for _ in range(400):
                q = gen(rng, m)
                tried += 1
                if is_rlc(q):  # input must be RLC on its full range
                    continue
                kept += 1
                p = selfconv(q, m)
                fails = is_rlc(p, top=m)  # the half range the application needs
                if fails:
                    broke += 1
                    if len(examples) < 5:
                        examples.append({"m": m, "failing_t": fails,
                                         "q": [str(v) for v in q]})
        out_rows.append(
            {
                "family": fam,
                "generated": tried,
                "rlc_inputs": kept,
                "outputs_not_rlc": broke,
                "examples": examples,
            }
        )
        print(f"{fam:<15} RLC inputs {kept:>5} of {tried:>5}   "
              f"outputs failing RLC: {broke}")

    # (P) attacked where it is tightest.  Collect real-rooted RLC inputs with their
    # margins, then test the SMALLEST-margin quarter -- the cases nearest to breaking.
    pool = []
    for m in range(6, 19):
        for _ in range(300):
            q = family_b(rng, m)
            if is_rlc(q):
                continue
            marg = min(
                (q[t + 1] ** 3 * q[t - 1] - q[t] ** 3 * q[t + 2]) / (q[t] ** 3 * q[t + 2])
                for t in range(1, m - 1)
            )
            pool.append((marg, m, q))
    pool.sort(key=lambda r: r[0])
    tight = pool[: max(1, len(pool) // 4)]
    tight_bad = []
    for marg, m, q in tight:
        fails = is_rlc(selfconv(q, m), top=m)
        if fails:
            tight_bad.append({"m": m, "margin": str(marg), "failing_t": fails,
                              "q": [str(v) for v in q]})
    print(f"(P) attacked at m = 6..18: {len(pool)} real-rooted RLC inputs, tightest "
          f"{len(tight)} tested (margin {float(tight[0][0]):.2e} to "
          f"{float(tight[-1][0]):.2e}), {len(tight_bad)} failures")

    # and the structured one the application actually uses, for contrast
    phys = []
    for m in range(4, 25):
        g = esym([fmpq((2 * j - 1) ** 2) for j in range(1, m + 1)])
        q = [g[i] / fmpq(comb(m, i)) for i in range(m + 1)]
        phys.append({"m": m, "input_failures": is_rlc(q),
                     "output_failures": is_rlc(selfconv(q, m), top=m)})
    phys_bad = [r for r in phys if r["input_failures"] or r["output_failures"]]
    print(f"physical half spectrum, m = 4..24: {len(phys_bad)} failures")

    out = {
        "question": "does hypergeometric self-convolution preserve ratio log-concavity?",
        "why": "the AP-square brief reduces the physical (B) to exactly this preservation",
        "seed": SEED,
        "random_families": out_rows,
        "conjecture_P_attack": {
            "statement": "real-rooted RLC input -> self-convolution RLC on the first half",
            "pool": len(pool),
            "tightest_quarter_tested": len(tight),
            "margin_range_of_those": [str(tight[0][0]), str(tight[-1][0])],
            "failures": tight_bad[:10],
            "failure_count": len(tight_bad),
        },
        "physical_half_spectrum": phys,
        "physical_failures": phys_bad,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "selfconv_preservation.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
