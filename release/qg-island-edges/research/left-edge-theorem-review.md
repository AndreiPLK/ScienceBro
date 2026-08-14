# Domain-critic review: left-edge-theorem.md

Reviewer: domain-critic agent, 2026-08-13.
Scope: the four claims in `left-edge-theorem.md` against
`lab/repro_r4_positivity_spot.py` and `2406.02665-notes.md`.

**Transparency note (binding).** This review session had no code-execution tool
(Read/Grep/Write only), so the reviewer could NOT run Python despite the task
offering it. Every item below marked "hand-verified" is exact integer/rational
algebra written out explicitly in this file — deterministic and auditable, not
verbal judgment. Every item that needs machine arithmetic is collected in the
prepared, UNRUN attack script:
`C:\Users\user\AppData\Local\Temp\claude\C--Users-user-ScienceBro\93847525-923a-41ca-a919-bf7a73c639c3\scratchpad\attack_left_edge.py`
Running that script (exit 0 required) is a REQUIRED FIX before any promotion.

## SUMMARY

| Claim | Verdict |
|---|---|
| 1. a_{n,n-1} closed form + sign law (mu0=0) | **PASS (conditional)** — derivation independently re-verified by hand, algebra correct; conditional only on route-2's residue being Eq. 16 at q→1 (two-route validated, but at mu0=0 only) and on the unrun machine attack. |
| 2. Generalization sign factor n(r+(1+mu0)/2)+w for n>3mu0 | **CONDITIONAL PASS** — algebra and threshold bookkeeping re-verified by hand and correct; BUT the evaluator it leans on was never two-route validated at mu0≠0 (real gap, see Errors E1), and the n=3mu0 degenerate case is unstated (E2). |
| 3. sign(a_{n,n-2}) bracket (mu0=0) | **PASS — and upgradeable.** Reviewer independently re-derived the bracket and proved it for ALL n (exact polynomial identity, below), strictly stronger than the file's n=3..8 brute force. Physical-domain conditioning applies as for claim 1. |
| 4. "Complete characterization" of the island | **CONDITIONAL / correctly a conjecture.** The status line labels it honestly; the section header and one corollary overstate it (see Overclaim check). The l≤n-2, n>5 non-binding assumption is empirical only; two logical gaps found (E3, E4). |

No mathematical error was found in the derivations of claims 1–3. The problems
found are validation-coverage gaps and wording, not algebra.

## Point-by-point checks requested

