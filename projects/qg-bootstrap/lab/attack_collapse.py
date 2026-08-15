"""Adversarial attack battery for the binomial collapse lemma (paper 5).

Role: domain-critic. Independent reimplementation -- nothing imported from
lab/collapse_zones.py. E_{2t} is cross-checked against a brute-force subset
sum over the doubled signed multiset {n-2k} x2 (the definition in the claim),
so the two implementations only meet at the definition, not at code.

ALL FALSIFICATION GATES ARE FROZEN IN THIS FILE BEFORE FIRST EXECUTION
(experiment contract). Companion analysis: research/collapse-lemma-review.md.

Frozen gates (falsify -> exit 1):
  F1  independent E disagrees with brute-force definition (bridge check)
  F2  Sigma identity e_1 != n(n-1)(n-2)/3
  F3  log-concavity of E-sequence violated at any tested (n,t)
  F3b Newton lower bound violated: E-ratio * Sigma/t - 1 < 0 anywhere
  F4  estimate (i) not O(1/m): m*R grows between m=320 and m=640 (ratio>1.3)
  F5  convergence rate slower than O(1/m) for |1-X|>=0.1 (measured p < 0.7)
  F6  B_j/term_0 does not approach (1-X)^{j-1} (|dev| not decreasing m=160->320)
  F7  zone battery: band count != floor(j/2) for j<=8 at low-rho configs,
      or lab's n=100 row not reproduced exactly
  F8  lab Dmax truncation missed an odd-j negativity zone at n=100
  F9  far-field sign anomaly (odd j killing at huge D, or even j not)
  F10 T_8 != 94 exact hand-check fails
  F11 rho* != 1+1/sqrt3 or envelope != (12+4sqrt3)lam (numerical minimize)

Frozen warnings (recorded, exit stays 0 -- these test MY sharper predictions,
not the paper's claims):
  W1  at X=1 exactly, measured order != ceil((j-1)/2) = j//2
  W2  band count deviation at j=9,10 (beyond lab battery; asymptotic claim)
  W3  splitting exponent outside [0.35, 0.65] (sqrt-m predicts ~0.5)
  W4  m*R constant differs from predicted 1.8*(t-1) by >30% at m=640
  W5  band count deviation at the high-rho probe (regime lab never tested)

Usage:   python lab/attack_collapse.py     (run from projects/qg-bootstrap)
Exit 0 iff no falsification. Artifact: results/attack_collapse.json
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from itertools import combinations
from math import factorial, log, log2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"

FALS: list[str] = []
WARN: list[str] = []

SQRT3 = 3 ** 0.5
TMAX = 10  # highest E index needed: t = j-1 <= 9


def sgn(x) -> int:
    return (x > 0) - (x < 0)


# ---------------- independent E implementation ----------------

def squares(n: int) -> list[int]:
    """Multiset {(n-2k)^2 : k=1..n-1}. E_{2t}(n) = e_t(this multiset)."""
    return [(n - 2 * k) ** 2 for k in range(1, n)]


def elem_sym(vals: list[int], tmax: int | None = None) -> list[int]:
    tmax = len(vals) if tmax is None else min(tmax, len(vals))
    e = [0] * (tmax + 1)
    e[0] = 1
    for cnt, a in enumerate(vals, 1):
        for t in range(min(cnt, tmax), 0, -1):
            e[t] += a * e[t - 1]
    return e


_ECACHE: dict[int, list[int]] = {}


def E2(n: int) -> list[int]:
    if n not in _ECACHE:
        _ECACHE[n] = elem_sym(squares(n), TMAX)
    return _ECACHE[n]


def brute_E2t(n: int, t: int) -> int:
    """|e_{2t}| of the doubled signed multiset -- the claim's definition,
    computed by raw subset sums (independent of the recursion above)."""
    ms: list[int] = []
    for k in range(1, n):
        ms += [n - 2 * k, n - 2 * k]
    tot = 0
    for c in combinations(range(len(ms)), 2 * t):
        p = 1
        for i in c:
            p *= ms[i]
        tot += p
    return abs(tot)


# ---------------- the bracket, from the claim statement ----------------

def bracket_terms(n: int, j: int, s, D) -> list:
    """B_j terms: (-1)^i E_{2(j-1-i)} (2n-2j+2i)!/(i! 2^i) s^{2i}
    prod_{r=i}^{j-2} (D + 4n-4j-1 + 2r)."""
    e = E2(n)
    c = 4 * n - 4 * j - 1
    terms = []
    for i in range(j):
        w = F(factorial(2 * n - 2 * j + 2 * i), factorial(i) * 2 ** i)
        tail = F(1)
        for r in range(i, j - 1):
            tail *= D + c + 2 * r
        terms.append((-1) ** i * e[j - 1 - i] * w * s ** (2 * i) * tail)
    return terms


# ---------------- part 1: the ratio estimate (i) ----------------

def part1() -> dict:
    out: dict = {"brute_check_ok": True, "sigma_identity_ok": True,
                 "logconcave_violations": [], "mR": {}, "mR_growth": {},
                 "corr_over_n2": {}}
    # definition bridge
    for n in (6, 7, 8, 9):
        e = elem_sym(squares(n))
        for t in range(0, 5):
            if e[t] != brute_E2t(n, t):
                out["brute_check_ok"] = False
                FALS.append(f"F1 E definition mismatch n={n} t={t}")
    # Sigma identity + full-sequence log-concavity
    for n in list(range(5, 61)) + [100, 140]:
        e = elem_sym(squares(n))
        if e[1] != n * (n - 1) * (n - 2) // 3:
            out["sigma_identity_ok"] = False
            FALS.append(f"F2 Sigma identity fails n={n}")
        for t in range(1, len(e) - 1):
            if e[t] ** 2 < e[t - 1] * e[t + 1]:
                out["logconcave_violations"].append([n, t])
    if out["logconcave_violations"]:
        FALS.append("F3 log-concavity violated: "
                    + str(out["logconcave_violations"][:5]))
    # ratio deviation R(t,m) = E_{2(t-1)}/E_{2t} * Sigma/t - 1; table of m*R
    ms = [20, 40, 80, 160, 320, 640]
    for t in range(2, 10):
        row = []
        for m in ms:
            e = E2(m + 3)
            r_exact = F(e[t - 1] * e[1], t * e[t]) - 1
            if r_exact < 0:
                FALS.append(f"F3b Newton lower bound violated t={t} m={m}")
            row.append(float(m * r_exact))
        out["mR"][t] = row
        growth = row[-1] / row[-2] if row[-2] else float("inf")
        out["mR_growth"][t] = round(growth, 4)
        if growth > 1.3:
            FALS.append(f"F4 (i) not O(1/m): m*R grows, t={t} "
                        f"ratio={growth:.3f}")
        pred = 1.8 * (t - 1)
        if abs(row[-1] / pred - 1) > 0.3:
            WARN.append(f"W4 m*R vs 1.8(t-1): t={t} m*R={row[-1]:.3f} "
                        f"pred={pred:.1f}")
    # additive correction: (Sigma - S_t)/n^2 with S_t = t E_{2t}/E_{2(t-1)}.
    # md claims correction O(m); my expansion predicts Theta(m^2), const 0.6(t-1)
    for t in range(2, 7):
        row = []
        for m in (160, 320, 640):
            n = m + 3
            e = E2(n)
            s_t = F(t * e[t], e[t - 1])
            row.append(float((e[1] - s_t) / n ** 2))
        out["corr_over_n2"][t] = row
    c320, c640 = out["corr_over_n2"][4][1], out["corr_over_n2"][4][2]
    out["md_correction_is_Theta_m2"] = abs(c640 / c320 - 1) < 0.15
    return out


# ---------------- part 2: convergence to (1-X)^{j-1} ----------------

CASES = [
    ("X=1.1025 rho=21/20 d=2", F(21, 20), F(2)),
    ("X=1 rho=21/20", F(21, 20), 6 * F(21, 20) ** 2 - 4),
    ("X=1/2 rho=13/10", F(13, 10), 12 * F(13, 10) ** 2 - 4),
    ("generic rho~rho* d=5", F(1577, 1000), F(5)),
    ("X=1-eps rho~sqrt(5/3)", F(1291, 1000),
     6 * F(1291, 1000) ** 2 - 4 + F(1, 10)),
    ("X=1 rho~rho*", F(1577, 1000), 6 * F(1577, 1000) ** 2 - 4),
]
MS2 = [10, 20, 40, 80, 160, 320]


def part2() -> dict:
    out: dict = {"m_grid": MS2, "cases": []}
    for name, rho, delta in CASES:
        x = 6 * rho ** 2 / (delta + 4)
        generic = abs(1 - x) >= F(1, 10)
        case: dict = {"name": name, "rho": str(rho), "delta": str(delta),
                      "X": float(x), "generic": generic, "j": {}}
        for j in range(2, 9):
            devs = []
            for m in MS2:
                n = m + 3
                terms = bracket_terms(n, j, rho * m, delta * m)
                devs.append(sum(terms) / terms[0] - (1 - x) ** (j - 1))
            fdevs = [float(d) for d in devs]
            orders = []
            for k in range(len(devs) - 1):
                if devs[k] == 0 or devs[k + 1] == 0:
                    orders.append(None)
                else:
                    orders.append(
                        round(log2(abs(float(devs[k] / devs[k + 1]))), 3))
            rec: dict = {"dev": fdevs, "orders": orders}
            if abs(devs[-1]) >= abs(devs[-2]):
                FALS.append(f"F6 no convergence: '{name}' j={j}")
            p = orders[-1]
            if generic and (p is None or p < 0.7):
                FALS.append(f"F5 rate slower than O(1/m): '{name}' j={j} p={p}")
            if x == 1:
                rec["order_pred_X1"] = j // 2
                if p is None or abs(p - j // 2) > 0.35:
                    WARN.append(f"W1 X=1 order: '{name}' j={j} p={p} "
                                f"pred={j // 2}")
            if not generic and x != 1:
                lim = float((1 - x) ** (j - 1))
                rec["dev_over_limit_m320"] = abs(fdevs[-1] / lim)
            case["j"][j] = rec
        out["cases"].append(case)
    return out


# ---------------- part 3: independent zone battery ----------------

def zone_scan(n: int, lam: int, jmax: int, dmax: int):
    m = n - 3
    s = lam + n - 1
    e = E2(n)
    zones: dict[int, list[list[int]]] = {}
    schanges: dict[int, int] = {}
    signs_all: dict[int, list[int]] = {}
    for j in range(2, jmax + 1):
        c = 4 * n - 4 * j - 1
        pre = []
        for i in range(j):
            q, rem = divmod(factorial(2 * n - 2 * j + 2 * i),
                            factorial(i) * 2 ** i)
            assert rem == 0
            pre.append((-1) ** i * e[j - 1 - i] * q * s ** (2 * i))
        signs = []
        for dv in range(4, dmax):
            lin = [dv + c + 2 * r for r in range(j - 1)]
            suf = [1] * j
            for r in range(j - 2, -1, -1):
                suf[r] = suf[r + 1] * lin[r]
            b = sum(pre[i] * suf[i] for i in range(j))
            a = b if j % 2 else -b
            signs.append(sgn(a))
        signs_all[j] = signs
        runs: list[list[int]] = []
        start = None
        for idx, sg in enumerate(signs):
            dv = 4 + idx
            if sg < 0 and start is None:
                start = dv
            if sg >= 0 and start is not None:
                runs.append([start, dv - 1])
                start = None
        if start is not None:
            runs.append([start, dmax - 1])
        zones[j] = runs
        nz = [x for x in signs if x != 0]
        schanges[j] = sum(1 for a_, b_ in zip(nz, nz[1:]) if a_ != b_)
    return zones, schanges, signs_all


def far_sign(n: int, j: int, s: int, dv: int) -> int:
    b = sum(bracket_terms(n, j, F(s), F(dv)))
    return sgn(b if j % 2 else -b)


def compare_lab(zones, dcrit: float, lab_row) -> tuple[bool, dict]:
    """Exact reproduction test of the lab's n=100 row, including their
    Dmax = int(2*Dcrit)+60 truncation and their rounding convention."""
    hi = int(dcrit * 2) + 60  # lab scanned D in [4, hi-1]
    ok = True
    detail: dict = {}
    for j in range(2, 9):
        theirs = lab_row["zones"][str(j)]["offsets_from_Dcrit"]
        clipped = []
        for a, b in zones[j]:
            a2, b2 = max(a, 4), min(b, hi - 1)
            if a2 <= b2:
                clipped.append([round(a2 - dcrit), round(b2 - dcrit)])
        if clipped != theirs:
            ok = False
            detail[j] = {"mine": clipped, "lab": theirs}
    return ok, detail


def part3() -> dict:
    out: dict = {"configs": []}
    spans: dict[int, list[tuple[int, int]]] = {5: [], 7: []}
    lab_rows = None
    labf = RES / "collapse_zones.json"
    if labf.exists():
        lab_rows = json.loads(labf.read_text(encoding="utf-8"))["rows"]
    else:
        WARN.append("collapse_zones.json missing; lab reproduction skipped")
    for n, lam, tag in [(100, 12, "lab-repro"), (120, 15, "extend"),
                        (150, 20, "extend"), (120, 60, "high-rho-probe")]:
        m = n - 3
        s = lam + n - 1
        dcrit = 6 * s * s / m - 4 * m
        dmax = int(3 * dcrit) + 80
        jmax = 10
        zones, schg, signs_all = zone_scan(n, lam, jmax, dmax)
        cfg = {"n": n, "lam": lam, "tag": tag, "rho": round(s / m, 4),
               "D_crit": round(dcrit, 2), "D_max": dmax,
               "sign_changes": schg,
               "zones": {j: {"bands": len(zones[j]), "expected": j // 2,
                             "offsets": [[round(a - dcrit), round(b - dcrit)]
                                         for a, b in zones[j]]}
                         for j in zones}}
        for j in range(2, jmax + 1):
            nb = len(zones[j])
            if nb != j // 2:
                msg = f"bands {nb} != {j // 2} at n={n} lam={lam} j={j}"
                if tag == "high-rho-probe":
                    WARN.append("W5 probe: " + msg)
                elif j >= 9:
                    WARN.append("W2 j>=9: " + msg)
                else:
                    FALS.append("F7 " + msg)
        dfar = 10 * int(dcrit) + 1000
        for j in (3, 4, 7, 8):
            a = far_sign(n, j, s, dfar)
            if (j % 2 == 1 and a <= 0) or (j % 2 == 0 and a >= 0):
                FALS.append(f"F9 far-field sign anomaly n={n} j={j}")
        if tag == "lab-repro" and lab_rows is not None:
            row = next(r for r in lab_rows if r["n"] == n)
            ok, detail = compare_lab(zones, dcrit, row)
            cfg["lab_reproduction_ok"] = ok
            if not ok:
                cfg["lab_mismatch"] = detail
                FALS.append("F7 lab zone battery NOT reproduced at n=100")
            hi = int(dcrit * 2) + 60
            missed = [j for j in (3, 5, 7)
                      if any(x < 0 for x in signs_all[j][hi - 4:])]
            cfg["lab_truncation_missed_odd_j"] = missed
            if missed:
                FALS.append(f"F8 lab truncation missed odd-j bands: {missed}")
        if tag in ("lab-repro", "extend"):
            for j in (5, 7):
                if zones[j] and zones[j][-1][1] < dmax - 1:
                    spans[j].append((m, zones[j][-1][1] - zones[j][0][0]))
                else:
                    WARN.append(f"span truncated n={n} j={j}; exponent fit "
                                f"skips this point")
        out["configs"].append(cfg)
    expo = {}
    for j in (5, 7):
        pts = spans[j]
        if len(pts) >= 2:
            xs = [log(p[0]) for p in pts]
            ys = [log(p[1]) for p in pts]
            xb, yb = sum(xs) / len(xs), sum(ys) / len(ys)
            num = sum((x - xb) * (y - yb) for x, y in zip(xs, ys))
            den = sum((x - xb) ** 2 for x in xs)
            expo[j] = round(num / den, 3)
            if not 0.35 <= expo[j] <= 0.65:
                WARN.append(f"W3 splitting exponent j={j}: {expo[j]} "
                            f"(sqrt-m predicts ~0.5)")
    out["splitting_exponent"] = expo
    return out


# ---------------- extras: T_8 and the tangency numbers ----------------

def extras() -> dict:
    out: dict = {}
    out["T8_root_at_94"] = (sum(bracket_terms(8, 2, F(12), F(94))) == 0)
    if not out["T8_root_at_94"]:
        FALS.append("F10 T_8 != 94 (hand-check in collapse-lemma.md fails)")
    lam = 10 ** 6
    m0 = round(SQRT3 * (lam + 2))
    best = min(range(m0 - 8, m0 + 9),
               key=lambda mm: F(6 * (lam + mm + 2) ** 2, mm) - 4 * mm)
    ratio = (lam + best + 2) / best
    dmin = float(F(6 * (lam + best + 2) ** 2, best) - 4 * best)
    out["rho_star_measured"] = round(ratio, 7)
    out["envelope_over_lam"] = round(dmin / lam, 5)
    if abs(ratio - (1 + 1 / SQRT3)) > 1e-3:
        FALS.append("F11 rho* != 1+1/sqrt3")
    if abs(dmin / lam - (12 + 4 * SQRT3)) > 0.01:
        FALS.append("F11 envelope asymptote != 12+4sqrt3")
    return out


def main() -> int:
    t0 = time.time()
    print("part1: ratio estimate (i) ...", flush=True)
    p1 = part1()
    print(f"part2: convergence to (1-X)^(j-1) ... ({time.time()-t0:.0f}s)",
          flush=True)
    p2 = part2()
    print(f"part3: zone battery j<=10 ... ({time.time()-t0:.0f}s)", flush=True)
    p3 = part3()
    ex = extras()
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True,
                         cwd=ROOT).stdout.strip()
    art = {"date": time.strftime("%Y-%m-%d"), "git": git,
           "command": "python lab/attack_collapse.py",
           "gates": "frozen in source docstring before first execution",
           "part1_ratio_estimate": p1, "part2_convergence": p2,
           "part3_zones": p3, "extras": ex,
           "warnings": WARN, "falsifications": FALS,
           "runtime_s": round(time.time() - t0, 1)}
    RES.mkdir(exist_ok=True)
    (RES / "attack_collapse.json").write_text(json.dumps(art, indent=1),
                                              encoding="utf-8")
    print(f"warnings ({len(WARN)}):")
    for w in WARN:
        print("  W:", w)
    print(f"falsifications ({len(FALS)}):")
    for f_ in FALS:
        print("  F:", f_)
    print(f"done {art['runtime_s']}s -> results/attack_collapse.json")
    return 1 if FALS else 0


if __name__ == "__main__":
    sys.exit(main())
