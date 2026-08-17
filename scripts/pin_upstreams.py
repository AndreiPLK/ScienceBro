"""Compare pinned commits in vendor/upstream-manifest.yaml against remote HEADs.

Read-only: prints a diff report; never updates pins automatically
(update policy is manual with a recorded reason — roadmap Phase 2).

Usage: uv run python scripts/pin_upstreams.py
"""

import subprocess
from pathlib import Path

from ruamel.yaml import YAML


def remote_head(url: str, ref: str = "HEAD") -> str | None:
    try:
        r = subprocess.run(
            ["git", "ls-remote", url, ref], capture_output=True, text=True, timeout=30
        )
        return r.stdout.split()[0] if r.returncode == 0 and r.stdout else None
    except Exception:
        return None


def main() -> int:
    manifest = Path(__file__).resolve().parents[1] / "vendor" / "upstream-manifest.yaml"
    data = YAML(typ="safe").load(manifest.read_text(encoding="utf-8"))
    drift = 0
    for up in data["upstreams"]:
        ref = f"refs/heads/{up['branch']}" if up.get("branch") else "HEAD"
        head = remote_head(up["repository"], ref)
        pinned = up["pinned_commit"]
        if head is None:
            print(f"?? {up['name']}: remote unreachable")
        elif head == pinned:
            print(f"ok {up['name']}: {pinned[:8]}")
        else:
            drift += 1
            print(
                f"!! {up['name']}: pinned {pinned[:8]} but remote {ref} is {head[:8]} "
                f"(update manually + record reason in docs/DECISIONS.md)"
            )
    return 0 if drift == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