**(a) Residue polynomial roots.** Hand-verified correct. Route 2's residue is
R(n,t') = (1+r+t')_n/(2+r)_n · (1+r+t'+w)(1+n+r+w)/((1+r+t')(1+r+w)).
The Pochhammer identity (1+r+t')_n = (1+r+t')(2+r+t')_{n-1} cancels the
denominator factor exactly, so the full t'-dependence is
(2+r+t')_{n-1}(1+r+t'+w): degree (n-1)+1 = n, roots t' = -(2+r+k), k=0..n-2,
and t' = -(1+r+w), exactly as claimed. Monic, so A = -(sum of roots) =
(n-1)(2+r)+(n-1)(n-2)/2+(1+r+w). Correct. (Conditional on R itself matching
Eq. 16 at q→1 — backed by the two-route Veneziano/A6 validation, mu0=0.)

**(b) Substitution kinematics.** Correct. Paper: t = -(s-4mu0)(1-x)/2 at
s = mu(n) = n+mu0, then t' = t-mu0, giving t' = alpha·x + beta with
alpha = (n-3mu0)/2, beta = -alpha-mu0 — exactly the code (line 138) and the
theorem file. At mu0=0 this is t = (n/2)(x-1). The threshold caveat
mu(n) ≥ 4mu0 ⇔ n ≥ 3mu0 lines up exactly with alpha ≥ 0; the file's strict
n > 3mu0 restriction is the right domain (see also E2).
Hand-recomputed: A - n²/2 = n(r+1/2)+w (twice, independently) — matches line 40.
A + n·beta with beta = -(n-mu0)/2 gives n(r+(1+mu0)/2)+w — matches line 79.

**(c) Legendre parity argument.** Valid, and (a point the file does not make)
valid for ANY mu0, since it never uses parity of the substituted polynomial —
only ∫P_m x^k dx = 0 when k<m or k≢m (mod 2). Among monomials x^0..x^n of the
degree-n polynomial in x: x^n has parity n ≠ n-1 (killed by parity),
x^{n-3}, x^{n-5}, ... have degree < n-1 (killed by orthogonality), so only
x^{n-1} feeds P_{n-1}. For P_{n-2}: x^n and x^{n-2} both survive (parity n-2 ≡ n,
degree ≥ n-2), x^{n-1} killed by parity, lower even-parity by degree — exactly
the two monomials claim 3 uses. The integral formula
∫P_{n-1}x^{n-1} = 2^n((n-1)!)²/(2n-1)! checks against m=1 (2/3) and m=2 (4/15).
K(n) > 0 is then immediate.

**(d) Sign bookkeeping of alpha^{n-1}.** The stated validity domain is right:
for n > 3mu0, alpha > 0, so alpha^{n-1} > 0 for both parities and the sign
factor is n(r+(1+mu0)/2)+w alone. For n < 3mu0 (alpha < 0, n-1 odd ⇒ extra
minus sign) the naive law would be wrong — but the paper's threshold caveat
means positivity is not imposed there at all, so the restriction is physical,
not cosmetic. Two unstated edge items: (i) at n = 3mu0 exactly (possible when
3mu0 ∈ Z, and this IS at threshold since mu(n)=4mu0), alpha=0 makes the residue
constant in x, so a_{n,n-1} = 0 identically while the sign factor is generically
nonzero — the strict inequality n>3mu0 silently saves the claim, but the file
should say so (E2). (ii) For mu0 < 0 every n ≥ 1 is above threshold and alpha>0
always — no issue.

**(e) "Conjecturally complete" labeling.** Mostly honest; two spots overreach
(see Overclaim check).

**(f) Threshold caveat at mu0 ≠ 0.** No step in the mu0≠0 derivation imposes
positivity below threshold: claim 2 is restricted to n>3mu0 ≡ above threshold;
the razor tests (n=19..21 at 3mu0=1.8; n=14..16 at 3mu0=-1.8) are all far above
threshold; the evaluator skips sub-threshold levels (repro line 159,
`n + mu0 < 4*mu0`). Claim 4 is mu0=0 where the caveat is vacuous. One forward
caution: the planned mu0-stack comparison (file lines 89–91) must use the
mu0-analog of the "n≤5 block" with sub-threshold n removed when mu0>0.

## ERRORS FOUND

- **E1 (validation gap, affects claim 2).** The theorem file calls the
  evaluator "two-route-validated", but `repro_r4_positivity_spot.py::main()`
  runs its three frozen spot checks at **mu0 = 0 only** (lines 187–193:
  `run_point(..., F(0), ...)` in every case). Route 2's mu0 enters solely
  through the kinematic substitution — the same substitution the claim-2
  derivation uses. If the mu0≠0 razor tests (file lines 86–88) were run through
  route 2, they are **circular**: they test the derivation against itself. The
  file does not say which route was used. Required: cross-check route 1
  (Eq. A6, structurally independent, has explicit mu0 dependence) against
  route 2 at mu0≠0, including both razor points (attack script, ATTACK 3).
- **E2 (unstated degenerate case, claim 2).** At n = 3mu0 (at threshold when
  3mu0 ∈ Z, e.g. mu0=1, n=3) the coefficient is identically zero while the sign
  factor is generically nonzero. Covered by the strict n>3mu0, but should be
  stated explicitly to prevent misuse of the formula at the boundary.
- **E3 (undefined term, claim 4).** "Within the domain" / "domain pole" is
  never defined in the file. The sign law needs 2+r>0 and 1+r+w>0; for r ≤ -2,
  (2+r)_n changes sign or vanishes with n. A characterization claimed
  "complete" must state its domain as an explicit set.
- **E4 (underived condition, claim 4).** The condition "not(r=-1/2 and w<0)"
  is not derivable from the ladder theorem as presented: at r=-1/2 with
  w ∈ (-3/2,-1/2) the prefactor flips (1+r+w<0) and hand-checking a_{1,0} =
  K·w·(3/2+w)/((3/2)(1/2+w)) gives a POSITIVE value, so neither the n≤5 block
  nor the (positive-prefactor) ladder law obviously excludes such points. Some
  other constraint must do the killing; the file must identify it or mark this
  clause empirical.
- No algebraic error found in claims 1–3.

## COUNTEREXAMPLE ATTEMPTS

1. **Independent re-derivation of the claim-3 bracket (strongest attack —
   failed, claim upgraded).** Reviewer re-derived a_{n,n-2} from scratch:
   x^{n-2} coefficient of p((n/2)(x-1)) is (n/2)^{n-2}[n³(n-1)/8 − A·n(n-1)/2 + B]
   (B = second elementary symmetric of the roots), plus the x^n feed-through
   with rho = I(n,n-2)/I(n-2,n-2) = n(n-1)/(2(2n-1)) (verified from the
   standard integral ∫x^j P_m dx at n=3: 3/5 ✓ and n=4: 6/7 ✓). Matching the
   claimed bracket H = 12(2n-1)(1+r)(nr+2w)+n(n²+5n-2) monomial by monomial
   over {1, r, r², w, rw} (both sides contain exactly these) fixes the constant
   C(n)=24(2n-1)/(n-1) from the w-coefficient; r, r², rw coefficients then
   match identically; the remaining constant-term identity
   (2n-1)(n-1)(n-2)(3n-4)(n-3) − 6n(2n-1)(n-1)²(n-2) + 6n⁴(n-1) − 24(2n-1)(n-1)²
   = n(n-1)(n²+5n-2)
   has cancelling degree-5 terms (6−12+6 = 0), leaving degree ≤ 4 on both
   sides, and was verified exactly at n = 3 (132), 4 (408), 5 (960), 6 (1920),
   7 (3444), 10 (13320) — six points > deg 4 + 1, so it is an identity.
   **Claim 3 is therefore proven for all n, not just checked to n=8.** Full
   closed form: a_{n,n-2} = pref · (2n-3)/2 · I(n-2,n-2) · (n/2)^{n-2} ·
   (n-1)/(24(2n-1)) · H (encoded as `cf_nn2` in the attack script for machine
   confirmation).
2. **Parity-leakage attack on the Legendre step (failed).** Tried to find a
   monomial of p(t(x)) that feeds P_{n-1} besides x^{n-1} (the substitution
   (x-1)^k generates ALL powers, so this looked like the weakest link). Every
   candidate is killed by parity (x^n, x^{n-2}, ...) or by degree
   (x^{n-3}, x^{n-5}, ...). The argument is airtight and even mu0-independent.
3. **Prefactor/domain attacks (blocked by stated domain, one gap logged).**
   (i) 1+r+w<0 flips the prefactor: the closed form (first display) remains an
   exact identity; the simplified sign law is explicitly restricted to
   1+r+w>0 — no overreach in the claim text. (ii) r<-2 makes (2+r)_n
   sign-indefinite: again outside the stated domain, but exposed E3 (claim 4
   never defines its domain). (iii) Machine razors at large n (40), on-edge
   w<0, and the prefactor-flip region are queued in ATTACK 1.
4. **alpha<0 / mu0 near n/3 attack (blocked by design, edge case logged).**
   For n<3mu0 with n-1 odd the naive sign law is genuinely wrong (alpha^{n-1}<0),
   but all such n are strictly below threshold where positivity is not imposed
   — the claim's n>3mu0 restriction is exactly right. Found the unstated
   identically-zero case n=3mu0 (E2). ATTACK 4 exercises this numerically.
5. **Circularity attack on the mu0 generalization (partially succeeded → E1).**
   Checked what the "validated two-route evaluator" actually validated: all
   frozen spot checks are mu0=0. The mu0≠0 razor "verification" is therefore
   not currently backed by an independent route. This does not exhibit a false
   statement, but it removes the claimed independent support for claim 2 until
   ATTACK 3 is run.
6. **Claim-4 interior probe (prepared, unrun).** Points passing the n≤5 block
   and ladder condition but sitting near constraint boundaries
   ((-0.49, 0.1); (-1/2, 1/20); just inside the a_{2,0}=0 curve) scanned for
   negative a_{n,l}, l≤n-2, n=6..25 — any hit falsifies claim 4 (ATTACK 5).
   Also re-derived the printed a_{2,0} curve by hand: b_0 core = r²+rw+r+w+1/3
   = [3(1+r)(r+w)+1]/3 ✓ exact match; a_{3,0} curve delegated to ATTACK 6.
7. **Internal-consistency arithmetic (passed).** Razor zero predictions:
   mu0=3/5: -n/50+2/5=0 → n=20 ✓; mu0=-3/5: -n/20+3/4=0 → n=15 ✓;
   r=-3/5 kill list n=10w+1 for w=1..9/5 → [11,10]..[19,18] ✓; 6+60=66 points ✓.

## OVERCLAIM CHECK

- Status line (lines 3–6) is exemplary: "do not promote beyond analytic
  derivation, numerically confirmed", review flagged as pending. Good.
- **Line 104 header "COMPLETE CHARACTERIZATION" (caps)** overstates a
  conjecture; the honest label sits 18 lines lower. Rename to "Conjectured
  characterization".
- **Corollary 2, "The island's true left edge at mu0=0 is r = -1/2"**: only
  half analytic. Exclusion of r<-1/2 (w>0) is proven; that the island actually
  extends to r=-1/2+eps (i.e., that nothing else pushes the edge rightward) is
  empirical-only (depth 80). Should read "analytic exclusion bound r ≤ -1/2;
  attainment of the bound is empirical."
- **Line 74 "(added same day, verified)"** for the mu0 generalization: with E1,
  "verified" is too strong — currently "spot-checked at 2 razor points, route
  unspecified". Same for line 85's bolded edge formula at general mu0.
- "3780/3780, zero mismatches" is fine as stated (grid-verified, finite depth),
  and the l≤n-2 assumption is explicitly flagged — good.
- No banned words ("discovered/proved/novel/confirmed") misused; "QED
  (elementary)" on claim 1 is acceptable given the derivation is genuinely
  complete modulo the Eq. 16 provenance condition.

## REQUIRED FIXES

1. **Run the attack script** (`attack_left_edge.py`, path in header) with the
   project venv and attach its output; exit code 0 required. It machine-checks:
   exact closed forms for claims 1–3 (incl. large n, prefactor flips, off-domain
   algebra), claim-3 razors adjacent to the bracket's zero curve, and the
   claim-4 interior probe to n=25. (Reviewer could not execute code this
   session.)
2. **Close E1**: add mu0≠0 cases to the frozen spot checks of
   `repro_r4_positivity_spot.py` (or record an equivalent route1-vs-route2 run
   at mu0=±3/5 incl. the razor zeros via route 1). Until then, claim 2 must
   not be described as resting on a "validated" evaluator.
3. **State the n=3mu0 degenerate case** (E2): a_{n,n-1} ≡ 0 there; sign formula
   applies only for n>3mu0, strictly.
4. **Define the domain** used in claims 1 and 4 as an explicit set
   (2+r>0 and 1+r+w>0, or whatever is intended), and define "domain pole" (E3).
5. **Justify or relabel the "not(r=-1/2 and w<0)" clause** (E4): identify the
   constraint that excludes r=-1/2, w∈(-3/2,-1/2), or mark the clause empirical.
6. **Wording**: rename the claim-4 header to "Conjectured characterization";
   split Corollary 2 into analytic bound vs empirical attainment; replace
   "verified" (line 74) per the Overclaim check.
7. **Optional upgrade**: adopt the reviewer's all-n proof of the claim-3
   bracket (Counterexample attempt 1) — it converts "positive constant checked
   n=3..8" into a theorem, and the explicit C(n) is in `cf_nn2`.

Verdict summary: claims 1 and 3 sound (claim 3 now provable for all n);
claim 2 sound-but-underdetermined pending E1; claim 4 a properly disclosed
conjecture with two bookkeeping gaps (E3, E4) and one header-level overclaim.
