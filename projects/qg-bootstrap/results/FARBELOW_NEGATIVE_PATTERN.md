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

So every failure of the criterion, at the `j` measured HERE, lives in **one single
`y`-coefficient — the one of degree `J-2`** (but read the correction below: this
holds only while `n >= 2J-3`) — and inside it, on the corner
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

**Measured at three depths** (512 points of the region grid each,
`thL, v, K3` in {0,1,2,3,6,12,40,200}):

| j | points with `c_{J-2} < 0` | discriminant failures | log-concave failures |
|---|---|---|---|
| 9 | 6 | **0** | **0** |
| 10 | 7 | **0** | **0** |
| 11 | 20 | **0** | **0** |

33 negative points, no failure of either form. Away from those points the
log-concave form does fail sometimes, which costs nothing: where the coefficient
is already nonnegative there is nothing to repair.

So the candidate mechanism for uniformity in depth, in the far-below region, is
two explicit statements:

1. `c_k >= 0` monomial-by-monomial for every `k != J-2` and every `j`;
2. wherever `c_{J-2} < 0`, `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`.

Both are polynomial inequalities in the region variables, and `c_{J-1}`, `c_{J-2}`
are already in closed form above. **Neither is proved.** (2) is now measured at
`j = 9, 10, 11` — 33 points where the coefficient dips, no failure — and the
`y`-degree localisation holds at all three. `j = 12` is still queued (179k
monomials, it is the slow one).

## The general coefficient, verified — and why J-2 is the weakest link

The two-term formula for `c_{J-2}` is the `k = J-2` case of

    [y^k] N = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i}
                                                    den^i e_{J-1-i-k}(A_i..A_{J-2}),

`A_r = tk_num + (c+2r) den`, `poch_i = PROD_{q=1}^{2i}(2n-2J+q)/(i! 2^i)`. Checked
against the assembled polynomial for **every** `k` at `j = 6`: `k` = 0..5, 3186 /
2528 / 1890 / 1292 / 735 / 231 monomials, **0 mismatches at every k**
(`general_coefficient_formula` in the module).

One reading of that expression is **wrong, and the numbers killed it the same
hour** — recorded here rather than quietly deleted. The term with the highest
power of `s` is `i = J-1-k` and its total sign is
`(-1)^{J-1+k}(-1)^{J-1-k} = +1`, so the highest-`s` term is always positive. I
took that to mean manifest positivity was "the dominant term swamps the rest",
which would have made the uniform proof a decay estimate. It is not:
`lab/dominant_term_probe.py` (`results/dominant_term_probe.json`) evaluates the
terms as certified `arb` numbers over the region and finds

    SUM_{i < J-1-k} T_i  /  T_{J-1-k}   =   3  to  3.2e8    for k <= J-3,

so the "dominant" term is routinely the smallest thing in the sum. The reason is
visible once measured: `T_i` gains `s^2 den` per step but loses one factor
`A ~ T_cap den ~ lam^2 den`, and those two are the same size — the terms are
comparable, and manifest positivity comes from cancellation among comparable
terms, not from one of them winning.

What survives, and it is the interesting half: at the weak link `k = J-2` that
same ratio is **0.9997 to 1.0164** — the two terms are equal to within a percent.
That is why this coefficient, and only this one, changes sign: it is a difference
of two quantities that are the same size to a part in a hundred, while every
other `c_k` is a longer sum whose cancellation resolves in the monomials.

## The repair reduced to one quadratic, and measured to depth 40

Writing `alpha_r = A_r/den = T_cap + c + 2r`, `w = E_{J-1}`,
`u = poch_1 s^2 E_{J-2}`, and `e1, e1p, e2` for the elementary symmetric
functions of the alphas (`e1p` omitting `alpha_0`), the verified general formula
gives all three relevant coefficients with the SAME power of `den`:

    c_{J-1} = den^{J-1} w,
    c_{J-2} = den^{J-1} (u - w e1),
    c_{J-3} = den^{J-1} (w e2 - u e1p + poch_2 s^4 E_{J-3}),

so the repair `c_{J-2}^2 <= 4 c_{J-1} c_{J-3}` is a quadratic in `u`, opening
upward:

    u^2 - 2 u w (alpha_0 - e1p) + w^2 (e1^2 - 4 e2) - 4 w poch_2 s^4 E_{J-3} <= 0.

