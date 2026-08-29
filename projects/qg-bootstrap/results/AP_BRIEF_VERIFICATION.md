# The AP-square brief, checked — and where it meets the tilt picture

*2026-08-29 evening. Artefact: `results/ap_square_brief_check.json`, module
`lab/ap_square_brief_check.py`. Source: a brief from the parallel chat, treated as
untrusted input and checked before use.*

## Everything checkable in it, checked exactly

| # | claim | verdict |
|---|---|---|
| C1 | counterexample `N=3, t=1, alpha=-1/2` gives `-5/108` | reproduced exactly |
| C2 | second failure at `N=4, t=2`, centered | confirmed, `H = -627/4096` |
| C3 | **Conjecture 1**: `N >= 5`, `1 <= t <= floor(N/2)`, every real AP | **14652 exact cases, 0 counterexamples** |
| C4 | shift identity `(1+a^2 z)F_N(z;a+1) = (1+(a+N)^2 z)F_N(z;a)` | 0 mismatches |
| C5 | centered factorisations (7) and (8) | 0 mismatches, `n = 4..30` |
| C6 | hypergeometric self-convolution `p_t = E[q_I q_{t-I}]` | 0 mismatches |

C3 was attacked, not sampled: a dense exact grid of the centered parameter `c` with
denominators to 6, spanning both the crossing regime `0 <= c < h` and the
non-crossing one out to `c = 20h+1`, at every `N` from 5 to 26. Their `c -> -c`
reflection symmetry was tested rather than assumed (0 mismatches), so half the
parameter line is genuinely redundant.

Nothing in the brief needed repair. That is the first of the four external answers
today for which that is true.

## The one thing it says that changes our plan

**Section 8: the physical spectrum is the centered point `c = 0`.** Our `b`-multiset
is `(n-2k)^2`, which is a centered AP, so we never need the general AP conjecture —
only its most special point. That agrees with what we proved here this morning
independently (`DOUBLED_MULTISET.md`): the generating polynomial is a perfect square.

**Section 9 then halves the object.** With `n = 2m+1`, `F = G^2` for the half
spectrum `G = prod (1 + (2j-1)^2 z)`, and

    p_t = SUM_i [C(m,i) C(m,t-i) / C(2m,t)] q_i q_{t-i} = E[q_I q_{t-I}],

`I ~ Hypergeom(2m, m, t)`. So the physical (B) is exactly: *does hypergeometric
self-convolution preserve ratio log-concavity?*

**And the input to that induction holds.** We tested whether the half spectrum
itself is ratio log-concave: `m = 5..40`, every `t` in the FULL index range, 738
cases, **0 failures** — not merely on the first half, which is all their Conjecture 1
would give. So the induction has a true premise and one missing step.

## Where it meets today's other finding

`POISSON_BINOMIAL_VIEW.md` reads the same family as a tilted Bernoulli sum. The
brief's Section 9 is that statement seen from the other side: `F = G^2` means

    Y = Y' + Y'',   Y', Y'' independent and identically distributed,

each a Poisson-binomial over the half spectrum. Two descriptions found the same
structure on the same day from opposite directions — one from a prior-art check on
central factorial numbers, one from a factorisation of the AP.

That is useful and not merely pleasing: a local limit theorem for a sum of two iid
copies is a strictly easier object than one for a general Bernoulli sum, and the
tilted cumulants halve with it.

## Not checked

The brief's Jacobi–Stirling transform (4), the LGV/total-positivity programme, and
the finite-`S`-transform curvature reading are proposals, not claims with numbers;
nothing was verified about them and nothing here relies on them.


## Follow-up the same night: their Problem 2 needs a stronger hypothesis

`SELFCONV_PRESERVATION.md` asks whether the preservation their Problem 2 wants is
true in general. It is not: 1561 of 2800 general ratio-log-concave inputs are
mapped to non-RLC outputs. It held for every real-rooted input tested (713 of 713),
and for the physical half spectrum at every `m = 4..24`.

So the route survives with its statement corrected -- the load-bearing hypothesis is
real-rootedness, not RLC -- and any attempt arguing only from RLC of the input is
provably doomed.
