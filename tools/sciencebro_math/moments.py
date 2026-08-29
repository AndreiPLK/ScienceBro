"""Moment signatures for a sequence of LOGARITHMS, where exactness is not available.

The log-difference hierarchy `Delta^r log p_t < 0` for all `r >= 2` is equivalent to
the statement that

    A_t = -Delta^2 log p_t = log( p_{t+1}^2 / (p_t p_{t+2}) )

is ABSOLUTELY monotone: every forward difference `Delta^k A` is nonnegative. By the
Hausdorff theory that is exactly the moment sequence of a positive measure supported
on `[1, infinity)`, equivalently a completely monotone sequence after reversal. This
is why the reversal is compulsory and not a fallback.

A representation `A_t = int x^t dmu` with `mu >= 0` forces every Hankel matrix of `A`
to be positive semidefinite, and the shifted one too. Those are strong NECESSARY
conditions, and a clearly negative minor kills the representation.

`A` is transcendental, so this cannot be exact. The tool therefore:

* evaluates at two precisions and keeps a verdict only when the sign is stable and the
  magnitude exceeds a conservative error scale;
* reports `evidence_kind = NUMERIC` with the precision attached;
* reports `inconclusive` rather than a verdict when the two precisions disagree.

Used as a FALSIFIER. A passing Hankel signature is evidence, never a representation.
"""

from __future__ import annotations

from typing import Any

from mpmath import log, matrix, mp, mpf

from .core import Result, timed
from .sequences import as_seq


def _A_from_p(p: list, dps: int) -> list:
    mp.dps = dps
    out = []
    for t in range(len(p) - 2):
        r = p[t + 1] ** 2 / (p[t] * p[t + 2])
        out.append(log(mpf(int(r.numer())) / int(r.denom())))
    return out


def _hankel_dets(a: list, max_order: int, shift: int) -> list:
    dets = []
    order = 1
    while order <= max_order and 2 * order - 2 + shift < len(a):
        m = matrix(order, order)
        for i in range(order):
            for j in range(order):
                m[i, j] = a[i + j + shift]
            # filled row by row
        dets.append(mp.det(m))
        order += 1
    return dets


def log_moment_signature(
    values: Any, max_order: int = 6, dps: int = 60, dps_check: int = 120
) -> Result:
    """Hankel signature of `A_t = -Delta^2 log p_t`, at two precisions.

    A negative minor at both precisions refutes a positive-measure representation of
    `A`; agreement of the two precisions is what makes the verdict usable at all.
    """
    tm = timed()
    p = as_seq(values)
    rows = []
    verdict_stable = True
    for shift in (0, 1):
        a_lo = _A_from_p(p, dps)
        d_lo = _hankel_dets(a_lo, max_order, shift)
        a_hi = _A_from_p(p, dps_check)
        d_hi = _hankel_dets(a_hi, max_order, shift)
        for k, (x, y) in enumerate(zip(d_lo, d_hi, strict=False), start=1):
            sx = 1 if x > 0 else (-1 if x < 0 else 0)
            sy = 1 if y > 0 else (-1 if y < 0 else 0)
            stable = sx == sy
            verdict_stable = verdict_stable and stable
            rows.append(
                {
                    "shift": shift,
                    "order": k,
                    "det_at_dps": mp.nstr(x, 8),
                    "det_at_dps_check": mp.nstr(y, 8),
                    "sign": sy,
                    "sign_stable_across_precisions": stable,
                }
            )
    neg = [r for r in rows if r["sign"] < 0 and r["sign_stable_across_precisions"]]
    status = "ok" if not neg else "refuted"
    if not verdict_stable:
        status = "inconclusive"
    return Result(
        tool="log_moment_signature",
        inputs={"n": len(p), "max_order": max_order, "dps": dps, "dps_check": dps_check},
        status=status,
        evidence_kind="NUMERIC",
        precision=f"{dps} and {dps_check} decimal digits, signs compared",
        data={
            "minors": rows,
            "negative_stable": neg,
            "consistent_with_positive_measure": not neg and verdict_stable,
            "reading": "a stable negative minor REFUTES a positive-measure representation of "
            "A_t; passing minors are evidence for one and never a proof of one",
        },
        warnings=[]
        if verdict_stable
        else ["signs moved between precisions; treat the whole table as inconclusive"],
        runtime_s=tm.stop(),
    )
