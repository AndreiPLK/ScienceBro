"""THE DESCENT LEMMA: positivity at D+2 implies positivity at D.

This reduces the whole theorem from a stretch of length ~19 lam to a STRIP
OF WIDTH 2 just below the shore -- and it does so uniformly in the spin,
which is exactly what every earlier route failed to do.

Setup. Partial waves are the coefficients of the residue in the Gegenbauer
basis C_l^(a) with a = (D-3)/2; for a > 0 the physical D-dimensional
Gegenbauer is a positive multiple of C_l^(a), so the signs agree (this is the
convention already used in lab/attack_gravity.py and in paper 2). Writing
b_l^(a) for those coefficients, the classical connection formula with
mu = a + 1 has (a - mu)_k = (-1)_k, which VANISHES for k >= 2, leaving only
two terms:

    C_l^(a) = c0(l, a) C_l^(a+1) + c1(l, a) C_{l-2}^(a+1),
    c0(l, a) = (a)_l (l + mu) / ( (mu+1)_l  mu ),
    c1(l, a) = - (a)_{l-1} (l - 2 + mu) / ( (mu+1)_{l-1}  mu ) ,   l >= 2.

Expanding the same residue in both bases therefore gives the DIMENSION WALK

    b_m^(a+1) = c0(m, a) b_m^(a) + c1(m+2, a) b_{m+2}^(a) .           (*)

SIGNS. For a > 0 every Pochhammer above is positive, so c0 > 0 and c1 < 0.

THE LEMMA. Invert (*) downward in m:

    b_m^(a) = [ b_m^(a+1) + |c1(m+2, a)| b_{m+2}^(a) ] / c0(m, a) ,

a POSITIVE combination of b_m^(a+1) and b_{m+2}^(a). By induction from the
top spin downward: if every b^(a+1) >= 0 then every b^(a) >= 0. That is,

    all partial waves positive at D + 2  ==>  all positive at D,

uniformly in the spin, with no cell-by-cell certificate.

CONSEQUENCE. For any D in [4, T_hat] put k = floor((T_hat - D)/2); then
D + 2k lies in (T_hat - 2, T_hat], and k applications of the lemma carry
positivity from there down to D. So the grand theorem reduces to

    prove positivity for D in the strip (T_hat(lam) - 2, T_hat(lam)] .

This also explains the physics in one line: the class of positive definite
functions on the sphere shrinks as the dimension grows (Schoenberg 1942), and
(*) is the explicit shrinking map for our family. The shore is the critical
dimension of that nesting.

WHAT IS PROVED AND WHAT IS NOT. The lemma is proved: the connection formula
is classical, the sign statement is immediate for a > 0, and the induction is
one line. What is NOT proved is positivity inside the strip -- that is now the
whole remaining task, and it is a strip of width 2 instead of a region of
width ~19 lam.

This module verifies both directions exactly in rational arithmetic against
our own independent partial-wave solver.

Run: python lab/keystone_dimension_walk.py
Artifact: results/keystone_dimension_walk.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack_gravity import gegen_basis, partial_waves, residue_x_coeffs  # noqa
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def poch(a: F, k: int) -> F:
    p = F(1)
    for i in range(k):
        p *= (a + i)
    return p


def conn(l: int, a: F) -> tuple[F, F]:
    """c0, c1 of C_l^(a) = c0 C_l^(a+1) + c1 C_{l-2}^(a+1)."""
    mu = a + 1
    c0 = poch(a, l) * (l + mu) / (poch(mu + 1, l) * mu)
    c1 = (F(0) if l < 2 else
          -poch(a, l - 1) * (l - 2 + mu) / (poch(mu + 1, l - 1) * mu))
    return c0, c1


def main() -> int:
    t0 = time.time()
    fwd_ok = fwd_tot = inv_ok = inv_tot = 0
    sign_bad = []
    for n in (5, 6, 7, 8, 9, 10):
        for lam in (F(1, 2), F(1), F(3), F(26), F(150)):
            for D in (F(6), F(10), F(26), F(60)):
                a = (D - 3) / 2
                p = residue_x_coeffs(n, lam)[0]
                deg = len(p) - 1
                b_a = partial_waves(p, a, gegen_basis(deg, a))
                b_mu = partial_waves(p, a + 1, gegen_basis(deg, a + 1))

                # signs of the connection coefficients
                for l in range(2, deg + 1):
                    c0, c1 = conn(l, a)
                    if not (c0 > 0 and c1 < 0):
                        sign_bad.append({"l": l, "a": str(a)})

                # forward walk (*)
                fwd_tot += 1
                good = True
                for m in range(deg + 1):
                    c0m, _ = conn(m, a)
                    c1 = conn(m + 2, a)[1] if m + 2 <= deg else F(0)
                    tail = b_a[m + 2] if m + 2 <= deg else F(0)
                    if c0m * b_a[m] + c1 * tail != b_mu[m]:
                        good = False
                        break
                fwd_ok += 1 if good else 0

                # inverse walk (the lemma's construction)
                inv_tot += 1
                rec = [F(0)] * (deg + 1)
                for m in range(deg, -1, -1):
                    c0m, _ = conn(m, a)
                    c1 = conn(m + 2, a)[1] if m + 2 <= deg else F(0)
                    tail = rec[m + 2] if m + 2 <= deg else F(0)
                    rec[m] = (b_mu[m] - c1 * tail) / c0m
                inv_ok += 1 if rec == b_a else 0

    out = {"lemma": "all partial waves positive at D+2 implies all positive"
                    " at D, uniformly in the spin",
           "mechanism": "Gegenbauer connection with mu = a+1 truncates after"
                        " two terms because (a-mu)_k = (-1)_k vanishes for"
                        " k >= 2; c0 > 0 and c1 < 0 for a > 0, so the inverted"
                        " relation is a POSITIVE combination and induction"
                        " runs downward in the spin",
           "consequence": "for any D in [4, T_hat], k = floor((T_hat-D)/2)"
                          " applications carry positivity down from the strip"
                          " (T_hat-2, T_hat]; the grand theorem reduces to"
                          " that strip of WIDTH 2",
           "context": "this is the explicit shrinking map behind Schoenberg's"
                      " nesting of positive-definite classes on spheres; the"
                      " shore is the critical dimension of the nesting",
           "forward_relation_exact": f"{fwd_ok}/{fwd_tot}",
           "inverse_reconstruction_exact": f"{inv_ok}/{inv_tot}",
           "sign_violations": sign_bad,
           "all_verified": (fwd_ok == fwd_tot and inv_ok == inv_tot
                            and not sign_bad),
           "still_open": "positivity INSIDE the strip (T_hat-2, T_hat], for"
                         " all spins; that is now the entire remaining task",
           "command": "python lab/keystone_dimension_walk.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_dimension_walk.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(f"forward relation exact: {fwd_ok}/{fwd_tot}", flush=True)
    print(f"inverse reconstruction exact: {inv_ok}/{inv_tot}", flush=True)
    print(f"sign violations: {len(sign_bad)}", flush=True)
    print("DESCENT LEMMA " + ("VERIFIED" if out["all_verified"]
                              else "FAILED"), flush=True)
    return 0 if out["all_verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
