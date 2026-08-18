# Reading notes: literature for the KEYSTONE (positivity uniform in the trajectory index)

Date: 2026-08-18. Reviewer role: literature-reviewer.
Machine-readable companions:
`research/corpus.jsonl` (27 entries), `research/bibliography.bib`,
`evidence/keystone-uniformity-records.jsonl` (EV-KS-001 .. EV-KS-011).

Search substrate actually used (all programmatic, all on 2026-08-18):
arXiv Atom API, Crossref REST, OpenAlex, Semantic Scholar graph API, and the raw
NIST DLMF HTML. Search-engine prose was not used as evidence anywhere.

Status context (commit `ed74b67`, same day): depths 3+ are RETRACTED
(ERR-0010, ERR-0011); only depth 2 stands. Nothing in these notes depends on the
retracted certificates — they are about the mathematics of the underlying
positivity statement, which the retraction commit confirms is intact. If
anything, the retraction raises the value of a keystone over a per-depth ladder.

Read before using these notes: `results/OPEN_PROBLEM.md` §5 "Closed routes — do
not rewalk". Several obvious literature hits (total positivity / Karlin,
Stieltjes moments, Pólya-type criteria on spheres, real-rootedness) are ALREADY
CLOSED there and are deliberately not re-offered below.

---

## 0. What the problem looks like from the literature's side

Restating the project's own reduction (OPEN_PROBLEM.md §2) in the vocabulary the
mathematical literature uses:

* `q(v) = prod_{k=0}^{N-1}(v - (N-1-2k)/s)` has roots in arithmetic progression.
  With `y = s v`, `s^N q = 2^N ((y-N+1)/2)_N`, i.e. **q is a rising factorial /
  Pochhammer product in the scattering angle**, with spacing set by `s = lam+n-1`.
* `F = q^2` is therefore the **square of a Pochhammer product**.
* "All knives non-negative" = "all Gegenbauer coefficients of `F` non-negative"
  = "`F` is an isotropic positive definite function on `S^{D-2}`"
  (Schoenberg 1942; Gneiting Theorem 1(a) — EV-KS-006).

That identification matters because the **undeformed** case of exactly this
object is the Veneziano / Virasoro-Shapiro residue: `Res_{s=n} A_0 =
(t+1)^{(n-1)}/n!` and `Res_{s=n} A_II = [(t+1)^{(n-1)}/n!]^2` (Mansfield
Eqs. (3.2), (3.7)). **The CHR family is a `lam`-deformation of a problem that
was solved for all `n` and all `j` in February 2025.** That is the single most
important finding of this pass.

---

## 1. Uniform-in-index positivity of Jacobi/Gegenbauer expansions

**Verdict: yes, a large classical literature exists, but it is uniform in the
WRONG index. No theorem found that gives coefficient positivity uniformly in the
trajectory index.**

### 1.1 The canonical uniform-in-degree results (EV-KS-001, EV-KS-002)

DLMF **18.14.25** (read verbatim from raw HTML):

```
sum_{m=0}^{n} [(lam+1)_{n-m}/(n-m)!] [(lam+1)_m/m!] P_m^(al,be)(x)/P_m^(be,al)(1) >= 0,
    x >= -1,  al+be >= lam >= 0,  be >= -1/2,  n = 0,1,...
```

DLMF **18.14.26** is the Askey–Gasper inequality, the `lam = 0` case, valid for
`al+be >= 0, be >= -1/2` or `al+be >= -2, be >= 0`. The DLMF provenance lines
read: *"Proved: Gasper (1977, Theorem 5)"* for 18.14.25 and *"Proved: Gasper
(1977, Theorem 4)"* for 18.14.26, both *"Source: Askey and Gasper (1976)"*.

Honest applicability: **not direct**. The uniform index there is the degree `n`
of a sum evaluated at a point `x`; we need uniformity in the index of a
*coefficient*. There is no formal reduction between the two.

What IS transferable is the **mechanism**, stated in Gasper's own abstract
(EV-KS-002, abstract_only): *"An expansion as a sum of squares of Jacobi
polynomials is used to prove ..."*. One explicit SOS identity discharges an
infinite family. This is the shape a keystone should have, and SOS-in-the-
Jacobi-basis is **not** on the closed-routes list (closed route 7 is total
positivity of a minor matrix, a different thing).

