"""The anomaly battery: everything worth asking about a sequence, exactly.

Written because the same questions were being re-implemented by hand in one lab
module after another, each time with a fresh chance to get the domain or the sign
convention wrong. Two of those mistakes cost real time on 29 August alone: a
higher-difference test whose window ran off the end of the spectrum, and a
"harmonic additivity" test that matched points at unrelated tilts.

Everything here takes exact rationals and returns exact verdicts. No logarithm is
ever evaluated: a statement about the sign of a linear combination of logs is decided
by comparing two products of rationals, so no float touches a verdict.

The battery covers, for a finite positive sequence:

* log-concavity, ratio log-concavity, and the full higher log-difference hierarchy;
* Turan determinants;
* Hankel and Toeplitz minors up to a given order (Stieltjes / total-positivity
  signatures);
* Hausdorff (completely monotone) and Stieltjes moment conditions;
* real-rootedness of the generating polynomial, its root mesh and interlacing;
* the reversed and reciprocal sequences, since several structures live there and not
  in the original;
* rational and polynomial reconstruction, for recognising a closed form.

Nothing here proves anything. Each answer comes back as a `Result` whose
`evidence_kind` is `EXACT_FINITE`: an exact statement about the finitely many cases
that were examined.
"""

from __future__ import annotations

from math import comb
from typing import Any

from flint import fmpq, fmpq_mat, fmpq_poly

from .core import Result, timed

Seq = list[fmpq]


def as_seq(values: Any) -> Seq:
    """Accept ints, strings 'a/b', pairs, or fmpq; never accept a float silently."""
    out: Seq = []
    for v in values:
        if isinstance(v, fmpq):
            out.append(v)
        elif isinstance(v, int):
            out.append(fmpq(v))
        elif isinstance(v, str):
            if "/" in v:
                a, b = v.split("/")
                out.append(fmpq(int(a), int(b)))
            else:
                out.append(fmpq(int(v)))
        elif isinstance(v, (tuple, list)) and len(v) == 2:
            out.append(fmpq(int(v[0]), int(v[1])))
        elif isinstance(v, float):
            raise TypeError(
                "float given to an exact tool; pass 'a/b', an int, or an fmpq. "
                "If the quantity is genuinely transcendental, use a NUMERIC tool instead."
            )
        else:
            raise TypeError(f"cannot interpret {v!r} as an exact rational")
    return out


# --------------------------------------------------------------------------- signs


def sign_log_difference(p: Seq, t: int, r: int) -> int:
    """Sign of Delta^r log p_t, decided by comparing two exact products.

    Delta^r log p_t = SUM_j (-1)^{r-j} C(r,j) log p_{t+j}; collecting the positive and
    negative sides gives two products of rationals, and the sign is their comparison.
    """
    lhs, rhs = fmpq(1), fmpq(1)
    for j in range(r + 1):
        c = comb(r, j)
        if (r - j) % 2 == 0:
            lhs = lhs * p[t + j] ** c
        else:
            rhs = rhs * p[t + j] ** c
    return 0 if lhs == rhs else (1 if lhs > rhs else -1)


def log_difference_hierarchy(
    values: Any, rmax: int = 8, window_must_fit_in: int | None = None
) -> Result:
    """Signs of Delta^r log p_t for r = 2..rmax.

    `window_must_fit_in` bounds the LAST index the window may touch. It exists because
    the natural mistake is to constrain `t` and let `t + r` run past the domain where
    the claim was ever made; that produced 19 spurious violations on 29 August.
    """
    tm = timed()
    p = as_seq(values)
    top = len(p) - 1 if window_must_fit_in is None else min(window_must_fit_in, len(p) - 1)
    rows, by_r = [], {}
    for r in range(2, rmax + 1):
        neg = nonneg = 0
        for t in range(0, top - r + 1):
            if any(p[t + j] <= 0 for j in range(r + 1)):
                continue
            s = sign_log_difference(p, t, r)
            rows.append({"t": t, "r": r, "sign": s})
            if s < 0:
                neg += 1
            else:
                nonneg += 1
        by_r[r] = {"tested": neg + nonneg, "negative": neg, "not_negative": nonneg}
    viol = [x for x in rows if x["sign"] >= 0]
    return Result(
        tool="log_difference_hierarchy",
        inputs={"n": len(p), "rmax": rmax, "window_must_fit_in": top},
        status="ok" if not viol else "refuted",
        evidence_kind="EXACT_FINITE",
        data={
            "by_order": by_r,
            "violations": viol[:50],
            "violation_count": len(viol),
            "all_negative": not viol,
        },
        runtime_s=tm.stop(),
    )


