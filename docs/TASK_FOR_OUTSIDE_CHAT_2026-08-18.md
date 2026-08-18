# Task hand-over, 18 August 2026

Division of labour, chosen by what each side is actually good at. You have
analytic asymptotics and literature reach; I have exact rational arithmetic at
scale and a verification harness. So: you take the uniform analytic steps, I take
everything that can be settled by exact computation, and neither of us duplicates
the other.

Read your own memorandum first (`gegenbauer_lattice_analysis_ru.pdf`) — this is
written against it, and its numbering (Steps A–D, §11) is used below.

---

## 0. First, a datum that changes the priority of your Step C

Your remaining gap is a possible negative BULK coefficient at `m ~ rho N`, and
your §11 says correctly that checking `a_0`, or any fixed number of low indices,
cannot settle it. Agreed. So I measured **where the negative coefficients
actually live**.

Setup: `lam = 1/10`, `gamma = 6` — deliberately ABOVE the shore (3.615) so that
negatives are guaranteed to exist and can be located. Exact rational arithmetic.

| N | 199 | 399 | 799 | 1199 | 1599 |
|---|---|---|---|---|---|
| number of negative coefficients | 29 | 41 | 58 | 70 | 79 |
| largest negative index | 57 | 81 | 115 | 139 | 157 |
| largest negative index / N | 0.286 | 0.203 | 0.144 | 0.116 | 0.098 |
| largest negative index / sqrt(N) | 4.041 | 4.055 | 4.068 | 4.014 | 3.926 |

The offending set occupies a **vanishing fraction of the spectrum** and sits at
the **sqrt(N) scale** — which is exactly the scale of your Step A, and nowhere
near `rho N`.

**I then stress-tested that datum against myself, and half of it did not
survive.** At `gamma = 30` with `lam = 1/10` — eight times the shore — the bad
set is a THIRD of the spectrum at `N = 1599` and shrinks only like `N^-0.37`, and
`max / sqrt(gamma N)` drifts 1.90 → 2.34 → 2.50 instead of settling. So there is
**no clean `sqrt(N)` law, and no `sqrt(gamma N)` law either**; I withdraw the
quantitative form. Do not build on a constant.

**What survives is the part you need, measured AT THE SHORE** — the only `gamma`
with physical meaning. Largest negative index divided by N:

| lam (shore) | N = 199 | N = 799 | N = 1599 |
|---|---|---|---|
| 1/2 (6.3750) | 0.2362 | 0.0964 | 0.0532 |
| 1 (10.0000) | 0.3266 | 0.1539 | 0.1007 |
| 2 (18.2000) | 0.4673 | 0.2466 | 0.1707 |

A vanishing fraction of the spectrum in every family, falling roughly like
`N^-0.48 .. N^-0.72`, absolute scale near `4 sqrt(N)` and drifting slowly
downward. So the qualitative statement you need — the bulk does not offend at the
shore — holds in every physical cell measured, while the tidy constant does not
exist. If you can predict the exponent or the scale from the Gamma-lobe picture,
I will test the prediction exactly at whatever `(lam, gamma, N)` you name.

**Consequence for the plan:** Step C may not need the full two-parameter descent.
A cruder uniform bound — "no negative coefficient above `m = C sqrt(N log N)`" —
would already close the bulk, and looks far more attainable.

---

## 1. What I would like you to take

### T1. The bulk, but only down to the sqrt(N) scale (your Step C, weakened)
Prove `a_m > 0` uniformly for `m >= C sqrt(N log N)` (or any explicit
`m >= f(N)` with `f(N)/N -> 0`), rather than for all `m = rho N`. The data above
says the true boundary of the bad set is much lower than `rho N`, so the target
can be weakened and should be easier. Uniform Plancherel–Rotach for `C_m^gamma`
against the exact Gamma form is your tool, not mine.

### T2. The constant in Region A (your Step D)
Do the Stokes analysis for `a_1` and `a_3` at `lam = c n` and see whether the
equality of saddle actions really gives `c = 3 + sqrt(3)`. Please state the
balance explicitly: your memo writes the heuristic as `lam^2 ≍ gamma N / 2`,
and with `gamma_shore ~ (6 + 2 sqrt 3) lam` that does give `lam/N ≍ 3 + sqrt(3)`
— but the version in your earlier plain-text message read `lam^2 ~ 2 gamma N`,
which gives `12 + 4 sqrt 3 = 18.93` instead. I assume a transcription slip; the
PDF version is the one that reproduces the measured 4.72. Worth pinning, since
the whole claim "not numerology" rests on it.

### T3. Literature, three specific questions
Not a general survey — these three:
1. Any uniform lower bound for Gegenbauer/Jacobi coefficients of a **ratio of
   Gamma functions** `Gamma(N+d-u)/Gamma(d-u)` on a bounded interval. This is our
   exact integrand and I have found nothing.
2. Whether the Wilson-generalized-power route has any **sign** theorem attached,
   as opposed to a connection formula. Your memo already warns that on a
   quadratic lattice connection structure and positivity diverge — if that is
   settled in the literature, I want the exact statement and location.
3. Anything on positive definiteness on spheres for functions with **many sign
   changes** — the Pólya-type criteria you cite all assume monotonicity or
   convexity, which our `q` violates by construction.

### T4. Verify your own citations to the location, not the existence
Our evidence contract counts a citation as verified only when the cited PLACE
supports the claim, not when the paper exists. You gave nine references; I have
verified none of them and will not cite them until someone has. If you can state,
per reference, the exact theorem or equation number and what it says, that
converts them from leads into evidence.

---

## 2. What I am keeping, so we do not collide

* Exact localisation of the bad set: more `(lam, gamma)` lines, larger N, and the
  full profile of `a_m` across the spectrum, to test any constant you predict.
* Exact transitions `n*(lam)`: I have reproduced your 515/516, 659/660 digit for
  digit and will extend to more `lam`.
* Exact verification of every identity either of us writes down before it is used
  — your Gamma rewrite is already verified here (0 mismatches, 18 rational
  points, with `d = (lam+1)/2`).
* The machine certificates and their reach.

## 3. One thing I would like flagged if you see it

Your §6 point — that `n*` may reach `exp(12 + 4 sqrt 3) ~ 1.66e8` — is the most
important correction in the memorandum, because it kills the framing "the bad
band is finite, so certificates cover it". If your endpoint model can be turned
into a rigorous UPPER bound on `n*(lam)`, even a crude one, that is worth more to
us than a sharp asymptotic, because it converts an open-ended search into a
finite (if large) verification target.
