# Dead routes

*Read this before proposing a proof route. A route here does not come back under new
wording unless you can say which mathematical assumption changed.*

Each entry records the exact statement that died, why it was tempting, what killed it,
whether the failure is local or structural, whether a weaker variant survives, and the
lesson. The lesson is the part that pays: most of these were killed by a test written
next to the idea, and the ones that were not cost days.

---

## DR-01 — A positive-measure representation for the second log difference

**Statement.** `A_t = -Delta^2 log p_t` is a moment sequence of a positive measure, so
the whole hierarchy `Delta^r log p_t < 0` follows from one representation.
*(registry: `CLAIM-MOMENT`)*

**Why it was tempting.** It would have explained the entire observed hierarchy at once,
and with it conjecture (B), from a single structural fact. It was proposed as the
"potential jackpot" of the anomaly-map brief.

**What killed it.** Hankel positivity is necessary for any such representation, and it
fails: a negative leading minor at order 4 forward and order 5 to 9 reversed, at every
`n` from 21 to 101. `A` is transcendental, so it was rationalised to 300 digits and the
determinants evaluated exactly over `Q`; every decisive minor clears its rigorous error
bound by more than 200 orders of magnitude.

**Local or structural.** Structural, and in both orientations. A separate one-line
argument had already excluded the un-reversed Hausdorff form: the hierarchy makes `A`
ABSOLUTELY monotone, hence a moment sequence on `[1, infinity)`, while a Hausdorff
sequence on `[0,1]` decreases.

**Weaker variant that survives.** The hierarchy itself is intact (0 violations,
`r = 2..8`, window inside the first half). Only its most attractive explanation is
gone. Total positivity, an LGV path model, a minor identity, or a sign-carrying
recurrence remain.

**Lesson.** The first negative order GROWS with `n` (4,4,4,5,5,6 forward). A check that
looked only at low orders and large `n` would have concluded the opposite.

---

## DR-02 — Harmonic additivity of the log-concavity excess

**Statement.** `1/L_{X+Y} >= 1/L_X + 1/L_Y` for independent sums, `L` the log-concavity
excess, matched at a common tilt. *(registry: `CLAIM-HARMONIC`)*

**Why it was tempting.** `L ~ 1/sigma^2` and variances add, so this would have given
the UPPER bound on the excess that real-rootedness alone cannot give.

**What killed it.** In the regime where the idea can apply at all — 30 to 70 summands a
side — the inequality goes uniformly the other way: 120 of 120. `1/L` is subadditive.

**Local or structural.** Structural, and explicable: `1/L = sigma^2 (1 - c/n + ...)`
and `sigma^2` is exactly additive, so the measured defect IS the Edgeworth correction.

**Weaker variant that survives.** Subadditivity itself, which bounds the excess from
below — the direction Newton already supplies, so it buys nothing.

**Lesson.** Two of my own tests of this were meaningless before the third was right:
matching arbitrary point pairs instead of a common tilt, and testing at 4-10 summands
where the excess is ~0.6 rather than ~1/sigma^2. An idea must be killed in its own
regime.

---

## DR-03 — General preservation of ratio log-concavity under self-convolution

**Statement.** Hypergeometric self-convolution carries ratio log-concavity from any RLC
input to its output.

**Why it was tempting.** It is the clean form of the AP-square brief's Problem 2 and
would close the physical case, since the physical `p_t` is exactly such a
self-convolution of the half spectrum.

**What killed it.** 1561 of 2800 general RLC inputs, constructed rather than filtered,
map to non-RLC outputs.

**Local or structural.** Structural for the general statement.

**Weaker variant that survives, and it is the useful one.** Restricted to real-rooted
inputs it held in 1409 of 1409 cases, including the 174 nearest to breaking. That is
`CLAIM-P`, and real-rootedness — not RLC — is the load-bearing hypothesis.

**Lesson.** Ask whether a preservation theorem can exist before trying to prove one.
Half an hour of exact computation replaced a week of a doomed approach.

---

## DR-04 — "Criterion S" (ERR-0015)

**Statement.** A criterion for knife positivity whose induction started from `A_r = 1`.

**What killed it.** Its hypothesis contained its conclusion: `A_0 = K_r`. Circular.

