# Gravity Card (FROZEN 2026-08-14): the exact edge of the closed-string island

**North star relevance: MAXIMAL** — this is the gravitational case itself
(CHR O3 answered by CHR in arXiv:2408.03362 / PRD 111, 086034; we now do to
their gravitational family what we did to their open-string family).

## The object (from 2408.03362, deep-read notes)

- Massless external, s+t+u=0, fully permutation-symmetric closed-string ansatz.
- Level truncation of M and dM/dt => residues are PERFECT SQUARES (Eq. 4):
  R(n,t) = c(n) prod_{k=1}^{n-1} (t - xi(k))^2  ("double copy" structure).
- Crossing at truncation points => ONE-parameter family (their Eq. 6-7),
  lambda >= 0, VS at lambda=1:
    mu(n) = (n+lambda-1)/lambda,  xi(n) = -(2n+lambda-1)/(2lambda),
    R(n,t) = [ ((1+lambda)/2 + lambda t)_{n-1} / ((1+3lambda)/2)_{n-1} ]^2.
- Their positivity status (p.6 + their Fig. 1): a_{n,l} = 0 for odd l; D=4
  positive for ALL lambda>=0; for D >= 9 positivity bounds lambda FROM BELOW —
  shown as a NUMERICAL finite-depth figure. No closed-form boundary given.

## Frozen question

Derive the boundary lambda_min(D, depth n) of the gravitational island in
closed form via the top-coefficient method, and its infinite-depth fate:
1. Leading even trajectory a_{n,2n-2} (top coefficient of the square: sign?).
2. Next even trajectory a_{n,2n-4}: closed-form sign law (the gravitational
   edge-law analog; odd trajectories vanish identically).
3. Fixed-spin tails and the finite-depth erosion clock (their Fig. 1 depth
   tolerance — the analog of our q-clock/D-cliff corrections).
4. Cross-checks: lambda=1 must reproduce VS D-cliff data (D_crit(n) from
   2210.14920); D=4 must be clean for all lambda (their claim); the
   lambda -> 0 and lambda -> infinity extremal corners.

## Primary metric (frozen BEFORE computing)

Exact rational sign of a_{n,2n-4}(lambda, D) versus the derived bracket; the
bracket counts as validated only after razor tests (predicted exact zeros at
never-scanned (lambda, D, n)) and a brute-force ratio check (positive,
n-only constant), same standard as Card A.

## Novelty status (radar 2026-08-14, 37 citing works listed in DATA_LOG)

- 2408.03362 itself: numerical finite-depth positivity only. Their open ends:
  planar analogues, uniqueness beyond first order.
- ADJACENT (must cite, differentiate, and read in full before any claim):
  2607.27300 (Shao-Vichi analytic boundaries via hidden zeros — abstract does
  NOT treat the lambda-family), 2606.19283 (dispersive VS bootstrap),
  2605.11084 (analytic Veneziano bootstrap), 2210.14920 (VS D_crit(n): our
  D-cliff reproduction), 2512.17828 (local pdf), 2502.20372, 2506.05253.
- No work found yet that gives the lambda-family island an exact boundary; to
  be re-verified against full texts of the adjacent papers before promotion.

## Stop conditions

- If full-text reading shows the lambda-edge already derived => pivot to the
  planar analogues / two-parameter deformations mentioned in 2408.03362.
- If the square structure makes all even trajectories positive identically
  (no edge at finite lambda in any D) => the result becomes "the gravitational
  island has NO finite-depth edge on these trajectories" — still publishable,
  smaller.


## SLICE 1 RESULT (2026-08-14): the gravitational edge law — derived and razor-verified

With the exact projection ratio rho(l,D) = (l+1)(l+2)/(2(D+2l-1)) (measured
exactly, closed form identified), the near-leading even trajectory obeys

  sign a_{n,2n-4} = sign[ q_n(lambda) * D + p_n(lambda) ],   e.g.
  n=3: (2l^2-6l+3)D + (9l^2-6l+21)     [l=lambda]
  n=4: (52l^2-120l+60)D + (379l^2-750l+555)
  n=5: (58l^2-126l+63)D + (645l^2-1330l+805)   (odd trajectories vanish identically)

