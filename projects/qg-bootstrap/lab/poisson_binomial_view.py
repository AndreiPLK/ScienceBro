"""What f(theta) actually is: the variance of a tilted Poisson-binomial.

Reading Fatehi & Kittaneh (arXiv:1911.12167) for prior art on conjecture (B)
turned up something better than a prior-art answer.  Their Theorem 6 says the
central factorial array is POISSON-BINOMIALLY DISTRIBUTED, and that reading
applies verbatim to our object, because

    SUM_k e_k(b) s^k  =  PROD_i (1 + b_i s)

is the probability generating function of Y = SUM_i Bernoulli(q_i(s)),
q_i(s) = b_i s/(1 + b_i s), up to the constant PROD (1 + b_i s).

Three consequences, and this file checks each one:

1. The raw Newton excess `rho_t = e_t^2/(e_{t-1} e_{t+1})` is TILT-INVARIANT:
   the s^t factors cancel, so rho_t is the log-concavity excess of the pmf at
   ANY tilt.  Exact, holds at finite n.

2. `M_{n,t}` splits exactly as `n(rho_t * beta_t - 1)` with the binomial factor
   `beta_t = t(N-t) / ((t+1)(N-t+1))` fully explicit; and `n(beta_t - 1)` is
   exactly the `-1/theta - 1/(1-theta)` pair that sits in `f`.

3. Therefore the whole content of the limit shape is in `rho`, and for a pmf
   that is nearly Gaussian with variance sigma^2 the excess is ~ 1/sigma^2.  So
   the prediction is

       f(theta) + 1/theta + 1/(1-theta)  =  n / sigma^2(s_t),

   sigma^2(s) = SUM_i b_i s/(1 + b_i s)^2, with s_t the tilt of mean t.

If (3) holds, the opaque `f` is decoded, and the remaining effective expansion
becomes a local-limit statement for a Bernoulli sum -- a subject with an
effective literature, which the current formulation has none of.

Exact parts are fmpq.  The tilt s_t is transcendental, so parts 3 and 4 are
NUMERIC PROBES at 40 digits, and are reported as measurements, not certificates.

Run: python lab/poisson_binomial_view.py -> results/poisson_binomial_view.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq
from mpmath import atan, exp, findroot, mp, mpf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
mp.dps = 40


def bset(n: int) -> list[int]:
    """The multiset {(n-2k)^2 / s^2}; scale drops out of every ratio here, so use (n-2k)^2."""
    return [(n - 2 * k) ** 2 for k in range(1, n)]


def rho(n: int, t: int) -> fmpq:
    E = E2_list(n, t + 1)
    return fmpq(E[t], 1) ** 2 / (fmpq(E[t - 1], 1) * fmpq(E[t + 1], 1))


def beta(n: int, t: int) -> fmpq:
    N = n - 1
    return fmpq(t * (N - t), (t + 1) * (N - t + 1))


def tilt_variance(n: int, t: int):
    """sigma^2 at the tilt whose mean is t, and the tilt itself."""
    b = [mpf(x) for x in bset(n)]
    # the mean is strictly increasing in s from 0 to N, so bracket in log s and bisect
    g = lambda L: sum(x * exp(L) / (1 + x * exp(L)) for x in b) - t  # noqa: E731
    lo, hi = mpf(-40), mpf(40)
    while g(lo) > 0:
        lo -= 40
    while g(hi) < 0:
        hi += 40
    s = exp(findroot(g, (lo, hi), solver="bisect", tol=mpf(10) ** -35))
    return sum(x * s / (1 + x * s) ** 2 for x in b), s


def f_of(theta):
    u = findroot(lambda z: 1 - atan(z) / z - theta, mpf("1.0"))
    dth = atan(u) / u**2 - 1 / (u * (1 + u**2))
    return (2 / u) / dth - 1 / mpf(theta) - 1 / (1 - mpf(theta))


def main() -> int:
    t0 = time.time()

    # (1) + (2): exact identities at finite n
    exact_bad = []
    for n in range(8, 41, 2):
        N = n - 1
        for t in range(2, N - 2):
            E = E2_list(n, t + 2)
            p = [fmpq(E[j], comb(N, j)) for j in (t - 1, t, t + 1)]
            R = p[1] * p[1] / (p[0] * p[2])
            if R != rho(n, t) * beta(n, t):
                exact_bad.append((n, t))
    print(f"(1)+(2) split M = n(rho*beta - 1) exactly: {len(exact_bad)} mismatches")

    # (3) does the tilted variance reproduce f?
    rows = []
    for theta in (0.1, 0.2, 0.3, 0.4, 0.49):
        for n in (100, 200, 400):
            t = round(theta * n)
            s2, _ = tilt_variance(n, t)
            pred = n / s2
            got = f_of(t / n) + 1 / mpf(t / n) + 1 / (1 - mpf(t / n))
            rows.append(
                {
                    "theta": theta,
                    "n": n,
                    "n_over_sigma2": float(pred),
                    "f_plus_binomial_terms": float(got),
                    "relative_gap": float(abs(pred - got) / got),
                    "gap_times_n": float(n * abs(pred - got) / got),
                }
            )
        g = [r["gap_times_n"] for r in rows[-3:]]
        print(f"   theta={theta}: (relative gap) x n at n=100,200,400 -> "
              f"{g[0]:.4f}, {g[1]:.4f}, {g[2]:.4f}")

    # (4) the candidate finite-n inequality:  rho_t - 1  <=  1/sigma^2(s_t)
    ineq = []
    for n in (60, 120, 200):
        for theta in (0.1, 0.25, 0.4, 0.49):
            t = max(2, round(theta * n))
            s2, _ = tilt_variance(n, t)
            lhs = mpf(int((rho(n, t) - 1).numer())) / int((rho(n, t) - 1).denom())
            ineq.append(
                {"n": n, "t": t, "rho_minus_1": float(lhs), "one_over_sigma2": float(1 / s2),
                 "holds": bool(lhs <= 1 / s2)}
            )
    bad = [r for r in ineq if not r["holds"]]
    print(f"(4) candidate rho - 1 <= 1/sigma^2:  {len(bad)} failures of {len(ineq)}")

    out = {
        "what": "the central factorial family is a Poisson-binomial pmf; f(theta) decoded as "
        "n/sigma^2 of the tilted distribution minus the binomial terms",
        "source_of_the_idea": "Fatehi & Kittaneh, arXiv:1911.12167, Theorem 6 (Poisson-binomial); "
        "the tilt reading and everything below are ours",
        "exact_split_mismatches": exact_bad,
        "limit_shape_vs_tilted_variance": rows,
        "candidate_finite_n_inequality": {
            "statement": "rho_t - 1 <= 1/sigma^2(s_t)",
            "rows": ineq,
            "failures": bad,
        },
        "status": "parts 1-2 exact; parts 3-4 numeric probes at 40 digits, NOT certificates",
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "poisson_binomial_view.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
