"""Adversarial verification for left-edge-theorem.md (domain-critic attack script).

Run:  python attack_left_edge.py   (from this lab/ directory)
Exit 0  = all attacks failed to break the claims (claims survive machine attack).
Nonzero = counterexample found (details printed).

Written by the domain-critic reviewer 2026-08-13. The reviewer session had no
execution tool, so this script is UNRUN as of the review; running it is a
REQUIRED FIX before promotion.
"""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repro_r4_positivity_spot import a_route1, a_route2, fact, poch  # noqa: E402

FAILS = 0


def fail(msg: str) -> None:
    global FAILS
    FAILS += 1
    print("  COUNTEREXAMPLE / MISMATCH:", msg)


def I_mm(m: int) -> F:
    """Int_{-1}^{1} P_m(x) x^m dx = 2^{m+1} (m!)^2 / (2m+1)!  (exact)."""
    return F(2 ** (m + 1) * fact(m) ** 2, fact(2 * m + 1))


def pref(n: int, r: F, w: F) -> F:
    return (1 + n + r + w) / (poch(F(2) + r, n) * (1 + r + w))


def K1(n: int) -> F:
    """Claim-1 K(n) = (2n-1)/2 * (n/2)^{n-1} * Int P_{n-1} x^{n-1}."""
    return F(2 * n - 1, 2) * F(n, 2) ** (n - 1) * I_mm(n - 1)


def cf_nn1(n: int, r: F, w: F) -> F:
    """Claim 1 closed form at mu0=0 (exact, incl. prefactor sign flips)."""
    return pref(n, r, w) * K1(n) * (n * (r + F(1, 2)) + w)


def cf_nn1_mu0(n: int, r: F, w: F, mu0: F) -> F:
    """Claim 2 closed form: alpha^{n-1} kept SIGNED (valid below threshold too,
    as pure algebra of route 2)."""
    alpha = (F(n) - 3 * mu0) / 2
    return (pref(n, r, w) * F(2 * n - 1, 2) * alpha ** (n - 1) * I_mm(n - 1)
            * (n * (r + (1 + mu0) / 2) + w))


def H_bracket(n: int, r: F, w: F) -> F:
    """Claim 3 sign bracket."""
    return 12 * (2 * n - 1) * (1 + r) * (n * r + 2 * w) + n * (n * n + 5 * n - 2)


def cf_nn2(n: int, r: F, w: F) -> F:
    """Reviewer's full closed form for a_{n,n-2} (mu0=0):
    a = pref * (2n-3)/2 * I(n-2,n-2) * (n/2)^{n-2} * (n-1)/(24(2n-1)) * H."""
    return (pref(n, r, w) * F(2 * n - 3, 2) * I_mm(n - 2) * F(n, 2) ** (n - 2)
            * F(n - 1, 24 * (2 * n - 1)) * H_bracket(n, r, w))


# ---------------- ATTACK 1: claim-1 closed form as exact identity ----------------
# Random + adversarial points, incl. large n, 1+r+w<0 (prefactor flip), and
# r<-2 (outside physical domain: identity must still hold as algebra).

def attack1() -> None:
    print("ATTACK 1: a_{n,n-1} closed form, exact equality vs route 2")
    random.seed(0)
    pts: list[tuple[int, F, F]] = []
    while len(pts) < 30:
        n = random.randint(2, 24)
        r = F(random.randint(-19, 30), 20)
        w = F(random.randint(-30, 36), 20)
        if poch(F(2) + r, n) == 0 or (1 + r + w) == 0:
            continue
        pts.append((n, r, w))
    pts += [
        (40, F(-11, 20), F(1, 2)),   # large n, r < -1/2
        (35, F(-1, 2), F(-1, 4)),    # on the edge, w < 0
        (12, F(-3, 2), F(2)),        # 2+r>0 still, deep-left r
        (15, F(-9, 4), F(3)),        # r < -2: (2+r)_n < 0, outside domain
        (25, F(-13, 25), F(1, 2)),   # the razor point, predicted zero at n=25
        (18, F(1, 5), F(-3, 2)),     # 1+r+w < 0: prefactor sign flip
    ]
    for n, r, w in pts:
        lhs = a_route2(n, n - 1, r, w, F(0))
        rhs = cf_nn1(n, r, w)
        if lhs != rhs:
            fail(f"claim1 n={n} r={r} w={w}: route2={lhs} closed={rhs}")
    print("  done")


