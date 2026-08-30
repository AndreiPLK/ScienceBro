"""Fitting P-recurrences exactly, and — the part that matters — testing them on held-out terms.

A P-recursive (holonomic) sequence satisfies

    SUM_{i=0}^{L} c_i(m) a_{m+i} = 0

for polynomials `c_i` of some degree `D`. Finding one is linear algebra over `Q`: the
unknowns are the `(L+1)(D+1)` coefficients, each term of the sequence gives one equation,
and a nonzero nullspace vector is a candidate recurrence.

The trap this module exists to avoid: with enough unknowns a nullspace vector ALWAYS
exists, and it means nothing. A fit is only evidence if it **predicts terms it never saw**.
So `fit` splits the data, solves on the first part, and verifies on the rest, reporting how
many held-out terms the recurrence reproduces. A recurrence that fits everything and
predicts nothing is reported as a failure, not a success.

Everything is exact: `fmpq` throughout, nullspace by exact row reduction.
"""

from __future__ import annotations

from typing import Any

from math import gcd

from flint import fmpq, fmpz_mat

from .core import Result, timed


def _nullspace(rows: list[list[fmpq]]) -> list[list[fmpq]]:
    """Exact nullspace of a rational matrix.

    python-flint exposes `nullspace` on the INTEGER matrix type only, so each row is
    cleared of denominators first -- which changes no solution, since scaling a row scales
    its equation.
    """
    if not rows:
        return []
    cleared = []
    for r in rows:
        den = 1
        for x in r:
            den = den * int(x.denom()) // gcd(den, int(x.denom()))
        cleared.append([int(x * den) for x in r])
    M = fmpz_mat(cleared)
    ns, nullity = M.nullspace()
    return [[fmpq(int(ns[i, j])) for i in range(ns.nrows())] for j in range(nullity)]


def fit_p_recurrence(
    terms: list[fmpq], order: int, degree: int, holdout: int | None = None
) -> Result:
    """Fit SUM_i c_i(m) a_{m+i} = 0 on part of the data, then test on the rest.

    `terms[k]` is `a_k`. The fit uses the first `len(terms) - holdout` usable equations and
    the verification uses the remainder; `holdout` defaults to a third of the equations.
    """
    tm = timed()
    n_unknowns = (order + 1) * (degree + 1)
    eqs = []
    for m in range(len(terms) - order):
        row = []
        for i in range(order + 1):
            for d in range(degree + 1):
                row.append(fmpq(m) ** d * terms[m + i])
        eqs.append(row)
    if len(eqs) < n_unknowns + 2:
        return Result(
            tool="fit_p_recurrence",
            inputs={"order": order, "degree": degree, "terms": len(terms)},
            status="inconclusive",
            evidence_kind="EXACT_FINITE",
            data={
                "reason": "not enough terms to both fit and test",
                "equations": len(eqs),
                "unknowns": n_unknowns,
                "needed": n_unknowns + 2,
            },
            runtime_s=tm.stop(),
        )

    hold = holdout if holdout is not None else max(2, len(eqs) // 3)
    fit_rows, test_rows = eqs[: len(eqs) - hold], eqs[len(eqs) - hold :]
    ns = _nullspace(fit_rows)
    if not ns:
        return Result(
            tool="fit_p_recurrence",
            inputs={"order": order, "degree": degree, "terms": len(terms)},
            status="refuted",
            evidence_kind="EXACT_FINITE",
            data={
                "reason": "no recurrence of this order and degree fits even the training part",
                "fit_equations": len(fit_rows),
                "unknowns": n_unknowns,
            },
            runtime_s=tm.stop(),
        )

    verified = []
    for v in ns:
        ok = all(sum(a * b for a, b in zip(row, v, strict=True)) == 0 for row in test_rows)
        verified.append(ok)
    good = sum(verified)
    return Result(
        tool="fit_p_recurrence",
        inputs={"order": order, "degree": degree, "terms": len(terms)},
        status="ok" if good else "refuted",
        evidence_kind="EXACT_FINITE",
        data={
            "nullspace_dimension": len(ns),
            "fit_equations": len(fit_rows),
            "held_out_equations": len(test_rows),
            "candidates_surviving_holdout": good,
            "predicts_unseen_terms": bool(good),
            "note": "a nullspace vector that fails the held-out equations is an artefact of "
            "having more unknowns than data, not a recurrence",
        },
        runtime_s=tm.stop(),
    )


def search_p_recurrence(
    terms: list[fmpq], max_order: int = 4, max_degree: int = 8
) -> Result:
    """Smallest (order, degree) whose recurrence survives the held-out test."""
    tm = timed()
    tried: list[dict[str, Any]] = []
    for total in range(2, max_order + max_degree + 1):
        for order in range(1, min(max_order, total) + 1):
            degree = total - order
            if degree > max_degree or degree < 0:
                continue
            r = fit_p_recurrence(terms, order, degree)
            tried.append(
                {
                    "order": order,
                    "degree": degree,
                    "status": r.status,
                    "survivors": r.data.get("candidates_surviving_holdout"),
                }
            )
            if r.status == "ok":
                return Result(
                    tool="search_p_recurrence",
                    inputs={"terms": len(terms), "max_order": max_order,
                            "max_degree": max_degree},
                    status="ok",
                    evidence_kind="EXACT_FINITE",
                    data={"found": {"order": order, "degree": degree},
                          "detail": r.data, "tried": tried},
                    runtime_s=tm.stop(),
                )
    return Result(
        tool="search_p_recurrence",
        inputs={"terms": len(terms), "max_order": max_order, "max_degree": max_degree},
        status="inconclusive",
        evidence_kind="EXACT_FINITE",
        data={
            "found": None,
            "tried": tried,
            "reading": "no recurrence in this window survived held-out verification; that is "
            "not proof the sequence is non-holonomic, only that it is not holonomic of this "
            "order and degree with this many terms",
        },
        runtime_s=tm.stop(),
    )
