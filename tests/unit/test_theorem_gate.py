"""Deterministic theorem-consolidation gate (ERR-0002: never again).

A *_theorem.json may claim COMPLETE only if EVERY artifact it cites exists
and records a recognized PASS flag. This is a hard gate in `sb check` /
pytest — no LLM judgment involved. A consolidation JSON is a claim like any
other: no COMPLETE without machine-checkable passing evidence.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "results"

PASS_FLAGS = ("all_certified", "far_below_factored", "ok_so_far", "all_unsat")
ARTIFACT_RE = re.compile(r"[\w][\w\-]*\.json")


def artifact_passes(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    data = json.loads(path.read_text(encoding="utf-8"))
    for flag in PASS_FLAGS:
        if flag in data:
            return bool(data[flag]), f"{flag}={data[flag]}"
    return False, "no recognized pass flag"


def test_no_complete_theorem_without_passing_artifacts():
    problems = []
    for tf in sorted(RESULTS.glob("*_theorem.json")):
        doc = json.loads(tf.read_text(encoding="utf-8"))
        status = str(doc.get("status", ""))
        if not re.search(r"\bCOMPLETE\b", status.upper()):
            continue  # downgraded/in-progress theorems are allowed to exist
        cited = set(ARTIFACT_RE.findall(json.dumps(doc.get("regions", {}))))
        cited.discard(tf.name)
        if not cited:
            problems.append(f"{tf.name}: COMPLETE with no cited artifacts")
            continue
        for name in sorted(cited):
            ok, why = artifact_passes(RESULTS / name)
            if not ok:
                problems.append(f"{tf.name}: cites {name} -> {why}")
    assert not problems, (
        "THEOREM GATE VIOLATIONS (a consolidation may claim COMPLETE only "
        "when every cited artifact records a PASS):\n" + "\n".join(problems)
    )