# ---------------- ATTACK 2: claim-3 bracket, incl. near-zero-curve razors -------

def attack2() -> None:
    print("ATTACK 2: a_{n,n-2} closed form + sign bracket near its zero curve")
    random.seed(1)
    for n in range(3, 21):
        for _ in range(2):
            r = F(random.randint(-19, 30), 20)
            w = F(random.randint(-30, 36), 20)
            if poch(F(2) + r, n) == 0 or (1 + r + w) == 0:
                continue
            lhs = a_route2(n, n - 2, r, w, F(0))
            rhs = cf_nn2(n, r, w)
            if lhs != rhs:
                fail(f"claim3 n={n} r={r} w={w}: route2={lhs} closed={rhs}")
        # razor: solve H=0 for w at random r, test w0 +/- 1/1000
        r = F(random.randint(-15, 30), 20)
        if (1 + r) == 0:
            continue
        w0 = (F(-n * (n * n + 5 * n - 2), 12 * (2 * n - 1)) / (1 + r) - n * r) / 2
        for eps in (F(1, 1000), F(-1, 1000)):
            w = w0 + eps
            if (2 + r) <= 0 or (1 + r + w) <= 0:
                continue  # outside physical domain, sign law not claimed
            a = a_route2(n, n - 2, r, w, F(0))
            h = H_bracket(n, r, w)
            if (a > 0) != (h > 0) or (a == 0) != (h == 0):
                fail(f"claim3 sign n={n} r={r} w={w}: a={a} bracket={h}")
    print("  done")


# ---------------- ATTACK 3: mu0 != 0 — close the two-route validation gap -------
# The frozen spot checks in repro_r4_positivity_spot.py ONLY ran mu0=0.
# Cross-validate route1 (Eq. A6) vs route2 (residue kinematics) at mu0 != 0,
# including both razor points from the theorem file.

def attack3() -> None:
    print("ATTACK 3: route1 vs route2 at mu0 != 0 (validation gap)")
    cases = [
        (F(3, 5), F(-82, 100), F(2, 5), [19, 20, 21]),
        (F(-3, 5), F(-1, 4), F(3, 4), [14, 15, 16]),
        (F(1, 2), F(1, 4), F(1, 4), [2, 3, 4, 5, 6]),
        (F(1), F(-3, 5), F(1), [4, 5, 6, 7]),
    ]
    for mu0, r, w, ns in cases:
        for n in ns:
            if F(n) + mu0 < 4 * mu0:
                continue  # below threshold: positivity not imposed (paper p.6)
            for ell in range(0, n + 1):
                a1 = a_route1(n, ell, r, w, mu0)
                a2 = a_route2(n, ell, r, w, mu0)
                if (a1 > 0) != (a2 > 0) or (a1 == 0) != (a2 == 0):
                    fail(f"mu0={mu0} n={n} l={ell}: route1={a1} route2={a2}")
            # claim-2 closed form vs route2 on the ladder
            lhs = a_route2(n, n - 1, r, w, mu0)
            rhs = cf_nn1_mu0(n, r, w, mu0)
            if lhs != rhs:
                fail(f"claim2 closed form mu0={mu0} n={n}: {lhs} vs {rhs}")
    # razor zeros from the theorem file, via ROUTE 1 (independent of derivation)
    for mu0, r, w, nzero in [(F(3, 5), F(-82, 100), F(2, 5), 20),
                             (F(-3, 5), F(-1, 4), F(3, 4), 15)]:
        vals = [a_route1(n, n - 1, r, w, mu0) for n in (nzero - 1, nzero, nzero + 1)]
        if not (vals[0] > 0 and vals[1] == 0 and vals[2] < 0):
            fail(f"razor via route1 mu0={mu0}: {vals}")
    print("  done")


# ---------------- ATTACK 4: sign bookkeeping below threshold (alpha < 0) --------

