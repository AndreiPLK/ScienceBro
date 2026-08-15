"""Очередь ночного батча (15->16.08, вечерняя): дожать проект 4.
d4-deep120 из утреннего батча продолжает считать отдельным процессом.
"""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "projects" / "qg-bootstrap" / "lab"
RES = ROOT / "projects" / "qg-bootstrap" / "results"
sys.path.insert(0, str(LAB))


def task_completeness_deep():
    """Скан полноты глубже: n<=80, lam до 200, все целые D под берегом."""
    from master_completeness_scan import master_sign, min_T_exact, ensure_E
    ensure_E(80)
    lams = ([F(i, 10) for i in range(1, 31)] +
            [F(4), F(5), F(7), F(10), F(20), F(50), F(100), F(200)])
    alarms = []
    checks = 0
    for lam in lams:
        mt = min_T_exact(lam)
        Dtop = mt.numerator // mt.denominator
        for Dv in range(4, Dtop + 1):
            for n in range(4, 81):
                for j in range(3, n):
                    checks += 1
                    if master_sign(n, j, lam, Dv) < 0:
                        alarms.append({"lam": str(lam), "D": Dv, "n": n, "j": j})
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    json.dump({"checks": checks, "alarms": alarms, "nmax": 80,
               "lam_max": "200", "git": git},
              open(RES / "completeness_deep_n80.json", "w"))
    return f"deep completeness n<=80: {checks} checks, {len(alarms)} alarms"


def task_closest_approach_exact():
    """Ближайший подход окна к берегу (lam~0.05, n=6): точная арифметика."""
    from master_checks import master_sign
    alarms = []
    checks = 0
    for num in range(1, 41):        # lam = num/100: 0.01..0.40
        lam = F(num, 100)
        for Dv in range(4, 40):
            for n in range(4, 30):
                for j in (3, 4, 5):
                    if j >= n:
                        continue
                    # только точки ПОД берегом (точная проверка)
                    from master_completeness_scan import min_T_exact
                    if Dv > min_T_exact(lam):
                        continue
                    checks += 1
                    if master_sign(n, j, lam, Dv) < 0:
                        alarms.append({"lam": str(lam), "D": Dv, "n": n, "j": j})
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    json.dump({"checks": checks, "alarms": alarms, "git": git},
              open(RES / "closest_approach_exact.json", "w"))
    return f"closest-approach exact: {checks} checks, {len(alarms)} alarms"


def task_j6_brackets():
    """Символьные скобки пятого ножа (j=6) для архива: n=7..9."""
    import os
    os.environ["TJ_J"] = "6"
    import importlib
    import tj_bracket
    importlib.reload(tj_bracket)
    out = {}
    for n in (7, 8, 9):
        fac, den = tj_bracket.bracket_for(n)
        out[str(n)] = {"numerator_factored": str(fac),
                       "denominator_factored": str(den)}
    json.dump(out, open(RES / "T2n12_brackets.json", "w"), indent=1)
    return f"j=6 brackets extracted for n=7..9"


def task_knife4_open_region():
    """Точная батарея открытого региона ножа 4: глубоководье ниже оптимали."""
    from master_completeness_scan import master_sign, min_T_exact, ensure_E
    ensure_E(320)
    alarms = []
    checks = 0
    for lam_i in list(range(26, 101, 2)) + [120, 150, 200, 250, 300]:
        lam = F(lam_i)
        mt = min_T_exact(lam)
        Dtop = mt.numerator // mt.denominator
        m_opt = int(1.733 * lam_i) + 5
        for n in range(44, min(m_opt + 6, 320)):
            for Dv in range(max(4, Dtop - 60), Dtop + 1):
                checks += 1
                if master_sign(n, 4, lam, Dv) < 0:
                    alarms.append({"lam": str(lam), "D": Dv, "n": n})
    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    json.dump({"checks": checks, "alarms": alarms, "git": git},
              open(RES / "knife4_open_region.json", "w"))
    return f"knife4 open region: {checks} checks, {len(alarms)} alarms"


def task_knife4_belowdiag_shift():
    """Диагональ снизу: сдвиг разреза вниз (v >= K-6 интервальным методом,
    который прошёл выше диагонали) + явные K=0..5."""
    import os
    os.environ["KNIFE_J"] = "4"
    os.environ["KNIFE_STAGE"] = "belowdiag_shift"
    os.environ["BERN_ELEV"] = "8"
    r = subprocess.run([sys.executable, "-u",
                        str(LAB / "knife_belowdiag_shift.py")],
                       capture_output=True, text=True, timeout=14400)
    tail = (r.stdout or "")[-300:]
    return f"belowdiag-shift exit {r.returncode}: {tail}"


def task_far_below_variants():
    """Ночной веер по куску (iv): compact4d, затем elevation sweep."""
    import os
    outs = []
    for mode, elev in (("compact4d", "6"), ("compact4d", "12"),
                       ("orthant", "16")):
        env = dict(os.environ, FAR_MODE=mode, BERN_ELEV=elev)
        r = subprocess.run([sys.executable, "-u",
                            str(LAB / "knife_belowdiag_shift.py")],
                           capture_output=True, text=True, timeout=10800,
                           env=env)
        outs.append(f"{mode}/e{elev}: exit {r.returncode}")
        if r.returncode == 0:
            break
    return "far-below variants: " + "; ".join(outs)


TASKS = [
    ("knife4-far-below-variants", task_far_below_variants),
    ("knife4-belowdiag-shift", task_knife4_belowdiag_shift),
    ("knife4-open-region", task_knife4_open_region),
    ("completeness-deep-n80", task_completeness_deep),
    ("closest-approach-exact", task_closest_approach_exact),
    ("j6-brackets", task_j6_brackets),
]
