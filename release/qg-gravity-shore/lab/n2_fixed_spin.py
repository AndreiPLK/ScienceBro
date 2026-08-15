"""Night slice N2: fixed-spin tails a_{n,l} for l=0..3 up to n=100 (exact).

Goal: establish (numerically first) that for every island point the fixed-spin
coefficients are positive for all n beyond a small threshold, and extract the
empirical growth exponent p in a_{n,l} ~ C * n^p to guide the analytic
derivation (extension of Mansfield-Spradlin Thm 10 to w != 0).

Points: interior, near left edge, near the a_{2,0} hyperbola, w<0 side, plus
one EXCLUDED control point (must show a negative somewhere).
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repro_r4_positivity_spot import a_route1  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"

POINTS = [
    ("interior",      F(1, 4), F(1, 4)),
    ("interior2",     F(1, 2), F(-1, 4)),
    ("near-edge",     F(-12, 25), F(1, 2)),      # r=-0.48
    ("on-edge",       F(-1, 2), F(1, 2)),
    ("near-hyperb",   F(-3, 10), F(-1, 10)),     # близко к 3(1+r)(r+w)+1=0
    ("w-neg",         F(1, 1), F(-6, 5)),
    ("far-interior",  F(3, 2), F(-3, 2)),
    ("veneziano",     F(0), F(0)),
    ("small-w",       F(0), F(1, 10)),
    ("neg-r",         F(-2, 5), F(4, 5)),
    ("EXCLUDED-ctrl", F(-3, 5), F(1, 2)),        # вне острова (контроль)
    ("EXCLUDED-ctr2", F(-1, 4), F(-2, 5)),       # за гиперболой (контроль)
]
NS = [10, 20, 35, 50, 70, 100]
LS = [0, 1, 2, 3]


def main() -> int:
    out = []
    t0 = time.time()
    for name, r, w in POINTS:
        rec = {"name": name, "r": str(r), "w": str(w), "tail": {}}
        for l in LS:
            vals = []
            for n in NS:
                if l > n:
                    continue
                a = a_route1(n, l, r, w, F(0))
                vals.append({"n": n, "sign": (1 if a > 0 else (0 if a == 0 else -1)),
                             "log10": None if a == 0 else float(
                                 (len(str(abs(a.numerator))) - len(str(a.denominator)))
                             )})
            rec["tail"][str(l)] = vals
            neg = [v["n"] for v in vals if v["sign"] < 0]
            print(f"{name} l={l}: signs {[v['sign'] for v in vals]}"
                  f"{' NEG at n=' + str(neg) if neg else ''}  ({time.time()-t0:.0f}s)",
                  flush=True)
        out.append(rec)
    (RES / "n2_fixed_spin.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written n2_fixed_spin.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