Bridge required: find `sigma_i(v)` with `F(v) = sum_i c_i sigma_i(v)^2` where the
`sigma_i` are Jacobi/Gegenbauer polynomials of parameter tied to `gamma_shore`,
i.e. an SOS certificate in the **Gegenbauer basis** rather than the monomial
basis. Note that `F = q^2` is already a square in the monomial sense and that
buys nothing; the content would be squaring inside the right basis.

### 1.2 Szwarc's discrete maximum principle (EV-KS-003)

Szwarc, Canad. Math. Bull. 35 (1992) 548-556, and the two SIAM companions
(10.1137/0523052, 10.1137/0523053): sufficient conditions, expressed on the
three-term recurrence coefficients, under which **every** connection /
linearization coefficient is non-negative. The proof idea (per the titles and the
abstracts) is a discrete boundary-value problem — a maximum principle run over
the two-index array, i.e. exactly "one argument for all indices at once".

Honest applicability: **needs a real bridge, and the bridge may not exist.**
Szwarc's theorems are about two *orthogonal* families; `q` is a single polynomial
and is not a member of one. Note also that OPEN_PROBLEM.md closed route 4 rejects
"a recursion in the knife index — not hypergeometric there"; Szwarc's criterion
does *not* require a hypergeometric closed form, only monotonicity conditions on
recurrence coefficients — but that distinction is my inference from titles and
abstracts, since the conditions themselves are paywalled.

### 1.3 Computer-assisted uniform positivity (EV-KS-004, EV-KS-005)

* Pillwein, Adv. Appl. Math. 41 (2008) 365-377: *"a computer-assisted proof of
  positivity of sums over kernel polynomials for ultraspherical Jacobi
  polynomials"* — the existence proof that machine certificates are accepted for
  uniform-in-index positivity in this exact corner of the literature.
* Gerhold & Kauers, ISSAC 2005 (10.1145/1073884.1073907): the CAD-plus-induction
  procedure for special function inequalities *involving a discrete parameter*.
* Kauers & Pillwein, ISSAC 2010: **the honest ceiling.** Their abstract states
  verbatim that the algorithms are not guaranteed to terminate and do not
  terminate for every input, with a priori termination criteria only for
  restricted classes of order <= 3.

Honest applicability: this is the closest existing tooling to what
`lab/depth_d_proof.py` already does, and it says our per-depth pipeline is a
recognised method, not a hack. It does **not** supply the keystone: there is no
general decision procedure, and none of these papers proves an inequality
uniformly in a parameter that changes the *degree* of the object.

---

## 2. Positivity criteria for sums with Pochhammer ratios

**Verdict: nothing found that applies to our sum. This is a genuine gap in the
literature, and it should be stated as such in the paper.**

Our sum is `sum_j r_j (m+1/2)_j / (2m+gamma+1)_j X^j` with *arbitrary* `r_j`
coming from elementary symmetric functions. Everything I found requires the
coefficient sequence to be hypergeometric (a fixed ratio of Pochhammers), which
`r_j` is not — consistent with the project's closed route 10 (creative
telescoping fails in the summation index).

Specifically checked and found not to apply:

* **Fields & Wimp**, Math. Comp. 15 (1961) 390-395 — a re-expansion toolbox
  (hypergeometric in hypergeometric), not a positivity theorem. Would need the
  summand to be hypergeometric.
* **Askey's SIAM CBMS-NSF 21 (1975)**, chapters verified by per-chapter Crossref
  DOI: ch.5 Linearization of Products (39-46), **ch.6 Rational Functions with
  Positive Power Series Coefficients (47-56)**, ch.7 Connection Coefficients
  (57-69), ch.8 Positive Sums (71-81), ch.9 More Positive Sums (83-91). Ch.6 is
  the interesting one, because "a rational function all of whose power series
  coefficients are positive" is precisely the mechanism AEHM and Mansfield use.
  Text not obtained — see blockers.
* **Gasper 1973**, Hahn discrete Poisson kernel (10.1016/0022-247X(73)90151-0):
  a Pochhammer-ratio positivity result, recorded as a lead only, not read.
