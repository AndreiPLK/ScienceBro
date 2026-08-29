"""How much room a root bound has: the certified margin 1 - c* at the shore.

WHY.  results/FFP_LITERATURE_PASS.md sec. 3 leaves one live route: a bound
theta_max(p BOX_N q) < 1 would give the whole diagonal (j,D) -> (j-m, D-2m) at
once, with no knife value known in advance.  Before hunting for such a bound it
is worth knowing how tight it has to be -- Theorem 9 died (sec. 6c of
BFORM_POSITIVITY_THEOREM.md) precisely because its slack could not be recovered
by any constant, and that was discovered too late.

WHAT IS MEASURED.  For each (n, r, lam) at the shore D = T_hat, the smallest c
on a dyadic bisection for which the exact Descartes test certifies that the
reduced composition has NO real zero in [c, inf).  c* is therefore a certified
UPPER bound on the largest real root, and the margin is 1 - c*.  A margin that
stays positive means a root bound can exist; how fast it shrinks in n says how
sharp that bound must be.

Everything is exact fmpq; floats appear only in the printed report and in the
fitted exponent.

Run: python lab/root_margin_scan.py -> results/root_margin_scan.json
"""

from __future__ import annotations

import json
import sys
import time
from math import log
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ffp_convolution_check import conv_e, real_root_bound, reduced_poly  # noqa: E402
from moment_kernel_probe import shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def depths(n: int) -> list[int]:
    """All depths for small n; a spread of five for large n, cost being quadratic."""
    if n <= 28:
        return list(range(2, n - 1))
    return sorted({2, max(2, n // 4), n // 2, (3 * n) // 4, n - 2})


def scan(ns: tuple[int, ...], lams: tuple[fmpq, ...]) -> list[dict]:
    rows = []
    for n in ns:
        for lam in lams:
            T_hat = shore(lam)[0]
            H = (T_hat + 4 * n - 7) / 2
            worst, worst_r, none_at = None, None, []
            for r in depths(n):
                c = real_root_bound(reduced_poly(conv_e(n, r, lam, H)))
                if c is None:
                    none_at.append(r)
                    continue
                margin = fmpq(1) - c
                if worst is None or margin < worst:
                    worst, worst_r = margin, r
            rows.append(
                {
                    "n": n,
                    "lam": str(lam),
                    "depths_tested": len(depths(n)),
                    "uncertified_depths": none_at,
                    "worst_margin": float(worst) if worst is not None else None,
                    "worst_margin_exact": str(worst) if worst is not None else None,
                    "worst_at_r": worst_r,
                    "worst_margin_times_n": float(worst) * n if worst is not None else None,
                }
            )
            print(
                f"n={n:4d} lam={float(lam):7.1f}  worst margin {float(worst):+.5f} "
                f"at r={worst_r}  (margin*n = {float(worst) * n:.2f})",
                flush=True,
            )
    return rows


def fit_exponent(rows: list[dict], lam: str) -> dict | None:
    """Least-squares slope of log(margin) against log(n) at fixed lam."""
    pts = [(r["n"], r["worst_margin"]) for r in rows if r["lam"] == lam and r["worst_margin"]]
    if len(pts) < 3:
        return None
    xs = [log(n) for n, _ in pts]
    ys = [log(m) for _, m in pts]
    xm = sum(xs) / len(xs)
    ym = sum(ys) / len(ys)
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys, strict=True))
    den = sum((x - xm) ** 2 for x in xs)
    return {"lam": lam, "points": len(pts), "slope_log_log": num / den if den else None}


def main() -> int:
    t0 = time.time()
    ns = (6, 8, 12, 16, 20, 28, 40, 60, 80)
    lams = (fmpq(1), fmpq(5, 2), fmpq(7), fmpq(30))
    rows = scan(ns, lams)
    fits = [f for f in (fit_exponent(rows, str(x)) for x in lams) if f]
    out = {
        "what": "certified margin 1 - c* at the shore, where c* upper-bounds the largest "
        "real root of the reduced Schur-Szego composition",
        "reading": "a positive margin everywhere means a root bound CAN close the diagonal; "
        "the log-log slope says how sharp it must be in n",
        "rows": rows,
        "log_log_fits": fits,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "root_margin_scan.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for f in fits:
        print(f"lam={f['lam']}: margin ~ n^({f['slope_log_log']:.2f})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
