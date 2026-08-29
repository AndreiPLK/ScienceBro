# HANDOVER — read this first

Last updated: 2026-08-29 16:07 local (from `date`, not memory).

## Starting a new session from scratch

Everything is in git; nothing lives only in a chat. To continue:

```
git checkout claude/handoff-markdown-review-anzwo5   # the working branch
uv sync && uv run sb check                           # must print: sb check passed
```

Read this file, then `article/DATA_LOG.md` from the bottom up (newest entries
first) — it is the running record of what was tried, what was banked and what
was killed, and it is the only place the reasoning behind a dead end survives.
`docs/ERRATA.md` holds every error found so far, newest last. Chat context does
NOT carry over between sessions and is not meant to; these files do.

## The goal

Make a discovery that enters science under Andrei Pluzhnik's name. Everything
else -- tools, provers, certificates -- is means.

The active target is the **keystone theorem** of the quantum-gravity S-matrix
bootstrap: prove that an infinite family of positivity constraints ("knives",
indexed by DEPTH `d`) holds for the CHR graviton family, with ONE argument
covering every depth rather than a per-depth ladder.

Read next, in this order:
1. **`projects/qg-bootstrap/results/FARBELOW_NEGATIVE_PATTERN.md` and
   `results/FFP_LITERATURE_PASS.md` -- the CURRENT front (29 Aug), summarised in
   the 29 Aug section below.**
2. `projects/qg-bootstrap/results/BFORM_POSITIVITY_THEOREM.md` (28 Aug). Theorems 1-9, both proved regions, both review passes, and
   the honest limits in sec. 6, 6b, 6c. Start here; the sections below on the
   odd-depth chain are finished work, not open work.
2. `projects/qg-bootstrap/results/BFORM_CRITIQUE.md` -- the domain-critic pass
   on it, including where it says the result is oversold
3. `docs/ERRATA.md` ERR-0014 -- two arithmetic slips of mine in those write-ups,
   found by BOTH review passes; then ERR-0013 (the odd-depth statement is FALSE)
   and ERR-0010..ERR-0012 (three bugs from 19 Aug, all instructive)
4. `projects/qg-bootstrap/results/UNGLUED_KEYSTONE.md` -- the older three-step
   argument (read its 24 Aug correction at the bottom)
5. `NORTH_STAR.md` and `CLAUDE.md` -- standing law

## Where we are

The argument has three steps. Status of each, from the artefacts:

| step | what it says | status |
|---|---|---|
| (a) | knife positive at `D = T_v(lam)` for all real `v` in `[8/5, 2]` | **certified** at depths 2, 4, 6 (all four pieces, both parities, 0 open boxes); **FALSE at odd depths** (ERR-0013) -- odd depths need the k-window form |
| (b) | apply it at an INTEGER `k_s` in that window, where `T_hat <= T_{k_s}` holds by definition | **PROVED** for `lam >= 7`; two finite bands below it covered by fixed levels (`k_s=4` under 5/2, `k_s=8` on `[5/2,7]`) |
| (c) | knife decreases in `D`, carrying positivity down the physical interval | **certified** at depths 2-6 |

Artefacts, which are the only thing to trust:
- `projects/qg-bootstrap/results/keystone_unglued.json` -> depths 2, 4, 6 true
- `projects/qg-bootstrap/results/monotonicity_cert.json` -> depths 2-6 true

## The one thing blocking progress

**Odd depths 3 and 5 do not close -- because at odd depths the statement is
FALSE (found 24 Aug, ERR-0013).** The 21 Aug cancellation diagnosis is
retracted: margins have no parity structure (depth 4 is 25x worse-conditioned
than 3 and certifies). The truth: odd depth = even knife order `j = d+1`, and
even-j knives HAVE thresholds; away from the argmin of `T_k` the window point
`T_{v*lam}` overshoots them at large `lam`. Exact two-engine witnesses from
`K=54` (depth 3) / `K=111` (depth 5): `results/odd_depth_window_refuted.json`.
The physics is intact -- the knife is positive at the true shore `T_hat` at
every witness. Do NOT retry SOS/factorisation/subdivision on the old
statement: it is false, not ill-conditioned.

