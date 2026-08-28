"""The derivative form: the truncated knife sum IS a product over r roots.

Starting from the B-form (lab/bform_positivity.py)

    K_r = sum_{t=0}^{r} (-1)^t c_t e_t(b),
    c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t],   b_k = (n-2k)^2 / s^2,

split c_t into the lam-free part and the D-carrying part,

    c_t = w_t * d_t,   w_t = (r)_t/(N)_t,   d_t = (H-r)_t/(n-3/2)_t,   N = n-1.

TWO OBSERVATIONS.

(1) w_t is a POLYNOMIAL in t. The standard identity C(r,t)/C(N,t) =
C(N-t, N-r)/C(N,r) gives w_t = (N-t)_m / [m! C(N,r)] with m = N - r, so w_t
vanishes identically for t = r+1..N -- the truncation at depth r is automatic,
not imposed. Hence the sum may be run to t = N, and

    sum_{t=0}^{N} (-1)^t (N-t)_m e_t(b) y^t  =  (d/dx)^m [ prod_k (x - b_k y) ]
                                                evaluated at x = 1,

because x^{N-t} differentiated m times at x = 1 is exactly (N-t)_m.

(2) That derivative is homogeneous. Writing x = y u turns prod_k (x - b_k y)
into y^N prod_k (u - b_k), so the roots in x are y times the roots of the m-th
derivative of prod_k (u - b_k), which do not depend on y. Cancelling the
constants (the leading coefficient N!/r! divided by m! C(N,r) is exactly 1):

    THEOREM (derivative form).
    Let eta_1..eta_r be the roots of the (n-1-r)-th derivative of
    prod_{k=1}^{n-1} (u - b_k). Then

        K_r  =  sum_{t=0}^{r} (-1)^t d_t e_t(eta)                        (D-FORM)
             =  INT_1^inf  prod_{i=1}^{r} (1 - eta_i y)  dsigma(y),

    where dsigma(y) = [Gamma(C+eps+1)/(Gamma(C+1)Gamma(eps))]
    y^{-C-eps-1} (y-1)^{eps-1} dy on [1, inf), C = n-3/2, eps = H-r-C =
    D/2 + (n-2-r) > 0, which represents d_t for every t < C+1 (so for every
    t <= r).

WHY IT MATTERS. prod_k (u - b_k) has only real roots in [0, B], B = (n-2)^2/s^2,
so by Rolle every eta_i is real and in [0, B] too. The integrand is therefore a
product of r REAL linear factors, strictly positive for y < 1/max_i eta_i, and
the whole depth dependence has moved from an alternating sum into r roots and
one explicit density on a single variable. The alternating sum is gone.

Differentiating m times CONTRACTS the root span: at r = 1 the only root is the
mean of the b's, and the span grows back to the full [min b, max b] as r -> N.
This script measures that contraction, because it is exactly the quantity that
decides how far out the integrand stays positive.

CHECKS (all exact where exact is possible):
  1. w_t = C(N-t, N-r)/C(N,r), and w_t = 0 for t > r;
  2. the D-FORM against the B-form and against the reference engine, at
     positive AND negative knife points;
  3. eta real and inside [0, B], via certified root enclosures;
  4. the root contraction max(eta)/B by depth;
  5. the sigma representation of d_t, by interval arithmetic on the Gamma ratio.

Run: python lab/bform_derivative_form.py -> results/bform_derivative_form.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import arb, ctx, fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bform_positivity import K_bform, b_values  # noqa: E402
from moment_kernel_probe import falling, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def base_poly(b: list[fmpq]) -> fmpq_poly:
    """prod_k (u - b_k), exact."""
    p = fmpq_poly([1])
    for x in b:
        p = p * fmpq_poly([-x, 1])
    return p


def eta_e_sym(b: list[fmpq], r: int) -> list[fmpq]:
    """e_t(eta), t = 0..r, from the coefficients of the m-th derivative.

    prod_i (u - eta_i) = sum_t (-1)^t e_t(eta) u^{r-t}, so
    e_t(eta) = (-1)^t a_{r-t} / a_r with a_i the coefficients.
    Exact: no root-finding is needed to get the symmetric functions.
    """
    p = base_poly(b)
    m = len(b) - r
    for _ in range(m):
        p = p.derivative()
    lead = p[r]
    return [fmpq((-1) ** t) * p[r - t] / lead for t in range(r + 1)]


def d_seq(n: int, r: int, H: fmpq) -> list[fmpq]:
    """d_t = (H-r)_t / (n-3/2)_t."""
    return [falling(H - r, t) / falling(fmpq(2 * n - 3, 2), t) for t in range(r + 1)]


def K_dform(n: int, j: int, lam: fmpq, D: fmpq) -> fmpq:
    r = j - 1
    H = (D + 4 * n - 7) / 2
    e = eta_e_sym(b_values(n, lam), r)
    d = d_seq(n, r, H)
    return sum((fmpq((-1) ** t) * d[t] * e[t] for t in range(r + 1)), fmpq(0))


def eta_roots(b: list[fmpq], r: int):
    p = base_poly(b)
    for _ in range(len(b) - r):
        p = p.derivative()
    return [z for z, _ in p.complex_roots()]


def main() -> int:
    t0 = time.time()
    ctx.prec = 300
    out: dict = {}

    # ---- 1. w_t = C(N-t, N-r)/C(N,r), and the automatic truncation
    bad_w, checked_w = [], 0
    for n in range(5, 40):
        N = n - 1
        for r in range(2, N):
            for t in range(0, N + 1):
                lhs = falling(fmpq(r), t) / falling(fmpq(N), t)
                rhs = fmpq(comb(N - t, N - r) if N - t >= N - r >= 0 else 0, comb(N, r))
                checked_w += 1
                if lhs != rhs:
                    bad_w.append([n, r, t])
    out["w_identity"] = {"checked": checked_w, "violations": bad_w[:8],
                         "n_violations": len(bad_w)}
    print(f"w_t = C(N-t,N-r)/C(N,r) (with the automatic zeros for t > r): "
          f"{checked_w} checks, {len(bad_w)} violations", flush=True)

    # ---- 2. the D-form against the B-form and the reference engine
    trials, bad_bd, bad_ref, negs, zeros = 0, 0, 0, 0, 0
    fails = []
    for lam in (fmpq(1, 2), fmpq(1), fmpq(5, 2), fmpq(7), fmpq(72), fmpq(650, 3)):
        Th = shore(lam)[0]
        for n in (8, 12, 20, 33):
            for j in range(3, min(n - 1, 10) + 1):
                for D in (Th, Th * fmpq(4, 5), Th * fmpq(3, 2), Th + 6, fmpq(4)):
                    if D <= 3:
                        continue
                    trials += 1
                    kd = K_dform(n, j, lam, D)
                    kb = K_bform(n, j, lam, D)
                    if kd != kb:
                        bad_bd += 1
                        if len(fails) < 5:
                            fails.append([str(lam), n, j, str(D)])
                    sr = ref_sign(j, n, lam, D)
                    negs += sr < 0
                    zeros += sr == 0
                    if ((kd > 0) - (kd < 0)) != sr:
                        bad_ref += 1
    out["dform_identity"] = {"trials": trials, "vs_bform_mismatches": bad_bd,
                             "vs_reference_mismatches": bad_ref,
                             "negative_refs": negs, "zero_refs": zeros,
                             "sample_fail": fails}
    print(f"D-form: {trials} trials, {bad_bd} disagreements with the B-form, "
          f"{bad_ref} with the reference engine "
          f"({negs} negative reference points, {zeros} zeros)", flush=True)
    if bad_bd or bad_ref:
        print("D-FORM FAILS -- the derivative identity is wrong", flush=True)
        return 1

    # ---- 3 & 4. eta real, inside [0, B], and the root contraction
    contraction = []
    bad_real = []
    for n in (12, 20, 33):
        for lam in (fmpq(1), fmpq(7), fmpq(72)):
            b = b_values(n, lam)
            B = max(b)
            for r in (2, 4, 6, n // 2, n - 2):
                if not 1 <= r <= n - 2:
                    continue
                roots = eta_roots(b, r)
                real_ok = all(z.imag.contains(arb(0)) for z in roots)
                lo = min(float(z.real.lower()) for z in roots)
                hi = max(float(z.real.upper()) for z in roots)
                inside = lo >= -1e-30 and arb(str(hi)) <= arb(str(float(B))) * arb("1.0000001")
                if not (real_ok and inside):
                    bad_real.append({"n": n, "lam": str(lam), "r": r,
                                     "all_real": real_ok, "lo": lo, "hi": hi,
                                     "B": float(B)})
                contraction.append({"n": n, "lam": str(lam), "r": r,
                                    "max_eta_over_B": hi / float(B),
                                    "one_over_max_eta": 1 / hi if hi > 0 else None,
                                    "B": float(B)})
    out["eta_real_and_bounded"] = {"violations": bad_real,
                                   "n_violations": len(bad_real),
                                   "cases": len(contraction)}
    out["root_contraction"] = contraction
    print(f"eta real and inside [0, B]: {len(bad_real)} violations "
          f"over {len(contraction)} cases", flush=True)
    print("root contraction max(eta)/B by depth (n = 20, lam = 7):", flush=True)
    for c in contraction:
        if c["n"] == 20 and c["lam"] == "7":
            print(f"   r={c['r']:>3}: max(eta)/B = {c['max_eta_over_B']:.4f}", flush=True)

    # ---- 5. the sigma representation of d_t, via the Gamma ratio
    bad_sigma = []
    for n in (12, 20):
        for r in (3, 6, n - 2):
            for Dv in (fmpq(20), fmpq(150)):
                H = (Dv + 4 * n - 7) / 2
                C = arb(2 * n - 3) / 2
                epsq = H - r - fmpq(2 * n - 3, 2)
                eps = arb(int(epsq.p)) / arb(int(epsq.q))
                for t in range(0, r + 1):
                    x = falling(H - r, t) / falling(fmpq(2 * n - 3, 2), t)
                    lhs = arb(int(x.p)) / arb(int(x.q))
                    rhs = ((C + eps + 1).gamma() * (C - t + 1).gamma()
                           / ((C + 1).gamma() * (C + eps - t + 1).gamma()))
                    if not (lhs - rhs).contains(arb(0)):
                        bad_sigma.append({"n": n, "r": r, "D": str(Dv), "t": t})
    out["sigma_gamma_identity_violations"] = bad_sigma
    print(f"d_t = Gamma(C+eps+1)Gamma(C-t+1)/[Gamma(C+1)Gamma(C+eps-t+1)] "
          f"(the sigma representation): {len(bad_sigma)} violations", flush=True)

    out["claim"] = (
        "THE DERIVATIVE FORM. The lam-free factor w_t = (r)_t/(n-1)_t of the "
        "B-form equals C(N-t,N-r)/C(N,r), a polynomial in t that vanishes for "
        "t > r, so the depth truncation is automatic and the sum may be run to "
        "t = N. Then x^{N-t} differentiated m = N-r times at x = 1 supplies "
        "(N-t)_m exactly, and homogeneity in y removes the y dependence of the "
        "roots. RESULT: K_r = sum_t (-1)^t d_t e_t(eta) with "
        "d_t = (H-r)_t/(n-3/2)_t and eta_1..eta_r the roots of the (n-1-r)-th "
        "derivative of prod_k (u - b_k); equivalently K_r = INT_1^inf "
        "prod_i (1 - eta_i y) dsigma(y) with sigma the explicit Beta-type "
        "density representing d_t. The alternating sum becomes a product of r "
        "real linear factors against one explicit density on one variable. "
        "By Rolle every eta_i is real in [0, B], B = (n-2)^2/s^2 < 1, and the "
        "m-fold differentiation CONTRACTS the span -- measured here. This is a "
        "structural identity, verified, NOT yet a positivity proof: sigma has "
        "unbounded support, so the integrand's positivity on y < 1/max(eta) "
        "does not by itself close the argument."
    )
    out["command"] = "python lab/bform_derivative_form.py"
    out["seconds"] = round(time.time() - t0, 1)
    path = RES / "bform_derivative_form.json"
    path.write_text(json.dumps({**out, **stamp()}, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
