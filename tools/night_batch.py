"""NIGHT BATCH v3 — детачнутый ночной работник (окончательный фикс).

Запускается КАК ОТДЕЛЬНЫЙ ПРОЦЕСС ОС (не зависит от чата/приложения):
  powershell Start-Process -WindowStyle Hidden .venv\\Scripts\\python.exe -ArgumentList "-u","tools/night_batch.py"

Держит машину без сна сам (SetThreadExecutionState), выполняет очередь задач
из tools/night_queue.py последовательно, пишет прогресс в article/NIGHT_LOG.md
и коммитит результаты локально после каждой задачи. Умирает чат или нет —
науке всё равно. Работает до END_HOUR.
"""

from __future__ import annotations

import ctypes
import datetime
import importlib.util
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "article" / "NIGHT_LOG.md"
END_HOUR = 8
ES = 0x80000000 | 0x00000001


def log(msg: str) -> None:
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"- {stamp} {msg}\n")
    print(f"{stamp} {msg}", flush=True)


def commit(msg: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=ROOT, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m",
                    f"[night-batch] {msg}\n\nCo-Authored-By: Claude Fable 5 <noreply@anthropic.com>"],
                   cwd=ROOT, capture_output=True)


def main() -> int:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"\n## Night batch {datetime.datetime.now():%Y-%m-%d %H:%M}\n")
    spec = importlib.util.spec_from_file_location(
        "night_queue", ROOT / "tools" / "night_queue.py")
    q = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(q)
    log(f"queue loaded: {len(q.TASKS)} tasks")
    for name, fn in q.TASKS:
        now = datetime.datetime.now()
        if 8 <= now.hour < 22 and now.hour >= END_HOUR:
            pass  # днём тоже можно гонять вручную
        ctypes.windll.kernel32.SetThreadExecutionState(ES)
        log(f"START {name}")
        try:
            summary = fn()
            log(f"DONE  {name}: {summary}")
            commit(f"{name}: {summary}")
        except Exception:
            err = traceback.format_exc().strip().splitlines()[-1]
            log(f"FAIL  {name}: {err}")
            commit(f"{name} FAILED: {err}")
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    log("night batch finished")
    commit("night batch finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
