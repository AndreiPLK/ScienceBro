"""Every result artefact is indexed, and new ones carry provenance.

Two findings from docs/SYSTEM_ASSESSMENT_2026-08-18.md, made mechanical:

  F3  96 of 163 artefacts were referenced nowhere, so a dead file and a
      load-bearing file were indistinguishable. Now every artefact must appear
      in results/MANIFEST.yaml with a status.
  F4  48 of 158 JSON artefacts carried no provenance. Existing ones are grandfathered
      (retrofitting provenance would be manufacturing it, not recording it);
      any NEW artefact must call lab/provenance.py stamp().
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "projects" / "qg-bootstrap" / "results"
MANIFEST = RES / "MANIFEST.yaml"
DEBT = Path(__file__).resolve().parent / "provenance_debt.txt"
VALID = {"live", "superseded", "dead-end", "retracted", "unreviewed"}
PROV_KEYS = {"git", "git_full", "git_commit", "commit", "command", "stamp"}


def _indexed() -> dict:
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    return doc.get("artefacts", {}) or {}


def _artefacts() -> list[str]:
    return [
        p.relative_to(RES).as_posix()
        for p in sorted(RES.rglob("*"))
        if not p.is_dir() and p.name != "MANIFEST.yaml" and p.suffix in (".json", ".md")
    ]


def test_every_artefact_is_indexed():
    """A new result file must be classified, not left to become sediment."""
    indexed = _indexed()
    missing = [a for a in _artefacts() if a not in indexed]
    assert not missing, (
        "these artefacts are not in results/MANIFEST.yaml -- run "
        "`uv run python tools/results_manifest.py` and set a status:\n  " + "\n  ".join(missing)
    )


def test_statuses_are_valid():
    bad = {k: v.get("status") for k, v in _indexed().items() if v.get("status") not in VALID}
    assert not bad, f"invalid statuses (allowed: {sorted(VALID)}): {bad}"


def test_new_json_artefacts_carry_provenance():
    """Grandfather the pre-rule files; require a stamp on everything new."""
    debt = set()
    if DEBT.exists():
        debt = {
            ln.strip()
            for ln in DEBT.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        }
    bad = []
    for rel in _artefacts():
        if not rel.endswith(".json") or rel in debt:
            continue
        try:
            doc = json.loads((RES / rel).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(doc, dict) and not (PROV_KEYS & set(doc)):
            bad.append(rel)
    assert not bad, (
        "new artefacts must be stamped by lab/provenance.py stamp() "
        "(.claude/rules/experiment-contract.md):\n  " + "\n  ".join(bad)
    )


def test_manifest_matches_the_generator():
    """The committed manifest is what the tool produces -- no hand edits that drift."""
    r = subprocess.run(
        ["uv", "run", "python", "tools/results_manifest.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
