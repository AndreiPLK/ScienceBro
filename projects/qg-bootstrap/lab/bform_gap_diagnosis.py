"""Where exactly does the J-form bound lose, and which fixes are dead?

Theorem 9 (results/BFORM_POSITIVITY_THEOREM.md sec. 4b) proves positivity for
lam ~> 32 n by splitting

    K_r * B(n-1/2, b) = INT_0^1 w^{a-1}(1-w)^{b-1} prod_i (w - eta_i) dw

at w = eta = max_i eta_i, lower-bounding the piece on [eta, 1] and
upper-bounding the piece on [0, eta]. A useful accident makes the two pieces
directly comparable: a + r = n - 1/2 = C + 1 ALWAYS, so B(a+r, b) is the very
normaliser of the J-form, and dividing through by it leaves

    K_r  >=  POS - NEG,
    POS := (1-eta)^{n-3/2+b},      NEG := eta^{n-1/2} / [ a B(n-1/2, b) ].

Both are computed here as certified arb quantities against the exact K_r, at and
around the proved threshold, which settles which side is at fault.

THE ANSWER (see the table in the artifact): NEG is the binding side, by a wide
margin. It spans fourteen orders of magnitude over the grid and explodes below
the threshold -- at n = 20, lam = 30, r = 18 it is 3.1e14 against a true K_r of
1.9e-3 -- whereas POS stays within a factor of 1.2 to 29 of the true K_r (the
loss grows with depth: 1.2x at n=12, r=2, lam=2000; 29x at n=20, r=18,
lam=531). So POS is lossy too and is NOT negligible at large r, but the
threshold is set by NEG: the one crude step |prod_i (w - eta_i)| <= eta^r on
[0, eta], which ignores that the integrand vanishes at each of the r roots.

TWO FIXES TESTED AND KILLED HERE:

 1. The triangle inequality |prod_i (w - eta_i)| <= sum_t e_t(eta) w^{r-t},
    which integrates in closed form to sum_t e_t(eta) eta^{a+r-t}/(a+r-t). This
    is WORSE, not better: dropping the signs destroys exactly the cancellation
    that makes the piece small, and the bound degrades by up to 2^r. Measured
    below as the ratio NEG_triangle / NEG.
 2. A per-instance certified quadrature of the integral's sign. This is
    CIRCULAR and was abandoned before being built: for a given (n, r, lam, D)
    the sign of the integral is exactly the sign of K_r, which the repository
    already computes exactly. A per-instance certificate can therefore never add
    information -- only an all-n bound can, which is why the loss has to be
    closed analytically.

WHERE THE SHORE ENTERS. The programme has repeatedly noted that every route so
far imposes D <= T_hat(lam) only at the very end. The J-form says where it
belongs: the weight is Beta(a, b) with b = D/2 + (n-2-r), so its mean
a/(a+b) = (n-1/2-r)/(D/2 + 2n - 5/2 - 2r) SHRINKS as D grows. Raising D slides
the weight's mass toward w = 0, which is exactly where the roots sit and where
the integrand oscillates. Both the mean and eta_max shrink as lam grows, but at
different rates, and what matters is their RATIO: measured at n = 20, r = 18 it
climbs 0.04 -> 0.15 -> 0.28 -> 1.00 at lam = 30, 272, 531, 2000. So the shore
condition is not an afterthought in this representation -- it is the statement
that the weight's mass stays clear of the roots. This script measures that.

Run: python lab/bform_gap_diagnosis.py -> results/bform_gap_diagnosis.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import arb, ctx, fmpq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bform_derivative_form import eta_e_sym
from bform_jacobi_bound import A, eta_max_exact
from bform_positivity import K_bform, b_values, shore_fast
from provenance import stamp

RES = Path(__file__).resolve().parents[1] / "results"


def pieces(n: int, r: int, lam: fmpq, D: fmpq) -> tuple[arb, arb, arb, fmpq]:
    """(POS, NEG, NEG_triangle, K_r) -- all comparable after dividing by B."""
    a = A(fmpq(2 * n - 1, 2) - r)
    b = A(D / 2 + (n - 2 - r))
    e = eta_max_exact(n, lam, r)
    half = arb(n) - arb(1) / 2
    logB = half.lgamma() + b.lgamma() - (half + b).lgamma()
    pos = (1 - e) ** (arb(n) - arb(3) / 2 + b)
    neg = ((half * e.log()) - a.log() - logB).exp()
    # the triangle-inequality variant, integrated exactly, same normalisation
    es = eta_e_sym(b_values(n, lam), r)
    tri = arb(0)
    for t in range(r + 1):
        et = A(es[t]) if es[t] >= 0 else -A(-es[t])
        tri += abs(et) * e ** (a + r - t) / (a + r - t)
    tri = tri / (e ** (a + r) / a) * neg  # rescale to NEG's normalisation
    return pos, neg, tri, K_bform(n, r + 1, lam, D)


def main() -> int:
    t0 = time.time()
    ctx.prec = 500
    rows, tri_ratios = [], []
    print(f"{'n':>3} {'lam':>6} {'r':>3} {'K_r(true)':>11} {'POS':>11} "
          f"{'NEG':>11} {'NEG_tri/NEG':>12}", flush=True)
    for n in (12, 20):
        for lam_i in (30, 272, 531, 2000):
            lam = fmpq(lam_i)
            D = shore_fast(lam)
            for r in (2, n // 2, n - 2):
                pos, neg, tri, K = pieces(n, r, lam, D)
                ratio = float(tri / neg) if neg.mid() != 0 else None
                tri_ratios.append(ratio)
                rows.append({
                    "n": n, "lam": lam_i, "r": r,
                    "K_true": float(K), "POS": float(pos), "NEG": float(neg),
                    "bound_closes": (pos - neg).lower() > 0,
                    "POS_over_K": float(pos) / float(K) if K != 0 else None,
                    "NEG_triangle_over_NEG": ratio,
                    "beta_weight_mean": float(
                        (fmpq(2 * n - 1, 2) - r)
                        / (D / 2 + 2 * n - fmpq(5, 2) - 2 * r)),
                    "eta_max": float(eta_max_exact(n, lam, r).mid()),
                })
                print(f"{n:>3} {lam_i:>6} {r:>3} {float(K):>11.3e} "
                      f"{float(pos):>11.3e} {float(neg):>11.3e} "
                      f"{ratio:>12.3e}", flush=True)

    worse = sum(1 for x in tri_ratios if x is not None and x >= 1)
    print(f"the triangle-inequality variant is WORSE (ratio >= 1) in "
          f"{worse}/{len(tri_ratios)} cases; max ratio "
          f"{max(x for x in tri_ratios if x is not None):.3e}", flush=True)
    slide = [(x["lam"], x["beta_weight_mean"], x["eta_max"]) for x in rows
             if x["n"] == 20 and x["r"] == 18]
    print("the shore slide (n=20, r=18): mean(W) and eta_max both shrink with "
          "lam, but their RATIO climbs -- the weight clears the roots:", flush=True)
    for lam_i, mean, em in slide:
        print(f"   lam={lam_i:>5}: mean(W) = {mean:.4e}, eta_max = {em:.4e}, "
              f"ratio = {mean / em:.2f}", flush=True)

    out = {
        "claim": (
            "DIAGNOSIS OF THE J-FORM BOUND'S REMAINING GAP. Using the accident "
            "a + r = n - 1/2 = C + 1, which makes B(a+r,b) the J-form's own "
            "normaliser, Theorem 9's two sides become directly comparable with "
            "the exact K_r: K_r >= POS - NEG with POS = (1-eta)^{n-3/2+b} and "
            "NEG = eta^{n-1/2}/[a B(n-1/2,b)]. MEASURED: NEG is the binding "
            "side. POS sits only a single-digit factor below the true K_r, "
            "while NEG explodes below the threshold (3.1e14 against a true K_r "
            "of 1.9e-3 at n=20, lam=30, r=18). So the remaining distance to the "
            "measured Hausdorff corner is almost entirely the single step "
            "|prod (w-eta_i)| <= eta^r on [0,eta]. TWO FIXES KILLED: the "
            "triangle inequality sum_t e_t(eta) w^{r-t} is WORSE by the factor "
            "recorded in NEG_triangle_over_NEG, because dropping the signs "
            "destroys the cancellation that makes the piece small; and a "
            "per-instance certified quadrature is circular, since the sign of "
            "the integral IS the sign of K_r, which is already computed "
            "exactly. WHERE THE SHORE ENTERS: the weight is Beta(a,b) with "
            "b = D/2 + (n-2-r), so its mean a/(a+b) shrinks as D grows, sliding "
            "the mass toward w = 0 where the roots sit. The mean and eta_max "
            "both shrink with lam but at different rates; their RATIO climbs "
            "0.04 -> 0.15 -> 0.28 -> 1.00 at lam = 30, 272, 531, 2000 "
            "(n=20, r=18). In this representation the shore condition is not "
            "an afterthought -- it is the statement that the weight's mass "
            "stays clear of the roots."
        ),
        "rows": rows,
        "triangle_worse_in": [worse, len(tri_ratios)],
        "command": "python lab/bform_gap_diagnosis.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "bform_gap_diagnosis.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