**The repair is BUILT and CERTIFIED at depth 3 (26 Aug).** The k-window form
-- knife positive at `D = T_{k+delta}(lam*(k))` along the critical curve
`dT/dk = 0`, `|delta| <= 9/8` -- is certified for BOTH parities at depth 3:
`results/odd_depth_kwindow_cert_d3.json`, 1 + 11 boxes per parity, 0 open,
covering ALL `K >= 3` and ALL `k >= 12` (no finite-coverage caveat). The
constructor (`lab/odd_depth_kwindow.py`) is validated by substitution and a
non-vacuous self-check (0/296 mismatches per depth, depths 3 and 5); the
certifier (`lab/odd_depth_kwindow_cert.py`) works in `rho = k/(2K)`
coordinates -- the (K, k) double-infinity corner is the UNGLUED two-variable
degeneration again, and `rho` makes it an ordinary point (piece 1 closes in
ONE box). Lesson pair: delta-slack you do not need is surface you cannot
defend (3/2 jammed, 9/8 closes); a jammed certificate means false statement
OR wrong coordinates -- measure which.

**The odd-depth chain is CLOSED for depths 3 and 5 (26 Aug).** Certified:
depth 5 k-window (`results/odd_depth_kwindow_cert_d5.json`, 1 + 11 boxes per
parity, 0 open, same as depth 3); the `lam in [5/2, 7]` band at `k_s = 8`
(`results/odd_depth_band_cert.json`, both depths); unimodality via strict
convexity of `T` in `k` on the window (`results/unimodality_cert.json`, ONE
box, replacing the 400-point sweep premise of step (b)). With
keystone_unglued's small piece (`k_s = 4`, `lam <= 5/2`) and step (c)
monotonicity (depths 2-6), nothing in the depth-3/5 chain rests on a
measurement any more. The certifier survived the process-killing environment
via G/Gw caches keyed by the constructor sha256, per-piece frontier
checkpoints with resume, and fmpq_mat matrix engines -- every change
regression-gated on depth 3's exact box counts.

**Depth 7 is closed as compute-bound here, not as mathematics** (28 Aug):
one grid split costs 19 s, restoring a frontier box ~230 s, and the
container kills processes at ~180 s, so it cannot advance regardless of
caching (banked: 24 boxes, 0 open). It was a uniformity test, never a link
in a proved chain. Unblocking options are in the DATA_LOG entry.

## The 29 Aug session — the literature pass, and where it led

Read `results/FFP_LITERATURE_PASS.md` and `results/FARBELOW_NEGATIVE_PATTERN.md`
before anything else on this front; `docs/ERRATA.md` ERR-0015 and ERR-0016 are
both from this day and both are mine.

**The transform is classical.** Multiplying `e_t` by a Pochhammer ratio is the
finite free multiplicative convolution, i.e. the **Schur–Szegő composition**
(arXiv:2309.10970 §1; preservation is Szegő 1922 / Walsh 1922). Identified
exactly: `K_r = (p BOX_{n-1} q)(1)`, 336 cases, 0 mismatches, 65 with a negative
reference knife. Novelty of the technique: POSSIBLY_KNOWN -> **KNOWN**. The route
it opened is closed too: `q` has complex zeros in 336 of 336 cases, so the
Szegő–Walsh preservation theorem does not apply.

**The diagonal identity.** `A_m = C(r,m) K_{r-m}` at `D -> D-2m` (1696 checks, 0
mismatches): the Taylor coefficients of the knife polynomial at `x = 1` are
knives of lower depth at lower dimension. With step (c) this makes positivity
below the shore ONE scalar inequality, `D_cross >= T_hat`, verified in 120 of 120
rows, monotonicity 0 violations in 1920 steps. It is also TIGHT — worst ratio
1.008 — so no bound that spends a constant factor can close it. Five such bounds
died today with numbers: Fujiwara/Cauchy (2.8-49), Grace–Szegő–Walsh product
(2-7.7), plus the three already in the J-form entry.

