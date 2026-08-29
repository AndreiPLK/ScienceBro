"""g is not a mystery constant: it is the Edgeworth term, written out.

`FINITE_N_BRIDGE.md` left one gap -- an effective expansion

    M_{n,t} = f(theta) + g(theta)/n + O(1/n^2)

with explicit remainder. `POISSON_BINOMIAL_VIEW.md` decoded `f` as the reciprocal
tilted variance of a Bernoulli sum. This file does the same for `g`.

Saddle point for the coefficient of a product generating function: with
`K(L) = SUM log(1 + b_i e^L)` and `K'(L_t) = t`,

    log e_t = K(L_t) - t L_t - (1/2) log(2 pi K'') + ...

`log rho_t = -Delta^2_t log e_t`, and since `dL/dt = 1/K''`, every `t`-derivative is
`(1/K'') d/dL`. Collecting everything of order `1/n^2` and no smaller:

    log rho = 1/K'' + (1/2) K''''/K''^3 - K'''^2/K''^4,
    rho - 1  = log rho + (1/2)(log rho)^2.

The terms from the fourth `t`-derivative are `O(1/n^3)` and are correctly absent.

The test is a rate, not an eyeball: if the expansion is right, the residual against
the EXACT `rho` must fall like `1/n^3`, while the Gaussian term `1/K''` alone must
leave an `O(1/n^2)` error. Both are checked by multiplying by the corresponding
power of `n` and looking for a flat column.

Cumulants come from the tilted Bernoulli weights `w_i = b_i e^L/(1 + b_i e^L)`:

    K'' = SUM w(1-w),  K''' = SUM w(1-w)(1-2w),  K'''' = SUM w(1-w)(1-6w+6w^2).

`rho` itself is exact (fmpq); the saddle point is transcendental, so the comparison
runs at 40 digits and is a measurement, not a certificate.

Run: python lab/edgeworth_prediction.py -> results/edgeworth_prediction.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq
from mpmath import exp, findroot, mp, mpf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
mp.dps = 40


def cumulants(b: list, t: int):
    """K'', K''', K'''' at the tilt whose mean is t."""

    def mean(L):
        return sum(x * exp(L) / (1 + x * exp(L)) for x in b) - t

    L = findroot(mean, (mpf(-60), mpf(60)), solver="bisect", tol=mpf(10) ** -30)
    w = [x * exp(L) / (1 + x * exp(L)) for x in b]
    return (
        sum(u * (1 - u) for u in w),
        sum(u * (1 - u) * (1 - 2 * u) for u in w),
        sum(u * (1 - u) * (1 - 6 * u + 6 * u * u) for u in w),
    )


def exact_rho_minus_1(n: int, t: int) -> mpf:
    E = E2_list(n, t + 1)
    r = fmpq(E[t], 1) ** 2 / (fmpq(E[t - 1], 1) * fmpq(E[t + 1], 1)) - 1
    return mpf(int(r.numer())) / int(r.denom())


def main() -> int:
    t0 = time.time()
    rows = []
    for n in (41, 61, 81, 121, 161, 201):
        b = [mpf((n - 2 * k) ** 2) for k in range(1, n)]
        for frac in (0.2, 0.35, 0.45):
            t = max(2, round(frac * (n - 1)))
            exact = exact_rho_minus_1(n, t)
            K2, K3, K4 = cumulants(b, t)
            gauss = 1 / K2
            lr = 1 / K2 + K4 / (2 * K2**3) - K3**2 / K2**4
            edge = lr + lr * lr / 2
            rows.append(
                {
                    "n": n,
                    "t": t,
                    "theta": round(t / (n - 1), 4),
                    "rho_minus_1_exact": float(exact),
                    "gaussian_error_times_n2": float((exact - gauss) * n**2),
                    "edgeworth_error_times_n3": float((exact - edge) * n**3),
                }
            )
            print(
                f"  n={n:<4} t={t:<4} theta={t / (n - 1):.2f}   "
                f"gaussian err x n^2 = {float((exact - gauss) * n**2):9.4f}   "
                f"edgeworth err x n^3 = {float((exact - edge) * n**3):9.4f}"
            )

    # a flat column is the claim; measure its drift rather than asserting flatness
    drift = {}
    for frac in (0.2, 0.35, 0.45):
        col = [r for r in rows if abs(r["theta"] - frac) < 0.03]
        if len(col) >= 2:
            a, b_ = col[0]["edgeworth_error_times_n3"], col[-1]["edgeworth_error_times_n3"]
            g0, g1 = col[0]["gaussian_error_times_n2"], col[-1]["gaussian_error_times_n2"]
            drift[str(frac)] = {
                "edgeworth_first_to_last": [round(a, 4), round(b_, 4)],
                "edgeworth_relative_drift": round(abs(b_ - a) / abs(a), 4),
                "gaussian_first_to_last": [round(g0, 4), round(g1, 4)],
                "gaussian_relative_drift": round(abs(g1 - g0) / abs(g0), 4),
            }

    out = {
        "what": "g identified: the 1/n^2 part of rho - 1 is the Edgeworth term in the tilted "
        "cumulants",
        "formula": "log rho = 1/K'' + K''''/(2 K''^3) - K'''^2/K''^4;  "
        "rho - 1 = log rho + (log rho)^2/2",
        "test": "residual against exact rho must be O(1/n^3); the Gaussian term alone leaves "
        "O(1/n^2). Both columns should be flat after scaling.",
        "rows": rows,
        "flatness": drift,
        "status": "numeric probe at 40 digits against exact rho; a measurement, not a "
        "certificate. The remainder bound is what a proof still owes.",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "edgeworth_prediction.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for k, v in drift.items():
        print(f"  theta~{k}: edgeworth column drifts {v['edgeworth_relative_drift']:.1%} "
              f"over n = 41..201, gaussian {v['gaussian_relative_drift']:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