Verified: (i) VS (lambda=1) thresholds D_n = 24, 23, 24, 51/2, 136/5 for
n=3..7 -> first negativity at D>23, killed by (4,4): matches the exact D-scan
(D=24 first negative (4,4); D=22 clean to 40) to the unit. (ii) Razor at
lambda=2, n=3: predicted zero at D*=45; exact arithmetic gives + at D=44 and
- at D=46. (iii) Bracket sign matches exact sign at random (lambda, D) spots.

Structure found: the dangerous lambda-window (where q_n < 0) shrinks toward
lambda = 1 (pure VS) roughly like 1 +- 1.1/n; within it the kill threshold is
D_n(lambda) = -p_n/q_n. General-n closed forms of q_n, p_n and the full
lambda_min(D) map: next slice. Status: derived + numerically verified;
independent review pending (Card-A standard).


## SLICE 2 (2026-08-14): closed form of the VS threshold sequence

  D_n(1) = 2(n^2 + 4n - 9)/(n - 2)   — matches all computed n=3..12 exactly
                                       (10/10); minimum over n is 23 at n=4.

Hence pure Virasoro-Shapiro keeps a_{n,2n-4} >= 0 iff D <= 23; first violation
at D=24 via (n,l)=(4,4) — previously our measured cliff, now a formula. Since
D_n(1) grows ~2n, this trajectory endangers VS only in a finite n-window for
any fixed D — the asymptotic D<=10 lore must come from low-spin constraints
(next slice target). Dangerous lambda-windows (l_n, u_n) computed exactly for
n=3..12, shrinking toward lambda=1; their closed form and the full
lambda_min(D) exclusion map are the remaining pieces. Status: derived +
verified 10/10; independent review pending.


## SLICE 3 (2026-08-14): the fate of the alternatives in D=4

(i) LEMMA (analytic, n=3..12): at D=4 the near-leading even trajectory bracket
q_hat*4+p_hat is a positive-definite quadratic in lambda (negative discriminant,
positive lead, all ten cases) — this trajectory excludes NOTHING in 4D.
(ii) Exact scan: 13 lambda values including the extremal corners 1/100 and 100
(gravity-plus-scalar and single-resonance limits): ALL clean on l<=8 to depth
n=60 at D=4. Artifact: results/grav_d4_lowspin.json.

Combined headline (current evidence level): within CHR's closed-string
bootstrap assumptions, string gravity is NOT forced in D=4 — the alternative
family survives deep unitarity; while in high D the dangerous lambda-window
shrinks toward pure VS. Uniqueness of the string is DIMENSION-GRADED.
Status: lemma derived (n<=12) + exact scans; general-n proof and independent
review pending before any promotion.


## SLICE 4 (2026-08-14): the exclusion map — and a CORRECTION

Exact lambda-exclusion union from the n<=16 brackets (per even D):
  D<=20: empty (this trajectory excludes nothing).
  D=22: [1.026, 1.533]  — a belt NEXT TO the string; VS itself still alive.
  D=24: [0.980, 1.632]  — the belt now swallows lambda=1 (VS dies; matches
        D_min = 23).
  D=40: [0.811, 1.953]  — belt widens slowly; EXTREME deformations (small and
        large lambda) SURVIVE this trajectory at every D scanned.

CORRECTION of the earlier framing: "unitarity squeezes neighbors toward the
string" was WRONG as stated. The shrinking q_n<0 windows mark VULNERABILITY,
and the realized exclusion at fixed D is a belt AROUND/NEAR lambda=1: at
D>=24 the string and its closest neighbors die on the near-leading trajectory
while extreme alternatives survive it. Complement (CHR): for D>=9 low-spin
constraints bound lambda from below, killing the small-lambda corner. The
combined picture (this trajectory + low spins) is the true lambda_min/max(D)
map — assembling it exactly is the next slice. Correction logged per playbook
(failures and corrections stay visible).


