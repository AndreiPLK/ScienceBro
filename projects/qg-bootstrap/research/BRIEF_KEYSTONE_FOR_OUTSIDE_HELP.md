# Request for ideas: one positivity argument for ALL orders of a Jacobi-coefficient family

This is a self-contained brief for an outside reader (human or AI). It states
an open mathematical problem from a quantum-gravity S-matrix bootstrap
programme, lists exactly what is proved, what is measured, which routes are
DEAD (do not propose them again), and which structures look load-bearing. We
have an exact rational-arithmetic engine and can test any concrete proposal
within hours; proposals should therefore be falsifiable, not just plausible.

## 1. The object

Fix an integer level `n >= 3`, a real parameter `lam > 0` (Regge slope-like
parameter of the Cheung–Hillman–Remmen graviton amplitude family, PRD 111,
086034, with `mu(n) = (n+lam-1)/lam`), and a real "spacetime dimension"
`D > 3`. The partial-wave positivity constraints of the family reduce, level
by level, to signs of Jacobi expansion coefficients (our "Jacobi normal
form", machine-verified):

- There is an EXPLICIT nonnegative polynomial `F(u)` of degree `n-1` on
  `[0,1]` (a perfect square times a monomial, built from the level-`n`
  spectrum of the family).
- Expand `F` in the Jacobi basis `P_m^{(alpha,beta)}(1-2u)` with
  `alpha = -1/2`, `beta = D/2 - 2`. Let `f_m` be the coefficients.
- Define the **knife of order `j`** at level `n` (we index by DEPTH
  `d = j - 1`): `knife_j = (-1)^m * f_m` with `m = n - j`.

**The physical claim (the "keystone theorem" we want):** for every level
`n`, every order `3 <= j <= n-1`, every `lam > 0`:

    knife_j >= 0   whenever   D <= T_hat(lam),

where the "shore" is `T_hat(lam) = min over integers k >= 3 of T_k(lam)`,

    T_k(lam) = 3(2k-3)/(k(k-2)) * (lam^2 + (2k-2)lam + 1) + 2k.

`T_hat` is the exact positivity boundary of the `j = 2` knife (published as
the "gravity shore"; the integer minimiser behaves like `k ~ sqrt(3)*lam`).
The claim is heavily tested numerically (hundreds of thousands of exact
sign checks over years-equivalent of grid and optimizer sweeps, zero
violations) and PROVED so far only depth by depth (see §3).

## 2. Structure you should know before proposing anything

**(a) Parity dichotomy.** Odd `j` knives have NO positivity threshold in
`D` (they stay positive above the shore too); even `j` knives DO have a
threshold `D*(n, lam) > T_hat`. In the scaling limit `n = rho*lam`,
`D = d*lam`, `lam -> inf` the knife has the closed form

    knife_j -> (2 rho^2 + 12 rho + 6 - d*rho)^(j-1) / (6 (rho+1)^2)^(j-1),

a perfect even power for odd `j` (hence never negative at leading order) and
linear-sign for even `j`, whose boundary `d = 2 rho + 12 + 6/rho` has
minimum `12 + 4 sqrt(3)` at `rho = sqrt(3)` — exactly the shore asymptote.

**(b) Gap law (measured, not proved).** The distance from the even-`j`
threshold to the shore tends to a constant: `D* - T_hat -> C*(j-2)` with
`C = 2.398 +- 0.002` (we do not claim `C = 12/5`).

**(c) Beta-mean form.** Each knife is a finite sum

    knife ~ sum_{i=0}^{d} r_i(n, lam) X^i (m+1/2)_i / (g)_i,
    X = (n + lam)^2 (up to normalization),  g = 2m + gamma + 1,
    gamma = (D-3)/2,

with explicit polynomial `r_i` and Pochhammer denominators — clearing
denominators makes every fixed-depth claim a polynomial positivity problem.

**(d) The critical curve is a conic.** `dT_k/dk = 0` is quadratic in `lam`
with discriminant `3 k^2 (k-2)^2 (4k^2 - 12k + 3)`; the non-square part is a
quadratic, so `w^2 = 12k^2 - 36k + 9` is a conic with rational point
`(k, w) = (3, 3)`, hence rationally parametrizable, and the critical branch
is `lam*(k) = (3b + k(k-2)w)/(6a)`, `a = k^2-3k+3`, `b = k^2-6k+6`.

**(e) Dimension walk.** Positivity at `D+2` implies positivity at `D`,
uniformly in spin (Schoenberg's dimension walk; Gneiting, Thm 2(b),(c),
arXiv:1111.7077). So per-`D` coverage only needs a strip of width 2 below
the shore.

## 3. What is PROVED (exact Bernstein certificates, rational arithmetic)

- Depths `d = 2, 4, 6` (odd `j`): positive at `D = T_v(lam)` for ALL real
  `v` in `[8/5, 2]`, all levels, all `lam > 0` (four-piece certificates,
  zero open boxes).
- Depths `d = 3, 5` (even `j`): the fixed-`v`-window statement is FALSE
  (exact counterexamples; even-`j` knives have thresholds and the window
  overshoots them at large `lam`). The TRUE statement is certified instead:
  positive at `D = T_{k+delta}(lam*(k))` along the critical curve, for ALL
  levels, ALL `k >= 12` on the curve, `|delta| <= 9/8` (both parities of the
  level, zero open boxes). Supporting certificates: the integer argmin of
  `T_k` lies within 1 of the continuous minimiser `k*` for `lam >= 7`
  (coefficient-sign arguments + certified strict convexity of `T` in `k` on
  the window); fixed shore integers `k_s = 4` on `lam <= 5/2` and `k_s = 8`
  on `lam in [5/2, 7]` are certified for depths 3 and 5.
- Monotonicity in `D` below the shore ("step (c)") is certified at depths
  2–6.

So: **every depth up to 6 is closed by certificates. The problem is the
INFINITE FAMILY.**

## 4. THE OPEN PROBLEM

Find ONE argument covering every depth `d >= 2` (equivalently every knife
order `j >= 3`) at once — or at least reduce the infinite family to a
finite check plus an induction/asymptotic step. The per-depth Bernstein
machinery works (depth 7 is running now) but each depth is a separate
finite computation whose size grows quickly; it can never close `j -> inf`
by itself.

Candidate shapes we consider promising but unproven:

1. **Depth induction.** A relation carrying positivity from knife_j to
   knife_{j+1} (or j+2, preserving parity). We have the hint
   `Q_{j+1} = Q_j / (j - t)` at the level of the falling-factorial kernels
   `Q(t) = prod_{i=j}^{n-1} (i - t)`, but no inequality-carrying form.
2. **Asymptotic + finite.** The scaling limit (§2a) settles `lam -> inf`
   at leading order per depth. Missing: an error bound UNIFORM IN `j`
   turning "leading order positive with margin" into "positive for all
   `lam > Lambda(j)` with `Lambda` explicit and slowly growing", plus a
   uniform-in-`j` treatment of the compact remainder.
3. **A positivity-preserving integral representation.** Write knife_j as a
   manifestly nonnegative integral/sum for `D <= T_hat` directly — the
   Askey–Gasper style. Note: an SOS-in-Jacobi-basis attempt aimed at the
   (false) fixed-window statement died; the target must be the k-window /
   at-the-shore statement.
4. **Total positivity / kernel structure IN j.** For fixed `(n, lam, D)`
   at the shore, the sequence `j -> knife_j` might have a structure
   (sign-regularity of some kernel) implying all-`j` positivity from small
   `j` — unexplored beyond the failed attempts listed below.

## 5. DEAD ROUTES — verified dead, do not propose

- **Endpoint-minimum lemma** ("`min_m C_m` is at an endpoint") — FALSE,
  exact counterexample at `n=24, lam=10, D=177`.
- **Log-concavity of the coefficient sequence** — FALSE (same
  counterexample); also normalisation-dependent and ill-posed as first
  stated.
- **Saddle-point/steepest-descent reduction of log-concavity** — the
  asymptotics does not resolve the deciding term at the counterexample; a
  "proof" there would have proved a false statement.
- **Real-rootedness, closed-form coefficient ratios, log-convexity, total
  positivity in m, Stieltjes moment structure, Newton inequalities via F**
  — all six excluded by explicit exact tests.
- **Fixed v-window uniform in depth** ("knife positive at `T_{v*lam}` for
  all `v in [8/5,2]`, every depth") — FALSE at even `j` (odd depth):
  exact two-engine counterexamples from `n = 109`.
- **Low-spin dominance** (Wang, arXiv:2403.00906) — does not hold in this
  family: binding constraints sit at spins 8–90, never `l <= 2`.
- **Bernstein on naive coordinates for the double limits** — jams; the
  cures (compactified `c = lam/N`, `rho = k/(2K)`) are already in use.
- **Z3/nlsat as the decider** — `unknown` on the hard boxes.

## 6. What a useful answer looks like

- A concrete inequality, recursion, kernel, or integral representation,
  stated precisely enough that we can test it in exact arithmetic on
  depths 2–7 within a day. We will run it against: depths 2..10 at levels
  up to `n ~ 800`, `lam` over seven orders of magnitude, both parities,
  optimizer-driven counterexample hunts (grids have burned us three
  times).
- Pointers to literature where a same-shaped problem was closed: families
  of Jacobi/Gegenbauer connection or expansion coefficients positive
  UNIFORMLY IN THE ORDER; Askey–Gasper-type results with parameter ranges
  matching `alpha = -1/2`, `beta = D/2 - 2`; sign-regular kernels in the
  order index; dimension-walk arguments combined with order induction.
- A disproof idea is equally valuable: a structured place to hunt for a
  counterexample to the grand claim itself (all our nulls are recorded).

Known nearby results that do NOT close it: Mansfield arXiv:2502.20372
(all `n`, all `j`, but only `D <= 10`, method does not transfer); the
Schoenberg/Gneiting dimension walk (walks `D`, not `j`).

## 7. Ground rules for proposals

- Every factual claim above marked "measured" is exactly that — do not
  build on it as if proved.
- We use exact rational arithmetic (FLINT) end to end; float-level
  heuristics are welcome for INTUITION but a route must terminate in exact
  or symbolic form.
- The engine, artifacts, and full negative-result log live in
  `github.com/AndreiPLK/ScienceBro` (branch
  `claude/handoff-markdown-review-anzwo5`), key files:
  `projects/qg-bootstrap/lab/odd_depth_kwindow*.py`,
  `results/UNGLUED_KEYSTONE.md`, `docs/ERRATA.md` (ERR-0005..0013),
  `results/SCALING_LIMIT_THEOREM.md`.
