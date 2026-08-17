"""CHR closed form for the knife brackets (keystone milestone).

RESULT (verified exactly, 8/8 + battery below):

    P_j(n, lam, D) = c0 * SUM_{t=0}^{j-1} (-1)^t E_{2t}(n)
                     * (1-j)_t (1-R)_t / ( (1-n)_t (3/2-n)_t s^{2t} )

with  s = lam + n - 1,  c = 4n - 4j - 1,  R = (D + c)/2 + j - 1,
      c0 = (2n-2)! / ((j-1)! 2^{j-1}) * s^{2(j-1)}  > 0,
      E_{2t}(n) = even elementary symmetric functions of the doubled
      Pochhammer roots (paper 3), i.e. coefficients of prod_k (1+(n-2k)z)^2.

Two structural facts follow immediately:
  * (1-j)_t TERMINATES the sum at t = j-1 — this is a terminating
    hypergeometric-type sum, so classical summation/positivity machinery
    (Saalschutz, Whipple, Gasper) becomes applicable;
  * the ONLY j-dependence left is the Pochhammer (1-j)_t and c0 > 0 —
    the j -> j+1 step is now an explicit shift, which is exactly what the
    keystone (uniform-in-j argument) needs.

Analogue of Rigatos-Wang arXiv:2401.13031 eq.(27)-(28) for the Coon family;
here derived for the CHR graviton family with the deformation parameter lam.

Run: python lab/chr_closed_form.py  -> results/chr_closed_form.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_hunt import T_hat, eval_P  # noqa: E402
from knife_proof2 import Bj_coeffs, e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def poch(a, t):
    p = Fraction(1)
    for r in range(t):
        p *= a + r
    return p


def P_closed(j, n, lam, D):
    e = e_doubled_int(n)
    c = Fraction(4 * n - 4 * j - 1)
    s = lam + n - 1
    R = (D + c) / 2 + j - 1
    c0 = Fraction(factorial(2 * n - 2), factorial(j - 1) * 2 ** (j - 1)) * s ** (2 * (j - 1))
    tot = Fraction(0)
    for t in range(j):
        num = poch(Fraction(1) - j, t) * poch(1 - R, t)
        den = poch(Fraction(1) - n, t) * poch(Fraction(3, 2) - n, t) * s ** (2 * t)
        tot += (-1) ** t * Fraction(e[t]) * num / den
    return c0 * tot


def main() -> int:
    t0 = time.time()
    checks, mismatches = 0, []
    for j in range(2, 26):
        for n in range(j + 1, j + 26, 3):
            for lam in (Fraction(1, 100), Fraction(1, 2), Fraction(3), Fraction(26), Fraction(150)):
                Th = T_hat(lam)
                for f in (
                    Fraction(0),
                    Fraction(1, 2),
                    Fraction(1),
                    Fraction(3),
                ):  # incl. outside the shore
                    D = 4 + (Th - 4) * f
                    ref = eval_P(Bj_coeffs(j, n - 3), lam, D)
                    reff = Fraction(int(ref.p), int(ref.q))
                    got = P_closed(j, n, lam, D)
                    checks += 1
                    if got != reff:
                        mismatches.append({"j": j, "n": n, "lam": str(lam), "D": str(D)})
    out = {
        "identity": "P_j = c0 * sum_t (-1)^t E_2t (1-j)_t (1-R)_t / ((1-n)_t (3/2-n)_t s^{2t})",
        "definitions": {
            "s": "lam + n - 1",
            "c": "4n - 4j - 1",
            "R": "(D + c)/2 + j - 1",
            "c0": "(2n-2)!/((j-1)! 2^{j-1}) * s^{2(j-1)} > 0",
        },
        "exact_checks": checks,
        "mismatches": mismatches,
        "verified": not mismatches,
        "significance": (
            "terminating hypergeometric structure; all "
            "j-dependence sits in (1-j)_t and the positive "
            "prefactor c0 — the keystone's j-shift is now "
            "explicit"
        ),
        "prior_art": "analogue of Rigatos-Wang 2401.13031 eq.(27)-(28) "
        "for the Coon family; new for CHR with lam",
        "command": "python lab/chr_closed_form.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "chr_closed_form.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"exact checks: {checks}, mismatches: {len(mismatches)}", flush=True)
    print("CLOSED FORM " + ("VERIFIED" if not mismatches else "FAILED"), flush=True)
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
