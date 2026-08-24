# Why odd depths do not close: measured, 2026-08-21

Even depths 2, 4, 6 certify. Odd depths 3 and 5 have now resisted several
sessions. This is the diagnosis, with the numbers, and the three things that
were tried and did NOT work.

## It is not size

| depth | K_deg | c_deg | v_deg | terms (even / odd) | certifies? |
|---|---|---|---|---|---|
| 2 | 12 | 8 | 6 | 180 / 301 | yes |
| 3 | 18 | 12 | 9 | 548 / 922 | **no** |
| 4 | 24 | 16 | 12 | 1232 / 2071 | yes |
| 5 | 30 | 20 | 15 | 2330 / 3912 | **no** |
| 6 | 36 | 24 | 18 | 3940 / 6613 | yes |

Depth 6 is seven times larger than depth 3 and closes in 937 boxes. Size is not
the obstacle, and the growth is perfectly regular across the parity split.

## It is not a sign

An earlier guess was that odd depths carry a global `(-1)^m`, so the polynomial
would be negative and Bernstein could never close it. Measured across the
certified box at depths 2-6: the sign is `+1` everywhere, odd depths included.
Wrong guess, discarded.

## It is CANCELLATION, and here is the number

Evaluate `H` at a point and compare the total against the largest single
monomial contribution at that same point -- a relative margin, since the
coefficients span dozens of orders of magnitude and an absolute value would say
nothing:

```
worst relative margin, depth 3 even:  7.8e-05
    at K = 1000, c = 5/12, v = 2.0   (the corner of the box)
```

So the polynomial is positive, but its value is ~13000 times smaller than the
biggest term being summed. Bernstein bounds a polynomial by its coefficients;
when the answer is a near-total cancellation between huge terms, those bounds
are useless until the box is subdivided far enough to separate the cancelling
pieces -- which is exactly the observed behaviour (box counts climb, open boxes
never reach zero).

The jamming region matches: every open box sits at `c` near its lower limit
`5/12` and `K` large -- the same corner where the margin is worst.

## Three attempts that did NOT work, recorded so they are not repeated

1. **Split the v window.** The worst margin sits at the top edge `v = 2`, so
   the window was cut at `v = 19/10`. Both halves still fail:
   `[1.6, 1.9]` -> 3349 boxes, 310 open; `[1.9, 2.0]` -> 4979 boxes, 573 open.
   The cancellation is distributed, not localised at the edge.

2. **Push the wedge up to swallow the hard zone.** The wedge substitutes
   `K = 5/(4c) + z` and so covers every `K >= 5/(4c)`, which for `c > 5/12`
   is below 3 -- meaning the wedge could in principle take over the region.
   It closes in **1 box** on `c <= 5/12` and fails immediately past it:
   `c <= 1` -> 7153 boxes, 2688 open. The wedge parametrisation is only good
   where it currently is.

3. **Z3 as an independent decider.** nlsat decides sign questions by cylindrical
   decomposition rather than coefficient bounds, so heavy cancellation is not
   automatically fatal for it. Asked to refute positivity on the depth-3 `lo`
   box (unsat would be a proof): **unknown after 300 s.** Not a refutation, not
   a proof -- it simply could not decide in the budget.

## What this points at

The obstacle is a *conditioning* problem, not a domain or size problem. The fix
has to be a representation in which the cancellation is gone -- i.e. writing the
object as a sum of manifestly non-negative pieces rather than as a difference of
large ones.

That is precisely the mechanism the literature pass already flagged: Gasper's
proof of the Askey-Gasper inequality works by "an expansion as a sum of squares
of Jacobi polynomials" (his own abstract; DLMF 18.14.25/26 attribute the proofs
to him). See `research/reading-notes/keystone-uniformity-2026-08-18.md` section
1.1, where it is recorded as the shape a keystone should have and as NOT on the
project's closed-routes list. An SOS certificate in the Gegenbauer/Jacobi basis
-- rather than the monomial basis Bernstein works in -- is the natural next
attempt, and the diagnosis above is the reason to spend effort on it rather than
on more subdivision.

Secondary option, cheaper to test: find an explicit factorisation of `H` at odd
depth. If a factor is responsible for the near-cancellation, certifying the
factors separately avoids it entirely.

---

# CORRECTION (2026-08-24): the diagnosis above is WRONG -- see ERR-0013

The conclusion "it is CANCELLATION" does not survive its own measure, and the
recommended fix (SOS basis change) was aimed at certifying a FALSE statement.

* The corner margin decreases smoothly with depth -- 2.2e-3 / 7.8e-5 / 3.1e-6 /
  1.1e-7 for depths 2 / 3 / 4 / 5 -- with no parity structure at all. Depth 4's
  margin is 25x worse than depth 3's, and depth 4 certifies in 1369 boxes.
  Cancellation therefore cannot be what separates even from odd.

* The truth: the step-(a) fixed-window statement is FALSE at odd depths. Exact
  witnesses inside the certified box, confirmed by build_branch AND the exact
  reference engine independently: depth 3 at K=54, c=239/400, v=2 the knife is
  NEGATIVE (also v=8/5 at K=226, c=3/5; depth 5 from K=111). Artifact:
  `results/odd_depth_window_refuted.json`.

* Mechanism: odd depth = even knife order j = d+1, and even-j knives MUST have
  a threshold (margin law, 2026-08-17). Away from the argmin of T_k the window
  point T_{v*lam} overshoots that threshold once lam is large. Even depths are
  thresholdless, hence immune. The Bernstein runs did not jam -- they correctly
  refused to prove a false claim.

* Why the scans above missed it: the negative region needs BOTH c in ~(0.52,
  0.67) AND K >= 54; every c grid used here stepped over that band (ERR-0005
  mechanism, third occurrence).

* The physics is untouched: at every witness point the knife is positive at the
  true shore T_hat (integer argmin), both engines agreeing.

* The three failed attempts recorded above now have a one-line explanation:
  subdividing (1), reparametrizing (2), or switching decision procedure (3)
  cannot prove a false statement. Z3's `unknown` was the only honest answer in
  the file.

Repaired route: certify positivity on a window of fixed width in k-units
around the critical level k*(lam). The critical curve dT/dk = 0 is a conic in
(k, lam) (discriminant 3 k^2 (k-2)^2 (4k^2-12k+3), non-square part quadratic,
rational point (3,3)), so it has an explicit rational parametrization and the
repaired claim is polynomial in (t, delta, K). See ERR-0013.
