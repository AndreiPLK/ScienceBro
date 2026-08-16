"""Honest provenance stamping for every artifact (fleet review S2/S8 fix).

Records the git HEAD *and* whether the working tree was dirty, plus platform
and python/flint versions. A PASS artifact from a dirty tree is stamped
dirty:true so the gate (tests/unit/test_theorem_gate.py) can reject it.
"""

from __future__ import annotations

import platform
import subprocess
import sys


def _sh(args):
    try:
        return subprocess.run(args, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
        return ""


def stamp(extra=None):
    head = _sh(["git", "rev-parse", "HEAD"])
    dirty_files = [ln for ln in _sh(["git", "status", "--porcelain"]).splitlines()
                   if ln.strip()]
    try:
        import flint
        fv = getattr(flint, "__version__", "unknown")
    except Exception:
        fv = "absent"
    out = {
        "git": head[:12],
        "git_full": head,
        "dirty": bool(dirty_files),
        "dirty_count": len(dirty_files),
        "python": sys.version.split()[0],
        "flint": fv,
        "platform": platform.platform(),
    }
    if extra:
        out.update(extra)
    return out
