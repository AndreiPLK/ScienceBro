"""N = 10000: product tree for the polynomial, certified ball arithmetic for the signs.

Two bottlenecks appear above N ~ 3000 and each needs a different fix.

BUILDING q. The naive product multiplies in one root at a time: O(N^2) big-integer
work. At N = 10000 that is 1e8 operations on numbers of ~8 kB. A product tree --
split the roots, build each half, multiply the halves -- turns it into
O(M(N) log N) and lets flint use its fast multiplication. The roots are INTEGERS,
so this runs in fmpz_poly with no denominators at all.

SIGNS OF a_m. Exact rationals here carry numerators of tens of thousands of
digits through a sum of thousands of terms. But only the SIGN is needed, and a
sign does not require exactness -- it requires a certificate. Ball arithmetic
gives one: evaluate at high precision, and if the resulting interval excludes
zero, the sign is PROVED. If it does not, raise the precision and repeat. No
float ever decides anything; a ball that straddles zero is reported as undecided,
never guessed.

Verified against the exact rational path before use.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from flint import arb, ctx, fmpq, fmpz_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
import machine_guard  # noqa: E402


def root_product(N: int) -> fmpz_poly:
    """prod_{k=0}^{N-1} (x - (N-1-2k)) by a balanced product tree, integer coefficients."""
    level = [fmpz_poly([-(N - 1 - 2 * k), 1]) for k in range(N)]
    step = 0
    while len(level) > 1:
        machine_guard.check(
            machine_guard.floor_for(N), what=f"tree level {step}, {len(level)} nodes"
        )
        nxt = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(level[i] * level[i + 1])
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
        step += 1
    return level[0]


_CACHE_KEY = None
_CACHE_VAL = None


def _caches(N: int, lam: fmpq, gamma: fmpq, coeffs, prec: int):
    """Per-precision caches: q_j, j!/2^j, (gamma+1)_p, p!. Built once, reused for all m."""
    global _CACHE_KEY, _CACHE_VAL
    key = (N, str(lam), str(gamma), prec)
    if _CACHE_KEY == key:
        return _CACHE_VAL
    S = arb(lam.p + N * lam.q) / arb(lam.q)  # s = lam + N, exactly
    G = arb(gamma.p) / arb(gamma.q)
    inv_s = arb(1) / S
    # q_j = coeffs[j] / s^(N-j); walk j downward so the power is one division per step
    qj = [arb(0)] * (N + 1)
    pw = arb(1)
    for j in range(N, -1, -1):
        qj[j] = arb(int(coeffs[j])) * pw if j < len(coeffs) else arb(0)
        pw = pw * inv_s
    jfac2 = [arb(1)] * (N + 1)
    for j in range(1, N + 1):
        jfac2[j] = jfac2[j - 1] * arb(j) / arb(2)
    poch = [arb(1)] * (N + 2)
    for p in range(1, N + 2):
        poch[p] = poch[p - 1] * (G + p)
    fact = [arb(1)] * (N + 2)
    for p in range(1, N + 2):
        fact[p] = fact[p - 1] * arb(p)
    _CACHE_KEY, _CACHE_VAL = key, (G, qj, jfac2, poch, fact)
    return _CACHE_VAL


def a_low_certified(
    N: int, lam: fmpq, gamma: fmpq, m_max: int, prec: int = 3000, verbose: bool = True
) -> dict:
    """Signs of a_0..a_m_max, each certified by ball arithmetic or reported undecided."""
    t0 = time.time()
    P = root_product(N)
    if verbose:
        print(f"  product tree done, degree {P.degree()} ({time.time() - t0:.0f}s)", flush=True)
    coeffs = P.coeffs()
    s = lam + N

    out: dict[int, tuple[int, str]] = {}
    for m in range(m_max + 1):
        if (m - N) % 2:
            continue  # q has the parity of N; the other indices vanish identically
        decided = False
        p = prec
        while not decided and p <= prec * 8:
            ctx.prec = p
            cache = _caches(N, lam, gamma, coeffs, p)
            G, qj_arb, jfac2, poch, fact = cache
            tot = arb(0)
            # a_m = SUM_j q_j (j!/2^j) (gamma+m)/gamma / ((gamma+1)_{(j+m)/2} ((j-m)/2)!)
            # Every factor comes from a cache built once per precision: no ratio
            # recurrence, so a vanishing coefficient cannot poison the chain.
            for j in range(m, N + 1, 2):
                if coeffs[j] == 0:
                    continue
                tot += qj_arb[j] * jfac2[j] / (poch[(j + m) // 2] * fact[(j - m) // 2])
            tot = tot * (G + m) / G
            if tot > 0:
                out[m] = (1, str(tot)[:26])
                decided = True
            elif tot < 0:
                out[m] = (-1, str(tot)[:26])
                decided = True
            else:
                p *= 2
        if not decided:
            out[m] = (0, "UNDECIDED")
        if verbose and m % 40 == 0:
            print(
                f"  m={m}: sign {out[m][0]:+d}  ({time.time() - t0:.0f}s) {machine_guard.note('')}",
                flush=True,
            )
        machine_guard.check(machine_guard.floor_for(N), what=f"m={m}")
    return out


def main() -> int:
    # cross-check against the exact rational path at a size both can do
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from gegenbauer_bigN import a_low

    print("cross-check vs the exact rational path at N = 200:", flush=True)
    lam, gamma = fmpq(1, 10), fmpq(6)
    exact = a_low(201, lam, gamma, 60)
    cert = a_low_certified(200, lam, gamma, 60, verbose=False)
    bad = [m for m in cert if cert[m][0] != (1 if exact[m] > 0 else -1 if exact[m] < 0 else 0)]
    print("  sign mismatches:", len(bad), "->", "PASS" if not bad else f"FAIL at {bad[:5]}")
    if bad:
        return 1

    N, predicted = 10000, 310
    print(
        f"\nN={N}, registered prediction {predicted}. {machine_guard.note('the run')}", flush=True
    )
    res = a_low_certified(N, lam, gamma, int(predicted * 1.3), prec=4000)
    neg = [m for m in sorted(res) if res[m][0] < 0]
    und = [m for m in sorted(res) if res[m][0] == 0]
    print(f"\n  undecided signs: {len(und)}", flush=True)
    print(f"  LAST NEGATIVE INDEX = {max(neg) if neg else None}", flush=True)
    print(f"  registered prediction  = {predicted}", flush=True)
    print(
        "  around the transition: "
        + ", ".join(
            f"{m}:{'-' if res[m][0] < 0 else '+' if res[m][0] > 0 else '?'}"
            for m in range(predicted - 4, predicted + 7, 2)
            if m in res
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
