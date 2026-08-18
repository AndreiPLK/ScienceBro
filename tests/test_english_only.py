"""Everything in this repository is written in English. Enforced, not promised.

Founder, 2026-08-18: "we never write any rules in Russian. This is code, it is
English only, everything in English. Russian is how I talk to you."

The same shape as the fast-engine guard: a debt register of files that predate
the rule, which may SHRINK but never grow, and a hard failure for anything new.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBT_FILE = Path(__file__).resolve().parent / "english_only_debt.txt"
CYRILLIC = re.compile("[\u0400-\u04ff]")
SKIP = (".git/", ".venv", "node_modules", "release/", "upstream/", "__pycache__", "/tmp/")
EXTS = {".md", ".py", ".txt", ".yaml", ".yml", ".json", ".html", ".tex"}


def _debt() -> set:
    if not DEBT_FILE.exists():
        return set()
    return {
        line.strip()
        for line in DEBT_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def _offenders() -> list:
    debt = _debt()
    out = []
    for p in ROOT.rglob("*"):
        if p.is_dir() or p.suffix not in EXTS:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if any(s in "/" + rel for s in SKIP) or rel in debt:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        n = len(CYRILLIC.findall(text))
        if n:
            out.append(f"{rel}: {n} Cyrillic characters")
    return out


def test_no_new_russian_in_the_repository():
    bad = _offenders()
    assert not bad, (
        "New files must be written in English (CLAUDE.md). Translate them, or -- "
        "only for files that predate the rule -- add the path to "
        "tests/english_only_debt.txt:\n  " + "\n  ".join(bad)
    )


def test_debt_register_only_lists_real_files():
    """The register is a backlog, not a hiding place."""
    missing = sorted(rel for rel in _debt() if not (ROOT / rel).exists())
    assert not missing, f"debt register lists files that no longer exist: {missing}"
