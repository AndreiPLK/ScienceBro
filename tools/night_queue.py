"""Ночная очередь 17->18.08: добить конвейер теорем. Задачи НАРЕЗАНЫ
(правило непрерывности): каждая пишет прогресс и артефакт.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "projects" / "qg-bootstrap" / "lab"
RES = ROOT / "projects" / "qg-bootstrap" / "results"
sys.path.insert(0, str(LAB))
PY = sys.executable


def _run(script, env_extra=None, timeout=5400):
    env = dict(os.environ, **(env_extra or {}))
    r = subprocess.run([PY, "-u", str(LAB / script)], capture_output=True,
                       text=True, timeout=timeout, env=env)
    return r.returncode, (r.stdout or "")[-200:]


def task_knife5_belowdiag_factored():
    """Нож 5, far-below тем же приёмом: факторизуй-потом-сертифицируй."""
    code, tail = _run("knife5_farbelow_factored.py")
    return f"knife5 far-below factored: exit {code}: {tail}"


def task_knife6_shallow():
    code, tail = _run("knife_proof.py", {"KNIFE_J": "6"}, timeout=7200)
    return f"knife6 shallow: exit {code}: {tail}"


def task_knife6_tails():
    code, tail = _run("knife_tail_deep.py", {"KNIFE_J": "6"}, timeout=7200)
    return f"knife6 tails: exit {code}: {tail}"


TASKS = [
    ("knife5-belowdiag-factored", task_knife5_belowdiag_factored),
    ("knife6-shallow", task_knife6_shallow),
    ("knife6-tails", task_knife6_tails),
]
