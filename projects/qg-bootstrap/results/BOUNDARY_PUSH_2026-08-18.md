# Pushing the boundary toward small lam: what moved, what did not

Written the same day as the Dougall reduction (`gegenbauer_term_by_term.json`).
The reduction proves the whole family for `lam >= lam*(n)`, with `lam*/n` measured
at 4.7165..4.7260. The task here was to move that boundary DOWN. **It did not
move.** What follows is what was tried, what was learned, and two errors of mine
caught on the way.

---

## 1. Route A -- block grouping. CIRCULAR, closed.

Dougall's non-negativity is preserved under products, so it is enough to split
`q^2` into blocks and prove each block non-negative separately. A greedy
partition was implemented (worst root first, absorb the smallest factors until
the block is clean).

**Why it is closed:** the greedy returned "1 block" in almost every cell, i.e.
it verified the whole product directly. That is a certificate, not an argument --
exactly what we already had. A block decomposition only helps if the blocks are
UNIFORM (a fixed shape whose non-negativity can be proved once for all n, lam),
and the measurements give no sign that such a shape exists: cleanliness emerges
from the whole product, not from any sub-product.

**Error caught here.** The greedy also returned "no" for `n = 8, 12, 20` at
`lam = 30`, and I first read that as "q^2 has a negative coefficient at the
shore" -- which would have contradicted 525,346 certificates. It does not. The
exact engine confirms zero negative coefficients and zero negative knives in all
three cells. The "no" meant only that the greedy's LAST block, left with
mid-sized factors, was not clean. A failed partition is not a negative result.

## 2. Route B -- closed form for the coefficients. PARTIAL, and exact as far as it goes.

The top ratios of `q`'s Gegenbauer coefficients are small rationals (13/42,
-13/20, 2/15), which is the signature of a closed form. Deriving it:

`q` has symmetric roots so `e_1 = 0` and `SUM t_k^2 = N(N^2-1)/(3 s^2)` -- the
same value for even and odd `N`. Comparing the `v^{N-2}` coefficients of `q` and
of `C_N^gamma` gives the sign of the second-highest coefficient in closed form:

```
a_{N-2} >= 0   <=>   gamma <= 3 (lam + N)^2 / (2 (N+1)) - N + 1 ,      N = n-1
```

**Verified: 30 checks (15 cells, both sides of the threshold), 0 mismatches.**
This is the first exact analytic sign condition in the program; everything before
it was computation.

It is also the BINDING coefficient for `lam >= 4`: at `n = 13, lam = 8` the
formula gives 35.1538 and the measured threshold is 35.1538; at `n = 21, lam = 8`
both are 37.0000; at `lam = 16` both agree to six figures.

**Why it does not finish the job.** At small `lam` the binding coefficient is a
DIFFERENT one, so using this formula as if it were sufficient predicts
`lam* = 1` for `n >= 20`, which is false. It is a necessary condition for one
coefficient, not a sufficient condition for all of them.

## 3. The other exact fact found, and the error it corrected

For `N` even the lowest coefficient has the clean closed form

```
a_0 = SUM_j q_{2j} (1/2)_j / (gamma+1)_j
```

which is the Beta integral `INT q(v) (1-v^2)^{gamma-1/2} dv` written out.
**Verified exactly against the expansion: 24 cells, ratio 1.000000 in every one.**

At `lam = 1` this single number decides the whole boundary: the first positive
root of `a_0(gamma) = 0` equals the true threshold in 6 of 6 cells.

**Error caught.** I concluded from that "index 0 always binds" -- from
measurements at `lam = 1` ONLY. It is false: at `lam = 4` the binding index is 8
(for `n = 13`) or 12 (for `n = 21`), and at `lam >= 8` it is `N-2`. The binding
index MIGRATES upward with lam. This is the same failure mode as ERR-0005 --
a conclusion from one value of a parameter -- and it is the second time this
week. The standing rule stands: vary every parameter before the word "always".

Also worth recording: `a_0` is NOT monotone in gamma (at `n = 7, lam = 1` its
sign runs +, -, + as gamma goes 2, 4, 9), so bisecting on `a_0` alone is invalid
and returns spurious roots. Only the first crossing is meaningful.

---

## 4. Where this leaves the boundary

Unmoved, and now better understood. The obstruction at small `lam` is a single
scalar -- the weighted mean of `q` -- going negative, and the obstruction at
large `lam` is a different, fully solved coefficient. The next attempt should
target the small-`lam` end directly:

* find the closed form of `a_0`'s first root (the Beta-integral sum above is
  explicit, so this is a concrete analytic question, not a search);
* or find a weaker sufficient condition than "all coefficients of q are
  non-negative" that is not equivalent to checking `q^2` directly -- every
  version tried today collapsed back into the direct check.
