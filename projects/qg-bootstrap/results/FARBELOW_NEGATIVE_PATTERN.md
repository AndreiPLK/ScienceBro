# Where the far-below criterion breaks, exactly

2026-08-29. `lab/farbelow_negative_pattern.py` ->
`results/farbelow_negative_pattern_j<J>.json`.

## The question

`lab/knife_farbelow2.py` proves knife positivity in the far-below region by
MANIFEST positivity: expand `N = (-1)^{J-1} B_j` at `D = T_cap - y` and check
that every monomial of every `y`-coefficient is nonnegative. It works for
`j = 4..8` and fails from `j = 9` — which is why `j = 9..17` were closed by the
heavier interval-Bernstein route instead (`knife*_farbelow_interval.json`).

The counts in the existing artefacts say how badly it fails:

| j | 9 | 10 | 11 | 12 |
|---|---|---|---|---|
| negative monomials | 11 | 30 | 41 | 71 |
| total monomials | 54331 | 84170 | 124881 | 178816 |

Two parts in ten thousand. That is not a wall; that is a list of exceptions. The
question is whether the list has a shape.

## It does, and the shape is a line

Rebuilt on the fast engine (`Q3Poly` over `Q(sqrt3)` via `knife_tail2.build_P`;
no new derivation, the same construction the certificates use), the negative
monomials are:

| j | count | y-degree | thL | K3 | v |
|---|---|---|---|---|---|
| 9 | 11 | **7 = J-2**, all of them | 0 | 0 | 0..10 |
| 10 | 30 | **8 = J-2**, all of them | 0 | 0 | 0..29 |
| 11 | 41 | **9 = J-2**, all of them | 0 | 0 and 1 | 0..37 |

So every failure of the criterion, at every `j` measured, lives in **one single
`y`-coefficient — the one of degree `J-2`** — and inside it, on the corner
`thL = 0`, `K3 = 0` (with two strays at `K3 = 1` for `j = 11`). All `J-1` other
coefficients are manifestly positive, monomial by monomial.

## Why this matters for the keystone

The programme's missing piece is uniformity in depth: every `j` from 4 to 17 has
its own certificate, and there is no single argument covering all `j`. This
localisation says what a uniform argument would have to do — not "handle the
general case", but:

1. show that the `y`-coefficients `c_0 .. c_{J-3}` are manifestly positive for
   every `j` (a statement about an explicit alternating sum of E-polynomials and
   Pochhammer weights, and it is what the machine already sees at `j = 4..11`);
2. handle `c_{J-2}` alone, where the negativity sits in a corner and must be
   dominated by a neighbouring power of `y` on the physical range.

That is a far smaller target than the general case, and it is the first time the
obstruction to uniformity has an address rather than a size.

## Why that coefficient and no other — a closed form

