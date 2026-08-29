"""Machine-check of the AP-square ratio-log-concavity brief from the parallel chat.

The brief (Downloads/AP_Squared_Ratio_Log_Concavity_Research_Brief.pdf) proposes a
corrected form of conjecture (B) for a general squared arithmetic progression, and
several exact structural identities. Everything here is checked before any of it is
used, per the lab rule that another chat's answer is untrusted input.

Checked, all exactly over fmpq:

  C1  their counterexample N=3, t=1, alpha=-1/2:  p_2^3 p_0 - p_1^3 p_3 = -5/108
  C2  their second failure, N=4, t=2, centered (-3/2,-1/2,1/2,3/2)
  C3  CONJECTURE 1 itself -- N >= 5, 1 <= t <= floor(N/2), every real AP -- attacked
      on a dense exact grid of the centered parameter c, both regimes
  C4  the shift identity (13)/(14): (1+a^2 z) F_N(z;a+1) = (1+(a+N)^2 z) F_N(z;a)
  C5  the centered factorisations (7) and (8) against our own b-multiset
  C6  the hypergeometric self-convolution (9): p_t = E[q_I q_{t-I}]

(B) is scale-invariant: replacing b by lambda b multiplies both sides by
lambda^{4t+2}, so only alpha = a/d matters, and the search runs over alpha alone.
By their own c -> -c symmetry only c >= 0 needs testing, and that is asserted here
rather than assumed: C3 tests the symmetry too.

Run: python lab/ap_square_brief_check.py -> results/ap_square_brief_check.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def esym(vals: list[fmpq]) -> list[fmpq]:
    acc = [fmpq(1)] + [fmpq(0)] * len(vals)
    for v in vals:
        for q in range(len(vals), 0, -1):
            acc[q] = acc[q] + acc[q - 1] * v
    return acc


def p_list(alpha: fmpq, N: int) -> list[fmpq]:
    e = esym([(alpha + k) ** 2 for k in range(N)])
    return [e[t] / fmpq(comb(N, t)) for t in range(N + 1)]


def H(p: list[fmpq], t: int) -> fmpq:
    """p_{t+1}^3 p_{t-1} - p_t^3 p_{t+2}; (B) is H >= 0."""
    return p[t + 1] ** 3 * p[t - 1] - p[t] ** 3 * p[t + 2]


def c_grid(N: int) -> list[fmpq]:
    """Centered parameter c = alpha + (N-1)/2, both regimes, denominators to 6."""
    h = fmpq(N - 1, 2)
    out = {fmpq(0), h, h + 1, 2 * h + 1, 5 * h + 1, 20 * h + 1}
    for q in (1, 2, 3, 4, 6):
        k = 0
        while fmpq(k, q) <= h + 2:
            out.add(fmpq(k, q))
            k += 1
    return sorted(out)


def main() -> int:
    t0 = time.time()
    res: dict = {}

    # C1
    p = p_list(fmpq(-1, 2), 3)
    res["C1"] = {
        "p": [str(x) for x in p],
        "H_at_t1": str(H(p, 1)),
        "brief_says": "-5/108",
        "matches": H(p, 1) == fmpq(-5, 108),
    }
    print(f"C1 counterexample N=3,t=1: H = {H(p, 1)}   matches brief: {res['C1']['matches']}")

    # C2  centered (-3/2,-1/2,1/2,3/2) is alpha = -3/2, N = 4
    p = p_list(fmpq(-3, 2), 4)
    res["C2"] = {"H_at_t2": str(H(p, 2)), "is_a_failure": H(p, 2) < 0}
    print(f"C2 N=4,t=2 centered:      H = {H(p, 2)}   a failure: {res['C2']['is_a_failure']}")

    # C3  attack Conjecture 1
    bad, tested, sym_bad = [], 0, 0
    for N in range(5, 27):
        half = N // 2
        for c in c_grid(N):
            alpha = c - fmpq(N - 1, 2)
            pl = p_list(alpha, N)
            plm = p_list(-c - fmpq(N - 1, 2), N)  # the c -> -c reflection
            for t in range(1, half + 1):
                if t + 2 > N:
                    continue
                tested += 1
                if H(pl, t) < 0:
                    bad.append({"N": N, "t": t, "c": str(c), "alpha": str(alpha),
                                "H": str(H(pl, t))})
                if H(pl, t) != H(plm, t):
                    sym_bad += 1
    res["C3"] = {
        "statement": "Conjecture 1: N >= 5, 1 <= t <= floor(N/2), every real AP",
        "cases_tested": tested,
        "counterexamples": bad[:20],
        "counterexample_count": len(bad),
        "reflection_c_to_minus_c_mismatches": sym_bad,
    }
    print(f"C3 Conjecture 1: {tested} exact cases, {len(bad)} counterexamples, "
          f"{sym_bad} reflection mismatches")

    # C4  shift identity (13)
    z = fmpq_poly([0, 1])

    def Fpoly(al: fmpq, N: int) -> fmpq_poly:
        out = fmpq_poly([1])
        for k in range(N):
            out = out * (fmpq_poly([1]) + z * ((al + k) ** 2))
        return out

    mism = 0
    for N in range(1, 9):
        for a in (fmpq(0), fmpq(1, 2), fmpq(3), fmpq(-5, 3), fmpq(7, 4)):
            lhs = (fmpq_poly([1]) + z * (a**2)) * Fpoly(a + 1, N)
            rhs = (fmpq_poly([1]) + z * ((a + N) ** 2)) * Fpoly(a, N)
            if lhs != rhs:
                mism += 1
    res["C4"] = {"identity": "(1+a^2 z)F_N(z;a+1) = (1+(a+N)^2 z)F_N(z;a)", "mismatches": mism}
    print(f"C4 shift identity: {mism} mismatches")

    # C5  the centered factorisations, against our own multiset
    fac_bad = []
    for n in range(4, 31):
        ours = sorted((n - 2 * k) ** 2 for k in range(1, n))
        if n % 2:
            m = (n - 1) // 2
            theirs = sorted([(2 * j - 1) ** 2 for j in range(1, m + 1)] * 2)
        else:
            m = n // 2
            theirs = sorted([0] + [(2 * j) ** 2 for j in range(1, m)] * 2)
        if ours != theirs:
            fac_bad.append(n)
    res["C5"] = {"formulas": "(7) n=2m+1 and (8) n=2m", "mismatched_n": fac_bad}
    print(f"C5 centered factorisations (7),(8): {len(fac_bad)} mismatches over n = 4..30")

    # C6  hypergeometric self-convolution, at the physical centered point
    conv_bad = 0
    for m in range(2, 13):
        n = 2 * m + 1
        g = esym([fmpq((2 * j - 1) ** 2) for j in range(1, m + 1)])
        q = [g[i] / fmpq(comb(m, i)) for i in range(m + 1)]
        e = esym([fmpq((n - 2 * k) ** 2) for k in range(1, n)])
        for t in range(0, 2 * m + 1):
            direct = e[t] / fmpq(comb(2 * m, t))
            conv = sum(
                (fmpq(comb(m, i) * comb(m, t - i), comb(2 * m, t)) * q[i] * q[t - i])
                for i in range(max(0, t - m), min(m, t) + 1)
            )
            if direct != conv:
                conv_bad += 1
    res["C6"] = {"formula": "(9) p_t = sum C(m,i)C(m,t-i)/C(2m,t) q_i q_{t-i}",
                 "mismatches": conv_bad}
    print(f"C6 hypergeometric self-convolution: {conv_bad} mismatches")

    # C7  is the HALF spectrum itself ratio log-concave?  That is the natural input to
    # any induction through their self-convolution (9), and it is itself an instance of
    # their Conjecture 1 (odd numbers are the AP a=1, d=2).
    half_bad, half_tested = [], 0
    for m in range(5, 41):
        g = esym([fmpq((2 * j - 1) ** 2) for j in range(1, m + 1)])
        q = [g[i] / fmpq(comb(m, i)) for i in range(m + 1)]
        for t in range(1, m - 1):
            half_tested += 1
            if q[t + 1] ** 3 * q[t - 1] < q[t] ** 3 * q[t + 2]:
                half_bad.append({"m": m, "t": t})
    res["C7"] = {
        "question": "is the half spectrum {(2j-1)^2} ratio log-concave over its full index range?",
        "why": "it is the induction input for the self-convolution (9), and an instance of "
        "their Conjecture 1",
        "tested": half_tested,
        "failures": half_bad[:20],
        "failure_count": len(half_bad),
    }
    print(f"C7 half spectrum RLC: {half_tested} cases, {len(half_bad)} failures")

    out = {
        "what": "machine-check of the AP-square brief before any of it is used",
        "source": "AP_Squared_Ratio_Log_Concavity_Research_Brief.pdf (parallel chat, untrusted)",
        "checks": res,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "ap_square_brief_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