**The live front: uniformity in depth, and it finally has an address.** The
far-below criterion (`knife_farbelow2`) proves knives 4..8 by manifest positivity
and breaks at `j = 9`. Every negative monomial — 11 at `j=9`, 30 at `j=10`, 41 at
`j=11` — sits in ONE `y`-coefficient, the one of degree `J-2`, at `thL = K3 = 0`.
Closed form for it verified (`j=6`: 735 monomials, `j=9`: 1752, 0 mismatches),
and the general-`k` formula verified at every `k` for `j=6`. The reason that
coefficient and no other: it is a difference of two terms equal to within a
percent (ratio 0.9997-1.0164 measured), while every other `c_k` is a longer sum.

**The candidate repair, measured at one depth only:** where `c_{J-2} < 0`, the
neighbours absorb it iff `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`. At `j = 9`, over 512
region points, 6 have `c_{J-2} < 0` and all 6 satisfy it — and the stronger
log-concave form too. `j = 10, 11` were queued. **Do not quote this as more than
one depth until those land.**

**Three corrections of my own claims, same day, same failure mode** — read
`docs/ERRATA.md` 0015-0017 together, they are one lesson:
* ERR-0015: "criterion S" had its conclusion inside its hypothesis;
* ERR-0016: "odd-`j` knives never dip" — they do, at small `lam`, 72 cases;
* ERR-0017: the depth law `j <= n/2+1` was fitted on a sample of multiples of 4
  and fails in 31 of 51 cases over `n = 11..61` (`results/depth_boundary_map.json`).
The rule that came out of it, saved to memory: before recording a law, check the
sample can distinguish it from its nearest rival — and if a claim PRUNES a
search, keep sampling the pruned branch.

**WHERE 29 AUGUST ENDED — the far-below front now stands on proofs.**

The far-below criterion (`knife_farbelow2`) proves knife positivity by manifest
positivity and fails from `j = 9`. It fails narrowly and in one place, and that
place is now repaired:

* **the failure is one coefficient.** Every negative monomial sits in the
  `y`-coefficient of degree `J-2` — measured at `j = 9..15` (11, 30, 41, 71, 96,
  130, 165 of them), always that one;
* **the repair is certified.** Grouping it with its neighbours reduces positivity
  to `(R) 4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0`, which is UNCONDITIONAL (holds at
  all 504 region points, not just the 117 dips) and **certified at `J` = 7, 9, 12, 16, 20,
  25-32, 35, 40, 50** — monomial signs to 29, in-regime monomial signs at 30, one
  Bernstein step in `thL` from 31 on, with no depth failing (`results/repair_certificate_j*.json`);
* **together they close `j = 9..15`** by manifest positivity plus one grouping,
  where the programme previously needed the interval-Bernstein route. The two legs
  are checked on the same set for `j <= 23`; beyond that only on the intersection.

**What is still measured, not proved:** that every `c_k` with `k != J-2` is
nonnegative. It holds on 1476 points tested on BOTH sides of its boundary, and the
boundary is `n >= 2J-3` (`results/farbelow_regime_map.json`).

**The road to depth-uniformity, and how much of it is built.** A `J`-uniform (R)
reduces to two statements. One is now **proved twice** — by a one-line cancellation
here and independently by the parallel chat. The other is a lemma about the
central factorial family, `p_t^2/(p_{t-1}p_{t+1}) <= 1 + 2/n`, and it has been
taken apart:

* its **asymptotic half is proved** (`results/LIMIT_SHAPE_BOUND.md`): the limit
  shape is `f(theta) = (2/u)/(dtheta/du) - 1/theta - 1/(1-theta)` with
  `theta = 1 - arctan(u)/u`, and `f < 2` on `(0, 1/2)`. That proof came from the
  parallel chat and needed one repair: its factorisation had `(z-1)` where the
  quartic has `z = 1` as a DOUBLE root;
* the **finite-`n` half** (`results/FINITE_N_BRIDGE.md`) rests on an exact
  recursion `e_t(n+2) = e_t(n) + 2n^2 e_{t-1}(n) + n^4 e_{t-2}(n)` — today's
  doubling, read as a step in `n` — plus two statements (B) and (C). With both,
  everything reduces to two computed numbers, `M_{44,21} = 1.8393` and
  `M_{45,22} = 1.8860`, against the 2 allowed;
