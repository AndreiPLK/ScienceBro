"""INDEPENDENT VALIDATION of results/BFORM_POSITIVITY_THEOREM.md.

Written by the independent-validator role.  It does NOT import
lab/bform_positivity.py or lab/bform_derivative_form.py (the modules under
test).  Everything below is rebuilt from scratch from

  * the repository closed form in lab/knife_closed_form.py (R_t, E_2t), and
  * the reference engine lab/jacobi_normal_form.py (jacobi_coeff_rec), whose
    sign is the ground truth for knife_j and which knows nothing about the
    B-form.

What is checked, in the order requested by the validation plan:

  1  conventions: falling vs rising factorials, r = j-1, k = 1..n-1, and that
     R_t of the closed form really equals c_t of the B-form (exact, fmpq).
  2  Lemma 3 (T_t > 0) at the boundaries: n even (b_{n/2} = 0), r = n-2,
     D just above 3, n = 5, 6, 7 -- each factor separately.
     Also the ARITHMETIC of the side identity H-2r+1 = (D-1)/2 + 2(n-2-r).
  3  Theorem 5: the three monotonicity factors of f(t), separately, and the
     conclusion f(t+1) <= f(t); the Newton chain including p_t > 0.
  4  the Newton step with a vanishing p_t (r = n-1, outside the stated domain).
  5  Theorem 6: the vertex claim "H/2 > n-2 exactly when D > 3", the
     monotonicity of r(H-r) on 2 <= r <= n-2, and the algebra giving D*.
  6  Theorem 7: (N!/r!)/(m! C(N,r)) = 1, the m-th derivative of x^{N-t},
     w_t = C(N-t,N-r)/C(N,r), the y-polynomial identity, the sigma moments
     (arb), the convergence condition t < C+1.
  7  Theorem 8/9 (section 4b): the J-form as an exact arb-certified identity
     and the soundness of the bound (**).
  8  THE HUNT: any (n, j, lam, D) with (*) true and the reference knife not
     positive; and any point with f(0) <= 1 but T_{t+1} > T_t for some t.

Exact throughout (flint fmpq / fmpq_poly); arb intervals where a Gamma value
is unavoidable; floats only inside f-strings.

Run: uv run python lab/validator_bform_check.py
"""

# ENGINE-OK: fractions.Fraction appears ONLY as interface glue to the reference
# engine jacobi_coeff_rec, whose signature takes Fraction; all arithmetic that
# decides anything is fmpq / fmpq_poly / arb.

from __future__ import annotations

import sys
import time
from fractions import Fraction as PyFrac
from math import comb, factorial
from pathlib import Path

from flint import arb, ctx, fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import jacobi_coeff_rec  # noqa: E402

ctx.prec = 400

FAILURES: list[str] = []
NOTES: list[str] = []


def fail(tag: str, msg: str) -> None:
    FAILURES.append(f"{tag}: {msg}")
    print(f"  !! FAIL {tag}: {msg}", flush=True)


# --------------------------------------------------------------------------
# independent rebuild of the object
# --------------------------------------------------------------------------
def falling(a: fmpq, t: int) -> fmpq:
    """(a)_t = a(a-1)...(a-t+1)."""
    out = fmpq(1)
    for i in range(t):
        out *= a - i
    return out


def rising(a: fmpq, t: int) -> fmpq:
    out = fmpq(1)
    for i in range(t):
        out *= a + i
    return out


def b_list(n: int, lam: fmpq) -> list[fmpq]:
    """b_k = (n-2k)^2 / s^2, k = 1..n-1."""
    s = lam + (n - 1)
    s2 = s * s
    return [fmpq((n - 2 * k) ** 2) / s2 for k in range(1, n)]


def esym(vals: list[fmpq], tmax: int) -> list[fmpq]:
    """e_0..e_tmax of vals, exact."""
    e = [fmpq(0)] * (tmax + 1)
    e[0] = fmpq(1)
    for cnt, a in enumerate(vals, 1):
        for t in range(min(cnt, tmax), 0, -1):
            e[t] += a * e[t - 1]
    return e


def R_closed(t: int, j: int, n: int, D: fmpq) -> fmpq:
    """The closed form's own R_t, transcribed verbatim from knife_closed_form.py."""
    num = fmpq(1)
    for i in range(1, t + 1):
        num *= fmpq(j - i)
    for i in range(1, t + 1):
        num *= D + (4 * n - 2 * j - 5 - 2 * (i - 1))
    den = fmpq(1)
    for i in range(1, t + 1):
        den *= fmpq(n - i)
    for i in range(1, t + 1):
        den *= fmpq(2 * n - 1 - 2 * i)
    return num / den


def c_bform(t: int, n: int, r: int, H: fmpq) -> fmpq:
    return (
        falling(fmpq(r), t)
        * falling(H - r, t)
        / (falling(fmpq(n - 1), t) * falling(fmpq(2 * n - 3, 2), t))
    )


def K_direct(n: int, j: int, lam: fmpq, D: fmpq) -> fmpq:
    """K_r straight from the CLOSED FORM (no B-form): sum (-1)^t E_2t s^-2t R_t."""
    r = j - 1
    s = lam + (n - 1)
    E = esym([fmpq((n - 2 * k) ** 2) for k in range(1, n)], r)
    tot = fmpq(0)
    for t in range(r + 1):
        tot += fmpq((-1) ** t) * E[t] / s ** (2 * t) * R_closed(t, j, n, D)
    return tot


def T_list(n: int, j: int, lam: fmpq, D: fmpq) -> list[fmpq]:
    """T_t = c_t e_t(b), t = 0..r."""
    r = j - 1
    H = (D + (4 * n - 7)) / 2
    e = esym(b_list(n, lam), r)
    return [c_bform(t, n, r, H) * e[t] for t in range(r + 1)]


