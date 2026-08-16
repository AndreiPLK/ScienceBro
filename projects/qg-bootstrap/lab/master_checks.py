"""Persisted verification battery for the master formula (paper 3, B1 fix).

Runs and RECORDS the three checks previously done inline:
  (1) symbolic bracket matches: master formula vs independently extracted
      brackets for j=2 (vs T_n law, n=3..11), j=3 (n=4..9), j=4 (n=5..10),
      j=5 (n=6, extracted HERE and persisted to results/T2n10_brackets.json);
  (2) the 16-monomial overdetermination at j=5, n=6;
  (3) the sign grid vs the exact evaluator (j=2..6 incl. blind j=6).
Artifact: results/master_checks.json. Exit 0 only if everything passes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from fractions import Fraction as F
from math import factorial
from pathlib import Path

import sympy as sp

LAB = Path(__file__).resolve().parent
RES = LAB.parent / "results"
sys.path.insert(0, str(LAB))
from hunt_2n8 import a_l  # noqa: E402  (exact evaluator, any l)

lam, D, s = sp.symbols('lam D s')


def e_doubled_int(n: int):
    poly = [1]
    for k in range(1, n):
        r = n - 2 * k
        for _ in range(2):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] += c * r
            poly = new
    return [abs(poly[2 * t]) for t in range(len(poly) // 2 + 1)]


def master_bracket(n: int, j: int):
    c = 4 * n - 4 * j - 1
    e = e_doubled_int(n)
    B = sp.Integer(0)
    for i in range(j):
        w = sp.Integer(factorial(2 * n - 2 * j + 2 * i)) / (
            factorial(i) * 2 ** i)
        tail = sp.prod(D + c + 2 * k for k in range(i, j - 1))
        B += (-1) ** i * e[j - 1 - i] * w * s ** (2 * i) * tail
    return sp.expand(B)


def master_sign(n: int, j: int, lamv: F, Dv: int) -> int:
    c = 4 * n - 4 * j - 1
    e = e_doubled_int(n)
    sv = lamv + n - 1
    B = F(0)
    for i in range(j):
        w = F(factorial(2 * n - 2 * j + 2 * i), factorial(i) * 2 ** i)
        tail = F(1)
        for k in range(i, j - 1):
            tail *= (Dv + c + 2 * k)
        B += (-1) ** i * e[j - 1 - i] * w * sv ** (2 * i) * tail
    if j % 2 == 0:
        B = -B
    return (B > 0) - (B < 0)


def extracted_bracket(numer_str: str, j: int):
    fac = sp.sympify(numer_str, locals={'lam': lam, 'D': D})
    for f, e in sp.factor_list(fac)[1]:
        if sp.degree(f, gen=D) == j - 1:
            return sp.expand(f)
    return None


def main() -> int:
    t0 = time.time()
    out = {"matches": [], "fails": []}

    # --- (1a) j=2 vs the published T_n law, n=3..11
    for n in range(3, 12):
        mb = master_bracket(n, 2)
        ref = sp.expand(3 * (2 * n - 3) * s ** 2
                        - n * (n - 2) * (D + 4 * n - 9))
        ratio = sp.simplify(mb / ref)
        (out["matches"] if ratio.is_constant() else out["fails"]).append(
            {"j": 2, "n": n, "scale": str(sp.nsimplify(ratio))})

    # --- (1b) j=3, j=4 vs extracted brackets
    for j, fname in ((3, "T2n6_brackets.json"), (4, "T2n8_brackets.json")):
        d = json.loads((RES / fname).read_text())
        for nk in sorted((k for k in d if k != "_meta"), key=int):
            n = int(nk)
            ex = extracted_bracket(d[nk]["numerator_factored"], j)
            ex_s = sp.expand(ex.subs(lam, s - (n - 1)))
            ratio = sp.simplify(ex_s / master_bracket(n, j))
            okc = ratio.is_constant() and sp.simplify(ratio) > 0
            (out["matches"] if okc else out["fails"]).append(
                {"j": j, "n": n, "scale": str(sp.nsimplify(ratio))})

    # --- (1c) j=5, n=6: extract HERE (persist) and match
    os.environ["TJ_J"] = "5"
    import importlib

    import tj_bracket
    importlib.reload(tj_bracket)
    fac, den = tj_bracket.bracket_for(6)
    (RES / "T2n10_brackets.json").write_text(json.dumps(
        {"6": {"numerator_factored": str(fac),
               "denominator_factored": str(den)},
         "_meta": {"command": "lab/master_checks.py (TJ_J=5, n=6)"}},
        indent=1), encoding="utf-8")
    ex = None
    for f, e in sp.factor_list(sp.expand(fac))[1]:
        if sp.degree(f, gen=tj_bracket.D) == 4:
            ex = sp.expand(f)
    ex_s = sp.expand(ex.subs(tj_bracket.lam, s - 5)).subs(tj_bracket.D, D)
    ratio = sp.simplify(ex_s / master_bracket(6, 5))
    okc = ratio.is_constant()
    (out["matches"] if okc else out["fails"]).append(
        {"j": 5, "n": 6, "scale": str(sp.nsimplify(ratio))})
    n_sym_matches = len(out["matches"])

    # --- (2) 16-monomial overdetermination at j=5, n=6
    p = sp.Poly(ex_s, D, s)
    mono = {k: v for k, v in p.as_dict().items()}
    mp = sp.Poly(master_bracket(6, 5), D, s).as_dict()
    scale = sp.nsimplify(ratio)
    over_ok = (len(mono) == 15 and
               all(sp.simplify(mono[k] - scale * mp[k]) == 0 for k in mono))
    out["monomial_overdetermination"] = {"monomials": len(mono), "dof": 5, "all_match": bool(over_ok)}

    # --- (3) sign grid vs exact evaluator (incl. blind j=6)
    lams = [F(1, 4), F(1, 2), F(1), F(3, 2), F(3), F(7)]
    cases = [(4, 2), (6, 2), (9, 2), (4, 3), (7, 3), (5, 4), (8, 4),
             (6, 5), (8, 5), (7, 6), (8, 6), (9, 6), (10, 6)]
    grid_checks, grid_mism = 0, 0
    for (n, j) in cases:
        for Dv in range(4, 37, 4):
            for lamv in lams:
                grid_checks += 1
                se = (lambda v: (v > 0) - (v < 0))(
                    a_l(n, 2 * n - 2 * j, lamv, Dv))
                if se != master_sign(n, j, lamv, Dv):
                    grid_mism += 1
    out["sign_grid"] = {"checks": grid_checks, "mismatches": grid_mism,
                        "blind_j6_cases": 4}

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out["_meta"] = {"command": "python lab/master_checks.py", "git": git,
                    "symbolic_matches": n_sym_matches,
                    "runtime_s": round(time.time() - t0, 1)}
    (RES / "master_checks.json").write_text(json.dumps(out, indent=1),
                                            encoding="utf-8")
    ok = (not out["fails"] and over_ok and grid_mism == 0)
    print(f"symbolic matches: {n_sym_matches}/{n_sym_matches + len(out['fails'])};"
          f" overdetermination 15/15: {over_ok};"
          f" sign grid: {grid_checks - grid_mism}/{grid_checks}", flush=True)
    print("PASS" if ok else "FAIL", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
