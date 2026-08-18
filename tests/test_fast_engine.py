"""The fast-engine law, enforced by a test instead of by the founder.

He has caught the same mistake repeatedly: new computational code written on
python `fractions.Fraction` (or numpy.roots, or float comparisons of exact
quantities) when flint is available and is the project's engine. Promises did
not hold, so this test does the catching.

ERR-0006 (2026-08-18): `depth_proof.py` passed this exact test while doing real
sympy bulk work (`.expand`/`.factor`/`.Poly` on the object being proved) behind
a false "ENGINE-OK, symbolic setup only" comment -- because back then, `import
flint` ANYWHERE in a file gave the whole file a free pass, even a file that
ALSO imported sympy and used it for heavy polynomial work. A file that imports
BOTH is exactly the dangerous case: it looks compliant at a glance. So sympy
heavy-use is now checked independently of whether flint is also imported --
importing flint no longer exempts a file that also does sympy bulk work.

A lab module may use Fraction only for interface glue (parameters, printing) or
with an explicit `# ENGINE-OK: <reason>` marker on the module. Anything that
computes in a loop must use flint. sympy is for one-off symbolic derivation
only, never for the actual object being proved -- see CLAUDE.md's fast-engine
law for the founder's exact words on this.
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

# ERR-0006: sympy doing BULK polynomial work (not one-off symbolic derivation)
# is banned outright, regardless of whether flint is also imported in the same
# file. These are the calls that actually chew memory on a growing object.
USES_SYMPY = re.compile(r"^\s*(import sympy|from sympy)\b", re.M)
SYMPY_BULK = re.compile(
    r"\.(?:expand|factor|factor_squarefree|simplify|nsimplify|together|resultant|discriminant)\s*\("
    r"|\bsp\.Poly\s*\(|\bsympy\.Poly\s*\("
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

        # sympy bulk-work check first: an ENGINE-OK marker can still exempt it
        # (a human reviewed and accepted the specific reason), but a plain
        # `import flint` elsewhere in the file CANNOT -- that combination is
        # exactly what let ERR-0006 through.
        if USES_SYMPY.search(src) and SYMPY_BULK.search(src) and MARKER not in src:
            offenders.append(
                f"{path.relative_to(ROOT)}: sympy used for bulk polynomial work "
                "(.expand/.factor/.simplify/.together/sp.Poly) -- banned outright "
                "unless there is genuinely no flint way and a human-reviewed "
                "'# ENGINE-OK: <reason>' says so"
            )
            continue

        # An IMPORT of flint exempts a file from the Fraction/numpy.roots checks
        # below; a mere mention in a comment does not. That hole let
        # knife4_proof.py through once already.
        imports_flint = (
            "from flint import" in src or "import flint" in src or "from fastnum import" in src
        )
        if MARKER in src or imports_flint:
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
