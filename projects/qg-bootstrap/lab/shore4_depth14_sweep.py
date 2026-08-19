"""Does the FIXED shore level k_s = 4 still work for lam <= 5/2 at depth 14?

Independent sweep, written against the exact reference engine
(`jacobi_normal_form.jacobi_coeff_rec`) directly -- NOT against any Bernstein
construction, and NOT importing keystone_unglued. The only thing borrowed from
keystone_unglued is the mathematical definition of the object, restated here:

    depth d  ->  j = d + 1,  m = n - j,  n = N + 1 (N = 2K or 2K+1, K >= 3)
    T_k(lam) = 3(2k-3)/(k(k-2)) * (lam^2 + (2k-2)lam + 1) + 2k
    knife(d, n, lam, k_s) = (-1)^m * jacobi_coeff_rec(j, n, lam, T_{k_s}(lam))

A "negative knife" is knife < 0. The claim under test: at k_s = 4, for every
lam in (0, 5/2] and every level, the knife is > 0.

Engine: flint fmpq only. Fraction appears solely as the argument type
jacobi_coeff_rec already takes (ENGINE-OK: interface glue, no arithmetic).
No float anywhere in a comparison.

e_doubled_int is memoised (pure function of n, recomputed identically inside
jacobi_coeff_rec on every call otherwise). This changes no value.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction as F  # ENGINE-OK: interface glue only
from functools import lru_cache
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))

import jacobi_normal_form as jnf  # noqa: E402
import knife_proof2 as kp2  # noqa: E402

# memoise the elementary-symmetric table: pure function of n
jnf.e_doubled_int = lru_cache(maxsize=None)(kp2.e_doubled_int)


def shore_D(k_s: fmpq, lam: fmpq) -> fmpq:
    """D = T_{k_s}(lam), exactly (same expression as keystone_unglued.ref_sign)."""
    B = lam * lam + (k_s * 2 - 2) * lam + 1
    kk2 = k_s * (k_s - 2)
    Qg = kk2 * 2
    Pg = (k_s * 2 - 3) * B * 3 + k_s * k_s * (k_s - 2) * 2 - kk2 * 3
    return (Pg / Qg) * 2 + 3


def knife(d: int, n: int, lam: fmpq, k_s: fmpq) -> fmpq:
    j = d + 1
    m = n - j
    D = shore_D(k_s, lam)
    val = jnf.jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
    return val if m % 2 == 0 else -val


def sweep(d: int, k_s: fmpq, lams, ns, stop_after: int = 8):
    """Return (trials, list of negative points, elapsed seconds)."""
    t0 = time.time()
    trials = 0
    negs = []
    j = d + 1
    for n in ns:
        if n - j < 0 or j > n - 1:
            continue
        for lam in lams:
            trials += 1
            v = knife(d, n, lam, k_s)
            if v <= 0:
                negs.append((n, lam, v))
                if len(negs) >= stop_after:
                    return trials, negs, time.time() - t0
    return trials, negs, time.time() - t0


def fmt(negs, limit=6):
    out = []
    for n, lam, v in negs[:limit]:
        sign = "ZERO" if v == 0 else "NEG"
        out.append(f"      n={n} lam={lam} ({float(lam):.4f}) knife={sign}")
    if len(negs) > limit:
        out.append(f"      ... and {len(negs) - limit} more")
    return "\n".join(out)


def cross_validate(d: int) -> tuple[int, int, int]:
    """Second, INDEPENDENTLY-CODED evaluator must agree in sign at depth d.

    `depth3_proof.knife_sign_via_beta_formula` builds the knife from the
    beta-mean form, not from the Jacobi recursion -- the third evaluator used
    to isolate ERR-0010. The ERR-0012 lesson is applied: points where the
    reference is NEGATIVE are included and counted, because a comparison that
    only ever sees +1 proves nothing.

    Returns (trials, mismatches, negative reference values).
    """
    from depth3_proof import elementary_symmetric, knife_sign_via_beta_formula

    e = elementary_symmetric(d)
    trials = bad = negs = 0
    j = d + 1
    for n in (16, 17, 22, 28, 31, 35, 40, 46, 61):
        m = n - j
        if m < 0 or j > n - 1:
            continue
        N = n - 1
        for lam in (fmpq(1, 100), fmpq(1, 2), fmpq(1), fmpq(12, 5), fmpq(5, 2)):
            # Shore levels plus levels KNOWN to drive the depth-14 knife
            # negative (k_s = 8, 12, 20 near lam = 1/100), so the comparison
            # actually sees both signs -- the ERR-0012 lesson.
            for D in (
                shore_D(fmpq(3), lam),
                shore_D(fmpq(4), lam),
                shore_D(fmpq(5), lam),
                shore_D(fmpq(8), lam),
                shore_D(fmpq(12), lam),
                shore_D(fmpq(20), lam),
                fmpq(4),
                fmpq(9, 2),
                fmpq(6),
                fmpq(1000),
            ):
                gamma = (D - 3) / 2
                s_formula = knife_sign_via_beta_formula(N, d, lam, gamma, e)
                v = jnf.jacobi_coeff_rec(j, n, F(int(lam.p), int(lam.q)), F(int(D.p), int(D.q)))
                if m % 2:
                    v = -v
                s_exact = (v > 0) - (v < 0)
                trials += 1
                bad += s_formula != s_exact
                negs += s_exact < 0
    return trials, bad, negs


def main() -> int:
    # ---- lam grid: (0, 5/2], dense, exact rationals -----------------------
    lam_fine = [fmpq(i, 100) for i in range(1, 251)]  # 0.01 .. 2.50 step 0.01
    # extra denominators so the grid is not all /100 (aliasing guard)
    lam_odd = [fmpq(i, 7) for i in range(1, 18)] + [fmpq(i, 13) for i in range(1, 33)]
    lam_tiny = [fmpq(1, q) for q in (1000, 500, 200, 64, 33)]
    lam_all = sorted(set(lam_fine + lam_odd + lam_tiny))

    # ---- levels: n = N+1, N = 2K or 2K+1, K >= 3 --------------------------
    ns_main = list(range(16, 121))
    ns_big = [131, 150, 181, 201, 251, 301, 401]

    print("=" * 74)
    print("CROSS-VALIDATION: depth 14 knife, two independently-coded evaluators")
    print("=" * 74)
    for dd in (2, 14):
        t0 = time.time()
        tr, bad, negs = cross_validate(dd)
        print(
            f"  depth {dd}: {tr} sign comparisons, {bad} mismatches, "
            f"{negs} of them with a NEGATIVE reference  ({time.time() - t0:.1f}s)"
        )
        if negs == 0:
            print("  WARNING: no negative reference values -> this check is near-vacuous")
    print()

    print("=" * 74)
    print("KNOWN-ANSWER BASELINE (negative control): depth 2, k_s = 3, lam ~ 2.4")
    print("  k_s=3 is documented to FAIL there. If it does not fail, the")
    print("  harness is wrong and nothing below can be believed.")
    print("=" * 74)
    lam_24 = [fmpq(i, 100) for i in range(200, 251)]
    tr, ng, dt = sweep(2, fmpq(3), lam_24, list(range(6, 40)), stop_after=10**9)
    print(f"  depth 2, k_s=3: trials={tr}  negatives={len(ng)}  ({dt:.1f}s)")
    print(fmt(ng))
    baseline_ok = len(ng) > 0
    print(f"  BASELINE {'OK (control fires)' if baseline_ok else 'BROKEN (control silent)'}")
    print()

    print("=" * 74)
    print("MAIN: depth 14 (j = 15), k_s = 4, lam in (0, 5/2]")
    print("=" * 74)
    print(f"  lam grid: {len(lam_all)} exact rationals, min={lam_all[0]} max={lam_all[-1]}")
    print(f"  levels:   n = {ns_main[0]}..{ns_main[-1]} plus {ns_big}")
    tr4, ng4, dt4 = sweep(14, fmpq(4), lam_all, ns_main + ns_big, stop_after=10**9)
    print(f"  depth 14, k_s=4: trials={tr4}  negatives={len(ng4)}  ({dt4:.1f}s)")
    if ng4:
        print(fmt(ng4, limit=20))
    print()

    print("=" * 74)
    print("CONTRAST at depth 14: k_s = 3 and k_s = 5 on the same grid")
    print("=" * 74)
    for ks in (3, 5):
        tr_, ng_, dt_ = sweep(14, fmpq(ks), lam_all, ns_main + ns_big, stop_after=10**9)
        print(f"  depth 14, k_s={ks}: trials={tr_}  negatives={len(ng_)}  ({dt_:.1f}s)")
        if ng_:
            print(fmt(ng_, limit=8))
    print()

    print("=" * 74)
    print("DISCRIMINATING POWER at depth 14: k_s that SHOULD fail, on this grid")
    print("  Without this, 'k_s=4 is clean at depth 14' could just mean the")
    print("  depth-14 knife is positive for every k_s and the test is vacuous.")
    print("=" * 74)
    power = {}
    for ks in (8, 12, 20):
        tr_, ng_, dt_ = sweep(14, fmpq(ks), lam_all, ns_main + ns_big, stop_after=3)
        power[ks] = len(ng_)
        print(f"  depth 14, k_s={ks}: {len(ng_)} negatives (stopped early)  ({dt_:.1f}s)")
        print(fmt(ng_, limit=3))
    have_power = any(v > 0 for v in power.values())
    print(f"  DISCRIMINATION {'OK' if have_power else 'ABSENT -> result is vacuous'}")
    print()

    print("=" * 74)
    print(
        f"VERDICT depth 14 k_s=4: {'CLEAN' if not ng4 else 'NEGATIVES_FOUND'}"
        f"  ({tr4} trials, {len(ng4)} negatives)"
    )
    print("=" * 74)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
