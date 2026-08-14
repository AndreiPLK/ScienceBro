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
