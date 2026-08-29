# Which hypothesis is load-bearing: self-convolution does NOT preserve RLC in general

*2026-08-29 night. Artefact: `results/selfconv_preservation.json`, module
`lab/selfconv_preservation.py`, seed 20260829, every number exact.*

The AP-square brief reduces the physical conjecture (B) to a preservation question:
does the hypergeometric self-convolution

    p_t = SUM_i [C(m,i) C(m,t-i) / C(2m,t)] q_i q_{t-i}

carry ratio log-concavity (RLC) from `q` to `p`? Their Problem 2 asks for a proof.
Before spending a week on that route, this asks a cheaper question: **is it even
true in general?**

## The answer, and it is a clean dichotomy

| input family | RLC inputs | outputs that FAIL RLC |
|---|---|---|
| A — general RLC sequences | 2800 of 2800 | **1561** |
| B — real-rooted (normalized elementary means of positive multisets) | 713 of 2800 | **0** |
| the physical half spectrum, `m = 4..24` | all | 0 |

**Preservation is false in general.** More than half of general RLC inputs are
mapped to non-RLC outputs. So no theorem of the form "hypergeometric
self-convolution preserves RLC" exists, and their Problem 2 cannot be closed by
one.

**But it held for every real-rooted input tested.** That is what the route actually
needs, and it sharpens the target from a false statement to a plausible one:

> **Conjecture (P).** If `q_i = e_i(x)/C(m,i)` for a positive multiset `x` and `q`
> is ratio log-concave, then its hypergeometric self-convolution is ratio
> log-concave on the first half of its range.

713 supporting cases, 0 against.

## Two things worth noticing in the same table

Family A was **constructed, not filtered**: a sequence is RLC exactly when
`r_t = q_t/q_{t-1}` is log-concave, so a decreasing `d_t = r_t/r_{t-1}` produces
one directly and every RLC sequence arises this way. So the 2800 are a fair sweep
of the class, not a corner of it.

Family B shows RLC is **not** automatic for real-rooted sequences: only 713 of 2800
random positive multisets gave an RLC `q` at all. That is consistent with the
brief's own Section 12 — real-rootedness alone cannot imply (B) — and it means the
two hypotheses in (P) are independent, neither implying the other.

## What it changes

The route survives, with its statement corrected. The load-bearing hypothesis is
real-rootedness, not RLC, and any attempt at Problem 2 that argues only from RLC of
the input is provably doomed — which is worth knowing before the attempt rather than
after.
