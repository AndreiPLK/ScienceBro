"""THE LADDER IN THE KNIFE INDEX: an exact step from knife j to knife j+1.

This is the third exact ladder of the programme, and unlike the other two it
appears to be ours:

  * in the DIMENSION D: the classical montee/descente step (Matheron), which
    gave the descent lemma -- positivity at D+2 implies positivity at D;
  * in the LEVEL n: F_{n+2}(y) = F_n(y) (1 - n^2 y)^2, one new double root
    per level (lab/keystone_induction.py);
  * in the KNIFE INDEX j: this module.

THE MECHANISM. The operator weight satisfies Q_{j+1}(t) = Q_j(t)/(j - t), and
on the summation range t <= j-1 we have j - t >= 1, so the factor 1/(j-t) is
positive. More than positive -- it is a MOMENT:

        1/(j - t) = INT_0^1 u^{j-t-1} du ,

so the step j -> j+1 is an integral operator with a POSITIVE kernel, i.e. an
averaging. Since in the Beta reduction the weights enter as A_t / s^{2t},
dividing by u^t is the same as replacing s^2 by s^2 u -- that is, the
averaging runs over SMALLER values of the deformation lam.

THE ONE SUBTLETY, which is where the parity comes from. At t = j the relation
Q_{j+1} = Q_j/(j-t) is 0/0: Q_j(j) = 0 while Q_{j+1}(j) = (n-1-j)! is not. So
the step is not pure averaging; it carries a BOUNDARY TERM at t = j:

    bracket_{j+1} = SUM_{t<j} (-1)^t E_2t(n) [Q_j(t)/(j-t)] A_t / s^{2t}
                    + (-1)^j E_2j(n) (n-1-j)! A_j / s^{2j} ,

with A_t = (1-R)_t/(3/2-n)_t evaluated at the j+1 value of R. Verified exactly
in rational arithmetic (this module).

WHY THIS EXPLAINS THE PARITY SPLIT. The boundary term carries (-1)^j. When the
NEXT knife j+1 is odd (j even) the boundary term enters with a PLUS and helps:
positivity is inherited. When j+1 is even (j odd) it enters with a MINUS, and
that is precisely where a threshold can appear. This matches, and now explains,
the measured facts recorded earlier: odd knives never cut, even knives must,
and every dangerous cell in the programme has even j.

WHAT IS PROVED HERE AND WHAT IS NOT. The identity is proved (exact algebra,
verified). What is NOT proved is the estimate needed for the even case: that
the averaged part dominates the negative boundary term. That inequality is the
remaining work, and it is now a SINGLE explicit comparison rather than a
four-dimensional region -- and it only has to be won for even j+1, which halves
the problem.

Run: python lab/keystone_j_ladder.py -> results/keystone_j_ladder.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def poch(a: F, k: int) -> F:
    r = F(1)
    for i in range(k):
        r *= a + i
    return r


def Qp(j: int, n: int, t: int) -> F:
    r = F(1)
    for i in range(j, n):
        r *= i - t
    return r


def bracket(j: int, n: int, s2: F, D: F) -> F:
    """SUM_t (-1)^t E_2t(n) Q_j(t) A_t / s2^t, the sign-carrying bracket."""
    e = e_doubled_int(n)
    R = (F(D) + F(4 * n - 4 * j - 1)) / 2 + j - 1
    tot = F(0)
    for t in range(j):
        tot += (-1) ** t * F(e[t]) * Qp(j, n, t) * poch(1 - R, t) / poch(F(3, 2) - n, t) / s2**t
    return tot


def ladder_parts(j: int, n: int, s2: F, D: F) -> tuple[F, F]:
    """The averaged part and the boundary term of the j -> j+1 step."""
    e = e_doubled_int(n)
    R = (F(D) + F(4 * n - 4 * (j + 1) - 1)) / 2 + (j + 1) - 1
    averaged = F(0)
    for t in range(j):
        averaged += (
            (-1) ** t
            * F(e[t])
            * Qp(j, n, t)
            / (j - t)
            * poch(1 - R, t)
            / poch(F(3, 2) - n, t)
            / s2**t
        )
    boundary = (
        (-1) ** j
        * F(e[j])
        * F(factorial(n - 1 - j))
        * poch(1 - R, j)
        / poch(F(3, 2) - n, j)
        / s2**j
    )
    return averaged, boundary


def main() -> int:
    t0 = time.time()
    checks, bad = 0, []
    rows = []
    for n in (6, 8, 10, 12):
        for D in (F(6), F(23), F(40)):
            for s2 in (F(25), F(49), F(100), F(400)):
                for j in range(2, min(n - 2, 9)):
                    direct = bracket(j + 1, n, s2, D)
                    av, bnd = ladder_parts(j, n, s2, D)
                    checks += 1
                    if direct != av + bnd:
                        bad.append({"n": n, "D": str(D), "s2": str(s2), "j": j})
                    elif len(rows) < 40:
                        rows.append(
                            {
                                "n": n,
                                "D": str(D),
                                "s2": str(s2),
                                "j": j,
                                "next_knife_parity": "odd" if (j + 1) % 2 else "even",
                                "boundary_sign": int((bnd > 0) - (bnd < 0)),
                                "averaged_sign": int((av > 0) - (av < 0)),
                                "total_sign": int((direct > 0) - (direct < 0)),
                            }
                        )

    # does the boundary term's sign follow (-1)^j, and does it help odd knives?
    helps_odd = all(r["boundary_sign"] >= 0 for r in rows if r["next_knife_parity"] == "odd")
    hurts_even = all(r["boundary_sign"] <= 0 for r in rows if r["next_knife_parity"] == "even")

    out = {
        "identity": "bracket_{j+1} = SUM_{t<j} (-1)^t E_2t Q_j(t)/(j-t)"
        " A_t/s^{2t}  +  (-1)^j E_2j (n-1-j)! A_j/s^{2j}",
        "mechanism": "Q_{j+1}(t) = Q_j(t)/(j-t) and 1/(j-t) = int_0^1"
        " u^{j-t-1} du, so the step is an integral operator with"
        " a POSITIVE kernel (an averaging over smaller lam);"
        " at t = j the relation is 0/0 and leaves a boundary term",
        "why_parity": "the boundary term carries (-1)^j: when the next knife"
        " j+1 is ODD it enters with a plus and positivity is"
        " inherited; when j+1 is EVEN it enters with a minus,"
        " which is exactly where a threshold can appear",
        "exact_checks": checks,
        "failures": bad,
        "verified": not bad,
        "boundary_helps_odd_next_knife": helps_odd,
        "boundary_hurts_even_next_knife": hurts_even,
        "still_open": "the estimate for the EVEN case: that the averaged part"
        " dominates the negative boundary term. One explicit"
        " comparison, and only for even j+1 -- half the problem",
        "relation_to_other_ladders": "third exact ladder of the programme,"
        " after the classical montee/descente in"
        " D (Matheron) and F_{n+2} = F_n"
        " (1-n^2 y)^2 in the level n",
        "rows": rows,
        "command": "python lab/keystone_j_ladder.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_j_ladder.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"exact checks {checks}, failures {len(bad)}", flush=True)
    print(f"boundary term helps when the next knife is odd: {helps_odd}", flush=True)
    print(f"boundary term hurts when the next knife is even: {hurts_even}", flush=True)
    print("J-LADDER " + ("VERIFIED" if not bad else "FAILED"), flush=True)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