**Lesson.** Write out what each symbol in an induction actually equals at the base
before trusting the step.

---

## DR-05 — "Odd-j knives never dip" (ERR-0016)

**What killed it.** They do: 72 cases, reproduced on both engines.

**Lesson.** A claim that prunes a search must keep being sampled inside the pruned
branch.

---

## DR-06 — The depth law `j <= n/2 + 1` (ERR-0017)

**What killed it.** It was fitted on `n = 12,16,20,24,28,36,44` — every one a multiple
of four. Over `n = 11..100` it fails in 70 of 90 rows.

**Local or structural.** The law is simply false off the sub-grid it was fitted on.

**Lesson.** This was the SECOND time this lab was bitten by a sub-grid, after the even-j
retraction of 18 August. Before recording a law, check that the sample can distinguish
it from its nearest rival.

---

## DR-07 — "The dominant term wins"

**What killed it.** The rest exceeds the dominant term by factors from 3 to 3.2e8.

**Lesson.** Measure the neglected part before neglecting it.

---

## DR-08 — Real-rootedness routes to an upper bound on the Newton excess

**Statement.** Some theorem depending only on real-rootedness bounds
`e_t^2/(e_{t-1} e_{t+1})` from above.

**What killed it.** No such theorem can exist: for real-rooted polynomials with widely
spread roots the excess is unbounded. Any upper bound must use the specific spectrum.

**Lesson.** Recorded because it explains why several attractive general tools — Newton,
Maclaurin, Muirhead — are structurally unable to give what the programme needs, and
saves re-deriving that each time.

---

## DR-09 — Total positivity / LGV as the mechanism behind the hierarchy

**Statement.** The log-difference hierarchy follows from total positivity of the
sequence, provable by a planar-network / Lindström-Gessel-Viennot argument.

**Why it was tempting.** It was the leading surviving candidate after the moment route
died, it is the standard machinery for exactly this kind of sign statement, and the
underlying polynomial genuinely IS real-rooted.

**What killed it.** The two properties are complementary. The raw `e_t` is a Polya
frequency sequence — as Aissen-Schoenberg-Whitney requires, and the positive control
confirms — and it does NOT satisfy the hierarchy. The normalised `p_t = e_t/C(N,t)` DOES
satisfy the hierarchy and is NOT a PF sequence: an explicit negative 3x3 Toeplitz minor
at rows (1,2,3), columns (0,1,2), at every `n` tested (`-40832/15` at n=11, `-106240/7`
at n=15, `-1384592/15` at n=21).

**Local or structural.** Structural, and now PROVED rather than measured: the minor has
the closed form `-(4/945) n(n+1)(7n^3-43n^2+58n+120)`, strictly negative for every
`n >= 4` (`CLAIM-NOPF`, `THEOREM_NO_POLYA_FREQUENCY.md`). An LGV argument proves things
about the totally positive object, and the totally positive object is not the one with
the hierarchy.

**Weaker variant that survives.** A determinant or minor identity for `H_{N,t}` AFTER
clearing the binomial denominators is a different object and is not excluded. The finite
free / S-transform reading lives in normalised coordinates and is on the correct side of
the division.

**Lesson.** The binomial normalisation is not cosmetic: it destroys one structure and
creates the other. Before importing machinery, check WHICH of the two sequences the
machinery actually applies to.

---

## DR-10 — The Jacobi-Stirling special parameters as the explanation

**Statement.** The hierarchy is a phenomenon of the special parameters `z = 0, 1` in the
deformation `j^2 -> j(j+z)`, where the physical parities sit.

**Why it was tempting.** Both physical parities land exactly on those values, and the
literature marks them as a distinguished Polya-frequency boundary.

**What killed it.** The hierarchy holds at every tested `z` from `-1/2` to `10`, with no
failing order anywhere. `z = 0` and `z = 1` are deep interior points of the region where
it holds, not a boundary.

**Local or structural.** Structural: the phenomenon is much more robust than the
special parameters, so no explanation resting on their specialness can be right.

**Weaker variant that survives.** The special parameters may still matter for the
STRENGTH of the inequality or for exact identities, just not for the sign itself. Worth
measuring the margin as a function of `z` rather than the sign.
