# Domain-critic review of the B-form / derivative-form positivity theorem

2026-08-28. Reviewer role: domain critic (not an accredited physicist or
mathematician; no literature access was used in writing this file, see the
caveat in §2.0). Target: `results/BFORM_POSITIVITY_THEOREM.md`, read against
`results/asymptotic_regime_probe.json`, `results/cancellation_bound_sweep.json`,
`results/KERNEL_TP_THEOREM.md`, `results/pairing_structures_probe.json` and
`research/BRIEF_KEYSTONE_FOR_OUTSIDE_HELP.md`.

**Everything numerical in this file that is not quoted from an artifact is my
own hand arithmetic at float precision.** It is orientation, not evidence. A
runnable float-level check script is parked at
`/tmp/claude-0/-home-user-ScienceBro/4b1f12bb-6f6b-5496-a404-cc35308b4fb8/scratchpad/check.py`;
anything that survives it must then be redone in exact arithmetic before it is
used for a claim.

---

## VERDICT (read this and nothing else, if nothing else)

**Present it as progress. Present it as STRUCTURAL progress, not as coverage
progress.** The coverage number (`lam ~> 3 n^2`) is the weakest thing in the
file and should never be the headline. The strong thing is the representation:
the CHR knife turns out to be a *Beta average of the m-th derivative of an
explicit real-rooted polynomial*, and that representation explains a fact the
programme has so far only measured (the odd-`j` / even-`j` parity dichotomy).
That is worth more than the theorem it currently supports.

Defensible wording:

- YES: "the first all-depths positivity region obtained from an argument rather
  than from a search";
- YES: "a representation of the knife as a one-dimensional integral of a
  real-rooted polynomial against an explicit Beta measure, verified against the
  reference engine";
- YES: "the proved region does not yet reach the physically interesting part of
  the domain";
- NO: "progress toward the keystone in the physical regime" — it is not in the
  physical regime (see §1.3, §1.4);
- NO: "proved the keystone in a region" without immediately stating that the
  region excludes `lam = 1`, the Virasoro-Shapiro point, at every level `n >= 6`
  (§1.4);
- NO: any use of "new / novel / first" for the transform itself (§2).

Claim state: leave at **source-supported by internal derivation and machine
verification**, exactly where the file puts it. Nothing here changes that.

Three specific defects found, in order of importance:

1. **The headline region is the file's own worst case and it undersells the
   result.** Condition `(*)` is depth-resolved; only the deepest knife
   `r = n-2` costs `n^2`. My hand arithmetic says the per-depth law is
   `lam* ~ (2 + 2/sqrt(3)) * r * n = 3.1547 * r * n` — **linear in `n` at each
   fixed depth**. At `n = 20`, `j = 3` that is `lam* ~ 86` against the
   all-depths `1069` in the file's table. Reporting only the max over depth
   throws away a factor of `n`. (§1.2)
2. **The bound's worst depth is not the empirically hard depth.** `(*)` is
   binding at `r = n-2`; `results/cancellation_bound_sweep.json` says the
   cancellation peaks at *intermediate* depth and falls back at large `j`
   (`n = 40, lam = 7`: 0.954 at `j = 14`, 0.54 by `j = 24`). So the theorem is
   at its most lossy exactly where the problem is easiest. That is where the
   cheap improvement is. (§1.2, §3.4)
3. **Two arithmetic slips**, both harmless to the conclusions but both wrong as
   written, and one of them is duplicated into `KERNEL_TP_THEOREM.md`. (§0)

---

## 0. Two arithmetic slips to fix before anyone else reads these files

**Slip A (appears twice).** `BFORM_POSITIVITY_THEOREM.md` Lemma 3 and
`KERNEL_TP_THEOREM.md` Corollary both write

    H - 2r + 1  =  (D-1)/2 + 2(n - 2 - r).

With `H = (D + 4n - 7)/2`:

    H - 2r + 1 = (D + 4n - 4r - 5)/2 = (D-1)/2 + 2(n - 1 - r),

so the correct offset is `n - 1 - r`, not `n - 2 - r`. The written version is
smaller than the truth, so every conclusion drawn from it (positivity of the
factor) still holds; it is a conservative slip. Fix it anyway: a reader who
checks one line and finds it wrong stops checking the rest.

**Slip B.** Theorem 6: "`H/2 = (D+4n-7)/4 > n-2` **exactly when** `D > 3`".
`(D+4n-7)/4 > n-2` reduces to `D > -1`. The vertex condition therefore holds on
the whole physical domain and is not equivalent to `D > 3`. The theorem is
unaffected (a fortiori), but "exactly when" is a false statement.

Neither slip touches the machine checks, which is itself a small warning: the
verification battery checks *identities and implications*, not the *prose
justifications*. That is normal and fine, but it means the prose is the
unverified part and should be re-read line by line.

---

## 1. SIGNIFICANCE: is `lam ~> 3 n^2` real progress or a consolation prize?

### 1.1 What the region actually is, in the project's own coordinates

`D*(n,lam) = (6n-9)s^2/(n(n-2)^2) - 2n + 3` with `s = lam+n-1`. For large `lam`
this is `~ 6 lam^2/(n-2)^2`, growing quadratically in `lam`; the shore grows
linearly, `T_hat(lam) -> (12 + 4 sqrt 3) lam ~ 18.93 lam`. Setting them equal
gives (hand arithmetic)

    lam*(n) / n^2  ->  (12 + 4 sqrt 3)/6  =  2 + 2/sqrt(3)  =  3.15470...

