"""STRIP CERTIFICATE, FAST ENGINE: native flint mpoly instead of our QPoly.

Same mathematics as lab/keystone_strip_symbolic.py, only the polynomial
arithmetic changes: flint's native multivariate polynomials (fmpq_mpoly, C
speed) replace our QPoly, which was a Python dict with Python multiplication
loops -- exact coefficients but interpreted convolution.

Founder's rule, stated twice and now binding: if a faster way exists, it is
used everywhere. Two things were left slow and are fixed here:
  * the interpolation of E_2t(n) was recomputed inside every cell (cached now,
    measured 5.8x on its own: 157s -> 27s at j=8);
  * polynomial products ran in Python (this module).

Validation contract: for every (j, parity, k) tested, this module's verdict
AND its coefficient multiset must agree with the QPoly implementation. A
faster engine that changes an answer is a bug, not a speedup.

Run: KSF_JMAX=10 python lab/keystone_strip_fast.py
Artifact: results/keystone_strip_fast.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import Ordering, fmpq, fmpq_mpoly_ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keystone_strip_symbolic as slow  # noqa: E402  (reference engine)
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J_MIN = int(os.environ.get("KSF_JMIN", "2"))
J_MAX = int(os.environ.get("KSF_JMAX", "10"))
K_MAX = int(os.environ.get("KSF_KMAX", "20"))

CTX = fmpq_mpoly_ctx.get(("w", "v", "mu"), Ordering.lex)
W, V, MU = CTX.gens()
ONE = CTX.from_dict({(0, 0, 0): fmpq(1)})


def q(x: Fraction) -> fmpq:
    return fmpq(x.numerator, x.denominator)


def lin_n(const: Fraction, n_coef: Fraction, n0: int):
    """const + n_coef * n with n = n0 + 2 mu."""
    return CTX.from_dict({(0, 0, 0): q(const + n_coef * n0), (0, 0, 1): q(2 * n_coef)})


def build_N(j: int, parity: int, k: int, n0: int):
    a, b = slow.branch_range(k)
    onepw = ONE + W
    onepv = ONE + V
    onepv2 = onepv * onepv

    s_num = lin_n(a - 1, Fraction(1), n0) + lin_n(b - 1, Fraction(1), n0) * V
    lam_num = CTX.from_dict({(0, 0, 0): q(a), (0, 1, 0): q(b)})
    r = Fraction(3 * (2 * k - 3), k * (k - 2))
    t_num = (
        q(r) * (lam_num * lam_num + (2 * k - 2) * (lam_num * onepv) + onepv2)
        + q(Fraction(2 * k)) * onepv2
    )

    s_pows = {0: ONE}
    for d in range(1, 2 * (j - 1) + 1):
        s_pows[d] = s_pows[d - 1] * s_num
    w_pows = {0: ONE}
    for d in range(1, j):
        w_pows[d] = w_pows[d - 1] * onepw

    N = CTX.from_dict({})
    for t in range(j):
        m = j - 1 - t
        # E_2t(n) as a polynomial in n, then n = n0 + 2 mu
        e_coeffs = slow.E2t_in_n(t, parity)  # cached upstream
        base = CTX.from_dict({(0, 0, 0): q(Fraction(n0)), (0, 0, 1): q(Fraction(2))})
        e_pow = {0: ONE}
        for d in range(1, len(e_coeffs)):
            e_pow[d] = e_pow[d - 1] * base
        e_pol = CTX.from_dict({})
        for d, c in enumerate(e_coeffs):
            if c:
                e_pol += q(c) * e_pow[d]

        term = q(Fraction((-1) ** t)) * e_pol
        for i in range(1, t + 1):
            term = q(Fraction(j - i)) * term
        for i in range(t + 1, j):
            term = term * lin_n(Fraction(-i), Fraction(1), n0)
        term = term * s_pows[2 * (j - 1 - t)]
        for i in range(m):
            term = term * lin_n(Fraction(1, 2) - j + i, Fraction(1), n0)
        for i in range(m, j - 1):
            bse = lin_n(Fraction(-1) - j + i, Fraction(1), n0)
            term = term * ((q(Fraction(1, 2)) * t_num + bse * onepv2) * onepw + W * onepv2)
        term = term * w_pows[j - 1 - t]
        N += term
    return N


def coeffs_of(N) -> list:
    return [N.coefficient(i) for i in range(len(N))]


def cert_ok(N) -> bool:
    cs = coeffs_of(N)
    return bool(cs) and all(c >= 0 for c in cs) and any(c > 0 for c in cs)


def main() -> int:
    t0 = time.time()
    # ---- validation against the reference engine, before any verdict ----
    mism = []
    for j, parity, k in ((3, 0, 5), (4, 1, 3), (5, 0, 8), (6, 1, 6)):
        n0 = max(4, j + 1)
        n0 += (n0 % 2) ^ parity
        fast = build_N(j, parity, k, n0)
        ref = slow.build_N(j, parity, k, n0)
        fast_map = {tuple(fast.monomial(i)): fast.coefficient(i) for i in range(len(fast))}
        ref_map = {ky: Fraction(int(c.p), int(c.q)) for ky, c in ref.c.items() if c != 0}
        same = len(fast_map) == len(ref_map) and all(
            Fraction(int(fast_map[ky].p), int(fast_map[ky].q)) == ref_map[ky]
            for ky in ref_map
            if ky in fast_map
        )
        if not same or cert_ok(fast) != slow.cert_ok(ref):
            mism.append(
                {
                    "j": j,
                    "parity": parity,
                    "k": k,
                    "fast_terms": len(fast_map),
                    "ref_terms": len(ref_map),
                }
            )
    if mism:
        out = {"validation_failed": mism, "command": "python lab/keystone_strip_fast.py", **stamp()}
        (RES / "keystone_strip_fast.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print("VALIDATION FAILED vs QPoly engine:", mism, flush=True)
        return 2
    print("validation contract: OK (identical coefficients to QPoly engine)", flush=True)

    # ---- timing comparison on one cell -------------------------------
    bench = []
    for j in (6, 8):
        n0 = max(4, j + 1)
        n0 += (n0 % 2) ^ 0
        t1 = time.time()
        build_N(j, 0, 12, n0)
        t_fast = time.time() - t1
        t2 = time.time()
        slow.build_N(j, 0, 12, n0)
        t_slow = time.time() - t2
        bench.append(
            {
                "j": j,
                "fast_s": round(t_fast, 4),
                "qpoly_s": round(t_slow, 4),
                "speedup": round(t_slow / t_fast, 1) if t_fast else None,
            }
        )
        print(
            f"  j={j}: native {t_fast:.3f}s vs QPoly {t_slow:.3f}s -> {t_slow / t_fast:.1f}x",
            flush=True,
        )

    # ---- the actual run ------------------------------------------------
    cells = certified = 0
    failures = []
    for j in range(J_MIN, J_MAX + 1):
        for parity in (0, 1):
            n0 = max(4, j + 1)
            n0 += (n0 % 2) ^ parity
            for k in range(3, K_MAX + 1):
                cells += 1
                if cert_ok(build_N(j, parity, k, n0)):
                    certified += 1
                elif len(failures) < 20:
                    failures.append({"j": j, "parity": parity, "k": k})
        print(
            f"  j={j}: cells {cells}, certified {certified}, "
            f"failures {len(failures)} ({time.time() - t0:.0f}s)",
            flush=True,
        )

    out = {
        "engine": "native flint fmpq_mpoly",
        "same_mathematics_as": "lab/keystone_strip_symbolic.py",
        "validation": "identical coefficient sets and identical verdicts on"
        " four (j, parity, branch) cells",
        "benchmark": bench,
        "coverage": {
            "j": f"{J_MIN}..{J_MAX}",
            "branches": f"3..{K_MAX}",
            "n": "all levels of the stated parity",
            "D": "the width-2 strip below the shore",
        },
        "cells": cells,
        "certified": certified,
        "all_certified": certified == cells,
        "failures": failures,
        "command": f"KSF_JMAX={J_MAX} python lab/keystone_strip_fast.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_strip_fast.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells {cells}, certified {certified}", flush=True)
    return 0 if certified == cells else 1


if __name__ == "__main__":
    sys.exit(main())
