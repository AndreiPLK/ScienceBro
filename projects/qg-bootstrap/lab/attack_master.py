"""Adversarial, independent attack on the Master Positivity Formula (paper 3).

Role: domain-critic. Everything below is written from scratch against the
STATEMENT of the claim (research/master-formula.md, paper3/main.tex), not
against the lab's implementation. It does NOT import lab/tj_bracket.py,
lab/t2n6_bracket.py, lab/grav_full_body.py or any other lab module.

What it checks
  A. Integral identity  I(l+2u,l)/I(l,l) = (l+2u)!/(l! u! 4^u (alpha+l+1)_u)
     as an identity of rational functions of alpha: exact evaluation at more
     rational points than the degree bound of the cross-multiplied difference
     (cleared of Pochhammer denominators the difference is a polynomial in
     alpha of degree <= 2l+2u; equality at > 2l+2u distinct points where the
     denominators are nonzero forces it to vanish identically). This is a
     genuine finite proof for every (l,u) tested, l<=10, u<=6.
  B. Known-answer, negative and zero controls for the from-scratch evaluator
     (hand-computed: a_{3,2}(lam=1,D=4) evaluates to exactly 48/7 in this
     normalisation; a_{3,2}=0 exactly at D=T_3(1)=24; a_{3,2}<0 at D=26).
  C. Sign grid: master formula vs an independent exact-rational partial-wave
     evaluator built directly from the CHR residue definition
     (Q(x)=prod_{k=1}^{n-1}(s x + 2k - n), s=lam+n-1, weight
     (1-x^2)^{alpha-1/2}, alpha=(D-3)/2; all monomial moments as exact
     Pochhammer ratios, valid for ODD and non-integer D as well).
     Coverage: all j=2..n-1 for n=3..12; D in {4,5,6,7,8,11,12,23,24,25,36,37}
     (odd D included -- the lab's scans were even-D only); extreme
     lambda 1/100 and 100; non-integer D (7/2, 53/7); deep levels n=14,15
     including l=2 (j=n-1); the string window at n=7 (odd D inside it).
  D. j=2 root test (proportionality, not just sign): the linear j=2 bracket
     root D*(n,lam) must equal the published T_n(lam) exactly, AND the
     independent evaluator must vanish EXACTLY at the (generally non-integer)
     rational D*.
  E. Boundary extrapolation j=n (l=0): NOT claimed by the paper (paper stops
     at j=n-1). Tested and reported for information only; excluded from the
     exit code.

Exit 0 <=> no falsification found in A-D.
Artifact: results/attack_master.json (new file, nothing overwritten).

Run:
  C:/Users/user/ScienceBro/.venv/Scripts/python.exe \
      projects/qg-bootstrap/lab/attack_master.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from functools import cache
from math import factorial
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"


def sgn(x):
    return (x > 0) - (x < 0)


def poch(a, k):
    p = F(1)
    for i in range(k):
        p *= a + i
    return p


@cache
def gegen(l, alpha):
    """Coefficients (index = power of x) of Gegenbauer C_l^{(alpha)} via the
    standard recurrence m C_m = 2(m-1+alpha) x C_{m-1} - (m-2+2alpha) C_{m-2}."""
    if l == 0:
        return (F(1),)
    prev, cur = (F(1),), (F(0), 2 * F(alpha))
    for m in range(2, l + 1):
        new = [F(0)] * (m + 1)
        for i, c in enumerate(cur):
            if c:
                new[i + 1] += 2 * (m - 1 + alpha) * c / m
        for i, c in enumerate(prev):
            if c:
                new[i] -= (m - 2 + 2 * alpha) * c / m
        prev, cur = cur, tuple(new)
    return cur


@cache
def jnorm(k, alpha):
    """int_{-1}^1 x^k (1-x^2)^{alpha-1/2} dx / int_{-1}^1 (1-x^2)^{alpha-1/2} dx
    = (1/2)_m / (alpha+1)_m for k=2m (Beta-function ratio), 0 for odd k.
    Exact rational for any rational alpha > -1/2 (D > 2)."""
    if k % 2:
        return F(0)
    m = k // 2
    return poch(F(1, 2), m) / poch(alpha + 1, m)


@cache
def residue_sq(n, s):
    """Coefficients of Q(x)^2 with Q = prod_{k=1}^{n-1} (s x + 2k - n).
    Equals the CHR level-n residue R(n, t(x)) up to a strictly positive
    prefactor for lam > 0 (verified by direct Pochhammer expansion with
    t = -(mu/2)(1-x), mu = (n+lam-1)/lam)."""
    q = [F(1)]
    for k in range(1, n):
        c0 = F(2 * k - n)
        new = [F(0)] * (len(q) + 1)
        for i, c in enumerate(q):
            new[i] += c * c0
            new[i + 1] += c * s
        q = new
    p = [F(0)] * (2 * len(q) - 1)
    for i, a in enumerate(q):
        for j, b in enumerate(q):
            p[i + j] += a * b
    return tuple(p)


def pw_value(n, l, lam, D):
    """Sign-faithful partial wave: equals a_{n,l} up to a strictly positive
    factor (residue prefactor, Gegenbauer norm, weight norm) for lam>0, D>3."""
    alpha = (F(D) - 3) / 2
    if alpha <= 0:
        raise ValueError("evaluator requires D > 3")
    s = F(lam) + n - 1
    p = residue_sq(n, s)
    c = gegen(l, alpha)
    val = F(0)
    for i, ci in enumerate(c):
        if not ci:
            continue
        for k, pk in enumerate(p):
            if pk:
                val += ci * pk * jnorm(i + k, alpha)
    return val


@cache
def ehat(n):
    """E_{2t}(n) = |e_{2t}| of the doubled multiset {n-2k : k=1..n-1}
    (generating polynomial prod_k (1 + (n-2k) z)^2); index = t.
    Also asserts the sign pattern coeff(z^{2t}) = (-1)^t E_{2t}, odd coeffs 0.
    NOTE: the display in paper3/main.tex Sec. 2 carries an extra (-1)^t and is
    wrong as printed; the definition used here is the |e_{2t}| one from
    research/master-formula.md."""
    poly = [1]
    for k in range(1, n):
        r = n - 2 * k
        fac = [1, 2 * r, r * r]  # (1 + r z)^2
        new = [0] * (len(poly) + 2)
        for i, c in enumerate(poly):
            if c:
                for j, d in enumerate(fac):
                    new[i + j] += c * d
        poly = new
    for m, c in enumerate(poly):
        if m % 2:
            assert c == 0, ("odd coeff nonzero", n, m)
        else:
            assert c * (-1) ** (m // 2) >= 0, ("sign pattern broken", n, m)
    return tuple(abs(poly[2 * t]) for t in range(n))


def bracket(n, j, lam, D):
    """The master-formula ladder sum, exactly as stated in the claim."""
    e = ehat(n)
    s = F(lam) + n - 1
    tot = F(0)
    for i in range(j):
        term = (
            F((-1) ** i)
            * e[j - 1 - i]
            * F(factorial(2 * n - 2 * j + 2 * i), factorial(i) * 2**i)
            * s ** (2 * i)
        )
        for r in range(i, j - 1):
            term *= F(D) + 4 * n - 4 * j - 1 + 2 * r
        tot += term
    return tot


def predicted_sign(n, j, lam, D):
    return (-1) ** (j - 1) * sgn(bracket(n, j, lam, D))


def t_published(n, lam):
    """T_n(lam) from paper 2 (as encoded in the repo's completeness scan):
    T_n = 3(2n-3)/(n(n-2)) (lam^2 + (2n-2)lam + 1) + 2n. Used as an external
    cross-reference for the j=2 rung; exact rational."""
    lam = F(lam)
    return F(3 * (2 * n - 3), n * (n - 2)) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n


def j2_root(n, lam):
    """Exact root in D of the linear j=2 master bracket."""
    e = ehat(n)
    s = F(lam) + n - 1
    lead = F(e[1] * factorial(2 * n - 4))
    sub = F(factorial(2 * n - 2), 2) * s * s
    return sub / lead - (4 * n - 9)


# ----------------------------------------------------------------------------


def part_a_identity(report):
    alphas = sorted(
        set([F(k, 7) for k in range(1, 41)] + [F(1, 100), F(1, 3), F(5, 2), F(100), F(999, 7)])
    )
    fails, checks = [], 0
    for l in range(0, 11):
        for u in range(0, 7):
            # interpolation bound: need > 2l+2u distinct sample points
            assert len(alphas) > 2 * l + 2 * u
            for a in alphas:
                cs = gegen(l, a)
                iu = sum(ci * jnorm(i + l + 2 * u, a) for i, ci in enumerate(cs) if ci)
                i0 = sum(ci * jnorm(i + l, a) for i, ci in enumerate(cs) if ci)
                assert i0 > 0, ("I(l,l) must be positive", l, str(a))
                rhs = F(factorial(l + 2 * u), factorial(l) * factorial(u) * 4**u) / poch(
                    a + l + 1, u
                )
                checks += 1
                if iu != i0 * rhs:
                    fails.append({"l": l, "u": u, "alpha": str(a)})
    report["identity"] = {
        "checks": checks,
        "fails": fails,
        "note": "per (l,u): equality at > 2l+2u rational alpha points = rational-function identity",
    }
    return [f"identity fail {f}" for f in fails]


def part_b_controls(report):
    bad = []
    ka = pw_value(3, 2, F(1), F(4))
    if ka != F(48, 7):
        bad.append(f"known-answer: a_(3,2)(1,4) = {ka} != 48/7")
    if not (pw_value(3, 2, F(1), F(26)) < 0):
        bad.append("negative control failed: a_(3,2)(lam=1,D=26) not < 0")
    if pw_value(3, 2, F(1), F(24)) != 0:
        bad.append("zero control failed: a_(3,2)(lam=1,D=24) != 0")
    if bracket(3, 2, F(1), F(24)) != 0:
        bad.append("zero control failed: j=2 bracket (n=3,lam=1,D=24) != 0")
    report["controls"] = {"known_answer_48_7": str(ka), "failures": bad}
    return bad


def compare(n, j, lam, D):
    a = pw_value(n, 2 * n - 2 * j, lam, D)
    pred = predicted_sign(n, j, lam, D)
    return sgn(a), pred


def part_c_sign_grid(report, t0):
    mismatches = []
    total = 0
    tallies = {
        "odd_D": [0, 0],
        "even_D": [0, 0],
        "noninteger_D": [0, 0],
        "lam_extreme": [0, 0],
        "deep_n": [0, 0],
        "zeros_seen": 0,
    }

    def record(n, j, lam, D, deep=False):
        nonlocal total
        sa, pred = compare(n, j, lam, D)
        total += 1
        ok = sa == pred
        Df = F(D)
        if Df.denominator != 1:
            key = "noninteger_D"
        elif Df.numerator % 2:
            key = "odd_D"
        else:
            key = "even_D"
        tallies[key][0] += ok
        tallies[key][1] += 1
        if F(lam) in (F(1, 100), F(100)):
            tallies["lam_extreme"][0] += ok
            tallies["lam_extreme"][1] += 1
        if deep:
            tallies["deep_n"][0] += ok
            tallies["deep_n"][1] += 1
        if sa == 0:
            tallies["zeros_seen"] += 1
        if not ok:
            mismatches.append(
                {
                    "n": n,
                    "j": j,
                    "lam": str(lam),
                    "D": str(D),
                    "sign_evaluator": sa,
                    "sign_master": pred,
                }
            )

    lams = [F(1, 100), F(1, 4), F(1), F(3), F(7), F(100)]
    ds = [4, 5, 6, 7, 8, 11, 12, 23, 24, 25, 36, 37]
    for n in range(3, 13):
        for j in range(2, n):
            for lam in lams:
                for D in ds:
                    record(n, j, lam, D)
        print(f"  main grid n={n} done, cumulative {total} ({time.time() - t0:.0f}s)", flush=True)

    for n, jlist in ((14, [2, 5, 9, 13]), (15, [2, 7, 10, 14])):
        for j in jlist:
            for lam in (F(1, 100), F(1), F(100)):
                for D in (5, 24, 37):
                    record(n, j, lam, D, deep=True)
    print(f"  deep n=14,15 done, cumulative {total} ({time.time() - t0:.0f}s)", flush=True)

    for n in (4, 7):
        for j in range(2, n):
            for lam in (F(1), F(3)):
                for D in (F(7, 2), F(53, 7)):
                    record(n, j, lam, D)
    print(f"  non-integer D done, cumulative {total} ({time.time() - t0:.0f}s)", flush=True)

    report["sign_grid"] = {
        "total": total,
        "mismatches": mismatches,
        "tallies": {
            k: (v if isinstance(v, int) else {"ok": v[0], "n": v[1]}) for k, v in tallies.items()
        },
    }
    return [f"sign mismatch {m}" for m in mismatches]


def part_c2_window(report):
    bad, rows = [], []
    paper_claim = {26: 1, 28: -1, 30: -1, 32: 1}  # a_{7,8} signs, lam=1
    for D in range(26, 33):
        sa, pred = compare(7, 3, F(1), D)
        rows.append({"D": D, "sign_evaluator": sa, "sign_master": pred})
        if sa != pred:
            bad.append(f"window n=7 D={D}: evaluator {sa} vs master {pred}")
        if D in paper_claim and sa != paper_claim[D]:
            bad.append(f"paper window claim broken at D={D}: got {sa}, paper says {paper_claim[D]}")
    report["window_n7_lam1"] = {"rows": rows, "failures": bad}
    return bad


def part_d_root(report):
    bad = []
    cases = 0
    for n in range(3, 11):
        for lam in (F(1, 3), F(1), F(5, 2)):
            cases += 1
            dstar = j2_root(n, lam)
            if dstar != t_published(n, lam):
                bad.append(
                    f"j2 root != published T_n at n={n}, lam={lam}: "
                    f"{dstar} vs {t_published(n, lam)}"
                )
            if bracket(n, 2, lam, dstar) != 0:
                bad.append(f"bracket not zero at its own root, n={n} lam={lam}")
            if dstar > 3:
                if pw_value(n, 2 * n - 4, lam, dstar) != 0:
                    bad.append(f"evaluator NOT zero at bracket root: n={n}, lam={lam}, D*={dstar}")
            else:
                bad.append(f"unexpected D* <= 3 at n={n}, lam={lam}")
    report["j2_root"] = {
        "cases": cases,
        "failures": bad,
        "note": "root of linear j=2 bracket == T_n(lam) and "
        "exact zero of the independent evaluator",
    }
    return bad


def part_e_boundary(report):
    rows, agree = [], 0
    total = 0
    for n in range(3, 11):
        for lam in (F(1, 4), F(1), F(7)):
            for D in (4, 5, 24, 25):
                sa, pred = compare(n, n, lam, D)  # j = n, l = 0: EXTRAPOLATION
                total += 1
                agree += sa == pred
                if sa != pred:
                    rows.append(
                        {"n": n, "lam": str(lam), "D": D, "sign_evaluator": sa, "sign_master": pred}
                    )
    report["boundary_j_eq_n_extrapolation"] = {
        "total": total,
        "agree": agree,
        "mismatches": rows,
        "note": "outside the paper's claimed domain (paper stops at j=n-1); "
        "critic's derivation predicts the formula extends to j=n; "
        "informational only, excluded from exit code",
    }


def main() -> int:
    t0 = time.time()
    report = {}
    falsifications = []

    print("A. integral identity (rational-function proof by interpolation)", flush=True)
    falsifications += part_a_identity(report)
    print(
        f"   done ({time.time() - t0:.0f}s), fails: {len(report['identity']['fails'])}", flush=True
    )

    print("B. evaluator controls (known-answer 48/7, negative, zero)", flush=True)
    falsifications += part_b_controls(report)

    print("C. sign grid master vs independent evaluator", flush=True)
    falsifications += part_c_sign_grid(report, t0)
    falsifications += part_c2_window(report)

    print("D. j=2 root/proportionality test", flush=True)
    falsifications += part_d_root(report)

    print("E. j=n (l=0) boundary extrapolation (informational)", flush=True)
    part_e_boundary(report)

    try:
        git = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).resolve().parents[3],
        ).stdout.strip()
    except Exception:
        git = "unavailable"
    report["meta"] = {
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
        "command": "python projects/qg-bootstrap/lab/attack_master.py",
        "falsified": bool(falsifications),
        "falsifications": falsifications,
    }
    RES.mkdir(exist_ok=True)
    (RES / "attack_master.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

    print()
    if falsifications:
        print(f"FALSIFIED: {len(falsifications)} finding(s):")
        for f_ in falsifications:
            print("  -", f_)
        print("artifact: results/attack_master.json")
        return 1
    print("NO FALSIFICATION FOUND.")
    print(f"  identity checks: {report['identity']['checks']}")
    print(
        f"  sign grid: {report['sign_grid']['total']} comparisons, "
        f"0 mismatches (tallies: {report['sign_grid']['tallies']})"
    )
    print(f"  j=2 root cases: {report['j2_root']['cases']}, all exact zeros")
    be = report["boundary_j_eq_n_extrapolation"]
    print(f"  j=n extrapolation (info): {be['agree']}/{be['total']} agree")
    print("artifact: results/attack_master.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
