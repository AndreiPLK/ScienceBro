"""Skill-graph audit — adapted from Hermes Agent's "learning made visible".

What Hermes does (agent/learning_graph.py): skills + memory chunks are graph
nodes; edges come from declared related_skills and lexical overlap; usage
timestamps expose dead branches. We adapt the health-audit part for the
lab's skill system (~/.claude/skills + project .claude/skills + memory).

Report (stdout + docs/SKILL_GRAPH.md):
  - orphan skills: referenced by nothing (no memory pointer, no cross-link);
  - stale skills: not touched in STALE_DAYS while their domain is active;
  - missing/weak descriptions (recall quality depends on them);
  - the link graph itself (who references whom) for the founder's eyes.

Run: python tools/skill_audit.py  (light, seconds, no LLM calls)
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

HOME = Path.home()
SKILL_ROOTS = [
    HOME / ".claude" / "skills",
    Path(__file__).resolve().parents[1] / ".claude" / "skills",
]
MEMORY_DIR = HOME / ".claude" / "projects" / "C--Users-user-ScienceBro" / "memory"
OUT = Path(__file__).resolve().parents[1] / "docs" / "SKILL_GRAPH.md"
STALE_DAYS = 21


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip('"')
    return fm


def main() -> int:
    skills = {}
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        for md in root.glob("*/SKILL.md"):
            text = md.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(text)
            name = fm.get("name") or md.parent.name
            skills[name] = {
                "path": md, "desc": fm.get("description", ""),
                "body": text, "age_days":
                    (time.time() - md.stat().st_mtime) / 86400,
                "refs_out": set(), "refs_in": set(),
            }

    mem_text = ""
    if MEMORY_DIR.exists():
        for f in MEMORY_DIR.glob("*.md"):
            mem_text += f.read_text(encoding="utf-8", errors="replace")

    names = set(skills)
    for name, s in skills.items():
        for other in names - {name}:
            if re.search(rf"\b{re.escape(other)}\b", s["body"]):
                s["refs_out"].add(other)
                skills[other]["refs_in"].add(name)

    lines = ["# Skill graph health (auto: tools/skill_audit.py)", ""]
    orphans, stale, weak = [], [], []
    for name, s in sorted(skills.items()):
        in_memory = re.search(rf"\b{re.escape(name)}\b", mem_text) is not None
        if not s["refs_in"] and not in_memory:
            orphans.append(name)
        if s["age_days"] > STALE_DAYS:
            stale.append(f"{name} ({s['age_days']:.0f}d)")
        if len(s["desc"]) < 40:
            weak.append(name)

    lines += [f"Skills scanned: {len(skills)}", ""]
    lines += ["## Orphans (no memory pointer, no skill links — invisible "
              "at recall time)", ""]
    lines += [f"- {n}" for n in orphans] or ["- none"]
    lines += ["", f"## Stale (> {STALE_DAYS} days untouched)", ""]
    lines += [f"- {n}" for n in stale] or ["- none"]
    lines += ["", "## Weak descriptions (< 40 chars — recall depends on "
              "these)", ""]
    lines += [f"- {n}" for n in weak] or ["- none"]
    lines += ["", "## Link graph", ""]
    for name, s in sorted(skills.items()):
        if s["refs_out"]:
            lines.append(f"- {name} -> {', '.join(sorted(s['refs_out']))}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:40]))
    print(f"...full report: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