* **Cho–Yun 1801.02312 / Cho–Chung–Yun 1805.11855**: a "Newton diagram" carving
  out a region of parameter space where a `1F2` is positive. Structurally
  interesting — a polyhedral positivity region in parameter space is the same
  *shape* as `T_hat(lam)` — but a `1F2` has hypergeometric coefficients and ours
  does not. Lead only; abstracts not retrieved in full.
* **Green & Wen 1908.08426**: recasts superstring unitarity as positivity of
  Hankel determinants of MZV polynomials. This is the moment-problem
  reformulation done on the *Wilson coefficient* side, not the residue side, and
  the project has already closed Stieltjes moments for the residue side
  (OPEN_PROBLEM.md closed route 8).

The beta-integral rewriting `(a)_j/(b)_j = B(a+j, b-a)/B(a, b-a)` turns our sum
into a Beta-average of `R(Xt)`, `R(y) = sum_j r_j y^j`. The natural literature
tool at that point is the variation-diminishing property of totally positive
kernels — **but the project has already tested and closed total positivity
(closed route 7: 37-47 % of 2x2 minors negative)**, so I did not pursue it
further and record no evidence for it.

---

## 3. SOS / SDP / Positivstellensatz uniform in spin (2015+)

**Verdict: negative, and the negative is well-documented (EV-KS-007).**

SDPB — the workhorse of the entire numerical bootstrap — gives an exact
SOS/Positivstellensatz certificate that is uniform in the *continuous* variable
`Delta` (Simmons-Duffin 1502.02033 §2.1, polynomial matrix programs). Spin is
handled by truncation. Verbatim from §3.2, numbered item 1, pp. 18-19:

> "In (2.2) we have a finite number of positive semidefiniteness conditions
> j = 1,...,J, whereas here we have an infinite number since l can be any
> nonnegative integer. In practice, we include spins l up to some large but
> finite lmax. As long as lmax is large enough, a functional obtained by solving
> the problem with l <= lmax should also satisfy positive semidefiniteness for
> spins l > lmax."

Appendix A repeats this and says the check is post hoc, listing e.g.
`S_{Lambda=19} = {0,...,26} u {49,50}`.

Consequence for the paper: **an exact certificate uniform in the spin/trajectory
index would be a genuinely new kind of object in this field**, not a catching-up
exercise. Searches for "all spins AND semidefinite", "uniform in spin
positivity", "spin truncation" on arXiv returned nothing that closes this.

One unread pointer: SDPB cites [27] = arXiv:1406.7845 (Caracciolo, Castedo
Echeverri, von Harling, Serone) for "a more careful analysis" of the truncation.
Worth 20 minutes.

---

## 4. Graviton bootstrap: has anyone already done all j?

**Verdict: no evidence that anyone has. But there IS a paper that solves the
undeformed endpoint of our family, and it must be engaged with.**

### 4.1 The gap is real (EV-KS-010, EV-KS-011)

CHR arXiv:2406.02665 gives the general coefficient (A3) but closed forms only for
the leading trajectory `l = n` (A4) and the **first** subleading trajectory
`l = n-1` (A5). Nothing beyond.

Citation scan: 33 + 25 citing works of the two CHR papers, 35 distinct. A regex
scan of every returned title and abstract for "all partial waves / all spins /
every spin / positivity of all / uniform in spin" gave **zero hits**. Caveat, and
it is a real one: abstracts only, plus full text for 7 of 35.

### 4.2 The paper that matters most: Mansfield arXiv:2502.20372 (EV-KS-008)

Read in full. Proves `B^D_{n,j} >= 0` for **all n and all j** for the type-I
Veneziano amplitude in `D <= 10`, directly from the beta function.

Mechanism, in four moves:

1. The AEHM double-contour representation (their Eq. (2.11)) writes the
   coefficient as the `x^{-1}y^{-1}` residue of a product of two Laurent series.
2. For `D <= 6` both series have only non-negative coefficients, so positivity is
   **manifest** — one argument, all `n`, all `j`. Eq. (2.12) shows exactly how
   this fails at `D = 8` (a single term `-z^{-2}/2`) and worse at `D = 10`
   (eight negative terms).
3. The fix: add a rational function `P_j(x,y)` (2.14) whose residue *vanishes*,
   chosen so that it dominates every negative Laurent coefficient. This is a
   finite hand computation.
