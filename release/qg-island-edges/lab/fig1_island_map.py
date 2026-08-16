"""Iteration 3: reproduce Fig. 1 of arXiv:2406.02665 — the positivity island.

Exact-rational scan of the (r, w) plane at q=1, D=4: a point is ALLOWED if every
above-threshold partial-wave coefficient a_{n,l} with n <= NMAX is non-negative
(threshold caveat of p.6: impose only for mu(n) >= 4*mu0, with shifted spectrum
mu(n) = n + mu0).

Output: results/fig1_map_mu{...}.json with the exact verdict per grid point and,
for excluded points, the first negative (n, l).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import os

from repro_r4_positivity_spot import a_route1  # validated two-route in iteration 2

NMAX = int(os.environ.get("NMAX", "10"))
GRID = [F(i, 10) for i in range(-18, 19)]  # -1.8 .. 1.8 step 0.1
OUT_DIR = Path(__file__).resolve().parents[1] / "results"


def point_allowed(r: F, w: F, mu0: F, nmax: int = NMAX):
    """Return (allowed, first_negative) checking all above-threshold n <= nmax."""
    if 1 + r + w == 0 or 1 + r == 0:  # poles of the normalization: outside domain
        return False, ("domain", 0)
    for n in range(1, nmax + 1):
        if n + mu0 < 4 * mu0:  # below threshold: no positivity constraint (p.6)
            continue
        for ell in range(0, n + 1):
            try:
                a = a_route1(n, ell, r, w, mu0)
            except ZeroDivisionError:
                return False, ("domain", n)
            if a < 0:
                return False, (n, ell)
    return True, None


def main() -> int:
    mu0 = F(0)
    if len(sys.argv) > 1:
        num, _, den = sys.argv[1].partition("/")
        mu0 = F(int(num), int(den or 1))
    rows = []
    allowed_count = 0
    for r in GRID:
        for w in GRID:
            ok, first_neg = point_allowed(r, w, mu0)
            allowed_count += ok
            rows.append({"r": str(r), "w": str(w), "allowed": ok,
                         "first_negative": first_neg})
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"fig1_map_mu{mu0.numerator}_{mu0.denominator}_N{NMAX}.json"
    out.write_text(json.dumps({
        "nmax": NMAX, "D": 4, "mu0": str(mu0),
        "grid": [str(g) for g in GRID],
        "allowed_count": allowed_count, "total": len(rows),
        "rows": rows,
    }), encoding="utf-8")
    print(f"mu0={mu0}: {allowed_count}/{len(rows)} grid points allowed (n<={NMAX}, exact)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
