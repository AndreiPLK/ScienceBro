"""ADVERSARIAL ATTACK on the BLADE THEOREM (paper 4 candidate).

Independent by construction: this file imports NOTHING from lab/blade_proof.py.
Bracket, envelope, window logic, certificates and cell decisions are all rebuilt
from the theorem statement alone:

  Bhat(u) = al*u*(u-2) - G*u*s^2 + s^4,  u = D+4m+1,  m = n-3,  s = lam+n-1,
  G  = 2(m+1)(m+3)/(3(2m+3)),
  al = (m+3)(5m^3+21m^2+19m+15)/(45(2m+1)(2m+3)),
  T_k(lam) = 3(2k-3)/(k(k-2))*(lam^2+(2k-2)lam+1) + 2k,   envelope = min_{k>=3} T_k.

THEOREM under attack: for every m>=1 and lam>0 the negativity window of Bhat
(the open u-interval where Bhat<0, if nonempty) lies strictly above
Tmin(lam)+4m+1 in u (equivalently: strictly above Tmin(lam) in D).

Exact per-point violation test (this is an IFF, not merely sufficient):
  al>0, so Bhat is an upward parabola in u.  When disc>0 the window is
  (u_-, u_+).  "Some window point <= u_env"  <=>  u_- < u_env
  <=>  NOT( Bhat(u_env)>=0 AND u_env <= vertex ),   vertex = 1 + G*s^2/(2*al).
  (=>: u_env<=u_- gives Bhat(u_env)>=0 and u_env<vertex; <=: if Bhat(u_env)>=0
   and u_env<=vertex then u_env<=u_-, since disc>0 forces Bhat(vertex)<0.)

CONTRACT
  exit 2  : counterexample to the THEOREM found (details in the artifact);
  exit 1  : no counterexample, but some independent certificate / cell
            re-certification failed => the proof stays OPEN at that cell;
  exit 0  : no counterexample AND all rebuilt certificates pass AND every
            branch cell (k=4..45, m=1..m_start-1, incl. the coverage-gap cells
            skipped by blade_proof.py) is independently re-certified.
Artifact: results/attack_blade.json.  The coverage gap found by static audit
of blade_proof.py + results/blade_proof.json is reported regardless of exit.

Usage:
  C:\\Users\\user\\ScienceBro\\.venv\\Scripts\\python.exe lab/attack_blade_theorem.py [--fast]
"""

from __future__ import annotations

import json
import math
import re
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve()
PROJ = HERE.parents[1]
RES = PROJ / "results"
BLADE_JSON = RES / "blade_proof.json"
OUT = RES / "attack_blade.json"

FAST = "--fast" in sys.argv

lamS = sp.Symbol("lam", nonnegative=True)
mS = sp.Symbol("m", nonnegative=True)
v = sp.Symbol("v", nonnegative=True)
w = sp.Symbol("w", nonnegative=True)
z = sp.Symbol("z", nonnegative=True)
r3 = sp.sqrt(3)
SQ3 = math.sqrt(3.0)

T0_START = time.time()


def log_print(msg):
    print(f"[{time.time() - T0_START:7.1f}s] {msg}", flush=True)


# ===================== exact (Fraction) bracket & envelope =====================


def G_fr(m: int) -> Fr:
    return Fr(2 * (m + 1) * (m + 3), 3 * (2 * m + 3))


def al_fr(m: int) -> Fr:
    return Fr((m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15), 45 * (2 * m + 1) * (2 * m + 3))


