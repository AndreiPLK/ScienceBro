"""Named exact families, so a tool call can say what it is about instead of pasting numbers.

Every family returns exact rationals and states its own domain. Adding one here is
cheaper than another ad-hoc script, and it means two tools asked about "the centred
spectrum at n = 41" are guaranteed to be looking at the same object -- which was not
true of the hand-written scripts these replace.
"""

from __future__ import annotations

from math import comb

from flint import fmpq


def esym(vals: list[fmpq]) -> list[fmpq]:
    """Elementary symmetric functions, all of them, by the standard product recursion."""
    acc = [fmpq(1)] + [fmpq(0)] * len(vals)
    for v in vals:
        for q in range(len(vals), 0, -1):
            acc[q] = acc[q] + acc[q - 1] * v
    return acc


def centered_squares(n: int) -> list[fmpq]:
    """The physical spectrum {(n-2k)^2 : k = 1..n-1}. Centred, hence doubled."""
    return [fmpq((n - 2 * k) ** 2) for k in range(1, n)]


def ap_squares(alpha: fmpq, N: int) -> list[fmpq]:
    """{(alpha + k)^2 : k = 0..N-1}. Scale drops out of every ratio, so only alpha matters."""
    return [(alpha + k) ** 2 for k in range(N)]


def deformed_grid(z: fmpq, N: int, odd: bool = True) -> list[fmpq]:
    """The Jacobi-Stirling deformation j^2 -> j(j+z).

    The physical parities sit at z = 0 and z = 1 (the odd branch is governed by
    k(k+1), the even branch by k(k+0)), so this family interpolates through the
    special parameters rather than around them.
    """
    return [fmpq(j) * (fmpq(j) + z) for j in (range(1, N + 1) if odd else range(0, N))]


def normalized_means(b: list[fmpq]) -> list[fmpq]:
    """p_t = e_t(b) / C(N,t), the normalized elementary symmetric means."""
    N = len(b)
    e = esym(b)
    return [e[t] / fmpq(comb(N, t)) for t in range(N + 1)]


def half_spectrum(n: int) -> list[fmpq]:
    """For odd n the centred multiset is a doubled half; this returns that half."""
    if n % 2 == 0:
        m = n // 2
        return [fmpq((2 * j) ** 2) for j in range(1, m)]
    m = (n - 1) // 2
    return [fmpq((2 * j - 1) ** 2) for j in range(1, m + 1)]


FAMILIES = {
    "centered_squares": centered_squares,
    "ap_squares": ap_squares,
    "deformed_grid": deformed_grid,
    "half_spectrum": half_spectrum,
}
