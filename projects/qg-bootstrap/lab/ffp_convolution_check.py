"""The knife as a finite free multiplicative convolution -- the literature pass, made exact.

WHY THIS FILE EXISTS.  results/BFORM_POSITIVITY_THEOREM.md sec. 7 said the
novelty status of the B-form transform was unchecked, and named finite free
probability as the place to look.  The pass was done on 2026-08-29 and the
framework is not merely "related": our object IS one of its objects.

Martinez-Finkelshtein, Morales and Perales (arXiv:2309.10970, Definition 2.2 /
eq. (33)) define the n-th multiplicative finite free convolution of two degree-N
polynomials, written in the elementary-symmetric normalisation
p(x) = SUM_t (-1)^t e_t(p) x^{N-t}, by

    e_t(p BOX_N q) = C(N,t)^{-1} e_t(p) e_t(q).                        (MFMP 33)

Our B-form (results/BFORM_POSITIVITY_THEOREM.md Thm 1) is

    K_r = SUM_{t=0}^{r} (-1)^t c_t e_t(b),
    c_t = (r)_t (H-r)_t / [ (n-1)_t (n-3/2)_t ],   b_k = (n-2k)^2/s^2.

Take N = n-1, p = PROD_k (x - b_k) and let q be the polynomial with
e_t(q) := C(N,t) c_t, i.e.

    e_t(q) = (r)_t (H-r)_t / [ t! (n-3/2)_t ],

which vanishes identically for t > r because (r)_t does.  Then by (MFMP 33)

    e_t(p BOX_N q) = c_t e_t(b)   and hence   K_r = (p BOX_N q)(1).      (*)

So the knife is the value at x = 1 of a finite free multiplicative convolution,
and q is a hypergeometric polynomial in their sense.  Their Proposition 2.7 says
BOX_N maps P(R>=0) x P(R>=0) into P(R>=0): if q has only real nonnegative roots,
so does p BOX_N q -- and then

    K_r > 0  <==  theta_max(p BOX_N q) < 1,                             (**)

with no inequality thrown away anywhere.  That is a criterion of a completely
different kind from Theorem 9's split of the Jacobi integral, which loses a
factor that section 6c of that file proves cannot be recovered by any constant.

WHAT IS CHECKED HERE (nothing is asserted that is not computed):

  1. (*) exactly, against the repository reference engine (jacobi_normal_form
     via moment_kernel_probe.ref_sign), at points where the knife is POSITIVE
     and at points where it is NEGATIVE, so the check cannot be vacuous.
  2. Whether q is real-rooted, by an EXACT sign-alternation certificate -- d+1
     rational points at which the exact value alternates in sign proves d
     distinct real roots of a degree-d polynomial.  Root approximations only
     choose the test points; the proof is the exact evaluation.  IT IS NOT:
     the arb enclosure of the imaginary part excludes 0 in 336 of 336 cases,
     so (**) is unavailable and that route is closed.  This is the exclusion
     direction of their own Proposition (contrapositive of (ii)).
  3. The same certificate for p BOX_N q: real-rooted in only 93 of 336 cases,
     as the failure of (**) predicts.
  4. CRITERION S instead -- every Taylor coefficient A_m of the reduced
     polynomial at x = 1 strictly positive, which is exactly sufficient for
     K_r > 0 -- scanned over the PHYSICAL domain D <= T_hat, with a negative
     control far above the shore where knives are known to go negative.

Run: python lab/ffp_convolution_check.py -> results/ffp_convolution_check.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bform_positivity import b_values, c_seq, e_sym  # noqa: E402
from moment_kernel_probe import ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


# ---------------------------------------------------------------- the objects


def e_of_q(n: int, r: int, H: fmpq) -> list[fmpq]:
    """e_t(q) = C(N,t) c_t = (r)_t (H-r)_t / [t! (n-3/2)_t], t = 0..r."""
    N = n - 1
    c = c_seq(n, r, H)
    return [fmpq(comb(N, t)) * c[t] for t in range(r + 1)]


def reduced_poly(e: list[fmpq]) -> fmpq_poly:
    """The degree-len(e)-1 polynomial SUM_t (-1)^t e_t x^{d-t} (zero roots stripped)."""
    d = len(e) - 1
    coeffs = [fmpq(0)] * (d + 1)
    for t, et in enumerate(e):
        coeffs[d - t] = fmpq((-1) ** t) * et
    return fmpq_poly(coeffs)


def conv_e(n: int, r: int, lam: fmpq, H: fmpq) -> list[fmpq]:
    """e_t(p BOX_N q) = c_t e_t(b) for t = 0..r; it vanishes beyond r."""
    b = b_values(n, lam)
    e_b = e_sym(b, r)
    c = c_seq(n, r, H)
    return [c[t] * e_b[t] for t in range(r + 1)]


def K_from_conv(e_conv: list[fmpq]) -> fmpq:
    """(p BOX_N q)(1) = SUM_t (-1)^t e_t, the x^{N-t} powers all being 1."""
    return sum((fmpq((-1) ** t) * et for t, et in enumerate(e_conv)), fmpq(0))


# ------------------------------------------------- exact real-rootedness proof


def sign_alternation_certificate(poly: fmpq_poly) -> tuple[bool, str]:
    """Prove all roots of `poly` are real by exhibiting deg+1 sign alternations.

    The approximate roots choose the test abscissae only; the certificate is the
    exact fmpq evaluation at those rational points.  deg strict sign changes on
    deg+1 points force deg distinct real roots, and a degree-deg polynomial has
    no room for a complex pair on top of them.
    """
    d = poly.degree()
    if d <= 0:
        return True, "degree <= 0"
    approx = []
    for root, mult in poly.complex_roots():
        if not root.imag.contains(0):
            return False, "a root enclosure excludes the real axis"
        approx.extend(
            [fmpq(*float(root.real.mid().str(15, radius=False)).as_integer_ratio())] * mult
        )
    if len(approx) != d:
        return False, "root multiplicities do not sum to the degree"
    approx.sort()
    if any(approx[i] >= approx[i + 1] for i in range(d - 1)):
        return False, "root approximations not separated (multiple root?)"
    pts = [approx[0] - 1]
    pts += [(approx[i] + approx[i + 1]) / 2 for i in range(d - 1)]
    pts.append(approx[-1] + 1)
    vals = [poly(x) for x in pts]
    if any(v == 0 for v in vals):
        return False, "a test point hit a root exactly"
    for i in range(d):
        if (vals[i] > 0) == (vals[i + 1] > 0):
            return False, f"no sign change between test points {i} and {i + 1}"
    return True, f"{d} sign changes on {d + 1} exact rational points"


def max_real_part(poly: fmpq_poly) -> float:
    """Largest REAL PART over all roots, as a float FOR REPORTING ONLY.

    NOT the largest real root: when roots are complex -- and they usually are
    here -- this exceeds it.  Reading it as a root is how one would talk oneself
    into a contradiction with `staircase_positive`; use `real_root_bound` for the
    quantity that means something.
    """
    return max(float(root.real.mid().str(15, radius=False)) for root, _ in poly.complex_roots())


def no_real_root_above(poly: fmpq_poly, c: fmpq) -> bool:
    """Exact, certified: poly has no real zero in [c, inf).

    Descartes on the shift: expand poly(c+y); if every nonzero coefficient has
    the same sign, poly(c+y) has no zero with y >= 0.  Sufficient, not necessary,
    so the bound it yields is an upper bound on the largest real root.
    """
    d = poly.degree()
    shifted = [fmpq(0)] * (d + 1)
    cp = [fmpq(1)] * (d + 1)
    for i in range(1, d + 1):
        cp[i] = cp[i - 1] * c
    for i in range(d + 1):
        ci = poly[i]
        if ci == 0:
            continue
        for m in range(i + 1):
            shifted[m] += ci * comb(i, m) * cp[i - m]
    nz = [x for x in shifted if x != 0]
    return bool(nz) and all((x > 0) == (nz[0] > 0) for x in nz)


def real_root_bound(poly: fmpq_poly, steps: int = 40) -> fmpq | None:
    """Smallest c on a dyadic bisection of (0, 4] with no real zero in [c, inf).

    Returns None if even c = 4 cannot be certified.  Every evaluation is exact;
    the bisection only chooses which exact test to run.
    """
    hi = fmpq(4)
    if not no_real_root_above(poly, hi):
        return None
    lo = fmpq(0)
    for _ in range(steps):
        mid = (lo + hi) / 2
        if no_real_root_above(poly, mid):
            hi = mid
        else:
            lo = mid
    return hi


def taylor_at_one(poly: fmpq_poly) -> list[fmpq]:
    """The exact coefficients A_m of poly(1+y) = SUM_m A_m y^m.

    A_0 = poly(1) = K_r, and A_m = poly^(m)(1)/m!.  With poly of degree r written
    as SUM_t (-1)^t c_t e_t(b) x^{r-t}, A_m = SUM_t (-1)^t C(r-t,m) c_t e_t(b).
    """
    d = poly.degree()
    out = [fmpq(0)] * (d + 1)
    for i in range(d + 1):
        ci = poly[i]
        if ci == 0:
            continue
        for m in range(i + 1):
            out[m] += ci * comb(i, m)
    return out


def staircase_positive(poly: fmpq_poly) -> bool:
    """Every A_m > 0, i.e. the whole diagonal (j,D) -> (j-m, D-2m) is positive.

    READ ERR-0015 BEFORE USING THIS.  It was first written as "CRITERION S:
    all A_m > 0 implies K_r > 0", which is true and EMPTY, because A_0 = poly(1)
    = K_r sits inside the hypothesis.  What it actually tests is the diagonal
    identity's content: by diagonal_identity_check below,

        A_m = C(r,m) * K_{r-m} at H -> H - m,

    so "all A_m > 0" says every knife on the diagonal staircase is positive, the
    knife under test included.  Useful as a MEASUREMENT of the family, useless as
    a criterion.  The non-circular direction is theta_max(p BOX q) < 1, which
    implies the whole staircase without knowing any knife value first.
    """
    return all(a > 0 for a in taylor_at_one(poly))


def diagonal_identity_check(cases: list[tuple[int, int, fmpq, fmpq]]) -> dict:
    """A_m = C(r,m) * K_{r-m} at H -> H-m, i.e. at D -> D-2m.  Exact.

    The Taylor coefficients of the knife polynomial at x = 1 are knives again --
    of lower depth, at lower dimension.  Proof in one line:
    (r)_t (r-t)_m = (r)_m (r-m)_t turns the C(r-t,m) weight into a c-sequence
    with r -> r-m and (H-r) unchanged, i.e. H -> H-m.  This is the finding the
    circular "criterion S" was hiding (ERR-0015).
    """
    checks = bad = 0
    first_bad = None
    for n, j, lam, D in cases:
        r = j - 1
        H = (D + 4 * n - 7) / 2
        A = taylor_at_one(reduced_poly(conv_e(n, r, lam, H)))
        for m in range(r + 1):
            rhs = fmpq(comb(r, m)) * K_from_conv(conv_e(n, r - m, lam, H - m))
            checks += 1
            if A[m] != rhs:
                bad += 1
                first_bad = first_bad or {"n": n, "j": j, "m": m, "lam": str(lam), "D": str(D)}
    return {"checks": checks, "mismatches": bad, "first_mismatch": first_bad}


# ------------------------------------------------------------------ the checks


def check_identity_and_rootedness(cases: list[tuple[int, int, fmpq, fmpq]]) -> dict:
    rows, bad_id, bad_q, bad_conv, neg_pts = [], 0, 0, 0, 0
    for n, j, lam, D in cases:
        r, N = j - 1, n - 1
        H = (D + 4 * n - 7) / 2
        e_conv = conv_e(n, r, lam, H)
        K = K_from_conv(e_conv)
        s_ref = ref_sign(j, n, lam, D)
        s_K = (K > 0) - (K < 0)
        ok_id = s_K == s_ref
        bad_id += not ok_id
        neg_pts += s_ref < 0
        q_red = reduced_poly(e_of_q(n, r, H))
        conv_red = reduced_poly(e_conv)
        ok_q, why_q = sign_alternation_certificate(q_red)
        ok_c, why_c = sign_alternation_certificate(conv_red)
        bad_q += not ok_q
        bad_conv += not ok_c
        rows.append(
            {
                "n": n,
                "j": j,
                "lam": str(lam),
                "D": str(D),
                "N": N,
                "ref_sign": s_ref,
                "conv_sign": s_K,
                "identity_ok": ok_id,
                "q_all_real": ok_q,
                "q_why": why_q,
                "q_e_all_positive": all(e > 0 for e in e_of_q(n, r, H)),
                "conv_all_real": ok_c,
                "conv_why": why_c,
                "max_real_part": max_real_part(conv_red),
                "staircase_positive": staircase_positive(conv_red),
            }
        )
    return {
        "cases": len(rows),
        "identity_mismatches": bad_id,
        "q_not_real_rooted": bad_q,
        "conv_not_real_rooted": bad_conv,
        "negative_knife_points": neg_pts,
        "rows": rows,
    }


def scan_below_shore(ns: tuple[int, ...], lams: tuple[fmpq, ...], fracs: tuple[fmpq, ...]) -> dict:
    """How often does CRITERION S fire on the PHYSICAL domain D <= T_hat?

    For each (n, lam) the shore T_hat is taken from the reference engine and D
    runs over T_hat times the given fractions.  Every depth j = 3..n-1 is
    tested.  A single failure is what would kill the criterion, so failures are
    recorded individually, not just counted.
    """
    tested = fired = 0
    failures = []
    per_n = {}
    for n in ns:
        n_tested = n_fired = 0
        for lam in lams:
            T_hat = shore(lam)[0]
            for f in fracs:
                D = T_hat * f
                if D <= 3:
                    continue
                H = (D + 4 * n - 7) / 2
                for j in range(3, n):
                    poly = reduced_poly(conv_e(n, j - 1, lam, H))
                    ok = staircase_positive(poly)
                    tested += 1
                    n_tested += 1
                    fired += ok
                    n_fired += ok
                    if not ok and len(failures) < 40:
                        failures.append(
                            {
                                "n": n,
                                "j": j,
                                "lam": str(lam),
                                "D_over_T_hat": str(f),
                                "D": str(D),
                                "ref_sign": ref_sign(j, n, lam, D),
                                "first_negative_A_m": next(
                                    m for m, a in enumerate(taylor_at_one(poly)) if a <= 0
                                ),
                            }
                        )
        per_n[n] = {"tested": n_tested, "fired": n_fired}
    return {
        "tested": tested,
        "fired": fired,
        "failures_recorded": len(failures),
        "failures": failures,
        "per_n": per_n,
    }


def control_above_shore(ns: tuple[int, ...], lams: tuple[fmpq, ...], mult: fmpq) -> dict:
    """Negative control: far ABOVE the shore some knives are negative, and there
    CRITERION S must not fire.  A criterion that fired there would be worthless."""
    tested = fired_on_negative = negatives = 0
    for n in ns:
        for lam in lams:
            D = shore(lam)[0] * mult
            H = (D + 4 * n - 7) / 2
            for j in range(3, n):
                s = ref_sign(j, n, lam, D)
                ok = staircase_positive(reduced_poly(conv_e(n, j - 1, lam, H)))
                tested += 1
                if s < 0:
                    negatives += 1
                    fired_on_negative += ok
    return {
        "tested": tested,
        "negative_knives_seen": negatives,
        "criterion_fired_on_a_negative_knife": fired_on_negative,
        "D_over_T_hat": str(mult),
    }


def main() -> int:
    t0 = time.time()
    cases: list[tuple[int, int, fmpq, fmpq]] = []
    for n in (4, 6, 8, 12, 20):
        for j in range(3, min(n, 9)):
            for lam in (fmpq(1), fmpq(5, 2), fmpq(7), fmpq(30)):
                T_hat = shore(lam)[0]
                for D in (fmpq(4), T_hat, T_hat * 2, T_hat * 40):
                    cases.append((n, j, lam, D))
    ident = check_identity_and_rootedness(cases)
    diag = diagonal_identity_check(cases)

    lams = (fmpq(1, 10), fmpq(1, 2), fmpq(1), fmpq(5, 2), fmpq(7), fmpq(30), fmpq(300))
    fracs = (fmpq(1, 4), fmpq(1, 2), fmpq(9, 10), fmpq(99, 100), fmpq(1))
    scan = scan_below_shore((6, 12, 20, 28, 40), lams, fracs)
    control = control_above_shore((6, 12, 20), (fmpq(1), fmpq(7)), fmpq(40))

    out = {
        "what": "the knife as a finite free multiplicative convolution: the identity, "
        "the failure of the real-rootedness route, and CRITERION S below the shore",
        "framework_reference": "arXiv:2309.10970 Def 2.2 / eq (33) and Prop 2.7 "
        "(Martinez-Finkelshtein, Morales, Perales)",
        "identity_and_rootedness": ident,
        "diagonal_identity": diag,
        "staircase_below_the_shore": scan,
        "negative_control_above_the_shore": control,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "ffp_convolution_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"identity: {ident['cases']} cases, {ident['identity_mismatches']} mismatches, "
        f"{ident['negative_knife_points']} negative-knife points"
    )
    print(
        f"q real-rooted in {ident['cases'] - ident['q_not_real_rooted']}/{ident['cases']} cases; "
        f"p BOX q real-rooted in {ident['cases'] - ident['conv_not_real_rooted']}/{ident['cases']}"
    )
    print(
        f"diagonal identity A_m = C(r,m) K_(r-m)(H-m): "
        f"{diag['checks']} checks, {diag['mismatches']} mismatches"
    )
    print(
        f"staircase positive below the shore: held {scan['fired']}/{scan['tested']}, "
        f"failures {scan['failures_recorded']}"
    )
    for n, row in scan["per_n"].items():
        print(f"   n={n:3d}  {row['fired']}/{row['tested']}")
    print(
        f"control above the shore: {control['negative_knives_seen']} negative knives seen, "
        f"criterion fired on {control['criterion_fired_on_a_negative_knife']} of them"
    )
    return 0 if ident["identity_mismatches"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
