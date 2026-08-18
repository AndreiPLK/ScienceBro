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

**(c) Monotonicity step.** The knife decreases in `D` at fixed `(n, lam)`, so
positivity at the largest admissible `D` (namely `T_{k_s} >= T_hat`) carries
down over the whole physical region `D <= T_hat`.

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

## What this does NOT yet establish

Step (c), monotonicity in `D`, is **measured, not proved**. 120 clean
configurations above `lam = 5/2` is strong evidence and it lines up exactly with
the independent step-(b) boundary, but it is not a proof, and the argument
leans on it. Turning it into a certificate is the next necessary piece of work,
and until then "depth 2 closed" means closed *modulo* a measured monotonicity.

## Prior art to cite before any preprint

The descent lemma used elsewhere in this project ("positivity at `D+2` implies
positivity at `D`, uniformly in spin") is **Schoenberg's dimension walk**,
`Psi_{d+1} subset Psi_d` — Gneiting, Theorem 2(b),(c), arXiv:1111.7077. It
appears in the amplitude literature as the branching-rule argument. Cite it.

See also `AEHM_ROUTE_VERDICT.md` for why the closest prior method
(Mansfield arXiv:2502.20372, all `n` and all `j` at `D <= 10`) does not transfer
to this regime, and why his theorem does not already contain this problem.