which is exactly the "still drifting upward at n = 100" (2.67, 2.81, 2.91,
2.99, 3.06) in the file's table. **Recommendation: state the limit constant.**
An asymptote you can name is worth more than a table that visibly has not
converged, and it is a cheap exact-arithmetic check (the file already has a
certified shore evaluator).

Inverted, the region is: **for a fixed coupling `lam`, the theorem covers levels
`n <~ sqrt(lam/3.155) = 0.563 sqrt(lam)`.** That is the honest reading. It is a
finite set of levels per coupling. The keystone needs all levels.

### 1.2 The headline number is the worst case over depth, and that is a mistake

Condition `(*)` is `r(H-r) n(n-2) <= (3n - 9/2) s^2`. Theorem 6 maximises the
left side over `r` and reports one `lam`-threshold. But at fixed depth the
condition is far weaker. Putting `D = T_hat ~ (12+4sqrt3) lam` and `s ~ lam` in
`(*)` (hand arithmetic, large `n` and large `lam`):

    r * (6 + 2 sqrt 3) * lam * n^2  <=  3 n lam^2
    =>  lam  >~  (6 + 2 sqrt 3)/3 * r * n  =  3.1547 * r * n.

Two consistency checks that this constant is right: at `r = n-2` it reproduces
`3.1547 n^2`, i.e. §6's table; and at `n = 20, r = 2` it gives `lam* ~ 126`
while a direct evaluation of `(*)` at `n=20, r=2` gives `lam* ~ 86` (the
asymptotic constant overshoots at small `r`, as expected). Either way:

| statement | region at the shore |
|---|---|
| proved, depth `j` fixed | `lam >~ 3.15 (j-1) n` — **linear in n** |
| proved, all depths (`j = n-1` binding) | `lam >~ 3.15 n^2` |
| measured (Hausdorff), `j <= n/2+1` | `lam >~ 2n` |

So at fixed shallow depth the proved region is within a **small constant factor**
of the measured Hausdorff region, not a factor of `n`. At `n = 20`: proved
`lam >~ 86` for `j = 3`, measured `lam >~ 40` for all `j <= 11`. That is a
respectable comparison and the file currently hides it behind its own worst
case. **Report `lam*(n, j)` as a table over depth, not a single number.**

The cost of the uniform-in-depth statement is entirely the deepest knife, and
§3.4 argues that the deepest knife is *not* the hard one, so this is loss, not
difficulty.

### 1.3 Is the region physically interesting? Mostly no, and it is worse than "an
asymptotic corner"

The programme's own scaling variable is `rho = n/lam` (`research/BRIEF...` §2a).
The shore asymptote `12 + 4 sqrt 3` is attained at `rho = sqrt 3`, i.e. levels
`n ~ 1.73 lam`. The proved region is `lam >~ 3.15 n^2`, i.e.
`rho <~ 1/(3.15 n) -> 0`.

**The proved region is the `rho -> 0` corner, and the shore is defined by the
physics at `rho = sqrt 3`.** These are disjoint regimes. Concretely: the shore
`T_hat(lam) = min_k T_k(lam)` is minimised at `k ~ sqrt(3) lam`; the levels the
theorem covers are `n ~ 0.56 sqrt(lam) << sqrt(3) lam`. Those are exactly the
levels whose own constraints are far from binding. The theorem proves positivity
for the slack constraints and says nothing about the ones that set the boundary.

On degeneracy: `mu(n) = 1 + (n-1)/lam`, so in the proved region the first `n`
levels are spread over `(n-1)/lam <~ 1/(3.15 n)` — they crowd toward `mu = 1` as
`n` grows. I would call that a near-degenerate corner of the spectrum, but I
have **not** verified from the CHR paper (PRD 111, 086034) what the `lam -> inf`
limit of the amplitude family is, and I will not assert that the family
"degenerates" as a physics statement. What I will assert, because it is internal
to this repo: `research/gravity-card.md` records that for `D >= 9` positivity
bounds `lambda` **from below**, i.e. large `lam` is the *allowed* direction and
the interesting edge is at small/moderate `lam`. The theorem covers the deep
interior of the island, far from the edge the programme is trying to draw.

### 1.4 The blunt version: the theorem is empty at the shore where the project
actually computes

Hand arithmetic on `max_n D*(n, lam)` against `T_hat(lam)` (`D*` is maximised at
`n = 4`, the smallest level with a nonempty knife range, and decreases in `n`):

| lam | `max_n D*` | `T_hat` | reaches shore? |
|---|---|---|---|
| 1 | 10.0 (n=4) | 23 | no |
| 5/2 | ~21 (n=4) | ~44 | no |
| 7 | 88.8 (n=4) | ~131 | no |
| ~14 | ~266 (n=4) | ~263 | first crossing |

So: **at every `lam` used in `cancellation_bound_sweep.json` and
`pairing_structures_probe.json` (`1/10, 1, 5/2, 7`), the theorem proves nothing
at the shore, at any level.** The first level to reach the shore anywhere is
`n = 4` at `lam ~ 14`. In particular the configurations where the programme
measured cancellation ratios of 0.95 (`n = 40, lam = 7`) are entirely outside
the theorem.

Worse, at `lam = 1` — the Virasoro-Shapiro point, the physically distinguished
member of the family — `D*(4,1) = 10`, `D*(5,1) = 4.67`, `D*(6,1) = 1.125 < 3`.
**At `lam = 1` the theorem is vacuous for every level `n >= 6`**, and at `n = 4`
it gives `D <= 10`, which is inside the range already covered for all `n` and
all `j` by Mansfield arXiv:2502.20372 (`D <= 10`), as recorded in the brief.