def attack4() -> None:
    print("ATTACK 4: below-threshold alpha<0 — naive sign law must FAIL there")
    mu0 = F(3, 2)  # 3*mu0 = 4.5, threshold n >= 4.5
    r, w = F(1, 10), F(1, 5)
    saw_flip = False
    for n in (2, 3, 4):  # all below threshold, alpha < 0
        a2 = a_route2(n, n - 1, r, w, mu0)
        naive = n * (r + (1 + mu0) / 2) + w  # sign law WITHOUT alpha^{n-1}
        if a2 != cf_nn1_mu0(n, r, w, mu0):
            fail(f"signed closed form wrong below threshold n={n}: {a2}")
        if (a2 > 0) != (naive > 0):
            saw_flip = True  # expected when n-1 odd
    if not saw_flip:
        print("  NOTE: no sign flip observed below threshold at this point; "
              "the n>3mu0 restriction untested here — try other (r,w).")
    print("  done")


# ---------------- ATTACK 5: claim-4 completeness probe (deep-n killers?) --------
# Points passing all n<=5 constraints AND the ladder condition; search n=6..25,
# l<=n-2 for any negative coefficient. Any hit = counterexample to claim 4.

def attack5() -> None:
    print("ATTACK 5: probing claimed island interior/boundary to n=25 (route 1)")
    pts = [
        (F(-49, 100), F(1, 10)),            # just right of the r=-1/2 edge
        (F(-1, 2), F(1, 20)),               # on the edge, w>0 (claimed marginal)
        (F(1, 4), F(-31, 60) + F(1, 200)),  # just inside the a_{2,0}=0 curve
        (F(-2, 5), F(1)),                   # file's own n=50-positive trajectory
        (F(0), F(0)),                       # Veneziano control (must be clean)
    ]
    for r, w in pts:
        if r < F(-1, 2) and w > 0:
            continue
        if r == F(-1, 2) and w < 0:
            continue
        ok5 = all(a_route1(n, ell, r, w, F(0)) >= 0
                  for n in range(1, 6) for ell in range(0, n + 1))
        if not ok5:
            print(f"  ({r},{w}): fails n<=5 constraints -> not in claimed island, skip")
            continue
        for n in range(6, 26):
            for ell in range(0, n - 1):  # l <= n-2 (ladder is analytic)
                if a_route1(n, ell, r, w, F(0)) < 0:
                    fail(f"claim4 counterexample at ({r},{w}): a_{{{n},{ell}}} < 0 "
                         f"but point passes n<=5 + ladder")
    print("  done")


# ---------------- ATTACK 6: the published n<=5 curve strings ---------------------

def attack6() -> None:
    print("ATTACK 6: printed a_{2,0} / a_{3,0} curve formulas vs route 2")
    random.seed(2)
    for _ in range(6):
        r = F(random.randint(-15, 30), 20)
        w = F(random.randint(-30, 36), 20)
        if poch(F(2) + r, 3) == 0 or (1 + r + w) == 0:
            continue
        c20 = 3 * (1 + r) * (r + w) + 1
        c30 = (4 * r ** 3 + 4 * r ** 2 * w + 6 * r ** 2 + 8 * r * w
               + 8 * r + 6 * w + 3)
        for n, curve in ((2, c20), (3, c30)):
            a = a_route2(n, 0, r, w, F(0))
            core = a * poch(F(2) + r, n) * (1 + r + w) / (1 + n + r + w)
            # core must be a positive n-only multiple of the printed curve
            if curve == 0:
                if core != 0:
                    fail(f"curve a_{{{n},0}} zero mismatch at ({r},{w})")
            elif core / curve <= 0:
                fail(f"curve a_{{{n},0}} sign mismatch at ({r},{w}): "
                     f"core={core} curve={curve}")
    print("  done")


def main() -> int:
    attack1()
    attack2()
    attack3()
    attack4()
    attack5()
    attack6()
    print(f"\nVERDICT: {'SURVIVED (no counterexample found)' if FAILS == 0 else f'{FAILS} FAILURES'}")
    return 0 if FAILS == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
