"""Persist every paper-cited computation as a reproducible artifact (fix for
release-review blockers 5-6): killer census, stack-wide comparison, dichotomy,
q-clock table + derivative, D-universality checks, fixed-spin tails to n=200.

Run: .venv/Scripts/python.exe -u projects/qg-bootstrap/lab/artifacts_battery.py
Writes: projects/qg-bootstrap/results/paper_artifacts.json (+ prints summary)
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from math import comb, log
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repro_r4_positivity_spot import a_route1  # noqa: E402
from fig1_island_map import point_allowed  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
OUT = {}


# ---------- 1. killer census (714 excluded cells, N=40 map) ----------
def census():
    d = json.loads((RES / "fig1_map_mu0_1_N40.json").read_text())
    from collections import Counter
    kinds = Counter()
    for row in d["rows"]:
        if row["allowed"] or row["first_negative"] is None:
            continue
        fn = row["first_negative"]
        kinds["domain" if fn[0] == "domain" else f"{fn[0]},{fn[1]}"] += 1
    OUT["killer_census_N40_mu0"] = dict(kinds)
    print(f"census: {sum(kinds.values())} excluded cells, "
          f"{len(kinds)} distinct killers", flush=True)


# ---------- 2. stack-wide comparison (the 11,994 verdicts) ----------
def verdict_analytic(r, w, mu0):
    if 1 + r == 0 or 1 + r + w == 0:
        return False
    n_min = 1
    while n_min + mu0 < 4 * mu0:
        n_min += 1
    for n in range(n_min, n_min + 5):
        for l in range(0, n + 1):
            try:
                if a_route1(n, l, r, w, mu0) < 0:
                    return False
            except ZeroDivisionError:
                return False
    edge = -(1 + mu0) / 2
    if r < edge and w > 0:
        return False
    if r == edge and w < 0:
        return False
    return True


def stack():
    files = [("fig1_map_mu-9_5.json", F(-9, 5)), ("fig1_map_mu-6_5.json", F(-6, 5)),
             ("fig1_map_mu-3_5.json", F(-3, 5)), ("fig1_map_mu0_1_N40.json", F(0)),
             ("fig1_map_mu3_5.json", F(3, 5)), ("fig1_map_mu6_5.json", F(6, 5)),
             ("fig1_map_mu9_5.json", F(9, 5))]
    total = 0
    doomed = []
    for name, mu in files:
        d = json.loads((RES / name).read_text())
        for row in d["rows"]:
            r, w = F(row["r"]), F(row["w"])
            pred = verdict_analytic(r, w, mu)
            total += 1
            if pred != row["allowed"]:
                doomed.append({"mu0": str(mu), "r": row["r"], "w": row["w"],
                               "map": row["allowed"], "analytic": pred})
    fine = json.loads((RES / "fine_boundary_mu0_N20_corrected.json").read_text())
    fine_mism = 0
    for row in fine["rows"]:
        if verdict_analytic(F(row["r"]), F(row["w"]), F(0)) != row["allowed"]:
            fine_mism += 1
    total += len(fine["rows"])
    OUT["stack_comparison"] = {
        "total_points": total, "coarse_discrepancies": len(doomed),
        "all_discrepancies_are_map_allowed_analytic_doomed":
            all(d_["map"] and not d_["analytic"] for d_ in doomed),
        "fine_mismatches": fine_mism, "doomed_cells": doomed}
    print(f"stack: {total} points, {len(doomed)} doomed-cell discrepancies, "
          f"{fine_mism} fine mismatches", flush=True)


# ---------- 3. odd/even dichotomy k=1..7 ----------
def dichotomy():
    w = F(3, 10)
    rows = []
    for k in range(1, 8):
        n = 40 + k
        s_out = a_route1(n, n - k, F(-55, 100), w, F(0))
        s_in = a_route1(n, n - k, F(-45, 100), w, F(0))
        rows.append({"k": k, "n": n,
                     "beyond_edge_sign": -1 if s_out < 0 else (0 if s_out == 0 else 1),
                     "inside_sign": -1 if s_in < 0 else (0 if s_in == 0 else 1)})
    # threshold confirmations
    thr = {"k3_crossover": {"r": "-13/25", "w": "1",
                            "sign_n55": 1 if a_route1(55, 52, F(-13, 25), F(1), F(0)) > 0 else -1,
                            "sign_n59": 1 if a_route1(59, 56, F(-13, 25), F(1), F(0)) > 0 else -1},
           "k1_w17_10": {"sign_n84": 1 if a_route1(84, 83, F(-13, 25), F(17, 10), F(0)) > 0 else -1,
                         "sign_n86": 1 if a_route1(86, 85, F(-13, 25), F(17, 10), F(0)) > 0 else -1}}
    OUT["dichotomy"] = {"table": rows, "thresholds": thr,
                        "note": "r=-0.55/-0.45 = -11/20,-9/20; k3/k1 thresholds at r=-13/25"}
    print("dichotomy: k=1..7 recorded", flush=True)


# ---------- 4. q-clock ----------
def qint(m, q):
    if q == 1:
        return F(m)
    if m >= 0:
        return sum(q ** k for k in range(m)) if m else F(0)
    return (F(1) / q ** (-m) - 1) / (q - 1)


def leg_coeffs(l):
    p0, p1 = [F(1)], [F(0), F(1)]
    if l == 0:
        return p0
    if l == 1:
        return p1
    for m in range(2, l + 1):
        xp = [F(0)] + p1
        new = [(2 * m - 1) * c / m for c in xp]
        for i, c in enumerate(p0):
            new[i] -= (m - 1) * c / m
        p0, p1 = p1, new
    return p1


def mono_int(k):
    return F(0) if k % 2 else F(2, k + 1)


def a_q(n, l, q):
    roots = [qint(-1 - k, q) for k in range(1, n)] + [qint(-1, q)]
    coeffs = [F(1)]
    for rt in roots:
        new = [F(0)] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i + 1] += c
            new[i] -= c * rt
        coeffs = new
    alpha = qint(n, q) / 2
    px = [F(0)] * len(coeffs)
    for m, cm in enumerate(coeffs):
        if cm == 0:
            continue
        am = cm * alpha ** m
        for j in range(m + 1):
            px[j] += am * comb(m, j) * (-1) ** (m - j)
    pl = leg_coeffs(l)
    b = F(0)
    for i, ci in enumerate(pl):
        for k2, ck in enumerate(px):
            if ci and ck:
                b += ci * ck * mono_int(i + k2)
    return b


def first_negative_q(q, nmax):
    for n in range(1, nmax + 1):
        for l in range(0, n + 1):
            if a_q(n, l, q) < 0:
                return [n, l]
    return None


def qclock():
    table = []
    for q in (F(1001, 1000), F(1005, 1000), F(101, 100), F(102, 100),
              F(105, 100), F(11, 10), F(6, 5), F(3, 2), F(2)):
        table.append({"q": str(q), "q_minus_1": float(q) - 1,
                      "first_negative": first_negative_q(q, 60)})
        print(f"q={q}: {table[-1]['first_negative']}", flush=True)
    ctrl = first_negative_q(F(1), 25)
    # derivative g(n) = -dlog a_{n,0}/dq at q=1, finite difference h=1e-6
    h = F(1, 10 ** 6)
    gs = []
    for n in (5, 10, 15, 20, 25, 30):
        a1, a2 = a_q(n, 0, F(1)), a_q(n, 0, 1 + h)
        g = float((a1 - a2) / (h * a1))
        gs.append({"n": n, "g": g, "g_over_n2": g / n ** 2})
    OUT["q_clock"] = {"table": table, "q1_control_clean_to": 25 if ctrl is None else ctrl,
                      "log_derivative_finite_diff_h": "1e-6", "g_values": gs}
    print("q-clock table + derivative recorded", flush=True)


# ---------- 5. D-universality + D-curves spot checks ----------
def d_checks():
    import sympy as sp
    r_, w_, x, tp = sp.symbols("r w x tp")

    def a_gegen(n, l, r, w, mu0, D):
        al = sp.Rational(D - 3, 2)
        p = sp.prod([tp + 2 + r + k for k in range(n - 1)]) * (tp + 1 + r + w)
        sub = -(sp.Rational(n) - 3 * mu0) * (1 - x) / 2 - mu0
        px = sp.expand(p.subs(tp, sub))
        C = sp.gegenbauer(l, al, x)
        return sp.nsimplify(sp.integrate(
            C * px * (1 - x ** 2) ** (al - sp.Rational(1, 2)), (x, -1, 1)))

    checks = []
    for D in (6, 10):
        v0 = a_gegen(10, 9, sp.Rational(-3, 5), 1, 0, D)
        v1 = a_gegen(11, 10, sp.Rational(-3, 5), 1, 0, D)
        checks.append({"D": D, "a_10_9_is_zero": bool(v0 == 0),
                       "a_11_10_negative": bool(v1 < 0)})
        print(f"D={D}: zero {v0 == 0}, neg {v1 < 0}", flush=True)
    OUT["D_universality"] = checks


# ---------- 6. fixed-spin tails to n=200 ----------
def fixed_spin_200():
    pts = [("veneziano", F(0), F(0)), ("interior", F(1, 4), F(1, 4)),
           ("w-neg", F(1), F(-6, 5)), ("near-edge", F(-12, 25), F(1, 2))]
    rows = []
    for name, r, w in pts:
        for l in (0, 2):
            signs = {}
            for n in (50, 100, 200):
                a = a_route1(n, l, r, w, F(0))
                signs[str(n)] = 1 if a > 0 else (0 if a == 0 else -1)
            rows.append({"point": name, "r": str(r), "w": str(w), "l": l,
                         "signs_n50_100_200": signs})
        print(f"fixed-spin {name}: done", flush=True)
    OUT["fixed_spin_to_200"] = rows


def main() -> int:
    census()
    stack()
    dichotomy()
    qclock()
    d_checks()
    fixed_spin_200()
    (RES / "paper_artifacts.json").write_text(json.dumps(OUT, indent=1),
                                              encoding="utf-8")
    print("written results/paper_artifacts.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
