# HANDOVER — read this first

Last updated: 2026-08-24 17:08 (from `date`, not memory).

## The goal

Make a discovery that enters science under Andrei Pluzhnik's name. Everything
else -- tools, provers, certificates -- is means.

The active target is the **keystone theorem** of the quantum-gravity S-matrix
bootstrap: prove that an infinite family of positivity constraints ("knives",
indexed by DEPTH `d`) holds for the CHR graviton family, with ONE argument
covering every depth rather than a per-depth ladder.

Read next, in this order:
1. `projects/qg-bootstrap/results/UNGLUED_KEYSTONE.md` -- the whole argument
   (read its 24 Aug correction at the bottom)
2. `docs/ERRATA.md` ERR-0013 -- 24 Aug: the odd-depth diagnosis was WRONG,
   the fixed-window statement is FALSE at odd depths, and the repair route
3. `projects/qg-bootstrap/results/ODD_DEPTH_DIAGNOSIS.md` -- the old
   diagnosis plus its correction (kept visible per the evidence contract)
4. `docs/ERRATA.md` ERR-0010 .. ERR-0012 -- three bugs from 19 Aug, all
   instructive
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

## The j-infinity front (28 Aug) -- where the real work now is

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

**Next, in order of promise:** (a) the ASYMPTOTIC route -- since the
tightness grows with `n`, expand `K_r` around the scaling limit, whose
leading behaviour is known in closed form (`results/SCALING_LIMIT_THEOREM.md`),
and control the correction uniformly in `j`; (b) check the kernel identity
against the binomial-determinant literature (Krattenthaler, *Advanced
Determinant Calculus*) before any novelty wording; (c) inject the shore
condition EARLIER -- every route so far imposes `D <= T_hat` only at the
end, while the measured control shows the bound failing exactly when the
physics does, so the shore may belong inside the representation itself.

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