Combining: the theorem's genuinely *new* content is the strip `D` in
`(10, D*(n,lam)]`, which is nonempty only when
`6 s^2/(n-2)^2 - 2n > 10`, i.e. roughly `lam >~ 0.6 n^{3/2}` (hand arithmetic;
`lam >~ 33` at `n = 20`). So there are three nested regimes and they should all
be stated:

- `lam <~ 0.6 n^{3/2}`: the theorem adds nothing beyond the cited `D <= 10`
  literature;
- `0.6 n^{3/2} <~ lam <~ 3.15 (j-1) n`: new content in `D`, but not up to the
  shore;
- `lam >~ 3.15 (j-1) n`: keystone statement proved at depth `j`.

(The Mansfield range is taken from `research/BRIEF_KEYSTONE_FOR_OUTSIDE_HELP.md`
§6; I did not read that paper and it should be re-verified before this
comparison is used outward-facing.)

### 1.5 So: progress or consolation prize?

**Both, and the file should say which part is which.**

Consolation-prize part: the coverage claim. It is a corner, it excludes the
distinguished point of the family, it is disjoint from the regime that defines
the shore, and it is strictly weaker in `lam` than a mechanism the project has
already *measured*. Anyone hostile will find §1.4 in ten minutes.

Real-progress part, and it is real:

1. **`c_t` carries no `lam`.** Stronger than the file says: writing
   `b_k = B v_k` with `v_k = ((n-2k)/(n-2))^2` and `B = (n-2)^2/s^2`, the
   `v_k` depend on `n` **only**. All of the `lam` dependence in the entire knife
   sits in the single scalar `B in (0, ((n-2)/(n-1))^2)`, and all of the `D`
   dependence sits in the single scalar `eps`. A four-parameter problem
   `(n, j, lam, D)` becomes `(n, r)` integers plus two bounded scalars. That is
   a genuine reduction and it is the thing to sell.
2. **The `v_k` are an exact squared uniform grid.**
   `v_k = (1 - 2(k-1)/(n-2))^2`, so the empirical distribution of `b/B` is
   exactly the law of `U^2` with `U` uniform on `[-1,1]`, for every `n` and
   every `lam`. Density `1/(2 sqrt v)` on `[0,1]`. This is what makes the
   finite-free-probability route in §3.3 computable in closed form.
3. **The derivative form explains the parity dichotomy** (§3.1). That is the
   single strongest argument that this representation is the right object, and
   it is currently not in the file at all.

---

## 2. PRIOR ART: is this transform a known genre?

### 2.0 Caveat, stated first

I have **not** run a literature search for this review. Everything in §2 is
recall, and recall is exactly the failure mode that produces false novelty
claims. Treat every name below as a *pointer to check*, not as evidence, and do
not put any of it into an evidence record without a real source with an exact
location. My confidence that the *combination* is known in some form is high;
my confidence in any specific attribution is moderate at best.

### 2.1 What the transform is, stripped of the physics

Let `p(u) = prod_{k=1}^{N} (u - b_k)`, all `b_k >= 0`, `N = n-1`. The object is

    K_r  =  L[ P ],   P(y) = prod_k (1 - b_k y) = sum_t (-1)^t e_t(b) y^t,

where `L` is the linear functional `y^t -> c_t` with
`c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t]`. This factors into two operations:

- **(i) a truncation-by-differentiation.** The factor `w_t = (r)_t/(n-1)_t` is
  `C(N-t, N-r)/C(N,r)`, a polynomial of degree `m = N-r` in `t`. Multiplying
  Taylor coefficients by a polynomial in the index of degree `m` is exactly `m`
  applications of the Euler operator `y d/dy`, and here it assembles into a
  plain `m`-th derivative of `p`.
- **(ii) a Pochhammer-ratio multiplier.** The remaining
  `d_t = (H-r)_t/(n-3/2)_t = (C+eps)_t/(C)_t` is a ratio of falling factorials
  = a ratio of Gammas = a Beta integral, i.e. `d_t` is a **Stieltjes moment
  sequence** and `L` is an integral operator.

Both operations are classical, and so is the idea of composing them.

### 2.2 Names to check, in decreasing order of how sure I am

**(a) Malo-Schur-Szego composition theorems / Polya-Schur multiplier
sequences.** This is, I believe, the exact genre. `{e_t(b)}` for `b_k >= 0` is a
Polya frequency (totally positive) sequence — that is Aissen-Schoenberg-Whitney
(1952), and the generating-function characterisation is Edrei's theorem.
`{d_t}` is a moment sequence. Sums of the form `sum_t a_t d_t x^t` where `{a_t}`
comes from a real-rooted polynomial and `{d_t}` is a multiplier sequence are the
Schur composition setting, and Pochhammer-ratio sequences
`Gamma(a+t)/Gamma(c+t)` are among the textbook examples of multiplier sequences
of the first kind. **If a specialist recognises this file in one sentence, I
expect that sentence to be "that is a Schur composition with a Gamma-ratio
multiplier sequence".** Modern reference to check: Borcea-Branden's solution of
the Polya-Schur problem (Ann. of Math. 170 (2009); Invent. Math. 177 (2009)),
which classifies linear operators preserving real-rootedness / half-plane
stability. If `L` falls under their classification, statements about the *roots*
of `L[P]` are available off the shelf, which is a good deal more than the file
currently extracts.

**(b) Erdelyi-Kober / Weyl fractional integration; the Askey-Gasper method.**
The operator `y^t -> Gamma(C+eps+1)Gamma(C-t+1)/[Gamma(C+1)Gamma(C+eps-t+1)]`
is the standard Erdelyi-Kober fractional integral of order `eps` (equivalently a
Weyl fractional integral at infinity). "Write the sum as a fractional integral
of something manifestly nonnegative" is *precisely* the Askey-Gasper technique
that proved the Jacobi-sum positivity used in de Branges' proof of the
Bieberbach conjecture. The brief's own candidate route 3 says
"a positivity-preserving integral representation, the Askey-Gasper style" — this
IS that route, arrived at from the other end. That is a point in the result's
favour and should be said explicitly; it is also a reason to expect the
technique is known.

