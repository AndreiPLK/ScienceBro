"""KEYSTONE STEP 2 groundwork: an exact induction in the level n.

Step 1 (symbolic lam) is done for j >= 3. The remaining gap is that n and j
are unbounded, and n cannot simply be made symbolic: the kernel

        F_n(y) = SUM_t (-1)^t E_2t(n) y^t = [ prod_{a in S_n} (1 - a^2 y) ]^2,
        S_n = { n - 2k > 0 },

has a NUMBER OF FACTORS that grows with n, so it is not a polynomial in n.
This module establishes the replacement: an exact recursion in n with step
2, verified in rational arithmetic.

FACT 1 (kernel recursion).  S_{n+2} = S_n union {n}, therefore

        F_{n+2}(y) = F_n(y) * (1 - n^2 y)^2 .

Each step adds exactly ONE DOUBLE root, at y = 1/n^2, and it enters at the
OUTER edge of the root set (the smallest 1/a^2). Verified for n = 3..39.

FACT 2 (operator induction step).  With theta = y d/dy, the bracket is
H_n(y) = Q_n(theta) F_n(y) where Q_n(t) = prod_{i=j}^{n-1} (i - t), and
Q_{n+2}(t) = Q_n(t) (n - t)(n + 1 - t). Using the Weyl-algebra relation
p(theta) y^m f = y^m p(theta + m) f to commute the operator past the new
factor (1 - n^2 y)^2 = 1 - 2n^2 y + n^4 y^2:

  H_{n+2} = (n - theta)(n + 1 - theta) [ Q_n(theta) F_n
            - 2 n^2 y Q_n(theta+1) F_n + n^4 y^2 Q_n(theta+2) F_n ] .

Verified exactly for j = 3, 4, 6, 8 across many n.

WHY THIS IS NOT YET THE PROOF, stated plainly: the step is exact but not
sign-preserving on its face. The prefactor (n-t)(n+1-t) is positive over
the range that survives (t <= j-1 < n), but the bracket carries -2n^2 and
+n^4 with shifted operators, so positivity of H_n does not immediately give
positivity of H_{n+2}. What the step DOES give is a closed three-term
system in the shifted family Q_n(theta + sigma) F_n, sigma = 0, 1, 2, which
is the natural object for an induction and the next thing to attack.

Run: python lab/keystone_induction.py -> results/keystone_induction.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knife_proof2 import e_doubled_int  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def F(n):
    e = e_doubled_int(n)
    return trim([Fraction((-1) ** t * e[t]) for t in range(len(e))])


def pmul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for k, bk in enumerate(b):
            out[i + k] += ai * bk
    return trim(out)


def Qt(j, n, t):
    v = Fraction(1)
    for i in range(j, n):
        v *= i - t
    return v


def in_theta(coeffs, fn):
    return trim([c * fn(t) for t, c in enumerate(coeffs)])


def shift(coeffs, m):
    return [Fraction(0)] * m + list(coeffs)


def padd(*ps):
    L = max(len(p) for p in ps)
    out = [Fraction(0)] * L
    for p in ps:
        for i, c in enumerate(p):
            out[i] += c
    return trim(out)


def main() -> int:
    t0 = time.time()
    f1_checks, f1_bad = 0, []
    for n in range(3, 60):
        lhs = F(n + 2)
        rhs = pmul(pmul(F(n), [Fraction(1), Fraction(-n * n)]), [Fraction(1), Fraction(-n * n)])
        f1_checks += 1
        if lhs != rhs:
            f1_bad.append(n)

    f2_checks, f2_bad = 0, []
    for j in (3, 4, 5, 6, 8, 10):
        for n in range(max(4, j + 1), j + 24, 2):
            fn = F(n)
            t_0 = in_theta(fn, lambda t, j=j, n=n: Qt(j, n, t))
            t_1 = shift(in_theta(fn, lambda t, j=j, n=n: Qt(j, n, t + 1)), 1)
            t_2 = shift(in_theta(fn, lambda t, j=j, n=n: Qt(j, n, t + 2)), 2)
            inner = padd(t_0, [-2 * n * n * c for c in t_1], [n**4 * c for c in t_2])
            rhs = in_theta(inner, lambda t, n=n: (n - t) * (n + 1 - t))
            lhs = in_theta(F(n + 2), lambda t, j=j, n=n: Qt(j, n + 2, t))
            f2_checks += 1
            if lhs != rhs:
                f2_bad.append({"j": j, "n": n})

    out = {
        "purpose": "exact induction in the level n, needed because the"
        " kernel has a number of factors growing with n and so"
        " cannot be made symbolic in n",
        "fact_1": {
            "statement": "F_{n+2}(y) = F_n(y) * (1 - n^2 y)^2",
            "meaning": "each level adds exactly one DOUBLE root at"
            " y = 1/n^2, at the outer edge of the root"
            " set",
            "checks": f1_checks,
            "failures": f1_bad,
            "verified": not f1_bad,
        },
        "fact_2": {
            "statement": "H_{n+2} = (n-theta)(n+1-theta) ["
            " Q_n(theta)F_n - 2n^2 y Q_n(theta+1)F_n"
            " + n^4 y^2 Q_n(theta+2)F_n ]",
            "tool": "Weyl algebra: p(theta) y^m f = y^m p(theta+m) f",
            "checks": f2_checks,
            "failures": f2_bad,
            "verified": not f2_bad,
        },
        "honest_limitation": "the step is exact but NOT sign-preserving on"
        " its face: the prefactor (n-t)(n+1-t) is"
        " positive on the surviving range t <= j-1 <"
        " n, but the bracket carries -2n^2 and +n^4"
        " with shifted operators, so positivity does"
        " not propagate for free. It gives a closed"
        " three-term system in Q_n(theta+sigma)F_n,"
        " sigma = 0,1,2 -- the object to attack next",
        "command": "python lab/keystone_induction.py",
        **stamp(),
        "runtime_s": round(time.time() - t0, 1),
    }
    (RES / "keystone_induction.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"fact 1: {f1_checks} checks, {len(f1_bad)} failures", flush=True)
    print(f"fact 2: {f2_checks} checks, {len(f2_bad)} failures", flush=True)
    print("INDUCTION MACHINERY " + ("VERIFIED" if not (f1_bad or f2_bad) else "FAILED"), flush=True)
    return 0 if not (f1_bad or f2_bad) else 1


if __name__ == "__main__":
    sys.exit(main())
