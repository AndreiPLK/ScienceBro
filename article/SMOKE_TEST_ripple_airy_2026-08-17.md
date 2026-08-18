# Smoke test: ripple, cusps, n^(2/3), positivity, family exclusion

Written 2026-08-17 late evening. Every number below comes from a run in this
repository on this date; the runs are named so they can be repeated.

## 1. What is already known (not ours)

| Known result | Where | What it gives us |
|---|---|---|
| Schoenberg: a zonal function is positive definite on S^{d-1} iff its ultraspherical expansion has nonnegative coefficients | Schoenberg 1942; modern restatement [arXiv:1701.07214](https://arxiv.org/pdf/1701.07214) | the exact frame for our reformulated statement |
| Nonnegative linearization of Jacobi polynomials (products expand with nonnegative coefficients under parameter conditions) | Gasper; Askey–Gasper 1971; survey [arXiv:1812.05542](https://arxiv.org/pdf/1812.05542) | why a factor-by-factor induction was worth trying at all |
| Dimension walks on spheres (Matheron montee/descente) | [arXiv:1303.6856](https://arxiv.org/pdf/1303.6856) | our "descent lemma" is this, and it is prior art -- credited in the code |
| Chester–Friedman–Ursell uniform asymptotics near two coalescing saddles; Airy behaviour | DLMF 2.4, 9.15 | the standard route IF two saddles coalesce |
| Global Airy asymptotics for Hahn polynomials | [arXiv:1210.2359](https://arxiv.org/abs/1210.2359) | the model to imitate if a second-order recursion in j exists |

## 2. What we actually observe (this repo, this date)

* The CHR graviton family reduces to ONE univariate object: sign of knife j is
  the sign of a single exact rational number (`lab/keystone_beta.py`, and the
  sharper form below).
* NEW tonight, verified: knife j enters only through m = n - j, and
      sign(knife j) = (-1)^m x (m-th Jacobi coefficient of F),
      F(u) = u^eps prod_a (u - (a/s)^2)^2 >= 0,  s = lam + n - 1,
      a in {n-2, n-4, ...},  alpha = -1/2,  beta = D/2 - 2.
  4500 exact sign checks against the independently computed value, 0 mismatches
  (`results/jacobi_normal_form.json`).
* Consequence: the grand theorem is exactly "F has an all-positive Jacobi
  expansion", i.e. by Schoenberg "F is positive definite on S^{D-2}" -- which is
  the celestial sphere of D-dimensional spacetime. So this is a faithful
  translation of partial-wave positivity, NOT a shortcut past it.
* Coverage so far: 7084 coefficients below the shore, zero non-positive; levels
  n = 24..80 at lam = 1, 7 and D = 6, 11, all m, zero non-positive; the running
  grid (`results/normal_form_certificates.json`) is at 1282 cells, zero
  negatives.
* Cost: n = 60 settles all 59 knives in 35 s, against 9941 s for the strip
  certificate run to reach j = 28.

## 3. Alternative explanations, and what happened to each

| Explanation | Verdict tonight | Evidence |
|---|---|---|
| Block widths follow an arithmetic law (step 6) | FALSIFIED | the widths 8, 14, 20 were an artefact of scanning only even j; on the full integer grid they are 9, 17, 2, 24, 33 |
| The pattern is an Airy / fold caustic (two saddles coalescing) | FALSIFIED in that form | minimum saddle separation falls smoothly and monotonically, 2.1e-5 -> 2.3e-6 over j = 44..94, with NO feature at block edges; the near-pairs sit at abs(z) ~ 1e-4, far inside the loop |
| The oscillation comes from one conjugate pair of saddles | FALSIFIED | its angle is constant to four digits, giving a fixed period of 14.87 knives, while measured peak spacings GROW: 10, 13, 15, 18, 21 |
| n^(2/3) scaling of the block widths | NOT ESTABLISHED | my earlier collapse metric was invalid (absolute spread shrinks mechanically as the exponent grows); on 16 well-separated extrema q = 1/2 and q = 2/3 are indistinguishable, R^2 0.9922 vs 0.9931, and residuals are 0.83 phase steps where a single phase needs well under 0.5 |
| The blocks are a property of the problem | PARTLY INSTRUMENT | the argument principle forces a sign-definite circle to enclose exactly N = j-1 roots of P; searching the radius in the correct window PROVED j = 52, 82, 86 dip-free although they were recorded as dips |
| Factor-by-factor (Gasper-style) induction proves the positivity | FALSIFIED | a single square (u-c)^2 has negative coefficients (18 of 84 tested); positivity is COLLECTIVE |

## 4. The next test that can most strongly confirm or destroy the live hypothesis

Live hypothesis: the positivity is proved by induction on the ladder of roots
taken SMALLEST FIRST. Measured tonight: adding factors smallest-first keeps every
coefficient positive at EVERY step, while largest-first fails until enough
factors accumulate.

The step threshold was measured by bisection (n = 31, lam = 1, D = 6): the
largest new root that preserves positivity satisfies

        1 - c_max  ~  0.446 * t^(-0.917),   t = number of factors already in,

while the real ladder's top root satisfies 1 - c_top = 0.125 at n = 31, and
1 - c_top ~ 4/n in general with t_max ~ n/2, i.e. threshold gap ~ 0.9/n against
ladder gap ~ 4/n. The margin therefore survives as n grows -- consistent with the
n = 80 check.

DECISIVE NEXT TEST: prove or refute the STEP LEMMA

    if H has an all-positive expansion and 1 - c >= C / deg-related-count,
    then H(u) (u - c)^2 also has an all-positive expansion,

first numerically over a wide (c, t, D, beta) grid to fix the constant C and the
exact form of the count, then by hand. If the lemma is false, the induction dies
and the collective mechanism must be found elsewhere; if it holds, the theorem
follows for all n at once and is a candidate for Lean formalisation.

## What was skipped, and why

* Paper Search MCP: third-party code; our security rules require inspection and
  a pinned commit SHA before running, and arXiv / Crossref / OpenAlex are
  already reachable. Deferred deliberately, not forgotten.
* Lean skills: Lean formalises finished proofs, it does not find them. Nothing
  is ready to formalise until the step lemma has a hand proof. That is the
  trigger to install it.
* Four science roles: already exist as `.claude/agents/` (literature-reviewer =
  Scout, domain-critic = Skeptic, independent-validator = Verifier) plus the
  `professor` skill (Teacher). Creating new ones would duplicate the contour.
* Zotero, Wolfram / Mathematica: not installed on this machine. No paid software
  installed without permission. Exact and interval arithmetic is already covered
  by flint / arb, with Z3 as the foreign judge.
* INSPIRE HEP MCP: added to `.mcp.json` at PROJECT scope, not user scope, because
  the standing rule in CLAUDE.md forbids touching global Claude settings. It
  becomes available at the next session start.