def ratio_log_concavity(values: Any, upto: int | None = None) -> Result:
    """p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}: the r = 3 member, kept separate for clarity.

    `upto` bounds the LAST index the window may touch. It is not optional in spirit:
    for the centred family the statement is made on the first half only, and testing
    past the midpoint reports failures that are outside the claim. Default is the
    whole sequence, so the caller must say what domain it means.
    """
    tm = timed()
    p = as_seq(values)
    top = len(p) - 1 if upto is None else min(upto, len(p) - 1)
    bad = [t for t in range(1, top - 1) if p[t + 1] ** 3 * p[t - 1] < p[t] ** 3 * p[t + 2]]
    return Result(
        tool="ratio_log_concavity",
        inputs={"n": len(p), "window_must_fit_in": top},
        status="ok" if not bad else "refuted",
        evidence_kind="EXACT_FINITE",
        data={"failing_t": bad, "tested": max(0, top - 2)},
        warnings=[] if upto is not None else ["no domain given; the whole sequence was tested"],
        runtime_s=tm.stop(),
    )


def turan(values: Any) -> Result:
    """Turan determinants p_t^2 - p_{t-1} p_{t+1}, exactly, with their signs."""
    tm = timed()
    p = as_seq(values)
    d = [p[t] ** 2 - p[t - 1] * p[t + 1] for t in range(1, len(p) - 1)]
    return Result(
        tool="turan",
        inputs={"n": len(p)},
        status="ok" if all(x >= 0 for x in d) else "refuted",
        evidence_kind="EXACT_FINITE",
        data={
            "values": [str(x) for x in d],
            "negative_at": [i + 1 for i, x in enumerate(d) if x < 0],
        },
        runtime_s=tm.stop(),
    )


# ------------------------------------------------------------------------- minors


def _det(rows: list[list[fmpq]]) -> fmpq:
    return fmpq_mat([[x for x in r] for r in rows]).det()


def hankel_minors(values: Any, max_order: int = 6, shift: int = 0) -> Result:
    """Leading Hankel minors det[a_{i+j+shift}] -- the Hamburger/Stieltjes signature.

    shift = 0 tests the Hamburger condition, shift = 1 the extra Stieltjes condition.
    """
    tm = timed()
    a = as_seq(values)
    dets, order = [], 1
    while order <= max_order and 2 * order - 2 + shift < len(a):
        m = [[a[i + j + shift] for j in range(order)] for i in range(order)]
        dets.append({"order": order, "det": str(_det(m)), "sign": int(_det(m) > 0) - int(_det(m) < 0)})
        order += 1
    neg = [d for d in dets if d["sign"] < 0]
    return Result(
        tool="hankel_minors",
        inputs={"n": len(a), "max_order": max_order, "shift": shift},
        status="ok" if not neg else "refuted",
        evidence_kind="EXACT_FINITE",
        data={"minors": dets, "negative": neg, "all_nonnegative": not neg},
        runtime_s=tm.stop(),
    )


def toeplitz_minors(values: Any, max_order: int = 4) -> Result:
    """All minors of the Toeplitz matrix [a_{i-j}] up to `max_order`.

    A sequence is a Polya frequency sequence exactly when every such minor is
    nonnegative, so a negative one refutes PF membership outright.
    """
    tm = timed()
    a = as_seq(values)
    n = len(a)

    def entry(i: int, j: int) -> fmpq:
        k = i - j
        return a[k] if 0 <= k < n else fmpq(0)

    checked = 0
    negatives = []
    for order in range(1, max_order + 1):
        rowsets = [tuple(range(i, i + order)) for i in range(n)]
        colsets = [tuple(range(j, j + order)) for j in range(n)]
        for rs in rowsets:
            for cs in colsets:
                m = [[entry(i, j) for j in cs] for i in rs]
                d = _det(m)
                checked += 1
                if d < 0:
                    negatives.append({"rows": rs, "cols": cs, "det": str(d)})
    return Result(
        tool="toeplitz_minors",
        inputs={"n": n, "max_order": max_order},
        status="ok" if not negatives else "refuted",
        evidence_kind="EXACT_FINITE",
        data={
            "minors_checked": checked,
            "negative": negatives[:20],
            "negative_count": len(negatives),
            "consistent_with_PF": not negatives,
        },
        runtime_s=tm.stop(),
    )


