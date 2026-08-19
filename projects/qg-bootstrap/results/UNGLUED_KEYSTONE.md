# The unglued keystone argument, and depth 2 closed with it

Night of 2026-08-18/19. Engine 2 throughout (`flint.fmpq`), no sympy, no float
in any comparison.

## What broke, and why it was not physics

The previous "half-level" argument (now retracted, ERR-0010/ERR-0011) proved
positivity at `D = T_K(lam)` where `K` was **the same integer that set the
level** `N = 2K`. That gluing is what killed it. The minimiser of `T_k(lam)`
over integers grows like `sqrt(3)*lam`, so forcing `k = N/2` leaves `T_K` far
above the true shore once `lam` is large, and in that gap the knife is
**legitimately** negative.

Measured at `n = 101`, `lam = 100`:

| where | D | knife |
|---|---|---|
| what the old trick tested, `T_K` | 2500.9 | **−1** |
| the true shore `T_hat` | 1890.4 | **+1** |
| below it | 945.2 | **+1** |

So the physical positivity claim was never in danger. The method was demanding
something strictly stronger than the physics, and then failing at its own
demand. That distinction — a method's self-imposed condition failing versus the
theorem failing — is the whole content of the retraction.

## The argument, in three steps

**(a) Continuum step.** Prove the depth-`d` knife positive at `D = T_v(lam)`
for **all real** `v` in a window, every level, every `lam`. No integrality is
used here, so an exact Bernstein certificate can carry it.

**(b) Integrality step, and only here.** Apply (a) at an **integer** `k_s = v*lam`
inside the window, where `T_hat(lam) <= T_{k_s}(lam)` holds **by definition** of
a minimum over integers. This is exactly the property ERR-0008 showed must never
be assumed for a non-integer.

**(c) Monotonicity step.** The knife decreases in `D` at fixed `(n, lam)` on the
physical interval, so positivity at the top of that interval carries down over
all of `D <= T_hat`.

### A gap in step (c), found 2026-08-19, and how it closes

As first written, step (b) delivered positivity at `D = T_{k_s}` for *some*
integer in the window, and step (c) was supposed to carry that down. **That does
not follow.** `T_{k_s} >= T_hat`, so the claim sits ABOVE the shore, while
monotonicity holds only up to the shore — measured, restricted to `3 < D <=
T_hat`:

| region | result |
|---|---|
| `lam >= 5/2` | **monotone on the whole physical interval**, every depth, every level tested |
| `lam < 5/2` | non-monotone only in a sliver at `D ~ 3.2..3.6`, i.e. 1.7-5% of the way to the shore |

Above the shore monotonicity genuinely fails, so "positive at `T_{k_s}`" could
not be walked down to `T_hat`. An earlier version of this file asserted the walk
anyway. That was the ERR-0008 error a second time — proving something at one
point and helping myself to an interval.

**What closes it.** The window does not merely *contain some* integer; it
contains the **integer minimiser** of `T_k`. Checked exactly at `lam` = 2.5, 3,
4, 5, 7, 10, 20, 50, 100, 300, 1000, 5000, 20000, 100000: argmin is inside
`[8/5 lam, 2 lam]` in **14 of 14** cases —

| lam | argmin | window |
|---|---|---|
| 100 | 173 | [160, 200] |
| 1000 | 1732 | [1600, 2000] |
| 100000 | 173205 | [160000, 200000] |

and the reason is structural rather than lucky: `argmin ~ sqrt(3)*lam`, and the
window `[1.6, 2]*lam` is centred on `sqrt(3) = 1.732...`. The window was fixed
EMPIRICALLY, by measuring where the knife's sign stays positive — and it landed
on the minimiser by itself, which makes sense, since the shore estimate is
tightest exactly there.

So choose `k_s = argmin`. Then `T_{k_s} = T_hat` **exactly**, step (a) gives
positivity **on the shore**, and step (c) only ever needs monotonicity on
`[3, T_hat]` — which is what holds. The argument is now shorter than before: it
never requires anything above the shore.

Note this also means step (b) needs a sharper statement than "the window
contains an integer": it needs "the window contains the minimiser". Verified
above for 14 values of lam; making it a proof means bounding
`argmin_k T_k(lam) / lam` inside `[8/5, 2]` for all lam >= 5/2, which is a
one-variable calculus statement about a known closed form, not a certificate
problem.

## The window was measured, not guessed

`v = 1.45` and `v = 2.10` both produce genuine negatives; `v` in `[1.50, 2.05]`
gave 0 negatives over 48 configurations. The working window `[8/5, 2]` is that
clean interval taken with margin at both ends.

