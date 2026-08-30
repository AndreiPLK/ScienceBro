# The rung polynomial factors, and the hard part shrinks by a factor of two and a half

*2026-08-30 morning shift. Exact, over `Q`.*

## What was found

The rung polynomial `D_{t,r}` — the one whose coefficient positivity after a shift proves
`Delta^r log p_t < 0` — is very far from generic. It factors as

    D_{t,r}(n) = c * (n + 1) * PROD_{k=0}^{t+r} (n - k)^{m_k} * Q_{t,r}(n),

with every root an integer in `-1, 0, 1, ..., t+r`, and:

* `m_0 = 2^{r-1}` and `m_1 = 2^r`, exactly, in every case examined;
* `m_{t+r} = 1` — **a simple root exactly at the shift point**;
* the multiplicities in between decrease smoothly (for `t=1, r=6`: 32, 64, 63, 57, 42, 22,
  7, 1).

| `t` | `r` | `deg D` | `deg Q` | ratio |
|---|---|---|---|---|
| 2 | 3 | 54 | 21 | 2.6 |
| 1 | 4 | 93 | 36 | 2.6 |
| 4 | 3 | 86 | 37 | 2.3 |
| 3 | 4 | 157 | 68 | 2.3 |
| 2 | 5 | 284 | 123 | 2.3 |
| 1 | 6 | 507 | 218 | 2.3 |

## The reduction

Every linear factor is `(n - k)` with `0 <= k <= t+r`, or `(n+1)`. Under a shift
`n = m + s` with `s >= t + r`, each becomes `m + (s-k)` with `s - k >= 0`, or `m` itself.
**A product of such factors has nonnegative coefficients automatically.** Therefore:

> **Reduction.** If `s >= t + r` and `Q_{t,r}(m + s)` has all nonnegative coefficients,
> then so does `D_{t,r}(m + s)`, and the rung `Delta^r log p_t < 0` is proved for every
> `n >= s`.

So the whole difficulty sits in the core factor `Q`, at roughly two-fifths of the degree.
The reduction is sufficient, not necessary: `Q` sometimes needs a smaller shift than `D`
(at `t=1, r=4`, `Q` needs 4 where `D` needs 5), so working with `Q` can only help.

## Where the parity actually lives

The parity law — minimal shift exactly `t+r` when `t+r` is odd, `t+r+2` or more when even —
is **not** in the root structure. Both parities have the same shape: a simple root at
`n = t+r`, multiplicity 4 to 6 at `n = t+r-1`, and a root at `n = -1`.

Measured on `Q` directly:

| parity | `Q(m + t + r)` nonnegative? | smallest shift for `Q` |
|---|---|---|
| `t+r` odd, 6 cases | **yes, all** | at most `t+r` |
| `t+r` even, 6 cases | no, none | `t+r+2` or `t+r+3` |

So **the parity lives inside `Q`**. That is where an argument has to look, and it is now a
much smaller object to look at.

## What this does to the open conjecture

`(U2)` asked that `D_{t,r}(m + 2(t+r)+1)` have nonnegative coefficients. By the reduction
it suffices to prove

> **(U2-core).** `Q_{t,r}(m + 2(t+r) + 1)` has all nonnegative coefficients for every
> `t >= 1`, `r >= 3`.

Same consequence — the entire log-difference hierarchy, and with it conjecture (B) — on an
object of two-fifths the degree, with all the trivially-positive structure already
stripped away.

## Honest limits

The multiplicity formulas `m_0 = 2^{r-1}`, `m_1 = 2^r` are observed on the cases examined,
not derived. They are believable — `2^r` is the total exponent weight `SUM_j C(r,j)` — but
until derived they are a pattern, not a lemma. The reduction itself does not depend on
them: it needs only that every root is an integer in `[-1, t+r]`, which is what the
factorisations show, and which should be provable from the fact that `e_j(n)` vanishes for
`n <= j`.
