# The Island Has Edges: Exact Boundary Laws for Unitary Deformations of the Veneziano Amplitude

Draft skeleton v0.1 (night of 2026-08-13/14). Author: Andrei Pluzhnik.
Target: short letter (5-6 pp) + ancillary code/data. All claims tabled below
with honest status; nothing here is submitted or public yet.

## Abstract (draft)

The three-parameter family of Veneziano deformations introduced by Cheung,
Hillman and Remmen (arXiv:2406.02665) is constrained by partial-wave
positivity to an "island" in the (r, w) plane, mapped numerically at finite
level depth. We derive exact closed-form sign laws for the near-leading Regge
trajectories of this family and show that (i) the island's left edge is the
line r = -(1+mu0)/2, exactly, at every level and in every spacetime dimension
D > 3; (ii) the observed erosion of finite-depth islands is fully explained,
cell by cell, by a single linear-in-n law; (iii) the remaining boundary is cut
by an explicit finite set of low-level algebraic curves whose D-dependence is
1/(D-1)-tightening; and (iv) the resulting analytic description reproduces
11,994 exact-arithmetic verdicts across seven mass shifts with zero
mismatches. On the w=0 slice our edge law matches the contour-asymptotic
factor of Mansfield-Spradlin (arXiv:2409.09561) while strengthening it to
every finite level; the w != 0 region is charted here for the first time.

## Results (with status)

| # | Claim | Status |
|---|---|---|
| R1 | sign a_{n,n-1} = sign[n(r+(1+mu0)/2)+w], D>3, n>3mu0 | derived; adversarial review passed; 8 razor zeros; D=6,10 checks |
| R2 | Left edge r=-(1+mu0)/2, D-universal; erosion depth n=w/dist | corollary of R1; matches all 30 doomed cells incl. 4 direct executions |
| R3 | sign a_{n,n-2} bracket (12(2n-1)(1+r)(nr+2w)+n(n^2+5n-2)) | proven for all n (reviewer identity) |
| R4 | a_{n,n-3} closed form; safe for r>-1/2 asymptotically | derived + verified n=4..9 |
| R5 | Scalar curves: a_{2,0}: (1+r)(r+w)>=-1/(D-1); a_{3,0} cubic | derived; D=4 limits reproduce verified curves |
| R6 | Threshold structure at mu0>0: binding level n_min>=3mu0, scalar-dominated | census + symbolic curve; 2 maps PERFECT |
| R7 | Complete characterization (n<=5 curves + ladder + domain) | CONJECTURE; 11,994/11,994 exact points, depth-80 stable |
| R8 | Fixed-spin tails ~ (2l+1)C/(n ln n), C>0 | heuristic + numeric (n<=200); rigor pending |
| R9 | w=0 cross-check vs Mansfield-Spradlin Thm 11 factor (2r+m^2+1) | verified against their published asymptotics |

## Sections

1. Introduction: bootstrap context; the CHR family; what was numeric, what
   becomes exact here.
2. Setup: residue polynomial, partial-wave projection, exact arithmetic,
   threshold caveat; two-route validation of the evaluator.
3. The edge theorem: derivation (top coefficients + parity), mu0 and D
   generalizations, razor tests.
4. Trajectory laws: a_{n,n-2}, a_{n,n-3}; finite kill-windows.
5. The island, analytically: killer census, explicit curve list, stack-wide
   verification protocol (11,994 points), doomed-cell predictions.
6. Threshold structure at mu0>0 and D-dependence of the curves.
7. Discussion: completeness conjecture and what remains; fixed-spin tails;
   relation to Mansfield-Spradlin; outlook (q-deformation, other families).

## Figures (from article/visuals/)

F1 qg-island-atlas.png — seven islands, one law (edge lines overlaid)
F2 qg-island-edge-theorem.png — fine scan + 176 theorem-killed points
F3 killer-census map (to make: boundary colored by binding constraint)
F4 erosion ladder diagram (to make: the nine casualties with kill levels)

## Honest limitations (to state explicitly)

- Completeness of the finite curve list is a conjecture (empirical to depth 80).
- Fixed-spin asymptotics currently heuristic-plus-numeric.
- q=1 only; D-scan verified symbolically, full-map verification only at D=4.
- Attainment of the edge (allowed points arbitrarily close) is empirical.

## Repro pack

lab/repro_r1_crossing.py, lab/repro_r4_positivity_spot.py (two-route),
lab/fig1_island_map.py, lab/boundary_n80.py, lab/fine_grid_boundary.py,
lab/attack_left_edge.py (independent adversarial script), results/*.json,
research/left-edge-theorem.md + left-edge-theorem-review.md.
