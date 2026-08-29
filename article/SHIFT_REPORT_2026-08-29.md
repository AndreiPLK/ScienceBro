# Shift report, 29 August 2026

Started on a literature pass, ended with a certificate. Times from `date`, numbers
from artefacts.

## Green, with numbers

**A proof where there was a measurement.** The far-below criterion has exactly one
negative coefficient, and grouping it with its neighbours reduces positivity to

    (R)  4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0.

(R) is UNCONDITIONAL (holds at all 504 region points, not only the 117 dips) and
**manifestly positive** — built exactly over `Q(sqrt3)` in variables that are all
nonnegative on the region, it expands with **zero negative monomials** at every
`J` from 7 to 29 (1322 to 5942 monomials), and at `J = 30` too once the region is
restricted to the regime the statement lives in. Nonnegative monomials over a
nonnegative orthant is a proof.

Combined with the one-negative-coefficient structure, that **closes the far-below
region at `j = 9, 10, 11, 12, 14`** — depths that previously needed the heavy
interval-Bernstein route.

**A structural fact the repository did not have.** `b_{n-k} = (2k-n)^2 = b_k`, so
the B-form's multiset is DOUBLED: `prod_k (u - b_k)` is a perfect square times at
most one linear factor, and `E_{2t}` is the self-convolution of a half-set of
`floor(n/2)` distinct values. Checked at 7 values of `n`, exact polynomial
identities at 5, 182 self-convolution checks, 0 mismatches.

**The literature question, answered.** Our transform is the finite free
multiplicative convolution — classically the **Schur–Szegő composition** (Szegő
1922, Walsh 1922). Verified as our object, not a lookalike: 336 cases, 0
mismatches, 65 with a negative reference knife. Novelty of the technique:
POSSIBLY_KNOWN -> KNOWN.

**One open piece, named.** A J-uniform (R) needs exactly one lemma about central
factorial numbers: `p_t^2/(p_{t-1}p_{t+1}) <= 1 + 2/n`. Stress-tested to `n = 200`
over all `t < n/2`: largest constant needed 1.9862, at the smallest `n`. Granting
it, the rest is elementary and holds on 78207 pairs.

## What remains, with reasons

* The other leg — every `c_k` with `k != J-2` nonnegative — is still a measurement.
  It holds on 1476 points tested both sides of its boundary, and the boundary is
  `n >= 2J-3`.
* Outside that regime several coefficients dip and one grouping is not enough.
* The keystone itself is untouched: all of this lives in the far-below region.

## What I need from you

Nothing. Two decisions were made without you and are reversible: the certificate
work took priority over the asymptotic route, and two pages were published as
artefacts.

## Where I was wrong today

Four of my own claims died, three of them by tests I wrote next to them.

* **ERR-0015** — "criterion S" had its conclusion inside its hypothesis
  (`A_0 = K_r`). True and empty.
* **ERR-0016** — "odd-`j` knives never dip": they do, 72 cases at small `lam`, on
  both engines. The limit I derived it from constrains infinity, not finite `D`.
* **ERR-0017** — the recorded depth law `j <= n/2+1` was fitted on
  `n = 12, 16, 20, 24, 28, 36, 44`, all multiples of four; over `n = 11..100` it
  fails in 70 of 90 rows. Withdrawn.
* **The doubling hypothesis** — that doubling explains the four half-depth
  boundaries. Refuted within the hour by the control I had named in the same
  paragraph: undoubled families of the same size sit at the same boundary.
* **"The dominant term wins"** — refuted by measurement: the rest exceeds it by 3
  to 3.2e8.
* **The J = 30 break** — my test domain, not the mathematics.

## What checks this now

* `lab/repair_certificate.py` — the certificate itself, per depth, as an artefact.
* `lab/farbelow_regime_map.py` — the regime law on a grid containing BOTH sides of
  its boundary, because a boundary inferred from corner scans is what ERR-0017 was
  about.
* `lab/depth_boundary_map.py` — the depth cutoff at EVERY `n`, including the odd
  ones the original run never touched.
* Two page builders that regenerate their pages from the artefacts and refuse to
  emit if the data stops supporting the claim.
* A rule in lab memory: before recording a law, check the sample can distinguish
  it from its nearest rival; and if a claim prunes a search, keep sampling the
  pruned branch.
* `moment_kernel_probe` no longer dies above `n ~ 100` — the int-to-string cap
  that kept these probes small is lifted at the source.