## SLICES 1-4 CORRECTED (2026-08-14, after the Pochhammer-step bug)

Corrected near-leading law (positive factors removed):
  positivity of a_{n,2n-4}  <=>  D <= T_n(lambda), with
  T_3 = 3l^2+12l+9;  T_4 = (15l^2+90l+79)/8;  T_5 = (7l^2+56l+57)/5;
  T_6 = (9l^2+90l+105)/8;  T_7 = (33l^2+396l+523)/35.   [l = lambda]

Consequences (all verified against the corrected exact scanner):
- lambda_min(D) = largest positive root of T_n(l) = D, maximized over n —
  the EXACT closed form of CHR's numerically observed lower bound.
- T_3(0) = 9 explains CHR's "when D >= 9" threshold exactly (their Fig. 1).
- lambda_min(10) ~ 0.0816 from the formula; scanner: 1/20 dead, 1/10 alive ✓.
- VS thresholds unchanged: D_n(1) = 2(n^2+4n-9)/(n-2), min 23 at n=4 (the
  lam=1 point was untouched by the bug).
- The buggy "exclusion belt around lambda=1" is VOID; the true structure is a
  lower bound in lambda rising with D. D=4 lemma to be re-derived next.
Bug provenance and validation: DATA_LOG 2026-08-14; razor lesson recorded —
razors sharing the evaluator with the bracket are circular; external anchors
(CHR Fig. 1 behavior) catch what internal razors cannot.


## SLICE 5 (2026-08-14): the single curve lambda_min(D) — exact

lambda_min(D) = max over n of the positive root of T_n(lambda) = D:
  D=10: -2+sqrt(39)/3 (n=3); D=12: -2+sqrt(5); D=16: -2+sqrt(57)/3;
  D=20: -3+6*sqrt(10)/5 (n=4 takes over); **D=23: EXACTLY 1 (the string)**;
  D=26: -3+2*sqrt(110)/5.
Story in one curve: born at 0 when D=9 (CHR onset explained), rises through
exact surds, hits pure VS at D=23, passes beyond it for D>=24 (string dies,
matching D_n(1) min=23). D<=9: this knife touches nothing => D=4 trivially
safe for all lambda on this trajectory. Dominant level switches n=3 -> n=4
between D=16 and 20. Remaining for paper: general-n T_n(lambda), full-l
corrected scans, independent review.


## SLICE 6 (2026-08-14): THE GENERAL LAW and the true shore

  T_n(lambda) = [3(2n-3)/(n(n-2))] * (lambda^2 + (2n-2)lambda + 1) + 2n
  positivity of a_{n,2n-4}  <=>  D <= T_n(lambda);  TRUE shore = min over n.

Verified exactly against all extracted brackets n=3..14 (12/12 identical).
Envelope computed to n=400: lambda_min(23) = 1 SURVIVES the full envelope
(the magic point is real, not an artifact of few levels). Large-D asymptote
derived: optimal level n* = sqrt(3)*lambda, giving

  D  ->  (12 + 4*sqrt(3)) * lambda_min,   slope 1/(12+4sqrt3) ~ 0.0528,

numerics: D/lambda_min = 18.96, 18.75, 18.76, 18.83 at D=60..400 vs
12+4sqrt3 = 18.928 — the creature's mouth closes onto an exactly straight
asymptotic edge. Founder's "figure is unfinished" instinct directly produced
the general law + the asymptote. Status: derived + verified numerically;
independent review pending (Card-A standard). Next: full-l envelope check,
review, paper 2.


## SLICE 7 (night 2026-08-14/15): the complete-model battery — CLEAN

Model test (alive <=> D <= min_n T_n) vs exact full-spin scans (all even l,
depth 16) over 494 grid points (lambda 0.1..10, D 4..40):
  AGREE 494/494 | doomed-discrepancies 0 | ALARMS (other knives) 0.
