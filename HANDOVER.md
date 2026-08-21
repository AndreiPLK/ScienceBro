# HANDOVER — read this first

Last updated: 2026-08-21 09:48 (from `date`, not memory).

## The goal

Make a discovery that enters science under Andrei Pluzhnik's name. Everything
else -- tools, provers, certificates -- is means.

The active target is the **keystone theorem** of the quantum-gravity S-matrix
bootstrap: prove that an infinite family of positivity constraints ("knives",
indexed by DEPTH `d`) holds for the CHR graviton family, with ONE argument
covering every depth rather than a per-depth ladder.

Read next, in this order:
1. `projects/qg-bootstrap/results/UNGLUED_KEYSTONE.md` -- the whole argument
2. `projects/qg-bootstrap/results/ODD_DEPTH_DIAGNOSIS.md` -- why we are stuck
3. `docs/ERRATA.md` ERR-0010 .. ERR-0012 -- three bugs from 19 Aug, all
   instructive
4. `NORTH_STAR.md` and `CLAUDE.md` -- standing law

## Where we are

The argument has three steps. Status of each, from the artefacts:

| step | what it says | status |
|---|---|---|
| (a) | knife positive at `D = T_v(lam)` for all real `v` in `[8/5, 2]` | **certified** at depths 2, 4, 6 (all four pieces, both parities, 0 open boxes) |
| (b) | apply it at an INTEGER `k_s` in that window, where `T_hat <= T_{k_s}` holds by definition | **PROVED** for `lam >= 7`; two finite bands below it covered by fixed levels (`k_s=4` under 5/2, `k_s=8` on `[5/2,7]`) |
| (c) | knife decreases in `D`, carrying positivity down the physical interval | **certified** at depths 2-6 |

Artefacts, which are the only thing to trust:
- `projects/qg-bootstrap/results/keystone_unglued.json` -> depths 2, 4, 6 true
- `projects/qg-bootstrap/results/monotonicity_cert.json` -> depths 2-6 true

## The one thing blocking progress

**Odd depths 3 and 5 do not close.** Even ones do. Diagnosed 21 Aug:

The polynomial is positive but its value at the hard corner is **7.8e-05** of
the largest single term being summed -- near-total cancellation. Bernstein
bounds a polynomial by its coefficients, so it cannot see through that. It is a
conditioning problem, not a size or domain problem (depth 6 is 7x larger than
depth 3 and closes fine).

Already tried and failed, do NOT repeat: splitting the `v` window; extending the
wedge upward past `c = 5/12`; Z3 (unknown after 300 s). Numbers in
`ODD_DEPTH_DIAGNOSIS.md`.

**Next move:** an SOS certificate in the Gegenbauer/Jacobi basis instead of the
monomial basis -- write the object as a sum of manifestly non-negative pieces so
the cancellation never happens. This is exactly Gasper's mechanism for the
Askey-Gasper inequality (his abstract: "an expansion as a sum of squares of
Jacobi polynomials"), it is NOT on our closed-routes list, and the diagnosis
above is the reason to spend effort there rather than on more subdivision.
Cheaper thing to try first: look for an explicit factorisation of `H` at odd
depth.

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
