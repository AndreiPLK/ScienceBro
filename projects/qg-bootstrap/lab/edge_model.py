"""The outside edge model, reimplemented here and tested against OUR exact data.

Their model is stated as parameter-free, and it hit an exact integer at N = 3000
(m = 204, registered before the computation). A hit like that deserves an
independent implementation rather than acceptance: if I can only check their
numbers by asking them for numbers, I am not checking anything.

The model. With alpha = gamma - 1/2, delta = (lam+1)/2, L = log N,
tau = (m+gamma)^2/(N+lam),

    B_K(tau, L) = INT_0^{delta+K} e^{-Lu} u^alpha  0F1(;alpha+1;-tau u) / Gamma(delta-u)  du

and the predicted boundary is the LAST zero in tau, converted back by
m = sqrt(s tau*) - gamma. The truncation at delta+K is theirs and is not a fudge:
the Gamma-ratio approximation that produces the model is not uniform out there,
and they report the root is stable for K = 10..28.

0F1(;alpha+1;-z) = Gamma(alpha+1) z^{-alpha/2} J_alpha(2 sqrt z) is used so the
oscillation is carried by a Bessel function rather than a slowly converging sum.

# ENGINE-OK: this is a numerical ASYMPTOTIC model, not an exact quantity. It is
# only ever compared against exact integers computed elsewhere on flint; nothing
# here decides a sign in a certificate.
"""

from __future__ import annotations

import math
import sys

from mpmath import besselj, mp, mpf, quad, rgamma
from mpmath import gamma as mp_gamma

mp.dps = 30


def _phi(tau: float, u: float, alpha: float) -> float:
    """0F1(;alpha+1;-tau u) via the Bessel form; 1 at u = 0."""
    z = tau * u
    if z <= 0:
        return 1.0
    r = mp_gamma(alpha + 1) * (z ** (-alpha / 2)) * besselj(alpha, 2 * mp.sqrt(z))
    return float(r)


def B(tau: float, L: float, alpha: float, delta: float, K: float = 14.0) -> float:
    """The truncated edge integral."""

    def f(u):
        uu = float(u)
        if uu <= 0:
            return mpf(0)
        # rgamma, not 1/gamma: the reciprocal Gamma is ENTIRE and simply
        # VANISHES at delta-u = 0,-1,-2,..., which is exactly the lobe structure
        # the model is about. 1/gamma raises at those points instead.
        return mpf(_phi(tau, uu, alpha)) * mpf(uu) ** alpha * mp.e ** (-L * uu) * rgamma(delta - uu)

    # split at the poles of 1/Gamma(delta-u): u = delta, delta+1, ... where it vanishes
    pts = [0.0]
    k = 0
    while delta + k < delta + K:
        pts.append(delta + k)
        k += 1
    pts.append(delta + K)
    return float(quad(f, pts))


def last_zero_tau(
    L: float, alpha: float, delta: float, K: float = 14.0, tau_max: float = 400.0, steps: int = 4000
) -> float | None:
    """Largest tau at which B changes sign."""
    prev_t, prev_v = None, None
    last = None
    for i in range(1, steps + 1):
        t = tau_max * i / steps
        v = B(t, L, alpha, delta, K)
        if prev_v is not None and v * prev_v < 0:
            lo, hi = prev_t, t
            for _ in range(60):
                mid = (lo + hi) / 2
                if B(mid, L, alpha, delta, K) * prev_v > 0:
                    lo = mid
                else:
                    hi = mid
            last = (lo + hi) / 2
        prev_t, prev_v = t, v
    return last


def predict_last_negative(N: int, lam: float, gamma_: float, K: float = 14.0) -> dict:
    alpha = gamma_ - 0.5
    delta = (lam + 1) / 2
    L = math.log(N)
    s = N + lam
    tau = last_zero_tau(L, alpha, delta, K)
    if tau is None:
        return {"N": N, "tau_star": None, "m_continuous": None, "m_predicted": None}
    m_cont = math.sqrt(s * tau) - gamma_
    # admissible indices share the parity of N; the boundary is the admissible
    # index immediately left of the continuous root
    m_pred = int(math.floor(m_cont))
    if (m_pred - N) % 2:
        m_pred -= 1
    return {
        "N": N,
        "tau_star": tau,
        "sqrt_tau": math.sqrt(tau),
        "m_continuous": m_cont,
        "m_predicted": m_pred,
    }


# Exact boundaries computed on this side, all in exact rational arithmetic.
EXACT = [
    (199, 0.1, 6.0, 57),
    (399, 0.1, 6.0, 81),
    (799, 0.1, 6.0, 115),
    (1199, 0.1, 6.0, 139),
    (1599, 0.1, 6.0, 157),
    (799, 0.1, 9.0, 173),
    (799, 1.0, 12.0, 163),
    (799, 3.0, 30.0, 281),
    (3000, 0.1, 6.0, 204),
]


def main() -> int:
    print("Independent reimplementation of the outside edge model, against OUR exact data")
    print("      N   lam  gamma   exact m   model m   diff   m/sqrt(N) exact vs model")
    worst = 0
    for N, lam, g, exact in EXACT:
        r = predict_last_negative(N, lam, g)
        mp_ = r["m_predicted"]
        if mp_ is None:
            print(f"  {N:5d} {lam:5} {g:6}   {exact:7d}   no root found")
            continue
        d = mp_ - exact
        worst = max(worst, abs(d))
        print(
            f"  {N:5d} {lam:5} {g:6}   {exact:7d}   {mp_:7d}  {d:+5d}   "
            f"{exact / math.sqrt(N):8.4f} vs {mp_ / math.sqrt(N):.4f}",
            flush=True,
        )
    print(f"\n  worst disagreement: {worst} index units")
    return 0


if __name__ == "__main__":
    sys.exit(main())
