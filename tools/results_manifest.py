"""The results index: which artefact is alive, which is superseded, which is a dead end.

Why this exists. `projects/qg-bootstrap/results/` holds 163 artefacts and 96 of
them are referenced by no paper and no document (docs/SYSTEM_ASSESSMENT_2026-08-18.md,
finding F3). A dead file and a load-bearing file look identical from outside, and
that is how a stale number reaches a paper.

Why the status lives HERE and not inside the artefacts. Raw results are immutable
(.claude/rules/experiment-contract.md). Editing 163 files to add a status field
would be rewriting the record. So the record stays untouched and the index sits
beside it.

Statuses:
  live        the artefact backs a current claim, paper or figure
  superseded  a later artefact covers the same ground -- kept, not deleted
  dead-end    produced by a route we closed; kept so the route is not rewalked
  retracted   the conclusion drawn from it was WRONG; see docs/ERRATA.md
  unreviewed  not yet classified (the honest default, never a hiding place)

Run:  uv run python tools/results_manifest.py          # refresh, keep decisions
      uv run python tools/results_manifest.py --check  # exit 1 if any file is missing
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "projects" / "qg-bootstrap" / "results"
MANIFEST = RES / "MANIFEST.yaml"
VALID = {"live", "superseded", "dead-end", "retracted", "unreviewed"}

# Hand-set statuses. Only entries I can justify; everything else stays
# `unreviewed` rather than being guessed into looking tidy.
CURATED: dict[str, tuple[str, str]] = {
    "FROZEN_PREDICTION_blocks.md": (
        "retracted",
        "the block-width step law was an artefact of scanning only even j; "
        "refuted by the full integer grid. Kept because freezing it first is "
        "exactly what made the refutation meaningful.",
    ),
    "step_lemma.json": (
        "retracted",
        "same step-6 artefact as FROZEN_PREDICTION_blocks.md",
    ),
    "OPEN_PROBLEM.md": (
        "live",
        "the standing statement of the open problem plus the list of CLOSED "
        "routes; read before any new attempt",
    ),
    "SCALING_LIMIT_THEOREM.md": (
        "live",
        "the bracket-to-the-power-(j-1) result and the parity mechanism that "
        "predicted knife 6 before it was computed",
    ),
    "jacobi_normal_form.json": (
        "live",
        "the reformulation the whole program now runs on; 4500 sign checks "
        "against the independent exact value, 0 mismatches",
    ),
    "knife_closed_form.json": ("live", "closed forms per knife, verified j = 2..6"),
    "wide_certificates.json": (
        "live",
        "525,346 coefficients computed exactly, 0 negatives -- the broadest evidence we have",
    ),
    "normal_form_certificates.json": ("live", "certificates from the normal-form route"),
    "knife4_box_proof.json": (
        "live",
        "knife 4 machine-proved to n <= 1000, lam <= 120 by exact Bernstein "
        "subdivision: 128,514 boxes, 0 open",
    ),
}


def _referenced_text() -> str:
    """Everything that could cite an artefact by name."""
    out = []
    for pat in (
        "projects/qg-bootstrap/**/*.tex",
        "projects/qg-bootstrap/**/*.md",
        "projects/qg-bootstrap/lab/*.py",
        "docs/**/*.md",
        "article/**/*.md",
        "release/**/*.md",
    ):
        for p in ROOT.glob(pat):
            if p.resolve() == MANIFEST.resolve():
                continue
            try:
                out.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return "\n".join(out)


def _first_added(rel: str) -> str:
    r = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "--format=%as",
            "-1",
            "--",
            f"projects/qg-bootstrap/results/{rel}",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return r.stdout.strip() or "untracked"


def artefacts() -> list[str]:
    out = []
    for p in sorted(RES.rglob("*")):
        if p.is_dir() or p.name == "MANIFEST.yaml" or p.suffix not in (".json", ".md"):
            continue
        out.append(p.relative_to(RES).as_posix())
    return out


def load() -> dict:
    if not MANIFEST.exists():
        return {}
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    return doc.get("artefacts", {}) or {}


def build(existing: dict) -> dict:
    refs = _referenced_text()
    out: dict[str, dict] = {}
    for rel in artefacts():
        name = Path(rel).name
        prev = existing.get(rel, {})
        if name in CURATED:
            status, note = CURATED[name]
        elif prev.get("status") in VALID and prev.get("status") != "unreviewed":
            status, note = prev["status"], prev.get("note", "")
        elif Path(rel).stem in refs:
            status = "live"
            note = "referenced by a paper, document or lab module"
        else:
            status = "unreviewed"
            note = "referenced nowhere; classify before relying on it"
        out[rel] = {"status": status, "note": note, "added": prev.get("added") or _first_added(rel)}
    return out


def main() -> int:
    check = "--check" in sys.argv
    existing = load()
    if check:
        missing = [a for a in artefacts() if a not in existing]
        if missing:
            print("artefacts absent from MANIFEST.yaml (run tools/results_manifest.py):")
            for m in missing:
                print("   ", m)
            return 1
        bad = [k for k, v in existing.items() if v.get("status") not in VALID]
        if bad:
            print("invalid status:", bad)
            return 1
        print(f"MANIFEST.yaml: {len(existing)} artefacts, all classified")
        return 0

    data = build(existing)
    counts: dict[str, int] = {}
    for v in data.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    header = (
        "# Index of result artefacts. The artefacts themselves are immutable\n"
        "# (.claude/rules/experiment-contract.md), so their status lives here.\n"
        "# Regenerate with: uv run python tools/results_manifest.py\n"
        "# Hand-set decisions are preserved; only new files get a default.\n"
    )
    MANIFEST.write_text(
        header
        + yaml.safe_dump({"artefacts": data}, sort_keys=True, allow_unicode=False, width=100),
        encoding="utf-8",
    )
    print(f"MANIFEST.yaml: {len(data)} artefacts")
    for k in sorted(counts):
        print(f"   {counts[k]:4d}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
