"""Environment diagnosis. Reports facts; never invents them."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass, field


@dataclass
class DoctorCheck:
    name: str
    ok: bool
    detail: str
    required: bool = True


@dataclass
class DoctorReport:
    checks: list[DoctorCheck] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks if c.required)

    @property
    def blockers(self) -> list[str]:
        return [f"{c.name}: {c.detail}" for c in self.checks if c.required and not c.ok]


def _cmd_version(cmd: list[str]) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        out = (r.stdout or r.stderr).strip().splitlines()
        return out[0] if out else "present"
    except Exception:
        return "present (version query failed)"


def run_doctor() -> DoctorReport:
    rep = DoctorReport()
    py = sys.version.split()[0]
    rep.checks.append(DoctorCheck("python", sys.version_info >= (3, 12), f"{py} (need >=3.12)"))
    rep.checks.append(
        DoctorCheck("platform", True, f"{platform.system()} {platform.release()}", required=False)
    )

    for name, cmd, required in [
        ("git", ["git", "--version"], True),
        ("uv", ["uv", "--version"], True),
        ("docker", ["docker", "--version"], False),
        ("node", ["node", "--version"], False),
    ]:
        v = _cmd_version(cmd)
        rep.checks.append(DoctorCheck(name, v is not None, v or "not found", required=required))

    gpu = _cmd_version(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
    rep.checks.append(
        DoctorCheck("gpu", gpu is not None, gpu or "no NVIDIA GPU detected", required=False)
    )

    for mod in ["pydantic", "typer", "rich", "streamlit", "plotly", "pandas", "numpy"]:
        try:
            __import__(mod)
            rep.checks.append(DoctorCheck(f"pkg:{mod}", True, "importable"))
        except ImportError as e:
            rep.checks.append(DoctorCheck(f"pkg:{mod}", False, f"import failed: {e}"))

    return rep
