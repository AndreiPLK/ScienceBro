"""Gegenbauer coefficients at LARGE N: closed formula instead of basis peeling.

Why. `gegenbauer_flint.to_gegenbauer` builds the whole basis, which is O(deg^2)
STORAGE -- about 9 million rational coefficients at deg 3000. That is what took
the machine from 31 GB to 0.3 GB on 18 August. Peeling is fine to deg ~1600 and
hopeless above it.

The fix is not a faster engine, it is a different algorithm. DLMF 18.18.17 gives
the monomial-to-Gegenbauer connection in closed form,

    (2x)^j = j! SUM_l (gamma + j - 2l)/gamma * C_{j-2l}^gamma(x)
                       / ( (gamma+1)_{j-l} l! )

so the coefficient of C_m^gamma in q = SUM_j q_j v^j is a single sum

    a_m = SUM_{j >= m, j = m (mod 2)} q_j * (j!/2^j) * (gamma+m)/gamma
                                          / ( (gamma+1)_{(j+m)/2} * ((j-m)/2)! )

which needs only the monomial coefficients: O(deg) memory, O(deg) work per
coefficient. And since the negatives live at the LOW end, only a few hundred
coefficients are ever needed, not all of them.

Every value here is checked against the peeling path on sizes where peeling still
runs, before anything at large N is believed.
"""

from __future__ import annotations

import sys
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
import machine_guard  # noqa: E402
from gegenbauer_flint import q_poly, to_gegenbauer  # noqa: E402


def q_monomials(n: int, lam: fmpq) -> list[fmpq]:
    """Monomial coefficients of q, built in the INTEGER root variable.

    q(v) = prod (v - r_k/s) with r_k integers, so s^N q(v) = prod (s v - r_k).
    Building the integer-rooted product first keeps the coefficients integers for
    as long as possible instead of accumulating denominators s^j at every step.
    """
    N = n - 1
    s = lam + (n - 1)
    # roots r_k = N-1-2k over s; build prod (x - r_k) with x = s v
    P = fmpq_poly([1])
    X = fmpq_poly([0, 1])
    for k in range(N):
        P = P * (X - fmpq(N - 1 - 2 * k))
        if k % 256 == 0:
            machine_guard.check(machine_guard.floor_for(N), what=f"building q, root {k}/{N}")
    # substitute x = s v : coefficient j gets s^j, then divide by s^N
    cs = P.coeffs()
    out = []
    for j, c in enumerate(cs):
        out.append(c * s**j / s**N)
    return out


def a_low(n: int, lam: fmpq, gamma: fmpq, m_max: int) -> dict:
    """Coefficients a_m for m = 0..m_max, by the DLMF 18.18.17 connection sum."""
    qs = q_monomials(n, lam)
    deg = len(qs) - 1
    out = {}
    # (gamma+1)_p and p! caches, built once
    poch = [fmpq(1)]
    for p in range(1, deg + 2):
        poch.append(poch[-1] * (gamma + p - 1 + 1))  # (gamma+1)_p
    fact = [fmpq(1)]
    for p in range(1, deg + 2):
        fact.append(fact[-1] * p)
    # j!/2^j cache
    jfac2 = [fmpq(1)]
    for j in range(1, deg + 1):
        jfac2.append(jfac2[-1] * fmpq(j, 2))
    for m in range(m_max + 1):
        tot = fmpq(0)
        j = m
        while j <= deg:
            qj = qs[j]
            if qj != 0:
                # l = (j-m)/2 and j-l = (j+m)/2, so the Pochhammer index is
                # (j+m)/2 exactly -- an off-by-one here was caught by self_check
                # before any large-N number was believed.
                tot += (
                    qj * jfac2[j] * (gamma + m) / gamma / (poch[(j + m) // 2] * fact[(j - m) // 2])
                )
            j += 2
        out[m] = tot
        if m % 32 == 0:
            machine_guard.check(machine_guard.floor_for(deg), what=f"coefficient m={m}")
    return out


def self_check() -> list[str]:
    """The formula path must reproduce the peeling path exactly."""
    bad = []
    for n, lam, g in ((13, fmpq(1), fmpq(4)), (20, fmpq(1, 10), fmpq(6)), (25, fmpq(3), fmpq(11))):
        ref = to_gegenbauer(q_poly(n, lam), g)
        got = a_low(n, lam, g, min(len(ref) - 1, 12))
        for m, v in got.items():
            if v != ref[m]:
                bad.append(f"n={n} lam={lam} gamma={g} m={m}: {v} != {ref[m]}")
    return bad


def main() -> int:
    bad = self_check()
    print("self-check vs the peeling path:", "PASS" if not bad else "FAIL " + "; ".join(bad[:3]))
    if bad:
        return 1
    lam, gamma = fmpq(1, 10), fmpq(6)
    for N, predicted in ((3000, 204),):
        n = N + 1
        print(f"\nN={N}: computing low coefficients ({machine_guard.note('the run')})", flush=True)
        m_max = int(predicted * 1.35)
        a = a_low(n, lam, gamma, m_max)
        neg = [m for m in sorted(a) if a[m] < 0]
        print(f"  negatives among m <= {m_max}: {len(neg)}", flush=True)
        print(f"  LAST NEGATIVE INDEX = {max(neg) if neg else None}", flush=True)
        print(f"  outside prediction, registered before this run = {predicted}", flush=True)
        print(
            "  signs near the transition: "
            + ", ".join(
                f"m={m}:{'-' if a[m] < 0 else '+'}"
                for m in range(predicted - 4, predicted + 7, 2)
                if m in a
            ),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