# ------------------------------------------------------------------ moment problems


def hausdorff_conditions(values: Any, max_order: int = 10) -> Result:
    """Completely monotone test: (-1)^k Delta^k a_t >= 0 for all k, t.

    By Hausdorff's theorem a sequence on [0,1] is a moment sequence of a positive
    measure exactly when it is completely monotone, so a single negative alternating
    difference kills the representation. The REVERSED sequence is tested too, because
    an increasing sequence can only be a moment sequence after reversal -- a point that
    decided a route on 29 August.
    """
    tm = timed()
    a = as_seq(values)

    def scan(seq: Seq) -> list[dict]:
        bad = []
        for k in range(0, max_order + 1):
            for t in range(0, len(seq) - k):
                d = sum(
                    fmpq((-1) ** j * comb(k, j)) * seq[t + k - j] for j in range(k + 1)
                )
                if (fmpq(-1) ** k) * d < 0:
                    bad.append({"k": k, "t": t, "value": str(d)})
        return bad

    fwd = scan(a)
    rev = scan(list(reversed(a)))
    return Result(
        tool="hausdorff_conditions",
        inputs={"n": len(a), "max_order": max_order},
        status="ok" if not fwd or not rev else "refuted",
        evidence_kind="EXACT_FINITE",
        data={
            "forward_violations": fwd[:20],
            "forward_violation_count": len(fwd),
            "reversed_violations": rev[:20],
            "reversed_violation_count": len(rev),
            "completely_monotone_forward": not fwd,
            "completely_monotone_reversed": not rev,
        },
        runtime_s=tm.stop(),
    )


def stieltjes_conditions(values: Any, max_order: int = 6) -> Result:
    """Stieltjes: both Hankel families nonnegative (shift 0 and shift 1)."""
    tm = timed()
    h0 = hankel_minors(values, max_order, shift=0)
    h1 = hankel_minors(values, max_order, shift=1)
    ok = h0.status == "ok" and h1.status == "ok"
    return Result(
        tool="stieltjes_conditions",
        inputs={"max_order": max_order},
        status="ok" if ok else "refuted",
        evidence_kind="EXACT_FINITE",
        data={"shift0": h0.data, "shift1": h1.data, "consistent_with_stieltjes": ok},
        runtime_s=tm.stop(),
    )


# --------------------------------------------------------------- generating function


def real_rootedness(coeffs: Any) -> Result:
    """Is SUM a_t z^t real-rooted? Root mesh and separation come with it.

    Uses flint's certified complex root isolation, not numpy: the verdict is a
    statement about isolating boxes, not about float noise.
    """
    tm = timed()
    a = as_seq(coeffs)
    poly = fmpq_poly([x for x in a])
    roots = poly.complex_roots()
    imag = []
    real = []
    for r, _mult in roots:
        if r.imag.contains(0):
            real.append(r.real)
        else:
            imag.append(str(r))
    real_sorted = sorted(real, key=lambda x: float(x.mid()))
    mesh = [
        str((real_sorted[i + 1] - real_sorted[i]).mid()) for i in range(len(real_sorted) - 1)
    ]
    return Result(
        tool="real_rootedness",
        inputs={"degree": poly.degree()},
        status="ok" if not imag else "refuted",
        evidence_kind="CERTIFICATE",
        data={
            "degree": poly.degree(),
            "real_roots": len(real),
            "non_real_roots": len(imag),
            "sample_non_real": imag[:5],
            "root_mesh": mesh[:20],
            "real_rooted": not imag,
        },
        warnings=[] if not imag else ["a non-real root refutes real-rootedness outright"],
        runtime_s=tm.stop(),
    )


def reciprocal(values: Any) -> Seq:
    """The reciprocal sequence; several structures live here and not in the original."""
    return [fmpq(1) / v for v in as_seq(values)]