What makes it a keystone candidate rather than one more per-depth trick: **the
same window is clean at every depth tested** — 0 negatives out of 160 per depth
for depths 2 through 8, and a stress test of 246 points across depths 2, 5, 10,
15, levels up to `n = 801`, and `lam` over seven orders of magnitude found none.

## Two independent requirements, one boundary

Step (b) needs the window `[8/5 lam, 2 lam]` to contain an integer. Its length
is `2 lam/5`, so this needs `lam >= 5/2`.

Step (c) was then measured **separately**, with no knowledge of that number:

| region | non-monotone configurations |
|---|---|
| `lam >= 5/2` | **0 out of 120** |
| `lam < 5/2` | 33 out of 96 |

Both steps fail at the same place. That is not a coincidence to be smoothed
over; it says `lam = 5/2` is a real feature of the object, not an artefact of
the parametrisation.

And it is also why the small-`lam` region needed a **different** argument rather
than a harder push on the same one — see below.

## The four pieces, and why each has the shape it does

| piece | region | boxes (even / odd) |
|---|---|---|
| `lo` | `c` in `[5/12, 50]` | 2211 / 2211 |
| `hi` | `c >= 50` | 1 / 1 |
| wedge | `c < 5/12`, `lam >= 5/2` | 1 / 1 |
| small | `lam <= 5/2` | 3 / 1 |

`c = lam/N`. Together these exhaust **every `lam > 0` at every `K >= 3`**, with
no side conditions and no uncovered sliver.

* **Why `c` and not `lam` as the coordinate.** The first version used `lam`,
  because "lam >= 5/2" is then a box face. It proved the near region and jammed
  on the tail: 69253 boxes and failure, and deeper bisection (214021 boxes), a
  leading-term bound (finite threshold, but `3.5e13`, useless) and a geometric
  ladder (301829 boxes on one rung) all failed too. Printing the open boxes back
  in the original variables showed every one sat in the corner where `K -> inf`
  **and** `lam -> inf` together. A two-variable degeneration is a statement
  about the coordinate, not about resources: in `(K, c)` that corner is an
  ordinary finite point, and the same tail closed in **one box**.

* **Why the wedge exists.** With `c` as the coordinate, `lam >= 5/2` becomes the
  slanted condition `c >= 5/(2N)`; the rectangular sufficient version is
  `c >= 5/12` (since `K >= 3` gives `N >= 6`). That leaves out large `N` at
  moderate `lam`. Substituting the **level** instead of bounding `c`,
  `K = 5/(4c) + z` with `z >= 0`, makes `lam = 5/2 + 2cz >= 5/2` and
  `K >= 5/(4c) >= 3` hold automatically, so the wedge is a plain box with
  nothing left over.

* **Why small `lam` uses a fixed integer.** There the window is too short to be
  guaranteed to contain an integer — but the window was only ever a convenience,
  since `T_hat <= T_k` holds for *every* integer `k >= 3`. So fix one. `k = 4`
  is clean on 392 trials across depths 2..10 and all `lam` in `(0, 5/2]`;
  `k = 3` already fails for depth 2 near `lam = 2.4`. Fixing `k` removes the `v`
  axis and the problem becomes 2-variable.

Every piece was verified against the exact reference engine
(`jacobi_coeff_rec`) at concrete points **before** any Bernstein run was
trusted — 320 trials for the main construction, 36 for the wedge, 30 per
depth/parity for the small-`lam` piece, all 0 mismatches.

## Status

**Depth 2: closed for every `lam > 0` and every `K >= 3`.**

Depths 3 and up: the self-check passes and the small-`lam` piece is proved at
depths 3, 4, 5; the remaining pieces are still running. Nothing here is claimed
for them yet.

## What this does NOT yet establish, and the concrete route to fixing it

Step (c), monotonicity in `D`, is **measured, not proved**. 120 clean
configurations above `lam = 5/2` is strong evidence and it lines up exactly with
the independent step-(b) boundary, but it is not a proof, and the argument
leans on it. Until it is certified, "depth 2 closed" means closed *modulo* a
measured monotonicity.

**But the route is now concrete, and it is the same machinery.** Differentiating
the beta-mean form term by term,

```
knife ~ sum_j r_j X^j (m+1/2)_j / (g)_j ,        g = 2m + gamma + 1
d/dgamma [1/(g)_j] = -(1/(g)_j) * psi_j(g),      psi_j(g) = sum_{i<j} 1/(g+i)
```

so

```
-d(knife)/dgamma  =  sum_j r_j X^j (m+1/2)_j * psi_j(g) / (g)_j .
```

