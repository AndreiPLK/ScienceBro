# Depths 2, 3, 4, 5: proved for K>=3, all lam -- by one generic tool

`lab/depth_d_proof.py <d1> <d2> ...` -- no per-depth file needed any more.

## What "proved" means here, precisely

For each depth `d` and each parity (`N=2K` even / `N=2K+1` odd, `K>=3`
integer):

1. Elementary symmetric functions `e_0..e_d(N)` derived from power sums
   (exact Lagrange interpolation, each checked against direct summation on
   held-out points -- not trusted blind).
2. The depth-d beta-mean formula built as a bivariate polynomial `H(K,c)`
   at the half-level `M=K`, using `T_hat(lam) <= T_K(lam)` which holds **by
   definition** for any integer `K>=3` (the ERR-0008 fix; depth-independent).
3. `H`'s sign verified against the exact reference engine (`jacobi_coeff_rec`)
   at concrete `(K,c)` points, BOTH parities -- before any Bernstein run.
4. Two overlapping exact Bernstein certificates -- `0<=c<=50` direct,
   `c>=1` via Moebius compactification -- together covering **all c>=0**.

## Results (this run, `results/depth_d_proofs.json`)

| depth | self-check | even: lo / hi | odd: lo / hi | proved for all lam |
|---|---|---|---|---|
| 2 | 56/56 | True(1 box) / True(1 box) | True(1 box) / True(1 box) | **yes** |
| 3 | 56/56 | True(1 box) / True(1 box) | True(1 box) / True(1 box) | **yes** |
| 4 | 56/56 | True(1 box) / True(1 box) | True(1 box) / True(1 box) | **yes** |
| 5 | 56/56 | True(1 box) / True(1 box) | True(1 box) / True(1 box) | **yes** |
| 6 | **54/56, 2 mismatches** (K=8,10, c=1/100) | not attempted | not attempted | **no -- unresolved** |

Depth 6's self-check mismatch was found with under 45 minutes left before a
deadline and was deliberately NOT chased tonight -- better to report an
honest "unresolved" than a rushed, possibly wrong fix. It needs a fresh look:
is it an algebra bug at higher depth, or a genuine breakdown of the half-level
trick for larger d at small c? Unknown. Next session's first job.

## What "K>=3" means in terms of n

`n = N+1`. Even branch: `N=2K>=6` so `n>=7`. Odd branch: `N=2K+1>=7` so
`n>=8`. **Levels below this floor are NOT covered by this file** -- exactly
like depth 2 needed n=3,4,5 checked separately (now resolved, ERR-0009) and
depth 3 needs n=5,6,7 checked separately (dense grid done, zero failures,
NOT yet a continuum proof -- see `D3_STATUS.md`). Depths 4, 5 have the same
kind of small-n gap and it has not been addressed yet.

## Honest summary

Four consecutive depths closed by exactly the same argument, each verified
against the exact engine before being trusted, in about 30 minutes once the
method existed. That is the payoff of building the generic tool instead of
hand-deriving each depth (depth 2 alone took the whole earlier part of the
night, largely because of an engine violation and a real logic bug, both now
fixed and recorded as ERR-0008/ERR-0009).

Two honest gaps remain, both already flagged rather than hidden:
1. Small n (below the K>=3 floor) for depths 3, 4, 5 -- evidence only, not
   proof, for depth 3 (n=5,6,7); not even checked yet for depths 4, 5.
2. Depth 6's self-check failure, cause unknown, not investigated tonight.
