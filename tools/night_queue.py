"""Очередь ночного батча (15->16.08): каждая задача — функция, возвращающая
однострочную сводку. Наука статьи №2: добить гипотезу полноты со всех сторон.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "projects" / "qg-bootstrap" / "lab"
RES = ROOT / "projects" / "qg-bootstrap" / "results"
sys.path.insert(0, str(LAB))


def _minT(lamf: float) -> float:
    return min((3 * (2 * n - 3) / (n * (n - 2))) * (lamf * lamf + (2 * n - 2) * lamf + 1) + 2 * n
               for n in range(3, 400))


def task_2n8_hunt():
    """2n-8 траектория у границы модели: режет ли глубже."""
    from grav_full_body import gegen_coeffs, mono_int  # reuse exact helpers
    def a_l(n, l, lam, D):
        mu = (n + lam - 1) / lam
        A = lam * mu / 2
        poly = [F(1)]
        for k in range(1, n):
            b = (1 + lam) / 2 + (k - 1) - A
            new = [F(0)] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c * b
                new[i + 1] += c * A
            poly = new
        P = [F(0)] * (2 * len(poly) - 1)
        for i, a_ in enumerate(poly):
            for j, b_ in enumerate(poly):
                P[i + j] += a_ * b_
        mW = (D - 4) // 2
        w = [F(0)] * (2 * mW + 1)
        for j in range(mW + 1):
            w[2 * j] = F((-1) ** j * comb(mW, j))
        Pw = [F(0)] * (len(P) + len(w) - 1)
        for i, c in enumerate(P):
            if c == 0:
                continue
            for jw, cw in enumerate(w):
                if cw:
                    Pw[i + jw] += c * cw
        cl = gegen_coeffs(l, D - 3)
        b = F(0)
        for i, ci in enumerate(cl):
            if ci == 0:
                continue
            for k2, ck in enumerate(Pw):
                if ck:
                    b += ci * ck * mono_int(i + k2)
        return b
    alarms = []
    lams = [F(i, 10) for i in range(1, 31)] + [F(4), F(5), F(7), F(10)]
    for lam in lams:
        Dtop = int(_minT(float(lam)))
        for D in range(max(4, Dtop - 3), Dtop + 1):
            if D % 2:
                continue
            for n in range(5, 15):
                if a_l(n, 2 * n - 8, lam, D) < 0:
                    alarms.append({"lam": str(lam), "D": D, "n": n})
                    break
    json.dump(alarms, open(RES / "hunt_2n8.json", "w"))
    return f"2n-8 hunt: {len(alarms)} alarms over {len(lams)} lambdas"


def task_lowspin_stress():
    """Низкие спины l=0..6 при больших D у границы: не режут ли глубже модели."""
    from grav_full_body import first_negative
    alarms = []
    checks = 0
    for lam in (F(1), F(3, 2), F(2), F(3), F(5), F(8)):
        Dtop = int(_minT(float(lam)))
        for D in range(max(4, Dtop - 2), Dtop + 1):
            if D % 2:
                continue
            checks += 1
            fn = first_negative(lam, D, 20)
            if fn is not None:
                alarms.append({"lam": str(lam), "D": D, "first_neg": fn})
    json.dump(alarms, open(RES / "lowspin_stress.json", "w"))
    return f"low-spin stress: {len(alarms)} alarms in {checks} checks (depth 20, all even l)"


def task_deep_d4():
    """Наш мир D=4: сверхглубокий скан до n=120 на 8 лямбдах (вечная жизнь?)."""
    from grav_full_body import first_negative
    rows = []
    for lam in (F(1, 100), F(1, 10), F(1, 2), F(1), F(3, 2), F(3), F(10), F(100)):
        fn = first_negative(lam, 4, 120)
        rows.append({"lam": str(lam), "first_neg": fn})
    json.dump(rows, open(RES / "d4_deep120.json", "w"))
    alive = sum(1 for r in rows if r["first_neg"] is None)
    return f"D=4 deep-120: {alive}/8 alive"


TASKS = [
    ("2n8-hunt", task_2n8_hunt),
    ("lowspin-stress", task_lowspin_stress),
    ("d4-deep120", task_deep_d4),
]
