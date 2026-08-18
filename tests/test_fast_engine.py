"""The fast-engine law, enforced by a test instead of by the founder.

He has caught the same mistake repeatedly: new computational code written on
python `fractions.Fraction` (or numpy.roots, or float comparisons of exact
quantities) when flint is available and is the project's engine. Promises did not
hold, so this test does the catching.

A lab module may use Fraction only for interface glue (parameters, printing) or
with an explicit `# ENGINE-OK: <reason>` marker on the module. Anything that
computes in a loop must use flint.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB_DIRS = sorted((ROOT / "projects").glob("*/lab"))
MARKER = "# ENGINE-OK:"

DEBT_FILE = Path(__file__).resolve().parent / "fast_engine_debt.txt"


def _debt() -> set[str]:
    """Modules written before the law. The register may shrink, never grow."""
    if not DEBT_FILE.exists():
        return set()
    return {
        line.strip()
        for line in DEBT_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


HEAVY = re.compile(r"^\s*(for|while)\b", re.M)
SLOW = (
    ("fractions.Fraction in a loop", re.compile(r"\bFraction\b")),
    ("numpy.roots (use fmpq_poly.complex_roots)", re.compile(r"np\.roots|numpy\.roots")),
)


def _modules():
    for lab in LAB_DIRS:
        for path in sorted(lab.glob("*.py")):
            if path.name.startswith("_"):
                continue
            yield path


def test_new_lab_modules_use_the_fast_engine():
    debt = _debt()
    offenders = []
    for path in _modules():
        if path.relative_to(ROOT).as_posix() in debt:
            continue
        src = path.read_text(encoding="utf-8")
        if MARKER in src or "flint" in src:
            continue
        if not HEAVY.search(src):
            continue
        for why, pattern in SLOW:
            if pattern.search(src):
                offenders.append(f"{path.relative_to(ROOT)}: {why}")
    assert not offenders, (
        "New computational modules must use the flint engine (see CLAUDE.md, "
        "ЗАКОН БЫСТРОГО ДВИЖКА). Port them, or add '# ENGINE-OK: <reason>' if "
        "the slow path is genuinely the right choice here:\n  " + "\n  ".join(offenders)
    )


def test_debt_register_only_lists_real_files():
    """The register is a debt list, not a hiding place: no phantom entries."""
    missing = sorted(rel for rel in _debt() if not (ROOT / rel).exists())
    assert not missing, f"debt register lists files that no longer exist: {missing}"
