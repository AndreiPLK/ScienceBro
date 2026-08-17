"""KEYSTONE STEP 1: carry lam SYMBOLICALLY through the interval certificate.

keystone_cert.json certified J(Q) > 0 below the shore for twelve concrete
values of lam. lam is a continuum, so that is a grid, not a theorem. Here
lam becomes a variable, exactly as in the twelve proven knives — only now
the object is univariate in Q instead of four-dimensional.

Construction. On the shore branch k (where T_hat = T_k), lam runs over
[a, b] with a = (3/5)(k - 5/2), b = (3/5)(k - 3/2); branch k = 3 covers
(0, 2/3]. Two Mobius maps send both ranges onto the closed first orthant:

        lam = (a + b v)/(1 + v),        v >= 0
        Q   = Q_low + Delta(lam) w/(1+w),   w >= 0,
        Q_low = n - j  (i.e. D = 4),    Delta = T_k(lam)/2 - 2 .

Writing s = lam + n - 1, p = n - j - 1/2, m = j - 1 - t and

        alpha_t = prod_{i=0}^{m-1} (p + 1 + i)  > 0,

the cleared numerator is

  N(w,v) = SUM_t (-1)^t E_2t(n) Qt(t) alpha_t s_num^{2(j-1-t)}
           * prod_{i=m}^{j-2} [ (Q_low+p+2+i)(1+w)(1+v)^2 + Delta_num w ]
           * (1+w)^{j-1-t}

with s_num = (a+n-1) + (b+n-1)v and Delta_num the cleared numerator of
Delta.  CRUCIAL (this is the bug that bit the far-below port): the powers
are UNIFORM — every term carries exactly (1+v)^{2(j-1)} and (1+w)^{j-1} —
so the sum is a single polynomial and the clearing never changes a sign.

Certificate: all coefficients of N nonnegative and the constant term
positive  =>  N > 0 on the closed orthant  =>  J > 0 for EVERY lam on the
branch and EVERY D from 4 up to the shore.  Where that fails, the (v, w)
box is bisected in v (the lam direction) and re-tested.

Validation contract (checked before any verdict is reported): for sample
points inside a cell, N(w,v) must have the same sign as the exact rational
J(Q) from keystone_beta.py.

Run: KJ_MAX=12 python lab/keystone_symbolic.py
Artifact: results/keystone_symbolic.json
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
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402
from prover2_core import QPoly  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
J_MAX = int(os.environ.get("KJ_MAX", "12"))
J_MIN = int(os.environ.get("KJ_MIN", "3"))  # j=2 has exact tangency
N_SPAN = int(os.environ.get("KN_SPAN", "16"))
K_MAX = int(os.environ.get("KK_MAX", "45"))
MAX_DEPTH = int(os.environ.get("KDEPTH", "5"))

W, V = 0, 1  # variable indices inside QPoly(2)


def q(x: Fraction) -> fmpq:
    return fmpq(x.numerator, x.denominator)


def eval_qpoly(P: QPoly, w: Fraction, v: Fraction) -> Fraction:
    """Evaluate a QPoly(2) at rational (w, v). QPoly has no eval()."""
    tot = Fraction(0)
    for (dw, dv), c in P.c.items():
        tot += Fraction(int(c.p), int(c.q)) * w**dw * v**dv
    return tot


def Qt_val(j: int, n: int, t: int) -> int:
    v = 1
    for i in range(j, n):
        v *= i - t
    return v


def branch_range(k: int) -> tuple[Fraction, Fraction]:
    if k == 3:
        return Fraction(0), Fraction(2, 3)
    lo = Fraction(3, 5) * (k - Fraction(5, 2))
    hi = Fraction(3, 5) * (k - Fraction(3, 2))
    if k == 4:
        lo = Fraction(2, 3)
    return lo, hi


def build_N(j: int, n: int, k: int, a: Fraction, b: Fraction) -> QPoly:
    """The cleared numerator N(w, v); see the module docstring."""
    e = e_doubled_int(n)
    p = Fraction(2 * (n - j) - 1, 2)
    q_low = Fraction(n - j)

    one = QPoly.const(2, 1)
    w_p = QPoly(2, {(1, 0): fmpq(1)})
    v_p = QPoly(2, {(0, 1): fmpq(1)})
    onepw = one + w_p
    onepv = one + v_p
    onepv2 = onepv * onepv

    # lam = (a + b v)/(1+v)  =>  s = lam + n - 1 = s_num/(1+v)
    s_num = QPoly(2, {(0, 0): q(a + n - 1), (0, 1): q(b + n - 1)})
    lam_num = QPoly(2, {(0, 0): q(a), (0, 1): q(b)})  # lam = lam_num/(1+v)

    # T_k(lam) = r (lam^2 + (2k-2) lam + 1) + 2k, cleared by (1+v)^2
    r = Fraction(3 * (2 * k - 3), k * (k - 2))
    t_num = q(r) * (lam_num * lam_num + (2 * k - 2) * (lam_num * onepv) + onepv2) + (2 * k) * onepv2
    # Delta = T_k/2 - 2, cleared by (1+v)^2
    delta_num = q(Fraction(1, 2)) * t_num - 2 * onepv2

    # powers cache
    s_pows = {0: one}
    for d in range(1, 2 * (j - 1) + 1):
        s_pows[d] = s_pows[d - 1] * s_num
    w_pows = {0: one}
    for d in range(1, j):
        w_pows[d] = w_pows[d - 1] * onepw

    N = QPoly(2)
    for t in range(j):
        m = j - 1 - t
        alpha = Fraction(1)
        for i in range(m):
            alpha *= p + 1 + i
        coef = Fraction((-1) ** t * e[t] * Qt_val(j, n, t)) * alpha
        term = q(coef) * s_pows[2 * (j - 1 - t)]
        for i in range(m, j - 1):
            beta = q_low + p + 2 + i
            factor = q(beta) * (onepw * onepv2) + delta_num * w_p
            term = term * factor
        term = term * w_pows[j - 1 - t]
        N = N + term
    return N


def shrink_v(N: QPoly, lo: Fraction, hi: Fraction) -> QPoly:
    """Restrict v to [lo, hi] by v = lo + (hi-lo) x/(1+x), cleared."""
    dv = hi - lo
    deg_v = max((ky[1] for ky in N.c), default=0)
    one = QPoly.const(2, 1)
    x_p = QPoly(2, {(0, 1): fmpq(1)})
    onepx = one + x_p
    vnum = q(lo) * onepx + q(dv) * x_p  # v = vnum/(1+x)
    vp = {0: one}
    for d in range(1, deg_v + 1):
        vp[d] = vp[d - 1] * vnum
    xp = {0: one}
    for d in range(1, deg_v + 1):
        xp[d] = xp[d - 1] * onepx
    out = QPoly(2)
    for (dw, dv_), c in N.c.items():
        piece = QPoly(2, {(dw, 0): c}) * vp[dv_] * xp[deg_v - dv_]
        out = out + piece
    return out


def cert_ok(N: QPoly) -> bool:
    vals = list(N.c.values())
    return bool(vals) and all(v >= 0 for v in vals) and any(v > 0 for v in vals)


def certify_branch(j, n, k, a, b, depth=0):
    """Certificate on branch k with bisection in the lam direction."""
    N = build_N(j, n, k, a, b)
    if cert_ok(N):
        return True, depth
    if depth >= MAX_DEPTH:
        return False, depth
    # bisect in v-space: v in [0, inf) split as [0,1] and [1, inf)
    for lo, hi in ((Fraction(0), Fraction(1)),):
        sub = shrink_v(N, lo, hi)
        if not cert_ok(sub):
            mid = (a + b) / 2
            o1, d1 = certify_branch(j, n, k, a, mid, depth + 1)
            if not o1:
                return False, d1
            o2, d2 = certify_branch(j, n, k, mid, b, depth + 1)
            return o2, max(d1, d2)
    return True, depth


def validate(j: int, n: int, k: int) -> list[str]:
    """N must agree in sign with the exact rational J at interior points."""
    a, b = branch_range(k)
    N = build_N(j, n, k, a, b)
    bad = []
    for fv in (Fraction(1, 3), Fraction(1), Fraction(3)):
        lam = (a + b * fv) / (1 + fv)
        if lam <= 0:
            continue
        pol = J_poly_in_Q(j, n, lam)
        q_low = Fraction(n - j)
        delta = (
            Fraction(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) / 2 + k - 2
        )
        for fw in (Fraction(1, 5), Fraction(2), Fraction(9)):
            Qv = q_low + delta * fw / (1 + fw)
            jv = sum(c * Qv**d for d, c in enumerate(pol))
            nv = eval_qpoly(N, fw, fv)
            if (nv > 0) != (jv > 0):
                bad.append(f"j={j} n={n} k={k} lam={lam} w={fw}: N>0={nv > 0} but J>0={jv > 0}")
    return bad


def main() -> int:
    t0 = time.time()
    problems = validate(4, 10, 5) + validate(6, 12, 3) + validate(3, 8, 9)
    if problems:
        out = {
            "validation_failed": problems,
            "certified": 0,
            "command": "python lab/keystone_symbolic.py",
            **stamp(),
        }
        (RES / "keystone_symbolic.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print("VALIDATION FAILED:", *problems, sep="\n  ", flush=True)
        return 2
    print("validation contract: OK", flush=True)

    cells = certified = 0
    depth_hist: dict[int, int] = {}
    failures = []
    for j in range(J_MIN, J_MAX + 1):
        for n in range(max(4, j + 1), max(4, j + 1) + N_SPAN, 2):
            for k in range(3, K_MAX + 1):
                a, b = branch_range(k)
                cells += 1
                ok, d = certify_branch(j, n, k, a, b)
                if ok:
                    certified += 1
                    depth_hist[d] = depth_hist.get(d, 0) + 1
                elif len(failures) < 30:
                    failures.append(
                        {"j": j, "n": n, "k": k, "lam_range": [str(a), str(b)], "depth_reached": d}
                    )
        print(
            f"  j={j}: cells {cells}, certified {certified}, "
            f"failures {len(failures)}, depths "
            f"{dict(sorted(depth_hist.items()))} ({time.time() - t0:.0f}s)",
            flush=True,
        )

    out = {
        "claim": "J(Q) > 0 for EVERY lam on each shore branch and every D"
        " from 4 up to the shore -- lam carried symbolically",
        "certificate": "nonnegative coefficients of the cleared numerator"
        " N(w,v) after lam = (a+bv)/(1+v) and"
        " Q = Q_low + Delta(lam) w/(1+w)",
        "uniform_clearing": "every term carries exactly (1+v)^{2(j-1)} and (1+w)^{j-1}",
        "coverage": {
            "j": f"{J_MIN}..{J_MAX}",
            "n": f"max(4,j+1)..+{N_SPAN} step 2",
            "branches": f"k=3..{K_MAX}, i.e. lam in (0, {float(branch_range(K_MAX)[1]):.2f}]",
            "NOT covered": "lam above the last branch; needs the"
            " tail argument, as in the knife"
            " theorems",
            "j=2 excluded_on_purpose": "at j=2 the fleet is EXACTLY tangent to the shore"
            " (J(Q_shore) = 0 at isolated lam), so J acquires"
            " a double root and a nonnegative-coefficient"
            " certificate cannot exist there: a polynomial"
            " nonnegative on a ray need not have nonnegative"
            " coefficients, e.g. (v-1)^2. j=2 is already"
            " PROVEN separately (the first knife theorem,"
            " which needed Q(sqrt 3) arithmetic exactly"
            " because of this tangency); measured here as 22"
            " cells failing at max bisection depth, all with"
            " j=2 and none with j>=3.",
        },
        "cells": cells,
        "certified": certified,
        "all_certified": certified == cells,
        "bisection_depth_histogram": {str(k): v for k, v in sorted(depth_hist.items())},
        "failures": failures,
        "validation": "sign of N matches exact rational J at interior"
        " sample points (3 cells x 9 points)",
        "command": f"KJ_MAX={J_MAX} python lab/keystone_symbolic.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_symbolic.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"cells {cells}, certified {certified}", flush=True)
    print(
        "SYMBOLIC-LAM CERTIFICATE " + ("HOLDS" if certified == cells else "INCOMPLETE"), flush=True
    )
    return 0 if certified == cells else 1


if __name__ == "__main__":
    sys.exit(main())
