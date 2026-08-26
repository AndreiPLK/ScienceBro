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

**Remaining for the odd-depth chain:** depth 5 with the same machinery (was
running at handover time -- check `results/odd_depth_kwindow_cert_d5.json`,
rerun `python lab/odd_depth_kwindow_cert.py 5` if absent); a 2-variable
certificate for the odd-depth `lam in [5/2, 7]` band at fixed `k_s = 8`
(currently measured: 1085 trials, 0 negatives); unimodality of `dT/dk` on
the window (measured, not proved); step (b)'s bracketing theorem already
places the argmin within `|delta| < 1` for `lam >= 7`.

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