This is **the same shape as step (a)** — the same coefficients `r_j`, the same
Pochhammer denominators — with one extra positive rational weight `psi_j(g)`.
Clearing `psi_j`'s denominators turns it back into a polynomial positivity
problem of exactly the kind the Bernstein pipeline already certifies. So step
(c) is not a different sort of obstacle; it is another instance of the problem
already solved, and can be closed with the existing tool rather than new theory.

The identity was verified against finite differences (agreement to `1e-9`, the
finite-difference floor) at depths 2, 3, 4.

One caveat found while checking it, worth recording because it is easy to
misread: the derivative **does** go negative at `D = 123` for `n = 21`,
`lam = 5` — but the shore there is `T_hat(5) = 93.7`, so that point is
**outside** the physical region. Strictly at or below the shore: 0 negatives out
of 320 configurations across depths 2..5, levels up to 80, and `lam` from 5/2 to
500. Monotonicity is a statement about the physical region, and only there.

## Prior art to cite before any preprint

The descent lemma used elsewhere in this project ("positivity at `D+2` implies
positivity at `D`, uniformly in spin") is **Schoenberg's dimension walk**,
`Psi_{d+1} subset Psi_d` — Gneiting, Theorem 2(b),(c), arXiv:1111.7077. It
appears in the amplitude literature as the branching-rule argument. Cite it.

See also `AEHM_ROUTE_VERDICT.md` for why the closest prior method
(Mansfield arXiv:2502.20372, all `n` and all `j` at `D <= 10`) does not transfer
to this regime, and why his theorem does not already contain this problem.

---

## A hole in step (b), found 2026-08-19 by a dense sweep, and closed the same way

The claim above -- "the window contains the integer MINIMISER" -- was checked at
14 values of lam (2.5, 3, 4, 5, 7, 10, 20, 50, 100, 300, 1000, 5000, 20000,
100000) and held 14 of 14. **A dense sweep breaks it.** Stepping lam by 0.05 from
2.5 to 70 (1351 values, exact arithmetic):

| lam band | argmin | window | side |
|---|---|---|---|
| 2.60 .. 2.95 | 6 | [4.16, 5.20] .. [4.72, 5.90] | RIGHT of it |
| 3.35 .. 3.45 | 7 | [5.36, 6.70] .. [5.52, 6.90] | RIGHT of it |

11 of 1351 fail, all just above `lam = 5/2`, all falling off the RIGHT edge.
Above `lam = 3.45` the argmin is inside the window at every one of the remaining
samples.

**Why it matters.** Step (b) only needs *some* integer in the window for
`T_hat <= T_{k_s}`, and one is always there. But the sharpened version -- the one
that closes step (c) without needing monotonicity above the shore -- needs the
MINIMISER, so that `T_{k_s} = T_hat` exactly. On this band the argument does not
close.

**Why the sparse check missed it, and it is the ERR-0005 mechanism again.** My
ladder jumped 2.5 -> 3 -> 4, straight over [2.6, 2.95], and 3 -> 4 straight over
[3.35, 3.45]. A sparse grid over a narrow feature is blind, and 14 of 14 read as
convincing. The derivative test is what pointed at it: `dT/dk` at the right edge
`k = 2 lam` is NEGATIVE for lam = 2.5 and 3, meaning the continuous minimiser
sits right of the window there -- so the integer one had no reason to be inside,
and only was at the sampled points because `2 lam` happened to be an integer.

**Closed, by the mechanism already in the file.** The bad band is FINITE, so it
gets a fixed shore level exactly as `lam <= 5/2` does. Measured on
lam in [2.5, 3.6], depths 2..8, 1127 trials:

| fixed k_s | negative knives |
|---|---|
| 4 | **5** (fails: d=2, n=13, lam=3.4) |
| 5 | **0** |
| 6 | 0 |
| 7 | 0 |
| 8 | 0 |

So `k_s = 5` covers the band. The lam axis is now three pieces, each closed by
its own device:

| lam | device |
|---|---|
| `<= 5/2` | fixed `k_s = 4` |
| `[5/2, 18/5]` | fixed `k_s = 5` (this band was the hole) |
| `>= 18/5` | the window `[8/5, 2]`, argmin inside |

**Still not a proof, and stated as such.** "argmin inside the window for all
lam >= 18/5" now rests on 1351 exact samples up to lam = 70 plus the sparse
ladder to 1e5 -- not on an argument. The derivative form above is the route to
proving it: show `dT/dk < 0` at `k = 8/5 lam` and `> 0` at `k = 2 lam` for all
lam >= 18/5, both being polynomial inequalities in (k, lam) after clearing the
positive denominator `(k(k-2))^2`. The first sign held at every lam tested; the
second is what fails below 18/5 and is exactly what needs bounding.
