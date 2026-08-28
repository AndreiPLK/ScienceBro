"""Build the outreach visualisation page from the exact data.

Reads results/shore_landscape_data.json (exact rational computations, rendered
to floats only at export) and injects it into
outreach/shore_of_universes.template.html, producing
outreach/shore_of_universes.html.

The counts quoted in the page's prose are computed here from the data rather
than typed by hand, so the text cannot drift away from the picture.

Run: python lab/build_shore_viz.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "shore_landscape_data.json"
TPL = ROOT / "outreach" / "shore_of_universes.template.html"
OUT = ROOT / "outreach" / "shore_of_universes.html"


def compact(d: dict) -> dict:
    """Round display floats; the source of truth stays in the JSON artifact."""
    m = d["mountains"]
    return {
        "mountains": {
            "k": [round(x, 4) for x in m["k"]],
            "lam": [round(x, 4) for x in m["lam"]],
            "T": [[round(x, 2) for x in row] for row in m["T"]],
            "clamp": m["clamp"],
        },
        "shore": {
            "points": [
                {"lam": round(p["lam"], 4), "T": round(p["T"], 3), "k": p["k"]}
                for p in d["shore"]["points"]
            ],
            "level_jumps": [
                {"lam": round(j["lam"], 4), "T": round(j["T"], 3),
                 "from_k": j["from_k"], "to_k": j["to_k"]}
                for j in d["shore"]["level_jumps"]
            ],
        },
        "sign_fields": [
            {
                "n": f["n"], "j": f["j"],
                "rows": [
                    {"lam": round(r["lam"], 4), "D": [round(x, 3) for x in r["D"]],
                     "sign": r["sign"]}
                    for r in f["rows"]
                ],
            }
            for f in d["sign_fields"]
        ],
    }


def main() -> int:
    if not DATA.exists():
        print("run lab/shore_landscape_data.py first", flush=True)
        return 1
    d = json.loads(DATA.read_text(encoding="utf-8"))
    if d["negative_below_shore_total"] != 0:
        print("REFUSING TO BUILD: the data contains a negative knife below the shore "
              f"({d['negative_below_shore_total']} points). The page's claim would be "
              "false. Investigate before rebuilding.", flush=True)
        return 1

    dots = sum(1 for f in d["sign_fields"] for r in f["rows"] for s in r["sign"] if s != 0)
    neg = sum(1 for f in d["sign_fields"] for r in f["rows"] for s in r["sign"] if s < 0)
    jumps = len(d["shore"]["level_jumps"])
    stampline = f"exact data from commit {d.get('git', d.get('git_commit', 'unknown'))}"

    html = TPL.read_text(encoding="utf-8")
    html = html.replace("/*__DATA__*/ null", json.dumps(compact(d), separators=(",", ":")))
    html = html.replace("__DOTS__", f"{dots:,}")
    html = html.replace("__NEG__", f"{neg:,}")
    html = html.replace("__STAMP__", stampline)
    if "18 handovers" in html and jumps != 18:
        html = html.replace("18 handovers", f"{jumps} handovers")
    OUT.write_text(html, encoding="utf-8")
    print(f"written {OUT} ({OUT.stat().st_size // 1024} KB): "
          f"{dots} dots, {neg} negative, {jumps} level handovers", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
