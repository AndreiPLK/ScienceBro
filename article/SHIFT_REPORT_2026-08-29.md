# Shift report, 29 August 2026

Started on a literature pass, ended with a front standing on proofs instead of
measurements. Times from `date`, numbers from artefacts. The map of every claim
and its status is `projects/qg-bootstrap/results/PROOF_STATUS_2026-08-29.md`.

## Green, with numbers

**A proof where there was a measurement.** The far-below criterion has exactly one
negative coefficient, and grouping it with its neighbours reduces positivity to

    (R)  4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0.

(R) is UNCONDITIONAL — it holds at all 504 region points, not only the 117 dips —
and **certified at `J` = 7, 9, 12, 16, 20, 25-32, 35, 40 and 50**: by monomial signs to `J = 29`,
by monomial signs inside the regime at 30, and by one Bernstein step in `thL` from
31 on. Nonnegative monomials over a nonnegative orthant is a proof.

**Combined with the one-negative-coefficient structure, that closes `j = 9..16`** —
depths that previously needed the heavy interval-Bernstein route. The conclusion
was then tested against the object itself, not only its parts: `N(y)` evaluated
exactly at 252 region points crossed with `y` up to `10^5`, at `j = 9, 11, 13, 15`,
zero non-positive.

**Four more things became proofs today:**

* the elementary half of the uniformity chain — two independent proofs, one a
  one-line cancellation found here, one from the parallel chat;
* the limit-shape bound `f(theta) < 2` on `(0,1/2)` — proof supplied by the
  parallel chat, one step repaired here: its factorisation printed `(z-1)` where
  the quartic has `z = 1` as a DOUBLE root;
* **(B) at every `t <= 100`** — one hundred finite proofs, degrees 22 to 1606,
  zero failures, each by the same all-nonnegative-coefficients move;
* the `b`-multiset is DOUBLED: `prod (u - b_k)` is a perfect square and `E_{2t}` is
  the self-convolution of a half-set — a one-line proof, absent from this
  repository until today.

**The literature question, answered.** Our transform is the finite free
multiplicative convolution — classically the **Schur–Szegő composition** (Szegő
1922, Walsh 1922). Identified exactly: 336 cases, 0 mismatches, 65 of them with a
negative reference knife. Novelty of the technique: POSSIBLY_KNOWN -> KNOWN.

## What remains, and it is now one ask

The finite-`n` bridge needed two conjectures, (B) and (C). (B) is a theorem for
`t <= 100`. And (C) turns out not to be independent: its margin is of order
`1/n^2`, exactly what `M = f + g/n + O(1/n^2)` with `g > 0` predicts, so it follows
from an effective second-order expansion — which also gives the bound directly.

So the whole remaining gap is **one effective expansion with explicit remainder**,
and its target is measured: `g` runs from 1.39 at `theta = 0.05` to 5.35 at 0.49,
positive and increasing.

Also still measured rather than proved: that every `c_k` with `k != J-2` is
nonnegative. It holds on 1476 points tested on both sides of its boundary
`n >= 2J-3`, and is now checkable per depth in minutes rather than hours.

## What I need from you

Nothing. Decisions taken without asking, all reversible: the certificate work took
priority over the asymptotic route; four pages were published as artefacts; four
questions went to the parallel chat and every answer was checked here before use.

## Where I was wrong today

Nine of my own claims died, most by tests I wrote next to them.

* **ERR-0015** — "criterion S" had its conclusion inside its hypothesis.
* **ERR-0016** — "odd-`j` knives never dip": they do, 72 cases, on both engines.
* **ERR-0017** — the recorded depth law `j <= n/2+1` was fitted on
  `n = 12, 16, 20, 24, 28, 36, 44`, all multiples of four; over `n = 11..100` it
  fails in 70 of 90 rows. Withdrawn — and it was the SECOND time this lab was bitten
  by a sub-grid, after the even-`j` retraction of 18 August.
* the doubling hypothesis for the half-depth boundaries — refuted by the control I
  had named in the same paragraph;
* "the dominant term wins" — the rest exceeds it by 3 to 3.2e8;
* "no depth fails the in-regime certificate" — it fails from `J = 31`, where a
  Bernstein step is needed;
* the AP form of (B) without a range restriction — false, with an explicit
  counterexample at `N = 10`, `t = 8`;
* an off-by-one in the central index that produced 150 spurious violations of (C);
* reaching for Newton to bound the excess from above — Newton bounds that ratio from
  BELOW, the wrong direction, caught by an assertion in the first run.

## What checks this now

* every module re-run from scratch at the end of the day, every number reproducing;
* three page builders that regenerate their pages from the artefacts and refuse to
  emit if the data stops supporting the claim;
* the regime law tested on a grid containing BOTH sides of its boundary, because a
  boundary inferred from corner scans is exactly what ERR-0017 was about;
* the depth cutoff computed at EVERY `n`, including the odd ones the original run
  never touched;
* a rule in lab memory: before recording a law, check the sample can distinguish it
  from its nearest rival; and if a claim prunes a search, keep sampling the pruned
  branch;
* `moment_kernel_probe` no longer dies above `n ~ 100` — the int-to-string cap that
  had kept these probes small is lifted at the source.