4. The remaining infinite set `Q^j_{mu,nu}` is proved non-negative by
   **induction on j** through the convolution recursion (2.20),
   `Q^{j+1}_{mu,nu} = Q^j_{mu,nu} + sum sum Q^j_{sigma,rho} G_{mu+nu-sigma-rho}`,
   where `G_k` are Gregory coefficients (2.18), with a finite list of lemmas and
   a finite base case `j = 4` (Sec. 2.3).

Then §3.1: the type-II Virasoro-Shapiro residue is the **square** of the type-I
Veneziano residue (3.5)-(3.7), and a product of two positive Gegenbauer
combinations is positive because `j (x) j'` of `SO(D-1)` decomposes into a
positive sum of irreps. (This is the same Dougall/linearization step the project
already uses as step 2 of OPEN_PROBLEM.md §2.)

And §3.2: proves `B^5_{n,j} >= 0` for all `n, j` for the massless hypergeometric
amplitude, which the paper explicitly says arises **in the `lambda -> 0` limit of
the Cheung–Hillman–Remmen "planar analogue amplitude"** (his ref. [25] =
arXiv:2408.03362).

So: one endpoint of the CHR parameter line, at one dimension, is already done by
someone else, by a method that is not on our closed-routes list.

Honest assessment of transferability:

* **In favour.** Their object and ours are the same species: Gegenbauer
  coefficients of a squared Pochhammer product. Their proof is exactly a
  keystone (induction on `j`, finite base case, finite lemma list) rather than a
  per-index certificate. Their `D <= 6` argument is *pure manifest positivity*,
  which is what we want.
* **Against.** Their spacing is 1; ours is `2/s` with `s = lam+n-1`, and the
  entire mechanism runs through the specific generating function `z/log(1-z)`
  whose coefficients are Gregory numbers. There is no verified `lam`-deformed
  analogue of (2.18)-(2.19). Their induction is in `j` with the generating
  function fixed; our depth `d` changes the polynomial. The `D <= 10` step needs
  a bespoke finite computation, and nothing guarantees the analogous negative set
  stays finite as `lam` varies.
* **Concrete first experiment.** Compute the `lam`-deformed analogue of the
  Laurent expansion in (2.12): for our family, at `D` just below `T_hat(lam)`,
  count the negative coefficients of the corresponding generating function. If
  that count is finite and `lam`-uniform, the whole Mansfield scheme has a chance.
  If it grows with `lam`, the route is dead and we say so.

### 4.3 AEHM arXiv:2201.11575 §4.1 and §4.3 — read; blocker B4 CLOSED (EV-KS-009)

**§4.1, the `D <= 6` argument, is the cleanest keystone in this literature.**
Eq. (4.2) is the double-contour formula; the integrand factorises into three
power series, and each has only non-negative Taylor coefficients:

* `1/((1-x)(-log(1-x))^{(D-2)/2})` — their Appendix-A function `h_alpha` at
  `alpha = (2-D)/2`, positive exactly for `alpha >= -2`, i.e. **`D <= 6`** (4.3);
* `(x-y)^{-(n-j)}`, positive since `n - j >= 0` (4.4);
* the last factor, via positivity of `f(z) = 1/log(1-x) + 1/x` (4.5)-(4.6).

The residue of a product of positive series is positive. One argument, every `n`,
every `j`, no induction at all. Note the shape: the whole difficulty is compressed
into "**is this one explicit generating function totally positive as a power
series?**" — a single question with a `D`-dependent answer, which is precisely
what a keystone should look like, and which is Askey's ch.6 territory (§2 above).

Also §3 Eq. (3.22): `Res_{s=n} A_{a,b} = (Res_{s=n} A_a)(Res_{s=n} A_b)` via KLT,
so the closed-string (graviton) case follows from the open-string case for free.

**§4.3 asymptotics: relevant, and a documented negative.** §4.3.1 (fixed `j`,
large `n`) deforms to a **Hankel contour** and substitutes `x = 1 + t/n`,
Eqs. (4.12)-(4.17), producing

```
beta^D_{n,j} ~ n^{j+(D-4)/2} / ( (j+(D-4)/2)! * log(n)^{(D-2)/2} )   > 0
```

