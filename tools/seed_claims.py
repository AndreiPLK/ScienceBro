"""Seed the claim registry from what the lab already knows, with statuses it can defend.

Run once to create `research/claims/`. Kept in the repository because it documents the
initial state of the registry and can regenerate it if a file is lost; it never
overwrites a claim that has been edited by hand (it skips existing files unless
FORCE=1).
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "research" / "claims"
P = "projects/qg-bootstrap/results/"
FORCE = os.environ.get("FORCE") == "1"

ORDER_KEYS = (
    "statement",
    "domain",
    "status",
    "proof_artifact",
    "certificate_artifact",
    "counterexample",
    "why_dead",
    "last_verified",
)
LIST_KEYS = ("dependencies", "evidence", "references")


def w(cid: str, body: str, **k: object) -> None:
    C.mkdir(parents=True, exist_ok=True)
    path = C / f"{cid}.md"
    if path.exists() and not FORCE:
        return
    lines = [f"id: {cid}"]
    for key in ORDER_KEYS:
        if key in k:
            lines.append(f"{key}: {k.pop(key)}")
    for key in LIST_KEYS:
        vals = k.pop(key, [])
        lines.append(f"{key}:")
        for v in vals:  # type: ignore[union-attr]
            lines.append(f"  - {v}")
    assert not k, f"unused keys for {cid}: {k}"
    path.write_text(
        "---\n" + "\n".join(lines) + "\n---\n\n" + body.strip() + "\n", encoding="utf-8"
    )


w(
    "CLAIM-PROP1",
    statement="If every y-coefficient outside degrees J-2 and J-3 is nonnegative and (R) "
    "holds, then the far-below polynomial N(y) > 0 for y >= 0.",
    domain="every depth J",
    status="PROVED",
    proof_artifact=P + "THEOREM_STATE.md",
    last_verified="2026-08-29",
    dependencies=["CLAIM-TOPCOEF"],
    evidence=[
        "grouping argument: a quadratic with positive leading coefficient and "
        "nonpositive discriminant"
    ],
    references=[],
    body="""
Group the three middle terms as `y^(J-3) (c_(J-1) y^2 + c_(J-2) y + c_(J-3))`. (R) makes the
discriminant nonpositive and CLAIM-TOPCOEF makes the leading coefficient positive, so the
quadratic is nonnegative; the remaining terms are nonnegative by hypothesis.

`c_(J-3) >= 0` is NOT a hypothesis: (R) bounds it below by a square over a positive number.
""",
)

w(
    "CLAIM-TOPCOEF",
    statement="c_(J-1) = den^(J-1) E_(J-1) > 0 on the whole far-below region.",
    domain="every depth J, whole region",
    status="PROVED",
    proof_artifact=P + "UNIFORM_TOP_COEFFICIENT.md",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=["the coefficient formula collapses to a single term at the top index"],
    references=[],
    body="""
`den = kk(kk-2)` with `kk = v + K3 + 53 >= 53`, and `E_(J-1)` is an elementary symmetric
function of squares. Neither factor's positivity mentions the depth.
""",
)

w(
    "CLAIM-R",
    statement="4 c_(J-1) c_(J-3) - c_(J-2)^2 >= 0 on the far-below region.",
    domain="J = 7,9,12,16,20,25-32,35,40,45,50; from J=30 inside the regime n >= 2J-3",
    status="CERTIFIED",
    certificate_artifact=P + "certificate_audit.json",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=["nonnegative monomials to J=29", "one Bernstein step in thL from J=31"],
    references=[],
    body="""
Certified depth by depth, audited by `lab/certificate_audit.py`. NOT known uniformly in J:
that is Gap 1 of the programme.
""",
)

w(
    "CLAIM-LEGA",
    statement="Every y-coefficient c_k with k outside {J-2, J-3} is nonnegative.",
    domain="j = 9..16",
    status="CERTIFIED",
    certificate_artifact=P + "farbelow_negative_pattern_j16.json",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "negative monomials occur only at y-degree J-2: 11,30,41,71,96,130,165,205 for j = 9..16"
    ],
    references=[],
    body="""
The current ceiling of Theorem 2, and it is machine time rather than mathematics: the
verified coefficient formula gives each c_k separately (`lab/farbelow_coeff_signs.py`, now
with V_OFFSET for in-regime runs).
""",
)

w(
    "CLAIM-THM2",
    statement="For j = 9..16, inside n >= 2J-3, the far-below polynomial is positive for "
    "all y >= 0.",
    domain="j = 9..16",
    status="CERTIFIED",
    certificate_artifact=P + "THEOREM_STATE.md",
    last_verified="2026-08-29",
    dependencies=["CLAIM-R", "CLAIM-LEGA"],
    evidence=[
        "252 exact region points crossed with y up to 1e5 at j = 9,11,13,15, zero non-positive"
    ],
    references=[],
    body="""
A theorem conditional on certificates that exist for these depths. CERTIFIED rather than
PROVED because its hypotheses are supplied per depth by certificates, not by an argument
covering all J.
""",
)

w(
    "CLAIM-B",
    statement="p_(t+1)^3 p_(t-1) >= p_t^3 p_(t+2) for the central factorial family.",
    domain="every t <= 100 proved individually; uniformity in t open; first half of the range",
    status="COMPUTATIONALLY_VERIFIED",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "100 finite polynomial proofs, degrees 22 to 1606, 0 failures (conjecture_B_rungs.json)",
        "each rung: all coefficients nonnegative after the shift n = m + 2t",
    ],
    references=[],
    body="""
