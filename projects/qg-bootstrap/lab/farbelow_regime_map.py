"""Where the far-below localisation holds: the regime n >= 2J-3, tested both ways.

THE CLAIM UNDER TEST.  `results/FARBELOW_NEGATIVE_PATTERN.md` found that every
negative monomial of the far-below criterion sits in the single y-coefficient of
degree J-2 -- and then that this stops being true at large J.  Scanning n upward
at fixed J put the switch at n = 2J-3 exactly, at the corner and just off it.

A boundary claimed from corner scans is exactly the kind of claim ERR-0017 was
about, so this file tests it on a grid that can REFUTE it: points on both sides
of the line, several depths, and two off-corner values of each region variable.
A clean point outside the regime, or a dirty point inside it, would kill the law.

Everything is evaluated as certified `arb` numbers through the verified closed
form, so it reaches depths the polynomial expansion cannot.

Run: python lab/farbelow_regime_map.py -> results/farbelow_regime_map.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402
from repair_inequality_probe import all_coefficients_signs  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
ctx.prec = 1500


def main() -> int:
    t0 = time.time()
    rows, inside_bad, outside_clean = [], [], []
    n_inside = n_outside = 0
    for J in (7, 9, 12, 16, 20, 25, 30, 35, 40):
        for k3 in (0, 4):
            for thl in (0, 3):
                for v in range(0, 121, 3):
                    n = 44 + v
                    inside = n >= 2 * J - 3
                    neg = all_coefficients_signs(J, v, k3, thl)["negative_k"]
                    others = [k for k in neg if k != J - 2]
                    clean = not others
                    rows.append(
                        {"J": J, "n": n, "K3": k3, "thL": thl, "inside": inside, "clean": clean}
                    )
                    if inside:
                        n_inside += 1
                        if not clean:
                            inside_bad.append(
                                {"J": J, "n": n, "K3": k3, "thL": thl, "other_dips": others[:6]}
                            )
                    else:
                        n_outside += 1
                        if clean:
                            outside_clean.append({"J": J, "n": n, "K3": k3, "thL": thl})
    out = {
        "what": "does 'only c_{J-2} dips' hold exactly on n >= 2J-3?",
        "reading": "a dirty point inside the regime or a clean point outside it refutes the law; "
        "the grid deliberately contains both sides",
        "grid": "J = 7..40, n = 44..164 in steps of 3, K3 in {0,4}, thL in {0,3}",
        "points_tested": len(rows),
        "points_inside_regime": n_inside,
        "violations_inside_regime": len(inside_bad),
        "points_outside_regime": n_outside,
        "clean_points_outside_regime": len(outside_clean),
        "violations": inside_bad[:30],
        "unexpected_clean": outside_clean[:30],
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "farbelow_regime_map.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"{len(rows)} points: inside {n_inside} with {len(inside_bad)} violations; "
        f"outside {n_outside} with {len(outside_clean)} unexpectedly clean"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
