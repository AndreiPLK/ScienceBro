"""Targeted counterexample hunt where it is ACTUALLY dangerous: high spin.

Why this run exists (methodological defect found 2026-08-17).
lab/keystone_hunt.py hunted counterexamples only at SPINS l in {0,2,4,6}
— i.e. it implicitly assumed low-spin dominance. Today's measurement
(results/keystone_lowspin.json) shows that assumption is FALSE for the CHR
graviton family: over 36 (j, lam) cells, the level n minimising the
D-threshold NEVER sat at l <= 2. The minimisers sit at spins 10 to 86, and
the tightest cell in the whole sweep is

        j = 4, lam = 26, n = 44  ->  spin l = 80,
        threshold D* = 494.84  vs  shore = 489.93,   ratio 1.0100 .

So the old hunt was blind exactly where the margin is 1%. This script
hunts there, with the CORRECTED shore (ERR-0003).

FROZEN CRITERIA (stated before the run): a violation is an exact rational
point (j, n, lam, D) with 4 <= D < T_hat(lam) and P_j < 0, computed by the
ORIGINAL master formula (knife_proof2.Bj_coeffs + keystone_hunt.eval_P) —
not by the Beta reduction, so a bug in the reduction cannot hide a
violation. Any violation is a counterexample candidate for the grand
theorem and freezes the claim immediately.

Grid: lam packed around the dangerous seam (26) and its neighbours; n
swept through the minimiser region; D on a boundary-hugging ladder that
approaches the shore from below (down to 1 part in 10^6).

Run: python lab/keystone_hunt_highspin.py
Artifact: results/keystone_hunt_highspin.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_hunt import T_hat, eval_P  # noqa: E402
from knife_proof2 import Bj_coeffs  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def lam_points() -> list[Fraction]:
    pts = set()
    # dense around the dangerous seam lam = 26 and the neighbouring seams
    for base in (26, 45, 12, 60, 100):
        for i in range(-6, 7):
            pts.add(Fraction(base) + Fraction(i, 5))
    for k in range(3, 61):  # every branch seam
        pts.add(Fraction(3, 5) * (k - Fraction(5, 2)))
    pts |= {
        Fraction(1, 100),
        Fraction(1, 2),
        Fraction(3),
        Fraction(7),
        Fraction(150),
        Fraction(400),
    }
    return sorted(p for p in pts if p > 0)


def d_ladder(shore: Fraction) -> list[Fraction]:
    """D values hugging the shore from BELOW, plus a coarse sweep."""
    out = [Fraction(4)]
    for f in (Fraction(1, 2), Fraction(9, 10), Fraction(99, 100)):
        out.append(4 + (shore - 4) * f)
    for e in (3, 4, 5, 6):  # 1 - 10^-e of the way up
        out.append(shore - (shore - 4) / 10**e)
    return [d for d in out if 4 <= d < shore]


def main() -> int:
    t0 = time.time()
    checks, violations = 0, []
    lams = lam_points()
    worst = None  # smallest positive margin
    for j in range(2, 13):
        for n in range(max(4, j + 1), j + 60, 3):
            mv = n - 3
            if mv < max(1, j - 2):
                continue
            coeffs = Bj_coeffs(j, mv)
            spin = 2 * n - 2 * j
            for lam in lams:
                shore = T_hat(lam)
                if shore <= 4:
                    continue
                for D in d_ladder(shore):
                    P = eval_P(coeffs, lam, D)
                    checks += 1
                    pf = Fraction(int(P.p), int(P.q))
                    if pf <= 0:
                        violations.append(
                            {
                                "j": j,
                                "n": n,
                                "spin": spin,
                                "lam": str(lam),
                                "D": str(D),
                                "shore": str(shore),
                                "D_over_shore": float(D / shore),
                                "P": str(pf),
                            }
                        )
                    else:
                        rel = float(pf) / float(shore) ** 0
                        if worst is None or rel < worst[0]:
                            worst = (rel, j, n, spin, str(lam), str(D))
        print(
            f"  j={j}: checks {checks}, violations {len(violations)} ({time.time() - t0:.0f}s)",
            flush=True,
        )

    out = {
        "purpose": "counterexample hunt at HIGH SPIN, where the margin is"
        " actually smallest -- the earlier hunt only looked at"
        " spins 0,2,4,6 and was blind here",
        "frozen_criteria": "violation = exact rational (j,n,lam,D) with"
        " 4 <= D < T_hat(lam) and P_j <= 0, computed by"
        " the ORIGINAL master formula (not the Beta"
        " reduction)",
        "shore": "corrected per ERR-0003 (lam-adaptive k window)",
        "grid": {
            "j": "2..12",
            "n": "up to j+59 step 3",
            "spins_reached": "up to ~118",
            "lam": f"{len(lams)} points, packed around the seam at 26"
            " and every branch seam k=3..60",
            "D": "boundary-hugging ladder, closest approach 1 - 10^-6 of the way to the shore",
        },
        "exact_checks": checks,
        "violations": violations,
        "clean": not violations,
        "command": "python lab/keystone_hunt_highspin.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_hunt_highspin.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"exact checks {checks}, violations {len(violations)}", flush=True)
    print(
        "HIGH-SPIN HUNT " + ("CLEAN" if not violations else "FOUND VIOLATIONS -- freeze the claim"),
        flush=True,
    )
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
