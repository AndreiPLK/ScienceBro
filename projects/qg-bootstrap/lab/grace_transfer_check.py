"""Testing the external Grace-Szego transfer bound against our exact engine.

PROVENANCE.  A brief was sent to a second assistant (the founder's parallel chat)
asking for root bounds on p BOX_N q when q is NOT real-rooted.  Its answer
(2026-08-29, PDF in the founder's Downloads, summarised in
results/GRACE_TRANSFER_VERDICT.md) proposes:

  (A)  theta_max(p BOX_N q)  <=  B * max{ Re zeta : q(zeta) = 0 },  B = (n-2)^2/s^2,
       from the CIRCULAR-REGION form of Grace-Szego, which does not need q to be
       real-rooted -- only the rightmost real part of its zeros matters;

  (C)  max Re zeta <= 2/(1-eta),  eta = (H+1)(H-2n+2) / [(H-2r+3)(H-2r+1)],
       from the Jacobi three-term recurrence: Q_r is a nonclassical Jacobi
       polynomial whose Jacobi matrix has A_{k-1}C_k < 0, hence a purely
       imaginary off-diagonal after similarity, hence a Hermitian part that is
       the real diagonal diag(d_k), hence Re y in [min d_k, max d_k];

  (E)  eta < 1 and s^2 > 2(n-2)^2/(1-eta)  ==>  theta_max < 1;

  (U)  s^2 > n(n-2) r (H-r) / [3(n-3/2)]  ==>  theta_max < 1  -- which is
       ALREADY our Theorem 5 condition (*), rederived from the coefficient side.

UNTRUSTED INPUT, so nothing here is assumed.  This file checks (A) and (C)
numerically against the exact engine, and then measures where (E) actually holds
compared with the regions we already have proved (Theorem 6: lam ~> 3n^2,
Theorem 9: lam ~> 32n).

Run: python lab/grace_transfer_check.py -> results/grace_transfer_check.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import ctx, fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ffp_convolution_check import conv_e, e_of_q, no_real_root_above, reduced_poly  # noqa: E402
from moment_kernel_probe import shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
ctx.prec = 250


def eta_value(n: int, r: int, H: fmpq) -> fmpq:
    """eta = (H+1)(H-2n+2) / [(H-2r+3)(H-2r+1)] from the external note."""
    return ((H + 1) * (H - 2 * n + 2)) / ((H - 2 * r + 3) * (H - 2 * r + 1))


def max_re_zero_of_q(n: int, r: int, H: fmpq) -> float:
    """Largest real part among the zeros of the reduced q, as a float (reporting)."""
    q = reduced_poly(e_of_q(n, r, H))
    return max(float(z.real.mid().str(20, radius=False)) for z, _ in q.complex_roots())


def check_A_and_C(cases) -> dict:
    rows, viol_A, viol_C, eta_ge_1 = [], 0, 0, 0
    for n, r, lam, D in cases:
        H = (D + 4 * n - 7) / 2
        B = fmpq((n - 2) ** 2) / ((lam + n - 1) ** 2)
        mre = max_re_zero_of_q(n, r, H)
        eta = eta_value(n, r, H)
        # (A): theta_max <= B * max Re zeta.  Our exact side: the certified
        # statement "no real zero of the composition at or above c".
        bound_A = float(B) * mre
        okA = bound_A <= 0 or no_real_root_above(
            reduced_poly(conv_e(n, r, lam, H)), fmpq(*bound_A.as_integer_ratio())
        )
        viol_A += not okA
        if eta < 1:
            okC = mre <= float(2 / (1 - eta))
            viol_C += not okC
        else:
            okC = None
            eta_ge_1 += 1
        rows.append(
            {
                "n": n,
                "r": r,
                "lam": str(lam),
                "D": str(D),
                "eta": float(eta),
                "max_Re_zero_q": mre,
                "bound_A_on_theta": bound_A,
                "A_consistent": okA,
                "C_holds": okC,
            }
        )
    return {
        "cases": len(rows),
        "A_violations": viol_A,
        "C_violations": viol_C,
        "cases_with_eta_ge_1": eta_ge_1,
        "rows": rows[:60],
    }


def condition_E(n: int, r: int, lam: fmpq, D: fmpq) -> bool:
    H = (D + 4 * n - 7) / 2
    eta = eta_value(n, r, H)
    if eta >= 1:
        return False
    return (lam + n - 1) ** 2 > 2 * fmpq((n - 2) ** 2) / (1 - eta)


def region_of_E(ns, cap: int = 4_000_000) -> list[dict]:
    """Smallest integer lam for which (E) holds at EVERY depth at the shore."""
    out = []
    for n in ns:
        lo, hi = 1, 1
        while hi <= cap:
            lam = fmpq(hi)
            if all(condition_E(n, j - 1, lam, shore(lam)[0]) for j in range(3, n)):
                break
            lo, hi = hi, hi * 2
        if hi > cap:
            out.append({"n": n, "lam_E": None, "thm6_3n2": 3 * n * n, "thm9_32n": 32 * n})
            continue
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            lam = fmpq(mid)
            if all(condition_E(n, j - 1, lam, shore(lam)[0]) for j in range(3, n)):
                hi = mid
            else:
                lo = mid
        out.append(
            {
                "n": n,
                "lam_E": hi,
                "lam_E_over_n": hi / n,
                "lam_E_over_n2": hi / (n * n),
                "thm6_3n2": 3 * n * n,
                "thm9_32n": 32 * n,
            }
        )
        print(
            f"   n={n:4d}: (E) needs lam >= {hi}   (Thm9 needs ~{32 * n}, Thm6 ~{3 * n * n})",
            flush=True,
        )
    return out


def main() -> int:
    t0 = time.time()
    cases = []
    for n in (6, 12, 20, 40):
        for r in (2, n // 2, n - 2):
            for lam in (fmpq(1), fmpq(7), fmpq(30), fmpq(300)):
                T_hat = shore(lam)[0]
                for D in (fmpq(4), T_hat / 2, T_hat):
                    cases.append((n, r, lam, D))
    print("checking (A) and (C) ...", flush=True)
    ac = check_A_and_C(cases)
    print(
        f"   (A) violations {ac['A_violations']}, (C) violations {ac['C_violations']}, "
        f"eta>=1 in {ac['cases_with_eta_ge_1']} of {ac['cases']}",
        flush=True,
    )
    print("measuring the region of (E) at the shore ...", flush=True)
    reg = region_of_E((6, 8, 12, 16, 20, 28, 40, 60))
    out = {
        "what": "verification of the external Grace-Szego transfer bound (A), its Jacobi "
        "spectral-abscissa companion (C), and the region where the resulting condition (E) holds",
        "source": "second-assistant answer, 2026-08-29; UNTRUSTED, hence checked here",
        "A_and_C": ac,
        "region_of_E_at_the_shore": reg,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "grace_transfer_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