* **(B) is now a theorem for every `t <= 100`**, hence for the whole needed range
  at every `n <= 200`. At fixed `t` it is one polynomial inequality in `n`, and
  `lab/conjecture_B_rungs.py` proves each rung by the same
  all-nonnegative-coefficients move (degrees 22 to 1606, zero failures). What is
  owed is only uniformity in `t`: that the shift `n = m + 2t` works for EVERY `t`;
* **(C) is open, and it is not locally derivable** — synthetic five-term windows
  fed through the recursion violate it under Newton (233/400), under Newton + (B)
  (25/600), and even inside the near-extremal band (865/2714). A proof must use
  the global structure: squares of an arithmetic progression have the Gamma-ratio
  generating function `PROD (1+(a+k)^2 z) = z^N Gamma-ratios at conjugate
  arguments`, verified exactly.

**A structural fact found on the way, absent from the repository before:** the
B-form's multiset is DOUBLED — `b_{n-k} = b_k` — so `prod_k (u - b_k)` is a perfect
square times at most one linear factor, and `E_{2t}` is the self-convolution of a
half-set of `floor(n/2)` distinct values (`results/DOUBLED_MULTISET.md`). My
hypothesis that this explains the half-depth boundaries was refuted the same hour
by the control written beside it.

**Refuted the same day, do not retry:** "the highest-`s` term dominates". Measured
`rest/dominant` = 3 to 3.2e8 (`results/dominant_term_probe.json`). The terms are
comparable in size; positivity is cancellation, not dominance.

## The j-infinity front (28 Aug)

An outside report (`research/reading-notes/keystone-outside-report-2026-08-28.pdf`,
answering our `research/BRIEF_KEYSTONE_FOR_OUTSIDE_HELP.md`) proposed
reorganizing the exact knife sum into an alternating binomial transform.
Same-day exact testing produced:

1. **A THEOREM (`results/KERNEL_TP_THEOREM.md`).** The depth kernel
   `B_{r,t} = C(r,t)(H-r)_t t!` has every solid `q x q` minor equal to
   `prod_a (H-r0-a)_{t0} * prod_a (r0+a)_{t0} * prod_{a<b}(b-a)(H-2r0-a-b)`
   -- proved by one quadratic substitution `z = y^2 - Hy` turning the
   matrix into a generalized Vandermonde; verified including the constant,
   86/86. Every root is `<= 2 r_max - 1 < H` on the physical domain, so the
   kernel is STRICTLY TOTALLY POSITIVE there. First uniform-in-depth
   theorem of the programme.
2. **The Charlier reduction (`results/charlier_reduction.json`).**
   `M_t^(r) = (H-r)_t m_t` with `m_t` independent of `r` and `D`, and
   `sum_t C(r,t)(g)_t(-y)^t = C_r(g;1/y)` is a Charlier polynomial
   (verified against its three-term recurrence). So a moment representation
   of `m` would give `K_r = INT C_r(H-r;1/y) dmu(y)`.
3. **Two exact kills.** The report's Hausdorff hypothesis for `M_t^(r)` is
   refuted (it quantifies over `r` while the sequence moves with `r`); and
   my own crude sufficient condition -- `P_r >= 0` on the measure's support
   -- is refuted too, the smallest zero sitting at 0.63-1.06 of a support
   lower bound (`results/charlier_zero_test.json`).
4. **A measured regime.** `m_t` IS a Hausdorff moment sequence for
   `t <~ n/2` and fails beyond, with the boundary INDEPENDENT of `lam` over
   five orders of magnitude -- so that failure is intrinsic to the central
   factorial numbers `E_{2t}(n)`.

5. **The mechanism, quantified (`results/measure_mass_test.json`).** The
   measure was extracted by exact-moment Gaussian quadrature (certified
   nodes, acb weights, and BOTH verifications -- moments and `K_r`
   reproduced -- in all 54 rows). `K_r > 0` holds not because `P_r >= 0`
   (up to 98% of the mass sits where `P_r < 0`) but because the negative
   contribution is a bounded fraction of the positive one. Control: above
   the shore that fraction exceeds 1 in 9 of 9 negative-knife rows, so the
   diagnostic tracks the physics.
