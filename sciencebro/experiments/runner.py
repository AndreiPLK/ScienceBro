"""Run context capture (roadmap §6 rule 11): commit, environment, hardware, runtime."""

from __future__ import annotations

import hashlib
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field


class RunRecord(BaseModel):
    experiment_id: str
    started_at: str
    finished_at: str | None = None
    git_commit: str | None = None
    git_dirty: bool | None = None
    uv_lock_sha256: str | None = None
    command: str
    seeds: list[int] = Field(default_factory=list)
    precision: str = "float64"
    hardware: str = ""
    exit_code: int | None = None
    raw_output_paths: list[str] = Field(default_factory=list)
    notes: str = ""


def _git(root: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def capture_run_context(root: Path, experiment_id: str, command: str) -> RunRecord:
    commit = _git(root, "rev-parse", "HEAD")
    dirty_out = _git(root, "status", "--porcelain")
    lock = root / "uv.lock"
    lock_hash = hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None
    return RunRecord(
        experiment_id=experiment_id,
        started_at=datetime.now(UTC).isoformat(),
        git_commit=commit,
        git_dirty=bool(dirty_out) if dirty_out is not None else None,
        uv_lock_sha256=lock_hash,
        command=command,
        hardware=f"{platform.system()} {platform.machine()}",
    )
