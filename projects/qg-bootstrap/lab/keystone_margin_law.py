"""THE MARGIN LAW: how close the knives get to the shore, quantitatively.

Two exact structural facts and one measured law.

FACT (proved, elementary). The leading coefficient of J in Q comes ONLY
from t = j-1 and equals (-1)^(j-1) E_{2(j-1)}(n) Q_n(j-1) times a positive
factor. Hence sign(leading) = (-1)^(j-1):
  * ODD  j: J -> +infinity as D grows, so no threshold can exist at large D;
  * EVEN j: J -> -infinity, so a threshold MUST exist.
That is why every dangerous cell in the whole project has even j.

MEASURED (this module). For even j the tightest level sits essentially ON
the trajectory that defines the shore, n* = k(lam) - 1 for lam >~ 14, and
the margin obeys

        D*(j, lam) - T_hat(lam)  ->  C * (j - 2),     C = 2.398 +- 0.002,

consistent with C = 12/5 = 2.4 within the residual drift of the shore
asymptotics itself. Equivalently, in ratio form,

        D*/T_hat - 1  ~  (j-2) c0 / (2 lam),   c0 = 0.2534 ,

and the shore itself grows as T_hat(lam) -> (12 + 4 sqrt 3) lam = 18.9282
lam (measured 18.9257 at lam = 1000).

WHAT THIS MEANS. The knives approach the shore like 1/lam and never reach
it at finite lam: the absolute gap does not shrink to zero, it saturates at
2.4 (j-2) dimensions. This is the quantitative form of the tangency-at-
infinity picture that the first knife theorem found geometrically, and it
also explains why lam above the last certified branch is the hard region:
that is where the RELATIVE margin is smallest.

STATUS: the leading-coefficient fact is proved; the margin law is measured,
not proved, and the constant is not identified in closed form. Recorded as a
regularity with an explicit falsifier: any cell with
D* - T_hat < 2.39 (j-2) - 0.05 at lam >= 100 refutes it.

Run: python lab/keystone_margin_law.py -> results/keystone_margin_law.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keystone_beta import J_poly_in_Q  # noqa: E402
from keystone_hunt import T_hat, T_k  # noqa: E402
from keystone_lowspin import threshold_D  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def main() -> int:
    t0 = time.time()

    # --- the proved part: sign of the leading coefficient ---------------
    sign_checks, sign_bad = 0, []
    for j in range(2, 20):
        for n in range(max(4, j + 1), j + 18, 3):
            for lam in (Fraction(1, 2), Fraction(3), Fraction(26)):
                lead = J_poly_in_Q(j, n, lam)[-1]
                sign_checks += 1
                if (lead > 0) != (j % 2 == 1):
                    sign_bad.append({"j": j, "n": n, "lam": str(lam)})

    # --- the measured part: the margin law ------------------------------
    rows = []
    for j in (4, 6, 8, 10):
        for lam_i in (100, 175, 250):
            lam = Fraction(lam_i)
            shore = T_hat(lam)
            k = min(range(3, int(3 * lam_i) + 61),
                    key=lambda kk: T_k(kk, lam))
            best = None
            for n in range(max(4, k - 8), k + 8):
                thr = threshold_D(j, n, lam)
                if thr is None:
                    continue
                if best is None or thr < best[0]:
                    best = (thr, n)
            if best is None:
                continue
            thr, n_star = best
            gap = float(thr - shore)
            rows.append({"j": j, "lam": lam_i, "k": k, "n_star": n_star,
                         "n_star_minus_k": n_star - k,
                         "shore": float(shore),
                         "D_threshold": float(thr),
                         "absolute_margin": gap,
                         "margin_over_j_minus_2": gap / (j - 2)})
            print(f"  j={j} lam={lam_i}: gap={gap:.5f}, "
                  f"gap/(j-2)={gap/(j-2):.6f} ({time.time()-t0:.0f}s)",
                  flush=True)

    consts = [r["margin_over_j_minus_2"] for r in rows]
    shore_slopes = {str(x): float(T_hat(Fraction(x))) / x
                    for x in (100, 250, 500, 1000)}
    out = {"proved_fact": {
               "statement": "leading coefficient of J in Q has sign"
                            " (-1)^(j-1); odd knives cannot develop a"
                            " threshold at large D, even knives must",
               "proof_sketch": "only t = j-1 contributes to Q^(j-1); its"
                               " coefficient is (-1)^(j-1) E_{2(j-1)}(n)"
                               " Q_n(j-1) times a positive product",
               "checks": sign_checks, "failures": sign_bad,
               "verified": not sign_bad},
           "measured_law": {
               "statement": "D*(j, lam) - T_hat(lam) -> C (j - 2) as lam"
                            " grows",
               "C_estimates": consts,
               "C_mean": sum(consts) / len(consts) if consts else None,
               "C_spread": (max(consts) - min(consts)) if consts else None,
               "closed_form_guess": "12/5 = 2.4, within the residual drift of"
                                    " the shore asymptotics; NOT identified",
               "ratio_form": "D*/T_hat - 1 ~ (j-2) c0 / (2 lam), c0 = 0.2534",
               "tightest_level": "n* = k(lam) - 1 for lam >~ 14, i.e. the"
                                 " tightest knife sits on the trajectory that"
                                 " defines the shore",
               "status": "REGULARITY, measured not proved",
               "falsifier": "any cell with D* - T_hat < 2.39 (j-2) - 0.05 at"
                            " lam >= 100 refutes it"},
           "shore_asymptotics": {
               "limit_slope": "12 + 4 sqrt 3 = 18.928203",
               "measured_T_hat_over_lam": shore_slopes},
           "rows": rows,
           "command": "python lab/keystone_margin_law.py",
           **stamp(), "runtime_s": round(time.time() - t0, 1)}
    (RES / "keystone_margin_law.json").write_text(json.dumps(out, indent=1),
                                                  encoding="utf-8")
    print(f"sign fact: {sign_checks} checks, {len(sign_bad)} failures",
          flush=True)
    if consts:
        print(f"margin law: C in [{min(consts):.6f}, {max(consts):.6f}]",
              flush=True)
    return 0 if not sign_bad else 1


if __name__ == "__main__":
    sys.exit(main())