6. **But the constant is not uniform (`results/cancellation_bound_sweep.json`).**
   Widening to `n <= 40`, `j <= 12`, five orders of `lam`: the ratio peaks
   at INTERMEDIATE depth (0.954 at `j = 14`, `n = 40`, falling to 0.54 by
   `j = 24`) and the peak GROWS with the level -- 0.68, 0.80, 0.89, 0.95 at
   `n = 14, 20, 28, 40`. So "sup c < 1 uniformly" is in doubt: the object is
   asymptotically tight in `n`.
7. **Three constant-free routes refuted (`results/pairing_structures_probe.json`).**
   Adjacent pairing (1/9), nonnegative partial sums (5/9 left, 1/9 right --
   the variation-diminishing shape the kernel TP theorem would have fed) and
   a Leibniz alternating tail (6/9) all fail. Only a restatement of the
   ratio survives: the head block at the smallest nodes beats the tail,
   `|tail|/head` in 0.00-0.79.

**The J-form split is exhausted — three dead ends, all measured, do not retry
them.** (1) The triangle inequality on `[0, eta]` is WORSE by up to 21.7x
(dropping signs destroys the cancellation). (2) A per-instance certified
quadrature is CIRCULAR: the sign of the integral is the sign of `K_r`, already
computed exactly, so only an all-`n` bound can add anything. (3) Replacing the
crude envelope by the TRUE envelope `max_{[0,eta]}|prod (w-eta_i)|` — which is
scale-invariant and genuinely tiny, about `2.4^{-r}` — moves the threshold only
1.1x, because `NEG ~ lam^{-(2n-1)}` means a gain of `G` buys `G^{1/(2n-1)}`.
**No constant, and no factor exponential in `r`, can move this threshold.**
Reaching `lam ~ 2n` needs a different decomposition, not a better bound inside
this one.

**Where the shore belongs, at last.** The weight is `Beta(a, b)` with
`b = D/2 + (n-2-r)`, so raising `D` slides its mass toward `w = 0` where the
roots sit; `mean(W)/eta_max` climbs `0.04 -> 1.00` over `lam = 30..2000` at
`n = 20, r = 18`. The shore condition is not an afterthought in this
representation — it is the statement that the weight's mass stays clear of the
roots. That is the "inject the shore earlier" question the programme has carried
for weeks, answered.

**Older next-steps, still open:** (a) the ASYMPTOTIC route -- since the
tightness grows with `n`, expand `K_r` around the scaling limit, whose
leading behaviour is known in closed form (`results/SCALING_LIMIT_THEOREM.md`),
and control the correction uniformly in `j`; (b) check the kernel identity
against the binomial-determinant literature (Krattenthaler, *Advanced
Determinant Calculus*) before any novelty wording; (c) inject the shore
condition EARLIER -- every route so far imposes `D <= T_hat` only at the
end, while the measured control shows the bound failing exactly when the
physics does, so the shore may belong inside the representation itself.

## The B-form (28 Aug) — the first PROVED all-depths positivity

Two elementary moves on the exact knife sum change its character. `C(r,t) t!`
is the falling factorial `(r)_t`, and `E_{2t}(n)/s^{2t}` is by definition
`e_t(b)` with `b_k = (n-2k)^2/s^2`. So

    K_r = sum_t (-1)^t c_t e_t(b),   c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t].

Every `b_k` is `< 1` for every `lam > 0` (`max_k b_k = (n-2)^2/s^2`), and `c_t`
carries no `lam` at all. Leibniz on `T_t = c_t e_t(b)` is uniform in depth, and
Newton's inequalities (the `b`'s are nonnegative, so `prod (1 + b_k x)` is
real-rooted) collapse the whole criterion to ONE inequality, worst at `r = n-2`:

    D <= D*(n, lam) = (6n-9) s^2 / (n (n-2)^2) - 2n + 3
      ==>  every knife positive, every depth, no computer search.

