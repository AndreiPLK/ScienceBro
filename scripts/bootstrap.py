"""Bootstrap: one-command environment setup + verification.

Usage: uv run python scripts/bootstrap.py
"""

import subprocess
import sys


def main() -> int:
    for cmd in [
        ["uv", "sync", "--all-groups"],
        [sys.executable, "-m", "pytest", "-q"],
        ["uv", "run", "sb", "doctor"],
    ]:
        print(f"== {' '.join(cmd)}")
        if subprocess.run(cmd).returncode != 0:
            print("BOOTSTRAP BLOCKED at:", " ".join(cmd))
            return 1
    print("Bootstrap OK. Next: uv run sb dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