**(c) Finite free probability.** The file already names Marcus-Spielman-
Srivastava correctly. The specific facts to check: differentiation as a finite
free convolution (Marcus, "Polynomial convolutions and (finite) free
probability"); the MSS inverse-Cauchy-transform bound on the largest root of a
finite free convolution; the repeated-differentiation limit theorem
(Steinerberger; Hoskins-Kabluchko; Shlyakhtenko-Tao, "Fractional free
convolution powers"). Any statement about `max(eta)` must be checked here first
— see §3.3, where I give the closed-form prediction this literature makes for
*this* polynomial, and it matches the measured numbers to a few percent at large
`r`.

**(d) Newton / Maclaurin inequalities.** Theorem 5 is Newton plus a telescoping
ratio bound. Entirely textbook; the file says so. Turan-type inequalities are a
neighbouring but different genre (they are about orthogonal polynomial
sequences, not about `e_t` of a fixed point set); I would not cite them.

**(e) Hypergeometric summation.** Not a separate route, but a useful
degeneration: if all `b_k` were equal, `e_t = C(N,t) b^t` and `K_r` collapses to
a terminating `2F1(-r, ...; ...; b)`, i.e. a Jacobi polynomial evaluation.
See KAT-1 in §4 — that is a free known-answer test and it closes the loop with
the fact that the knives are Jacobi coefficients to begin with.

**(f) Askey-Wilson, Charlier.** I see no connection and would not invoke either.
Askey-Wilson is the `q`-level of the Askey scheme and nothing here is `q`-;
Charlier polynomials go with a Poisson weight and the weight here is Beta. If
someone wants these in the write-up they need a reason, not an association.

### 2.3 Verdict on novelty

The file's own assessment — **POSSIBLY_KNOWN for the technique, the CHR
application is the project's** — is correct, and if anything I would move the
technique to *likely known*: it is the composition of two operations each of
which has a name and a textbook. Keep the wording exactly as the file has it.
The two things I would defend as this project's own:

- that the CHR knife sum has a form in which all `b_k` lie in `[0, B]` with
  `B < 1` uniformly in `n` and `lam`, and in fact `b/B` is a *fixed*
  `n`-dependent squared uniform grid carrying no `lam` at all;
- the `(B, eps)` reduction and the parity explanation in §3.1.

Neither of those is a theorem about polynomials; both are observations about
this specific family. That is the right size of claim.

---

## 3. WHERE TO PUSH NEXT

### 3.0 First, a change of variable that makes everything easier

Substitute `x = 1/y` in Theorem 7's integral. Then

    dsigma(y) = [Gamma(C+eps+1)/(Gamma(C+1)Gamma(eps))] y^{-C-eps-1}(y-1)^{eps-1} dy
             =  [1/B(C+1, eps)] x^{C} (1-x)^{eps-1} dx  on  x in (0,1],

i.e. **`sigma` is a Beta(C+1, eps) distribution in disguise**, `C+1 = n-1/2`.
Therefore

    K_r  =  E_{x ~ Beta(n-1/2, eps)} [ x^{-r} prod_{i=1}^{r} (x - eta_i) ]
         =  E [ x^{-r} Q(x) ],   Q = monic m-th derivative of prod_k (u - b_k),

with `eta_i = B theta_i(n,r)`, where `theta_i` are the roots of the `m`-th
derivative of `prod_k (u - v_k)` and **depend only on `(n, r)` — not on `lam`,
not on `D`**. (Check of the moments: `E[x^{-t}] = B(C+1-t, eps)/B(C+1, eps)
= Gamma(C+eps+1)Gamma(C-t+1)/[Gamma(C+1)Gamma(C+eps-t+1)] = d_t`, exactly the
file's `d_t`, and the convergence condition `t < C+1` is the same.)

This is worth doing for three reasons.

1. **The "unbounded support" objection in §4 of the theorem file dissolves.**
   The measure is compactly supported on `[0,1]`; the apparent tail was an
   artifact of the `y` coordinate. The obstruction is not a tail, it is the mass
   near `x = 0`, weighted by `x^{C-r}` with `C - r = n - 3/2 - r >= 1/2 > 0` —
   always integrable, and the singular `x^{-r}` is always beaten by the density.
   Saying "sigma has unbounded support so the argument does not close" is
   technically true and strategically misleading; it makes the obstruction sound
   harder than it is.
2. **The whole problem is now four scalars**: `(n, r)` integers, `B in (0,1)`
   carrying all of `lam`, `eps` carrying all of `D`. `B -> 0` is `lam -> inf`
   and is a *regular* endpoint. The brief records that "Bernstein on naive
   coordinates for the double limits jams"; `(B, eps)` is a natural
   compactification in which it may not.
3. It makes §3.1 visible.

### 3.1 The representation explains the parity dichotomy (do this first, it is
free)

`Q(x) = prod_{i=1}^r (x - eta_i)` has all roots in `[0, eta_max]` with
`eta_max = B theta_max < 1`. So the integrand `x^{-r}Q(x)`:

- is **positive** for `x > eta_max` (always a nonempty part of `[0,1]`, since
  `B < 1`);
- has sign `(-1)^r` as `x -> 0`.

`D` enters only through `eps = D/2 + (n-2-r)`, and the Beta mean is
`(C+1)/(C+1+eps) = (n-1/2)/(n-1/2+eps)`, which **decreases** as `D` grows: more
`D` pushes the mass toward `x = 0`. Hence, at fixed `n, lam`:

    D -> inf   =>   sign(K_r) -> (-1)^r = (-1)^{j-1}.

So odd `j` (even `r`) knives are positive for all large `D` and even `j` (odd
`r`) knives must eventually turn negative. **That is exactly the measured parity
dichotomy of `research/BRIEF_KEYSTONE_FOR_OUTSIDE_HELP.md` §2a — "odd `j` knives
have NO positivity threshold in `D`; even `j` knives DO" — obtained here as a
one-line consequence of a verified identity rather than as an observation.**

This is the most valuable thing in the derivative form and it is currently
missing from the file. It should be written up as a lemma (with the one gap
closed: it needs `e_r(eta) = prod_i eta_i > 0`, i.e. no zero root of the `m`-th
derivative; note that `b_{n/2} = 0` for even `n`, so this needs an argument, not
an assertion — and if it can vanish, the next order decides the sign).

It also gives a sharp falsifiable prediction to test against the existing engine
(KAT-4 in §4). If that test fails, the identity chain has a bug somewhere and
the whole file is in trouble; if it passes, it is real evidence that the
representation is capturing the mechanism and not just re-encoding it.

### 3.2 (a) Can the shore be injected INTO the integral? Yes, and it becomes a
one-variable problem

In `(B, eps)` coordinates the shore is a curve, not an afterthought:

    lam = (n-2)/sqrt(B) - (n-1),
    eps_shore(n, r, B) = T_hat(lam)/2 + (n - 2 - r).

For large `lam` (small `B`), `T_hat ~ (12+4sqrt3) lam`, so

    eps_shore * sqrt(B)  ~  (6 + 2 sqrt 3)(n-2)  =  9.46 (n-2),

a hyperbola in the `(sqrt B, eps)` plane. Two consequences.

**Consequence 1: the keystone is a ONE-parameter positivity problem per
`(n, r)`.** The brief §2e records the Schoenberg/Gneiting dimension walk:
positivity at `D+2` implies positivity at `D`, i.e. positivity at `eps+1`
implies positivity at `eps`. So it suffices to prove positivity on the shore
itself (strictly, on a strip of width 1 in `eps`). Define

    G(n, r, B)  :=  K_r  evaluated at  eps = eps_shore(n, r, B),
                =  E_{x ~ Beta(n-1/2, eps_shore)} [ x^{-r} prod_i (x - B theta_i) ].

**Target: `G(n, r, B) > 0` for all `B` in `(0, ((n-2)/(n-1))^2)`.** One bounded
variable, both endpoints regular (`B -> 0` is the scaling limit whose closed
form is already known, `B -> B_max` is `lam -> 0` where `T_hat(0) = 9` and `D`
is small). `eps_shore` is piecewise smooth in `B` because of the integer
minimiser `k` in `T_hat`, but the project already has certified `k`-window
machinery for exactly that. This is the concrete answer to "every route so far
has imposed the shore only at the end": here the shore *is* the parametrisation.

**Consequence 2: a heuristic that says the right answer is linear in `n`.**
Positivity is comfortable when the Beta mass sits well above `eta_max`:

    Beta mean  =  (n-1/2)/(n-1/2+eps)  >>  eta_max = B theta_max.

On the shore, `eps ~ 9.46 n / sqrt(B)`, so the condition becomes
`sqrt(B) theta_max <~ 1/9.46`, i.e. (using `sqrt B = (n-2)/s ~ n/lam`)

    lam  >~  9.5 * theta_max(n,r) * n.

**Linear in `n` at every depth, with `theta_max in [1/3, 1]`.** Compare: the
current proved bound is `3.15 r n` (linear in `n` but with an `r` in front, so
`n^2` at the deepest knife), and the measured Hausdorff mechanism is `2n`. So a
successful quantitative version of the Beta-concentration argument would land
within a factor of ~5 of the *measured* mechanism, uniformly in depth — an
`n`-fold improvement on Theorem 6. **This is the single most promising route I
can identify.**

A concrete sufficient condition to try to prove (crude but fully explicit; both
bounds are two lines): with `a = eta_max = B theta_max`, using `|Q(x)| <= a^r`
on `[0,a]` and `Q(x) >= (x-a)^r` on `[a,1]`,

    INT_a^1 (1 - a/x)^r x^C (1-x)^{eps-1} dx   >=   a^r INT_0^a x^{C-r}(1-x)^{eps-1} dx.

Both sides are incomplete Beta functions; the inequality involves only
`(C, eps, r, a)`. It is lossy for large `r` (the factor `(1-a/x)^r` is small
just above `a`), so expect it to work first at shallow and moderate depth, which
is fine — that is already more than Theorem 6 gives there. Refinements in order
of cheapness: replace `a^r` by `e_r(eta) = prod_i eta_i` on `[0, eta_min]` (the
exact value at `x=0`, computable as the constant term of the `m`-th derivative);
split `[eta_min, eta_max]` off separately; and for even `r` note that the
`[0, eta_min]` region contributes with a **positive** sign and can be moved to
the other side of the inequality.

### 3.3 (b) Does finite free probability give a usable bound on `max(eta)`?

**Yes, in closed form, because the root measure here is explicit — but it will
not help at the deepest knife, for a structural reason that must be flagged.**

*The good part.* `b_k/B = ((n-2k)/(n-2))^2` is exactly the squared uniform grid,
so the empirical measure converges to the law of `U^2`, `U` uniform on
`[-1,1]`: density `1/(2 sqrt v)` on `[0,1]`. Its Cauchy transform is elementary:
with `z = zeta^2`, `zeta > 1`,

    G(z) = INT_0^1 du/(z - u^2) = (1/(2 zeta)) ln((zeta+1)/(zeta-1)).

The standard finite-free / fractional-free-convolution edge formula for keeping
a fraction `alpha = r/N` of the roots after differentiation is

    edge(alpha) = min_{z > 1} [ z - (1-alpha)/G(z) ],

so, for this family, `theta_max(n,r) -> edge(r/N)` with `N = n-1`, **independent
of `lam` and `D`**. My hand evaluation against the file's measured numbers at
`n = 20` (`N = 19`):

| r | alpha | free-limit edge (hand) | measured `max(eta)/B` |
|---|---|---|---|
| 1 | 0.053 | 1/3 (exact limit of the formula as alpha -> 0) | (mean, `= n/(3(n-2)) = 0.370` exactly at n=20) |
| 2 | 0.105 | ~0.54 | 0.448 |
| 10 | 0.526 | ~0.83 | 0.795 |
| 18 | 0.947 | ~0.99 | 1.000 |

Agreement is a few percent at large `r` and poor at small `r`, which is what one
expects (`O(1/N)` corrections dominate when only two roots survive). The
`alpha -> 0` endpoint is an exact check: the formula returns the mean of the
measure, and the `r=1` root of the `(N-1)`-th derivative *is* the mean — the
file's Lemma 2 in another guise. **So the free-probability reading is correct
and gives a lam-free, `n`-free (in the limit) law `theta_max = edge(r/N)`.**
That is exactly the input `a = B * theta_max` needs in §3.2.

What is needed to make it a proof rather than an asymptotic: a **finite-`N`
upper bound** on `theta_max`. The MSS inverse-Cauchy-transform inequality for
finite free convolutions is the place to look (differentiation is a finite free
convolution; the MSS bound is a genuine inequality at finite `N`, not an
asymptotic). If that yields
`theta_max(n,r) <= min_{z>1} [z - (1 - r/N)/G_n(z)]` with `G_n` the *exact*
finite Cauchy transform `(1/N) sum_k 1/(z - v_k)`, the route closes and the
bound is computable in exact arithmetic (it is a rational optimisation in `z`).

*The bad part, and it is important.* `b_1 = b_{n-1} = B` exactly (both `k=1` and
`k=n-1` give `(n-2)^2`). So `prod_k(u - b_k)` has a **double root at `u = B`**.
Hence its first derivative has a root at `u = B` exactly, and

    theta_max(n, r = n-2) = 1   EXACTLY, for every n and every lam,

because the deepest physical knife `r = n-2` has `m = N - r = 1` — a single
differentiation. **There is no contraction at the deepest depth, ever.** So
route (b) cannot by itself help at `r = n-2`, and any bound built on
`theta_max < 1` will degrade to nothing there. This also explains, structurally,
why Theorem 6's worst case is `r = n-2`: both routes lose exactly there.

Which raises the question in §3.4.

### 3.4 The deepest knife is the bound's worst case but not the problem's

`cancellation_bound_sweep.json` is explicit: the cancellation ratio peaks at
*intermediate* depth and falls back at large `j` (`n=40, lam=7`: 0.954 at
`j = 14`, 0.54 at `j = 24`). `pairing_structures_probe.json` likewise puts the
hard cases at `j = 8..14` for `n = 20..40`. Yet `(*)` is binding at `r = n-2`,
i.e. `j = n-1`, where the measurement says the problem is comparatively easy.

Two readings, both actionable:

- **The bound is very lossy at large `r`.** Newton's chain
  `p_{t+1}/p_t <= bbar` is tight at `t = 0` (the file's §6 is right about that)
  but the *number* of terms grows with `r`, and requiring monotonicity of every
  one of them is a much stronger demand at `r = n-2` than at `r = 2`. Fixing
  large-`r` behaviour buys the whole gap between `3.15 r n` and `3.15 n^2`
  without touching the constant.
- **Alternatively, deep knives may be easy for a reason the B-form cannot see.**
  At `r = n-2`, `m = 1`: `Q` is (up to a constant) the derivative of a polynomial
  whose roots are a squared uniform grid with a double endpoint — an extremely
  rigid object. A direct argument at `m = 1` (and maybe `m = 2, 3`) may be
  available in closed form, closing the deepest depths by hand and letting the
  general bound handle the rest. **Cheap and worth an afternoon.**

### 3.5 (c) `sigma`'s tail: the premise in the question is wrong, and that is
good news

The question asks whether `eps` growing with `D` makes the density decay
`D`-dependently. It does not. For `y -> inf`,

    y^{-C-eps-1}(y-1)^{eps-1}  ~  y^{-C-2},

so the **tail exponent is `-(n + 1/2)` and is completely `D`-independent**. What
`D` changes is the normalising constant `Gamma(C+eps+1)/(Gamma(C+1)Gamma(eps))`,
which grows with `eps`, so larger `D` puts *more* relative mass at large `y`.
In the `x = 1/y` coordinate this is transparent: the measure is
`Beta(n-1/2, eps)` and increasing `eps` shifts mass toward `x = 0`. There is no
tail problem at all; there is a mass-allocation problem near `x = 0`, and it is
governed by one number:

    P( x <= a ),  a = B theta_max,  x ~ Beta(n-1/2, eps),

which is a regularised incomplete Beta `I_a(n-1/2, eps)`, increasing in `eps`
and hence increasing in `D`. **So yes — the shore condition controls it, exactly
and monotonically**, via `eps <= eps_shore(n,r,B)`. That is the clean version of
"inject the shore into the integral": the shore is an upper bound on the second
Beta shape parameter, and everything that can go wrong is measured by
`I_{B theta_max}(n-1/2, eps)`. Classical incomplete-Beta tail bounds (or the
Beta-Binomial / Chernoff relation) are then off-the-shelf tools.

### 3.6 Ranked recommendation

1. Do the `x = 1/y` substitution and rewrite §4 of the theorem file in Beta
   language. Half a day, no new mathematics, and it removes a misleading
   sentence about unbounded support. (§3.0)
2. Write up the parity lemma (§3.1) and test its `D -> inf` prediction against
   the reference engine (KAT-4). This is the strongest claim in the whole file
   and it is currently absent.
3. Report the depth-resolved region `lam*(n,j)` instead of the max over depth.
   (§1.2) Purely a reporting change, and it multiplies the apparent strength of
   the theorem by `n` at shallow depth without weakening a single statement.
4. Attempt the incomplete-Beta sufficient condition of §3.2, first at fixed
   shallow depth. Target: `lam >~ C * theta_max(n,r) * n` uniformly in depth.
5. Attack `m = 1` (deepest knife) directly and separately. (§3.4)
6. Only then chase the finite-`N` MSS bound on `theta_max`. (§3.3)

---

## 4. Known-answer tests I would require before this goes anywhere

The existing battery (870 trials, 37 negative reference points, certified root
enclosures) is good and non-vacuous. These are the gaps.

- **KAT-1 (degenerate `b`).** Force all `b_k = b` equal. Then
  `e_t = C(N,t) b^t` and `K_r` must collapse to a terminating `2F1`, i.e. a
  Jacobi polynomial evaluation. Check the collapse symbolically and check the
  positivity condition against the classical Jacobi sign rules. This is a
  free structural test of the whole chain and it reconnects to the fact that the
  knives are Jacobi coefficients in the first place.
- **KAT-2 (`r = 1` and `theta` scale-freeness).** `eta_1` must equal
  `bbar = n(n-2)/(3 s^2)`, and `theta_1 = n/(3(n-2))` for every `lam`. More
  importantly: verify in exact arithmetic that **`eta_i / B` is independent of
  `lam`** across the existing 45-case root-enclosure grid. If that fails, my
  §3.0 reduction is wrong and everything downstream of it collapses.
- **KAT-3 (Beta representation).** Verify
  `K_r = E_{Beta(n-1/2,eps)}[x^{-r} prod (x - eta_i)]` by exact Gauss-Jacobi
  quadrature against the reference engine, including at `r = n-2` (where the
  `x^{-r}` singularity is strongest: `C - r = 1/2`) and at `D` just above 3
  (smallest `eps`). Those are the two corners most likely to break it.
- **KAT-4 (parity prediction, the sharp one).** For fixed `n, lam`, take
  `D -> inf`. Predicted: `sign(knife_j) -> (-1)^{j-1}`, i.e. odd `j` stays
  positive and even `j` goes negative and stays negative. The programme already
  believes this from measurement; here it is a *derived consequence*, so it is a
  real test of the derivation. Include the even-`n` case where `b_{n/2} = 0`.
- **KAT-5 (negative control on the hypothesis).** At each of the 37 reference
  points with a negative knife, verify that `(*)` is violated — and record how
  far. The file checks the implication ("Leibniz true but `K_r < 0`: 0"), which
  is the same information logically, but the *margin* distribution at the
  negative points tells you how much slack there is to recover.
- **KAT-6 (coverage of the verification grid).** State, for the 870 trials, the
  joint coverage in `(n, r, lam, D)`: specifically whether `r = n-2` and small
  `eps` were both sampled, and whether any trial had `B` near its maximum
  `((n-2)/(n-1))^2` (i.e. `lam -> 0`). A grid that never visits the corner where
  a step is tightest is a grid that cannot falsify it. The repo's own history
  ("grids have burned us three times") argues for this.

## 5. Adversarial checks

- **The `n = 100` row is an extrapolation of a trend, not a limit.** The table's
  ratio `3.06` is presented as "still drifting upward". Either compute the
  asymptote `2 + 2/sqrt3 = 3.1547` and state it as a proved corollary, or say
  the trend is unresolved. Right now the table invites a reader to guess.
- **`max(eta)/B = 1.000` at `r = 18` is not a numerical coincidence** — it is
  exactly 1 (§3.3, double root at `B`). Printing it as `1.000` next to genuinely
  approximate values suggests the file did not notice. Notice it, and say why.
- **"Strictly weaker than what the programme has already measured" is generous
  to the file in one direction and harsh in another.** Generous: the Hausdorff
  region has a depth cutoff `j <= n/2+1` and the new theorem has none — those
  are not comparable regions, and saying "strictly weaker" is imprecise. Harsh:
  at fixed shallow depth the new theorem is only a small constant factor away
  from the Hausdorff region. Fix both.
- **Theorem 6 covers `D <= D*`, not `D = T_hat`.** The end-to-end spot check
  ("every knife `j = 3..n-1` is positive at the shore") is at the shore, good.
  But the D-strip between `T_hat` and `D*` is also proved and is *outside* the
  keystone claim — which means the theorem proves things the keystone does not
  assert. That is a hint that `(*)` is not shaped like the truth (the true
  boundary for even `j` is `D*(n,lam) > T_hat` with the measured gap law
  `D* - T_hat -> C(j-2)`, `C = 2.398`). Worth checking whether Theorem 6's `D*`
  and the *measured* even-`j` threshold `D*` have any relation at all, or whether
  the coincidence of notation is misleading readers (including me on first
  reading — **rename one of them**).
- **Is the `n = 4` endpoint real?** `r in [2, n-2]` forces `n >= 4`, and my
  §1.4 numbers all come from `n = 4`. If `n = 4` is excluded for a physical
  reason not recorded here, all the §1.4 thresholds move up and get worse for
  the theorem. Check.
- **`e_r(eta) > 0`** is assumed implicitly whenever the `x -> 0` sign is used.
  For even `n`, `b_{n/2} = 0`. Prove `0` is not a root of the `m`-th derivative,
  or handle the case.

## 6. Questions for external experts

Ordered so that a specialist can answer 1-3 in minutes and either save or cost
the project weeks.

1. The functional `y^t -> Gamma(C+eps+1)Gamma(C-t+1)/[Gamma(C+1)Gamma(C+eps-t+1)]`
   applied to `prod_k(1 - b_k y)` with `b_k >= 0` — does this composition have a
   name? Is it covered by the Malo-Schur-Szego composition theorems, by
   Polya-Schur multiplier sequences, or by the Borcea-Branden classification of
   real-rootedness-preserving operators? If so, what does that literature say
   about the *sign at `y = 1`*, as opposed to the location of the roots?
2. Is there a finite-`N` (not asymptotic) upper bound on the largest root of the
   `m`-th derivative of a real-rooted polynomial in terms of its Cauchy
   transform — of the form
   `maxroot(p^{(m)}) <= min_{z > maxroot(p)} [z - (1 - r/N)/G_p(z)]`, `r = N-m`?
   Is that in Marcus-Spielman-Srivastava, in Marcus's finite-free-probability
   paper, or is it only true in the `N -> inf` limit?
3. For `p` with a *double root at its right endpoint*, the first derivative
   inherits that root, so there is no contraction at `m = 1`. Is there a
   standard workaround, i.e. a bound on the largest root of `p^{(m)}` that is
   useful when the extreme root has multiplicity 2?
4. Askey-Gasper-style question: given `Q` real-rooted with all roots in
   `[0, a]`, `a < 1`, and `x ~ Beta(A, eps)`, is there a sharp criterion for
   `E[x^{-r} Q(x)] >= 0` better than splitting the integral at `a`? This is the
   exact form of our open problem and it feels like it should be classical.
5. Does the empirical measure "law of `U^2`, `U` uniform on `[-1,1]`" (density
   `1/(2 sqrt v)` on `[0,1]`) have a known image under fractional free
   convolution powers, with a closed-form right edge as a function of
   `alpha = r/N`?
6. Independent of all of the above: is there a reason to expect the CHR knife
   positivity boundary to be *simpler* in the variables
   `B = (n-2)^2/(lam+n-1)^2` and `eps = D/2 + (n-2-r)` than in `(lam, D)`? We
   observe that these two variables separate `lam` and `D` completely, and that
   the remaining data is a fixed squared-uniform grid depending only on `n`.

## 7. Plain-language brief for the founder

The knife is a big alternating sum, and alternating sums are hard because the
positive and negative pieces nearly cancel (the project measured cancellation
ratios up to 0.95 — only 5% of the positive mass survives). This result does two
different things, and only one of them is a theorem.

**The theorem.** It finds a region of parameters where the terms shrink fast
enough that the alternating sum is positive for the same reason
`1 - 1/2 + 1/3 - ...` is positive: group them in pairs. That works when the
coupling `lam` is very large compared with the level `n` — roughly
`lam > 3 n^2` if you want every depth at once. Honest assessment: that region
does not contain the string amplitude itself (`lam = 1`), does not contain any
of the settings where the project has measured the hard cases (`lam = 1` to
`7`), and lives in the corner of the domain where the boundary the project is
trying to draw is not being touched. It is a real theorem in a place nobody was
worried about.

**The thing that matters more.** Along the way the file discovers that the knife
can be rewritten as: take an explicit polynomial whose roots are a simple grid
of squared numbers, differentiate it `n-1-r` times, and then average the result
against a Beta distribution. In that form, the coupling `lam` appears in exactly
one place (a scale factor `B` on the roots) and the dimension `D` appears in
exactly one other place (a shape parameter of the Beta). Everything else depends
only on the two integers `n` and `r`. That is a big simplification of a
four-parameter problem down to two knobs.

And in that form, a fact the project had only *seen in data* — that odd-order
knives never go negative no matter how large `D` gets, while even-order ones do
— falls out of the picture in one line: cranking `D` pushes the Beta average
toward zero, and the polynomial's sign at zero is `+` for odd knives and `-` for
even ones. When a rewriting explains something you previously only measured,
that is usually the sign that the rewriting is the right one. **My recommendation
is to spend the next block of effort on that representation, not on widening the
theorem.**

**What I am unsure about.** Whether the transform is already known under another
name. My honest guess is that a specialist in polynomials-with-real-roots would
recognise it immediately as a standard composition and would not consider the
technique new; the application to this amplitude family is another matter and is
the project's own. Also unsure: whether the incomplete-Beta route in §3.2
actually closes — the heuristic says it should give `lam > ~10 n` at every
depth, which would be an `n`-fold improvement and close to the measured
mechanism, but heuristics of exactly this shape have died in this project
before, and the crude bound I wrote down is visibly lossy at large depth.

---

*Reviewer's own limits, stated for the record: I did not run any code for this
review (the domain-critic role has no execution tools in this session), so every
number I produced is hand arithmetic at float precision and at least two of them
(`lam ~ 14` for the first shore crossing; the free-probability edge values)
should be regarded as rough. I did not consult any literature. The three
findings I would stake the most on are structural rather than numerical: the
`x = 1/y` Beta rewriting (§3.0), the parity explanation (§3.1), and
`theta_max = 1` exactly at the deepest knife (§3.3).*
