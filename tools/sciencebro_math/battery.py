"""anomaly_scan: ask a sequence everything at once, and report what is UNUSUAL.

Phase 6 of the lab charter says: never test only the inequality that was asked for.
This runs the whole battery and, more importantly, ranks the answers by how surprising
they are, because a report that lists forty passing checks buries the one that matters.

A finding is called an ANOMALY when it is stronger than what was asked, or holds where
there was no reason for it to, or fails at a distinguished place. The scan does not
interpret; it flags, and says exactly what was tested.
"""

from __future__ import annotations

from typing import Any

from flint import fmpq

from . import sequences as S
from .core import Result, timed
from .families import esym, normalized_means


def anomaly_scan(values: Any, rmax: int = 8, window_inside_first_half: bool = True) -> Result:
    """Run the battery on one positive sequence and rank what came back."""
    tm = timed()
    p = S.as_seq(values)
    n = len(p)
    half = (n - 1) // 2
    win = half if window_inside_first_half else None

    checks: dict[str, Result] = {
        "ratio_log_concavity": S.ratio_log_concavity(p),
        "turan": S.turan(p),
        "log_difference_hierarchy": S.log_difference_hierarchy(p, rmax, win),
        "hankel": S.hankel_minors(p, max_order=min(6, n // 2)),
        "stieltjes": S.stieltjes_conditions(p, max_order=min(5, n // 2)),
        "hausdorff": S.hausdorff_conditions(p, max_order=min(10, n - 1)),
        "toeplitz": S.toeplitz_minors(p, max_order=min(4, n // 2)),
    }
    try:
        checks["real_rootedness"] = S.real_rootedness(p)
    except Exception as exc:  # certified root isolation can be expensive; never fatal
        checks["real_rootedness"] = Result(
            tool="real_rootedness",
            inputs={"n": n},
            status="error",
            evidence_kind="EXACT_FINITE",
            data={"error": str(exc)},
        )

    anomalies: list[dict] = []
    h = checks["log_difference_hierarchy"]
    if h.status == "ok" and h.data["by_order"]:
        top = max(int(k) for k in h.data["by_order"])
        anomalies.append(
            {
                "what": f"every log difference of order 2..{top} is negative",
                "why_unusual": "log-concavity alone gives only order 2; a whole hierarchy "
                "suggests a positive-measure or total-positivity mechanism",
                "strength": "stronger than asked",
            }
        )
    if checks["hausdorff"].data.get("completely_monotone_reversed") and not checks[
        "hausdorff"
    ].data.get("completely_monotone_forward"):
        anomalies.append(
            {
                "what": "completely monotone only after reversing the index",
                "why_unusual": "a Hausdorff representation exists for the reversed sequence "
                "and cannot exist for the forward one",
                "strength": "structural",
            }
        )
    if checks["toeplitz"].status == "ok":
        anomalies.append(
            {
                "what": f"all Toeplitz minors to order {checks['toeplitz'].inputs['max_order']} "
                "are nonnegative",
                "why_unusual": "consistent with a Polya frequency sequence, which would imply "
                "far more than log-concavity",
                "strength": "stronger than asked",
            }
        )
    if checks["hankel"].status == "ok":
        anomalies.append(
            {
                "what": "all leading Hankel minors nonnegative",
                "why_unusual": "a Hamburger moment signature; worth testing Stieltjes next",
                "strength": "structural",
            }
        )

    refuted = {k: v.status for k, v in checks.items() if v.status == "refuted"}
    return Result(
        tool="anomaly_scan",
        inputs={"n": n, "rmax": rmax, "window_inside_first_half": window_inside_first_half},
        status="ok",
        evidence_kind="EXACT_FINITE",
        data={
            "checks": {k: {"status": v.status, "data": v.data} for k, v in checks.items()},
            "refuted": refuted,
            "anomalies": anomalies,
            "reading": "an anomaly is a flag, not a theorem; each one is a conjecture to be "
            "attacked next, not a result to be reported",
        },
        runtime_s=tm.stop(),
    )


def scan_family_centered(n_values: list[int], rmax: int = 8) -> Result:
    """The scan over the physical centred family, which is what most questions are about."""
    tm = timed()
    from .families import centered_squares

    rows = []
    for n in n_values:
        b = centered_squares(n)
        p = normalized_means(b)
        r = anomaly_scan(p, rmax=rmax)
        rows.append(
            {
                "n": n,
                "N": len(b),
                "refuted": r.data["refuted"],
                "anomaly_count": len(r.data["anomalies"]),
                "hierarchy_all_negative": r.data["checks"]["log_difference_hierarchy"]["data"][
                    "all_negative"
                ],
                "hausdorff_forward": r.data["checks"]["hausdorff"]["data"][
                    "completely_monotone_forward"
                ],
                "hausdorff_reversed": r.data["checks"]["hausdorff"]["data"][
                    "completely_monotone_reversed"
                ],
                "hankel_ok": r.data["checks"]["hankel"]["status"] == "ok",
                "toeplitz_ok": r.data["checks"]["toeplitz"]["status"] == "ok",
                "stieltjes_ok": r.data["checks"]["stieltjes"]["status"] == "ok",
            }
        )
    return Result(
        tool="scan_family_centered",
        inputs={"n_values": n_values, "rmax": rmax},
        status="ok",
        evidence_kind="EXACT_FINITE",
        data={"rows": rows},
        runtime_s=tm.stop(),
    )


def raw_elementary(n: int) -> list[fmpq]:
    """e_t of the centred spectrum, unnormalised -- some structures live here instead."""
    from .families import centered_squares

    return esym(centered_squares(n))