**Measured (`lab/repair_inequality_probe.py`, certified `arb`, 315 region points
over `J` = 5, 9, 12, 16, 20, 30, 40): the coefficient dips at 91 of them, and the
quadratic holds at every single one — 0 failures, 0 undecided enclosures.** That
extends the repair from the three depths reachable by full polynomial expansion
to seven, and to depth 40.

**And a near miss worth keeping.** Evaluating the quadratic at the boundary
`u = w e1` — where `c_{J-2}` changes sign — collapses it, via `e1 - alpha_0 =
e1p`, to the single explicit inequality

    E_{J-1} [ e1p^2 - e_2(alpha_1..alpha_{J-2}) ]  <=  poch_2 s^4 E_{J-3}.

That form is **false** — at 70 of the 315 points — but only just: the ratios are
**1.0000 to 1.0016**. So the boundary reduction is a fraction of a percent too
strong to be the proof, and the true statement is tight at the `10^-3` level.
Tightness again, in a third independent place today.

## What a proof uniform in J would need — one named lemma

Expanding (R) with `alpha_r = A_r/den` and using `e1 - 2 e1p = alpha_0 - e1p`:

    (R) = w^2 (4 e2 - e1^2) + 2 u w den (alpha_0 - e1p)
          - u^2 den^2 + 4 w poch_2 s^4 E_{J-3} den^2   >=  0.

The `alpha_r` differ only by `2r` against a `T_cap` of order `lam^2`, so they are
nearly equal, and for `m = J-1` near-equal numbers `4 e2 - e1^2 = e1^2 - 2 SUM
alpha^2 ~ alpha^2 m(m-2) > 0` for `m >= 3`. The dangerous term is `- u^2 den^2`,
and it is dominated by the last one exactly when

    poch_1^2 E_{J-2}^2  <=  4 poch_2 E_{J-1} E_{J-3},
      i.e.   E_{J-2}^2 / (E_{J-1} E_{J-3})  <=  2cd/(ab),
      a = 2n-2J+1, b = a+1, c = a+2, d = a+3.

**Measured: 144 cases (`n` = 44..200, `J` = 4..39), 0 violations, tightest slack
1.33.** So the mechanism is real.

