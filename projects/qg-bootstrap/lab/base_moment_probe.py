"""The r-independent base sequence m_t: is IT a Hausdorff moment sequence?

The outside report tested M_t^(r) = t! (H-r)_t E_{2t}(n) / [s^{2t}(n-1)_t(n-3/2)_t]
for a positive measure and it failed. But M carries an r-DEPENDENT weight:

    M_t^(r) = (H-r)_t * m_t,      m_t := t! E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ],

and m_t depends on NEITHER r NOR D -- only on the level n and s = lam+n-1.
A Hausdorff hypothesis for a sequence that changes with r was ill-posed;
for m_t it is a clean statement about central factorial numbers.

WHY IT MATTERS. If m_t = INT_0^1 y^t dmu(y) with dmu >= 0, then

    K_r = sum_t (-1)^t C(r,t) M_t^(r) = INT sum_t C(r,t) (H-r)_t (-y)^t dmu(y)
        = INT 2F0(-r, -(H-r); ; -y) dmu(y)
        = INT C_r(H-r ; 1/y) dmu(y),

a CHARLIER polynomial in the variable g = H-r, integrated against a positive
measure. Charlier polynomials have r real positive zeros, so positivity of
K_r would reduce to "g exceeds the largest zero of C_r(.;1/y) on supp mu" --
a one-variable question with classical zero bounds, uniform in r by
construction. That is the shape an all-depths theorem needs.

This probe tests the premise exactly: Hankel and [0,1]-localizer minors of
the m-sequence over the physical (n, lam) domain, including the small-lam
region where the M-version died.

Run: python lab/base_moment_probe.py -> results/base_moment_probe.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_kernel_probe import E2_list, falling, leading_minors  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def m_seq(n: int, lam: fmpq, tmax: int) -> list[fmpq]:
    """m_t, t = 0..tmax -- independent of r and D."""
    s = lam + n - 1
    E = E2_list(n, tmax)
    out = []
    fact = fmpq(1)
    for t in range(tmax + 1):
        if t:
            fact *= t
        num = fact * E[t]
        den = (s ** (2 * t)) * falling(fmpq(n - 1), t) * falling(fmpq(2 * n - 3, 2), t)
        out.append(num / den)
    return out


def moment_report(m: list[fmpq]) -> dict:
    """Hankel [m_{a+b}], shifted [m_{a+b+1}] and [0,1]-localizer minors."""
    r = len(m) - 1
    q0 = r // 2
    q1 = (r - 1) // 2
    H0 = [[m[a + b] for b in range(q0 + 1)] for a in range(q0 + 1)]
    rep = {"H0": [str(x) for x in leading_minors(H0)]}
    neg = [x for x in leading_minors(H0) if x < 0]
    if q1 >= 0:
        H1 = [[m[a + b + 1] for b in range(q1 + 1)] for a in range(q1 + 1)]
        L01 = [[m[a + b] - m[a + b + 1] for b in range(q1 + 1)] for a in range(q1 + 1)]
        rep["H1"] = [str(x) for x in leading_minors(H1)]
        rep["L01"] = [str(x) for x in leading_minors(L01)]
        neg += [x for x in leading_minors(H1) if x < 0]
        neg += [x for x in leading_minors(L01) if x < 0]
    rep["all_nonneg"] = not neg
    return rep


def main() -> int:
    t0 = time.time()
    rows = []
    tmax = 10
    for lam in (fmpq(1, 10), fmpq(1), fmpq(5, 2), fmpq(3), fmpq(7), fmpq(72), fmpq(650, 3), fmpq(5000)):
        for n in (8, 12, 24, 40, 101):
            if n - 1 < tmax + 1:
                continue
            m = m_seq(n, lam, tmax)
            rep = moment_report(m)
            # also record whether m is decreasing in [0,1] fashion
            rows.append(
                {
                    "lam": str(lam),
                    "n": n,
                    "m0": str(m[0]),
                    "m1_over_m0": float(m[1] / m[0]) if m[0] != 0 else None,
                    "in_unit_range": all(0 <= x <= 1 for x in m),
                    **rep,
                }
            )
    ok = sum(1 for r_ in rows if r_["all_nonneg"])
    unit = sum(1 for r_ in rows if r_["in_unit_range"])
    print(
        f"base sequence m_t: {len(rows)} (n, lam) points; "
        f"all moment minors nonneg in {ok}; m_t in [0,1] in {unit}",
        flush=True,
    )
    for r_ in rows:
        if not r_["all_nonneg"]:
            print(f"  FAIL lam={r_['lam']} n={r_['n']}", flush=True)

    out = {
        "claim": (
            "TEST of the corrected moment hypothesis: is the r-INDEPENDENT base "
            "sequence m_t = t! E_2t(n) / [s^2t (n-1)_t (n-3/2)_t] a Hausdorff moment "
            "sequence on [0,1]? (The outside report tested M_t^(r) = (H-r)_t m_t, "
            "which carries an r-dependent weight and cannot be a fixed moment "
            "sequence.) If m is Hausdorff, then K_r = INT C_r(H-r; 1/y) dmu(y) with "
            "C_r the Charlier polynomial, reducing all-depths positivity to a zero "
            "bound uniform in r."
        ),
        "points": len(rows),
        "all_minors_nonneg": ok,
        "m_in_unit_range": unit,
        "rows": rows,
        "command": "python lab/base_moment_probe.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "base_moment_probe.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