The localisation is not an accident of the region. Writing the tail factor as
`tail_i = PROD_{r=i}^{J-2} (A_r - y den)` with `A_r = tk_num + (c+2r) den`, the
`y`-expansion of `N = (-1)^{J-1} B` is

    [y^k] N = (-1)^{J-1+k} den^k SUM_{i <= J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                  den^i e_{J-1-i-k}(A),

an alternating sum over `i` with `J-k` terms. So:

* `k = J-1` has **one** term: `c_{J-1} = den^{J-1} E_{J-1} > 0`, positive by
  inspection;
* `k = J-2` has **exactly two, of opposite sign** — it is the first difference in
  the family:

      c_{J-2} = den^{J-2} [ poch_1 s^2 den E_{J-2} - E_{J-1} (J-1)(tk_num + den(c+J-2)) ],
      poch_1  = (2n-2J+1)(2n-2J+2)/2;

* every `k < J-2` has three or more terms, and their expansions come out with
  nonnegative monomials — which is the manifest positivity the criterion lives
  on.

**The two-term formula is verified against the assembled polynomial, not
asserted:** `j = 6`, 735 monomials, **0 mismatches**; `j = 9`, 1752 monomials,
**0 mismatches** (`results/farbelow_negative_pattern_j9.json`, field
`c_Jm2_closed_form_check`).

Dividing by `den` and using `T_cap = tk_num/den`, the sign of the exceptional
coefficient is decided by one explicit inequality:

    c_{J-2} > 0   <==>   (2n-2J+1)(2n-2J+2)/2 · s^2 · E_{J-2}
                          >  (J-1)(T_cap + 4n - 4J - 1 + J - 2) · E_{J-1}.

Both sides are elementary; the only non-elementary ingredient is the ratio
`E_{J-1}/E_{J-2}`, which Newton's inequalities bound by
`[n(n-2)/3](n-J+1)/(J-1)` — the same tool Theorem 5 of
`BFORM_POSITIVITY_THEOREM.md` runs on. And it explains the observed breakdown at
`j = 9` without any further computation: as `J` grows toward `n` the left side
carries `(2n-2J)^2` and shrinks, while the right side carries `(J-1)` and grows.

**What this does and does not give.** It does not restore the criterion — for
`j >= 9` the coefficient really is negative in that corner, which is why the
interval route was needed. What it gives is an explicit handle: `c_{J-2}` and
`c_{J-1}` are now both in closed form, so the natural repair
`y^{J-2}(c_{J-1} y + c_{J-2}) >= 0` becomes a threshold in `y` that can be
written down rather than searched for. Whether that threshold sits inside or
outside the physical range is the next thing to measure, and it is measured
nowhere yet.

## The repair the structure suggests, and its first measurement

With every `c_k >= 0` except `c_{J-2}`, positivity of `N(y) = SUM_k c_k y^k` on
`y >= 0` follows if the one negative term is absorbed by its two neighbours:

    c_{J-3} + c_{J-2} y + c_{J-1} y^2 >= 0  for y >= 0
      <==>  c_{J-2}^2 <= 4 c_{J-1} c_{J-3}   (discriminant),

and the stronger log-concave form `c_{J-2}^2 <= c_{J-1} c_{J-3}` is the discrete
Newton inequality on the coefficient sequence — the same shape of tool as
Theorem 5 in `BFORM_POSITIVITY_THEOREM.md`.

**First measurement (`j = 9`, 512 points of the region grid,
`thL, v, K3` in {0,1,2,3,6,12,40,200}):** 6 points have `c_{J-2} < 0`, and at
**every one of them both inequalities hold** — 0 discriminant failures, 0 failures
even of the stronger log-concave form. Away from those points the log-concave
form does fail sometimes, which costs nothing: where the coefficient is already
nonnegative there is nothing to repair.

So the candidate mechanism for uniformity in depth, in the far-below region, is
two explicit statements:

1. `c_k >= 0` monomial-by-monomial for every `k != J-2` and every `j`;
2. wherever `c_{J-2} < 0`, `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`.

Both are polynomial inequalities in the region variables, and `c_{J-1}`, `c_{J-2}`
are already in closed form above. **Neither is proved, and (2) is measured at one
depth only** — `j = 10, 11, 12` were queued and stopped when the founder's machine
went under the memory rule (a game was running); they are the first thing to run
next.

## The general coefficient, verified — and why J-2 is the weakest link

The two-term formula for `c_{J-2}` is the `k = J-2` case of

    [y^k] N = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                    den^i e_{J-1-i-k}(A_i..A_{J-2}),

`A_r = tk_num + (c+2r) den`, `poch_i = PROD_{q=1}^{2i}(2n-2J+q)/(i! 2^i)`. Checked
against the assembled polynomial for **every** `k` at `j = 6`: `k` = 0..5, 3186 /
2528 / 1890 / 1292 / 735 / 231 monomials, **0 mismatches at every k**
(`general_coefficient_formula` in the module).

That expression also says why `J-2` is where it breaks. The term with the highest
power of `s` is `i = J-1-k`, and its total sign is
`(-1)^{J-1+k}(-1)^{J-1-k} = +1` — **the dominant term is always positive**, for
every `k`. Manifest positivity is then the statement that this term's monomials
swamp the alternating remainder. The swamping is strongest for small `k`, where
the dominant term carries `s^{2(J-1-k)}` with `s ~ lam` large, and weakest for
`k = J-2`, where it carries only `s^2` against a term with none. `k = J-1` is
trivially safe because the sum has a single term.

So the two statements the uniformity argument needs are not arbitrary: (1) is
"the dominant term wins" for `k <= J-3`, a chain of ratio bounds of exactly the
kind Theorem 5 runs on, and (2) covers the one place where it cannot win.

## What is NOT claimed

Nothing here proves anything. This is a localisation of a known failure, measured
on 3 depths, and the `y`-degree pattern `J-2` is an observation over `j = 9, 10,
11` — three points. `j = 12` and up are running; the pattern is a hypothesis
until they land, and the artefacts are what will decide it, not this file.