Plus two direct executions of doomed cells at predicted level n=4 (both
confirmed with sign flip +/-). The conjectured complete model of the
gravitational island has survived its first total battery. Independent
adversarial review running. Artifact: results/model_test.json.


## REVIEW ROUND CLOSED (night 2026-08-15)

Independent adversarial review (gravity-review.md): claims 1-3 re-derived
from scratch and STRENGTHENED (lambda_min(23)=1 proven for ALL n analytically;
cross-term bookkeeping validated — the edge exists precisely because the
x^{2n-4} coefficient is a pure cross term). Attack script executed:
NO FALSIFICATION, 0 failures (incl. non-circular razors at fractional
D*=271/4 and D*=57; envelope converging to (12+4sqrt3) through D=10000).

Fixes applied per review:
- (F1) Slice-3 D=4 statement now rests on CORRECTED artifacts only
  (grav_full_body 40/40 at D=4; model_test D=4 rows; trivial bound
  T_n(lambda) >= T_n(0) >= 9 > 4), with CHR p.6 as external anchor. The
  pre-bug "positive-definite lemma" is VOID and superseded.
- (F2) Terminology: "true shore" = shore of the NEAR-LEADING trajectory;
  completeness of the full boundary remains Conjecture (falsifiable; the
  a_{n,2n-6} law is the designated next hunt).
- Caveats recorded: D>3 domain; lambda>=0 imported from CHR; n=2 hand-checked;
  discrete-n oscillation O(1/lambda) around the asymptote to be stated.


## SLICE 8 (2026-08-15): the 2n-6 hunt — CLEAN

The reviewer-designated most-plausible second knife (a_{n,2n-6}) tested across
stress zones hugging the model boundary (34 lambda values incl. 0.1..3 and
4..10; D windows [minT-3, minT]; n=4..14): ZERO alarms — it never cuts inside
the model. Artifact: results/hunt_2n6.json. Conjecture 1 (completeness)
survives its designated hunt; next natural probes: 2n-8 spot checks + low-spin
stress at large D.

## Slice 9 (2026-08-15): SECOND KNIFE LAW l=2n-6 + window-vs-shore
- Closed form: Bhat = alpha*u*(u-2) - G*u*s^2 + s^4 (m=n-3, s=lam+n-1,
  u=D+4m+1); exact relations R=8mA, W=A(16m^2-1), V=P(4m+1).
- Blind verification 2052/2052 (n=10..12 unseen by fit). String window at
  n=7, lam=1: (26.2, 30.3) predicted, exact evaluator confirms (28,30 NEG).
- Window never dips below min_n T_n (lam to 1000, n to 4*lam): worst margin
  2.17 dims at lam=0.05 n=6. Conjecture 1 strengthened.

## Slice 10 (2026-08-15, FROZEN BEFORE RESULTS): EFT map of D=4 survivors
- Hypothesis: members of the lambda-family differ in low-energy (Wilson)
  coefficients; the family is thus observationally distinguishable in
  principle, with lambda=1 (string) a specific point on the dial.
- Primary metric: dimensionless ratios r_k(lambda) = c_k(lambda)/c_k(1),
  where c_k = sum_n R(n,0)/mu(n)^k, k=3,5 (analogues of 2*zeta(3), 2*zeta(5)
  coefficients of the VS low-energy expansion).
- Known-answer anchor (gate): at lambda=1 the sums must reproduce zeta(3),
  zeta(5) structure of Virasoro-Shapiro to stated precision.
- Negative control: r_k(1) = 1 identically by construction.
- Status: EXPLORATORY (first map; no claim promotion from this slice alone).

## Slice 11 (2026-08-15/16): BLADE THEOREM (paper 4 core)
- Proven: j=3 windows never dip below the shore for all lam <= 26.1, all n
  (blade_proof.py, ALL CERTIFIED, exit 0); plus for lam >= 26 levels n <= 81
  have no window (78 certificates). Open: single deep-water cell
  (n >= 82, lam > 26); regime-split certificates next.
