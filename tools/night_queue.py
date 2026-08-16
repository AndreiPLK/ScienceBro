"""Очередь ремонта 16.08: хвосты j=6,7,4,5 + полосы/дно ножей 6-7.
Задачи НАРЕЗАНЫ (правило непрерывности): каждая пишет прогресс и артефакт.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "projects" / "qg-bootstrap" / "lab"
RES = ROOT / "projects" / "qg-bootstrap" / "results"
sys.path.insert(0, str(LAB))
PY = sys.executable


def _run(script, env_extra=None, timeout=9000):
    env = dict(os.environ, **(env_extra or {}))
    r = subprocess.run([PY, "-u", str(LAB / script)], capture_output=True,
                       text=True, timeout=timeout, env=env)
    return r.returncode, (r.stdout or "")[-200:]


def _tail(j):
    def run():
        code, tail = _run("knife_tail_deep.py", {"KNIFE_J": str(j)})
        return f"tails j={j}: exit {code}: {tail}"
    return run


def _belowdiag(j):
    def run():
        code, tail = _run("knife_belowdiag_shift.py",
                          {"KNIFE_J": str(j), "PIECES": "band,k0"})
        return f"belowdiag j={j}: exit {code}: {tail}"
    return run


def _farbelow(j):
    def run():
        code, tail = _run("knife_farbelow_factored.py", {"KNIFE_J": str(j)})
        return f"farbelow j={j}: exit {code}: {tail}"
    return run


TASKS = [
    ("tails-j6", _tail(6)),
    ("tails-j7", _tail(7)),
    ("tails-j4", _tail(4)),
    ("tails-j5", _tail(5)),
    ("belowdiag-j6", _belowdiag(6)),
    ("belowdiag-j7", _belowdiag(7)),
    ("farbelow-j6", _farbelow(6)),
    ("farbelow-j7", _farbelow(7)),
]