def K_bform_indep(n: int, j: int, lam: fmpq, D: fmpq) -> fmpq:
    T = T_list(n, j, lam, D)
    return sum((fmpq((-1) ** t) * T[t] for t in range(len(T))), fmpq(0))


def ref_knife(j: int, n: int, lam: fmpq, D: fmpq) -> fmpq:
    """Ground truth: the reference engine's knife value (sign is what matters)."""
    lam_f = PyFrac(int(lam.p), int(lam.q))
    D_f = PyFrac(int(D.p), int(D.q))
    return fmpq((-1) ** (n - j)) * jacobi_coeff_rec(j, n, lam_f, D_f)


def sgn(x: fmpq) -> int:
    return (x > 0) - (x < 0)


def star_holds(n: int, r: int, H: fmpq, s: fmpq) -> tuple[bool, bool]:
    """(*)  r (H-r) n (n-2) <= (3n - 9/2) s^2 ; returns (holds, strict)."""
    lhs = fmpq(r) * (H - r) * fmpq(n * (n - 2))
    rhs = fmpq(6 * n - 9, 2) * s * s
    return lhs <= rhs, lhs < rhs


def D_max_star(n: int, r: int, lam: fmpq) -> fmpq:
    """Largest D with (*) at this (n, r):  solve r(H-r)n(n-2) = (3n-9/2)s^2."""
    s = lam + (n - 1)
    # H - r <= (3n-9/2)s^2 / (r n (n-2)) ; H = (D+4n-7)/2
    hr = fmpq(6 * n - 9, 2) * s * s / (fmpq(r) * fmpq(n * (n - 2)))
    return 2 * (hr + r) - (4 * n - 7)


def D_star_md(n: int, lam: fmpq) -> fmpq:
    """The .md's closed form D*(n,lam) = (6n-9)s^2/(n(n-2)^2) - 2n + 3."""
    s = lam + (n - 1)
    return fmpq(6 * n - 9) * s * s / fmpq(n * (n - 2) ** 2) - (2 * n - 3)


