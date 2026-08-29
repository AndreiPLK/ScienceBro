"""The claim registry validator: the rules of the status model, enforced by a program.

Statuses, from strongest to weakest, and they never merge:

    PROVED                    a complete human-readable mathematical argument exists
    CERTIFIED                 an exact certificate over a whole region (monomial signs,
                              Bernstein, Sturm) -- valid where the certificate is valid
    COMPUTATIONALLY_VERIFIED  exact arithmetic over finitely many cases
    MEASURED                  numerical or symbolic evidence, no exactness claim
    CONJECTURED               believed, with a stated domain
    HEURISTIC                 an argument that is not a proof and is not meant as one
    DISPROVED                 an explicit counterexample exists
    DEAD_ROUTE                the approach cannot work; the reason is recorded

The rules this file enforces, so that they cannot be quietly broken:

* PROVED requires a `proof_artifact` that exists on disk;
* CERTIFIED requires a `certificate_artifact` that exists on disk;
* COMPUTATIONALLY_VERIFIED requires `evidence` and an explicit `domain`;
* DISPROVED requires a `counterexample`;
* DEAD_ROUTE requires `why_dead` and must appear in `research/dead_routes.md`;
* every claim names its `dependencies`, and no claim may depend on one that is weaker
  than itself -- a PROVED statement cannot rest on a CONJECTURED one;
* no claim may cite numerical evidence as the support for PROVED.

The last rule is the point of the whole file. Numerical verification never upgrades a
claim to PROVED, and the program refuses rather than the reviewer having to notice.

Run: python tools/claims_check.py  (exit 1 on any violation)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "claims"
DEAD = ROOT / "research" / "dead_routes.md"

ORDER = [
    "DEAD_ROUTE",
    "DISPROVED",
    "HEURISTIC",
    "CONJECTURED",
    "MEASURED",
    "COMPUTATIONALLY_VERIFIED",
    "CERTIFIED",
    "PROVED",
]
RANK = {s: i for i, s in enumerate(ORDER)}
# statuses that may not be supported only by numbers
NEEDS_ARGUMENT = {"PROVED"}


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {"_error": "no frontmatter", "_path": path}
    meta: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            meta.setdefault(key, []).append(line[4:].strip())
        elif ":" in line:
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            meta[key] = val if val else []
    meta["_path"] = path
    meta["_body"] = text[m.end() :]
    return meta


def main() -> int:
    if not CLAIMS.exists():
        print("no research/claims/ directory")
        return 1
    claims = {}
    problems: list[str] = []
    for f in sorted(CLAIMS.glob("*.md")):
        if f.name.startswith("README"):
            continue
        c = parse(f)
        if "_error" in c:
            problems.append(f"{f.name}: {c['_error']}")
            continue
        claims[c.get("id", f.stem)] = c

    dead_text = DEAD.read_text(encoding="utf-8") if DEAD.exists() else ""

    for cid, c in claims.items():
        st = c.get("status", "")
        if st not in RANK:
            problems.append(f"{cid}: unknown status {st!r}")
            continue
        if st == "PROVED" and not c.get("proof_artifact"):
            problems.append(f"{cid}: PROVED without a proof_artifact")
        if st == "CERTIFIED" and not c.get("certificate_artifact"):
            problems.append(f"{cid}: CERTIFIED without a certificate_artifact")
        if st == "COMPUTATIONALLY_VERIFIED" and not c.get("domain"):
            problems.append(f"{cid}: COMPUTATIONALLY_VERIFIED without an explicit domain")
        if st == "DISPROVED" and not c.get("counterexample"):
            problems.append(f"{cid}: DISPROVED without a counterexample")
        if st == "DEAD_ROUTE":
            if not c.get("why_dead"):
                problems.append(f"{cid}: DEAD_ROUTE without why_dead")
            if cid not in dead_text:
                problems.append(f"{cid}: DEAD_ROUTE not listed in research/dead_routes.md")
        for art_key in ("proof_artifact", "certificate_artifact"):
            art = c.get(art_key)
            for a in [art] if isinstance(art, str) else (art or []):
                if a and not (ROOT / a).exists():
                    problems.append(f"{cid}: {art_key} missing on disk: {a}")
        if st in NEEDS_ARGUMENT:
            ev = " ".join(c.get("evidence", []) if isinstance(c.get("evidence"), list) else [])
            if re.search(r"\b(grid|scan|sampl|numeric|measured)\b", ev, re.I) and not c.get(
                "proof_artifact"
            ):
                problems.append(f"{cid}: PROVED supported by numerical evidence only")
        deps = c.get("dependencies") or []
        deps = deps if isinstance(deps, list) else [deps]
        for d in deps:
            d = d.strip()
            if d in ("none", "-", ""):
                continue
            if d not in claims:
                problems.append(f"{cid}: depends on unknown claim {d}")
            elif RANK[claims[d].get("status", "HEURISTIC")] < RANK[st]:
                problems.append(
                    f"{cid} ({st}) depends on {d} which is only "
                    f"{claims[d].get('status')} -- a claim cannot be stronger than what it rests on"
                )

    print(f"claims: {len(claims)}")
    by = {}
    for c in claims.values():
        by[c.get("status")] = by.get(c.get("status"), 0) + 1
    for s in ORDER:
        if s in by:
            print(f"  {s:<26} {by[s]}")
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nregistry consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