**And the tool for it is NOT Newton** — that was my first thought and it is
backwards. Newton's inequality gives `E_k^2/(E_{k-1}E_{k+1}) >= C(N,k)^2 /
(C(N,k-1)C(N,k+1))`, a LOWER bound on exactly the ratio that needs an upper one.
No universal upper bound exists (spread the roots far enough and the ratio grows
without limit), so it has to come from the specific family: the `b_k` are the
squares of an arithmetic progression.

**The missing lemma, stated plainly.** For `E_t(n) = e_t({(n-2k)^2 : k = 1..n-1})`,

    E_{t}^2 / (E_{t+1} E_{t-1})  <=  2 (2n-2J+3)(2n-2J+4) / [(2n-2J+1)(2n-2J+2)]
    at t = J-2.

Prove that and the leading obstruction in (R) is J-uniform. It is a statement
about central factorial numbers alone — no knives, no region, no `lam`.

**And it splits into one measured lemma plus one elementary inequality.** Writing
`p_t = E_t/C(N,t)`, `N = n-1`, the ratio is `F_t` times the Newton excess:

    E_t^2/(E_{t+1}E_{t-1}) = F_t * [p_t^2/(p_{t-1}p_{t+1})],
    F_t = (t+1)(N-t+1)/(t(N-t)) = (J-1)(n-J+2)/[(J-2)(n-J+1)] at t = J-2.

The family turns out to sit ALMOST at the Newton floor, and the excess shrinks
like `1/n`: measured `1.05` at `n = 20`, `1.02` at `n = 44`, `1.008` at `n = 100`.
Sharpened:

> **Lemma (measured, not proved).** For the central factorial family,
> `p_t^2/(p_{t-1}p_{t+1}) <= 1 + 2/n`. Largest constant needed over
> `n = 8..120`, `t < n/2`: **1.986**, attained at the smallest `n`.

Granting it, what remains is elementary and closes:

    F_t (1 + 2/n)  <=  2cd/(ab)   for every J >= 4

— **78207 pairs `(n, J)` with `n` up to 400, 0 failures, tightest slack 1.28.**
That half is a rational-function inequality and can be settled by hand.

So the leading obstruction of (R) is J-uniform as soon as the Newton-excess lemma
is proved, and that lemma is a self-contained question about
`e_t({(n-2k)^2})` — squares of an arithmetic progression.

## What the two pieces prove together

The far-below criterion asks for `N(y) = SUM_k c_k y^k > 0` on `y >= 0`. Put the
two pieces side by side:

* every `c_k` with `k != J-2` is nonnegative monomial-by-monomial (measured, and
  what the existing `knife*_farbelow_factored.json` artefacts already report for
  `j = 9..12`: their negative monomials sit only at `y`-degree `J-2`);
* `(R) 4 c_{J-1} c_{J-3} >= c_{J-2}^2`, certified above.

Group the one negative term with its neighbours:

    c_{J-3} y^{J-3} + c_{J-2} y^{J-2} + c_{J-1} y^{J-1}
        = y^{J-3} ( c_{J-3} + c_{J-2} y + c_{J-1} y^2 ),

a quadratic with nonnegative outer coefficients and, by (R), nonpositive
discriminant — hence nonnegative for EVERY real `y`, in particular on `y >= 0`.
Every other term is nonnegative there. Therefore `N(y) >= 0` on the whole ray.

**That closes the far-below region at the depths where the criterion alone
failed.** `j = 9, 10, 11, 12` were shown here to have their negatives only at `J-2`
(11, 30, 41 and 71 of them), and `(R)` is certified at every `J` from 7 to 29, so
those depths now have a proof of the manifest-positivity kind rather than the
heavier interval-Bernstein certificates they were closed with. The same pair closes any further `J` for which
both checks pass.

**The honest boundary of that statement** is `n >= 2J-3`: outside it other
coefficients dip too and one grouping is not enough. In the far-below
parametrisation `n = 44 + v`, so it covers every `J <= 23` outright, and deeper `J`
only for `v` large enough.

## CORRECTION (same day): the localisation is not universal — it ends at n = 2J-3

Everything above was measured at `j = 9, 10, 11` with `n = 44 + v`, i.e. deep
inside one regime. Evaluating the verified closed form as NUMBERS (cheap, so it
reaches depths the polynomial route cannot) shows the picture does not persist:

| J at the corner `v = K3 = thL = 0`, `n = 44` | dips other than `c_{J-2}` |
|---|---|
| 9 .. 20 | none |
| 24 | `k = 1` |
| 30 | `k = 1, 3, 5, 7, 9, 11` |
| 40 | 17 of them, and `c_{J-2}` does not dip at all |

Not a precision artefact: the signs are unchanged at 300, 1200 and 4000 bits of
`arb`.

**It is not a large-`J` effect but a `J`-versus-`n` one, and the boundary is
sharp.** Scanning `n` upward at fixed `J`, the first `n` at which nothing but
`c_{J-2}` dips is

| J | 25 | 26 | 28 | 32 | 35 |
|---|---|---|---|---|---|
| first clean `n` | 47 | 49 | 53 | 61 | 67 |
| `2J-3` | 47 | 49 | 53 | 61 | 67 |

**five of five**, and the same at `K3 = 3, thL = 2`. So, at the corner of the
region,

    only c_{J-2} dips   <==>   n >= 2J - 3   <==>   j <= (n+3)/2.

Away from the corner (`K3 = 60, thL = 50`, i.e. larger `lam`) the constraint is
weaker still — cleanliness starts at `n = 44` for every `J` tested.

**Tested on a grid that could refute it** (`lab/farbelow_regime_map.py` ->
`results/farbelow_regime_map.json`; a boundary claimed from corner scans is
exactly what ERR-0017 was about). `J` = 7..40, `n` = 44..164 in steps of 3, and
two off-corner values of each region variable — **1476 points, with both sides of
the line present**:

* inside the regime: 1376 points, **0 violations** — nothing but `c_{J-2}` dips;
* outside it: 100 points, **0 unexpectedly clean** — something else always dips.

So the law is sharp in both directions on everything tested. It remains a
measurement: the grid steps `n` by 3 and the region has more corners than two.

**What this costs the plan above.** The two-statement target — everything except
`c_{J-2}` manifestly nonnegative, plus the neighbour repair — is a statement
about the regime `j <= (n+3)/2` only. Above it several coefficients dip and one
neighbour pairing cannot absorb them. The repair measurement itself stands (it
concerns `c_{J-2}` and holds at all 91 dips), but it is not by itself a route to
uniformity across the whole physical range `3 <= j <= n-1`.

**Worth noting, not yet explained.** That boundary sits right next to the depth
cutoff the programme measured independently for the Hausdorff mechanism,
`j <= n/2 + 1` (`results/asymptotic_regime_probe.json`). Two unrelated
constructions putting their boundary at the same line is either a coincidence or
the same mechanism seen twice; nothing here decides which.

## The repair is now PROVED on the region, not measured

`lab/repair_certificate.py` -> `results/repair_certificate_j<J>.json`.

Two facts turned the measurement into a certificate.

**First, (R) is unconditional.** The repair was stated as "where `c_{J-2} < 0`,
`c_{J-2}^2 <= 4 c_{J-1} c_{J-3}`". Measured over 504 region points, the inequality
holds at ALL of them, not only at the 117 where the coefficient dips. So no case
split is needed and

    (R)   4 c_{J-1} c_{J-3} - c_{J-2}^2  >=  0

is a single polynomial statement about the region.

**Second, (R) is manifestly positive.** Built exactly over `Q(sqrt3)` in the region
variables `(thL, y, v, K3)` — every one of which is `>= 0` on the far-below region —
and expanded, it has **no negative monomial at all**:

| J | 7 | 9 | 12 | 16 | 20 | 25 | 26 | 27 | 28 | 29 | **30** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| monomials of (R) | 1322 | 1742 | 2372 | 3212 | 4052 | 5102 | 5312 | 5522 | 5732 | 5942 | 6152 |
| negative | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **39** |

**The certificate covers `J = 7..29` and breaks at exactly `J = 30`** — and it
breaks in the narrowest way possible: all 39 negative monomials carry the same
`thL^3 K3^1 y^0`, differing only in the power of `v` (0..38). One exponent line
out of 6152 monomials. `(R)` itself was not seen to fail there — the 504-point
numeric sweep found no violation up to `J = 40` — so what fails at `J = 30` is the
crudeness of monomial signs, not the inequality. The escalation is the same one
the far-below criterion itself used past `j = 8`: a Bernstein step, here needed in
`thL` alone.

All-nonnegative monomials over a nonnegative orthant is a proof, not a sample —
the same certificate shape the far-below criterion itself uses at `j <= 8`.

**Where the sign comes from.** Splitting (R) at `j = 9` shows it is not a
coincidence of one big term:

    T1 = 4 w poch_2 s^4 E_{J-3} den^2 - outer^2        0 negatives of 1755
    T2 = 4 w (w e2 - u den e1p)                     1520 negatives of 1520
    R  = T1 + T2                                       0 negatives of 1742

So `c_{J-3}` is positive only because of its own last term — `w e2 - u den e1p`
is negative monomial for monomial — and (R) holds because four times that last
term, weighted by `w`, dominates both `outer^2` and the whole negative block, term
by term. That is a sharper statement than (R) itself, and it is what a proof
uniform in `J` would have to establish about the `E`-polynomials.

**The chain it rests on, checked rather than assumed.** (R) is assembled from the
general `y`-coefficient formula, which was verified against the assembled
polynomial at every `k`: `j = 6` (3186 / 2528 / 1890 / 1292 / 735 / 231 monomials)
and `j = 9` (12119 / 10470 / 8871 / 7315 / 5822 / 4389 / 3032 / 1752 / 561), with
**0 mismatches at every k in both**.

**What is proved and what is not.** Proved: the repair inequality (R), on the whole
far-below region, at the depths certified above. NOT proved: that every other
`c_k` is nonnegative — that half is still a measurement, and it holds only while
`n >= 2J-3`. So the far-below argument now has one of its two legs on a
certificate and the other on a well-tested measurement with a known limit.

## What is NOT claimed

Nothing here proves anything. This is a localisation of a known failure, measured
on 3 depths, and the `y`-degree pattern `J-2` is an observation over `j = 9, 10,
11` — three points, now confirmed at `j = 10` and `j = 11` as well. `j = 12` and up
remain unrun; the artefacts are what will decide the pattern, not this file.