plus a full asymptotic series in `1/log(n)`. §4.3.2 does the fixed-`Delta = n-j`
Regge direction by a saddle point at `u = -2`.

Two consequences, both important:

1. **Prior-art match.** OPEN_PROBLEM.md §4 describes the live route as "a
   ONE-dimensional Hankel integral, all index dependence sitting in a single
   factor `exp[-tau/(L - log t)]` with `L = log N`". That is structurally the same
   reduction as AEHM (4.13)-(4.14), where the `log(n)` appears exactly the same
   way. Cite it; do not present the reduction as new.
2. **The rigorous bound is NOT there.** Both derivations are formal. The step
   (4.14) -> (4.15) is justified only by *"The remaining integrand converges
   uniformly for any bounded domain of the t-plane and hence we can replace it
   with its value at large n"*, and §4.3.2 by *"we can replace u with -2 in most
   places"*. **No explicit error bounds anywhere.** So the thing OPEN_PROBLEM.md
   says is "worth more than a sharp asymptotic" — a rigorous upper bound on
   `n*(lam)` — has not been done by AEHM either, and would be new work rather
   than a lookup. Appendices A and C of 2201.11575 remain unread and could still
   contain bounds; that residual is now blocker B4'.

### 4.4 Other graviton-side items (all abstract_only)

* Caron-Huot, Li, Parra-Martinez, Simmons-Duffin 2205.01495: the full set of
  `SO(D-1)` graviton partial waves in any `D`, via Young tableaux. Technology,
  not a positivity theorem for a family.
* Caron-Huot, Mazác, Rastelli, Simmons-Duffin 2102.08951: dispersive sum rules
  with the graviton pole at small impact parameter. Numerical bounds.
* Maity 2110.01578: generating function of the Gegenbauer coefficients as an
  Appell hypergeometric; exact form only on the **leading** trajectory in `D = 4`;
  the paper itself says the full statement is only "indicated".
* Mansfield & Spradlin 2409.09561 (already EV-QG-0002): claims a large region of
  `(r, m^2, D)` where **all** partial wave coefficients are positive. Abstract
  only; the argument is unverified here. Should be read next.

---

## 5. Prior-art flag the project must act on

`lab/keystone_dimension_walk.py` proves "positivity at `D+2` implies positivity
at `D`, uniformly in the spin" and calls it THE DESCENT LEMMA. This is the
classical **dimension walk**: Schoenberg (1942) via Gneiting Theorem 2(b),(c),
`Psi_{d+1} subset Psi_d`, strictly (EV-KS-006, full text read). The same step
appears in the amplitude literature as the branching-rule argument — Mansfield
p.5: *"from the branching rules for representations of SO(D), it follows that any
D-dimensional Gegenbauer polynomial can be decomposed into a positive linear
combination of (D-1)-dimensional Gegenbauer polynomials. Therefore positivity in
D dimensions implies positivity in D-1 dimensions."*

Our version is the `D -> D+2` / step-2 form and OPEN_PROBLEM.md §2 already routes
it through DLMF 18.18.16, so the project is not claiming it as new — but the
paper text should cite Schoenberg/Gneiting and the branching-rule statement
explicitly, or a referee will raise it.

This also independently **confirms** the project's own verdict in closed route 17:
the Schoenberg characterisation is a restatement, and every usable sufficient
condition in that literature (monotonicity, convexity, complete monotonicity of
the Gegenbauer coefficients — Gneiting §4.3) is violated by `q`, which oscillates
by construction.

---

## 6. What the literature does NOT have

Stated plainly, because these are the paper's novelty claims if they survive:

1. No positivity theorem for Jacobi/Gegenbauer **expansion coefficients** uniform
   in the trajectory index for a deformed family. Uniform-in-degree results
   (Askey-Gasper, Gasper) are about a different object.
2. No positivity criterion for `sum_j r_j (a)_j/(b)_j X^j` with **arbitrary**
   `r_j`, uniform in the parameters. Everything found assumes a hypergeometric
   summand.
3. No SOS/SDP/Positivstellensatz certificate uniform in spin anywhere in the
   bootstrap literature; SDPB explicitly truncates and checks post hoc.
4. No proof of positivity of all trajectories of the CHR graviton family. The
   nearest is Mansfield §3.2: `D = 5` only, `lam -> 0` only.
