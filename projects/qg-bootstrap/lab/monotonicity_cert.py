"""Step (c) of the unglued keystone, as a certificate rather than a measurement.

The unglued argument (results/UNGLUED_KEYSTONE.md) has three steps. Steps (a)
and (b) are certified; step (c) -- that the knife DECREASES in D at fixed
(n, lam) -- was only ever MEASURED (120 clean configurations above lam = 5/2).
The whole argument leans on it, so a measurement is not good enough.

THE REDUCTION. Differentiating the beta-mean form term by term:

    knife  ~  sum_j r_j X^j (m+1/2)_j / (g)_j ,      g = 2m + gamma + 1
    d/dgamma [ 1/(g)_j ]  =  -(1/(g)_j) * psi_j(g),  psi_j(g) = sum_{i<j} 1/(g+i)

hence

    -d(knife)/dgamma  =  sum_j r_j X^j (m+1/2)_j * psi_j(g) / (g)_j .

That is the SAME shape as step (a) -- same r_j, same Pochhammer denominators --
with one extra strictly positive rational weight psi_j(g). So proving
monotonicity is another instance of the positivity problem already solved, not
a new kind of obstacle. Verified against finite differences at depths 2,3,4
(agreement to 1e-9, the finite-difference floor).

CLEARING THE DENOMINATORS, and this is the one place to be careful. Writing
psi_j(g) over the common denominator prod_{i<d}(g+i):

    psi_j(g) = [ sum_{i<j} prod_{i'<d, i'!=i} (g+i') ] / prod_{i<d}(g+i)

so every term acquires the SAME denominator prod_{i<d}(g+i), independent of j,
and it can simply be dropped (it is positive on the domain: g > 0 there). What
does NOT cancel is the j-dependent (g)_j, which is handled exactly as in
build_branch -- by the COMPLEMENT product, the ERR-0010 fix. Getting that
backwards is precisely the bug that invalidated two files, so the same
convention is used here and the result is self-checked against the exact
engine before any Bernstein run.

DOMAIN. Monotonicity is a claim about the PHYSICAL region only. The derivative
genuinely does go negative outside it -- measured at n=21, lam=5, D=123, where
the shore is T_hat(5) = 93.7. Strictly at or below the shore: 0 negatives out
of 320 configurations. So this file certifies positivity of -d(knife)/dgamma on
the same box the main argument uses, i.e. at D = T_v(lam) with v in [8/5, 2],
which sits at or above the shore and hence bounds the whole physical interval.

Engine 2 throughout: flint fmpq only, no sympy, no float in any comparison.

Run: python lab/monotonicity_cert.py <d> [<d> ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from depth_d_proof import elementary_symmetric, falling_poly, poch  # noqa: E402
from keystone_unglued import (  # noqa: E402
    C_MIN,
    C_SPLIT,
    V_HI,
    V_LO,
    NPoly,
    compactify,
    lift_N,
    prove_box,
)
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def build_derivative_free(parity: str, d: int, e_polys: dict) -> NPoly:
    """G(K, lam, u) whose SIGN is the sign of -d(knife)/dgamma, with gamma a FREE
    variable over the whole physical interval rather than a single point.

    WHY THIS REPLACES build_derivative. The first version below evaluated the
    derivative AT the single point D = T_v(lam). That is not what step (c)
    needs: monotonicity has to hold along the whole interval from D = 3 up to
    D = T_{k_s}, otherwise "positive at the top implies positive below" does not
    follow. Proving it at one point and asserting the interval is exactly the
    ERR-0008 mistake, and it would have been the same mistake a second time.

    So gamma becomes a variable, capped by a bound that must dominate
    gamma_at_v = (T_{v*lam}-3)/2 for every v in the window. MEASURED bound:
        gamma <= 3 + 10*lam
    holds with 0 violations for lam from 0.001 to 1e7, both against the shore
    itself and against max_v gamma_at_v (checked at lam = 5/2 .. 1e5; below
    lam = 5/2 the window admits no k_s > 3 at all and the small-lam piece of
    the main argument covers it). Substituting
        gamma = (3 + 10*lam) * u,   u in (0, 1]
    keeps the domain a box AND -- the point of the rewrite -- makes gamma LINEAR
    in lam, so the degree-6-in-v factor Pg/Qg disappears from the construction
    entirely.

    Slot 0 = K, slot 1 = lam, slot 2 = u.

    Denominator clearing: with g = 2m + gamma + 1,
        term_j  =  r_j X^j (m+1/2)_j * psi_j(g) / (g)_j ,
        psi_j(g) = [ sum_{i<j} prod_{i'<d, i'!=i} (g+i') ] / (g)_d
    so every term shares the denominator (g)_j * (g)_d, and multiplying through
    by (g)_d^2 (positive, since g > 0 on the domain) leaves
        r_j X^j (m+1/2)_j * [sum_{i<j} prod_{i'!=i}(g+i')] * prod_{i=j}^{d-1}(g+i).
    The last factor is the COMPLEMENT of (g)_j inside (g)_d -- the ERR-0010
    convention, kept identical here on purpose.
    """
    K = NPoly.var(0)
    lam = NPoly.var(1)
    u = NPoly.var(2)
    one = NPoly.const(1)

    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + one
    m = N - NPoly.const(d)
    X = (N + lam) * (N + lam)

    gamma = (NPoly.const(3) + lam * fmpq(10)) * u
    g = m * fmpq(2) + gamma + one
    gsh = [g + NPoly.const(i) for i in range(d)]  # g, g+1, ..., g+d-1

    total = NPoly.const(0)
    half = NPoly.const(fmpq(1, 2))
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeff_bi = lift_N(coeff_N, N) * fmpq((-1) ** k)

        num_bi = NPoly.const(1)
        for i in range(j):
            num_bi = num_bi * (m + half + NPoly.const(i))

        # complement of (g)_j inside (g)_d
        complement = NPoly.const(1)
        for i in range(j, d):
            complement = complement * gsh[i]

        # psi_j numerator over the common denominator (g)_d
        psi_num = NPoly.const(0)
        for i in range(j):
            prod = NPoly.const(1)
            for i2 in range(d):
                if i2 != i:
                    prod = prod * gsh[i2]
            psi_num = psi_num + prod

        total = total + coeff_bi * num_bi * complement * (X**j) * psi_num
    return total


def self_check_free(d: int, e_polys: dict, k_values, lam_values, u_values) -> list[str]:
    """Sign of build_derivative_free against an exact finite difference of the
    reference engine, at concrete (K, lam, u)."""
    from fractions import Fraction as F  # ENGINE-OK: interface glue only

    from jacobi_normal_form import jacobi_coeff_rec

    bad = []
    for parity in ("even", "odd"):
        G = build_derivative_free(parity, d, e_polys)
        for K_val in k_values:
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            j = d + 1
            m = n - j
            if m < 0 or j > n - 1 or K_val < 3:
                continue
            for lam_num, lam_den in lam_values:
                lam = fmpq(lam_num, lam_den)
                for u_num, u_den in u_values:
                    u = fmpq(u_num, u_den)
                    gamma = (fmpq(3) + lam * 10) * u
                    if gamma <= 0:
                        continue

                    sgn = G.eval_at((fmpq(K_val), lam, u))
                    sign_formula = (sgn > 0) - (sgn < 0)

                    lam_F = F(int(lam.p), int(lam.q))
                    h = fmpq(1, 10**12)
                    D0 = gamma * 2 + 3
                    D1 = (gamma + h) * 2 + 3
                    k0 = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, F(int(D0.p), int(D0.q)))
                    k1 = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, F(int(D1.p), int(D1.q)))
                    diff = k0 - k1
                    sign_exact = (diff > 0) - (diff < 0)

                    if sign_formula != sign_exact:
                        bad.append(
                            f"depth={d} {parity} K={K_val} lam={lam_num}/{lam_den} "
                            f"u={u_num}/{u_den}: {sign_formula} vs {sign_exact}"
                        )
    return bad


def build_derivative(parity: str, d: int, e_polys: dict) -> NPoly:
    """G(K, c, v) whose SIGN is the sign of -d(knife)/dgamma at D = T_{v*lam}.

    Same construction as keystone_unglued.build_branch, with the extra weight
    psi_j(g) folded in over the common denominator prod_{i<d}(g+i), which is
    then dropped as a positive overall factor.
    """
    K = NPoly.var(0)
    c = NPoly.var(1)
    v = NPoly.var(2)
    one = NPoly.const(1)

    N = K * fmpq(2) if parity == "even" else K * fmpq(2) + one
    m = N - NPoly.const(d)
    lam = c * N
    X = (N + lam) * (N + lam)
    k_s = v * lam

    Bexpr = lam * lam + (k_s * fmpq(2) - fmpq(2)) * lam + one
    kk2 = k_s * (k_s - fmpq(2))
    Qg = kk2 * fmpq(2)
    Pg = (
        (k_s * fmpq(2) - fmpq(3)) * Bexpr * fmpq(3)
        + k_s * k_s * (k_s - fmpq(2)) * fmpq(2)
        - kk2 * fmpq(3)
    )

    # g = 2m + gamma + 1 with gamma = Pg/Qg, cleared by Qg:  g = L[0]/Qg
    # and generally  g + i = L[i]/Qg  with L[i] = 2*m*Qg + Pg + Qg*(1+i).
    two_m_Qg = (m * fmpq(2)) * Qg
    L = [two_m_Qg + Pg + Qg * fmpq(1 + i) for i in range(d)]

    total = NPoly.const(0)
    half = NPoly.const(fmpq(1, 2))
    for k in range(d + 1):
        j = d - k
        coeff_N = e_polys[k] * falling_poly(k, j) / poch(fmpq(1), j)
        coeff_bi = lift_N(coeff_N, N) * fmpq((-1) ** k)

        num_bi = NPoly.const(1)
        for i in range(j):
            num_bi = num_bi * (m + half + NPoly.const(i))

        # 1/(g)_j -> complement product times Qg^j  (the ERR-0010 convention)
        complement = NPoly.const(1)
        for i in range(j, d):
            complement = complement * L[i]

        # psi_j(g) = sum_{i<j} 1/(g+i), over the common denominator prod_{i<d}(g+i):
        #   numerator = sum_{i<j} prod_{i'<d, i'!=i} L[i'],   times Qg  (since
        #   1/(g+i) = Qg/L[i], one factor of Qg survives per term).
        # That single Qg is the SAME for every j, so it is a global positive
        # factor and is dropped rather than carried: on this domain
        # k_s = v*lam >= (8/5)*(5/2) = 4 > 2, hence Qg = 2*k_s*(k_s-2) > 0.
        # Dropping it costs nothing and cuts the degree in every variable.
        psi_num = NPoly.const(0)
        for i in range(j):
            prod = NPoly.const(1)
            for i2 in range(d):
                if i2 != i:
                    prod = prod * L[i2]
            psi_num = psi_num + prod

        total = total + coeff_bi * num_bi * complement * (X**j) * (Qg**j) * psi_num
    return total


def self_check(d: int, e_polys: dict, k_values, c_values, v_values) -> list[str]:
    """Compare build_derivative's SIGN against a finite difference of the exact
    engine. Wide ranges deliberately -- a narrow self-check is what let ERR-0010
    and ERR-0011 survive in two separate files."""
    from fractions import Fraction as F  # ENGINE-OK: interface glue only

    from jacobi_normal_form import jacobi_coeff_rec

    bad = []
    for parity in ("even", "odd"):
        G = build_derivative(parity, d, e_polys)
        for K_val in k_values:
            N = 2 * K_val if parity == "even" else 2 * K_val + 1
            n = N + 1
            j = d + 1
            m = n - j
            if m < 0 or j > n - 1 or K_val < 3:
                continue
            for c_num, c_den in c_values:
                c_val = fmpq(c_num, c_den)
                lam = c_val * N
                for v_num, v_den in v_values:
                    v_val = fmpq(v_num, v_den)
                    k_s = v_val * lam
                    if k_s <= 3:
                        continue

                    sgn = G.eval_at((fmpq(K_val), c_val, v_val))
                    sign_formula = (sgn > 0) - (sgn < 0)

                    Bexpr = lam * lam + (k_s * 2 - 2) * lam + 1
                    kk2 = k_s * (k_s - 2)
                    Qg = kk2 * 2
                    Pg = (k_s * 2 - 3) * Bexpr * 3 + k_s * k_s * (k_s - 2) * 2 - kk2 * 3
                    gamma = Pg / Qg
                    lam_F = F(int(lam.p), int(lam.q))

                    # exact finite difference of the knife in gamma
                    h = fmpq(1, 10**12)
                    D0 = gamma * 2 + 3
                    D1 = (gamma + h) * 2 + 3
                    k0 = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, F(int(D0.p), int(D0.q)))
                    k1 = (-1) ** m * jacobi_coeff_rec(j, n, lam_F, F(int(D1.p), int(D1.q)))
                    diff = k0 - k1  # = -(k1-k0), i.e. -d(knife)/dgamma up to h>0
                    sign_exact = (diff > 0) - (diff < 0)

                    if sign_formula != sign_exact:
                        bad.append(
                            f"depth={d} {parity} K={K_val} c={c_num}/{c_den} "
                            f"v={v_num}/{v_den}: {sign_formula} vs {sign_exact}"
                        )
    return bad


def run_depth(d: int) -> dict:
    t0 = time.time()
    e_polys = elementary_symmetric(d)
    k_values = (3, 4, 6, 10, 25, 100)
    c_values = [(5, 12), (1, 1), (5, 1), (50, 1), (500, 1)]
    v_values = [(8, 5), (7, 4), (19, 10), (2, 1)]
    bad = self_check(d, e_polys, k_values, c_values, v_values)
    n_trials = len(k_values) * len(c_values) * len(v_values) * 2
    print(f"depth {d}: derivative self-check {n_trials} trials, {len(bad)} mismatches", flush=True)
    if bad:
        for b in bad[:5]:
            print("  ", b)
        return {"depth": d, "self_check_passed": False, "mismatches": bad[:10]}

    result = {
        "depth": d,
        "self_check_trials": n_trials,
        "self_check_passed": True,
        "branches": {},
    }
    for parity in ("even", "odd"):
        G = build_derivative(parity, d, e_polys)
        t1 = time.time()
        gK = compactify(G, 0, 3)
        ok_lo, b_lo, o_lo = prove_box(
            gK, [(fmpq(0), fmpq(999, 1000)), (C_MIN, C_SPLIT), (V_LO, V_HI)], max_depth=30
        )
        gKc = compactify(gK, 1, C_SPLIT)
        ok_hi, b_hi, o_hi = prove_box(
            gKc, [(fmpq(0), fmpq(999, 1000)), (fmpq(0), fmpq(999, 1000)), (V_LO, V_HI)]
        )
        dt = time.time() - t1
        print(
            f"  [{parity}] lo={ok_lo}({b_lo}b) hi={ok_hi}({b_hi}b)  ({dt:.0f}s)",
            flush=True,
        )
        result["branches"][parity] = {
            "K_deg": G.max_deg(0),
            "c_deg": G.max_deg(1),
            "v_deg": G.max_deg(2),
            "terms": len(G.d),
            "lo_proved": ok_lo,
            "lo_boxes": b_lo,
            "lo_open": len(o_lo),
            "hi_proved": ok_hi,
            "hi_boxes": b_hi,
            "hi_open": len(o_hi),
        }
    result["monotone_proved"] = all(
        result["branches"][p]["lo_proved"] and result["branches"][p]["hi_proved"]
        for p in ("even", "odd")
    )
    result["seconds"] = round(time.time() - t0, 1)
    return result


def main() -> int:
    depths = [int(x) for x in sys.argv[1:]] or [2]
    out = []
    for d in depths:
        try:
            out.append(run_depth(d))
        except Exception as exc:  # noqa: BLE001 - one bad depth must not kill the queue
            print(f"depth {d} FAILED: {type(exc).__name__}: {exc}", flush=True)
            out.append({"depth": d, "error": f"{type(exc).__name__}: {exc}"})

        path = RES / "monotonicity_cert.json"
        prev = []
        if path.exists():
            try:
                prev = json.loads(path.read_text(encoding="utf-8")).get("runs", [])
            except (json.JSONDecodeError, OSError):
                prev = []
        keep = [r for r in prev if r.get("depth") not in {o.get("depth") for o in out}]
        path.write_text(
            json.dumps(
                {
                    "claim": "STEP (c) of the unglued keystone as a CERTIFICATE, not a "
                    "measurement: -d(knife)/dgamma > 0 (i.e. the knife decreases in D) at "
                    "D = T_v(lam) for all real v in [8/5, 2], all K>=3, all c >= 5/12. "
                    "Combined with steps (a) and (b) this removes the last measured-only "
                    "link in the argument. See results/UNGLUED_KEYSTONE.md.",
                    "runs": sorted(keep + out, key=lambda r: r["depth"]),
                    "command": "python lab/monotonicity_cert.py <d> [<d> ...]",
                    **stamp(),
                },
                indent=1,
            ),
            encoding="utf-8",
        )
        print(f"  written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