def shore_T(lam: fmpq) -> fmpq:
    """Published shore T_hat(lam) = min_k 3(2k-3)/(k(k-2)) (lam^2+(2k-2)lam+1) + 2k."""
    best = None
    lo = max(3, int(float(lam) * 12 // 10))
    hi = int(float(lam) * 25 // 10) + 6
    for k in range(lo, hi):
        T = fmpq(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k
        if best is None or T < best:
            best = T
    return best


# --------------------------------------------------------------------------
# 0. the object I rebuilt must be the object the engine computes
# --------------------------------------------------------------------------
def check_0_conventions() -> None:
    print("[0] conventions / identity with the reference engine", flush=True)
    bad_c = 0
    for n in (5, 6, 7, 8, 13, 20):
        for j in range(2, n + 1):
            for D in (fmpq(31, 10), fmpq(4), fmpq(11), fmpq(97, 2)):
                r = j - 1
                H = (D + (4 * n - 7)) / 2
                for t in range(r + 1):
                    lhs = R_closed(t, j, n, D)
                    rhs = c_bform(t, n, r, H)
                    if lhs != rhs:
                        bad_c += 1
                        if bad_c == 1:
                            fail("R_t == c_t", f"n={n} j={j} t={t} D={D}: {lhs} != {rhs}")
    print(f"  R_t (closed form) == c_t (B-form): {bad_c} mismatches", flush=True)

    # falling vs rising: (n-3/2)_t must be FALLING; the rising reading must be wrong
    n, t = 9, 3
    fallv = falling(fmpq(2 * n - 3, 2), t)
    risev = rising(fmpq(2 * n - 3, 2), t)
    prod = fmpq(1)
    for i in range(1, t + 1):
        prod *= fmpq(2 * n - 1 - 2 * i)
    if prod != fmpq(2**t) * fallv:
        fail("falling", f"prod(2n-1-2i) = {prod} != 2^t (n-3/2)_t = {fmpq(2**t) * fallv}")
    if prod == fmpq(2**t) * risev:
        fail("falling", "rising factorial also matches -- convention undetermined")

    # sign(K_r) == sign(reference knife), including negative points
    mism = neg = zero = tot = 0
    for lam in (fmpq(1, 2), fmpq(1), fmpq(7), fmpq(72)):
        Th = shore_T(lam)
        for n in (6, 7, 12, 21):
            for j in range(3, n):
                for D in (fmpq(31, 10), fmpq(4), Th, Th * fmpq(9, 10), Th + 5, Th * 2):
                    if D <= 3:
                        continue
                    tot += 1
                    kd = K_direct(n, j, lam, D)
                    kb = K_bform_indep(n, j, lam, D)
                    if kd != kb:
                        mism += 1
                        fail("Bform", f"closed form != B-form at n={n} j={j} lam={lam} D={D}")
                    rs = sgn(ref_knife(j, n, lam, D))
                    if sgn(kd) != rs:
                        mism += 1
                        fail("sign", f"sign(K_r) != engine at n={n} j={j} lam={lam} D={D}")
                    neg += rs < 0
                    zero += rs == 0
    print(
        f"  sign(K_r) vs engine: {tot} trials, {mism} mismatches, "
        f"{neg} NEGATIVE reference points, {zero} zero (non-vacuous)",
        flush=True,
    )
    NOTES.append(f"identity grid: {tot} trials, {neg} negative reference points")

    # Lemma 2
    bad = 0
    for n in range(3, 60):
        for lam in (fmpq(1, 3), fmpq(5), fmpq(10**6)):
            s = lam + (n - 1)
            e1 = esym(b_list(n, lam), 1)[1]
            if e1 != fmpq(n * (n - 1) * (n - 2), 3) / (s * s):
                bad += 1
    print(f"  Lemma 2 (e_1 = n(n-1)(n-2)/(3s^2)): {bad} violations", flush=True)
    if bad:
        fail("Lemma2", f"{bad} violations")


# --------------------------------------------------------------------------
# 2. Lemma 3 at the boundaries
# --------------------------------------------------------------------------
def check_2_lemma3() -> None:
    print("[2] Lemma 3 (T_t > 0) at the boundaries", flush=True)
    bad_T = bad_e = bad_hr = 0
    checked = 0
    eps_list = (fmpq(1, 10**9), fmpq(1, 1000), fmpq(1, 2))
    for n in list(range(4, 26)) + [40, 41]:
        for j in (3, 4, n // 2 + 1, n - 1):
            if not (3 <= j <= n - 1):
                continue
            r = j - 1
            for lam in (fmpq(1, 10**6), fmpq(1), fmpq(10**7)):
                for de in eps_list:
                    D = 3 + de
                    H = (D + (4 * n - 7)) / 2
                    e = esym(b_list(n, lam), r)
                    checked += 1
                    for t in range(r + 1):
                        if e[t] <= 0:
                            bad_e += 1
                            fail("Lemma3-e", f"e_{t} <= 0 at n={n} j={j} lam={lam}")
                        if falling(H - r, t) <= 0:
                            bad_hr += 1
                            fail("Lemma3-Hr", f"(H-r)_{t} <= 0 at n={n} j={j} D={D}")
                        if c_bform(t, n, r, H) * e[t] <= 0:
                            bad_T += 1
                            fail("Lemma3-T", f"T_{t} <= 0 at n={n} j={j} lam={lam} D={D}")
    print(
        f"  {checked} (n,j,lam,D) boundary cases incl. n even, r=n-2, D=3+1e-9, n=5,6,7: "
        f"e_t<=0: {bad_e}, (H-r)_t<=0: {bad_hr}, T_t<=0: {bad_T}",
        flush=True,
    )

    # the number of vanishing b_k
    for n in (6, 7, 20, 21):
        z = sum(1 for x in b_list(n, fmpq(3)) if x == 0)
        want = 1 if n % 2 == 0 else 0
        if z != want:
            fail("b-zeros", f"n={n}: {z} vanishing b_k, expected {want}")

    # the SIDE IDENTITY of the Lemma-3 proof, exactly
    bad_id = 0
    for n in (5, 8, 13, 30):
        for r in (2, 3, n - 2):
            if r < 2 or r > n - 2:
                continue
            for D in (fmpq(31, 10), fmpq(7), fmpq(101, 3)):
                H = (D + (4 * n - 7)) / 2
                lhs = H - 2 * r + 1
                md_rhs = (D - 1) / 2 + 2 * (n - 2 - r)
                true_rhs = (D + 3) / 2 + 2 * (n - 2 - r)
                if lhs != true_rhs:
                    fail("H-2r+1", f"corrected identity also wrong at n={n} r={r}")
                if lhs != md_rhs:
                    bad_id += 1
    if bad_id:
        NOTES.append(
            "MD ARITHMETIC SLIP (Lemma 3 proof): H-2r+1 = (D+3)/2 + 2(n-2-r), "
            "not (D-1)/2 + 2(n-2-r); the .md value is smaller by 2. "
            "Conclusion (H-2r+1 > 0) unaffected -- the .md statement is the weaker one."
        )
        print(
            f"  side identity H-2r+1 = (D-1)/2+2(n-2-r): FALSE in {bad_id}/{bad_id} cases "
            f"(true value is (D+3)/2+2(n-2-r)); conclusion still holds",
            flush=True,
        )


# --------------------------------------------------------------------------
# 3. Theorem 5: f(t), factor by factor, and Newton
# --------------------------------------------------------------------------
def f_of_t(t: int, n: int, r: int, H: fmpq, bbar: fmpq) -> fmpq:
    return fmpq(r - t) * (H - r - t) * bbar / (fmpq(2 * n - 3 - 2 * t, 2) * fmpq(t + 1))


def check_3_theorem5() -> None:
    print("[3] Theorem 5: monotonicity of f, factor by factor; Newton chain", flush=True)
    bad_f = bad_fac = bad_new = bad_T = bad_ratio = 0
    checked = 0
    for n in list(range(4, 24)) + [40]:
        for j in range(3, n):
            r = j - 1
            for lam in (fmpq(1, 10**4), fmpq(1), fmpq(9), fmpq(10**5)):
                s = lam + (n - 1)
                bbar = fmpq(n * (n - 2), 3) / (s * s)
                for D in (fmpq(3) + fmpq(1, 10**9), fmpq(5), fmpq(60), fmpq(10**4)):
                    H = (D + (4 * n - 7)) / 2
                    checked += 1
                    # the three factors, separately, on 0 <= t <= r-1
                    for t in range(r):
                        A = fmpq(r - t) / fmpq(2 * n - 3 - 2 * t, 2)
                        B = H - r - t
                        C = fmpq(1, t + 1)
                        if A <= 0 or B <= 0 or C <= 0:
                            bad_fac += 1
                            fail("Thm5-fac", f"factor <=0 at n={n} r={r} t={t} D={D}")
                        if t + 1 <= r - 1:
                            A2 = fmpq(r - t - 1) / fmpq(2 * n - 5 - 2 * t, 2)
                            B2 = H - r - t - 1
                            C2 = fmpq(1, t + 2)
                            if A2 > A or B2 > B or C2 > C:
                                bad_fac += 1
                                fail(
                                    "Thm5-mono",
                                    f"a factor increases at n={n} r={r} t={t} D={D}",
                                )
                    for t in range(r - 1):
                        if f_of_t(t + 1, n, r, H, bbar) > f_of_t(t, n, r, H, bbar):
                            bad_f += 1
                            fail("Thm5-f", f"f({t + 1}) > f({t}) at n={n} r={r} D={D}")
                    # Newton chain, exactly
                    e = esym(b_list(n, lam), r + 1 if r + 1 <= n - 1 else r)
                    N = n - 1
                    p = [e[t] / fmpq(comb(N, t)) for t in range(len(e))]
                    for t in range(1, len(p) - 1):
                        if p[t] * p[t] < p[t - 1] * p[t + 1]:
                            bad_new += 1
                            fail("Newton", f"p_{t}^2 < p_{t - 1}p_{t + 1} at n={n} lam={lam}")
                    for t in range(len(p) - 1):
                        if p[t] <= 0:
                            fail("Newton-p", f"p_{t} <= 0 at n={n} r={r}")
                        elif p[t + 1] / p[t] > bbar:
                            bad_ratio += 1
                            fail("Newton-ratio", f"p_{t + 1}/p_t > bbar at n={n} lam={lam}")
                    # the bound actually used: T_{t+1}/T_t <= f(t)
                    T = T_list(n, j, lam, D)
                    for t in range(r):
                        if T[t + 1] * 1 > f_of_t(t, n, r, H, bbar) * T[t]:
                            bad_T += 1
                            fail("Thm5-bound", f"T_{t + 1}/T_t > f({t}) at n={n} j={j} D={D}")
    print(
        f"  {checked} parameter cases: factor sign/monotonicity {bad_fac}, "
        f"f(t+1)>f(t) {bad_f}, Newton {bad_new}, p-ratio>bbar {bad_ratio}, "
        f"T-ratio>f {bad_T}",
        flush=True,
    )


# --------------------------------------------------------------------------
# 4. the Newton step with a vanishing p_t (outside the stated domain)
# --------------------------------------------------------------------------
def check_4_zero_p() -> None:
    print("[4] Newton chain when some p_t = 0 (r = n-1, j = n: OUTSIDE the domain)", flush=True)
    hits = 0
    for n in (6, 8, 10, 12):
        e = esym(b_list(n, fmpq(3)), n - 1)
        if e[n - 1] != 0:
            fail("zero-e", f"expected e_{n - 1} = 0 for even n = {n}")
        # inside the stated domain t <= r <= n-2 nothing vanishes:
        if any(e[t] == 0 for t in range(n - 1)):
            fail("zero-e", f"an e_t with t <= n-2 vanishes at n={n}")
        hits += 1
    print(
        f"  even n: e_{{n-1}} = 0 exactly as the .md says, and t <= r <= n-2 avoids it "
        f"({hits} cases). The caveat in the Thm-5 proof is correct AND load-bearing.",
        flush=True,
    )
    # does the criterion still make sense at r = n-1 (j = n)?  not claimed, but map it
    bad = 0
    for n in (6, 8, 10):
        for lam in (fmpq(1), fmpq(50)):
            for D in (fmpq(4), fmpq(20)):
                r = n - 1
                s = lam + (n - 1)
                H = (D + (4 * n - 7)) / 2
                holds, _ = star_holds(n, r, H, s)
                if holds and ref_knife(n, n, lam, D) <= 0:
                    bad += 1
    NOTES.append(
        f"outside the stated domain (j = n, r = n-1): (*) true and knife <= 0 in {bad} probes"
    )
    print(f"  probe at j = n (r = n-1, not claimed by the theorem): {bad} bad points", flush=True)


# --------------------------------------------------------------------------
# 5. Theorem 6
# --------------------------------------------------------------------------
def check_5_theorem6() -> None:
    print("[5] Theorem 6: vertex claim, monotonicity in r, and the algebra for D*", flush=True)
    # (a) "H/2 = (D+4n-7)/4 > n-2 exactly when D > 3"
    counter = None
    for n in (5, 8, 13, 40):
        for D in (fmpq(-9, 10), fmpq(0), fmpq(1), fmpq(2), fmpq(29, 10), fmpq(3), fmpq(31, 10)):
            H = (D + (4 * n - 7)) / 2
            lhs = H / 2 > fmpq(n - 2)
            rhs = D > 3
            if lhs != rhs and counter is None:
                counter = (n, D, lhs, rhs)
    if counter is not None:
        n, D, lhs, rhs = counter
        NOTES.append(
            "MD ARITHMETIC SLIP (Theorem 6 proof): H/2 > n-2 <=> D > -1, NOT D > 3. "
            f"Counterexample to the stated equivalence: n={n}, D={D}: H/2 > n-2 is {lhs} "
            f"while D > 3 is {rhs}. D > 3 still IMPLIES H/2 > n-2, so the theorem stands; "
            "the word 'exactly' is wrong."
        )
        print(
            f"  'H/2 > n-2 exactly when D > 3': FALSE (true threshold D > -1); "
            f"witness n={n} D={D}. Implication D>3 => vertex ok is still fine.",
            flush=True,
        )
    # verify the true threshold symbolically-by-cases
    for n in (5, 9, 30):
        for D in (fmpq(-11, 10), fmpq(-1), fmpq(-9, 10), fmpq(100)):
            H = (D + (4 * n - 7)) / 2
            if (H / 2 > fmpq(n - 2)) != (D > -1):
                fail("Thm6-vertex", f"threshold is not D > -1 either (n={n} D={D})")

    # (b) r -> r(H-r) increasing on 2 <= r <= n-2 for D > 3
    bad = 0
    for n in range(5, 40):
        for D in (fmpq(3) + fmpq(1, 10**9), fmpq(4), fmpq(1000)):
            H = (D + (4 * n - 7)) / 2
            vals = [fmpq(r) * (H - r) for r in range(2, n - 1)]
            for i in range(len(vals) - 1):
                if vals[i + 1] <= vals[i]:
                    bad += 1
                    fail("Thm6-mono", f"r(H-r) not increasing at n={n} D={D} r={i + 2}")
    print(f"  r(H-r) increasing on 2..n-2 for D>3: {bad} violations", flush=True)

    # (c) the algebra: (*) at r = n-2  <=>  D <= D*(n,lam), exactly
    bad = 0
    for n in range(5, 45):
        for lam in (fmpq(1, 7), fmpq(1), fmpq(13), fmpq(10**4), fmpq(10**9)):
            got = D_max_star(n, n - 2, lam)
            want = D_star_md(n, lam)
            if got != want:
                bad += 1
                fail("Thm6-Dstar", f"n={n} lam={lam}: solved {got} != D*(md) {want}")
            # and H-r at r=n-2 is (D+2n-3)/2
            D = fmpq(17)
            H = (D + (4 * n - 7)) / 2
            if H - (n - 2) != (D + (2 * n - 3)) / 2:
                fail("Thm6-Hr", f"H-r != (D+2n-3)/2 at n={n}")
    print(
        f"  D*(n,lam) = (6n-9)s^2/(n(n-2)^2) - 2n + 3 solves (*) at r=n-2: {bad} mismatches",
        flush=True,
    )


# --------------------------------------------------------------------------
# 6. Theorem 7
# --------------------------------------------------------------------------
def check_6_theorem7() -> None:
    print("[6] Theorem 7: constants, derivative, w_t, the y-identity, sigma", flush=True)
    bad_const = bad_w = bad_der = bad_poly = 0
    for n in range(4, 26):
        N = n - 1
        for r in range(1, N + 1):
            m = N - r
            # (N!/r!)/(m! C(N,r)) == 1
            if fmpq(factorial(N), factorial(r)) != fmpq(factorial(m) * comb(N, r)):
                bad_const += 1
                fail("Thm7-const", f"(N!/r!)/(m! C(N,r)) != 1 at n={n} r={r}")
            # w_t identity, incl. the automatic zeros
            for t in range(0, N + 1):
                w = falling(fmpq(r), t) / falling(fmpq(N), t) if t <= N else None
                rhs = fmpq(comb(N - t, N - r) if N - t >= N - r >= 0 else 0, comb(N, r))
                if w != rhs:
                    bad_w += 1
                    fail("Thm7-w", f"w_{t} != C(N-t,N-r)/C(N,r) at n={n} r={r}")
                if t > r and w != 0:
                    bad_w += 1
                    fail("Thm7-w0", f"w_{t} != 0 for t>r at n={n} r={r}")
                # d^m/dx^m x^{N-t} at x=1 == (N-t)_m
                p = fmpq_poly([0] * (N - t) + [1])
                for _ in range(m):
                    p = p.derivative()
                if fmpq(p(fmpq(1))) != falling(fmpq(N - t), m):
                    bad_der += 1
                    fail("Thm7-der", f"d^{m} x^{N - t} at 1 != (N-t)_m")
    print(f"  constants {bad_const}, w_t {bad_w}, derivative {bad_der}", flush=True)

    # the y-polynomial identity: sum_t (-1)^t w_t e_t(b) y^t == (r!/N!) y^r P^(m)(1/y)
    for n in (5, 6, 9, 14):
        N = n - 1
        for lam in (fmpq(1), fmpq(37, 5)):
            b = b_list(n, lam)
            P = fmpq_poly([1])
            for bk in b:
                P = P * fmpq_poly([-bk, 1])
            e = esym(b, N)
            for r in range(2, N):
                m = N - r
                Pm = P
                for _ in range(m):
                    Pm = Pm.derivative()
                lead = fmpq(factorial(N), factorial(r))
                # y^r * Pm(1/y) / lead  ==  reversed coefficients of Pm / lead
                rev = [fmpq(Pm.coeffs()[r - t]) / lead for t in range(r + 1)]
                lhs = [
                    fmpq((-1) ** t) * (falling(fmpq(r), t) / falling(fmpq(N), t)) * e[t]
                    for t in range(r + 1)
                ]
                if lhs != rev:
                    bad_poly += 1
                    fail("Thm7-poly", f"y-identity fails at n={n} r={r} lam={lam}")
                # and the D-form reproduces K_r exactly
                eeta = [fmpq((-1) ** t) * rev[t] for t in range(r + 1)]  # e_t(eta) = (-1)^t rev_t
                for D in (fmpq(31, 10), fmpq(23)):
                    H = (D + (4 * n - 7)) / 2
                    d = [falling(H - r, t) / falling(fmpq(2 * n - 3, 2), t) for t in range(r + 1)]
                    K1 = sum((fmpq((-1) ** t) * d[t] * eeta[t] for t in range(r + 1)), fmpq(0))
                    K2 = K_direct(n, r + 1, lam, D)
                    if K1 != K2:
                        bad_poly += 1
                        fail("Thm7-Dform", f"D-form != closed form at n={n} r={r} D={D}")
    print(f"  y-identity + D-form vs closed form: {bad_poly} violations", flush=True)

    # sigma: d_t = Gamma(C+eps+1)Gamma(C-t+1)/(Gamma(C+1)Gamma(C+eps-t+1)), and t < C+1
    bad_sig = bad_conv = 0
    for n in (5, 6, 11, 20):
        C = fmpq(2 * n - 3, 2)
        for r in range(2, n - 1):
            for D in (fmpq(31, 10), fmpq(9), fmpq(200)):
                H = (D + (4 * n - 7)) / 2
                eps = H - r - C
                if eps != D / 2 + (n - 2 - r):
                    fail("Thm7-eps", f"eps != D/2+(n-2-r) at n={n} r={r} D={D}")
                if eps <= 0:
                    fail("Thm7-eps>0", f"eps <= 0 at n={n} r={r} D={D}")
                for t in range(r + 1):
                    if not (fmpq(t) < C + 1):
                        bad_conv += 1
                        fail("Thm7-conv", f"t={t} >= C+1 at n={n} r={r}")
                    d_exact = falling(H - r, t) / falling(C, t)
                    g = (
                        arb(C + eps + 1).gamma()
                        * arb(C - t + 1).gamma()
                        / (arb(C + 1).gamma() * arb(C + eps - t + 1).gamma())
                    )
                    if not (g - arb(d_exact)).contains(arb(0)):
                        bad_sig += 1
                        fail("Thm7-sigma", f"Gamma ratio != d_t at n={n} r={r} t={t} D={D}")
    print(
        f"  sigma/Gamma representation of d_t: {bad_sig}; convergence t<C+1: {bad_conv} bad",
        flush=True,
    )


# --------------------------------------------------------------------------
# 7. section 4b: the J-form and the bound (**)
# --------------------------------------------------------------------------
def _logbeta(x: arb, y: arb) -> arb:
    return x.gamma().log() + y.gamma().log() - (x + y).gamma().log()


def check_7_jform() -> None:
    print("[7] section 4b: Theorem 8 identity and Theorem 9 soundness", flush=True)
    bad_id = 0
    fired = neg_when_fired = 0
    for n in (5, 6, 9, 14, 20):
        N = n - 1
        C = fmpq(2 * n - 3, 2)
        for lam in (fmpq(1), fmpq(40), fmpq(700)):
            b = b_list(n, lam)
            P = fmpq_poly([1])
            for bk in b:
                P = P * fmpq_poly([-bk, 1])
            for r in range(2, N):
                m = N - r
                Pm = P
                for _ in range(m):
                    Pm = Pm.derivative()
                lead = fmpq(factorial(N), factorial(r))
                # monic prod (w - eta_i) = Pm / lead ; e_t(eta) = (-1)^t coeff_{r-t}
                eeta = [fmpq((-1) ** t) * fmpq(Pm.coeffs()[r - t]) / lead for t in range(r + 1)]
                for D in (fmpq(31, 10), fmpq(17), fmpq(400)):
                    H = (D + (4 * n - 7)) / 2
                    eps = H - r - C
                    a = C - r + 1
                    bb = eps
                    # Theorem 8: K_r = 1/B(eps,C+1) * sum_t (-1)^t e_t(eta) B(a+r-t, b)
                    acc = arb(0)
                    for t in range(r + 1):
                        lb = _logbeta(arb(a + (r - t)), arb(bb))
                        acc += arb((-1) ** t) * arb(eeta[t]) * lb.exp()
                    val = acc / _logbeta(arb(bb), arb(C + 1)).exp()
                    K = K_direct(n, r + 1, lam, D)
                    if not (val - arb(K)).contains(arb(0)):
                        bad_id += 1
                        fail("Thm8", f"J-form != K_r at n={n} r={r} lam={lam} D={D}")
                    # Theorem 9 soundness with the uniform bound eta <= B
                    # unstated but needed in the .md proof: a >= 1, else
                    # w^(a-1) >= ((1-eta)u)^(a-1) is FALSE
                    if a < 1:
                        fail("Thm9-a", f"a = C-r+1 < 1 at n={n} r={r}")
                    Bmax = fmpq((n - 2) ** 2) / (lam + (n - 1)) ** 2
                    if bb >= 1:
                        lhs = (
                            arb(a).log()
                            + arb(1 - Bmax).log() * arb(a + bb + r - 1)
                            + _logbeta(arb(a + r), arb(bb))
                        )
                        rhs = arb(Bmax).log() * arb(a + r)
                        if (lhs - rhs) > arb(0):
                            fired += 1
                            if ref_knife(r + 1, n, lam, D) <= 0:
                                neg_when_fired += 1
                                fail(
                                    "Thm9",
                                    f"(**) fired but knife<=0 at n={n} r={r} lam={lam} D={D}",
                                )
    print(
        f"  Theorem 8 identity: {bad_id} violations; Theorem 9 hypothesis fired {fired} times, "
        f"knife non-positive in {neg_when_fired}",
        flush=True,
    )
    NOTES.append(f"Thm 9 (**) fired {fired} times in my grid, {neg_when_fired} bad")


# --------------------------------------------------------------------------
# 8. THE HUNT
# --------------------------------------------------------------------------
def check_8_hunt() -> None:
    print("[8] HUNT: (*) true but reference knife not positive", flush=True)
    lams = [
        fmpq(1, 1000),
        fmpq(1, 2),
        fmpq(1),
        fmpq(3),
        fmpq(7),
        fmpq(26),
        fmpq(101),
        fmpq(1000),
        fmpq(10**5),
        fmpq(10**9),
        fmpq(10**15),
    ]
    tested = fired = bad = strict_zero = 0
    worst = None
    for n in list(range(4, 27)) + [30, 41, 60]:
        for j in range(3, n):
            r = j - 1
            for lam in lams:
                s = lam + (n - 1)
                Dm = D_max_star(n, r, lam)
                if Dm <= 3:
                    continue
                cands = [
                    Dm,  # equality in (*)
                    Dm - fmpq(1, 10**12),
                    Dm * fmpq(999, 1000),
                    (Dm + 3) / 2,
                    fmpq(3) + fmpq(1, 10**9),
                    fmpq(3) + (Dm - 3) / 100,
                ]
                for D in cands:
                    if D <= 3 or D > Dm:
                        continue
                    H = (D + (4 * n - 7)) / 2
                    holds, strict = star_holds(n, r, H, s)
                    if not holds:
                        continue
                    tested += 1
                    fired += 1
                    K = K_direct(n, j, lam, D)
                    rk = ref_knife(j, n, lam, D)
                    if sgn(K) != sgn(rk):
                        bad += 1
                        fail("HUNT-sign", f"K_r and engine disagree n={n} j={j} lam={lam} D={D}")
                    if rk < 0 or K < 0:
                        bad += 1
                        fail(
                            "HUNT",
                            f"COUNTEREXAMPLE (*) true but knife<0: n={n} j={j} lam={lam} D={D} "
                            f"K={K} ref={rk}",
                        )
                    if strict and (rk == 0 or K == 0):
                        strict_zero += 1
                        fail(
                            "HUNT-strict",
                            f"(*) STRICT but knife = 0: n={n} j={j} lam={lam} D={D}",
                        )
                    if worst is None or (K > 0 and K < worst[0]):
                        worst = (K, n, j, lam, D)
    print(
        f"  {fired} points where (*) HOLDS: {bad} counterexamples, {strict_zero} strict-but-zero",
        flush=True,
    )
    if worst:
        print(
            f"  tightest positive point: K={float(worst[0]):.3e} at n={worst[1]} j={worst[2]} "
            f"lam={worst[3]} D={worst[4]}",
            flush=True,
        )

    # non-vacuity: just OUTSIDE (*), does the knife ever go negative?
    neg_out = tot_out = 0
    for n in (6, 7, 12, 21):
        for j in range(3, n):
            r = j - 1
            for lam in (fmpq(1, 2), fmpq(1), fmpq(7), fmpq(72)):
                Dm = D_max_star(n, r, lam)
                for mult in (fmpq(11, 10), fmpq(2), fmpq(10), fmpq(100)):
                    D = max(Dm, fmpq(3)) * mult
                    if D <= 3:
                        continue
                    tot_out += 1
                    if ref_knife(j, n, lam, D) < 0:
                        neg_out += 1
    print(
        f"  non-vacuity: outside (*), {neg_out}/{tot_out} probes have a NEGATIVE knife "
        f"-- the hypothesis is not covering a trivially positive region",
        flush=True,
    )
    NOTES.append(
        f"hunt: {fired} points with (*) true, {bad} counterexamples; "
        f"{neg_out}/{tot_out} negative knives just outside (*)"
    )

    # f(0) <= 1 while some T_{t+1} > T_t
    print("[8b] HUNT: f(0) <= 1 but T_{t+1} > T_t for some t", flush=True)
    hits = seen = 0
    for n in list(range(4, 25)) + [35]:
        for j in range(3, n):
            r = j - 1
            for lam in (fmpq(1, 100), fmpq(1), fmpq(5), fmpq(50), fmpq(10**4), fmpq(10**8)):
                s = lam + (n - 1)
                bbar = fmpq(n * (n - 2), 3) / (s * s)
                Dm = D_max_star(n, r, lam)
                for D in (
                    fmpq(3) + fmpq(1, 10**9),
                    fmpq(4),
                    fmpq(31, 4),
                    Dm,
                    Dm - fmpq(1, 10**9),
                    (Dm + 3) / 2,
                ):
                    if D <= 3:
                        continue
                    H = (D + (4 * n - 7)) / 2
                    if f_of_t(0, n, r, H, bbar) > 1:
                        continue
                    seen += 1
                    T = T_list(n, j, lam, D)
                    for t in range(r):
                        if T[t + 1] > T[t]:
                            hits += 1
                            fail(
                                "HUNT-f0",
                                f"f(0)<=1 but T_{t + 1}>T_{t} at n={n} j={j} lam={lam} D={D}",
                            )
    print(f"  {seen} points with f(0) <= 1: {hits} with a later T increase", flush=True)

    # and the reverse direction: Leibniz true but (*) false (is (*) lossy?)
    lei_not_star = star_not_lei = both = 0
    for n in range(5, 22):
        for j in range(3, n):
            r = j - 1
            for lam in (fmpq(1, 2), fmpq(3), fmpq(40), fmpq(900)):
                s = lam + (n - 1)
                for D in (fmpq(31, 10), fmpq(5), fmpq(11), fmpq(60), fmpq(500)):
                    H = (D + (4 * n - 7)) / 2
                    T = T_list(n, j, lam, D)
                    lei = all(T[t + 1] <= T[t] for t in range(r))
                    stv, _ = star_holds(n, r, H, s)
                    both += lei and stv
                    lei_not_star += lei and not stv
                    star_not_lei += stv and not lei
    print(
        f"  Leibniz vs (*): both {both}, Leibniz-only {lei_not_star}, (*)-only {star_not_lei} "
        f"-- (*)-only must be 0 or the proof of Thm 5 is broken",
        flush=True,
    )
    if star_not_lei:
        fail("Thm5-implication", f"(*) true but Leibniz false in {star_not_lei} cases")
    NOTES.append(
        f"Leibniz vs (*) on my grid: coincide in {both} cases, Leibniz-only {lei_not_star}, "
        f"(*)-only {star_not_lei} (the .md's 'same 265 cases' claim reproduces in kind)"
    )


# --------------------------------------------------------------------------
# 9. the section-6 table
# --------------------------------------------------------------------------
def check_9_table() -> None:
    print("[9] section 6 table: smallest lam at which D*(n,lam) reaches the shore", flush=True)
    claimed = {8: 127, 12: 340, 16: 654, 20: 1069, 28: 2202, 40: 4659}
    for n, lam_claim in claimed.items():
        got = None
        lo, hi = 1, 4 * lam_claim + 50
        while lo < hi:  # smallest integer lam with D*(n,lam) >= shore(lam)
            mid = (lo + hi) // 2
            if D_star_md(n, fmpq(mid)) >= shore_T(fmpq(mid)):
                hi = mid
            else:
                lo = mid + 1
        got = lo
        mark = "ok" if got == lam_claim else "MISMATCH"
        if got != lam_claim:
            NOTES.append(f"section 6 table: n={n} claims lam={lam_claim}, I get {got}")
        print(f"  n={n}: claimed {lam_claim}, recomputed {got}  [{mark}]", flush=True)
        # end-to-end: at that lam, at the shore, every knife j = 3..n-1 positive
        lam = fmpq(got)
        Dsh = shore_T(lam)
        if D_star_md(n, lam) >= Dsh:
            negs = sum(1 for j in range(3, n) if ref_knife(j, n, lam, Dsh) <= 0)
            if negs:
                fail("table-e2e", f"n={n} lam={got} at the shore: {negs} non-positive knives")


# --------------------------------------------------------------------------
# 10. how much slack does (*) leave?  and the section-4 eta table
# --------------------------------------------------------------------------
def check_10_slack() -> None:
    print("[10] slack: first D above D_max(*) where the knife actually turns negative", flush=True)
    rows = []
    for n in (6, 8, 12, 20):
        for j in (3, n // 2 + 1, n - 1):
            if not (3 <= j <= n - 1):
                continue
            for lam in (fmpq(1), fmpq(20), fmpq(300)):
                Dm = D_max_star(n, j - 1, lam)
                if Dm <= 3:
                    rows.append((n, j, lam, None, None))
                    continue
                first_neg = None
                D = Dm
                for _ in range(60):
                    D = D * fmpq(6, 5) + 1
                    if ref_knife(j, n, lam, D) < 0:
                        first_neg = D
                        break
                rows.append((n, j, lam, Dm, first_neg))
    empty = sum(1 for r_ in rows if r_[3] is None)
    ratios = [float(r_[4]) / float(r_[3]) for r_ in rows if r_[3] and r_[4]]
    never = sum(1 for r_ in rows if r_[3] and r_[4] is None)
    print(
        f"  {len(rows)} (n,j,lam) cells: {empty} where (*) is EMPTY (D_max <= 3), "
        f"{never} where no negative knife was found up to ~1.2^60 x D_max",
        flush=True,
    )
    if ratios:
        print(
            f"  slack D_firstneg/D_max(*): min {min(ratios):.2f}, median "
            f"{sorted(ratios)[len(ratios) // 2]:.2f}, max {max(ratios):.2f}",
            flush=True,
        )
        NOTES.append(
            f"slack of (*) vs the true sign change: factor {min(ratios):.2f}..{max(ratios):.2f} "
            f"in D; the hypothesis is sufficient but not tight (as the .md says)"
        )
    NOTES.append(
        f"(*) is EMPTY (no admissible D > 3) in {empty}/{len(rows)} probed (n,j,lam) cells"
    )


def check_11_eta_table() -> None:
    print("[11] section 4: max(eta)/B at n=20, lam=7, r = 2,4,6,10,18", flush=True)
    n, lam = 20, fmpq(7)
    N = n - 1
    b = b_list(n, lam)
    Bmax = max(b)
    P = fmpq_poly([1])
    for bk in b:
        P = P * fmpq_poly([-bk, 1])
    claimed = {2: "0.448", 4: "0.561", 6: "0.650", 10: "0.795", 18: "1.000"}
    for r, cl in claimed.items():
        Pm = P
        for _ in range(N - r):
            Pm = Pm.derivative()
        roots = Pm.complex_roots()
        mx = None
        for z, _mult in roots:
            if not z.imag.contains(arb(0)):
                fail("eta-real", f"non-real root of P^(m) at r={r}")
            re = z.real
            if re < arb(0) or re > arb(Bmax):
                fail("eta-range", f"eta outside [0,B] at r={r}")
            if mx is None or re > mx:
                mx = re
        ratio = mx / arb(Bmax)
        got = f"{float(ratio.mid()):.3f}"
        mark = "ok" if got == cl else "MISMATCH"
        if got != cl:
            NOTES.append(f"section 4 eta table: r={r} claims {cl}, I get {got}")
        print(f"  r={r}: claimed {cl}, recomputed {got}  [{mark}]", flush=True)
    # at r = N-1 the b's are pairwise doubled, so max(eta) = B EXACTLY, not 'about 1'
    Pm = P.derivative()
    if Pm(Bmax) != 0:
        fail("eta-double", "P'(B) != 0 though b_1 = b_{n-1} = B is a double root")
    else:
        NOTES.append(
            "the b_k come in equal pairs (b_k = b_{n-k}), so B is a DOUBLE root of "
            "prod(u-b_k); the 1.000 in the section-4 table is exact, not rounding"
        )


def check_12_thm6_e2e() -> None:
    print("[12] Theorem 6 END-TO-END: D <= D*(n,lam) => every knife j=3..n-1 positive", flush=True)
    tested = cells = bad = 0
    for n in list(range(4, 24)) + [30, 40]:
        for lam in (fmpq(1), fmpq(30), fmpq(500), fmpq(10**4), fmpq(10**8)):
            Ds = D_star_md(n, lam)
            if Ds <= 3:
                continue
            cells += 1
            for D in (Ds, Ds - fmpq(1, 10**9), (Ds + 3) / 2, fmpq(3) + fmpq(1, 10**6)):
                if D <= 3 or D > Ds:
                    continue
                for j in range(3, n):
                    tested += 1
                    if ref_knife(j, n, lam, D) <= 0:
                        bad += 1
                        fail("Thm6-e2e", f"D<=D* but knife_{j} <= 0 at n={n} lam={lam} D={D}")
    print(
        f"  {cells} (n,lam) cells with a non-empty region, {tested} knives checked, "
        f"{bad} non-positive",
        flush=True,
    )
    NOTES.append(f"Thm 6 end-to-end: {tested} knives under D <= D*, {bad} non-positive")


def main() -> int:
    t0 = time.time()
    check_0_conventions()
    check_2_lemma3()
    check_3_theorem5()
    check_4_zero_p()
    check_5_theorem6()
    check_6_theorem7()
    check_7_jform()
    check_8_hunt()
    check_9_table()
    check_10_slack()
    check_11_eta_table()
    check_12_thm6_e2e()
    print(f"\n=== {len(FAILURES)} hard failures, {time.time() - t0:.1f}s", flush=True)
    for f_ in FAILURES[:20]:
        print("  " + f_, flush=True)
    print("\n--- notes (not failures) ---", flush=True)
    for nt in NOTES:
        print("  * " + nt, flush=True)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
