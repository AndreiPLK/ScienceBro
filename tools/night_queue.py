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


SCRATCH = Path(
    "C:/Users/user/AppData/Local/Temp/claude"
    "/C--Users-user-ScienceBro"
    "/93847525-923a-41ca-a919-bf7a73c639c3/scratchpad"
)


def _run(script, env_extra=None, timeout=9000, logname=None):
    """Поток задачи пишется в видимый лог (live-страница его показывает)."""
    env = dict(os.environ, **(env_extra or {}))
    logf = SCRATCH / f"{logname or script}.log"
    with open(logf, "a", encoding="utf-8") as fh:
        r = subprocess.run(
            [PY, "-u", str(LAB / script)],
            stdout=fh,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            env=env,
        )
    tail = logf.read_text(encoding="utf-8", errors="replace")[-200:]
    return r.returncode, tail


def _tail(j):
    def run():
        code, tail = _run("knife_tail_deep.py", {"KNIFE_J": str(j)}, logname=f"tail_rerun_j{j}")
        return f"tails j={j}: exit {code}: {tail}"

    return run


def _belowdiag(j):
    def run():
        code, tail = _run(
            "knife_belowdiag_shift.py",
            {"KNIFE_J": str(j), "PIECES": "band,k0"},
            logname=f"belowdiag_j{j}",
        )
        return f"belowdiag j={j}: exit {code}: {tail}"

    return run


def _farbelow(j):
    def run():
        code, tail = _run(
            "knife_farbelow_factored.py", {"KNIFE_J": str(j)}, logname=f"farbelow_j{j}"
        )
        return f"farbelow j={j}: exit {code}: {tail}"

    return run


TASKS = [  # быстрые победы вперёд (видимый прогресс), длинные хвосты после
    ("farbelow-j6", _farbelow(6)),
    ("farbelow-j7", _farbelow(7)),
    ("belowdiag-j6", _belowdiag(6)),
    ("belowdiag-j7", _belowdiag(7)),
    ("tails-j4", _tail(4)),
    ("tails-j5", _tail(5)),
    ("tails-j6", _tail(6)),
    ("tails-j7", _tail(7)),
]
