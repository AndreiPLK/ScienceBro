# Microproblem cards — week 1 (frozen before any results)

north_star_relevance: the (q,r,w) family of 2406.02665 IS the space of consistent tree
amplitudes under explicitly stated assumptions. Mapping exactly which members survive
unitarity, and whether deformations of the axioms admit new solutions, is the tree-level
core of the mission: "how unavoidable is the string amplitude, and which assumptions are
minimally necessary." Gravity (Virasoro–Shapiro, authors' open direction O3) is the next
rung on the same ladder.

---

## CARD A — The fate of the (r,w) island: positivity at all levels ⭐ SELECTED

**Exact statement.** For the q=1 amplitude family of Eq. 18 (parameters r, w, and external
mass² µ(0)), characterise the region P_N = {(r,w,µ(0)) : a_{n,ℓ} ≥ 0 for all
above-threshold levels n ≤ N and spins ℓ}, using the exact partial-wave coefficients of
Eq. A6, and determine the behaviour of P_N as N→∞: does it shrink to the Veneziano point,
converge to a stable open region, or collapse to a lower-dimensional set?

**Why it matters to the North Star.** The paper's headline is "Veneziano unique under the
strongest axioms"; but under the weaker (physically better motivated) axioms the whole
(r,w) family survives *crossing*. Whether *unitarity alone* already kills the deformations
is exactly a "minimal assumptions" question — if P_∞ has positive measure, there exists a
multi-parameter family of crossing-symmetric, dual-resonant, unitarity-compatible
non-string tree amplitudes; if it collapses, unitarity forces (near-)Veneziano without
invoking superpolynomial softness. Either outcome is a real statement.

**Already known** (novelty radar 2026-08-13 over all 49 citing papers, INSPIRE):
- Anchor paper: "broad regions consistent with positivity" at n ≤ 10, D = 4 (Fig. 1);
  region diminishes with D; q>1 excluded asymptotically via a_{n,n−1}/a_{n,n}.
- **Mansfield–Spradlin 2409.09561** rule large (r, m², D) regions in/out — but for the
  w = 0 hypergeometric slice (plus their own superstring analogue). MUST cite and build on;
  do not blindly redo w=0.
- 2502.20372: Veneziano point only, D=10. 2406.04410: bespoke family (different).
- 2607.24922 (de Rham–Tolley–Wang–Zhou, Jul 2026): unitarization-by-widths program,
  different object; cite as context.
- **No dedicated analysis found of the w ≠ 0 class or the joint (r,w,µ(0)) island fate at
  N→∞.** That is our unique slice; the card's focus narrows accordingly to w ≠ 0 and the
  joint island, with the w = 0 boundary cross-checked against Mansfield–Spradlin as an
  external control.

**Suspected gap.** No asymptotic analysis of a_{n,ℓ} at q=1 in (r,w); n=10 may be far from
asymptopia. Analogy with the q>1 sign-clash argument suggests trying closed-form ratios
a_{n,n−j}/a_{n,n} at large n as an analytic route after the numerics.

**Required knowledge.** Partial waves/Gegenbauer in D dims, threshold subtlety
(µ(n) ≥ 4µ(0) only — p.6 caveat), Stirling numbers; no string theory beyond the paper.

**Deterministic verifier.** Eq. A6 is rational in all arguments → evaluate a_{n,ℓ} in EXACT
rational arithmetic (Python fractions/flint) for rational (r,w,µ(0)); positivity checks are
exact, no floating point anywhere. Independent cross-check: numerically decompose the
residues of Eq. 18 in Gegenbauer polynomials at 50 digits (mpmath) and compare — two
implementations sharing no core code.

**Maximum possible claim.** NUMERICALLY_SUPPORTED map of P_N up to N ~ 10³ with exact
arithmetic + (if the pattern is clean) ANALYTICALLY_PROVED asymptotic statement about
P_∞; Lean formalisation candidate: the sign of an explicit rational sequence.

**Expected compute.** Rational arithmetic, laptop CPU; hours, not days.

**Success criteria (frozen).** (i) Reproduce Fig. 1 at n≤10 exactly; (ii) extend to N≥100
on a (r,w) grid ≥ 41×41 for at least 3 values of µ(0); (iii) a defensible statement about
monotonicity/limit of P_N with either proof sketch or explicit counter-behaviour.
**Kill criteria.** If exact evaluation at n~100 exceeds 1 min/point after optimisation, or
the region behaves non-monotonically with no pattern by day 3 of the card — stop, publish
the exact map as the artifact, record the obstruction.

---

## CARD B — Which λ=1 deformations survive second order?

**Exact statement.** For partial level truncation λ=1 (Eq. 21), the paper finds 5 solutions
of the linearised crossing system with superpolynomial falloff. Extend the perturbative
expansion of the crossing equations (Eq. 10 analogue) to second order and determine how
many of the 5 survive; characterise any survivor.

**Why (North Star).** A survivor = candidate NEW consistent amplitude family beyond
(q,r,w) — authors: "enticing to imagine these could be bona fide amplitudes." Zero
survivors = rigidity of Veneziano under λ=1, a new uniqueness-strengthening statement.
The authors explicitly left this to future work (O1).

**Known.** Counts 1,5,11,18,27 for λ=0..4 (linear order only, p.4).
**Gap.** Second order never computed (per the paper).
**Knowledge.** Perturbation theory on sequence spaces; careful bookkeeping; the residue
ansatz Eq. 21 with γ(n,j) unknowns.
**Verifier.** Exact symbolic algebra (SymPy over ℚ); the second-order system is finite at
each truncation level; consistency = exact rational identities.
**Max claim.** New amplitude candidate (then feed it to Card A machinery for unitarity) or
rigidity lemma; both ANALYTICALLY_PROVED-able in principle.
**Compute.** Symbolic; risk of expression swell.
**Success.** Survivor count at second order with certificates. **Kill.** If the
second-order system is not reducible below ~10⁴ terms per equation by day 3 → stop,
document the frontier, keep the λ=1 linear solutions as a verified artifact.

---

## CARD C — Full reproduction of the core theorem (the baseline; prerequisite)

**Exact statement.** Reproduce R1–R5 of the reading notes: derive Eqs. 11–13 from Eq. 9–10
symbolically; verify Eq. 15→17/18 and generic-point crossing at 50 digits; verify Regge
(Eq. 19) and fixed-angle (Eq. 20) asymptotics; reproduce Fig. 1 (n≤10, D=4); reproduce the
λ=0..4 counts 1,5,11,18,27.
**Why.** Our own doctrine: prove the laboratory does not lie before pointing it anywhere
(the Schwarzschild-reproduction move). Every later claim inherits credibility from this.
**Verifier.** SymPy exact algebra + mpmath 50-digit numerics, two routes per statement.
**Max claim.** Public artifact "independent reproduction with code"; not a paper by itself.
**Compute.** Days 3–5. **Kill.** A genuine failure to reproduce any of R1–R5 is not a kill
— it is a finding; triple-check, then it becomes the week's result.

---

## FROZEN DECISION (2026-08-13, before any computation)

Order: **C (days 3–5) → A (days 5–7)**; B queued behind A as the ambitious follow-up.
Rationale: A has the best product of importance × verifiability × finishability, an exact
(rational-arithmetic) verifier, and a real gap stated by the paper's own figure caption.
Evaluation criteria and kill criteria above are frozen with this commit; they may be
tightened, never loosened after results are seen.
