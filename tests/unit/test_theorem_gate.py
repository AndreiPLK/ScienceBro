"""Deterministic theorem-consolidation gate (ERR-0002 + fleet review S3).

A *_theorem.json may claim COMPLETE only if EVERY artifact it cites:
  - exists and parses;
  - records a recognized PASS flag set to true;
  - was produced for the SAME knife j as the theorem file;
  - did real work (cells/coefficients > 0 where the field exists);
  - has no nested false verdict in `pieces` / `stage_verdicts`;
  - was not produced by a partial run (env.KNIFE_STAGE must be all/absent);
  - was produced from a CLEAN tree (dirty must be false when present).
Every value inside `regions` must be an artifact filename (no prose).
This is a hard gate in `sb check` / pytest — no LLM judgment involved.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "results"

PASS_FLAGS = ("all_certified", "far_below_factored", "far_below_interval", "ok_so_far", "all_unsat")
COUNT_FIELDS = ("cells", "y_coefficients")
ARTIFACT_RE = re.compile(r"^[\w][\w\-]*\.json$")
COMPLETE_RE = re.compile(r"\bCOMPLETE\b")


def artifact_problems(path: Path, expect_j: int) -> list[str]:
    if not path.exists():
        return ["missing"]
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"unparsable: {exc}"]
    bad = []
    flag = next((f for f in PASS_FLAGS if f in d), None)
    if flag is None:
        bad.append("no recognized pass flag")
    elif not d[flag]:
        bad.append(f"{flag}=false")
    if "j" in d and int(d["j"]) != expect_j:
        bad.append(f"j={d['j']} but theorem is j={expect_j}")
    counts = [d[f] for f in COUNT_FIELDS if f in d]
    if counts and not all(int(c) > 0 for c in counts):
        bad.append("zero work recorded (cells/coefficients = 0)")
    if not counts and flag in ("all_certified", "ok_so_far"):
        bad.append("no work counter recorded")
    for nested in ("pieces", "stage_verdicts"):
        for k, v in (d.get(nested) or {}).items():
            if v is False:
                bad.append(f"{nested}.{k} is false")
    stage = (d.get("env") or {}).get("KNIFE_STAGE")
    if stage not in (None, "all"):
        bad.append(f"partial run: KNIFE_STAGE={stage}")
    if d.get("dirty") is True:
        bad.append("produced from a dirty working tree")
    return bad


def test_no_complete_theorem_without_passing_artifacts():
    problems = []
    for tf in sorted(RESULTS.glob("knife*_theorem.json")):
        doc = json.loads(tf.read_text(encoding="utf-8"))
        if not COMPLETE_RE.search(str(doc.get("status", "")).upper()):
            continue
        mj = re.search(r"knife(\d+)_theorem", tf.name)
        expect_j = int(mj.group(1)) if mj else -1
        regions = doc.get("regions") or {}
        if not regions:
            problems.append(f"{tf.name}: COMPLETE with no regions")
            continue
        for key, val in regions.items():
            if not isinstance(val, str) or not ARTIFACT_RE.match(val):
                problems.append(f"{tf.name}: region '{key}' is not an artifact filename ({val!r})")
                continue
            for bad in artifact_problems(RESULTS / val, expect_j):
                problems.append(f"{tf.name}: {val} -> {bad}")
    assert not problems, "THEOREM GATE VIOLATIONS:\n" + "\n".join(problems)