Each fixed t IS proved -- the shifted polynomial has nonnegative coefficients, which is an
argument and not a measurement. What is open is uniformity in t, so the general statement
sits at COMPUTATIONALLY_VERIFIED while the individual rungs are proofs.
""",
)

w(
    "CLAIM-HIER",
    statement="Delta^r log p_t < 0 for every r >= 2, with the difference window inside the "
    "first half.",
    domain="n = 9..32, r = 2..8, window inside the first half",
    status="COMPUTATIONALLY_VERIFIED",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "exact: signs decided by comparing products of rationals, no logarithm is evaluated",
        "0 violations (higher_difference_hierarchy.json)",
    ],
    references=["Central_Factorial_Anomaly_Map.pdf (parallel chat), section 2"],
    body="""
(B) is the member r = 3. Windows crossing the midpoint DO fail, consistently with the
reciprocal spectrum taking over past the midpoint.
""",
)

w(
    "CLAIM-MOMENT",
    statement="A_t = -Delta^2 log p_t admits a positive-measure (moment) representation.",
    domain="centred family, first half",
    status="DISPROVED",
    counterexample="negative Hankel minor at order 4 (forward) and 5-9 (reversed), n = 21..101",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "moment_route_refutation.json: exact fmpq determinants of A rationalised to "
        "300 digits, every decisive minor 200+ orders of magnitude above its error bound"
    ],
    references=[],
    body="""
Killed in both orientations. On paper the un-reversed Hausdorff form was already excluded:
the hierarchy makes A absolutely monotone, hence a moment sequence on [1, infinity), not on
[0,1]. See `research/dead_routes.md`.
""",
)

w(
    "CLAIM-P",
    statement="If q is real-rooted and ratio log-concave, its hypergeometric self-convolution "
    "is ratio log-concave on the first half.",
    domain="real-rooted inputs, m = 4..18",
    status="CONJECTURED",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "1409 supporting cases, 0 against, including the 174 with the smallest input "
        "margin (selfconv_preservation.json)"
    ],
    references=["AP_Squared_Ratio_Log_Concavity_Research_Brief.pdf, Problem 2"],
    body="""
The unrestricted version -- preservation for ANY ratio-log-concave input -- is FALSE: 1561 of
2800 general RLC inputs break. Real-rootedness is the load-bearing hypothesis.
""",
)

w(
    "CLAIM-NEWTON",
    statement="M_{n,t} = n(R_t - 1) <= 2 on the needed range.",
    domain="asymptotic half proved; finite n open",
    status="CONJECTURED",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=[
        "limit shape f < 2 on (0,1/2) proved (LIMIT_SHAPE_BOUND.md)",
        "M = f + g/n with g identified as the Edgeworth term (edgeworth_prediction.json)",
    ],
    references=[],
    body="""
Gap 2 of the programme. What remains is a remainder bound for a saddle-point expansion of a
Bernoulli sum -- by the doubling F = G^2, a sum of two i.i.d. halves.
""",
)

w(
    "CLAIM-POISSON",
    statement="M_{n,t} = n(rho_t beta_t - 1) exactly, with rho tilt-invariant and "
    "beta = t(N-t)/((t+1)(N-t+1)).",
    domain="algebraic identity; verified at all even n = 8..40 and all 2 <= t <= N-3",
    status="PROVED",
    proof_artifact=P + "POISSON_BINOMIAL_VIEW.md",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=["0 mismatches over the tested range; the split is an algebraic identity"],
    references=["Fatehi and Kittaneh, arXiv:1911.12167, Theorem 6"],
    body="""
prod(1 + b_i s) is the pgf of a Bernoulli sum and s is an exponential tilt; the s^t factors
cancel in rho, and beta is the binomial normalisation.
""",
)

w(
    "CLAIM-EDGEWORTH",
    statement="log rho = 1/K'' + K''''/(2 K''^3) - K'''^2/K''^4 up to O(1/n^3), in the "
    "tilted cumulants.",
    domain="n = 41..201, theta = 0.2..0.45",
    status="MEASURED",
    last_verified="2026-08-29",
    dependencies=["CLAIM-POISSON"],
    evidence=[
        "residual falls like 1/n^3, scaled column flat to about 5 percent "
        "(edgeworth_prediction.json)",
        "the Gaussian term alone leaves O(1/n^2)",
    ],
    references=[],
    body="""
The SHAPE of the expansion, verified as a rate. MEASURED and not PROVED because it carries no
remainder bound; supplying one is exactly Gap 2.
""",
)

w(
    "CLAIM-HARMONIC",
    statement="1/L is additive under independent sums, L the log-concavity excess.",
    domain="Bernoulli sums, matched at a common tilt",
    status="DISPROVED",
    counterexample="120 of 120 cases with 30-70 summands a side go the other way: 1/L is "
    "subadditive",
    last_verified="2026-08-29",
    dependencies=[],
    evidence=["excess_subadditivity.json"],
    references=[],
    body="""
My own idea, killed the same night. It would have given an upper bound on the excess; instead
it bounds it from below, which Newton already does. See `research/dead_routes.md`.
""",
)

print(f"claims present: {len(list(C.glob('*.md')))}")
