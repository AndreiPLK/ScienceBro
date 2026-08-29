# The b-multiset is doubled, and everything halves

2026-08-29. Checks in `lab/doubled_multiset.py` ->
`results/doubled_multiset.json`.

## The fact, with its one-line proof

The B-form of the knife runs over `b_k = (n-2k)^2` for `k = 1..n-1`
(`BFORM_POSITIVITY_THEOREM.md` Thm 1). Those numbers are **pairwise equal**:

    b_{n-k} = (n - 2(n-k))^2 = (2k - n)^2 = (n - 2k)^2 = b_k.

So the multiset is a doubled copy of the half-set

    beta = { (n-2k)^2 : k = 1 .. ceil(n/2) - 1 },   |beta| = ceil(n/2) - 1,

together with the single value `0` when `n` is even (`k = n/2`). Consequently

    PROD_{k=1}^{n-1} (u - b_k)  =  [ PROD_{beta} (u - b) ]^2  *  u^{[n even]},

a **perfect square** times at most one linear factor, and

    E_{2t}(n) = e_t(b) = SUM_i e_i(beta) e_{t-i}(beta),

the central factorial numbers are the **self-convolution** of the half-set's
elementary symmetric functions. Both statements are proofs, not measurements —
but both were checked anyway: the pairing at `n` = 7, 8, 12, 13, 20, 41; the
square factorisation exactly as `fmpz_poly` identities at `n` = 8, 13; the
self-convolution over **182 checks at both parities, 0 mismatches**.

## Why it was worth stopping to notice

`BFORM_POSITIVITY_THEOREM.md` §6c records that `b_1 = b_{n-1} = B` is a double
root — the extreme pair. The whole multiset being doubled, with only
`floor(n/2)` distinct values, is not recorded anywhere in this repository, and it
is a different order of fact: it says the object the programme has been
factorising, differentiating and convolving all month is the square of a
polynomial half its size.

## Four boundaries at half depth, and a candidate reason

Everything measured on 29 August broke at the same line:

| where | boundary |
|---|---|
| condition (E) from the Grace–Szegő transfer | vacuous for `r > (2n+1)/4` |
| the far-below localisation (only `c_{J-2}` dips) | ends at `n = 2J-3`, i.e. `j <= (n+3)/2` |
| the Hausdorff depth cutoff | drifts just below `n/2` |
| the Newton-excess lemma `<= 1 + 2/n` | holds up to `t ~ n/2` |

Four unrelated mechanisms, one line. The doubling supplies a candidate reason:
there are only `floor(n/2)` DISTINCT values among the `b_k`, so every statement
that reads off `e_t` for `t` beyond that count is asking about elementary
symmetric functions past the number of distinct generators — where a doubled set
stops behaving like a generic one.

**REFUTED, within the hour, by its own test.** The test named here was: compute
one of those boundaries for a family of the SAME size with no doubling, and see
whether it moves. It does not. For the Newton-excess boundary at `lam`-free level:

| n | 20 | 30 | 40 | 50 |
|---|---|---|---|---|
| ours, doubled `(n-2k)^2` | 9 | 14 | 20 | 25 |
| distinct `k^2` | 10 | 15 | 21 | 26 |
| distinct `((n-2)k)^2` | 10 | 15 | 21 | 26 |

The undoubled families sit at the same place, one step higher. So the half-depth
line is a property of the SIZE of the multiset — the midpoint of the elementary
symmetric range for `N = n-1` numbers — and not of the doubling. The hypothesis is
dead; the doubling itself stands, and so does the coincidence of the four
boundaries, now without an explanation.

## What it might buy

* Newton's inequalities for `b` are those of a self-convolution, which is why the
  measured Newton excess is only `1 + O(1/n)` — a self-convolution of a Pólya
  frequency sequence is again one, so log-concavity is inherited with room. The
  lemma that a J-uniform (R) needs
  (`FARBELOW_NEGATIVE_PATTERN.md`) is a statement about exactly this, and should
  be attacked through the half-set rather than through the doubled one.
* Every route that treated `prod_k (u - b_k)` as a generic real-rooted polynomial
  — the derivative form of Thm 7, the Schur–Szegő composition of
  `FFP_LITERATURE_PASS.md`, the root-contraction argument of §6c — was working
  with a perfect square without using it.