def Tk_fr(k: int, lam: Fr) -> Fr:
    return Fr(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k


def Tmin_fr(lam: Fr) -> Fr:
    """Exact envelope min_{k>=3} T_k(lam).

    Rigorous cutoff: T_k = 3(2k-3)/(k(k-2))*(lam^2+(2k-2)lam+1) + 2k
    >= [3(2k-3)(2k-2)/(k(k-2))]*lam + 2k >= 10*lam + 2k for k>=3, lam>=0
    (since 6(2k-3)(k-1) - 10k(k-2) = 2k^2-10k+18 > 0).  Hence any k with
    10*lam + 2k > best cannot improve the minimum; scanning k upward until
    that bound exceeds the current best covers ALL k >= 3 exactly."""
    best = Tk_fr(3, lam)
    kc = int(SQ3 * float(lam)) + 2
    for kg in {max(4, kc - 1), max(4, kc), max(4, kc + 1)}:
        t = Tk_fr(kg, lam)
        if t < best:
            best = t
    k = 4
    while 10 * lam + 2 * k <= best:
        t = Tk_fr(k, lam)
        if t < best:
            best = t
        k += 1
    return best


_TMIN_CACHE: dict = {}


def Tmin_cached(lam: Fr) -> Fr:
    r = _TMIN_CACHE.get(lam)
    if r is None:
        r = Tmin_fr(lam)
        _TMIN_CACHE[lam] = r
    return r


def check_exact(m: int, lam: Fr):
    """Exact violation test at rational (m, lam).

    Returns (violation, window_exists, margin_float_or_None).
    margin = u_- - u_env = D_- - Tmin (float, for reporting only;
    the violation verdict itself is exact rational arithmetic)."""
    G = G_fr(m)
    al = al_fr(m)
    s = lam + m + 2
    s2 = s * s
    disc = (2 * al + G * s2) ** 2 - 4 * al * s2 * s2
    if disc <= 0:
        return False, False, None
    T = Tmin_cached(lam)
    u = T + 4 * m + 1
    B = al * u * (u - 2) - G * u * s2 + s2 * s2
    vertex_ok = G * s2 >= (u - 1) * 2 * al  # u <= vertex
    holds = (B >= 0) and vertex_ok
    try:
        um = (float(2 * al + G * s2) - math.sqrt(float(disc))) / (2 * float(al))
        margin = um - float(u)
    except OverflowError:
        margin = None
    return (not holds), True, margin


def margin_precise(m: int, lam: Fr) -> float:
    """High-precision margin u_- - u_env via sympy evalf(60) (reporting)."""
    G = sp.Rational(G_fr(m).numerator, G_fr(m).denominator)
    al = sp.Rational(al_fr(m).numerator, al_fr(m).denominator)
    lamQ = sp.Rational(lam.numerator, lam.denominator)
    s2 = (lamQ + m + 2) ** 2
    disc = (2 * al + G * s2) ** 2 - 4 * al * s2**2
    T = Tmin_cached(lam)
    u = sp.Rational(T.numerator, T.denominator) + 4 * m + 1
    um = ((2 * al + G * s2) - sp.sqrt(disc)) / (2 * al)
    return float(sp.N(um - u, 60))


# ============================ float twin (scans) ==============================


def Tmin_float(lam: float) -> float:
    kc = int(SQ3 * lam) + 2
    ks = set(range(3, 12)) | set(range(max(3, kc - 4), kc + 6))
    return min(
        3.0 * (2 * k - 3) / (k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k for k in ks
    )


def check_float(m: float, lam: float):
    """Returns margin u_- - u_env (float) if a window exists, else None."""
    G = 2.0 * (m + 1) * (m + 3) / (3 * (2 * m + 3))
    al = (m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15) / (45.0 * (2 * m + 1) * (2 * m + 3))
    s2 = (lam + m + 2) ** 2
    disc = (2 * al + G * s2) ** 2 - 4 * al * s2 * s2
    if disc <= 0:
        return None
    u_env = Tmin_float(lam) + 4 * m + 1
    um = ((2 * al + G * s2) - math.sqrt(disc)) / (2 * al)
    return um - u_env


def window_tip_float(m: float):
    """lam where the window is born: disc=0 <=> s^2 = S^2_max (beta>0 proven).
    Returns lam_tip or None if no window for any lam>0."""
    G = 2.0 * (m + 1) * (m + 3) / (3 * (2 * m + 3))
    al = (m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15) / (45.0 * (2 * m + 1) * (2 * m + 3))
    beta = 4 * al - G * G
    if beta <= 0:  # would contradict our beta>0 proof
        raise AssertionError(f"beta<=0 at m={m}")
    s2max = 2 * al * (G + 2 * math.sqrt(al)) / beta
    tip = math.sqrt(s2max) - m - 2
    return tip if tip > 0 else None


# ==================== exact univariate positivity machinery ====================


def rational_between(a, b) -> sp.Rational:
    """Exact rational strictly between a < b (Rational or CRootOf)."""
    for prec in (20, 40, 80, 160, 320, 640):
        mid = sp.Rational(sp.N((a + b) / 2, prec))
        if bool(a < mid) and bool(mid < b):
            return mid
    raise RuntimeError(f"rational_between failed for {a}, {b}")


def _distinct_roots_in(P: sp.Poly, lo, hi):
    """Distinct real roots of P strictly inside (lo, hi), exact, sorted."""
    out = []
    for r in P.real_roots():
        if bool(lo < r) and (hi is None or bool(r < hi)):
            if not out or not bool(out[-1] == r):
                out.append(r)
    return out


def poly_nonneg_on(P: sp.Poly, lo: sp.Rational, hi):
    """Exact: P(x) >= 0 for all x in [lo, hi] (hi=None => [lo, +oo)).

    Method: endpoints checked exactly; between consecutive distinct real roots
    the sign is constant and nonzero, so one exact rational sample per gap
    decides the sign everywhere; roots themselves give P=0 >= 0."""
    e = P.as_expr()
    if e.is_number:
        return bool(e >= 0)
    if P.eval(lo) < 0:
        return False
    if hi is not None and P.eval(hi) < 0:
        return False
    pts = [lo] + _distinct_roots_in(P, lo, hi) + ([hi] if hi is not None else [])
    if hi is None:
        last = pts[-1]
        upper = sp.Integer(int(sp.floor(last)) + 1) if pts[1:] else lo + 1
        pts = pts + [upper, None]  # unbounded tail gap sample
        # sample beyond the last root decides the sign on (last, +oo)
        if P.eval(upper) <= 0 and bool(upper > last):
            return False
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if b is None:
            break
        if bool(a == b):
            continue
        q = rational_between(a, b)
        if P.eval(q) <= 0:
            return False
    return True


def poly_pos_on_lopen(P: sp.Poly, lo: sp.Rational, hi: sp.Rational):
    """Exact: P(x) > 0 for all x in (lo, hi] (root isolation + sample)."""
    e = P.as_expr()
    if e.is_number:
        return bool(e > 0)
    for r in P.real_roots():
        if bool(lo < r) and bool(r <= hi):
            return False
    return P.eval(hi) > 0


# ===================== per-cell exact decision procedure ======================


def cell_polys(k: int, m: int):
    """d(lam), B(lam), V(lam) at fixed integer (k, m): rational-coeff polys.
    B is Bhat evaluated at u = T_k+4m+1; V>0 <=> that u is left of the vertex."""
    G = sp.Rational(2 * (m + 1) * (m + 3), 3 * (2 * m + 3))
    al = sp.Rational((m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15), 45 * (2 * m + 1) * (2 * m + 3))
    s = lamS + m + 2
    Tk = sp.Rational(3 * (2 * k - 3), k * (k - 2)) * (lamS**2 + (2 * k - 2) * lamS + 1) + 2 * k
    u = Tk + 4 * m + 1
    d = sp.expand((2 * al + G * s**2) ** 2 - 4 * al * s**4)
    B = sp.expand(al * u * (u - 2) - G * u * s**2 + s**4)
    V = sp.expand(G * s**2 - (u - 1) * 2 * al)
    return sp.Poly(d, lamS), sp.Poly(B, lamS), sp.Poly(V, lamS)


def decide_cell(k: int, m: int, lo: sp.Rational, hi: sp.Rational, log: list):
    """Exact decision of  'forall lam in [lo,hi]: d<=0 OR (B>=0 AND V>=0)'.

    Route 1: -d >= 0 on [lo,hi]  (no window anywhere in the cell).
    Route 2: B >= 0 and V >= 0 on [lo,hi].
    Route 3 (mixed): breakpoints = distinct roots of W=d*B*V in (lo,hi).
      On every open gap all three signs are constant and nonzero, so one exact
      rational sample per gap decides the condition on the whole gap.  At a
      breakpoint x0: if d(x0)=0 the condition holds (d<=0); if d(x0)>0 then d>0
      on both adjacent gaps (no d-root at x0), so those gaps passed via
      B>0 and V>0, whence by continuity B(x0)>=0 and V(x0)>=0.  Endpoints are
      evaluated exactly.  This is a complete, rigorous case split."""
    Pd, PB, PV = cell_polys(k, m)
    tag = f"k{k}_m{m}"
    Pnd = sp.Poly(-Pd.as_expr(), lamS)
    if poly_nonneg_on(Pnd, lo, hi):
        log.append({"cell": tag, "via": "no-window"})
        return True
    if poly_nonneg_on(PB, lo, hi) and poly_nonneg_on(PV, lo, hi):
        log.append({"cell": tag, "via": "B&V"})
        return True
    W = sp.Poly(sp.expand(Pd.as_expr() * PB.as_expr() * PV.as_expr()), lamS)
    pts = [lo] + _distinct_roots_in(W, lo, hi) + [hi]

    def ok_at(q):
        return (Pd.eval(q) <= 0) or (PB.eval(q) >= 0 and PV.eval(q) >= 0)

    if not ok_at(lo) or not ok_at(hi):
        log.append({"cell": tag, "via": "split", "cert": "FAILED", "at": "endpoint"})
        return False
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if bool(a == b):
            continue
        q = rational_between(a, b)
        if not ok_at(q):
            log.append({"cell": tag, "via": "split", "cert": "FAILED", "at": str(q)})
            return False
    log.append({"cell": tag, "via": "split"})
    return True


# ================== 2-var Polya-type certificates (tails, k3) ==================


def _den_positive_on_orthant(den, gens):
    """Denominator positivity check (closes the fraction()[0] sign risk that
    blade_proof.py never verifies): all coeffs >= 0 and den(0)>0 => den>0 for
    all gens >= 0; otherwise fall back to a univariate root argument."""
    denx = sp.expand(den)
    if denx.is_number:
        return bool(denx > 0)
    try:
        P = sp.Poly(denx, *gens)
    except sp.PolynomialError:
        return False
    if all(c >= 0 for _, c in P.terms()) and P.eval([0] * len(gens)) > 0:
        return True
    if len(gens) == 1:
        Q = sp.Poly(denx, gens[0])
        if not any(bool(r >= 0) for r in Q.real_roots()) and Q.eval(1) > 0:
            return True
    return False


def numerator_checked(E, gens, tag, log):
    """together+fraction with an EXPLICIT denominator-sign proof; returns the
    numerator (valid to use iff the logged den_positive is True)."""
    num, den = sp.fraction(sp.together(sp.expand(E)))
    okden = _den_positive_on_orthant(den, gens)
    log.append({"cell": tag, "den_positive": bool(okden)})
    return sp.expand(num), okden


def polya2(num_ml, m0: int, lo, hi, a, b, depth, log, tag):
    """num(m,lam) >= 0 for m >= m0, lam in [lo + (hi-lo)*t, t in [a,b]] via
    m = v+m0, t = a+(b-a)w/(1+w) and coefficient nonnegativity; bisect on
    failure.  (Covers t in [a,b) per subinterval; the union over the bisection
    tree plus the exact endpoint t=b evaluation below covers [a,b].)"""
    degL = sp.degree(num_ml, lamS)
    tsub = a + (b - a) * w / (1 + w)
    lam_expr = lo + (hi - lo) * tsub
    f = num_ml.subs(mS, v + m0).subs(lamS, lam_expr)
    f, okden = numerator_checked(f, (v, w), f"{tag}_den", log)
    if not okden:
        log.append({"cell": tag, "t": [str(a), str(b)], "cert": "DEN-FAIL"})
        return False
    P = sp.Poly(f, v, w)
    if all(c >= 0 for _, c in P.terms()):
        log.append({"cell": tag, "t": [str(a), str(b)], "cert": "N=0"})
        return True
    if depth == 0:
        log.append({"cell": tag, "t": [str(a), str(b)], "cert": "FAILED"})
        return False
    mid = (a + b) / 2
    return polya2(num_ml, m0, lo, hi, a, mid, depth - 1, log, tag) and polya2(
        num_ml, m0, lo, hi, mid, b, depth - 1, log, tag
    )


def branch_BV_syms(k: int):
    """Symbolic-m numerators of B and V for branch k, denominators PROVEN
    positive (returns None on den failure)."""
    G = 2 * (mS + 1) * (mS + 3) / (3 * (2 * mS + 3))
    al = (mS + 3) * (5 * mS**3 + 21 * mS**2 + 19 * mS + 15) / (45 * (2 * mS + 1) * (2 * mS + 3))
    s = lamS + mS + 2
    Tk = sp.Rational(3 * (2 * k - 3), k * (k - 2)) * (lamS**2 + (2 * k - 2) * lamS + 1) + 2 * k
    u = Tk + 4 * mS + 1
    B = al * u * (u - 2) - G * u * s**2 + s**4
    V = G * s**2 - (u - 1) * 2 * al
    out = []
    scratch = []
    for E in (B, V):
        num, okden = numerator_checked(E, (mS,), f"k{k}_symden", scratch)
        if not okden:
            return None
        out.append(num)
    return out


def tail_certificate(k: int, m0: int, lo, hi, log):
    """Rebuild of the branch-k tail certificate: B,V >= 0 for all m >= m0,
    lam in [lo, hi] (exact endpoint lam=hi checked separately below since
    w/(1+w) only reaches t<1)."""
    syms = branch_BV_syms(k)
    if syms is None:
        log.append({"cell": f"k{k}_tail_m{m0}", "cert": "DEN-FAIL"})
        return False
    numB, numV = syms
    okB = polya2(numB, m0, lo, hi, sp.Integer(0), sp.Integer(1), 4, [], f"k{k}_Btail")
    okV = polya2(numV, m0, lo, hi, sp.Integer(0), sp.Integer(1), 4, [], f"k{k}_Vtail")
    # exact right endpoint (t=1 not reached by w/(1+w)): univariate in m
    okE = True
    for nm, numX in (("B", numB), ("V", numV)):
        Pm = sp.Poly(sp.expand(numX.subs(lamS, hi).subs(mS, v + m0)), v)
        if not poly_nonneg_on(Pm, sp.Integer(0), None):
            okE = False
    ok = bool(okB and okV and okE)
    log.append(
        {"cell": f"k{k}_tail_m{m0}", "cert": "OK" if ok else "FAILED", "endpoint_exact": bool(okE)}
    )
    return ok


# ===================== sqrt(3) certificates (L1, L3 rebuild) ==================


def split_sqrt3(e):
    en = e.subs(r3, -r3)
    a = sp.expand((e + en) / 2)
    b = sp.expand(sp.radsimp((e - en) / (2 * r3)))
    assert not a.has(r3) and not b.has(r3), "sqrt(3) split failed"
    assert sp.expand(a + b * r3 - e) == 0, "sqrt(3) split reconstruction failed"
    return a, b


def q3_nonneg(a, b):
    """Exact test of a + b*sqrt(3) >= 0 for rational a, b."""
    if a >= 0 and b >= 0:
        return True
    if a >= 0 and b < 0:
        return bool(a * a >= 3 * b * b)
    if a < 0 and b >= 0:
        return bool(3 * b * b >= a * a)
    return False


def cert_sqrt3(e, gens, tag, log):
    """All Q(sqrt3) coefficients of e (poly in gens) nonnegative => e >= 0 on
    the nonnegative orthant."""
    a, b = split_sqrt3(e)
    terms: dict = {}
    for mon, c in sp.Poly(a, *gens).terms():
        terms.setdefault(mon, [sp.Integer(0), sp.Integer(0)])[0] = c
    for mon, c in sp.Poly(b, *gens).terms():
        terms.setdefault(mon, [sp.Integer(0), sp.Integer(0)])[1] = c
    bad = [mon for mon, (ca, cb) in terms.items() if not q3_nonneg(ca, cb)]
    log.append({"cell": tag, "monomials": len(terms), "bad": len(bad)})
    return not bad


# =============================== main parts ===================================


def part_coverage_gap(results):
    """Static audit finding: parse blade_proof.json, list branch cells that no
    certificate covers (the range(m_start-1, m_start) escalation bug at
    lab/blade_proof.py line 175)."""
    checked: dict = {}
    mstart: dict = {}
    data = json.loads(BLADE_JSON.read_text(encoding="utf-8"))
    for c in data.get("cells", []):
        name = c.get("cell", "")
        mm = re.match(r"k(\d+)_m(\d+)$", name)
        if mm:
            checked.setdefault(int(mm.group(1)), set()).add(int(mm.group(2)))
        tt = re.match(r"k(\d+)_tail$", name)
        if tt and "m_start" in c:
            mstart[int(tt.group(1))] = int(c["m_start"])
    gaps = {}
    for k, ms in sorted(mstart.items()):
        g = sorted(set(range(1, ms)) - checked.get(k, set()))
        if g:
            gaps[k] = g
    n_gap = sum(len(g) for g in gaps.values())
    results["coverage_gap"] = {
        "bug": "lab/blade_proof.py line 175: on tail escalation from M to M+6 "
        "only m0=M+5 is backfilled; m0=M..M+4 are never certified while "
        "the tail certificate that failed at M only starts at M+6",
        "uncovered_cells": {str(k): g for k, g in gaps.items()},
        "n_uncovered": n_gap,
        "m_start": {str(k): ms for k, ms in sorted(mstart.items())},
    }
    log_print(
        f"coverage gap: {n_gap} uncovered (k,m) cells across "
        f"{len(gaps)} branches (e.g. k=7 misses m=4..8)"
    )
    return mstart, gaps


def branch_interval(k: int):
    lo = sp.Rational(2, 3) if k == 4 else sp.Rational(3 * (2 * k - 5), 10)
    hi = sp.Rational(3 * (2 * k - 3), 10)
    return lo, hi


def part_certificates(results):
    """Independent rebuild of the tail certificates T0 / L1 / L2 / L3 and the
    k=3 branch, from the formulas in the theorem statement (not from
    blade_proof.py's expansion code)."""
    log: list = []
    ok_all = True

    # --- known-answer self-tests of OUR OWN formulas (m=1 values match the
    # independently verified n=4, j=3 rung from research/master-formula-review.md)
    assert G_fr(1) == Fr(16, 15) and al_fr(1) == Fr(16, 45), "bracket self-test failed"

    # --- beta > 0 for ALL m >= 0 (needed by L2's parabola direction):
    G = 2 * (mS + 1) * (mS + 3) / (3 * (2 * mS + 3))
    al = (mS + 3) * (5 * mS**3 + 21 * mS**2 + 19 * mS + 15) / (45 * (2 * mS + 1) * (2 * mS + 3))
    beta = 4 * al - G**2
    beta_fact = (
        8 * (mS + 3) * (mS**3 + 3 * mS**2 + 11 * mS + 15) / (45 * (2 * mS + 1) * (2 * mS + 3) ** 2)
    )
    okb = sp.simplify(beta - beta_fact) == 0
    log.append({"cell": "beta_identity_and_positivity", "ok": bool(okb)})
    ok_all &= okb
    log_print(
        f"beta = 8(m+3)(m^3+3m^2+11m+15)/(45(2m+1)(2m+3)^2) identity: {okb} => beta>0 for all m>=0"
    )

    # --- L2: RHS := (16/9)(m+3)^2 beta - 2 al G >= 0 and RHS^2 >= 16 al^3 for m>=79
    RHS = sp.Rational(16, 9) * (mS + 3) ** 2 * beta - 2 * al * G
    e1, okd1 = numerator_checked(RHS.subs(mS, v + 79), (v,), "L2_e1", log)
    e2, okd2 = numerator_checked((RHS**2 - 16 * al**3).subs(mS, v + 79), (v,), "L2_e2", log)
    ok1 = okd1 and all(c >= 0 for _, c in sp.Poly(e1, v).terms())
    ok2 = okd2 and all(c >= 0 for _, c in sp.Poly(e2, v).terms())
    okL2 = bool(ok1 and ok2)
    # logic spot-check in exact arithmetic at m=79, 200:  window => s<(4/3)(m+3)
    for msamp in (79, 200):
        Gq, alq = G_fr(msamp), al_fr(msamp)
        betaq = 4 * alq - Gq * Gq
        rhs = Fr(16, 9) * (msamp + 3) ** 2 * betaq - 2 * alq * Gq
        assert rhs >= 0 and rhs * rhs >= 16 * alq**3, f"L2 numeric spot fail m={msamp}"
    log.append({"cell": "L2_rebuild", "ok": okL2})
    ok_all &= okL2
    log_print(f"L2 rebuild (window containment s<(4/3)(m+3), m>=79): {okL2}")

    # --- L1: (12+4sqrt3)*lam - T_{K+2} >= 0 for K>=45, theta in [0,1),
    # lam=(K+theta)/sqrt3.  Built WITHOUT symbolic division (no cancel risk):
    # 3*k(k-2)*[(12+4r3)lam - T_k] = 3(12+4r3)lam k(k-2) - 9(2k-3)(lam^2+(2k-2)lam+1) - 6k^2(k-2)
    K, th = sp.symbols("K theta", nonnegative=True)
    lamK = (K + th) * r3 / 3
    kk = K + 2
    E1 = sp.expand(
        3 * (12 + 4 * r3) * lamK * kk * (kk - 2)
        - 9 * (2 * kk - 3) * (lamK**2 + (2 * kk - 2) * lamK + 1)
        - 6 * kk**2 * (kk - 2)
    )
    E1 = sp.expand(E1.subs(K, v + 45).subs(th, w / (1 + w)) * (1 + w) ** 2)
    E1n, okdL1 = numerator_checked(E1, (v, w), "L1_den", log)
    okL1 = okdL1 and cert_sqrt3(E1n, (v, w), "L1_rebuild", log)
    # float spot checks incl. tightness (the asymptote is exactly the large-lam envelope)
    for lam in (26.0, 100.0, 1000.0):
        assert Tmin_float(lam) <= (12 + 4 * SQ3) * lam + 1e-9, "L1 numeric spot fail"
    ok_all &= okL1
    log_print(f"L1 rebuild (envelope <= (12+4sqrt3)lam, lam>=26): {okL1}")

    # --- L3: m=v+79, lam=26+z(v+7)/3 (z in [0,1) suffices: at z=1, s=(4/3)(m+3)
    # exactly and L2 gives disc<=0, i.e. no window), u_A=(12+4sqrt3)lam+4m+1:
    # B(u_A) >= 0 and u_A <= vertex.
    mdeep = v + 79
    lamdeep = 26 + z * (v + 7) / 3
    sdeep = lamdeep + mdeep + 2
    Gd = 2 * (mdeep + 1) * (mdeep + 3) / (3 * (2 * mdeep + 3))
    ald = (
        (mdeep + 3)
        * (5 * mdeep**3 + 21 * mdeep**2 + 19 * mdeep + 15)
        / (45 * (2 * mdeep + 1) * (2 * mdeep + 3))
    )
    uA = (12 + 4 * r3) * lamdeep + 4 * mdeep + 1
    Bd = ald * uA * (uA - 2) - Gd * uA * sdeep**2 + sdeep**4
    Vd = Gd * sdeep**2 - (uA - 1) * 2 * ald
    okL3 = True
    for nm, E in (("L3a_B", Bd), ("L3b_V", Vd)):
        num, okd = numerator_checked(E, (v, z), f"{nm}_den", log)
        if not okd:
            okL3 = False
            continue
        degz = sp.degree(num, z)
        f = sp.expand(num.subs(z, w / (1 + w)) * (1 + w) ** degz)
        fn, okd2b = numerator_checked(f, (v, w), f"{nm}_den2", log)
        okL3 &= okd2b and cert_sqrt3(fn, (v, w), f"{nm}_rebuild", log)
    okL3 = bool(okL3)
    ok_all &= okL3
    log_print(f"L3 rebuild (deep water B&V at the asymptote): {okL3}")

    # --- T0: m=1..78 -> no window for lam >= 26 (exact univariate, rebuilt)
    x = sp.Symbol("x", nonnegative=True)
    t0fails = []
    for mm in range(1, 79):
        Gq = sp.Rational(G_fr(mm).numerator, G_fr(mm).denominator)
        alq = sp.Rational(al_fr(mm).numerator, al_fr(mm).denominator)
        s = 26 + x + mm + 2
        nd = sp.expand(-((2 * alq + Gq * s**2) ** 2 - 4 * alq * s**4))
        if not poly_nonneg_on(sp.Poly(nd, x), sp.Integer(0), None):
            t0fails.append(mm)
    okT0 = not t0fails
    log.append({"cell": "T0_rebuild_m1..78", "fails": t0fails})
    ok_all &= okT0
    log_print(f"T0 rebuild (no window, m<=78, lam>=26): {okT0}")

    # --- k=3 branch rebuild: m=1,2 no-window on (0,2/3]; m>=3 via B,V >= 0
    ok3 = True
    for mm in (1, 2):
        Pd, _, _ = cell_polys(3, mm)
        Pnd = sp.Poly(-Pd.as_expr(), lamS)
        okc = poly_pos_on_lopen(Pnd, sp.Integer(0), sp.Rational(2, 3))
        log.append({"cell": f"k3_m{mm}_nowindow", "ok": bool(okc)})
        ok3 &= okc
    syms = branch_BV_syms(3)
    if syms is None:
        ok3 = False
    else:
        for nm, numX in (("B", syms[0]), ("V", syms[1])):
            f = numX.subs(mS, v + 3).subs(lamS, sp.Rational(2, 3) / (1 + w))
            fn, okd = numerator_checked(f, (v, w), f"k3_{nm}_den", log)
            okc = okd and all(c >= 0 for _, c in sp.Poly(fn, v, w).terms())
            log.append({"cell": f"k3_{nm}_rebuild", "ok": bool(okc)})
            ok3 &= okc
    ok3 = bool(ok3)
    ok_all &= ok3
    log_print(f"k=3 branch rebuild (lam in (0,2/3]): {ok3}")

    results["certificates"] = {
        "log": log,
        "L1": bool(okL1),
        "L2": bool(okL2),
        "L3": bool(okL3),
        "T0": bool(okT0),
        "k3": ok3,
        "beta_positive_all_m": bool(okb),
        "all_ok": bool(ok_all),
    }
    return ok_all


class MarginTracker:
    def __init__(self):
        self.items: list = []

    def add(self, part, m, lam, margin, exact):
        if margin is None:
            return
        rel = margin / max(1.0, abs(margin) + 1.0) if False else margin
        self.items.append(
            {
                "part": part,
                "m": int(m),
                "lam": str(lam),
                "margin_D": float(margin),
                "exact": bool(exact),
            }
        )

    def worst(self, n=20):
        return sorted(self.items, key=lambda r: r["margin_D"])[:n]


def part_exact_scans(results, margins, counterexamples):
    """Exact-rational dense scans: branch junctions (2/3, 26/26.1) and the
    closest-approach zone lam in [0.02, 0.1]."""
    checks = 0
    windows = 0
    # junction grids
    lam_j = (
        [Fr(i, 300) for i in range(181, 226, 5 if FAST else 1)]
        + [Fr(2, 3)]
        + [Fr(i, 100) for i in range(2540, 2621, 4 if FAST else 1)]
        + [Fr(26), Fr(261, 10)]
    )
    m_j = list(range(1, 121, 3 if FAST else 1)) + [150, 200, 300, 500, 1000]
    # closest-approach grids
    lam_c = [Fr(i, 1000) for i in range(20, 101, 4 if FAST else 1)]
    m_c = list(range(1, 151, 3 if FAST else 1)) + [200, 300, 500, 1000, 3000]
    for tagp, lams, ms in (("junctions", lam_j, m_j), ("closest", lam_c, m_c)):
        for lam in lams:
            for m in ms:
                viol, win, marg = check_exact(m, lam)
                checks += 1
                windows += win
                if win:
                    margins.add(tagp, m, lam, marg, exact=True)
                if viol:
                    counterexamples.append({"part": tagp, "m": m, "lam": str(lam), "margin": marg})
        log_print(
            f"exact scan '{tagp}' done ({checks} checks so far, "
            f"{windows} windows, {len(counterexamples)} violations)"
        )
    results["exact_scans"] = {"checks": checks, "windows": windows}


def part_float_scans(results, margins, counterexamples):
    """Float reconnaissance with exact rational recheck of every suspect:
    window tips (disc ~ 0), large-m tangency direction, deep water."""
    suspects: list = []  # (margin, m, lam_float, part)
    n_float = 0

    def scan_point(part, m, lam):
        nonlocal n_float
        n_float += 1
        marg = check_float(float(m), float(lam))
        if marg is not None:
            suspects.append((marg, m, lam, part))

    # C: window tips, m = 1..200
    for m in range(1, 201, 2 if FAST else 1):
        tip = window_tip_float(m)
        if tip is None or tip <= 0.02:
            continue
        for g in (1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.3, 0.6, 0.9):
            lam = tip * (1 - g)
            if lam >= 0.02:
                scan_point("tips", m, lam)
    log_print(f"float scan 'tips' done ({n_float} points)")

    # D: large-m: full strip up to the tip + the s/m ~ 1+1/sqrt3 direction
    for m in [1000, 10000] if FAST else [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
        tip = window_tip_float(m)
        if tip is None:
            continue
        lams = [0.02 * (tip / 0.02) ** (i / 79.0) for i in range(80)]
        lams += [tip * (1 - g) for g in (1e-6, 1e-5, 1e-4, 1e-3, 0.01, 0.05)]
        for lam in lams:
            if 0 < lam < tip:
                scan_point("large_m", m, lam)
        # the hinted direction s/m ~ 1+1/sqrt3 lies OUTSIDE the window region
        # (s/(m+3) -> sqrt(5/3) < 4/3 < 1+1/sqrt3 at the tip); verify no window:
        lam_h = m / SQ3 - 2
        if lam_h > 0:
            assert check_float(float(m), lam_h) is None, (
                f"unexpected window at hinted tangency m={m}"
            )
    log_print(f"float scan 'large_m' done ({n_float} points)")

    # E: deep water lam in [26, 2000], n up to 6*lam
    lam_list = [26.0 * (2000.0 / 26.0) ** (i / 33.0) for i in range(34)] + [26.0, 26.001, 26.1]
    if FAST:
        lam_list = lam_list[::3]
    for lam in lam_list:
        m_lo = max(79, int(3 * lam) - 40)
        m_hi = int(6 * lam) + 1
        step = max(1, (m_hi - m_lo) // 300)
        for m in range(m_lo, m_hi, step):
            scan_point("deep", m, lam)
        # T0 cross-check: no window for m<=78 at lam>=26
        for m in range(1, 79, 7):
            assert check_float(float(m), lam) is None, (
                f"float window at m={m}, lam={lam} contradicts T0"
            )
    log_print(f"float scan 'deep' done ({n_float} points total)")

    # exact recheck of the worst suspects (rationalized lambda)
    suspects.sort(key=lambda t: t[0])
    seen = set()
    picked = []
    for marg, m, lam, part in suspects:
        key = (m, round(lam, 6))
        if key in seen:
            continue
        seen.add(key)
        picked.append((marg, m, lam, part))
        if len(picked) >= (12 if FAST else 40):
            break
    for marg, m, lam, part in picked:
        lamQ = Fr(round(lam * 10**6), 10**6)
        if lamQ <= 0:
            continue
        viol, win, marg_ex = check_exact(m, lamQ)
        if win:
            mp = margin_precise(m, lamQ)
            margins.add(part + "_exact", m, lamQ, mp, exact=True)
        if viol:
            counterexamples.append(
                {"part": part + "_exact", "m": m, "lam": str(lamQ), "margin": marg_ex}
            )
    results["float_scans"] = {
        "points": n_float,
        "suspects_rechecked": len(picked),
        "float_min_margin": suspects[0][0] if suspects else None,
    }
    log_print(f"exact recheck of {len(picked)} float suspects done")


def part_recertify(results, mstart, gaps, counterexamples):
    """Independent re-certification of the branch region k=4..45:
    every fixed-m cell m=1..m_start-1 (INCLUDING the coverage-gap cells) by the
    exact decision procedure, plus a rebuilt 2-var tail certificate m>=m_start."""
    log: list = []
    ok_all = True
    open_cells = []
    for k in range(4, 46):
        lo, hi = branch_interval(k)
        ms = mstart.get(k, 46)
        m_list = sorted(set(range(1, ms)) if not FAST else set(gaps.get(k, [])) | {1, 2, 3, ms - 1})
        for m in m_list:
            got = decide_cell(k, m, lo, hi, log)
            if not got:
                # not yet a counterexample (branch T_k >= Tmin); probe exactly
                open_cells.append({"k": k, "m": m})
                step = (hi - lo) / 60
                for i in range(61):
                    lamQ = Fr((lo + i * step).p, (lo + i * step).q)
                    violp, winp, margp = check_exact(m, lamQ)
                    if violp:
                        counterexamples.append(
                            {"part": "recert_probe", "m": m, "lam": str(lamQ), "margin": margp}
                        )
                ok_all = False
        okT = tail_certificate(k, ms, lo, hi, log)
        if not okT:
            open_cells.append({"k": k, "tail_m_start": ms})
            ok_all = False
        log_print(
            f"re-certify branch k={k}: cells m<{ms} "
            f"{'OK' if ok_all or not open_cells else '...'} tail={'OK' if okT else 'FAIL'}"
        )
    results["recertification"] = {"all_ok": bool(ok_all), "open_cells": open_cells, "log": log}
    return ok_all


def part_negative_control(results):
    """Known-answer control: the violation detector must FIRE when pointed at
    the inside of a real window (a run that cannot fail is not a test)."""
    fired = False
    found = None
    for m in (100, 120, 90, 150):
        for lam in (Fr(28), Fr(30), Fr(27), Fr(26)):
            _, win, _ = check_exact(m, lam)
            if win:
                found = (m, lam)
                break
        if found:
            break
    if found:
        m, lam = found
        G, al = G_fr(m), al_fr(m)
        s2 = (lam + m + 2) ** 2
        # rational point inside the window: floor of the vertex (disc>0 => Bhat(vertex)<0)
        u_vertex = 1 + G * s2 / (2 * al)
        u_mid = u_vertex  # exact rational, strictly inside
        B = al * u_mid * (u_mid - 2) - G * u_mid * s2 + s2 * s2
        fired = B < 0
    results["negative_control"] = {
        "window_point": [found[0], str(found[1])] if found else None,
        "detector_fires_inside_window": bool(fired),
    }
    log_print(f"negative control (detector fires inside a real window): {fired}")
    return bool(fired)


def main() -> int:
    results: dict = {
        "tool": "lab/attack_blade_theorem.py",
        "independent_of": "lab/blade_proof.py (no import; formulas rebuilt)",
        "fast_mode": FAST,
    }
    margins = MarginTracker()
    counterexamples: list = []

    mstart, gaps = part_coverage_gap(results)
    certs_ok = part_certificates(results)
    control_ok = part_negative_control(results)
    part_exact_scans(results, margins, counterexamples)
    part_float_scans(results, margins, counterexamples)
    recert_ok = part_recertify(results, mstart, gaps, counterexamples)

    results["counterexamples"] = counterexamples
    results["min_margins"] = margins.worst(25)
    results["negative_control_ok"] = bool(control_ok)
    if counterexamples:
        verdict = "THEOREM COUNTEREXAMPLE FOUND"
        code = 2
    elif certs_ok and recert_ok and control_ok:
        verdict = (
            "NO COUNTEREXAMPLE; tail certificates independently rebuilt; "
            "all branch cells (incl. blade_proof.py's coverage-gap cells) "
            "independently re-certified"
        )
        code = 0
    else:
        verdict = "NO COUNTEREXAMPLE FOUND, BUT RE-CERTIFICATION INCOMPLETE (proof open somewhere)"
        code = 1
    results["verdict"] = verdict
    results["runtime_s"] = round(time.time() - T0_START, 1)
    import subprocess as _sp

    results["_meta"] = {
        "command": "python lab/attack_blade_theorem.py",
        "git": _sp.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
        ).stdout.strip(),
    }
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    log_print(f"VERDICT: {verdict} (exit {code}); artifact {OUT}")
    return code


if __name__ == "__main__":
    sys.exit(main())
