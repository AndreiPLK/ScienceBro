"""Keystone step 1: adversarial counterexample hunt in the FIXED-SPIN regime.

The grand completeness theorem needs all knives j at once, including j
growing with n (fixed spin l = 2n - 2j small). Per protocol, BEFORE any
proof attempt we hunt for counterexamples exactly there.

FROZEN CRITERIA (before results): a violation is an exact rational point
(lam, D, n, j) with 4 <= D <= T_hat(lam) = min_{3<=k<=60} T_k(lam) and
P_j = (-1)^{j-1} B_j < 0 (exact fmpq arithmetic, no floats). Any violation
is a counterexample candidate for the grand theorem (double-check + freeze).
Grid: l in {0,2,4,6}; n = l/2+j+... i.e. j = n - l/2, n up to NMAX;
lam: dense rational grid incl. branch seams k(k+1) transitions, tiny lam,
lam near 26; D: 4, midpoints, T_hat - eps ladder (boundary-hugging).

Artifact: results/keystone_hunt.json (checks, violations, runtime).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import Bj_coeffs  # exact integer coefficients

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = int(os.environ.get("NMAX", "120"))
SPINS = [0, 2, 4, 6]


def T_k(k, lam):
    return Fraction(3 * (2 * k - 3), k * (k - 2)) * (lam * lam + (2 * k - 2) * lam + 1) + 2 * k


def T_hat(lam):
    """The shore: min over ALL k >= 3, with an lam-adaptive scan window.

    ERR-0003 (found 2026-08-17): this used a hard-coded range(3, 61). For
    large lam the minimising k grows like sqrt(3)*lam, so the cap silently
    OVERESTIMATED the shore: 1.06x at lam = 60, 1.47x at lam = 150, 5.96x
    at lam = 1000. The older release code (release/qg-blade-theorem/lab/
    bruteforce_recheck.py) already scanned an adaptive window -- the new
    code was a regression against the old one. Published results were NOT
    affected (their scripts scan range(3, 400) or range(3, 3000), and the
    bruteforce recheck used min(4000, 3*lam+50)); the keystone_* artifacts
    of 2026-08-17 were, and are regenerated.
    """
    kmax = max(61, int(3 * lam) + 60)
    return min(T_k(k, lam) for k in range(3, kmax))


def lam_grid():
    pts = set()
    for base in range(1, 46):  # branch seams and midpoints
        pts.add(Fraction(3, 5) * (base - Fraction(5, 2)))
        pts.add(Fraction(3, 5) * base - Fraction(9, 10))
    pts |= {Fraction(1, 10**k) for k in range(1, 7)}  # tiny lam
    pts |= {Fraction(26) + Fraction(i, 7) for i in range(-3, 8)}  # deep seam
    pts |= {Fraction(i, 3) for i in range(1, 130)}  # dense sweep
    return sorted(p for p in pts if p > 0)


def eval_P(coeffs, lam, D):
    lamq, Dq = fmpq(lam.numerator, lam.denominator), fmpq(D.numerator, D.denominator)
    lam_pows, d_pows = {0: fmpq(1)}, {0: fmpq(1)}
    for p in range(1, max(pp for pp, _ in coeffs) + 1):
        lam_pows[p] = lam_pows[p - 1] * lamq
    for q in range(1, max(qq for _, qq in coeffs) + 1):
        d_pows[q] = d_pows[q - 1] * Dq
    return sum(fmpq(c) * lam_pows[p] * d_pows[q] for (p, q), c in coeffs.items())


def main() -> int:
    t0 = time.time()
    checks, violations = 0, []
    grid = lam_grid()
    for l in SPINS:
        for n in range(max(4, l // 2 + 2), NMAX + 1, 3):
            j = n - l // 2
            mv = n - 3
            if j < 2 or mv < max(1, j - 2):
                continue
            coeffs = Bj_coeffs(j, mv)
            for lam in grid:
                Th = T_hat(lam)
                if Th <= 4:
                    continue
                Ds = [
                    Fraction(4),
                    (Fraction(4) + Th) / 2,
                    Th - (Th - 4) / 1000,
                    Th - (Th - 4) / 10**6,
                    Th,
                ]
                for D in Ds:
                    val = eval_P(coeffs, lam, D)
                    checks += 1
                    if val < 0:
                        violations.append(
                            {"l": l, "n": n, "j": j, "lam": str(lam), "D": str(D), "P": str(val)}
                        )
                        print(f"VIOLATION l={l} n={n} lam={lam} D={D}", flush=True)
        print(f"spin l={l}: done ({checks} checks, {time.time() - t0:.0f}s)", flush=True)
    git = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = {
        "regime": "fixed spin l=2n-2j, boundary-hugging exact grid",
        "frozen_criterion": "violation iff P_j<0 exact, 4<=D<=T_hat(lam)",
        "nmax": NMAX,
        "spins": SPINS,
        "checks": checks,
        "violations": violations,
        "command": f"NMAX={NMAX} python lab/keystone_hunt.py",
        "git": git,
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_hunt.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(
        ("NO VIOLATIONS" if not violations else f"{len(violations)} VIOLATIONS")
        + f" in {checks} checks",
        flush=True,
    )
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