5. No **rigorous** (explicitly error-bounded) large-level estimate of these
   partial wave coefficients anywhere I could find. AEHM §4.3 is formal; nobody
   has turned the Hankel-integral asymptotics into a theorem with constants. A
   rigorous upper bound on `n*(lam)` would therefore be new in the amplitude
   literature as well as new for us.

---

## 7. Source-access blockers (explicit, per the evidence contract)

Blocking further verification, in priority order:

| # | Source | What is missing | Why it matters |
|---|---|---|---|
| B1 | Gasper, SIAM J. Math. Anal. 8 (1977) 423-447, doi:10.1137/0508032 | Full text. Only the publisher abstract was read. Theorem numbers 4 and 5 come from DLMF annotations, not from the paper. | The SOS-in-Jacobi-basis construction is the most promising untried keystone template. |
| B2 | Askey, SIAM CBMS-NSF 21 (1975), doi:10.1137/1.9781611970470 | Whole book. Chapter titles and page ranges verified via Crossref only. | Ch.6 "Rational Functions with Positive Power Series Coefficients" (pp.47-56) is the classical version of the exact mechanism AEHM/Mansfield use. |
| B3 | Szwarc, Canad. Math. Bull. 35 (1992) 548-556 + SIAM J. Math. Anal. 23 (1992) 959-969 | Full text; in particular the actual sufficient conditions. | The only "all indices at once" machine found that does not need a hypergeometric closed form. |
| ~~B4~~ | Arkani-Hamed, Eberhardt, Huang, Mizera 2201.11575, §4.1 and §4.3 | **CLOSED 2026-08-18.** Read; see §4.3 of these notes. Result: the asymptotics are formal, with no explicit error bounds. | Answered: a rigorous `n*(lam)` bound is not available off the shelf. |
| B4' | Same paper, Appendix A (p.25) and Appendix C (p.30) | Not read. | App. A is where the positivity of `h_alpha` and of `f(z)=1/log(1-x)+1/x` is actually proved — that is the technique to deform to `lam != 1`. App. C has the alternative quadruple-contour derivations. Highest remaining value. |
| B5 | Askey & Gasper, Amer. J. Math. 98 (1976) 709-737 | Full text; not even an abstract is exposed by any API. JSTOR paywall. | Source of the conjectures proved by Gasper 1977. |
| B6 | Gerhold & Kauers, ISSAC 2005; Pillwein, ISSAC 2013 | Full text (ACM DL paywall). RISC preprints not yet tried. | The induction+CAD procedure our per-depth prover informally imitates. |
| B7 | Gasper 1973, JMAA 42 (1973) 438-451 | Full text; no abstract exposed. | A Pochhammer-ratio positivity result, unassessed. |
| B8 | Mansfield & Spradlin 2409.09561 | PDF not downloaded; abstract only. | Claims "all partial wave coefficients positive" on a large parameter region of a deformed family — potentially the closest competitor. |
| B9 | Rigatos & Wang 2401.13031; Wang 2403.00906 | PDFs held locally (6 pp., 25 pp.) but unread since 2026-08-16. | The harmonic-number basis is advertised as making positivity manifest. |
| B10 | Caracciolo et al. 2406.7845 | Not read; metadata taken from the SDPB bibliography line, not independently verified. | SDPB's own pointer to "a more careful analysis" of spin truncation. |

None of these blockers is a wall; B1, B3, B4, B8, B9 are all reachable by
interlibrary request, arXiv, or a RISC/author preprint page.

---

## 8. Metadata corrections made in this pass

`evidence/keystone_prior_art.jsonl` recorded arXiv:2401.13031 as
"Coon unitarity via partial waves (harmonic numbers)" with no authors. Verified
title and authors (arXiv API 2026-08-18): *"Coon unitarity via partial waves or:
how I learned to stop worrying and love the harmonic numbers"*, Konstantinos C.
Rigatos and Bo Wang, Phys. Rev. D 110 (2024) 126024,
doi:10.1103/PhysRevD.110.126024. The same file records 2502.20372 with no author;
it is Gareth Mansfield (single author, UCLA). Corrected entries are in
`research/corpus.jsonl`; the old file was left untouched so nothing is
retroactively rewritten.
