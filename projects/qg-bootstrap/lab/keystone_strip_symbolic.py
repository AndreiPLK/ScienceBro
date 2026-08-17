"""STRIP CERTIFICATE: the whole theorem, symbolic in lam AND n, on the
width-2 strip below the shore.

The descent lemma (lab/keystone_dimension_walk.py, PROVED) says positivity at
D+2 implies positivity at D, uniformly in the spin. So everything below the
strip D in (T_hat - 2, T_hat] is free, and the entire remaining task is that
strip. Measured first on a grid: the Polya certificate there is MANIFEST --
1248 cells, all certified at bisection depth ZERO, including j = 2, which on
the full stretch could not be certified at all (its tangency needed sqrt-3
arithmetic).

This module carries lam and n symbolically on the strip, so one cell covers
a whole shore branch AND all levels of one parity:

        n   = n0 + 2 mu,                       mu >= 0
        lam = (a + b v)/(1 + v),               v  >= 0
        Q   = Q_shore - 1 + w/(1+w),           w  >= 0
              i.e. D from T_hat - 2 up to T_hat, with
              Q_shore = T_k(lam)/2 + n - j - 2 .

Uniform clearing, spelled out because this is where the far-below sign bug
came from: multiply by (1+w)^{j-1} (1+v)^{2(j-1)} prod_{i=1}^{j-1}(n-i)
s^{2(j-1)}. Each Q-factor becomes

    [ T_num/2 + (n - j - 1 + p + i)(1+v)^2 ](1+w) + w (1+v)^2

which carries degree 1 in (1+w) and degree 2 in (1+v), so with the
(1+w)^{j-1-t} and s_num^{2(j-1-t)} tails every term has the SAME total
degrees. Certificate: all coefficients nonnegative.

Validation contract runs first: the sign of N must match the exact rational
J at interior points of the strip.

Run: KSN_JMAX=10 python lab/keystone_strip_symbolic.py
Artifact: results/keystone_strip_symbolic.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_poly_in_Q  # noqa: E402
from keystone_npoly import interpolate, peval  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import QPoly  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J_MAX = int(os.environ.get("KSN_JMAX", "6"))
K_MAX = int(os.environ.get("KSN_KMAX", "12"))
MU_CAP = int(os.environ.get("KSN_MUCAP", "0"))  # 0 = unbounded mu (a ray)

W, V, MU = 0, 1, 2


def q(x: Fraction) -> fmpq:
    return fmpq(x.numerator, x.denominator)


def qp(d: dict) -> QPoly:
    return QPoly(3, {k: q(v) for k, v in d.items()})


def one3() -> QPoly:
    return QPoly.const(3, 1)


_E2T_CACHE: dict[tuple[int, int], list[Fraction]] = {}


def E2t_in_n(t: int, parity: int) -> list[Fraction]:
    """E_2t(n) as a polynomial in n for the given parity (Fact A)."""
    key = (t, parity)
    if key in _E2T_CACHE:  # interpolation is expensive; do it ONCE
        return _E2T_CACHE[key]
    start = 2 * t + 4
    start += (start % 2) ^ parity
    fit_k = 3 * t + 5
    pts = [
        (Fraction(n), Fraction(e_doubled_int(n)[t]))
        for n in range(start, start + 2 * (fit_k + 6), 2)
    ]
    pol = interpolate(pts[:fit_k])
    for n, y in pts[fit_k:]:  # must PREDICT, not fit
        if peval(pol, n) != y:
            raise AssertionError(f"E_2{2 * t} not polynomial in n (parity {parity})")
    _E2T_CACHE[key] = pol
    return pol


def poly_of_n(coeffs_in_n: list[Fraction], n0: int) -> QPoly:
    """Substitute n = n0 + 2 mu into a polynomial in n; returns QPoly(3)."""
    out = QPoly(3)
    base = qp({(0, 0, 0): Fraction(n0), (0, 0, 1): Fraction(2)})
    pw = {0: one3()}
    for d in range(1, len(coeffs_in_n)):
        pw[d] = pw[d - 1] * base
    for d, c in enumerate(coeffs_in_n):
        if c:
            out = out + q(c) * pw[d]
    return out


def linear_in_n(const: Fraction, n_coef: Fraction, n0: int) -> QPoly:
    """const + n_coef * n, with n = n0 + 2 mu."""
    return qp({(0, 0, 0): const + n_coef * n0, (0, 0, 1): 2 * n_coef})


def branch_range(k: int) -> tuple[Fraction, Fraction]:
    if k == 3:
        return Fraction(0), Fraction(2, 3)
    lo = Fraction(3, 5) * (k - Fraction(5, 2))
    hi = Fraction(3, 5) * (k - Fraction(3, 2))
    if k == 4:
        lo = Fraction(2, 3)
    return lo, hi


def build_N(j: int, parity: int, k: int, n0: int) -> QPoly:
    a, b = branch_range(k)
    one = one3()
    w_p = qp({(1, 0, 0): Fraction(1)})
    v_p = qp({(0, 1, 0): Fraction(1)})
    onepw, onepv = one + w_p, one + v_p
    onepv2 = onepv * onepv

    # s = lam + n - 1  ->  s_num = (a + n - 1) + (b + n - 1) v
    s_num = linear_in_n(a - 1, Fraction(1), n0) + linear_in_n(b - 1, Fraction(1), n0) * v_p

    lam_num = qp({(0, 0, 0): a, (0, 1, 0): b})  # lam = lam_num/(1+v)
    r = Fraction(3 * (2 * k - 3), k * (k - 2))
    t_num = q(r) * (lam_num * lam_num + (2 * k - 2) * (lam_num * onepv) + onepv2) + (2 * k) * onepv2
    delta_num = q(Fraction(1, 2)) * t_num - 2 * onepv2

    s_pows = {0: one}
    for d in range(1, 2 * (j - 1) + 1):
        s_pows[d] = s_pows[d - 1] * s_num
    w_pows = {0: one}
    for d in range(1, j):
        w_pows[d] = w_pows[d - 1] * onepw

    N = QPoly(3)
    for t in range(j):
        m = j - 1 - t
        e_pol = poly_of_n(E2t_in_n(t, parity), n0)
        term = q(Fraction((-1) ** t)) * e_pol
        for i in range(1, t + 1):  # prod (j - i)
            term = term * q(Fraction(j - i)) * one
        for i in range(t + 1, j):  # leftover prod (n - i)
            term = term * linear_in_n(Fraction(-i), Fraction(1), n0)
        term = term * s_pows[2 * (j - 1 - t)]
        for i in range(m):  # alpha_t, p = n-j-1/2
            term = term * linear_in_n(Fraction(1, 2) - j + i, Fraction(1), n0)
        for i in range(m, j - 1):  # the STRIP Q-factors
            # Q + p + 2 + i  with  Q = Q_shore - 1 + w/(1+w),
            # Q_shore = T_k(lam)/2 + n - j - 2, cleared by (1+w)(1+v)^2
            base = linear_in_n(Fraction(-1) - j + i, Fraction(1), n0)
            fac = (q(Fraction(1, 2)) * t_num + base * onepv2) * onepw + w_p * onepv2
            term = term * fac
        term = term * w_pows[j - 1 - t]
        N = N + term
    return N


def eval3(P: QPoly, w: Fraction, v: Fraction, mu: Fraction) -> Fraction:
    tot = Fraction(0)
    for (dw, dv, dm), c in P.c.items():
        tot += Fraction(int(c.p), int(c.q)) * w**dw * v**dv * mu**dm
    return tot


def validate(j: int, parity: int, k: int, n0: int) -> list[str]:
    N = build_N(j, parity, k, n0)
    a, b = branch_range(k)
    bad = []
    for mu in (Fraction(0), Fraction(2), Fraction(5)):
        n = n0 + 2 * int(mu)
        for fv in (Fraction(1, 3), Fraction(2)):
            lam = (a + b * fv) / (1 + fv)
            if lam <= 0:
                continue
            pol = J_poly_in_Q(j, n, lam)
            delta = (
                Fraction(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) / 2
                + k
                - 2
            )
            for fw in (Fraction(1, 4), Fraction(3)):
                Qv = Fraction(n - j) + delta * fw / (1 + fw)
                jv = sum(c * Qv**d for d, c in enumerate(pol))
                nv = eval3(N, fw, fv, mu)
                if (nv > 0) != (jv > 0):
                    bad.append(
                        f"j={j} par={parity} k={k} n={n} lam={lam} "
                        f"w={fw}: N>0={nv > 0} vs J>0={jv > 0}"
                    )
    return bad


def cert_ok(N: QPoly) -> bool:
    vals = list(N.c.values())
    return bool(vals) and all(v >= 0 for v in vals) and any(v > 0 for v in vals)


def main() -> int:
    t0 = time.time()
    problems = validate(3, 0, 5, 6) + validate(4, 1, 3, 7) + validate(5, 0, 8, 8)
    if problems:
        out = {
            "validation_failed": problems[:10],
            "certified": 0,
            "command": "python lab/keystone_strip_symbolic.py",
            **stamp(),
        }
        (RES / "keystone_strip_symbolic.json").write_text(
            json.dumps(out, indent=1), encoding="utf-8"
        )
        print("VALIDATION FAILED:", *problems[:6], sep="\n  ", flush=True)
        return 2
    print("validation contract: OK (sign of N matches exact J)", flush=True)

    # The certificate is NOT manifest from the very first level: the
    # D-threshold has an interior minimum in n, so positivity in n is not
    # monotone and a nonnegative-coefficient certificate cannot start at n0.
    # Structure used instead: TAIL (all levels n >= n_tail, certified
    # symbolically in one shot) + BASE (the finitely many levels below it,
    # already covered cell by cell by step 1, which certified n up to j+20).
    STEP1_N_MAX = 20  # step 1 covered n <= j + 20
    cells = certified = 0
    failures, rows = [], []
    for j in range(3, J_MAX + 1):
        for parity in (0, 1):
            n0 = max(4, j + 1)
            n0 += (n0 % 2) ^ parity
            for k in range(3, K_MAX + 1):
                cells += 1
                M = None
                for cand in range(0, 60):
                    if cert_ok(build_N(j, parity, k, n0 + 2 * cand)):
                        M = cand
                        break
                if M is None:
                    failures.append(
                        {
                            "j": j,
                            "parity": parity,
                            "k": k,
                            "n0": n0,
                            "reason": "no manifest tail up to M=59",
                        }
                    )
                    continue
                n_tail = n0 + 2 * M
                base_levels = list(range(n0, n_tail, 2))
                gap = [n for n in base_levels if n > j + STEP1_N_MAX]
                if gap:
                    failures.append(
                        {
                            "j": j,
                            "parity": parity,
                            "k": k,
                            "reason": "base level outside step-1 coverage",
                            "levels": gap,
                        }
                    )
                    continue
                certified += 1
                rows.append(
                    {
                        "j": j,
                        "parity": parity,
                        "k": k,
                        "n_tail_start": n_tail,
                        "base_levels": base_levels,
                        "M": M,
                    }
                )
        print(
            f"  j={j}: cells {cells}, certified {certified}, "
            f"failures {len(failures)} ({time.time() - t0:.0f}s)",
            flush=True,
        )
    max_M = max((r["M"] for r in rows), default=None)
    max_tail = max((r["n_tail_start"] for r in rows), default=None)

    out = {
        "claim": "one certificate per (j, parity, branch) covering ALL"
        " levels n of that parity and ALL lam on the branch,"
        " on the width-2 STRIP below the shore; everything"
        " below the strip follows from the proved descent lemma",
        "substitutions": {
            "n": "n0 + 2 mu, mu >= 0",
            "lam": "(a + b v)/(1+v), v >= 0",
            "Q": "(n-j) + Delta(lam) w/(1+w), w >= 0",
        },
        "uniform_clearing": "(1+w)^{j-1} (1+v)^{2(j-1)}"
        " prod_{i=1}^{j-1}(n-i) s^{2(j-1)}, each factor"
        " strictly positive on the domain",
        "validation": "sign of N matches the exact rational J at interior"
        " points (3 cells x 12 points)",
        "coverage": {
            "j": f"3..{J_MAX}",
            "branches": f"k=3..{K_MAX}",
            "n": "every level of the stated parity, unbounded",
            "NOT covered": "j above the tested range, and lam above the last branch",
        },
        "structure": "TAIL + BASE. The nonnegative-coefficient certificate"
        " cannot start at the first level, because the"
        " D-threshold has an INTERIOR minimum in n and so"
        " positivity in n is not monotone. Instead: for each"
        " (j, parity, branch) find the smallest shift M such"
        " that the tail n >= n0 + 2M is manifestly positive"
        " (one certificate, infinitely many levels), and let"
        " the finitely many levels below it be the base,"
        " which step 1 already certified cell by cell.",
        "join_condition_checked": "every base level must satisfy"
        " n <= j + 20, the coverage of step 1;"
        " cells failing this are reported as"
        " failures, not silently dropped",
        "cells": cells,
        "certified": certified,
        "all_certified": certified == cells,
        "max_shift_M": max_M,
        "max_tail_start_level": max_tail,
        "rows": rows[:60],
        "failures": failures,
        "command": f"KSN_JMAX={J_MAX} python lab/keystone_strip_symbolic.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_strip_symbolic.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells {cells}, certified {certified}", flush=True)
    print("SYMBOLIC-n CERTIFICATE " + ("HOLDS" if certified == cells else "INCOMPLETE"), flush=True)
    return 0 if certified == cells else 1


if __name__ == "__main__":
    sys.exit(main())
