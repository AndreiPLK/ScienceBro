# (B) lives on a proper sub-cone of the PSD cone, not on the cone and not on the boundary

*2026-08-30. Artefact: `results/psd_cone_hypothesis.json`, module
`lab/psd_cone_hypothesis.py`. All arithmetic exact over `Q`.*

## The question

Our weights are `b_k = (a + kd)^2`, which is the **rank-one** case of a quadratic form

    b_k = (1  k) Q (1  k)^T = A + 2Bk + C k^2,     Q = [[A, B], [B, C]] >= 0.

Does (B) hold for every positive semidefinite `Q`? If so the mechanism is
quadratic-form positivity rather than the arithmetic progression, and cone-restricted
Rayleigh / K-Lorentzian machinery is the natural tool. If it holds only on the rank-one
boundary `B^2 = AC`, the mechanism is much narrower.

## The answer: neither

| regime | tested | failures |
|---|---|---|
| rank-one boundary (our case) | 300 | **0** |
| near the rank-one boundary | 300 | **0** |
| PSD interior | 300 | **15** |
| extreme ray `C = 0` (constant weights) | 25 | 0 |

**(B) is false on the PSD cone** — it fails in the interior. **But it is not confined to
the rank-one boundary either**: a whole neighbourhood of that boundary satisfies it.

Every interior failure had `B < 0` and a large `AC - B^2`, so the informative
parametrisation is by the height of the minimum. Writing

    b_k = C (k - v)^2 + h,      rho = h / (C * max_k (k-v)^2),

`rho = 0` is the perfect square and `rho` measures how far the quadratic sits above zero
relative to its spread. The critical `rho`, bisected to `10^-4` at the centred vertex
`v = N/2`:

| `N` | 10 | 12 | 14 | 16 | 18 | 20 | 24 | 30 | 36 | 44 |
|---|---|---|---|---|---|---|---|---|---|---|
| critical `rho` | 0.1223 | 0.1277 | 0.1314 | 0.1342 | 0.1364 | 0.1381 | 0.1407 | 0.1431 | 0.1446 | 0.1459 |

So **(B) holds on a proper sub-cone**: the quadratic must be close enough to a perfect
square, with a threshold that is scale-invariant (both `h` and the spread scale together),
hence genuinely a cone condition — just a narrower cone than PSD.

## What this settles for the proof programme

* The **cone idea is right in kind** — the condition is scale-invariant, so cone-restricted
  Rayleigh / K-Lorentzian machinery is the right family of tools.
* The **cone is not the PSD cone**, so a theorem quantified over all PSD `Q` cannot be what
  proves (B), and looking for one is wasted effort.
* Our case `rho = 0` sits comfortably in the interior of the valid region, not on its
  boundary, which is reassuring: (B) for the centred squares is not a knife-edge fact.

## A constant I am not claiming

A fit `rho*(N) = a - b/N` on `N = 10..24` gives `a = 0.15375`, which is within `10^-4` of
`2/13 = 0.153846`. That is not a result. Tested by **prediction rather than by fitting** —
the honest test — the fit drifts: at `N = 30, 36, 44` the errors are `0.00022`, `0.00045`,
`0.00072`, growing steadily. So the `1/N` form is incomplete and the limiting constant is
not pinned beyond "somewhere near `0.15`". The `2/13` coincidence is recorded only so that
nobody rediscovers it and believes it.

## Method note

The test was run on the same domain (B) is stated on, `1 <= t <= floor(N/2)`. Testing past
the midpoint would have reported failures outside the statement — a mistake this lab has
already paid for once, and the reason the domain is now written into every such module.
