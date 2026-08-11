"""Clean-clone reproduction check (roadmap §6 rule 36).

Clones the current repo into a temp dir, runs uv sync + pytest + sb doctor there.
Usage: uv run python scripts/verify_clean_clone.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="sb-clean-") as tmp:
        clone = Path(tmp) / "clone"
        steps = [
            (["git", "clone", "--quiet", str(root), str(clone)], tmp),
            (["uv", "sync", "--all-groups"], clone),
            (["uv", "run", "pytest", "-q", "tests/unit"], clone),
            (["uv", "run", "sb", "doctor"], clone),
            (["uv", "run", "sb", "project", "status", "ainstein-audit"], clone),
        ]
        for cmd, cwd in steps:
            print(f"== {' '.join(map(str, cmd))}")
            if subprocess.run(cmd, cwd=cwd).returncode != 0:
                print("CLEAN CLONE FAILED at:", " ".join(map(str, cmd)))
                return 1
    print("Clean-clone check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
