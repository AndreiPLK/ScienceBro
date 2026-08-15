"""Adversarial attack on the gravity-card claims (CHR lambda-family, arXiv:2408.03362).

Written by the domain-critic reviewer. INDEPENDENT implementation: shares no
code with the lab scanners and uses a different exact method (triangular solve
in the Gegenbauer basis C_l^a, a=(D-3)/2), valid for ANY rational D > 3 --
including odd and fractional D, which the weight-integration scanners never
touched.

Claims under attack (gravity-card.md, slices 1-6 corrected):
  C1: a_{n,2n-4} >= 0  <=>  D <= T_n(lam),
      T_n = 3(2n-3)/(n(n-2)) * (lam^2 + (2n-2) lam + 1) + 2n
  C2: VS thresholds D_n(1) = 2(n^2+4n-9)/(n-2), min 23 at n=4
  C3: shore = min_n T_n; lam_min(23) = 1; asymptote D -> (12+4sqrt3) lam
  C4: (conjecture) alive <=> D <= min_n T_n  (no other knives at any (n,l))

Falsification attempts (each independent):
  A0  kinematic substitution check vs paper Eq. (7) residues (razor on the
      t = -mu(n)(1-x)/2 map and the product form)
  A1  random exact points, odd/fractional D included: bracket sign vs direct
      full Gegenbauer projection of a_{n,2n-4}; also leading a_{n,2n-2} > 0
  A2  odd-trajectory vanishing, symbolic in lambda (t<->u symmetry)
  A3  razor zeros at never-tested points: (n=5, lam=7/2) => D* = 271/4 exactly
      (fractional!), (n=6, lam=3) => D* = 57; D* solved from the DIRECT
      projection with D symbolic -- not from the bracket (non-circular)
  A4  full-(n,l) knife hunt inside the claimed alive region (attacks C4),
      plus dead-controls and the D=4 extremal corners (slice-3 re-check)
  A5  symbolic re-derivation of the bracket incl. squared-poly cross terms
      (q_{n-2} == 0 identically; C = 2 q_{n-1} q_{n-3}); threshold == T_n
  A6  envelope: magic point lam_min(23) = 1 (exact, n <= 2000); large-D
      asymptote ratios; spot sign-flip at D = 200 (never scanned)

Run:
  C:/Users/user/ScienceBro/.venv/Scripts/python.exe projects/qg-bootstrap/lab/attack_gravity.py
Exit code 0 = no falsification succeeded; 1 = at least one claim falsified;
2 = script error. Raw verdict lines on stdout; JSON artifact next to results.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

x = sp.symbols("x")
LAM = sp.symbols("lam", positive=True)
DD = sp.symbols("D", positive=True)

RES = Path(__file__).resolve().parents[1] / "results"

FAILURES: list[str] = []
NOTES: list[str] = []


def note(msg: str) -> None:
    print(msg, flush=True)
    NOTES.append(msg)


def fail(msg: str) -> None:
    print("FALSIFIED: " + msg, flush=True)
    FAILURES.append(msg)


# ----------------------------------------------------------------------------
# Core objects (independent implementation)
# ----------------------------------------------------------------------------

def T_frac(n: int, lam: F) -> F:
    """Card slice-6 general law, exact Fractions."""
    return F(3 * (2 * n - 3), n * (n - 2)) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n


def T_sym(n: int, lam):
    return sp.Rational(3 * (2 * n - 3), n * (n - 2)) * (lam**2 + (2 * n - 2) * lam + 1) + 2 * n


def residue_x_coeffs(n: int, lam: F):
    """R(n, t(x)) as a polynomial in x = cos(theta), up to a POSITIVE constant.

    Derivation (independent of lab code): at s = mu(n) = (n+lam-1)/lam with
    massless external states (s+t+u=0), t = -mu(n)(1-x)/2. Then
      lam*(t - xi(k)) = [ (n+lam-1)*x + (2k-n) ] / 2,
    so R(n,t) is a positive constant times
      P(x) = [ prod_{k=1}^{n-1} ((n+lam-1)*x + (2k-n)) ]^2.
    Returns (p, q): coefficient lists (index = power of x) of P and of the
    unsquared product Q.
    """
    w = F(n) + lam - 1
    q = [F(1)]
    for k in range(1, n):
        c0 = F(2 * k - n)
        new = [F(0)] * (len(q) + 1)
        for i, c in enumerate(q):
            new[i] += c * c0
            new[i + 1] += c * w
        q = new
    deg = 2 * (n - 1)
    p = [F(0)] * (deg + 1)
    for i, a_ in enumerate(q):
        if a_ == 0:
            continue
        for j, b in enumerate(q):
            p[i + j] += a_ * b
    return p, q


def gegen_basis(lmax: int, a: F):
    """Coefficient lists of C_l^a(x), exact Fractions, a > 0."""
    C = [[F(1)], [F(0), 2 * a]]
    for l in range(1, lmax):
        xc = [F(0)] + C[l]
        new = [F(2) * (l + a) * c / (l + 1) for c in xc]
        for i, c in enumerate(C[l - 1]):
            new[i] -= (l + 2 * a - 1) * c / (l + 1)
        C.append(new)
    return C[: lmax + 1]


def partial_waves(p, a: F, basis=None):
    """Exact coefficients c_l of P in the C_l^a basis.

    For a > 0 (i.e. D > 3) the physical D-dim Gegenbauer G_l^(D) is a positive
    multiple of C_l^a, so sign(c_l) == sign(a_{n,l}).
    """
    deg = len(p) - 1
    C = basis if basis is not None else gegen_basis(deg, a)
    rem = list(p)
    out = [F(0)] * (deg + 1)
    for l in range(deg, -1, -1):
        c = rem[l] / C[l][l]
        out[l] = c
        for i, cc in enumerate(C[l]):
            rem[i] -= c * cc
    assert all(v == 0 for v in rem), "triangular basis solve failed"
    return out


def min_T_over_n(lam: F, dmax: F):
    """min_n T_n(lam) among n that could matter (T_n > 2n kills large n)."""
    best = None
    n = 3
    while 2 * n <= dmax + 2:
        t = T_frac(n, lam)
        if best is None or t < best[0]:
            best = (t, n)
        n += 1
    if best is None:
        best = (T_frac(3, lam), 3)
    return best


# ----------------------------------------------------------------------------
# A0: kinematic substitution vs paper Eq. (7)
# ----------------------------------------------------------------------------

def attack0():
    rng = random.Random(1)
    bad = []
    for n in range(2, 7):
        for _ in range(3):
            lam = sp.Rational(rng.randint(1, 50), rng.randint(1, 11))
            t = sp.Rational(rng.randint(-40, 40), rng.randint(1, 7))
            mu = (n + lam - 1) / lam
            xval = 1 + 2 * t / mu
            w = n + lam - 1
            Pval = sp.prod([w * xval + (2 * k - n) for k in range(1, n)]) ** 2
            direct = (2 ** (n - 1) * sp.rf((1 + lam) / 2 + lam * t, n - 1)) ** 2
            if sp.simplify(Pval - direct) != 0:
                bad.append((n, str(lam), str(t)))
    if bad:
        fail(f"A0 kinematics/product form mismatch at {bad}")
    else:
        note("A0 PASS: t=-mu(n)(1-x)/2 substitution matches paper Eq.(7) "
             "residues exactly (15 random exact points, n=2..6)")


# ----------------------------------------------------------------------------
# A1: random exact points, bracket vs direct projection
# ----------------------------------------------------------------------------

def attack1(trials=40, seed=20260814):
    rng = random.Random(seed)
    bad = []
    tested = 0
    while tested < trials:
        n = rng.randint(3, 8)
        lam = F(rng.randint(1, 120), rng.randint(1, 24))
        D = F(rng.randint(14, 400), rng.randint(1, 4))
        if D <= 3:
            continue
        tested += 1
        a = (D - 3) / 2
        p, _ = residue_x_coeffs(n, lam)
        pw = partial_waves(p, a)
        c = pw[2 * n - 4]
        lead = pw[2 * n - 2]
        pred = T_frac(n, lam) - D
        ok = (c > 0 and pred > 0) or (c < 0 and pred < 0) or (c == 0 and pred == 0)
        if not ok:
            bad.append((n, str(lam), str(D), str(c), str(pred)))
        if lead <= 0:
            bad.append(("leading<=0", n, str(lam), str(D), str(lead)))
    if bad:
        fail(f"A1 bracket-vs-projection mismatches: {bad}")
    else:
        note(f"A1 PASS: sign a_(n,2n-4) == sign(T_n - D) at {trials} random exact "
             "points (odd/fractional D included); leading a_(n,2n-2) > 0 at all")


# ----------------------------------------------------------------------------
# A2: odd trajectories vanish identically (symbolic lambda)
# ----------------------------------------------------------------------------

def attack2():
    bad = []
    for n in range(3, 10):
        w = n + LAM - 1
        Qp = sp.prod([w * x + (2 * k - n) for k in range(1, n)])
        P = sp.expand(Qp**2)
        if sp.expand(P - P.subs(x, -x)) != 0:
            bad.append(n)
        # also: Q itself parity-definite => q_{n-2} = 0 identically
        if sp.expand(sp.Poly(Qp, x).all_coeffs()[::-1][n - 2]) != 0:
            bad.append((n, "q_{n-2} != 0"))
    if bad:
        fail(f"A2 odd-vanishing / parity failure at n={bad}")
    else:
        note("A2 PASS: R(n,t(x)) even in x symbolically for n=3..9 "
             "(t<->u root pairing xi(k)+xi(n-k)=-mu(n)); odd a_(n,l) == 0; "
             "q_(n-2) == 0 identically (cross-term bookkeeping forced)")


# ----------------------------------------------------------------------------
# A3: razor zeros at never-tested (lambda, D), solved from DIRECT projection
# ----------------------------------------------------------------------------

def razor(n: int, lam: F, expected):
    target = 2 * n - 4
    a = (DD - 3) / 2
    pF, _ = residue_x_coeffs(n, lam)
    deg = len(pF) - 1
    C = [[sp.Integer(1)], [sp.Integer(0), 2 * a]]
    for l in range(1, deg):
        xc = [sp.Integer(0)] + C[l]
        new = [sp.cancel(2 * (l + a) * c / (l + 1)) for c in xc]
        for i, c in enumerate(C[l - 1]):
            new[i] = sp.cancel(new[i] - (l + 2 * a - 1) * c / (l + 1))
        C.append(new)
    rem = [sp.Rational(v.numerator, v.denominator) for v in pF]
    coeff = None
    for l in range(deg, target - 1, -1):
        c = sp.cancel(rem[l] / C[l][l])
        if l == target:
            coeff = c
            break
        for i, cc in enumerate(C[l]):
            rem[i] = sp.cancel(rem[i] - c * cc)
    num = sp.expand(sp.numer(sp.together(coeff)))
    roots = sp.solve(sp.Eq(num, 0), DD)
    hit = any(sp.simplify(r - expected) == 0 for r in roots)
    spurious = [r for r in roots
                if sp.simplify(r - expected) != 0 and r.is_real and r > 3]
    return hit, roots, spurious


def attack3():
    ok = True
    # razor 1: n=5, lam=7/2 -> T_5(7/2) = 271/4 (fractional D*, brand new point)
    hit, roots, spurious = razor(5, F(7, 2), sp.Rational(271, 4))
    if not (hit and not spurious):
        ok = False
        fail(f"A3 razor(n=5,lam=7/2): expected sole root D*=271/4, got {roots}")
    # sign flip around 271/4 in exact arithmetic
    p, _ = residue_x_coeffs(5, F(7, 2))
    lo = partial_waves(p, (F(67) - 3) / 2)[6]
    hi = partial_waves(p, (F(69) - 3) / 2)[6]
    at = partial_waves(p, (F(271, 4) - 3) / 2)[6]
    if not (lo > 0 and hi < 0 and at == 0):
        ok = False
        fail(f"A3 sign flip n=5,lam=7/2: D=67 -> {lo}, D*=271/4 -> {at}, D=69 -> {hi}")
    # razor 2: n=6, lam=3 -> T_6(3) = 57
    hit2, roots2, spurious2 = razor(6, F(3), sp.Integer(57))
    if not (hit2 and not spurious2):
        ok = False
        fail(f"A3 razor(n=6,lam=3): expected sole root D*=57, got {roots2}")
    p6, _ = residue_x_coeffs(6, F(3))
    lo6 = partial_waves(p6, (F(56) - 3) / 2)[8]
    hi6 = partial_waves(p6, (F(58) - 3) / 2)[8]
    at6 = partial_waves(p6, (F(57) - 3) / 2)[8]
    if not (lo6 > 0 and hi6 < 0 and at6 == 0):
        ok = False
        fail(f"A3 sign flip n=6,lam=3: D=56 -> {lo6}, D*=57 -> {at6}, D=58 -> {hi6}")
    if ok:
        note("A3 PASS: razor zeros at never-tested points confirmed from the "
             "DIRECT projection with symbolic D: (n=5, lam=7/2) vanishes at "
             "exactly D*=271/4 (fractional), (n=6, lam=3) at D*=57; exact sign "
             "flips on both sides; no spurious real roots D>3")


# ----------------------------------------------------------------------------
# A4: full-(n,l) knife hunt (attacks C4 -- "no other knives")
# ----------------------------------------------------------------------------

def full_scan(lam: F, D: F, nmax: int):
    a = (D - 3) / 2
    basis = gegen_basis(max(2 * nmax - 2, 2), a)
    neg, zeros = [], []
    for n in range(1, nmax + 1):
        p, _ = residue_x_coeffs(n, lam)
        pw = partial_waves(p, a, basis)
        for l, c in enumerate(pw):
            if c < 0:
                neg.append((n, l, str(c)))
            elif c == 0 and l % 2 == 0 and l <= 2 * n - 2:
                zeros.append((n, l))
    return neg, zeros


def attack4():
    t0 = time.time()
    alive_points = [
        # (lam, D, nmax) -- model says ALIVE (D <= min_n T_n(lam))
        (F(1, 10), F(10), 30),    # near CHR onset; min T = T_3(0.1) = 10.23
        (F(1, 20), F(8), 25),     # D < 9: model says nothing bites anywhere
        (F(10), F(180), 40),      # large-lambda flank; min T ~ 187.5 (n~17)
        (F(1), F(23), 25),        # VS at its exact cliff: a_{4,4}=0, rest >= 0
        (F(1, 100), F(4), 30),    # slice-3/D=4 extremal corner, ALL l (re-check)
        (F(100), F(4), 30),       # slice-3/D=4 other extremal corner, ALL l
    ]
    dead_controls = [
        (F(1, 20), F(10), 8, (3, 2)),   # model: dead, first knife (3,2)
        (F(1), F(24), 8, (4, 4)),       # VS dies at D=24 via (4,4)
    ]
    ok = True
    for lam, D, nmax in alive_points:
        mt, mtn = min_T_over_n(lam, D)
        model_alive = D <= mt
        neg, zeros = full_scan(lam, D, nmax)
        note(f"A4 point lam={lam} D={D} n<={nmax}: min_n T_n = {mt} (n={mtn}), "
             f"model={'ALIVE' if model_alive else 'DEAD'}, negatives={len(neg)}, "
             f"even zeros={zeros[:6]}")
        if model_alive and neg:
            ok = False
            fail(f"A4 KNIFE FOUND: lam={lam}, D={D}: negative a_(n,l) at "
                 f"{neg[:10]} although D <= min_n T_n={mt} -- C4 falsified")
        if not model_alive:
            note(f"A4 WARNING: test point lam={lam},D={D} not in model-alive "
                 "region; recheck point selection")
    for lam, D, nmax, knife in dead_controls:
        neg, _ = full_scan(lam, D, nmax)
        found = [(n, l) for (n, l, _) in neg]
        if knife not in found:
            ok = False
            fail(f"A4 dead-control lam={lam},D={D}: expected knife {knife}, "
                 f"negatives found: {found}")
        else:
            note(f"A4 dead-control PASS: lam={lam}, D={D}: knife {knife} "
                 f"negative as predicted (all negatives: {found})")
    if ok:
        note(f"A4 PASS (no counterexample found; NOT a proof of C4). "
             f"runtime {time.time()-t0:.1f}s")


# ----------------------------------------------------------------------------
# A5: symbolic re-derivation of the bracket (cross terms) and threshold == T_n
# ----------------------------------------------------------------------------

def attack5():
    bad = []
    rng = random.Random(7)
    for n in range(3, 9):
        w = n + LAM - 1
        Qp = sp.Poly(sp.prod([w * x + (2 * k - n) for k in range(1, n)]), x)
        qc = Qp.all_coeffs()[::-1]
        if sp.expand(qc[n - 2]) != 0:
            bad.append((n, "q_{n-2} nonzero"))
            continue
        A = sp.expand(qc[n - 1] ** 2)
        Cc = sp.expand(2 * qc[n - 1] * qc[n - 3])  # pure cross term
        l = 2 * n - 4
        rho = sp.Rational((l + 1) * (l + 2), 2) / (DD + 2 * l - 1)
        bracket = sp.together(Cc + A * rho)
        Dstar = sp.solve(sp.Eq(sp.expand(sp.numer(bracket)), 0), DD)
        if len(Dstar) != 1 or sp.simplify(Dstar[0] - T_sym(n, LAM)) != 0:
            bad.append((n, "threshold != T_n", [str(d) for d in Dstar]))
        # C < 0 for lam >= 0 (direction of the inequality) -- spot checks
        for _ in range(3):
            lv = sp.Rational(rng.randint(0, 200), rng.randint(1, 20))
            if Cc.subs(LAM, lv) >= 0:
                bad.append((n, f"C >= 0 at lam={lv}: direction flips"))
        # full projection == positive * bracket at random exact points
        for _ in range(2):
            lv = F(rng.randint(1, 60), rng.randint(1, 12))
            Dv = F(rng.randint(14, 200), rng.randint(1, 3))
            if Dv <= 3:
                continue
            p, _ = residue_x_coeffs(n, lv)
            cfull = partial_waves(p, (Dv - 3) / 2)[l]
            lsym = sp.Rational(lv.numerator, lv.denominator)
            Dsym = sp.Rational(Dv.numerator, Dv.denominator)
            bnum = (Cc + A * rho).subs({LAM: lsym, DD: Dsym})
            cf = sp.Rational(cfull.numerator, cfull.denominator)
            if bnum == 0 and cf == 0:
                continue
            ratio = sp.cancel(cf / bnum)
            if not ratio.is_positive:
                bad.append((n, f"projection/bracket ratio not positive at "
                               f"lam={lv}, D={Dv}: {ratio}"))
    if bad:
        fail(f"A5 symbolic bookkeeping failures: {bad}")
    else:
        note("A5 PASS: for n=3..8 (symbolic lambda): q_(n-2)==0, the x^(2n-4) "
             "coefficient is PURE cross term 2 q_(n-1) q_(n-3) < 0, the bracket "
             "C + A*rho has its unique D-root exactly at T_n(lambda), and the "
             "full projection is a positive multiple of the bracket")


# ----------------------------------------------------------------------------
# A6: envelope -- magic point, large-D asymptote, D=200 spot
# ----------------------------------------------------------------------------

def lam_root(n: int, Dval) -> float | None:
    """Positive root of T_n(lam)=D, float (exactness only needed at winners)."""
    alpha = 3.0 * (2 * n - 3) / (n * (n - 2))
    c0 = alpha + 2.0 * n - float(Dval)
    disc = (alpha * (2 * n - 2)) ** 2 - 4 * alpha * c0
    if disc < 0:
        return None
    r = (-alpha * (2 * n - 2) + disc**0.5) / (2 * alpha)
    return r if r > 0 else None


def attack6():
    ok = True
    # magic point: lam_min(23) = 1 exactly, i.e. T_n(1) >= 23 for ALL n, eq at 4
    if T_frac(4, F(1)) != 23:
        ok = False
        fail("A6: T_4(1) != 23")
    viol = [n for n in range(3, 2001) if T_frac(n, F(1)) < 23]
    eq = [n for n in range(3, 2001) if T_frac(n, F(1)) == 23]
    if viol or eq != [4]:
        ok = False
        fail(f"A6 magic point: T_n(1)<23 at {viol}; equality set {eq} != [4]")
    else:
        note("A6 PASS: lam_min(23)=1 exact -- T_n(1) >= 23 for n=3..2000 with "
             "equality only at n=4 (plus analytic: integer min of "
             "2(n^2+4n-9)/(n-2) sits at n=4)")
    # VS threshold closed form vs T_n(1)
    bad2 = [n for n in range(3, 200)
            if T_frac(n, F(1)) != F(2 * (n * n + 4 * n - 9), n - 2)]
    if bad2:
        ok = False
        fail(f"A6: T_n(1) != 2(n^2+4n-9)/(n-2) at n={bad2}")
    else:
        note("A6 PASS: D_n(1) = 2(n^2+4n-9)/(n-2) == T_n(1) for n=3..199")
    # asymptote
    target = 12 + 4 * 3**0.5
    rows = []
    for Dv in [60, 100, 200, 400, 1000, 3000, 10000]:
        best_r, best_n = 0.0, None
        for n in range(3, max(60, int(2 * (Dv / target)) + 40)):
            r = lam_root(n, Dv)
            if r is not None and r > best_r:
                best_r, best_n = r, n
        rows.append((Dv, best_n, best_r, Dv / best_r, 3**0.5 * best_r))
        note(f"A6 envelope D={Dv}: lam_min~{best_r:.5f} (n*={best_n}), "
             f"D/lam_min={Dv/best_r:.4f} vs 12+4sqrt3={target:.4f}, "
             f"sqrt3*lam_min={3**0.5*best_r:.2f}")
    drift = [abs(r[3] - target) for r in rows[-3:]]
    if not all(d < 0.2 for d in drift):
        ok = False
        fail(f"A6 asymptote: D/lam_min not approaching 12+4sqrt3: {rows}")
    # spot sign-flip at D=200 (never scanned): exact arithmetic both sides
    Dv = F(200)
    best_r, best_n = 0.0, None
    for n in range(3, 80):
        r = lam_root(n, Dv)
        if r is not None and r > best_r:
            best_r, best_n = r, n
    lam_lo = F(int(best_r * 10**6) - 20, 10**6)
    lam_hi = F(int(best_r * 10**6) + 20, 10**6)
    p_lo, _ = residue_x_coeffs(best_n, lam_lo)
    c_lo = partial_waves(p_lo, (Dv - 3) / 2)[2 * best_n - 4]
    a = (Dv - 3) / 2
    basis = gegen_basis(2 * 60 - 2, a)
    clean = True
    for n in range(3, 61):
        p, _ = residue_x_coeffs(n, lam_hi)
        if partial_waves(p, a, basis)[2 * n - 4] < 0:
            clean = False
            break
    if not (c_lo < 0 and clean):
        ok = False
        fail(f"A6 D=200 spot: below lam_min a_({best_n},{2*best_n-4})={c_lo} "
             f"(want <0), above lam_min clean={clean} (want True)")
    else:
        note(f"A6 PASS: D=200 spot: a_({best_n},{2*best_n-4}) < 0 at "
             f"lam_min-2e-5, trajectory clean for n<=60 at lam_min+2e-5")
    return ok


# ----------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    note("attack_gravity.py -- adversarial battery vs gravity-card slices 1-6")
    note(f"sympy {sp.__version__}; seeds fixed; all sign decisions in exact "
         "arithmetic")
    for name, fn in [("A0", attack0), ("A1", attack1), ("A2", attack2),
                     ("A3", attack3), ("A4", attack4), ("A5", attack5),
                     ("A6", attack6)]:
        try:
            fn()
        except Exception as e:  # report, keep going
            fail(f"{name} crashed: {type(e).__name__}: {e}")
    verdict = "NO FALSIFICATION" if not FAILURES else "FALSIFIED / ERRORS"
    note(f"TOTAL: {verdict}; failures={len(FAILURES)}; "
         f"runtime {time.time()-t0:.1f}s")
    RES.mkdir(exist_ok=True)
    out = RES / "attack_gravity.json"
    out.write_text(json.dumps({"verdict": verdict, "failures": FAILURES,
                               "log": NOTES}, indent=1))
    note(f"artifact: {out}")
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
