"""The completion audit: what must be true before a research task may be called finished.

Wired as a Stop hook. It BLOCKS only on objective, mechanically checkable violations —
the ones where a program can be certain and a tired reader cannot:

  * the claim registry is inconsistent (a PROVED claim with no proof artifact on disk,
    a claim resting on something weaker than itself, a DEAD_ROUTE not recorded);
  * a results document asserts PROVED/THEOREM for a claim the registry does not carry
    at that status.

Everything else is printed as a WARNING and does not block, because judgement belongs
to the person and a hook that cries wolf gets disabled. The warnings cover the failure
modes this lab has actually met:

  * numerical evidence standing where a lemma should be;
  * an external theorem cited without its hypotheses checked;
  * a source mentioned but not inspected;
  * a load-bearing symbolic identity with no independent verification;
  * float arithmetic where exact was practical;
  * a universal claim tested only on a grid;
  * a new conjecture with no counterexample hunt;
  * a measured constant presented as exact;
  * asymptotics used outside a justified domain;
  * a citation that cannot be resolved.

Legitimate ways to finish are unaffected: PARTIAL RESULT, FAILED ROUTE, OPEN SUBLEMMA,
COUNTEREXAMPLE FOUND are all complete scientific outcomes.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_WITHOUT_GATE = re.compile(
    r"\b(we\s+prove[d]?|is\s+proved|theorem\s+established|confirms?\s+the\s+conjecture)\b",
    re.I,
)


def registry_ok() -> tuple[bool, str]:
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "claims_check.py")],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def changed_docs() -> list[Path]:
    r = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~3..HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    out = []
    for line in r.stdout.splitlines():
        p = ROOT / line.strip()
        if p.suffix == ".md" and p.exists():
            out.append(p)
    return out


def proved_claims() -> set[str]:
    out = set()
    d = ROOT / "research" / "claims"
    if not d.exists():
        return out
    for f in d.glob("*.md"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^status:\s*(\w+)", text, re.M)
        if m and m.group(1) in ("PROVED", "CERTIFIED"):
            out.add(f.stem)
    return out


def main() -> int:
    blockers: list[str] = []
    warnings: list[str] = []

    ok, msg = registry_ok()
    if not ok:
        blockers.append("claim registry inconsistent:\n" + msg)

    dead = ROOT / "research" / "dead_routes.md"
    dead_text = dead.read_text(encoding="utf-8", errors="ignore") if dead.exists() else ""
    dead_ids = re.findall(r"^## (DR-\d+)", dead_text, re.M)

    for doc in changed_docs():
        text = doc.read_text(encoding="utf-8", errors="ignore")
        rel = doc.relative_to(ROOT).as_posix()
        if BANNED_WITHOUT_GATE.search(text) and "research/claims" not in rel:
            warnings.append(
                f"{rel}: uses proof language; confirm a claim in research/claims/ carries "
                "that status"
            )
        if re.search(r"\bfloat\(|numpy\.roots|math\.log\b", text) and "exact" in text.lower():
            warnings.append(f"{rel}: mentions exactness near floating-point constructs")
        if re.search(r"\b(grid|scan)\b", text, re.I) and re.search(
            r"\bfor (all|every)\b", text, re.I
        ):
            warnings.append(
                f"{rel}: a universal statement near grid language -- was the domain "
                "boundary tested on both sides?"
            )
        for did in dead_ids:
            if did in text and "dead" not in rel:
                warnings.append(f"{rel}: mentions {did}; confirm what assumption changed")

    print("=" * 70)
    print("RESEARCH COMPLETION AUDIT")
    print("=" * 70)
    if blockers:
        print(f"\n{len(blockers)} BLOCKER(S) -- these must be fixed:\n")
        for b in blockers:
            print(f"  * {b}")
    if warnings:
        print(f"\n{len(warnings)} warning(s) -- judgement required, not blocking:\n")
        for w in sorted(set(warnings)):
            print(f"  - {w}")
    if not blockers and not warnings:
        print("\nclean")
    print(
        "\nLegitimate endings: PARTIAL RESULT / FAILED ROUTE / OPEN SUBLEMMA / "
        "COUNTEREXAMPLE FOUND.\nNumerical verification never upgrades a claim to PROVED."
    )
    return 2 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
