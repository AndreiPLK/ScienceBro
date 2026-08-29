# Verdict on the external root-bound answer (Grace–Szegő transfer)

2026-08-29. Source: a second assistant, answering
`research/BRIEF_KEYSTONE_FOR_OUTSIDE_HELP`-style questions put by the founder in
a parallel chat; delivered as a PDF. **Untrusted input by the repository's own
rule**, so every checkable statement in it was re-derived or re-measured here
before being used. Machine checks: `lab/grace_transfer_check.py` ->
`results/grace_transfer_check.json`.

## What it proposes

1. **(A)** The real-rootedness-preservation corollary of Grace–Szegő is
   unavailable because `q` has complex zeros — but the CIRCULAR-REGION form is
   not, and it does not need `q` real-rooted:

       theta_max(p BOX_N q)  <=  B * max{ Re zeta : q(zeta) = 0 },   B = (n-2)^2/s^2.

   Only the rightmost REAL PART of `q`'s zeros matters.
2. **(C)** An explicit spectral-abscissa bound for that quantity, via the Jacobi
   three-term recurrence: `Q_r` is a nonclassical Jacobi polynomial whose Jacobi
   matrix has `A_{k-1}C_k < 0`, so after a diagonal similarity the off-diagonal
   entries are purely imaginary, the Hermitian part is the real diagonal
   `diag(d_k)`, and the numerical range gives `Re y <= max_k d_k`. Hence

       max Re zeta <= 2/(1-eta),  eta = (H+1)(H-2n+2)/[(H-2r+3)(H-2r+1)]   (eta < 1).

3. **(E)** Consequently `eta < 1` and `s^2 > 2(n-2)^2/(1-eta)` imply
   `theta_max < 1`.

## What we verified

* **(A): 0 violations in 144 cases** (`n` = 6..40, three depths, `lam` = 1, 7,
  30, 300, `D` = 4, `T_hat/2`, `T_hat`). Checked against the exact composition,
  using the certified Descartes test for "no real zero at or above the bound".
* **(C): 0 violations** in every case where `eta < 1` (`eta >= 1` in 39 of the
  144, which is itself the interesting part — see below).
* **Their control example reproduces exactly.** They report `n = 20, r = 8,
  D = 4` giving `eta = 0.032958`, `s^2 > 670.085`, `lam > 6.886`. We get
  `eta = 0.03295786399666249`, `s^2 > 670.0845556514237`, `lam > 6.885991...`.
  So their arithmetic is right and our reading of their formula matches theirs.

## What it buys, measured at the shore

Smallest `lam` at which (E) holds at `D = T_hat`, per depth:

| n | r = 2 | r = 3 | r = n/4 | r = n/2 | r >= 3n/4 |
|---|---|---|---|---|---|
| 8 | 62 | 122 | — | 662 | never |
| 12 | 90 | 124 | — | 1858 | never |
| 20 | 150 | 175 | 255 | 6057 | never |
| 40 | 301 | 322 | 590 | 27094 | never |

`lam/n` at `r = 2` is **7.75, 7.50, 7.50, 7.53** — flat, and **four times better
than Theorem 9's `32n`**, by a completely different mechanism. At `r = n/4` it is
still 12-15n, better than `32n`. So for shallow and mid depths this is a genuine
improvement on the best region the programme had.

## Where it stops, and why — the honest headline

**(E) is vacuous for deep knives, at every `lam`.** As `D` grows, `eta -> 1`:
the numerator loses `(2n-3)H`, the denominator loses `(4r-4)H`, so

    eta < 1 at large D   <==>   4r - 4 < 2n - 3   <==>   r < (2n+1)/4.

Past that depth `eta >= 1` and the hypothesis is empty no matter how large `s`
is. That is why the last column is "never" rather than a large number, and it is
the same wall as before: the deep knives, which is where uniformity in depth
lives, are untouched.

## Two further items in the answer

* Its **(U)**, `s^2 > n(n-2) r(H-r)/[3(n-3/2)]`, is **exactly our Theorem 5
  condition (*)**, rederived from the coefficient side. An independent
  rederivation of a result we already have is a useful cross-check and nothing
  more.
* Its **(W)** — "all Taylor coefficients at `x = 1` positive implies
  `F_r(x) > 0` for `x >= 1`" — is the criterion this repository already filed as
  circular in **ERR-0015**: `c_0 = F_r(1) = K_r` is the conclusion. Its **(Y)**,
  however, is not circular: `delta < r/(r-1)` plus the single exact check
  `F_r(1) > 0` gives the whole ray, relaxing Theorem 5's `delta < 1` by
  `1 + 1/(r-1)`. Small, but real, and untested here.
* Its **Routh–Hurwitz route (AC)** — Hurwitz determinants of `Q_r(z+R)`,
  `R = s^2/(n-2)^2`, as an exact necessary-and-sufficient test for the
  intermediate condition — is the strongest thing offered and is **not yet
  tested**. It is the obvious next experiment.

## The ceiling, measured: it is (A) itself

Their Routh–Hurwitz route (AC) was implemented (`hurwitz_test` in the module) and
is **strictly stronger than (E)**, as advertised: at `lam = 300` it fires at
`n = 12, r = 6` and `r = 10`, and at `n = 40, r = 2`, where (E) does not. But it
still fails at the deep knives (`n = 20, r = 18`; `n = 40, r = 20, 38`), while the
truth — no real zero of the composition at or above 1 — holds in all 27 cases
tested.

That is not a defect of the spectral estimate. It is the transfer bound itself.
Measured loss, `[B · max Re zeta] / [certified true bound c*]` at the shore:

| n | r = 2 | r = n/2 | r = n-2 |
|---|---|---|---|
| 12 | 2.50 | 3.5 | 5.9-6.1 |
| 20 | 2.70 | 3.8-3.9 | 6.8-7.5 |
| 40 | 2.7-2.9 | 3.4-4.1 | 6.1-8.7 |

The true `c*` at the shore sits at 0.74-0.99 (§3b of
`results/FFP_LITERATURE_PASS.md`), so a bound that overshoots by 2.5 to 8.7 can
only certify where the truth has that much room — which is large `lam`, and that
is exactly the corner (E) reaches. **No improvement to the spectral-abscissa part
can change this**: even the exact Hurwitz test inherits the factor. Reaching the
physical small-`lam` region through (A) would need a transfer with loss under
about 1.05.

So the route is a better corner, honestly obtained, and a sixth measured dead end
for the keystone itself. The only line still standing with room in it is the one
that never passes through an inequality: the far-below manifest positivity plus
the neighbour repair (`results/FARBELOW_NEGATIVE_PATTERN.md`), which is an
identity-level argument.

## Status

Nothing here is promoted. (A) and (C) are external claims that our engine failed
to falsify on 144 cases; that is evidence, not proof, and the derivations behind
them were not audited line by line. The region measurement is ours and stands on
its own artefact.