Then the same object, handled better. Substituting `w = 1-v` turns the
derivative form's integral over an unbounded ray into a COMPACT one — a Jacobi
(Beta) moment of a real-rooted polynomial on `[0,1]`, all roots in `[0,B]`,
`B = (n-2)^2/s^2 < 1` — and splitting at the largest root gives a second proved
region, `lam ~> 32 n`, LINEAR in `n` (`lam/n` plateaus at 31.9 by `n = 420`
while `lam/(n ln n)` keeps falling).

**All of it is written up in `results/BFORM_POSITIVITY_THEOREM.md`** (Theorems
1-9, proofs, verification, honest limits), with
`lab/bform_positivity.py`, `lab/bform_derivative_form.py`,
`lab/bform_jacobi_bound.py`, `lab/bform_gap_diagnosis.py`.

**Both review passes are done and folded in** (the rule: never self-approved).
Independent validator: PASS, `validation/VAL-BFORM-0001.yaml` — rebuilt from the
reference engine alone, 13380 adversarial points with the hypothesis true, no
counterexample. Domain critic: `results/BFORM_CRITIQUE.md`. Between them they
found two real arithmetic slips of mine (ERR-0014) and three substantive
additions, now in the file.

**Read the honest limits before quoting any of this.** The region is a corner:
Theorem 6 is VACUOUS at `lam = 1, 5/2, 7` for `n >= 6` — the values the
project's own sweeps use. At fixed depth the threshold is linear in `n`
(`lam* ~ c r n`), which is a much better statement than the all-depths `3 n^2`.
Claim state: independently-validated for the MATHEMATICS, NOT for novelty — no
literature pass has been done and the critic would call the technique LIKELY
KNOWN (Polya-Schur multiplier sequences, Malo-Schur-Szego composition,
finite free probability).

## Outreach: how this project shows its work (founder, 28 Aug)

`outreach/shore_of_universes.html` — an interactive 3D explainer of the whole
problem, built for the founder's children and adopted by him as the house style
("we will share our work like this style and interactive"). The pattern is in
`docs/DECISIONS.md`: data exported from the SAME exact engine the certificates
use, every quoted number computed by the builder from that data, and the builder
refuses to emit the page if the data would falsify the page's central claim.
Live: https://claude.ai/code/artifact/7e16abf9-09a6-463b-822f-b1ebc5382bd8

## Also open, smaller

- step (c) leaves a sliver `[9*lam, gamma_shore]`, up to 5% of the interval
- coverage is finite in `K` (to ~3000), not literally all `K >= 3`
- prior art to cite before any preprint: our descent lemma is Schoenberg's
  dimension walk (Gneiting Thm 2(b),(c), arXiv:1111.7077)

## How to work here (learned the hard way, 19 Aug)

- **`date` at the start of every turn.** I once invented the timestamps in a
  shift report. I have no sense of time and no signal of not-knowing; any field
  I do not measure, I will fill with plausible text. See memory
  `timestamps-are-measurements`.
- **`ScheduleWakeup` at the end of every turn** while a loop is running, or the
  loop silently dies.
- **flint `fmpq` only.** No sympy, no float in an exact comparison. Enforced by
  `tests/test_fast_engine.py`.
- **A check that cannot fail is not a check.** ERR-0012: `build_wedge` shipped
  wrong because `self_check` never touched it AND because inside the window the
  reference sign is always +1, so a sign comparison there could not distinguish
  the intended polynomial from any positive one. `self_check_all` now probes
  outside the window and prints VACUOUS when it has proved nothing.
- **An independent verifier beats self-checking.** That bug survived my review,
  two commits and a night; it did not survive one Workflow graph of four agents
  told to disbelieve the prover. Use `Workflow` for anything substantial.
- **Machine rule:** check free memory before heavy runs; under 8 GB or a game
  running, do not launch. Do not run 16 agents at once -- that took memory to
  7.3 GB on 19 Aug.

## Commands

```
uv run sb check          # ruff + mypy + pytest + integrity
python lab/keystone_unglued.py <d>     # main argument, one depth
python lab/monotonicity_cert.py <d>    # step (c)
```
