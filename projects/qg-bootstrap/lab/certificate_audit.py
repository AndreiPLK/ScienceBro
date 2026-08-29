"""Read the certificate artefacts back and say exactly what is certified.

This exists because the ad-hoc version of it had two bugs in one evening, and
both pushed the recorded claim off the data:

* it globbed `repair_certificate_j*.json` and read the FULL-REGION artefact for a
  depth that also has an IN-REGIME one under a `_v<offset>` suffix, so J = 45
  looked uncertified when its in-regime run had certified it;
* it looked for a key named `bernstein`, while the module writes
  `bernstein_in_thL`, so every depth was reported as certified by monomial signs
  even where a Bernstein step had been needed.

The first bug made a true claim look false and cost a correction in the wrong
direction. So the audit is a module now, with the key names in one place.

A depth counts as certified if ANY of its artefacts certifies it; the row records
which shift that took and by which of the two tests.

Run: python lab/certificate_audit.py -> results/certificate_audit.json
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
NAME = re.compile(r"repair_certificate_j(\d+)(?:_v(\d+))?\.json$")


def verdict(d: dict) -> tuple[bool, str]:
    """Certified, and by which test -- tolerant of the older artefact schema."""
    bern = d.get("bernstein_in_thL")
    if d.get("certified") is not None:
        by = "Bernstein in thL" if bern and not d.get("manifestly_positive") else "monomial signs"
        return bool(d["certified"]), by
    # older schema: no Bernstein step existed, so manifest positivity was the whole test
    return bool(d.get("manifestly_positive", d.get("negative_monomials") == 0)), "monomial signs"


def main() -> int:
    t0 = time.time()
    by_depth: dict[int, list[dict]] = {}
    for f in sorted(RES.glob("repair_certificate_j*.json")):
        m = NAME.search(f.name)
        if not m:
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        ok, how = verdict(d)
        by_depth.setdefault(int(m.group(1)), []).append(
            {
                "v_offset": int(m.group(2) or 0),
                "certified": ok,
                "by": how,
                "negative_monomials": d.get("negative_monomials"),
                "artefact": f.name,
            }
        )

    rows = []
    for J in sorted(by_depth):
        good = [r for r in by_depth[J] if r["certified"]]
        best = min(good, key=lambda r: r["v_offset"]) if good else None
        rows.append(
            {
                "j": J,
                "certified": bool(good),
                "smallest_certified_v_offset": best["v_offset"] if best else None,
                "by": best["by"] if best else None,
                "runs": by_depth[J],
            }
        )
        mark = "CERT" if good else "NO  "
        detail = f"v>={best['v_offset']:<3} {best['by']}" if best else "-"
        print(f"  J={J:<3} {mark}  {detail}")

    cert = [r["j"] for r in rows if r["certified"]]
    out = {
        "what": "which depths the repair criterion (R) is certified at, read back from artefacts",
        "certified_depths": cert,
        "uncertified_depths": [r["j"] for r in rows if not r["certified"]],
        "full_region": [r["j"] for r in rows if r["smallest_certified_v_offset"] == 0],
        "in_regime_only": [
            r["j"] for r in rows if r["certified"] and r["smallest_certified_v_offset"]
        ],
        "needed_a_bernstein_step": [r["j"] for r in rows if r["by"] == "Bernstein in thL"],
        "rows": rows,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "certificate_audit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\ncertified: {cert}")
    print(f"  full region: {out['full_region']}")
    print(f"  in regime only: {out['in_regime_only']}")
    print(f"  needed a Bernstein step: {out['needed_a_bernstein_step']}")
    return 0 if not out["uncertified_depths"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
