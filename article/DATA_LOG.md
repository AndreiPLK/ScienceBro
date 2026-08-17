# Data log (append-only)

Every significant event with its measured numbers. Newest at the bottom. Never edit
old entries; append corrections as new entries.

---

## 2026-08-11

- 13:29 — Project start. Environment: Windows 11, Python 3.12.10, uv 0.11.7, no
  Docker, RTX 4070 SUPER 12 GB (TF CPU-only on native Windows).
- 13:45 — Core scaffold committed: schemas + deterministic claim gate + `sb` CLI;
  12 unit tests green.
- 13:42 — arXiv:2607.05489 verified via API ("Black Hole Black Boxes..."); PDF
  sha256=40b0fb98...; 33 pages.
- 13:51 — Upstream pinned @ 54736e46. License conflict found: LICENSE=GPL-2.0 vs
  pyproject=MIT. TensorFlow/float64 stack. No candidate checkpoints in repo.
- 13:59 — Upstream smoke run (hps_local_lorentzian, 100 epochs, CPU): exit 0, final
  loss 1.57e-10; artifacts hashed.
- 14:05 — Verifier calibration sweep (analytic Schwarzschild, x=(0,8,1.1,0.3)):
  h=3e-3 optimal; max|Ricci| 8.7e-11; Kretschmann rel err 1.1e-9. 16 tests green.
- 14:07 — Export interface end-to-end: 33 stencil points, independent FD Ricci of
  smoke model max|R_ab|=3.3e-6 at (0.1,0.2) vs upstream loss 1.6e-10 — flagged as
  unexplained, no conclusions.
- 14:50 — Discrepancy EXPLAINED (measured): FD sweep stable (ratio 1.0002);
  sqrt(1.57e-10)=1.253e-5 vs our max|Ricci|=1.261e-5 (0.7%); full upstream formula
  replicated with our Ricci: 8.08e-11 vs 1.57e-10 (factor 1.94).
- 14:50 — 4D known-answer pipeline PASS (analytic route): floor 6.7e-9..1.5e-8;
  Kretschmann vs independent Lambert-W r(T,X): 4.4e-9..1.2e-8; Lorentzian signature
  at all probes. NN interim (31/500 epochs, exploratory): Ricci 0.09..0.18,
  Kretschmann 0.4..1.7%.
- 15:00 — float32 test: median residual inflation 203x (float64 median 7.87e-6 vs
  float32 1.60e-3 over 197 grid points). Protocol: float64 mandatory.
- 15:00 — EXP-0001 frozen (config sha 5e39a538..., command, analysis plan);
  H-0001 frozen. Clean 500-epoch baseline run started (CPU, BelowNormal, 6 threads).
- 15:10 — Proof-Gate implemented. Stage-1 ENGINEERING VERIFIED (4/4);
  Stage-2 VERIFIED (8/8). Attestations with SHA-256; integrity check passes.
- 15:07 — WSL2 + Ubuntu installed; Windows reboot pending (founder decision).
- 15:50 — Recon: upstream git history clean; 0 citations of the paper (likely first
  independent audit); seed_models/old has 11 architecture variants.
- 16:00 — AL_embed supervised seed measured: max|Ricci| 0.064-0.149, Kretschmann err
  1.5-8.2% — worse curvature than 6%-trained unsupervised interim. Recorded, no claim.
- 16:05 — Dashboard translated to English; game-style Mission Control (quest map,
  HUD, proof-gate chips). Screenshot: visuals/dashboard-mission-control-2026-08-11.png.
- 16:05 — Article folder created (this file).
- 18:00 — Baseline training milestone: epoch 100/500, loss 1.03e-3 (clean run, CPU BelowNormal).
- 20:45 — Baseline training milestone: epoch 200/500, loss 7.64e-4.
- 22:54 — Reboot for WSL2; CPU run preserved at epoch 275 (loss 7.04e-4, checkpoint sha 550a9463...). GPU env install in progress. Loss-curve visual saved.
- 23:34 — GPU measured: 17 min/epoch (float64 on consumer RTX = 1/64 FP64 rate) vs CPU 1.7 min/epoch — GPU 10x SLOWER; documented, falling back to full-speed CPU for the night. GPU finding itself is article material.
- 23:45 — Full-speed CPU rate measured: 26 s/epoch (3 epochs / 78 s). New ETA: baseline complete ~03:15, thresholds frozen ~04:30, candidate launch ~04:45.
- 00:20 — night2 clean run: epoch 100/500, loss 1.03e-3 (trajectory matches previous runs).
- 01:05 — night2: epoch 200/500, loss 7.62e-4.
- 01:47 — night2: epoch 300/500, loss 6.78e-4.
- 02:30 — night2: epoch 400/500, loss 5.91e-4. Final 100 epochs ~45 min.
- 03:55 — EXP-0001 artifacts preserved (ckpt sha 7651ff3d, seeds 66/66). Hidden-point stress: Ricci median 0.123 / p95 0.286 / max 0.297; K err <=1.34%; signature 24/24. Detection floor: bump amp 0.2 (max 0.58) detectable, 0.05 not. THRESHOLDS FROZEN + git tag before any candidate. EXP-0002 (Petrov-I BH, upstream config verbatim + documented epochs fix) LAUNCHED ~03:50.
- 03:35 — EXP-0002: epoch 100/500, loss 1.83e-2 (composite BH objective), ~10s/epoch, ETA ~04:45.
- 04:06 — EXP-0002: epoch 300/500, loss 1.26e-2.
- 05:00 — EXP-0002 candidate trained (500 epochs, EXIT=0, ckpt sha fd56f170). FROZEN-CRITERIA EVALUATION: FAIL on vacuum comparability — hidden max|Ricci| median 0.915 (limit 0.286; baseline 0.123), FD-converged (spread 1.7e-6), signature 24/24, control works (p95 56.7). Scope: our retrain only; not a refutation of the paper (no published checkpoints). VAL-0001 recorded, run preserved.
- 04:46 — Boundary/horizon map (95 pts): candidate residual GLOBAL (exterior median 1.098, interior 0.986), not boundary-localized. Stage-4 complete. EXP-0003 seed-124 training in background.
- 05:34 — EXP-0003: epoch 300/500, loss 1.37e-2 (run1 at 300: 1.26e-2 — similar trajectory).
- 06:30 — EXP-0003 (seed 124) complete + evaluated: PASS frozen criteria (median 0.233 vs limit 0.286; p95 0.319; signature 24/24; convergence 3.9e-6). Seed contrast: 123 FAIL (0.915) vs 124 PASS (0.233) — 4x seed-to-seed variability of the committed BH config, measured. VAL-0002 recorded. Petrov-type diagnostics still pending — PASS is vacuum-comparability only.
- 08:51 — PRESS_RELEASE.md living draft assembled (all night results + visuals table); morning dashboard screenshot captured.
- 09:42 — Letter to AInstein authors SENT by founder (all three authors, with verified attachment). Awaiting reply.
- 12:20 — INDEPENDENT PETROV DIAGNOSTICS (verifier/petrov.py, own Weyl operator, no upstream code).
  Controls: analytic Schwarzschild |S-1| = 4.4e-16; TRAINED neural Schwarzschild |S-1| <= 1.7e-6
  (so a type-D neural metric still reads S = 1 through this pipeline).
  Candidates: seed 123 S = 2.294..2.580; seed 124 S = 2.273..2.550 -> both algebraically
  GENERAL (Petrov type I), ~6 orders above the neural-metric floor. Caveat recorded: the
  upstream loss explicitly trains S toward ~2 (Eq. 47), so this corroborates the method,
  it does not demonstrate a new solution. VAL-0003 (pass, scope-limited) + CL-0004
  (experimentally-supported) recorded. Combined with VAL-0002, seed 124 is both
  vacuum-comparable and type I under independent evaluation.
- 13:05 — INDEPENDENT TRAPPED-SURFACE DIAGNOSTICS (verifier/horizon.py, own 2+2 split).
  Controls: analytic Schwarzschild 4/4 exterior untrapped (Xi +0.038..+0.151), 8/8 interior
  future-trapped (Xi -0.005..-0.390), areal radius = independent Lambert-W r(T,X) to 3 dp;
  TRAINED neural Schwarzschild reproduces the identical 4/8 split (horizon location learned).
  Candidates: seed 124 and seed 123 both 11/12 future-trapped, areal radius departing from
  Schwarzschild by up to 0.44 -> a trapped region exists and sits elsewhere.
  Known-answer tests added (4 pass), incl. the honest orientation rule: inside a
  Schwarzschild-coordinate horizon x^0 is spacelike, so orientation is reported as ambiguous
  instead of guessed. VAL-0004 (pass, scope-limited) recorded; CL-0004 now carries all three
  legs (vacuum + type I + trapped) with the caveat that all three are training targets.
- 10:30 (2026-08-12) — Checkpoint hunt: no GitHub releases/tags on xand-stapleton/ainstein,
  only seed_models (2 current + 11 archived). Their repo DOES contain
  notebooks/examine_output_schwarzschild.ipynb with saved outputs from one of their own runs:
  det(g) spans -3.3e8 .. -699 (never near zero, so their determinant barrier works, but the
  metric scale explodes by ~6 orders near the Penrose boundary), plus a printed
  einstein_loss = 0.0690. Which seed the notebook loaded is ambiguous from the saved output,
  so no comparison claim is made from it. Independent agreement worth noting: our own
  boundary measurement showed the same region as the hardest (edge max|Ricci| 5.5e-5 vs
  interior 1.3e-5). Seeds 125/126/127 launched for the instability statistics.
- 16:06 — All five candidate seeds trained (123, 124, 125, 126, 127). Final training losses
  1.11e-2, 1.18e-2, 1.10e-2, 1.32e-2, 1.09e-2 — a spread of only 1.21x, so the runs are nearly
  indistinguishable by their own loss. Checkpoints preserved and hashed.
- 16:12 — FIVE-SEED SWEEP (verifier/seed_sweep.py, three legs per seed, hidden points derived
  from each checkpoint's own SHA-256):
  seed 123 vac 0.915 FAIL | S 2.29-2.58 | 11/12 trapped -> no
  seed 124 vac 0.233 PASS | S 2.27-2.55 | 11/12 trapped -> YES
  seed 125 vac 0.317 FAIL | S 2.30-2.58 | 11/12 trapped -> no
  seed 126 vac 0.228 PASS | S 2.29-2.56 | 11/12 trapped -> YES
  seed 127 vac 1.100 FAIL | S 2.29-2.58 | 11/12 trapped -> no
  => 2 of 5 satisfy all three legs. The instability is CONFINED TO THE VACUUM LEG: type I and
  trapping reproduce 5/5 and cluster tightly, vacuum holds 2/5 with a 4.8x spread. The reported
  training loss does not track independent vacuum quality (1.21x vs 4.8x) and in this sample the
  ordering is inverted: lowest-loss run (127) has the worst residual, highest-loss run (126) the
  best. n=5, reported as suggestive not established. VAL-0005 + CL-0005 recorded.
- 15:43 — HORIZON SHAPE (bisection of Xi=0, +-0.003 in X): analytic control X_h = T exactly;
  trained NN Schwarzschild X_h = T within +0.009 (network learned the horizon to ~1%);
  candidate seed124 horizon is a near-vertical line X ~ 0.63-0.65 (delta from analytic
  +0.53..+0.15), seed123 X ~ 0.62-0.71. Quantitatively different horizon geometry, measured.
- 10:22 — PUBLISHED: github.com/AndreiPLK/spacetime-verifier (public, MIT) — verifier + note + audit data + proof packs; the proof-gate workbench deliberately kept private (middle option per founder). 20 tests green standalone; local paths stripped; secret scan clean. Next: ORCID + Zenodo toggle -> DOI.
- 2026-08-13 — PUBLISHED WITH DOI. GitHub release v0.1.1; Zenodo archived the repository:
  DOI 10.5281/zenodo.21915627 (concept 10.5281/zenodo.21915604), record
  zenodo.org/records/21915627. ORCID registered: 0009-0005-5660-2603. Stage-6 gate
  VERIFIED 7/7 — first fully closed public-release gate of the project. Remaining human
  action: JOSS form (values prepared).
- 2026-08-13 (late) — JOSS compliance pass: requirements read in full; submission POSTPONED
  to earliest 2027-02-13 (6-month public-history rule; single-burst histories explicitly out
  of scope) — checked BEFORE submitting, desk rejection avoided. JOSS profile completed
  (email + @AndreiPLK) via founder's browser. Public repo hardened: CI (pytest on
  Linux/Windows, py3.10/3.12) GREEN on GitHub's clean machines; JOSS draft-pdf action GREEN
  (paper.md compiles with their own tooling); CONTRIBUTING.md + CHANGELOG.md added.
  One-pager artifact switched to public link sharing.
- 2026-08-13 13:0x — QG PROGRAM, ITERATION 1 (vertical slice): Eqs. (11)-(13) of 2406.02665
  derived independently from truncation-point crossing (SymPy, pure symbols, N=5): 6/6 PASS.
  Calibration: N=5 ~3 min foreground; N=7 heavy (background). Next slice: exact-rational
  positivity spot-check of one Fig.1 point (in/out of the island).
- 2026-08-13 13:2x — QG ITERATION 2 (PASS): exact-rational positivity machine validated by
  two independent routes (paper Eq. A6 in Fractions VS first-principles residue + exact
  Legendre projection): signs agree everywhere tested; Veneziano clean n<=8; far point
  (-3/2,3/2) excluded with 19 negative coefficients. Bonus: removable singularity in A6 at
  n = mu0+2r+4 documented (naive implementations divide by zero there). Predicted 30 min,
  actual ~25. Next: full Fig.1 island map (visual).
- 2026-08-13 14:xx — QG ITERATION 3 (Fig.1 + Card A start): stacked islands over 7 values of
  mu0 reproduced exactly (allowed counts 399/504/615/664/605/455/302 of 1369); structure
  matches the paper's Fig.1 (wedge, lower lobe, Veneziano marginal). DEPTH ESCALATION at
  mu0=0: N=10 -> 664 allowed, N=20 -> 655 (nine cells fell, ALL in one column r=-3/5,
  w>=1), N=40 -> 655 (STABLE under doubling). Boundary-only N=80 re-test running.
  Early read: the island STABILIZES rather than melting to the Veneziano point —
  candidate first finding of the program (needs N=80 + finer grid before any claim).

## 2026-08-13 — Card A: boundary stable under N=40 -> N=80 doubling
- All 42 boundary cells of the mu0=0 island (allowed cells touching an excluded
  neighbour at N=40) re-tested at unitarity depth n<=80, exact rational arithmetic,
  incremental levels 41..80 only. Result: **0 fell — BOUNDARY STABLE**.
- Island trajectory at 0.1 grid: N=10 664/1369 -> N=20 655 -> N=40 655 -> N=80
  boundary unchanged. The only casualties ever seen: 9 cells, all in column r=-3/5,
  w>=1 (N=10->20). Status: NUMERICALLY_SUPPORTED, grid 0.1, mu0=0, D=4, q=1.
- Artifact: projects/qg-bootstrap/results/boundary_N80_mu0.json
- Ops note: first N=80 attempt died at spawn (exit 127, uv wrapper) with zero log;
  rewritten per compute-runner rules (direct python -u, per-cell progress,
  incremental depth) -> full run ~75 min.

## 2026-08-13 — Author reply received (AInstein audit) + N=2000 re-evaluation
- Dr. Edward Hirst replied (EV-CORR-0001): confirms the search is statistical
  ("sometimes it will converge... sometimes it won't"); reads our seed-124 run as
  approximately Ricci-flat below our threshold; flags 24 hidden points as too few
  (paper standard 2000). No checkpoints offered.
- Response-in-kind: vacuum leg re-running on N=2000 hidden points, all 5 seeds,
  same frozen thresholds (H1/H2 frozen in verifier/vacuum_deep.py BEFORE results).
  Smoke test at N=20 reproduced the 24-point verdicts (123 FAIL / 124 PASS /
  125 FAIL / 126 PASS / 127 FAIL).

## 2026-08-13 — N=2000 vacuum re-evaluation: all five verdicts unchanged
- Hirst's methodological point addressed: hidden test set 24 -> 2000 points
  (paper standard), same frozen thresholds, same evaluator, hidden seeds derived
  from checkpoint sha256. Runtime ~3-5 min/seed.
- seed 123: median 0.9606 FAIL | 124: 0.2223 PASS | 125: 0.3781 FAIL |
  126: 0.1865 PASS | 127: 1.1763 FAIL — identical verdict pattern to the
  24-point run (frozen H1/H2 both confirmed). 2/5 seeds pass the vacuum leg.
- Artifact: projects/ainstein-audit/results/processed/vacuum_deep_N2000.json

## 2026-08-13 — Reply to Hirst SENT (founder pressed Send)
- Content: N=2000 re-evaluation (verdicts unchanged, 2/5 pass), repo+DOI link,
  soft repeat of the checkpoint request. Correspondence continues as EV-CORR-0001.

## 2026-08-13 — ANALYTIC RESULT: the island's left edge is r = -1/2
- Derived in closed form: a_{n,n-1} = K(n)(n(r+1/2)+w)(1+n+r+w)/((2+r)_n(1+r+w)),
  K(n)>0, at mu0=0, D=4, q=1. In the physical domain sign(a_{n,n-1}) =
  sign(n(r+1/2)+w).
- Explains ALL nine N=10->20 casualties exactly (kill level n=10w+1 at r=-3/5,
  matches the measured (n,l) list cell by cell) and why no cell fell afterwards.
- Razor test passed: predicted an exact zero at n=25 for the never-scanned point
  (r,w)=(-13/25,1/2); exact arithmetic confirms a_{24,23}>0, a_{25,24}=0,
  a_{26,25}<0. Plus 60/60 random points.
- Corollary: true left edge of the island at mu0=0 is r=-1/2; finite-N maps
  overstate the sliver (-0.6,-0.5); erosion depth ~ w/|r+1/2|.
- Note: projects/qg-bootstrap/research/left-edge-theorem.md. Independent review
  pending — not promoted beyond "analytic derivation, numerically confirmed".

## 2026-08-13 — Left-edge theorem generalized to arbitrary mu0
- sign(a_{n,n-1}) = sign(n(r+(1+mu0)/2)+w) for n > 3mu0: the island's left edge
  moves as r = -(1+mu0)/2. Razor tests at mu0=+-3/5 passed with exact zeros at
  predicted off-grid points (n=20 and n=15).

## 2026-08-13 — Fine boundary 0.02 + theorem correction + mu0-stack test
- Fine scan (84 boundary squares, 2411 points, NMAX=20 exact): 1321 allowed raw.
- Theorem post-processing removed 176 false positives (r<-1/2 cells doomed at
  n>20) -> 1145/2411 allowed. Artifact: fine_boundary_mu0_N20_corrected.json.
- mu0-stack left edges vs theorem -(1+mu0)/2: EXACT match for mu0 = -9/5, -6/5,
  -3/5, 0 (predicted -0.20/-0.10.../-0.50 all observed). For mu0 > 0 the island
  is cut tighter than the theorem line -> a_{n,n-1} is not the binding
  constraint there; next suspect a_{n,n-2}. Theorem is one-sided (outer bound),
  so no contradiction.
- Visual: article/visuals/qg-island-edge-theorem.png (Relic style, real data).

## 2026-08-13 — a_{n,n-2} closed form + COMPLETE analytic characterization (mu0=0)
- Third trajectory: sign(a_{n,n-2}) = sign[12(2n-1)(1+r)(nr+2w)+n(n^2+5n-2)] —
  kills only in a finite n-window (cubic term wins asymptotically). Verified vs
  brute force n=3..8 (positive constant ratios).
- Killer census over all 714 excluded cells: every binding constraint is either
  n<=5 (explicit curves, e.g. a_{2,0}: 3(1+r)(r+w)+1>=0) or the l=n-1 ladder.
- COMPLETE CHARACTERIZATION TEST: analytic island (n<=5 curves + ladder + domain)
  vs scans: 1369/1369 coarse (N=40, boundary stable to 80) and 2411/2411 fine
  (0.02, theorem-corrected) — ZERO mismatches on 3780 exact points.
- Status: conjecturally complete (n>5, l<=n-2 non-binding proven empirically to
  depth 80); independent domain-critic review pending.

## 2026-08-13 — mu0>0 solved: threshold scalar binds; stack-wide characterization
- Killers at mu0>0 = first above-threshold level n_min = ceil(3mu0 boundary)
  (2/4/6 for mu0=3/5,6/5,9/5), scalar l=0 dominant; symbolic threshold curve
  a_{2,0}(r,w,mu0) derived, factors at mu0=2/3 as (3r+4)(3r+3w+1)/9.
- Analytic verdict vs ALL SIX mu0!=0 maps: 2 perfect; 30 discrepancies total,
  every one a predicted-doomed cell (dist 0.1 from edge, dies at n=10w+1);
  4 verified by direct deep evaluation incl. exact marginal zeros.
- Combined score: 11994 exact points across 7 maps + fine grid, zero true
  mismatches. The island is now analytically characterized across the stack
  (conjectural completeness caveat unchanged; domain-critic review running).

## 2026-08-13 — External control passed: Mansfield-Spradlin agree on the edge at w=0
- Their Theorem 11 (contour asymptotics, w=0): odd-Delta Regge coefficient sign
  ruled by (2r+m^2+1) -> critical line r=-(1+m^2)/2 = our edge -(1+mu0)/2.
  Different method, same line. Our law is exact per-n and covers w!=0 (novel).

## 2026-08-13 — Island Atlas visual
- article/visuals/qg-island-atlas.png: seven mu0 islands, one analytic edge law
  -(1+mu0)/2 overlaid; mu0<=0 islands hug the line, mu0>0 gap = threshold scalar.

## 2026-08-13 — Independent review PASSED; all 7 fixes applied
- Domain-critic verdict: NO algebraic error in the three closed forms; a_{n,n-2}
  bracket upgraded to proven-for-all-n (reviewer's polynomial identity,
  C(n)=24(2n-1)/(n-1)). Adversarial script (6 attacks incl. route1-vs-route2 at
  mu0!=0 and below-threshold sanity) executed: SURVIVED, exit 0. Script archived
  as lab/attack_left_edge.py.
- Fixes applied: domain defined explicitly; n=3mu0 identical-zero edge case
  stated; "true left edge" reworded to exclusion-direction-only; caps header ->
  "conjectured"; redundant r=-1/2,w<0 clause resolved via n=1 block (6 exact
  sample points).
- Card A core status: analytic laws INDEPENDENTLY REVIEWED + adversarially
  survived; completeness of the characterization remains a labeled conjecture.

## 2026-08-13 — Stage-closure cinematic THE ISLAND delivered
- 40 s Godot film (NOVA/viz/island.gd, art-bible style): every plate = real
  allowed (r,w) point (655 coarse + 1145 fine), yellow wall = theorem edge
  r=-1/2, 176 pink crystals = theorem-killed points sinking, probe scans the
  rim. Music Truthfall 0.08 + space rumble at the execution. QC: 6 frames from
  the FINAL mp4 inspected. Copy: article/visuals/qg-the-island-cinematic.mp4.
- Ops lesson archived in reality-production skill: MovieMaker PNG has alpha=0
  on BG pixels; viewers render it white — phantom "white sky" (30 min bisect).

## 2026-08-13 night — Left edge is dimension-universal
- sign(a_{n,n-1}) = sign(n(r+(1+mu0)/2)+w) for all D>3 (x^{n-1} coefficient is
  D-free; Gegenbauer norm positive). 10/10 checks incl. 4 exact zeros at D=6,10.
- The island shrinks with D, but its left edge stays pinned at -(1+mu0)/2.

## 2026-08-13 night N1 — a_{n,n-3} closed form derived and verified
- Ratio to brute force = positive constant for n=4..9 at random (r,w).
- Leading n^3(2r+1): fourth trajectory asymptotically safe for r>-1/2 —
  another brick under the completeness conjecture.
- Video paused by founder; captions switch to ENGLISH on resume.

## 2026-08-13 night N2 (numeric part) — fixed-spin tails clean to n=100
- 10 island points (incl. on-edge r=-1/2 and near-hyperbola): a_{n,l} > 0 for
  l=0..3 at n=10..100, exact arithmetic. Both excluded controls show negatives
  (control valid). Artifact: results/n2_fixed_spin.json.
- New structural note: beyond the edge (r=-3/5) fixed-spin coefficients also
  turn negative at large n (l=1,3 from n=50) — the edge is witnessed at fixed
  spin, not only on the l=n-1 ladder. To derive analytically next.

## 2026-08-13 night N2 (analytic part, in progress)
- Localization at x=1 gives fixed-spin law a_{n,l} ~ (2l+1) * C(r,w)/(n ln n),
  C > 0 in the domain (heuristic derivation; leading order w-free, C ~ 1/(1+r)
  up to a Gamma-ratio integral). Numeric: (2l+1) scaling exact (l=0 vs l=2
  ratios coincide to 3 digits); measured C at 4 points positive, drifting
  logarithmically (0.27..0.86 at n=200). Exact constant + rigor = morning task.
- Implication: fixed-spin family asymptotically safe across the domain —
  completeness conjecture now supported on ALL asymptotic families
  (l=n-1, n-2, n-3 exact; fixed-l asymptotic).

## 2026-08-14 night N3 — D-dependence of binding curves in closed form
- a_{1,0}: D-independent; a_{2,0}: (1+r)(r+w) >= -1/(D-1); a_{3,0}: closed form
  with 1/(D-1) coefficients. D=4 limits reproduce all verified curves exactly.
- Explains analytically why the island shrinks with D while the left edge is
  pinned at -(1+mu0)/2.

## 2026-08-14 night N4 — paper skeleton drafted
- article/qg-island-draft.md: title, abstract, 9-claim status table (honest),
  section plan, figure list, limitations, repro pack. Morning review target.

## 2026-08-14 morning — Comic video delivered (N6)
- article/visuals/comic/comic_island.mp4: 33 s, 8 panels, EN captions, black
  outlines + halftone comic system (panel_style.css reusable), real data in
  every panel (atlas, edge map, MS match, 11994/0 stats). Music Truthfall ->
  Civilize, boom on finale. QC frames from final mp4 inspected.
- Night loop incident: no wakeups fired 00:15-08:16 (machine/app sleep
  suspected); N5 (q-deformation) carried to today.

## 2026-08-14 — Odd/even trajectory dichotomy at the edge
- k=1..7: odd trajectories kill beyond the edge (finite thresholds, predicted
  by our brackets and confirmed exactly: k=3 at n=57, k=1 w=1.7 at n=85);
  even trajectories positive on both sides. Edge witnessed by an infinite
  constraint family. Initial "failures" were finite-threshold effects — now
  quantitatively explained, no contradictions.

## 2026-08-14 — Video abstract for the paper delivered
- article/visuals/vabstract/video_abstract.mp4: 66 s, 1920x1080, academic
  style (7 slides: setting, edge theorem + prediction table, erosion + 176
  corrections, boundary algebra, cross-checks, honest status + repro links).
  Quiet bed, slow fades. QC frames from final mp4 inspected.

## 2026-08-14 N5 — the q-clock: n_crit ~ 1.1/sqrt(q-1)
- q-Veneziano exclusion depth measured exactly for six q values; exponent -1/2
  stable; q=1 control clean. Explains finite-depth scans admitting small q-1.
  New beyond the anchor paper (they had q>1 asymptotic-only).

## 2026-08-14 — q-clock exponent -1/2 mechanically derived
- g(n) = -dlog a_{n,0}/dq |_{q=1} ~ 0.3 n^2 (exact finite difference h=1e-6);
  eps*n^2 ~ 1 crossing reproduces the measured exponent; first-order constant
  1.8 vs measured 1.1 (higher orders kill sooner).

## 2026-08-14 — Big-idea concept video delivered
- article/visuals/qg-island-bigidea.mp4 (35 s, EN): black hole (EHT shader) ->
  "which string theory?" -> landscape slice -> consistency wave sinks bad tiles
  -> glowing edge + formula -> "our piece of the big puzzle". QC 6 frames from
  final mp4. Scenes: NOVA/viz/bh_intro.gd + island_mini.gd (reusable).

## 2026-08-14 — Preprint main.tex written (full draft v1)
- projects/qg-bootstrap/paper/main.tex: complete LaTeX (abstract, setup, edge
  theorem with proof sketch, trajectory laws + dichotomy, island
  characterization as labeled Conjecture, threshold + D-dependence, q-clock
  section, Mansfield-Spradlin relation, honest discussion, AI disclosure,
  repro section). MiKTeX installing for local compile QC.

## 2026-08-14 — Big-idea video v2 (BH -> particle collision -> map), 41 s
- New collide_beat.gd (two particles -> flash: the S-matrix as "the sharpest
  test"); captions rewritten for lay accuracy (probabilities-never-negative =
  positivity; PROVED refers to the exclusion direction which is proven).
- Paper compiled: main.pdf, 5 pages (MiKTeX). Next: internal validation.

## 2026-08-14 — Validation battery round 1 + fixes; story videos RU/EN
- Independent validator (fresh code, no lab imports): PASS 5/5 (razor, a_{2,0}
  law, nine casualties, q-clock spots, D=6 zero).
- Release review: 6 blockers found and ALL FIXED in main.tex v2: correct CHR
  title (PRL 133, 251601), abstract reworded to exclusion-only + mu0>0 caveat,
  novelty scoped to INSPIRE-citing works, repo link removed pending release
  package, n=200 wording matched to artifacts, "unexplained" mismatches,
  finite-difference wording; figures added (atlas + edge map). 6 pages.
- artifacts_battery.py persists all paper-cited computations (census, stack
  11994, dichotomy, q-clock + derivative, D checks, fixed-spin) -> re-running
  after JSON-serialization fix.
- Story videos RU + EN (48 s: BH -> vibrating string -> collision -> map ->
  edge): delivered; frozen-tail bug in batch renders diagnosed (single renders
  fine), segments re-rendered individually, QC of final mp4 tails passed.

## 2026-08-14 — PUBLISHED: qg-island-edges v1.0.0
- github.com/AndreiPLK/qg-island-edges public (repo/release/PDF all verified
  reachable without login, HTTP 200). Founder approved; push executed with his
  explicit authorization after his Run attempts failed. Zenodo DOI pending the
  founder's toggle; then v1.0.1 re-release mints DOI -> final PDF update.

## 2026-08-14 — Portfolio updated and live
- andreiplk.github.io: new work card + one-pager works/qg-island-edges/ with
  paper.pdf and edge map; visibility verified (page 200, paper 200, 5 mentions
  on the front page). Placement checklist vs project 1: GitHub+release+web
  paper+portfolio DONE; Zenodo DOI pending founder toggle; arXiv planned via
  endorsement.

## 2026-08-14 — DOI MINTED: 10.5281/zenodo.21934462
- Zenodo toggle (founder) -> release v1.0.1 -> DOI. Final PDF with DOI in
  author footnote + repro section; pushed to repo and site; DOI badge in
  README, DOI buttons on portfolio. CHR letter draft updated with final links
  (site PDF, repo, DOI); awaiting founder's Send.

## 2026-08-14 — CHR letter SENT by founder; publication stage CLOSED
- Letter (short, human tone) to Cheung cc Remmen with paper/repo/DOI links and
  endorsement request; forward-to-Hillman asked. EV-CORR-0002.
- Stage totals: theorems reviewed+attacked+validated; repo+release v1.0.1;
  DOI 10.5281/zenodo.21934462; site with 'Explain it to anyone' section and
  site-wide readability fix (dark link contrast verified programmatically);
  two outreach letters live (Hirst thread + CHR).
- Next: await replies (CHR endorsement -> arXiv submission); science resumes
  with Card B and the gravity direction (CHR open problem O3).

## 2026-08-14 — GRAVITY SLICE 1 STARTED: the D-clock of Virasoro-Shapiro
- Scientist playbook (12 steps + house methods) saved to permanent memory per
  founder's order; North Star confirmed (are gravitational amplitudes forced
  to be string-like?).
- VS residues derived exactly: R_n(t) = [prod_{k=1}^{n-1}(t+k)]^2 / const —
  double zeros confirmed (CHR O3 gateway).
- First scan: positivity clean to n=16 for D=4..20; D=26 breaks at (n,l)=(3,2).
  The critical dimension D=10 must emerge at depth — a D-clock, mirroring our
  q-clock. Deep scan to n=40 running (lab/vs_d_clock.py).

## 2026-08-14 — VS D-clock deep scan: a CLIFF, not a clock
- D=12..22: positivity clean to n=40. D=24: first negative (4,4); D=26,28,30:
  (3,2). Sharp transition between D=22 and 24 — near the bosonic critical
  dimension 26, NOT a smooth n_crit(D) divergence. Either the true positivity
  bound for massless VS sits at ~23, or the transition is cliff-like.
  Artifact: results/vs_d_clock.json. Literature check + deeper D=22 scan next.

## 2026-08-14 — Novelty radar on the gravity slice (worked as designed)
- Our VS D-cliff reproduces KNOWN physics: arXiv:2210.14920 maps D_crit(n)
  from ~26 (low n) to 10 (n->infinity). Method validated on the gravity side;
  no novelty claim made (playbook step 2 saved us again).
- Found 'Uniqueness criteria for the Virasoro-Shapiro amplitude' — possibly
  the CHR program already done for VS. MUST read before freezing the gravity
  card. Next: deep-read that + 2210.14920, then freeze our unique slice
  (candidate: the deformation-FAMILY island of VS analogs via our
  top-coefficient machinery — the analog of our w!=0 niche).

## 2026-08-14 — GRAVITY CARD FROZEN: exact edge of the closed-string island
- Deep-read 2408.03362 (CHR did O3 themselves!): one-parameter lambda-family
  of VS deformations, residues are perfect squares, D>=9 positivity bounds
  lambda from below -- NUMERICALLY, finite depth, no closed form. Our frozen
  question: lambda_min(D) exactly via top-coefficient method (a_{n,2n-4} law,
  odd trajectories vanish), + erosion clock, + lambda=1 VS cross-check.
- Novelty radar: 37 citing works enumerated; adjacent art flagged (2607.27300
  hidden-zeros analytic bounds -- abstract does not treat the lambda-family;
  full-text verification required before any novelty claim).
- Card: research/gravity-card.md (metric frozen before computing).

## 2026-08-14 — GRAVITY SLICE 1: edge law of the closed-string island DERIVED
- sign a_{n,2n-4} = sign[q_n(lambda) D + p_n(lambda)] with explicit quadratics;
  exact rho(l,D)=(l+1)(l+2)/(2(D+2l-1)). VS thresholds D_n=24,23,24,51/2,136/5
  (min 23 at n=4) EXPLAIN our measured D-cliff to the unit; razor zero D*=45
  at lambda=2 confirmed (+/- bracketing at 44/46). Dangerous lambda-window
  shrinks to pure VS like ~1.1/n. Note: research/gravity-card.md.

## 2026-08-14 — Gravity slice 2: VS threshold in closed form
- D_n(1) = 2(n^2+4n-9)/(n-2), verified 10/10 for n=3..12; min = 23 at n=4.
  The D-cliff of pure closed-string gravity is now a formula. lambda-windows
  for n=3..12 computed exactly.

## 2026-08-14 — Gravity slice 3: alternatives SURVIVE in D=4
- Lemma: near-leading bracket positive-definite at D=4 for all lambda (10/10
  discriminants negative). Exact scan: 13 lambdas incl. corners 1/100, 100 —
  clean, l<=8, depth 60. Headline forming: string uniqueness is
  dimension-graded (free in 4D, forced in high D on these trajectories).

## 2026-08-14 — Gravity slice 4: exclusion map + honest correction
- Exact exclusion belts per D (n<=16): empty for D<=20; [1.03,1.53] at D=22;
  swallows lambda=1 at D=24; widens to [0.81,1.95] at D=40. Extremes survive
  this trajectory. CORRECTED earlier "squeeze toward the string" claim: the
  belt kills the string's NEIGHBORHOOD (and VS itself for D>=24); small-lambda
  corner is killed separately by low-spin constraints (CHR, D>=9).

## 2026-08-14 — BUG FOUND & OWNED: gravity-family Pochhammer step
- ((1+lam)/2+lam*t)_{n-1} increments by 1; my evaluator incremented by lam.
  At lam=1 both coincide -> all VS (lam=1) results REMAIN VALID (D-cliff,
  D_n(1) formula checks at lam=1). All lam != 1 claims (windows, belts, D=4
  lemma/scans, razor at lam=2) are VOID and being recomputed. Found while
  chasing a contradiction with CHR's "D>=9 bounds lambda from below" (my
  small-lambda scans were clean — too clean). Lesson: razor tests that share
  the evaluator with the bracket are circular; independent check caught it.

## 2026-08-14 — Gravity slices corrected: lambda_min(D) in closed form
- Corrected law: positivity <=> D <= T_n(lambda) (quadratics listed in card);
  T_3(0)=9 explains CHR's D>=9 onset; lambda_min(10)=0.0816 matches scanner
  bracket; VS D_n(1) formula unaffected. Buggy belt claims voided.

## 2026-08-14 — Gravity slice 5: lambda_min(D) exact; lambda_min(23)=1
- Single curve: onset D=9 at lambda=0; exact surd values; reaches the string
  exactly at D=23; beyond it for D>=24. n=3->n=4 dominance switch at D~18.

## 2026-08-14 — M2 main frame delivered: THE FATE CURVE
- article/visuals/qg-fate-curve.png: exact lambda_min(D) curve, dead zone,
  string line, magic point (23,1), our-world marker. Lesson delivered (below).

## 2026-08-14 — THE CONTINENT: full body drawn, analytic shore matches
- grav_full_body.json: 560 exact verdicts (lambda 0.05..2 x D 4..30, all even
  spins, depth 14). D<=8 fully alive (40/40); erosion from below as D grows
  (12/40 at D=30). Analytic shore lambda_min(D) traces the frontier; string
  drowns past D=23 as predicted. Visual: qg-continent.png. Founder's question
  "can we draw the full object?" answered: yes — this is it.

## 2026-08-14 — Zoom-out: the whole creature
- grav_zoomout.json (lambda 0.05..10, D 4..60, depth 12): the body is an OPEN
  WEDGE — for every D there survive sufficiently string-y candidates
  (lambda above the shore); the dead mouth widens with D; the string lane
  drowns past 23. Visual: qg-zoomout.png. Doctrine elevated: memorize+improve
  at every step = the main development thread (iteration-doctrine).

## 2026-08-14 — GENERAL LAW: T_n closed form + straight asymptote
- T_n = 3(2n-3)/(n(n-2))(lambda^2+(2n-2)lambda+1)+2n, verified 12/12;
  true shore (n<=400): lambda_min(23)=1 survives; asymptote D=(12+4sqrt3)lambda
  (n* = sqrt(3) lambda). The unfinished-figure question is answered exactly.

## 2026-08-15 night — Complete-model battery: 494/494, zero alarms
- alive <=> D <= min_n T_n matched every exact verdict; executions confirmed.

## 2026-08-15 night — Gravity review round CLOSED
- Claims 1-3 independently re-derived and strengthened; attack script: NO
  FALSIFICATION (0 failures, 4.3 s); fixes F1-F2 applied; completeness stays
  a labeled conjecture with a designated next hunt (a_{n,2n-6}).

## 2026-08-15 — THE BODY: full 3D island assembled from the 7 mu0 slices
- 9583 exact voxels (r, w, mu0) -> isosurface body; the slanted top facet is
  the -(1+mu0)/2 edge tilting with mass shift. Visual: island-body-3d.png.
  Founder's intuition "we hold edges of a full figure" rendered literally.
- Night rules v2 recorded (batch nights, always-background); fast 2n-6 hunt
  running (completeness test of the gravity model).

## 2026-08-15 — 2n-6 hunt: zero alarms; completeness conjecture strengthened

## 2026-08-15 — Pop-science key insight visual delivered
- string-inside-vs-edge.png: two-panel "inside vs on-the-wall" — the core
  meaning of both papers in one glance (gravity is the stricter judge).
  Yellow diamond visibility issue in the 3D bow noted (opaque body) — cutaway
  version queued.

## 2026-08-15 — Paper 2 goes public: package, GitHub, site
- Paper 2 final: 6 pages, max visuals per the new explain-to-everyone law
  (Fig 3 = 3D cliff of survival, new "Explain it to anyone" section,
  Fig 4 = companion ship's bow as fun). Lost 
ef repaired (CR byte).
- B6 closed: generators written for grav_zoomout (v2 matches original 330/330),
  hunt_2n8 (0 alarms, 680 checks, now with metadata), lowspin_stress (0 alarms).
- Package release/qg-gravity-shore assembled per release-review manifest;
  EV-CORR-0002 (private correspondence) excluded from public evidence file;
  py_compile all green, smoke run clean, secret scan clean.
- Published: github.com/AndreiPLK/qg-gravity-shore (main), portfolio one-pager
  live with Explain-it-to-anyone + 3D media. Zenodo toggle = founder's click.

## 2026-08-15 — DOI minted, publication complete
- Zenodo toggle by founder -> release v1.0.0 -> DOI 10.5281/zenodo.21944818.
- Final PDF (DOI in footnote + Reproducibility) recompiled, propagated to the
  public repo (v1.0.1), the site one-pager (DOI button), package README badge,
  CITATION.cff. Letter 2 draft ready (same thread, no-ask tone), awaiting
  founder Send.

## 2026-08-15 — Letter 2 sent by founder
- Reply in the same CHR thread, no-ask tone, no em-dashes (new standing rule:
  no AI-sounding style in letters). Contents: T_n law, D>=9 onset explained,
  shore through VS at D=23, asymptote, repo + DOI. EV-CORR-0003.
- Paper 2 pipeline CLOSED end to end: science -> review -> package -> GitHub
  -> site -> Zenodo -> DOI -> final PDF -> letter. Same-day publication.

## 2026-08-15 — SECOND KNIFE LAW (l = 2n-6): closed form found
- Symbolic brackets extracted for n=4..9 (polynomial Pochhammer ratios killed
  the gamma soup; sympify-locals bug found and fixed). All spot signs match the
  exact evaluator.
- The bracket collapses to ONE line: with m=n-3, s=lam+n-1, u=D+4m+1,
  Bhat = alpha*u*(u-2) - G*u*s^2 + s^4,
  G = 2(m+1)(m+3)/(3(2m+3)), alpha = (m+3)(5m^3+21m^2+19m+15)/(45(2m+1)(2m+3)).
  Exact relations verified on all six levels: R = 8mA, W = A(16m^2-1),
  V = P(4m+1). Structure: QUADRATIC in D => the knife cuts a WINDOW of D,
  releasing at large D (first knife was a half-line).
- Live confirmation: predicted string window at n=7 (D~26.2..30.3) confirmed
  by exact evaluator: a_{7,8}<0 exactly at D=28,30; positive at 26 and 32.
  Window lies BELOW the shore (string already dead at D=24) => completeness
  conjecture untouched so far; analytic dip-check is the next slice.
- Blind grid verification running: law fitted on n=4..9, scanned n=4..12
  (n=10..12 never seen by the fit), lam 0.1..20, D 4..40, exact arithmetic.

## 2026-08-15 — Slice 9: the window never dips below the shore
- Blind law check: 2052/2052 exact sign agreements (fit n=4..9, scan n=4..12).
- Dip scan with BOTH closed forms (lam 0.05..100 dense, n 4..300): the 2n-6
  negativity window stays ABOVE min_n T_n everywhere; closest approach
  margin 2.17 dimensions at lam=0.05, n=6. Large-lambda tail (lam 200..1000,
  n to 4*lam): margin grows (336 at lam=200). Zero dips.
- CONSEQUENCE: the completeness conjecture survives its strongest analytic
  attack to date: the second knife is now a THEOREM-GRADE formula and it
  provably (numerically, closed-form scan) never cuts into conjectured-alive
  territory on the scanned ranges. Artifact: t2n6_window_vs_shore.json.

## 2026-08-15 — Slice 10 (EXPLORATORY): the lambda dial of D=4 survivors
- Known-answer gate did its job TWICE: first version expected zeta(3) at
  lam=1 and FAILED (R(n,0)=1/n^2, not 1 - my reference was wrong, machinery
  right); corrected anchors c3(1)=zeta(5), c5(1)=zeta(7) pass to <1e-10.
- Moment sums c_k = sum R(n,0)/mu^k, dial ratios r_k = c_k/c_k(1):
  r3 runs 0.965 (lam=0.1) -> 1.076 (lam=20); r5: 0.992 -> 1.095.
  Monotone in lambda; two moments give independent coordinates.
- Meaning (exploratory): the surviving D=4 family members differ from the
  string by only ~3-10% in these low-energy moments - the dial exists and is
  monotone (distinguishable in principle), but the family is low-energy
  QUASI-STRING-LIKE. Artifact: eft_map_d4.json.

## 2026-08-15 — MASTER STRUCTURE of all knives (j = 2..5 verified)
- Every knife l = 2n-2j has the LADDER form:
    B_j = sum_{i=0}^{j-1} (-1)^i a_i(n,j) s^{2i} PROD_{k=i}^{j-2}(D + 4n-4j-1 + 2k)
  (s = lam+n-1; ladder of D-shifts step 2, top factor always D+4n-2j-5).
- Overdetermination test at j=5, n=6: 16 monomial coefficients vs 5 ladder
  dof - ALL 16 match exactly (a = 4096, 15360, 23760, 16800, 4725).
- j=2 (T_n law) and j=3 (Bhat law) are the ladder's first two rungs:
  j=3 exact relations R=8mA, W=A(16m^2-1), V=P(4m+1) are ladder identities.
- Remaining open piece: closed form of a_i(n,j) (generating coefficients).
  Data in hand: j=2 all n (exact), j=3 n=4..9 (closed form known), j=4
  n=5..10 (bg finishing), j=5 n=6. Next: fit/derive a_i(n,j).

## 2026-08-15 — MASTER FORMULA derived and verified (candidate paper 3 core)
- Derived (not fitted): residue roots + exact monomial-Gegenbauer integral
  I(l+2u,l)/I(l,l) = (l+2u)!/(l! u! 4^u (alpha+l+1)_u) + Pochhammer clearing
  => sign a_{n,2n-2j} = (-1)^{j-1} sign SUM_i (-1)^i E_{2(j-1-i)}(n)
  (2n-2j+2i)!/(i!2^i) s^{2i} PROD_{r=i}^{j-2}(D+4n-4j-1+2r).
- Verified: 21/21 symbolic bracket matches (j=2..5); 16-monomial
  overdetermination at j=5; 702/702 sign grid vs exact evaluator INCLUDING
  blind j=6. Note: research/master-formula.md.
- Next: (a) all-j window-vs-shore scan (completeness); (b) paper 3 draft.

## 2026-08-15 — COMPLETENESS BATTERY VIA MASTER FORMULA: 1,538,164 / 0
- Every knife j=3..n-1, n<=40, every even D inside the conjectured-alive
  region, lam 0.05..50: ZERO alarms. The j=2 envelope min_n T_n is the
  boundary as far as every trajectory constraint can see.
  Artifact: master_completeness_scan.json (160s runtime).
- Paper 3 drafting starts now.

## 2026-08-15 — Paper 3 review round 1 closed
- Critic (independent, from-scratch evaluator, no lab imports): integral
  identity CORRECT (mechanical interpolation proof, 3465 checks); master
  formula CORRECT (re-derived by hand end-to-end); his attack script executed
  by lab: EXIT 0, 4060/4060 signs incl. odd D, non-integer D (7/2, 53/7),
  lam 0.01/100, n=15; j=2 roots = exact amplitude zeros 24/24.
- Defects fixed: (1) sign typo in generating identity (tex); (2) float
  region boundary in completeness scan -> exact rational floor; (3) scan
  extended to ALL integer D: now 3,053,832 checks, 0 alarms; (4) abstract
  wording tempered (finite ranges, l>=2, formula-dependency stated).
- Paper recompiled (4 pages). Remaining before publication: release-review,
  package, founder's go.

## 2026-08-15 — Paper 3 published to GitHub + site; Zenodo = founder click
- All 7 release blockers + 8 warnings closed; master_checks.py PASS
  (22/22 symbolic, 15/15 monomials, 702/702 signs); window_vs_shore.py and
  fig_knives.py persisted; figure regenerated with fresh battery count.
- github.com/AndreiPLK/qg-master-formula live (main); portfolio one-pager
  + index card live. Awaiting founder Zenodo toggle -> v1.0.0 -> DOI ->
  final PDF -> letter 3.

## 2026-08-15 — PAPER 3 PUBLISHED: DOI 10.5281/zenodo.21947272
- Founder toggled Zenodo -> release v1.0.0 -> DOI minted -> final PDF (DOI in
  footnote + Reproducibility, W5 abstract fix) -> repo v1.0.1 -> site updated
  with DOI button. Final QC circle: 4 PDF pages eyeballed, package
  master_checks re-run in place (PASS), site 200, repo PDF 200.
- THREE papers published in the program, all with DOI. Letter 3 next
  (founder send).

## 2026-08-15/16 — BLADE THEOREM: proof 95% closed (paper 4 core)
- THEOREM (proven, certificates in results/blade_proof.json, exit 0):
  for ALL lambda <= 26.1 and ALL levels n, the j=3 negativity window lies
  strictly above the shore min_k T_k. Architecture: branches k=3..45;
  per-cell semantics (no-window via disc root isolation) OR (B(T_k)>0 AND
  vertex condition), all in exact arithmetic. The closest-approach zone
  (margin 2.17 dims at lam=0.05) is INSIDE the proven region.
- LEMMA (proven): for lam >= 26 no level n <= 81 has any window at all
  (78 univariate certificates, k-free).
- OPEN CELL (last): n >= 82 AND lam > 26 (deep water). Polya diverges due to
  branch drift at infinity; needs tip/off-tip regime split. Battery coverage
  meanwhile: scans to lam=1000, margins >= 336 dims there.
- v1/v2 prover lessons: (1) fixed-width symbolic-k branches drift from the
  argmin (linear in k) - certify explicit branches instead; (2) cell logic
  must include the no-window alternative; (3) head-pipe on a background run
  kills the process before it writes artifacts - log to file.

## 2026-08-16 — BLADE THEOREM COMPLETE (pending final adversarial review)
- Tail lam >= 26 closed with four lemmas, all by exact certificates:
  T0 (m<=78: no windows at all, 78 univariate certs);
  L2 (windows require s <= (4/3)(m+3): S2max <= (16/9)(m+3)^2, two
  positive-coefficient certs, m>=79);
  L1 (envelope <= (12+4sqrt3)lam for lam>=26, k=floor(sqrt3 lam)+2,
  certificate over Q(sqrt3), 9/9 monomials);
  L3 (deep water: Bhat(u_A)>0 and u_A<vertex at the asymptote shore bound,
  region s<=(4/3)(m+3), certs over Q(sqrt3), 40+21 monomials, 0 bad).
- KEY discovery en route: the tangency at infinity is EXACT: the margin
  quadratic 6 rho^2 - (12+4sqrt3) rho + 8+4sqrt3 has a DOUBLE root at
  rho = 1+1/sqrt3 (discriminant exactly 0) - the blade cone is tangent to
  the shore asymptote; windows live at rho <= sqrt(5/3) < 1+1/sqrt3, which
  is why the theorem holds and why naive Polya diverged.
- Full prover: one command (lab/blade_proof.py), ALL CERTIFIED, exit 0.
- Recheck rule applied (founder 2026-08-16: recheck important math many
  times): brute force 60,000 random points incl. deep water and tangency
  direction: min margin 2.18 dims, zero counterexamples. Independent
  adversarial review of the full proof chain launched (logic audit +
  numeric attack + certificate rebuild).

## 2026-08-16 — Critic round on the blade theorem: GAP FOUND AND FIXED
- Critic verdict: GAP FOUND (740 uncovered (k,m) cells from an escalation
  off-by-bug: range backfilled only 1 of 6 skipped m-values), theorem NOT
  refuted; all other audit points (junctions, strictness, vertex logic,
  L2 squaring, L1 floor bookkeeping) sound. The lab's 'ALL CERTIFIED' was
  false as a coverage statement - the review gate did exactly its job.
- Fix: backfill range(m_start-6, m_start) on escalation; full prover re-run:
  ALL CERTIFIED, exit 0 (75s), coverage verified in artifact.
- Critic's independent battery (attack_blade_theorem.py, no imports from the
  prover, own exact evaluator, re-certifies the 740 gap cells) running.
- Lesson: 'exit 0' proves what the script CHECKED, not what it COVERED;
  coverage must be auditable from the artifact (per-cell log now includes
  every m).

## 2026-08-16 — BLADE THEOREM ESTABLISHED (both gates passed)
- Critic battery (attack_blade_theorem.py, independent evaluator): exit 0,
  NO COUNTEREXAMPLE; all branch cells incl. the 740 gap cells re-certified
  independently; tail lemmas rebuilt from scratch. Artifact attack_blade.json.
- Paper 4 placeholders filled with the honest review story (gap found,
  fixed, re-verified). Ready for release-review.

## 2026-08-16 — Paper 4 published to GitHub + site; Zenodo = founder click
- All release blockers closed incl. honest margin numbers (inf ~2.15 as
  lam->0, not attained; 2.17 was a grid-edge artifact) and 4/3-vs-sqrt(5/3)
  attribution. Both provers re-run on clean HEAD with metadata.
- github.com/AndreiPLK/qg-blade-theorem live; portfolio one-pager + card
  live (hero: the tangent fleet; the caught-bug story told openly).

## 2026-08-16 — PAPER 4 PUBLISHED: DOI 10.5281/zenodo.21948833
- Founder toggle -> v1.0.0 -> DOI -> final PDF (DOI in footnote + repro) ->
  repo v1.0.1 -> site with DOI button. FOUR published works in the program,
  all with DOI; the fourth carries the lab's first fully proven theorem.

## 2026-08-16 — Dashboard + a beautiful negative result
- github.com/AndreiPLK profile dashboard live (news EN, program progress bar,
  latest visual); standing rule: update at every milestone.
- NEGATIVE RESULT (logged honestly): the Schoenberg shortcut to the grand
  theorem dies. Q itself is NOT positive-definite inside the allowed region
  (negative Gegenbauer coefficients of Q at every test point, e.g. n=7
  lam=1 D=22: b_4<0) - so positivity of Q^2 rests on cancellation structure,
  not on Q-PD + product theorem. The grand theorem needs the per-j
  certificate road (or a smarter identity).

## 2026-08-16 — BINOMIAL COLLAPSE: every knife is a power of the first
- Scaling limit of the master formula (m->infty, rho=s/m, u=(delta+4)m):
  term_{i+1}/term_i = -[(j-1-i)/(i+1)] * X with X = 6 rho^2/(delta+4)
  => B_j ~ term_0 * (1 - X)^{j-1}. EVERY knife's bracket is, at leading
  order, a PERFECT POWER of the first knife's linear form. One critical
  surface u = 6 rho^2 m for all j; minimizing over levels reproduces
  rho* = 1+1/sqrt3 and the envelope asymptote - the tangency of the blade
  theorem is the j=3 shadow of this universal structure.
- Exact-arithmetic verification (n=30..60, j=2..6): all negativity zones of
  all knives cluster within ~O(sqrt(m)) offsets (-50..+30) of the level's
  critical line, splitting into floor(j/2) zones - exactly the degenerate
  root of (1-X)^{j-1} splitting at subleading order. Sign pattern matches
  the (-1)^{j-1} convention: even-j knives kill on the dead side only,
  odd-j knives cut thin slabs hugging the line.
- GRAND THEOREM ROADMAP: (1) binomial collapse organizes the large-m tail
  UNIFORMLY IN j (one lemma instead of infinitely many cones); (2) moderate
  m stays on exact certificates per the blade architecture; (3) remaining
  hard core: subleading (sqrt-m) control of slab edges near the optimal
  level. Caveat logged: the asymptotic critical line is quantitatively far
  from exact T_n at moderate m (checked: n=8, lam=5: 152.8 vs exact 94) -
  the collapse is a tail tool, not a substitute for certificates.

## 2026-08-16 — Publication strategy v2 (founder decision)
- No more mini-papers: full rigor per result (freeze, artifacts, critic,
  batteries) but output = research note + site news/media only. One FLAGSHIP
  paper when the grand theorem lands (integrating shore + master + blades +
  collapse). The scientist decides and announces when a result is
  paper-worthy. Paper 5 stays as research note collapse-lemma.md; its critic
  round continues as an internal gate.

## 2026-08-16 — Deep completeness battery: 25,002,978 / 0
- Night task (fixed KeyError, ensure_E(80)): ALL knives j=3..n-1, n<=80,
  every integer D inside the conjectured-allowed region, lam 0.05..200:
  ZERO alarms (results/completeness_deep_n80.json). The conjecture's total
  battery now exceeds 25M exact verdicts.

## 2026-08-16 — Documentооборот запущен; первый кейс — фантом
- docs/ERRATA.md создан (правило основателя: любая ошибка в опубликованном
  исправляется везде с формальной записью).
- ERR-0001 (окно 30.3 в paper 3) оказался ФАНТОМОМ: published v1.0.1 уже
  содержала 30.4 (W2 закрыт до публикации). Ошибочный erratum-релиз v1.0.2
  отозван немедленно. Урок в реестре: проверяй published-артефакт, не память.
- Попутно: paper5-нота — все правки критика внесены (E1-E6, скоуп пояса,
  rate rescoped, замыкающая лемма); батарея критика attack_collapse
  исполнена (прямое подтверждение центрального предела; два F5-флага о
  скорости учтены в формулировке).

## 2026-08-16 — KNIFE 4 SHALLOW CERTIFIED: the general-j architecture works
- knife_proof.py (interval positivity, no window bookkeeping): j=4, branches
  k=3..45 (lam <= 26.1), m=2..40: ALL 1677 cells certified, 0 failures,
  130 s. The per-knife theorem conveyor is OPEN.
- Remaining for the j=4 theorem: shallow m-tail (m>=41; negativity provably
  escapes upward, linear in m vs bounded T_k - certificate stage designed)
  and deep water (reuse j-free L1 + direct region certificates). Then j=5,6...
  and the fixed-spin regime for the j-tail of the grand theorem.

## 2026-08-16 — Knife 5 shallow certified; Bernstein trick added to the conveyor
- KNIFE_J=5 shallow: 1634/1634 cells, 43 branches, 209 s, zero failures.
  Shallow now certified for knives j=3,4,5.
- Incident: first j=4 tail/deep attempt hung >15 min on a 3-var symbolic
  expansion (killed per compute-runner rules). Fix: BERNSTEIN-IN-D
  decomposition - the bracket is degree j-1 in D, so interval positivity
  reduces to j Bernstein coefficients, each with ONE variable fewer.
  Reusable for the whole conveyor. Rerun in progress.

## 2026-08-16 — Knife-4 deep-tail: the diagonal fight (honest log)
- Bernstein v1 (rational subs): hung, killed. Double Bernstein (polynomial
  subs): shallow-tail 43/43 in 19 s + deep-fixed OK; deep-tail FAIL.
- Drift-free k-parametrization (v2): still FAIL. Quad-bisection depth 3:
  still FAIL (487 s) -> diagnosis: the tight direction is DIAGONAL
  (optimal level tracks the branch, m* ~ K+49); per-coefficient positivity
  in (v, K) is blind along diagonals.
- v3 (running): split v relative to the diagonal: below (v=(K+4)sigma,
  Bernstein in sigma, root isolation in K) and above (v=K+4+v'').

## 2026-08-16/17 — Knife-4: proven everywhere EXCEPT one region (honest map)
- v3 diagonal split verdict: above-diagonal (m >= optimal band) CERTIFIED;
  below-diagonal FAIL after 1936 s of subdivision. Combined with earlier
  stages, knife-4 is now PROVEN on: all lam <= 26.1 (all levels); deep water
  fixed levels m <= 40; deep water m above the optimal diagonal. OPEN: deep
  water, 41 <= m below the optimal band (m ~< K+49), lam >= 26 - margins
  there are O(1) against O(500) scales (0.04% relative), the cubic analogue
  of the blade theorem's core. Next tool: a cubic root-separation lemma
  (D < r1 characterization), not more subdivision.
- Night queue: exact battery over the open region (knife 4, levels below
  optimal, lam 26..300, D <= envelope) + j=5 tail stages.

## 2026-08-17 — Knife-4 below-diagonal: margin measured, elevation deployed
- MEASUREMENT (the scientific move after two certificate failures): exact
  scan of knife-4 first-negativity edge vs envelope in the open region:
  MINIMUM MARGIN = 5.0 dimensions (n=90, lam=54) - healthier than the blade
  theorem's 2.15. The theorem is comfortably true; the certificate is
  technically blind, not the math.
- Cure: Bernstein DEGREE ELEVATION (BERN_ELEV=8) + targeted stage flag
  (KNIFE_STAGE=belowdiag) to re-run only the stubborn cell. Also v4's
  Descartes-at-cap lemma stays: positivity of all y-coefficients of
  P(T_cap - y) covers the whole half-line D <= T_cap - the universal
  deep-water tool for every knife degree.
- j=5 tails running in parallel (E-interpolation range bug fixed).

## 2026-08-17 — Knife-4 endgame: v5 recon + plan handed to the night
- v5 (K-split): FAIL uniformly across K=0..7 => the tight sliver is at the
  diagonal FROM BELOW, not at branch edges. Key asset: the INTERVAL 2D
  Bernstein method (deep_cell3) PASSED above the diagonal including the
  optimal band itself (the tightest zone, margin 5.0) - so the fix is to
  SHIFT the cut down (v >= K-6 by the working interval method; v <= K-6 by
  Descartes-at-cap where margins are fat). Night task queued; morning
  session implements if night placeholder does not.
- j=5 tails: shallow-tail 43/43 OK + deep-fixed OK (72 s) - awaiting
  diagonal verdicts.

## 2026-08-17 — Knife-4 (iv) far-below: three certificate attempts, night fan
- Interval chain and orthant variants both blind on the fat-margin far
  region (sign mixing of comparable ladder terms). Night fan queued:
  compact4d Bernstein (both orthant vars compactified) at elevations 6/12,
  then orthant at elevation 16. Everything else of knife-4 is CERTIFIED:
  shallow full, deep fixed, above-diagonal, diagonal band, first branches.

## 2026-08-17 — Knife-5 tails verdict: mirrors knife-4 exactly
- j=5: shallow-tail 43/43 OK, deep-fixed OK, ABOVE-diagonal OK (9827 s),
  below-diagonal FAIL - the same single structural blind spot as j=4.
  The pattern is systematic: one recipe (the shift assault + whatever cracks
  the far-below piece) closes BOTH knives; then the conveyor is mechanical
  for j=6..8. Night fan is working the far-below variants.

## 2026-08-17 (после перезагрузки app) — ИСТИННЫЙ ДИАГНОЗ far-below
- Ночной детачнутый батч ПЕРЕЖИЛ перезагрузку приложения (v3-архитектура
  оправдалась) — веер вариантов продолжает счёт.
- ДИАГНОЗ третьего порядка: в far-below регионе точное значение
  P(T_cap) = t0*(X-1)^3 + O(1/m)-поправки, где X = 6rho^2/(delta+4) и
  X-1 ~ 0.03 у границы с лентой: позитив — КУБИЧЕСКИ малое сокращение
  (~3e-5 относительных). Именно поэтому слепнут ВСЕ покоэффициентные
  сертификаты (Бернштейн любой степени, ортанты, Декарт у мыса): они
  смешивают гигантские члены, чья разность — куб малой величины.
- ЛЕКАРСТВО (утренняя сессия): КООРДИНАТЫ КОЛЛАПСА — точная замена
  Z ~ 6s^2 - m(D+c): разложить лесенку по Z (это её родной
  Ньютоновский базис узлов -c-2r); в этих координатах позитив должен
  стать явным ((X-1)^3 - ведущий член с положительным коэффициентом).
  Прогноз: ночной веер вариантов не пробьёт (та же слепота) - и это ок,
  его отрицательный результат подтвердит диагноз.

## 2026-08-17 — KNIFE-4 THEOREM COMPLETE + разбор сбоя
- FAR-BELOW ЗАКРЫТ: sp.factor раскрыл структуру (кубы коллапса ЯВНО в
  факторизации: (K3+v+51)^3 (K3+v+53)^3 x позитивный фактор deg 15, все
  574 монома точно положительны в Q(sqrt3)); все 4 y-коэффициента Декарта
  у мыса явно положительны => P>0 на всём луче D<=T_cap. Вместе с ранее
  сертифицированными 6 регионами: ТЕОРЕМА НОЖА 4 ПОЛНА (все n, все lam).
  Артефакт: knife4_farbelow_factored.json. Урок-инструмент: ФАКТОРИЗУЙ
  ПРЕЖДЕ ЧЕМ СЕРТИФИЦИРОВАТЬ — факторизация снимает третьепорядковую
  слепоту, которую не берут Бернштейн/ортанты любой степени.
- РАЗБОР СБОЯ (правило основателя): три причины, три железных фикса —
  в skill sciencebro-scientist (нарезка задач, протокол воскрешения,
  10-минутные идеи сразу).

## 2026-08-17 (ночь) — Knife 6 shallow certified
- KNIFE_J=6 shallow: 1591/1591 cells, 43 branches, 369 s, zero failures.
  Shallow now certified for knives j=3..6. Knife 7 at branch 24/45 and
  climbing; knife 5 far-below factoring (night batch).

## 2026-08-17 (ночь) — Knife 7 shallow certified
- KNIFE_J=7 shallow: 1548/1548 cells, 43 branches, 729 s, zero failures.
  Shallow certified for knives j=3..7. Knife 6 tails running; knife 5
  far-below factoring (night batch).

## 2026-08-17 (ночь) — KNIFE 5 FAR-BELOW CLOSED => knife-5 theorem complete
- knife5_farbelow_factored.json: far_below_factored = true, 5/5 y-coefficients
  manifestly positive after exact factorization over Q(sqrt3); runtime 2923 s.
  Knife-5 theorem now COMPLETE (pending adversarial review), same architecture
  as knife 4. Consolidated: results/knife5_theorem.json.

## 2026-08-17 (ночь) — PROVER V2 (flint engine): 28-57x speedup, validated
- lab/prover2_core.py + lab/knife_proof2.py: exact fmpq arithmetic (flint),
  B_j built once per m, denominators cleared analytically (p+2q<=2(j-1)).
- Validation contract passed: shallow j=4..7 reproduce v1 cell-by-cell —
  identical verdicts AND cell counts (1677/1634/1591/1548).
  Runtimes: 130.6->2.3 s (57x), 209->5.7 s, 350->12.4 s, 729->24 s.
- Memory: MB instead of GB. New standing rule: machine never loaded to 99%.
- v2 immediately deployed: shallow j=8..12 running.

## 2026-08-17 (ночь) — Shallow certified to j=12; Z3 pilot; tools digest
- Prover2 shallow: knives 8-12 ALL CERTIFIED (1505/1462/1419/1376/1333 cells).
  Shallow stage now proven for j=3..12.
- Z3 pilot: independent SMT check of a certified cell (j=4,k=3,m=2): unsat in
  0.0s — foreign-engine confirmation path opened for the validator role.
- docs/LINKS_DIGEST.md: 22 links verified (GitHub API), 3 adopted, 1 adopting.
- Adversarial workflow-critic (diamond) launched on knife-4/5 theorems.

## 2026-08-17 (ночь) — ADVERSARIAL FLEET VERDICT: theorems 4-5 DOWNGRADED
- Fleet (36 agents, 7 zones x fresh-context skeptics, 2 refuters per finding):
  13 confirmed findings, 3 FATAL-class on knife 5. Zone verdicts: numeric
  anchor SOUND (4000+ adversarial points, zero violations of the CLAIM);
  tail-deep-stages / region-tiling / artifact-honesty BROKEN (proof chain).
- Key gaps: (1) knife-5 below-diagonal band {m>=41, K-6<v<K+4} has NO
  certificate (shift script was hard-coded J=4); (2) lam in (0,1/1000) strip
  covered by no stage for j>=4 (k=3 branch starts at 1/1000; blade j=3 used
  the onto substitution); (3) knife_tail_deep artifacts record only a global
  all_certified=false, per-stage results discarded; STAGE/FAR_MODE env not
  recorded — partial run can masquerade as full; (4) knife-4 far-below has
  no script (command: "to be scripted").
- ACTIONS: statuses downgraded in knife{4,5}_theorem.json (this commit);
  repair plan: lam-strip patch + belowdiag generalization to j=5 + artifact
  writer fix + full re-runs with per-stage artifacts. Full report:
  results/adversarial_review_knife45.json. Failures stay visible.

## 2026-08-17 (ночь) — Charter deltas + repairs in flight
- Anchor papers verified via arXiv API: 2406.02665 (our frozen anchor),
  2512.17828 (Regge trajectories for UV completions of graviton scattering
  from polynomial bounds), 2606.09980 (Where is tree-level heterotic string
  theory?) — the two new ones queued for full-text evidence records.
- python-fxint: zero occurrences in repo (nothing to fix).
- .claude/skills/research-iteration/SKILL.md created (iteration must end in
  an artifact; truth/novelty status taxonomy; honest time estimation).
- Repairs running: shallow j=5..12 re-run with onto-zero lambda coverage;
  knife5 belowdiag band+K0 queued behind knife6 tail (machine-load rule).

## 2026-08-17 — Z3 independent judge, knife 4 shallow: 1642/1677 confirmed
- Foreign engine (Z3 nlsat) independently re-proved 1642 of 1677 shallow
  cells (unsat), ZERO alarms, 35 unknown (120 s timeout) — retry with 600 s
  + interval splitting running. Keystone prior art captured: Mansfield
  2502.20372 (Veneziano positivity ALL levels D<=10), Rigatos-Wang
  2401.13031 (harmonic-number manifest positivity), Eberhardt-Mizera
  2201.11575 (uniform-in-level asymptotics).

## 2026-08-17 — Keystone step 2: Mansfield architecture mapped + first probe
- Mansfield 2502.20372 read (pp. 1-8): uniform-in-j via convolution recursion
  Q^{j+1}=Q^j+Q^j*G with positive Gregory kernel + finite exceptional set.
  Transfer plan frozen in research/keystone-plan.md (H_rec hypothesis).
- First probe (exact, 972 ratios, l=2,4,6, n=6..40, belt grid): P>0 at every
  point, ratio P_{n+1}/P_n in [740, 1.3e6] — bounded well away from zero.
  H_rec (positive-kernel recursion along fixed-spin diagonal) strongly
  supported numerically. Artifact: results/keystone_ratio_probe.json.

## 2026-08-17 — KNIFE-5 FATAL GAP CLOSED: below-diagonal band + K0..K5
- KNIFE_J=5 PIECES=band,k0 knife_belowdiag_shift.py: ALL CERTIFIED
  (band K>=6 + explicit K0..5; 1913 s; artifact knife5_belowdiag_shift.json
  with honest per-piece verdicts). Combined with knife5_farbelow_factored
  (v<=K-6) and above-diagonal (tail rerun queued), the deep-water quadrant
  for j=5 is now fully covered by passing artifacts.

## 2026-08-17 — Keystone probe 2: kernel with constant works
- Exact K0 (ratio of i=0 master-formula terms) is too big alone: R<0 at ~35%%
  of belt points, BUT the ratio P_{n+1}/(K0 P_n) >= 0.295 EVERYWHERE on the
  grid (936 exact checks, worst at l=6 n=6 lam=12 D~=T_hat). Refined H_rec:
  P_{n+1} >= c*K0*P_n with c=1/4 — enough for induction (any c>0 propagates
  positivity). Proof route: collapse form P = term0*(1-X)^{j-1}*(1+err) with
  bounded err — connects keystone to the Binomial Collapse note (article 5).
  Artifact: results/keystone_kernel_probe.json.

## 2026-08-17 — Keystone hunt complete: 109,980 exact checks, 0 violations
- Fixed-spin regime (l=0,2,4,6 diagonals, n<=120, boundary-hugging exact
  grid incl. D within 1e-6 of T_hat): NO violations. The grand-theorem
  claim survives its most dangerous regime. results/keystone_hunt.json.

## 2026-08-17 — Keystone: two simple lemmas FALSIFIED (preserved), binomial insight
- FALSIFIED (grid level): (a) uniform alternating dominance |t_{i+1}/t_i|<=q<1
  fails at shore-bottom D=4 large lam (ratio up to 6767); (b) V-shape
  (monotone ratios) fails at 360/360 points; pure two-regime A/B does not
  cover (worst gap 51). Failure signature: ratio profile matches BINOMIAL
  weights C(j-1,i) — nonmonotonicity is exactly binomial.
- INSIGHT: the right lemma is about NORMALIZED X: rho_i = t_{i+1}(i+1) /
  (t_i (j-1-i)) ~ X uniform; belt: X<=Xmax<1 => P >= t0(1-Xmax)^{j-1}.
  Outside belt a separate argument is needed (as in per-knife proofs).
- Today's conveyor extended: belowdiag+farbelow for knives 6-7 queued
  (queue 2 after tail re-runs) => four COMPLETE knife theorems (4,5,6,7)
  targeted today; infinite-j remains the keystone (research continues).

## 2026-08-16 — Keystone: candidates 3 and 4 falsified (fast kills)
- H-mono (S monotone in each rho): FALSIFIED 1855/4000 random tests.
- H-X (normalized rho < 1 in inner belt): FALSIFIED, rho up to 22.9 at
  small lam / large n fixed spin (top-dominated zone).
- Product-form conjecture (fixed spin P factors into (lam+2k-1)(lam+2n-2k-1)):
  FALSIFIED — sp.factor: P irreducible for n=5..8, l=2.
- Score: 4 approaches killed in hours (protocol working: counterexamples
  before proofs). Strongest remaining: Eberhardt-Mizera-style uniform
  large-n asymptotics at fixed spin (2201.11575, full text on disk)
  + machine conveyor for all finite j (automated per-j certificates).

## 2026-08-16 — Keystone route update (AEHM read, pp. 15-23)
- AEHM honestly failed to rigorize fixed-spin (their 4.3.1) — confirms the
  keystone is field-hard; Mansfield route (induction) is the rigorous one.
- STRUCTURAL FIND: CHR residue = SQUARE of a product of linear factors in t
  (Pochhammer^2) = exactly AEHM closed-string structure => their
  triple-contour machinery (3.23-3.24, App. C) is the direct template for
  a CHR contour representation with lam as a parameter. Route A/B/C frozen
  in research/keystone-plan.md.

## 2026-08-16 — Z3 retry done: 24/35 hard cells confirmed
- Foreign-engine total for knife-4 shallow: 1666/1677 cells unsat-confirmed,
  0 alarms; 11 cells remain unknown after 600 s + 4-way splitting (recorded
  honestly; certificates for them stand on prover v1+v2 agreement).
- Repair batch relaunched at full priority (8 tasks, fast wins first).

## 2026-08-16 — Keystone Step A validated: residue-bridge holds
- Gegenbauer quadrature of the CHR squared-Pochhammer residue (50-digit
  mpmath, t = mu(n)(x-1)/2) matches the master-formula bracket sign at all
  5 cross-check points (n=5..8, lam=0.5..12, D=8..20). Our knives ARE
  partial waves of a squared product of linear factors — the AEHM
  closed-string triple-contour machinery applies. Step B (derive the
  contour rep for CHR with lam parameter) is now the active front.

## 2026-08-16 — Accelerator verdict: harmonic-numbers method TRANSFERS to CHR
Read Rigatos-Wang 2401.13031 (pp. 1-6). Three structural matches:
1. Their residue = product of linear factors in t (eq. 20); ours = SQUARED
   product (Pochhammer^2) — same class, doubled roots.
2. Their key identity (eq. 21): coefficients of the t-expansion are multiple
   harmonic numbers = elementary symmetric functions of the roots. Ours are
   EXACTLY that already: E-hat from prod(1+(n-2k)z)^2 (paper 3).
3. Their trajectory-wise analysis (eqs. 29-32): k-th trajectory below leading
   = explicit combination of <=k+1 harmonic numbers, analyzed FOR ALL N at
   once. Our knives ARE those trajectories (a_{n,2n-2j}).
NEW TOOL they add that we lack: SUM RULES (eq. 26) from equating two
expansions of the residue — candidate source of the j->j+1 recursion with
explicit kernel (what our probes hunted blindly). Next shortest experiment:
derive CHR sum rules numerically, then in closed form.

## 2026-08-16 — CHR SUM RULES VERIFIED (keystone milestone)
- Rigatos-Wang eq.(26)-type sum rules derived for CHR and verified to 1e-41
  at (n,lam,D) = (5,2,10), (6,0.5,8), (7,12,23): sum_l c_l T_{l,m} = Zhat_m
  with Zhat = elementary symmetric of DOUBLED Pochhammer roots (our E-hats),
  T from Gegenbauer expansion at angle x = 1 + 2t/mu. All knives at level n
  now sit in ONE linear system with harmonic-number data — the doorway to a
  closed single-sum formula and the j->j+1 relation. Next: invert T (their
  eq. 25/27 analog) in closed form for CHR.

## 2026-08-16 — v2 PORT of farbelow: 11-35x, knife-6 far-below CLOSED
- lab/knife_farbelow2.py: N built in flint (uniform den^(J-1) clearing,
  contract bug caught by validation and fixed). Verdicts match v1:
  j=4 CLOSED 14s (v1 152s), j=5 CLOSED 83s (v1 2923s, 35x).
  j=6 FAR-BELOW CLOSED (first ever, ~8 min vs hours on sympy).

## 2026-08-16 (вечер) — FAR-BELOW CLOSED FOR ALL FOUR KNIVES (4,5,6,7)
- knife7_farbelow_factored.json: CLOSED, 7/7 coefficients, 1316 s on the
  flint build (v2 port). Far-below now closed j=4 (14s), j=5 (83s),
  j=6 (438s), j=7 (1316s) — all honest artifacts, engine recorded.
- Queue 3 running: belowdiag j6/j7 (v1, ~30-60 min each) then honest tail
  re-runs j4/5/6/7. Then: reconsolidation of theorems 4-7 through the gate.

## 2026-08-16 (ночь) — TAILS PORTED TO V2: all four knives certified in SECONDS
- lab/knife_tail2.py (flint): shallow-tail + deep-fixed + above-diagonal
  for j=4/5/6/7 ALL CERTIFIED, ~1-2 s each (v1: hours). Below-diagonal is
  covered by dedicated belowdiag_shift + farbelow artifacts (no overlap
  gaps: band[K-6,K+4] + K0..5 + far v<=K-6 + above-diag = full quadrant).
- Remaining for four complete theorems: belowdiag j6/j7 (v1 queue running).

## 2026-08-16 (ночь) — Keystone: T-inverse structure found
- Universal T^{-1} rows for CHR are strictly ALTERNATING (+-+-...) with
  smooth weight ratios (hypergeometric-looking). Hence c_{n,l} =
  alternating functional of elementary symmetric functions of POSITIVE
  (doubled) Pochhammer roots. Positivity for ALL n at fixed l becomes a
  real-rootedness statement — the classical total-positivity door.
  Next: closed form of weights w_{l,m} (ratio fit), then the n->n+1
  3-term recursion e_m(S+{r,r}) = e_m + 2r e_{m-1} + r^2 e_{m-2}.

## 2026-08-17 (ночь) — FOUR COMPLETE KNIFE THEOREMS (4,5,6,7), GATE GREEN
- belowdiag2 (flint port): j=5 contract-matched v1 in 1 s (v1: 32 min);
  j=4/6/7 closed in ~1 s each. ENTIRE prover now on v2.
- Reconsolidated knife{4,5,6,7}_theorem.json: status COMPLETE pending
  adversarial review; every cited artifact PASSES; deterministic gate
  (test_theorem_gate) GREEN. Coverage: onto lam->0, full deep-tail tiling.
- v1 queue retired (v1 remains as cross-check twin only).
- Knives proven: 2,3 (published) + 4,5,6,7 (tonight). Next: fleet review
  round 2, then the keystone (uniform j).

## 2026-08-17 (ночь) — FLEET REVIEW 2: math SOUND, artifact layer repaired (S1-S8)
- Verdict: zero counterexamples in 6 attack zones; two independent
  re-derivations (from-scratch sympy master formula; Gegenbauer projection
  1200/1200 sign agreement) + ~93k exact in-region evaluations, 27k of them
  within 1e-9 of D=T_hat. Sign flips ABOVE T_hat confirmed => statement tight.
- Repairs landed: S1 truthful coverage (m>=max(1,j-2), l>=2); S2 provenance
  stamp with CODE-only dirty flag + full re-run at clean HEAD; S3 gate
  hardened (j-match, work counters, nested verdicts, partial-run env, dirty,
  prose regions); S4 STRICT positivity implemented and CERTIFIED (every
  Bernstein block has a strictly positive constant term => P > 0 on the
  CLOSED region, not merely >= 0) for j=4..7 in tails and belowdiag;
  S5/S6 unsound latent branches deleted; S7 J-consistency assert; S8
  far-below artifacts now carry scope/per-coefficient/monomial counts.

## 360-ANALYSIS of the strictness finding (founder's law 3.1)
1. INSIDE: strict P>0 everywhere including the closed shore boundary is
   NOT in conflict with the blade theorem's exact tangency: tangency there
   is of the WINDOW EDGE to the shore (discriminant zero at rho*), not a
   zero of the bracket P. Two different objects — worth one sentence in the
   flagship to prevent a referee confusing them.
2. NEIGHBOURING AMPLITUDES: Veneziano/type-I partial waves VANISH whenever
   n+j is even (parity zeros, AEHM eq. after 3.9; Mansfield table 1). Our
   CHR brackets have NO such zeros — strict positivity holds across the
   whole ladder. Structural difference: the CHR residue is a SQUARE of a
   Pochhammer ratio (no parity cancellation), whereas Veneziano's residue
   has alternating-parity structure. => the square is what buys strictness.
3. ADJACENT MATH: strictly positive Bernstein blocks = the polynomial lies
   in the INTERIOR of the Bernstein cone on that box. For families indexed
   by n this is the setting of total positivity / Polya-type theorems: a
   uniform interior margin is exactly what an induction in j would need.
   => concrete keystone lead: quantify the interior margin as a function of
   (j, n) and prove it does not degrade — a quantitative strictness lemma.

## 2026-08-17 (ночь) — *** CHR CLOSED FORM VERIFIED (4320 exact checks) ***
   P_j = c0 * SUM_t (-1)^t E_2t(n) (1-j)_t (1-R)_t / ((1-n)_t (3/2-n)_t s^2t)
   s = lam+n-1, c = 4n-4j-1, R = (D+c)/2+j-1, c0 = (2n-2)!/((j-1)!2^{j-1}) s^{2(j-1)} > 0.
- 4320/4320 exact rational agreements with the master formula, j=2..25,
  n up to j+25, lam from 0.01 to 150, D from the shore to 3x beyond it.
  Artifact: results/chr_closed_form.json, script lab/chr_closed_form.py.
- WHY IT MATTERS: (a) the sum TERMINATES via (1-j)_t => classical
  terminating-hypergeometric machinery (Saalschutz/Whipple/Gasper) applies;
  (b) ALL j-dependence is now explicit — (1-j)_t and the positive c0 — so
  the j -> j+1 step of the keystone is a Pochhammer shift, not a mystery.
- Falsified on the way (signatures kept): MOMENT hypothesis (c_t are NOT a
  Stieltjes moment sequence — Hankel minors negative at every tested point);
  LEIBNIZ hypothesis (term ratios exceed 1 in 26516/91728 belt samples,
  max 57 at large lam near the cap) — so no naive alternating-series bound.

## 2026-08-17 (night) — FIVE COMPLETE KNIFE THEOREMS (4,5,6,7,8), gate green
- Knife 8 fully certified on v2 and consolidated; ALL artifacts re-run at a
  CLEAN commit (the hardened gate rejected the dirty-tree ones — it works).
- SECOND MANIFESTNESS DISCOVERY: far-below needs NO factorization — in the
  (thL, v, K3, y) chart every coefficient of N is already nonnegative for
  j=4..8 (hours -> seconds). sp.factor was the last sympy bottleneck; the
  prover is now flint end-to-end.
- HONEST LIMIT: manifestness BREAKS at j=9 — coefficient c7 has 11 negative
  monomials of 1752. Bernstein elevation (2/4/8) and thL-bisection (depth 6)
  both FAIL => real structure, not a chart artifact. Factorization fallback
  queued. A precise, reproducible boundary of the phenomenon.

## 360-ANALYSIS: manifest positivity and where it ends
1. INSIDE: manifestness holds in BOTH charts for j<=8; monomial count is
   FULL (j(2j-1) in shallow — zero cancellations). At j=9 exactly one
   coefficient (c7, second-highest y-power) breaks. Testable prediction:
   the fragile index tracks the top y-powers, not the bulk.
2. NEIGHBOURS: Mansfield had to "add a clever zero" precisely because
   Laurent coefficients went negative in D=10; our c7 is the same species
   in a different chart. His cure (null term + induction) is the next tool.
3. ADJACENT MATH: positivity on a region WITHOUT a nonnegative-coefficient
   representation is exactly the Polya/Bernstein gap. Degree elevation is
   guaranteed only for compact regions — ours is unbounded in (v, K3),
   which explains the failure. Correct tools: Handelman/Positivstellensatz
   with the region's own constraints, or a chart compactifying v and K3.

## 2026-08-17 (night) — j=9 far-below: method boundary CONFIRMED (negative result)
- Compactification (v=V/(1-V), K3=W/(1-W)) + Bernstein elevation on the
  resulting compact chart: negatives GROW with elevation (11 -> 15 -> 45 ->
  134). Conclusion: the y-coefficient criterion ("every coefficient of the
  D = T_cap - y expansion is nonnegative") is SUFFICIENT, not necessary,
  and it genuinely stops being satisfied at j=9. Not a bug, a boundary.
- Consequence for the pipeline: knives j>=9 need a different far-below
  certificate (interval Bernstein in D on [4, T_cap] as in v1 belowdiag,
  or Handelman with the region's constraints), NOT the y-expansion.
- Preserved failure signatures: MOMENT, LEIBNIZ, high-spin ABEL induction
  (1.46% violations on the large grid), Bernstein elevation, thL-bisection,
  compactification. Six honest negatives — each narrows the keystone.

## 2026-08-17 (night) — CARD A1 PILOT: positivity alone does NOT pin the string
- Perturbing the SQUARED-residue roots away from the Pochhammer values
  (r_k -> r_k(1+eps_k), |eps| up to 0.1) at n=9, lam=1, D=10: 120/120
  perturbations keep every knife j<=6 positive (control eps=0 passes too).
- Reading: positivity is an OPEN condition — at a single level it cannot
  select a functional form. What actually rigidifies the CHR family is
  CROSSING SYMMETRY tying the residues of DIFFERENT levels together.
- Consequence for card A1 (recorded in research/NEXT_GOAL.md): the
  deterministic falsifier MUST impose crossing across levels, not just
  positivity at one level. Rewritten evaluator: perturb the generating
  data (spectrum + a global root rule), then check crossing exactly and
  positivity for n <= 20 — only then is a survivor meaningful.
- Value of the pilot: it kills a naive version of the search before it eats
  a week of compute, and it sharpens the North Star question: the string
  rigidity we are chasing lives in CROSSING x POSITIVITY, not positivity.

## 2026-08-17 (night) — QUADRATIC-FORM hypothesis FALSIFIED (7th negative)
- Since the residue is a SQUARE, E_2t = sum_i e_i e_{2t-i} (convolution), so
  P_j = c0 * e^T M e with M block-Hankel from B_m = (-1)^m A_m. If M were
  PSD, positivity would hold for ARBITRARY root sets. It is NOT: 779/912
  parameter points have a negative eigenvalue (min -7.8e-5).
- 360-ANALYSIS of this negative (it is informative, not just a dead end):
  1. INSIDE: positivity is therefore NOT a formal consequence of "residue =
     square". It genuinely uses WHICH roots CHR has — the arithmetic
     progression r_k = ((1+lam)/2 + k)/lam. Any proof MUST use the
     progression; generic-square arguments cannot work. This kills a whole
     class of attempted proofs at once (valuable pruning).
  2. NEIGHBOURS: same lesson explains why Veneziano proofs (Mansfield,
     AEHM) all lean on the explicit Gamma/Pochhammer structure rather than
     on abstract positivity of squares.
  3. ADJACENT MATH: elementary symmetric functions of an ARITHMETIC
     PROGRESSION have closed forms via Stirling numbers / q-binomials, and
     such families are exactly where Gasper-type positivity theorems live.
     => NEXT SHORTEST EXPERIMENT: substitute the AP closed form for e_i into
     the closed form of P_j and look for a Gasper-summable structure.

## 2026-08-17 (night) — *** SQUARE IDENTITY *** (second structural result)
   sum_t (-1)^t E_{2t}(n) x^t = [ prod_{a in S_n} (1 - a^2 x) ]^2 = G_n(x)^2
   where S_n = {n-2k > 0} — verified symbolically for n=7,10 (exact).
- WHY: the CHR root multiset {n-2k} is SYMMETRIC (contains +-a in pairs),
  so the doubled-root generating function collapses to a perfect square.
  The alternating E-sum is therefore NONNEGATIVE FOR EVERY x — the sign
  problem in the master formula is entirely carried by the WEIGHTS A_t.
- Consequence: P_j = c0 * L[G_n^2] where L is the linear functional with
  L[x^t] = A_t. Positivity of P_j is now the single statement
  "L is nonnegative ON THIS ONE SQUARE" — not on all squares.
- FALSIFIED (8th negative, exact Bareiss determinants, not floats): A_t is
  NOT a moment sequence — Hankel minors of order 2 are negative at 42/42
  tested parameter points. Reason found: A_t is log-CONCAVE (ratios
  A_t/A_{t-1} decrease), while moment sequences must be log-convex.
  => No positive measure exists; the "integrate G^2 against dmu" route is
  closed for good. The remaining route is the ORTHOGONAL-POLYNOMIAL one:
  expand G_n^2 in the basis where L is diagonal (L's own orthogonal
  polynomials) — the expansion coefficients are then explicit and their
  signs decide the theorem. NEXT SHORTEST EXPERIMENT for the next session.

## 2026-08-17 (day) — ORTHOGONAL-POLYNOMIAL route: L is INDEFINITE (9th negative)
- Gram-Schmidt for the functional L (L[x^t] = A_t) at four representative
  belt points: the norms L[p_i^2] have signs ++-, ++-+, ++-++, +-+-+- —
  i.e. L is INDEFINITE (as expected from non-momentness) and the sum
  L[G^2] = sum c_i^2 L[p_i^2] mixes signs. So the orthogonal expansion does
  NOT by itself decide positivity: the theorem lives in the interplay of the
  expansion coefficients c_i of THIS square with the indefinite norms.
- Sharper consequence (this is progress, not just a dead end): positivity of
  P_j is equivalent to a WEIGHTED inequality between the c_i^2 of G_n^2 in
  L's orthogonal basis — a finite, explicit inequality for each (j, n).
  The keystone is now: prove that inequality uniformly in j.

## 2026-08-17 (day) — far-below BOUNDARY BROKEN: interval certificate works
- lab/knife_farbelow3.py: instead of the y-expansion (fails from j=9), map
  D to a FINITE interval, D = 4 + (T_cap-4)*th, and certify with Bernstein
  in (thL, th) + orthant in (v, K3). Result: far-below CLOSED for
  j = 4,5,6,7,8,9,10,11 in 0-222 s each (ONE cell, no bisection needed).
  => knives 9, 10, 11 now have all four regions; consolidated as COMPLETE.
- Keystone hypotheses 9 and 10 falsified: (9) L's orthogonal norms have
  mixed signs (L indefinite) so the orthogonal expansion alone does not
  decide; (10) the Hankel form H_{pq}=A_{p+q} is NOT always Lorentzian —
  exact Jacobi-rule signature counts give 1, 2 or 3 negative directions
  (63/96/73 cases). Two more clean negatives, each with a signature.
- Structural map of the hard regime (fixed spin, n -> inf): argmax_t |a_t|
  grows like ~n/4 (3,5,7,11 at n=12,20,30,44) and the tail after the max is
  1-3 times the max itself. So no crude majorant can work: the theorem
  needs the exact cancellation, confirming the binomial-collapse picture.
- NEW LEAD (from the closed form): our G(x) = prod (1 - a^2 x) with a in an
  arithmetic progression is exactly the argument structure of the RACAH /
  WILSON polynomial family (quadratic-lattice orthogonal polynomials).
  If L[G^2] is a connection coefficient in that family, positivity may be a
  known theorem. Next: literature check on that specific identification.

## 2026-08-17 (day) — WEIGHT FACTORISATION: the sharpest reduction so far
- Decomposed the weights: A_t = M1_t * M2_t with
    M1_t = (j-1)^{(t)} / (n-1)^{(t)} = C(j-1,t)/C(n-1,t)   [falling factorials]
    M2_t = (R-1)^{(t)} / ((n-3/2)^{(t)} s^{2t})
- **M2 IS a moment sequence** (exact Hankel minors nonnegative) => M2_t =
  int v^t dnu(v) with nu >= 0. Therefore
      P_j ~ int Phi(v) dnu(v),  Phi(v) = sum_t (-1)^t E_2t M1_t v^t
  — the theorem is reduced to ONE function of ONE variable.
- **M1 is NOT a moment sequence** (exact minors negative) — that is where the
  sign problem now lives, and it is a single explicit object: a ratio of
  binomial coefficients.
- FALSIFIED (12th, 13th): Phi(v) >= 0 for all v >= 0 is false (309/780);
  and Phi >= 0 even on the (crudely estimated) support of nu is false —
  violations appear ONLY at the far edge of the support and are small
  (worst relative -0.05). So the theorem is true not because Phi is
  positive, but because nu puts little mass where Phi dips. That is a
  QUANTITATIVE statement — the first one that is both necessary and
  sufficient in this chart, and the natural next target.
- 360-ANALYSIS: this is exactly the structure of Gasper-type positivity
  proofs for Jacobi/Racah kernels — positivity of an integral whose
  integrand changes sign, closed by an explicit majorant on the measure.
  Concrete next experiment: compute nu explicitly (it is a finite discrete
  measure — the moments terminate) and check the weighted inequality
  sum_k nu_k Phi(v_k) > 0 term by term. Finite, exact, decidable.

## 2026-08-17 (day) — *** THE CRITICAL ZONE = THE OLD TANGENCY *** (strategy)
- Built the MARGIN MAP: margin(j, lam) = 1 - |dip|/plateau over the reduced
  one-variable inequality (artifact results/keystone_margin_map.json).
  Structure found:
    * lam <= 2      : margin 0.15-0.25 (comfortable)
    * lam ~ 4..50   : margin collapses to 2e-4 — the CRITICAL ZONE
    * lam >= 100    : margin ~ 1 (trivial)
  The critical zone MOVES with j: lam_crit ≈ 1.7 j (7 at j=6, 14 at j=10,
  30 at j=18).
- CANDIDATE LINK (honest status: SUGGESTIVE, not established): our published
  blade theorem found an EXACT TANGENCY at rho* = 1 + 1/sqrt(3) ≈ 1.577 in
  rho = lam/k. The measured critical ratio lam_crit/j averages 1.27 (spread
  1.0-1.67) on a coarse lam grid, i.e. the SAME ORDER but not yet matched.
  Refining the grid to locate lam_crit(j) precisely is a cheap next test; if
  it converges to rho*, the grand theorem''s hard core is exactly the
  tangency we already beat for j=3.
- STRATEGY that follows (three regimes, only one is hard):
    (i) lam small: crude majorant suffices (margin >= 0.13 everywhere tested);
    (ii) lam large: margin -> 1, trivial;
    (iii) lam ~ rho* k: the tangency regime — reuse the exact machinery from
         the blade theorem (discriminant identity at rho*, window confinement)
         instead of generic bounds. THIS is the keystone's real content.
- This reframing is why 14 generic attempts failed: they all tried to beat a
  regime where the margin is 2e-4 with tools that need a finite margin.

## 2026-08-17 (day, close) — canyon located; one numeric alarm raised and cleared
- Golden-section search for lam_crit(j) (artifact results/keystone_lamcrit.json):
  the canyon floor sits at lam_crit ≈ 10.7 (j=8) rising to ≈ 18.8 (j=16),
  with the minimum margin shrinking monotonically: 4.9e-3 -> 3.4e-4.
  The ratio lam_crit/j is NOT constant (1.34 -> 1.17 -> then falls), so the
  suggested identification with rho* = 1+1/sqrt(3) is NOT supported by this
  measurement. Recorded as such: the link stays a hypothesis, downgraded.
- ALARM AND RESOLUTION (protocol: never leave a negative unexplained): at
  j=24 the quadrature reported a NEGATIVE margin (-0.17). Direct exact check
  of P_j by the master formula at 15 belt points (j=24, n=32, lam 7..30):
  ALL POSITIVE. So the negative margin is a NUMERICAL artifact — Hankel
  systems of order K=12 are catastrophically ill-conditioned in float.
  Consequence for the method: the margin map is trustworthy only up to about
  j <= 16 in floating point; beyond that it needs exact rational quadrature.
  Logged as a tool limitation, not a mathematical one.
- Day's net: the keystone is now localised (a canyon whose floor we can
  compute), the two structural results stand, and 14+ approaches are
  documented as dead ends with signatures. The remaining task is an exact
  argument inside the canyon.

## 2026-08-17 (canyon) — *** THE CANYON HAS AN EXACT ASYMPTOTIC LAW ***
- Replaced the ill-conditioned quadrature with a DIRECT exact computation of
  the margin: margin(j) = (sum of even terms - sum of odd terms)/(even sum),
  all in rational arithmetic. Values for j = 8..40 (artifact
  results/keystone_asymptotics.json, exact):
     j= 8: 1.618e-07   j=20: 2.985e-14   j=30: 2.062e-19
     j=12: 5.023e-10   j=24: 2.608e-16   j=36: 1.589e-22
     j=16: 3.392e-12   j=28: 2.237e-18   j=40: 1.324e-24
  Every value STRICTLY POSITIVE; the theorem holds with an exponentially
  small but nonzero margin.
- LAW: the ratio margin(j)/margin(j+2) converges: 10.82, 10.85, 10.88, 10.91,
  10.93, 10.95, 10.96 (j = 26..40), i.e. an exponential law with base
  q ≈ 11.0 per two units of j (it passes 4+4sqrt3 = 10.928 near j=35 and
  keeps rising slowly — the limit is ~11.0, exact value not yet identified).
- SADDLE: the dominant term sits at t*/j ≈ 0.40-0.44, stable across
  j = 10..30 — so the sum is a genuine Laplace/saddle-point problem, and the
  exponentially small answer is the classic signature of near-total
  cancellation resolved by a COMPLEX saddle (exactly the technique AEHM used
  for their contour representation).
- CONSEQUENCE — the proof architecture is now fully specified:
  (1) write the alternating sum as a contour integral (Mellin-Barnes);
  (2) locate the complex saddle at t = alpha j, alpha ≈ 0.42, and extract the
      leading term with its explicit POSITIVE constant;
  (3) bound the remainder uniformly for lam in the canyon;
  (4) finite set of small j closed by the machine (already done for j<=12).
  This is the same skeleton Mansfield used for Veneziano; ours now has
  measured constants to check every step against.

## 2026-08-17 (canyon) — *** CONTOUR REPRESENTATION FOR CHR OBTAINED ***
Verified numerically to 1e-13 (j = 5..10):

    P_j / c0 = (1/2pi) * INTEGRAL_0^{2pi} G_n(x)^2 * Psi_j(1/x) dtheta,
    x = r e^{i theta},  any r inside the first singularity,
    G_n(x) = prod_{a in S_n} (1 - a^2 x),   S_n = { n - 2k > 0 },
    Psi_j(y) = SUM_{t=0}^{j-1} A_t y^t,
    A_t = (1-j)_t (1-R)_t / ( (1-n)_t (3/2-n)_t s^{2t} )  > 0.

KEY SIMPLIFICATION found on the way: since [x^t] G^2 = (-1)^t E_{2t}, the
alternating signs CANCEL against the master formula's signs. The bracket is
therefore a pairing of POSITIVE weights A_t with the (sign-alternating)
Taylor coefficients of a perfect square — not an alternating sum of positive
terms. That is a structurally different and much friendlier statement.

Why this matters: this is the CHR analogue of the AEHM/Mansfield contour
representation (arXiv:2201.11575 eq. 2.10-2.11, arXiv:2502.20372 eq. 2.11).
Both existing proofs of all-level positivity (Veneziano, D<=6 and D<=10) work
by manipulating exactly such a contour integrand into a manifestly positive
form. We now have the same handle for the graviton family with lambda.

Immediate next steps inside the canyon:
  (a) deform the contour to the saddle at t*/j ~ 0.42 (equivalently a specific
      |x| in the integrand) and extract the leading asymptotics with an
      explicit positive constant;
  (b) attempt Mansfield's trick: add a term with vanishing residue that
      cancels the negative Laurent coefficients of the integrand;
  (c) both are now concrete manipulations of one explicit integral.

## 2026-08-17 (canyon, evening) — integrand structure mapped; 15th negative
- Negative Laurent coefficients of the contour integrand sit on a STRICT
  CHECKERBOARD: even NEGATIVE powers (-2, -4, -6, ...) and odd POSITIVE
  powers (1, 3, 5, ...); the x^0 coefficient (= the answer) is positive.
  Fraction of negative coefficients grows slowly: 0.41 (j=6) -> 0.45 (j=12).
- FALSIFIED (15th): adjacent pairing (cancel each odd term with its even
  neighbour) does NOT work — 1-3 pairs out of 3-7 stay negative for every j
  tested. So a local Leibniz-style pairing cannot close the theorem, in line
  with the earlier Leibniz failure.
- What the pairing test DOES tell us: the cancellation is NON-LOCAL — the
  positive mass that beats a given negative term sits several indices away.
  That is precisely what Mansfield's "add a vanishing-residue term" trick is
  for: it redistributes the mass globally inside the contour integral.
- Progress this session (all recorded, all reproducible): exact margin law
  (positive, decaying by ~11x per +2 in j), saddle position (t*/j ~ 0.42),
  the CONTOUR REPRESENTATION (verified 1e-13), and the checkerboard structure
  of the obstruction. The keystone is now a concrete manipulation of one
  explicit integral rather than a search for a strategy.

## 2026-08-17 (canyon, 19:45) — SADDLE = THE LARGEST DOUBLE ROOT
- Optimising the contour radius (minimax of |coef * r^k|) cuts the oscillation
  of the integrand from 10^21 down to 10^6 (j=8), 10^27 -> 10^7.6 (j=10),
  10^33 -> 10^8.6 (j=12).
- The optimal radius is r* = 3.2e-3 ... 5.6e-3, which equals 1 / a_max^2 with
  a_max = n-2 EXACTLY (1/16^2 = 3.9e-3, 1/18^2 = 3.1e-3). So the saddle sits
  precisely at the LARGEST DOUBLE ROOT of G^2 — the outermost zero of the
  perfect square.
- Interpretation: the asymptotics of the bracket are governed by the local
  behaviour of the integrand at that double zero. This is the concrete local
  model to expand: G^2 vanishes quadratically there while Psi(1/x) is large,
  and their product's residue is what survives.
- Residual oscillation at the saddle still grows like ~0.6 orders per +2 in j,
  i.e. exactly the q^{j/2} law of the margin. Conclusion: no numeric or
  majorant method can win; the cancellation must be done ANALYTICALLY at the
  double zero. That is now the single remaining technical task.

## 2026-08-17 (canyon, 20:30) — the cancellation is localised at theta = pi
On the saddle circle |x| = x0 = 1/a_max^2 the integrand's maximum sits at
theta = pi EXACTLY (i.e. at x = -x0, the negative real axis) for every j
tested (8, 10, 12, 14). Ratio |answer| / max|integrand|:
    1.44e-06 (j=8), 1.45e-07 (10), 1.67e-08 (12), 2.06e-09 (14)
— a factor ~10 per +2 in j, matching the measured margin law exactly.

So the whole story is now one localised computation: the bracket equals a
stationary-phase integral around theta = pi, where G^2(-x0) is a large
POSITIVE number (product of (1 + a^2 x0)^2) and Psi(-1/x0) oscillates. The
exponential smallness is the phase cancellation there, nothing else.

Next technical step (fully specified): expand G^2 and Psi around x = -x0,
apply stationary phase, read off the leading coefficient. If that coefficient
is positive for all j (it should be, given 40 exact data points), the grand
theorem follows for large j, with small j already machine-proven (j <= 12).

## 2026-08-17 (canyon, 21:40) — WHY D=6 IS SPECIAL (independent derivation)
- Wrote the weight kernel as a terminating 3F2[1-j, 1-R, 1; 1-n, 3/2-n; z]
  with z = -1/s^2. The SAALSCHUTZ condition on the PARAMETERS
  (sum of numerator params + 1 = sum of denominator params) holds
  identically iff R = 3/2 + 2n - j, i.e. **exactly when D = 6** — verified
  for all tested (j, n). This is an independent, structural explanation of
  why D <= 6 is the "manifest unitarity" case throughout the literature
  (AEHM sec. 4.1, Mansfield sec. 2.1) — here derived for the graviton family.
- HONEST LIMIT: Saalschutz needs z = 1, ours is z = -1/s^2, so the classical
  summation does NOT apply directly. Measured: the kernel value at D=6 is
  0.9945 (j=6), 0.9969 (8), 0.9981 (10) — tending to 1 as j grows, i.e. the
  kernel is a small perturbation of unity in that corner. Recorded as a lead:
  a transformation carrying z to 1 (Thomae/Bailey) is the natural next tool.
- Interpretation for the flagship: D=6 sits at a distinguished point of the
  hypergeometric parameter space; the physical "critical dimensions" of the
  literature are shadows of classical summation conditions. Worth one
  paragraph in the paper regardless of how the keystone closes.

## 2026-08-17 (canyon, 23:00) — *** THE MECHANISM: ABEL-PLANA, exponent pi*alpha ***
The exponential smallness of the bracket in the canyon is now EXPLAINED, not
just measured:
- For an alternating sum, the Abel-Plana formula gives
      SUM (-1)^t f(t)  ~  exp(-pi * y*) * (prefactor),
  where y* is the distance to the nearest complex singularity of f(t).
- Measured decay: the margin falls by q ≈ 10.9 per +2 in j, i.e. the exponent
  is ln(q)/2 = 1.19438 per unit of j.
- Solving 1.19438 = pi * alpha gives alpha = 0.38018.
- INDEPENDENTLY measured saddle position: t*/j = 0.40 ± 0.02 across
  j = 10..30. The two numbers agree to within the grid resolution
  (pi * 0.379 = 1.19066 vs 1.19438 observed; predicted q = 10.82 vs 10.90).
=> The canyon's exponential smallness is the Abel-Plana suppression of an
   alternating sum whose singularity sits at t = alpha*j with alpha ~ 0.38.

WHY THIS MATTERS: it converts "the margin is mysteriously tiny" into a
standard asymptotic computation with a KNOWN mechanism. The remaining work is
to evaluate the Abel-Plana prefactor and show it is positive — the prefactor
is an explicit integral of our f along the imaginary axis. That is the
narrowest formulation of the keystone we have ever had:
      keystone  <=>  positivity of one explicit Abel-Plana prefactor.
Also: this explains a posteriori why 15 earlier attempts failed — every one of
them was a real-axis estimate, and the answer lives off the real axis.

## 2026-08-17 (canyon, 23:50) — naive Abel-Plana FAILS (16th negative), but the
## exponent match stands
- Applying the standard Abel-Plana formula to the analytic continuation of a_t
  (via Gamma-ratios, pole-free at integer j) misses the true value by 6 orders
  of magnitude. Reason understood: Abel-Plana is for INFINITE sums of decaying
  f; our sum TERMINATES at t=j because of (1-j)_t, and the continuation keeps
  growing past t=j, so the boundary terms dominate. Recorded as negative #16.
- What survives: the numerical coincidence exponent = pi * alpha with
  alpha = 0.380 vs measured saddle 0.40 +- 0.02 is still the best explanation
  of the exponential law; it just has to be derived from the CONTOUR integral
  (which is exact for a terminating sum) rather than from Abel-Plana.
- Next concrete step: find the COMPLEX saddle points of the contour integrand
  G^2(x) Psi(1/x) — solve d/dx log(integrand) = 0 numerically, then deform the
  contour through them. That is precisely the AEHM manoeuvre and it is exact
  for our finite sum.

## 2026-08-18 (canyon, 01:30) — naive saddle summation FAILS (17th negative)
Summing the two dominant complex saddles with the standard Gaussian formula
overshoots by 250+ orders of magnitude (10^254 vs the true 6.7e-4). Cause is
textbook: with several saddles present, only those on the correctly deformed
steepest-descent path contribute (Stokes phenomenon), and the naive sum adds
exponentially large non-contributing ones. Recorded as negative #17.
Correct route: determine the steepest-descent topology (which saddles are
"active" for our parameter range) before summing — the same care AEHM took
when deforming to the Hankel contour. This is a well-defined but delicate step
and is now the single open item of the keystone.

## 2026-08-17 11:28 — KEYSTONE: the bracket is ONE Beta-weighted integral (D enters only as a weight)

**What was found.** Three exact algebraic steps collapse the knife problem
from a four-dimensional region (j, n, lam, D) onto one univariate polynomial.

1. M1_t = (1-j)_t/(1-n)_t is a POLYNOMIAL in t:
   M1_t = (j-1)!/(n-1)! * Qt,  Qt = product over i=j..n-1 of (i - t).
   So the truncation of the sum at t = j-1 is not an extra condition: Qt
   vanishes at t = j..n-1, and the squared kernel has degree
   2*floor((n-1)/2) <= n-1, hence every surviving power is below j.
2. M2_t = (1-R)_t / ((3/2-n)_t s^{2t}) is a STIELTJES MOMENT SEQUENCE with
   an explicit Beta density (alpha = R-1 > beta = n-3/2 > 0 throughout the
   canyon; the moments exist for every t <= j-1 because j <= n).
3. Therefore

       sign P_j(n, lam, D) = sign I(Q),
       I(Q) = integral over u in (0,1) of Hhat(u) u^p (1-u)^Q du,
       Hhat(u) = sum_t (-1)^t E_2t(n) Qt s^{-2t} u^{j-1-t},
       p = n - j - 1/2,      Q = D/2 + n - j - 2.

   **Hhat is D-FREE.** The dimension only slides the exponent of (1-u): it
   moves where the positive weight sits, nothing else. Large D pushes the
   weight to u -> 0, where the sign is that of the lowest coefficient;
   small D spreads it over the whole interval. That is the mechanism of the
   kill windows, stated with no asymptotics at all — no saddle points and
   no Stokes topology, which removes the previously open item.

**Verification (exact, no floating point).** results/keystone_beta.json:
6720 exact rational checks over j = 2..21, many n and lam, and D on both
sides of the shore. Zero mismatches, both for the algebraic identity and
for sign agreement with the master formula. Every Beta ratio is rational,
so after clearing one positive denominator the integral becomes a
polynomial J(Q) of degree j-1 with rational coefficients in (n, lam);
that form was cross-checked against direct evaluation as well.

**The theorem now reads as one inequality.** results/keystone_shore.json:
5616 cells (j = 2..40, twelve values of lam, n up to j+24), exact rational
bisection for the D-threshold. Result: ZERO cells where the threshold falls
strictly below the shore. In exactly three cells (j=2 with (n,lam) =
(4,1), (6,3), (12,7)) the threshold sits EXACTLY on the shore — the
tangency already known from the first knife theorem, now visible as
J(Q_shore) = 0 with a vanishing constant term.

**Negative #19 (recorded).** Manifest positivity in the depth below the
shore is FALSE: substituting Q = Q_shore - z, the z-coefficients of J are
not all nonnegative (first failures at j=3, a single negative coefficient
at z^1). Signature: results/keystone_manifest.json. Not fatal — below the
shore z is bounded by (T_hat-4)/2, so what is needed is positivity on a
segment, not on a ray.

**Inconclusive, not a negative.** The Gosper closed-summability test timed
out (background task, exit code 124). Tool limitation; no information
either way.

**The closing argument, now being computed.** Substituting v = -log(1-u)
turns the kernel into exp(-Q v), a Laplace kernel, which is strictly
totally positive. Karlin's variation-diminishing property then bounds the
number of sign changes of I(Q) in Q by the number of sign changes of Hhat
in u. If Hhat has exactly ONE sign change on (0,1), the positivity region
in D is a single interval, and the whole statement reduces to the single
inequality J(Q_shore) >= 0 that the 5616 cells already measure.
lab/keystone_sturm.py counts those sign changes exactly by Sturm chains in
rational arithmetic (running).

Status: NOT a proof yet. The reduction is exact and machine-checked, and
the remaining gap is explicit: (a) confirm the single sign change of Hhat,
(b) prove J(Q_shore) >= 0 as a function of (n, j, lam) rather than on a
grid.

## 2026-08-17 11:44 — KEYSTONE CERTIFICATE: J > 0 on the whole stretch below the shore

**Result.** results/keystone_cert.json: 5616 cells (j = 2..40, twelve values
of lam, n up to j+24), every single one CERTIFIED — and 5595 of them with no
bisection at all, meaning the certificate is manifest: after the map

        Q = Q_low + (Q_shore - Q_low) * w/(1+w),     w >= 0,
        Q_low = n - j (this is D = 4),  Q_shore = T_hat(lam)/2 + n - j - 2,

and clearing (1+w)^(j-1), EVERY coefficient of J is nonnegative and the
constant term is positive. No root for w >= 0, hence J > 0 on the entire
closed stretch below the shore. This is a Polya-type certificate: finite,
exact, rational, and free of any asymptotics — no saddle points, no Stokes
topology, no summation of divergent series.

What that means physically: for each of these cells the knife is PROVEN
never to cut anywhere below the shore, in one univariate argument that has
the same shape for every knife j. Twelve knives previously needed twelve
separate four-dimensional proofs.

**Negative #20 (recorded).** The total-positivity route to uniqueness of
the threshold is dead. results/keystone_descartes.json: after the Mobius
map u = w/(1+w) the D-free shape Hhat shows exactly j-1 sign changes for
every j tested (10620 cells, histogram is a clean diagonal), so all j-1
roots of Hhat lie inside (0,1). Karlin's variation-diminishing property
therefore bounds the number of D-thresholds by j-1, not by 1, and cannot
by itself prove a single positivity interval. The structural fact behind
the failure is itself worth keeping: Hhat is a hyperbolic polynomial with
ALL of its roots in the unit interval.

**Tool limitation (not a result).** The Sturm-chain implementation
(lab/keystone_sturm.py) blew up in rational arithmetic: 28 minutes, zero
output, killed. Descartes after a Mobius map answered the same question in
44 seconds. Kept in the tree as a recorded failure.

**What is still missing for the grand theorem.** The certificate is per
cell, and (n, lam) range over infinitely many values, j over all knives.
Two honest gaps remain:
  (a) lam is a continuum — the twelve knife theorems solved exactly this by
      carrying lam SYMBOLICALLY through the same certificate; the next step
      is to do that here, where the polynomial is univariate instead of
      four-dimensional;
  (b) n and j are unbounded — the coefficients of J are explicit finite
      sums in E_2t(n), Q(t) and binomials, so the target is nonnegativity
      of those coefficients as functions of (n, j, lam).

Status: NOT the grand theorem yet. It is a complete reduction plus a
uniform certificate architecture, with the two remaining gaps named
precisely. Artifacts: keystone_beta.json (6720 exact checks),
keystone_shore.json (5616 cells), keystone_cert.json (5616 certified),
keystone_descartes.json (10620 cells), keystone_manifest.json (negative).
All five regenerated from a clean tree (dirty = false), commit f0d8d86.

**Visual.** article/visuals/sliding-spotlight.png — the mechanism on exact
data for the tightest measured case (knife j=4, level n=14, lam = 7): the
shape is fixed, the dimension only slides the spotlight, and the verdict
flips at D = 139.7 while the shore sits at D = 131.1.

## 2026-08-17 13:33 -- Symbolic lam closed for j>=3; low spin dominance FAILS here; ERR-0003

**Step 1 of the keystone plan is done for j >= 3.** lam is now carried
SYMBOLICALLY through the interval certificate, so each cell covers a whole
continuum of lam rather than a point. Construction: on shore branch k, both
ranges are mapped to the closed first orthant by lam = (a+bv)/(1+v) and
Q = Q_low + Delta(lam) w/(1+w), with UNIFORM clearing -- every term carries
exactly (1+v)^(2(j-1)) and (1+w)^(j-1), the discipline the far-below port
taught us. Result (results/keystone_symbolic.json): every cell certified
for j >= 3, zero failures, all at bisection depth 0.

**j = 2 is excluded on purpose, with a reason.** At j = 2 the fleet is
EXACTLY tangent to the shore, so J acquires a double root and a
nonnegative-coefficient certificate cannot exist there: a polynomial that
is nonnegative on a ray need not have nonnegative coefficients, e.g.
(v-1)^2. Measured: 22 failing cells, all with j = 2, none with j >= 3.
j = 2 is already proven separately (the first knife theorem, which needed
sqrt-3 arithmetic precisely because of this tangency).

**Prior art checked in FULL TEXT, not from abstracts.** Bo Wang,
Positivity of the Hypergeometric Coon Amplitude (arXiv:2403.00906, JHEP),
proves manifest positivity using HARMONIC NUMBERS as a basis plus contour
integrals and stationary-point estimates, coefficient by coefficient, for
d = 4 and d = 6 (his eqs. 4.5-4.12). He states plainly that a statement of
manifest unitarity below the critical dimension of the (super)string was
still missing. Our route is different and complementary: a rational
Beta/moment reduction plus a machine-checked Polya certificate uniform in
j. Also relevant: On unitarity of the hypergeometric amplitude
(arXiv:2409.09561, JHEP 02 (2025) 145), partial coverage of the parameter
space.

**NEW FINDING -- low spin dominance does NOT hold for the CHR family.**
Wang hypothesises partial-wave low spin dominance: that unitarity bounds
are controlled by the low-spin coefficients (numerical support at m^2 = 0,
his fig. 1). We tested the analogous statement here, exactly:
results/keystone_lowspin.json. Over 36 (j, lam) cells, the level n that
minimises the D-threshold NEVER sits at spin l <= 2, not once. The
minimisers sit at spins 10 to 86. The tightest cell in the sweep is

        j = 4, lam = 26, n = 44  ->  spin l = 80,
        threshold D* = 494.84  vs shore = 489.93,  ratio 1.0100 ,

so the knives come within ONE PERCENT of the shore, and they do it at high
spin. Artifact check performed: the minimiser is interior and stable when
the n-window is widened from 20 to 45, 90 and 150 (n* stays put), so this
is not a truncation artifact -- the same check that killed two earlier
candidate findings today.

**METHODOLOGICAL DEFECT, now repaired.** Our own earlier counterexample
hunt (lab/keystone_hunt.py) swept only spins l in 0, 2, 4, 6 -- it
implicitly assumed low spin dominance, and was therefore blind exactly
where the margin is 1 percent. Repaired by lab/keystone_hunt_highspin.py,
which hunts at high spin with the corrected shore and a boundary-hugging
D-ladder approaching to 1 part in 10^6: 227,040 exact rational checks by
the ORIGINAL master formula, so a bug in the Beta reduction cannot hide a
violation. ZERO violations. results/keystone_hunt_highspin.json.

**ERR-0003 filed (docs/ERRATA.md).** The shore itself was computed with a
hard-coded cap k <= 60, which overestimates it for large lam (1.47x at
lam = 150, 5.96x at lam = 1000) because the minimising k grows like
sqrt(3)*lam. Found by chasing an apparent counterexample at j = 4, n = 94,
lam = 150 where both the master formula and the reduction agreed P_j < 0 at
D = 0.85 of the shore; with the CORRECT shore that point is above the
shore, so there is no counterexample -- the shore was the bug. Published
work is not affected (release scripts scan wide ranges and the papers
define the shore with no cap); the regression was in new code only, and the
older release code was already more careful. All keystone artifacts
regenerated with the fix, and the certificate came out cleaner than before.

Status after this block: step 1 (symbolic lam) DONE for j >= 3; step 2
(unbounded n and j) still open -- that remains the only creative gap.
Commit 301505c.

## 2026-08-17 13:37 -- Step 2 groundwork: an exact induction in the level n

The obstacle for step 2 is structural, not technical: the kernel

    F_n(y) = sum_t (-1)^t E_2t(n) y^t = [ prod_{a in S_n} (1 - a^2 y) ]^2,
    S_n = { n - 2k > 0 },

has a NUMBER OF FACTORS growing with n, so unlike lam it cannot be carried
symbolically. Two exact facts replace that (results/keystone_induction.json,
57 + 72 checks in rational arithmetic, zero failures):

**Fact 1, kernel recursion.** S_{n+2} = S_n union {n}, hence

    F_{n+2}(y) = F_n(y) * (1 - n^2 y)^2 .

Every level adds exactly ONE DOUBLE root, at y = 1/n^2, and it enters at
the OUTER edge of the root set. That is the same double-root structure that
made the square identity work, now appearing as a ladder in n.

**Fact 2, operator induction step.** With theta = y d/dy the bracket is
H_n = Q_n(theta) F_n, Q_n(t) = prod_{i=j}^{n-1}(i-t), and Q_{n+2}(t) =
Q_n(t)(n-t)(n+1-t). Commuting the operator past the new factor with the
Weyl relation p(theta) y^m f = y^m p(theta+m) f gives the closed step

    H_{n+2} = (n-theta)(n+1-theta) [ Q_n(theta) F_n
              - 2n^2 y Q_n(theta+1) F_n + n^4 y^2 Q_n(theta+2) F_n ] .

**Honest limitation, stated before anyone asks.** The step is exact but NOT
sign-preserving on its face. The prefactor (n-t)(n+1-t) is positive on the
surviving range (t <= j-1 < n), but the bracket carries -2n^2 and +n^4 with
shifted operators, so positivity of H_n does not propagate for free. What
the step gives is a CLOSED three-term system in the shifted family
Q_n(theta + sigma) F_n for sigma = 0, 1, 2 -- the right object to attack,
and the next thing I attack.

Also in this block: the symbolic-lam certificate (step 1) has now been
pushed to j = 19 -- 7310 cells, zero failures, every one at bisection depth
zero.

## 2026-08-17 13:43 -- Step 1 CLOSED for j=3..20; the road into step 2 is open

**Step 1 finished.** results/keystone_symbolic.json: 7740 cells, ALL
certified, zero failures, every one at bisection depth zero. Each cell
covers a whole continuum of lam (a shore branch), not a sample point, for
j = 3..20 and n up to j+20. j = 2 stays excluded with the stated reason
(exact tangency; already proven separately with sqrt-3 arithmetic).

**Where the danger actually lives -- a clean structural picture.** In the
FIXED-SPIN regime (l = 2n - 2j held fixed, n growing) there is no
D-threshold at all: positivity survives up to 40x the shore for every spin
and level tested, at the dangerous seam lam = 26. The reason is visible in
the algebra: at fixed spin the operator weight Q_n(t) has exactly l/2
factors -- a FIXED number -- and every factor is positive on the summation
range, the smallest being n-1-(l/2-1)-(j-1) = 1.

So the risk is not at low spin, and not at fixed spin. It sits at SMALL j
with LARGE n, where the spin grows -- exactly the corner the tightest cell
lives in (j = 4, lam = 26, n = 44, spin 80, margin one percent). This
retro-explains why the old low-spin hunt found nothing: there was nothing
there to find.

**Negative #21 (recorded).** The cheap route to large n is dead: the t = 0
term does NOT dominate the tail. At lam = 26 with D just below the shore,
|tail|/head is 2.7 at j = 3, 6.7 at j = 4, 28 at j = 6, and 417 at j = 10.
Positivity here is produced by CANCELLATION inside the alternating tail, not
by majorisation -- consistent with everything else in this problem, and it
means step 2 needs a certificate, not an estimate.

**And the certificate route into step 2 is open (two exact facts).**
results/keystone_npoly.json:

  FACT A. For fixed t and fixed parity of n, E_2t(n) is a POLYNOMIAL in n.
  E_2t is the t-th elementary symmetric function of the squares of an
  arithmetic ladder, so at fixed t it is a fixed-length combination of power
  sums. Verified in 16 cases by fitting on the first points and PREDICTING
  the held-out ones -- never by fitting all of them.

  FACT B. Q_n(t)/Q_n(0) = prod_{i=1..t} (j-i)/(n-i). The factorial growth of
  the weight is an overall POSITIVE constant that divides out of any sign
  question; the t-dependence is rational in n of degree t. 900 checks, zero
  failures.

Together: at fixed j and fixed parity, the whole bracket is a polynomial in
(n, lam, D) after uniform clearing. So n can be carried SYMBOLICALLY exactly
like lam, and the Polya certificate can in principle cover ALL n at once --
which would leave j as the single remaining unbounded index.

Next: build that three-variable certificate in (w, v, n), carrying the
uniform-clearing discipline into three variables. If the clearing is not
uniform the far-below sign bug comes straight back, so the validation
contract goes in first.

## 2026-08-17 13:52 -- STEP 2 (level n) CLOSED; the last infinity is j, and it splits by parity

**Step 2 done for j = 3..8 (extending).** results/keystone_symbolic_n.json:
216 of 216 cells certified, branches k = 3..20, both parities. A cell now
means: ALL levels n of that parity (infinitely many), the WHOLE continuum of
lam on that branch, and EVERY D from 4 up to the shore. Three of the four
parameters are now carried symbolically.

Construction: n = n0 + 2 mu with mu >= 0, on top of the step-1 maps for lam
and D. Facts A and B (keystone_npoly.json) are what make it legal. Uniform
clearing spelled out in the module docstring, and the VALIDATION CONTRACT
runs before any verdict: the sign of the three-variable polynomial must
match the exact rational bracket at interior points. It does.

**Structure of the certificate: TAIL + BASE.** Manifest positivity cannot
start at the first level, because the D-threshold has an INTERIOR minimum in
n, so positivity in n is not monotone. So for each (j, parity, branch) we
find the smallest shift M with a manifestly positive tail n >= n0 + 2M (one
certificate, infinitely many levels), and the finitely many levels below it
form the base, already certified cell by cell by step 1. Measured shifts are
small, M = 0..4. The join condition (every base level must lie inside step
1's coverage, n <= j+20) is CHECKED, not assumed: a cell that fails it is
reported as a failure.

**The last infinity is j, and the data splits it cleanly by PARITY.**
Minimum of D-threshold/shore over n and lam, per knife:

    j = 3, 5, 7, ..., 25 (ODD):  no threshold anywhere in the sweep
                                 -- positive for every D tested
    j = 4  -> 1.010030   (n = 44, lam = 26)
    j = 6  -> 1.020237     j = 8  -> 1.030848
    j = 10 -> 1.042520     j = 12 -> 1.057350
    j = 14 -> 1.079265     j = 16 -> 1.107950
    j = 18 -> 1.140049     j = 20 -> 1.159676
    j = 22 -> 1.209487     j = 24 -> 1.227631

Two structural statements come out of this. First, ODD knives never cut at
all: at large D the sign is that of the leading term, which carries
(-1)^(j-1) = +1 for odd j, so no threshold can exist. Second, for EVEN
knives the margin is MONOTONE INCREASING in j over the whole tested range,
so the danger lives at SMALL EVEN j -- the tightest cell in the entire
project is j = 4, lam = 26, n = 44, spin 80, margin one percent. Every
dangerous cell sits at lam = 26, the seam of branch k = 45.

**Negative #22 (recorded).** Positivity of odd knives is NOT manifest on the
ray: substituting Q = Q_low + z, the z-coefficients of J are not all
nonnegative in any of 140 cells tested, for j = 3..15. So even where no
threshold exists, positivity comes from cancellation rather than from
term-by-term dominance -- the same lesson as negatives #19 and #21. Harmless
for the programme, because the working certificate lives on the SEGMENT
[Q_low, Q_shore], not on the ray.

**Honest status of the grand theorem now.**
  lam  -- closed symbolically, branches k <= 45, i.e. lam up to about 26.1
  D    -- closed on the whole stretch below the shore
  n    -- closed symbolically (tail + base)
  j    -- closed only FINITELY (certificates through j = 8, extending; the
          twelve earlier knife theorems reach j = 13). For unbounded j what
          exists is a strong, exactly measured REGULARITY (odd knives never
          cut; even-knife margin monotone in j), not a proof.
Still outside coverage and named: lam above the last branch, which needs a
tail argument as in the knife theorems.

## 2026-08-17 14:10 -- THE MARGIN LAW: how close the knives get, and why they never arrive

**A proved fact first (elementary, and it explains the parity split).** The
leading coefficient of J in Q comes ONLY from t = j-1, and equals
(-1)^(j-1) E_{2(j-1)}(n) Q_n(j-1) times a strictly positive product. So

        sign(leading coefficient) = (-1)^(j-1) ,

which means ODD knives run to +infinity as D grows and cannot develop a
threshold at all, while EVEN knives run to -infinity and MUST develop one.
324 checks, zero mismatches (results/keystone_margin_law.json). That is why
every dangerous cell in this entire project has even j -- it was never an
accident of sampling.

**Where the tightest knife sits.** For lam >~ 14 the most dangerous level is

        n* = k(lam) - 1 ,

i.e. the tightest knife sits essentially ON the trajectory that defines the
shore (the shore is min over trajectories k; the knife that comes closest is
the one on that same k). Measured across lam = 5..40: n* - k = +1, +1, 0,
-1, -1, -1, -1, -1.

**The margin law (measured).** For even j, at large lam,

        D*(j, lam) - T_hat(lam)  ->  C (j - 2),    C = 2.398 +- 0.002,

measured over j = 4, 6, 8, 10 and lam = 100, 175, 250, 500 -- twelve cells,
all within 0.2 percent of each other. The closed-form guess C = 12/5 = 2.4
sits inside the residual drift of the shore asymptotics itself, so I record
2.398 +- 0.002 and do NOT claim 12/5. In ratio form the same law reads

        D*/T_hat - 1  ~  (j - 2) c0 / (2 lam),   c0 = 0.2534 ,

and the shore itself grows linearly, T_hat(lam) -> (12 + 4 sqrt 3) lam =
18.928203 lam (measured 18.925746 at lam = 1000; the sqrt 3 is the same one
that appears in the tangency of the first knife theorem).

**What it means physically.** The knives approach the shore like 1/lam in
relative terms, but the ABSOLUTE gap does not vanish -- it saturates at
about 2.4 (j - 2) dimensions. So the fleet never reaches the shore at finite
lam, and the closer one looks (larger lam), the thinner the relative margin
becomes. This is the quantitative version of the tangency-at-infinity that
the first knife theorem found geometrically, and it explains cleanly why lam
above the last certified branch is the hard region: that is exactly where the
relative margin is smallest, not where the mathematics changes.

**Status and falsifier.** The leading-coefficient fact is PROVED. The margin
law is a measured REGULARITY, not a theorem, and the constant is not
identified in closed form. Explicit falsifier recorded in the artifact: any
cell with D* - T_hat < 2.39 (j-2) - 0.05 at lam >= 100 refutes it.

Also in this block: the symbolic-n certificate (step 2) has reached j = 13 --
396 cells, zero failures.

## 2026-08-17 14:12 -- Negative #23: the margin law does NOT come from the first two terms

Attempt: derive the constant C = 2.398 analytically. Scale analysis
suggested that at large lam the expansion parameter is small, so the
threshold should be fixed by the balance of the t = 0 and t = 1 terms alone.
Solving term0 + term1 = 0 for D and comparing with the exact threshold:

    j = 4, lam = 100:  exact D* - shore = +4.797,  two-term = -1708.94
    j = 4, lam = 250:  exact D* - shore = +4.796,  two-term = -4295.07
    j = 6, 8:          the two-term equation has no root in the bracket

Off by a factor of -356 and -896, and structurally absent for j >= 6. Dead.

Why my scale analysis was wrong, recorded so I do not repeat it: I estimated
E_2t(n) as (n^2)^t times a mild factor, but E_2t carries a binomial
C(K, t) with K ~ n/2 ~ sqrt(3) lam / 2, which is LARGE. The true expansion
parameter is therefore O(1), not O(j/lam), and every term in the sum
contributes comparably. Same lesson as negatives #19 and #21: in this
problem positivity and thresholds alike are produced by cancellation across
the whole alternating sum, never by a few leading terms.

Consequence for the programme: the constant in the margin law cannot be
extracted cheaply. Getting it needs the asymptotics of the FULL terminating
sum -- which is the saddle/Abel-Plana route where the Stokes topology was
the obstacle. The margin law therefore stays exactly where it was recorded:
a measured regularity with an explicit falsifier, not a theorem, and the
closed form 12/5 stays a guess.

## 2026-08-17 14:19 -- A TOOL DEFECT found and fixed; negative #24

**Negative #24: the margin is NOT monotone in j pointwise.** I hoped that at
fixed (n, lam) the margin grows with j, which would reduce the whole theorem
to the first few knives. It does not: 4 violations out of 12 tested (n, lam)
pairs. The monotonicity that IS real is only of the MINIMUM over (n, lam),
not of the value at a fixed cell. So the reduction to small j does not follow
this way.

**And chasing those violations exposed a defect in my own instrument.**
threshold_D bisected [4, 40*shore] directly, which is valid only if J has a
SINGLE sign change there. Fine-grid counting shows J can have 5 or even 9
sign changes on that stretch: at (j=6, n=44, lam=7) the first flip is at 1.18
of the shore, while bisection reported 1.69. Any number produced for such a
cell was simply wrong -- including some of the "violations" of monotonicity I
had just recorded.

Fixed: a coarse scan now locates the FIRST sign change and bisection refines
only inside that bracket. The docstring records what went wrong.

**Both earlier conclusions RE-CHECKED after the fix, and both survive.**
  * The margin law is unchanged: gap/(j-2) = 2.3971 .. 2.4015 over j = 4, 6,
    8, 10 and lam = 100, 250 -- identical to before, because in the
    dangerous cells (n near k) J has exactly ONE sign change, where the old
    bisection was already correct.
  * Low spin dominance still fails: over 46 (j, lam) cells the minimising
    spin is never l <= 2; the minimisers run from l = 8 to l = 90.

Why this matters beyond the numbers: the defect only bit in cells where the
polynomial oscillates several times, and those were never the tight cells.
But it could have bitten the headline result, and it was found only because
a monotonicity check produced values that looked implausible. Recording the
pattern: when a measured quantity jumps around (1.23, 1.69, 1.51, 1.24,
2.05), suspect the measuring tool before believing the pattern.

## 2026-08-17 14:29 -- 360-analysis: the knife problem IS a Schoenberg problem

Stepping back from the machinery to look sideways, the question we have been
grinding on is a classical one in a different field. "Are all partial-wave
coefficients of the residue nonnegative in D dimensions?" is verbatim
Schoenberg's 1942 characterisation: an isotropic function on the sphere
S^(d-1) is POSITIVE DEFINITE iff its Gegenbauer expansion has nonnegative
coefficients (the d-dimensional Schoenberg coefficients). Our partial waves
ARE those coefficients and our D is the sphere dimension.

Two things follow, one conceptual and one practical.

Conceptually, it explains why a shore must exist at all: the class of
positive definite functions on S^(d-1) SHRINKS as d grows, so for a fixed
residue there is a largest dimension where positivity survives. The shore is
that critical dimension, and its existence needs no amplitude physics.

Practically, it points at an existing toolkit we were not using: DIMENSION
WALKS -- montee/descente operators relating Gegenbauer coefficients in
dimension d and d+2 (Gneiting, arXiv:1303.6856; strictly-PD refinements in
J. Approx. Theory 2017). Monotonicity classes of the coefficient sequence
there guarantee positive definiteness in higher dimensions. If our
coefficient family lands in such a class, the D-dependence might be
available wholesale AND uniformly in j -- which is exactly the single gap
left in the keystone.

Written up with a deterministic first test in research/schoenberg-direction.md:
check exactly whether the descente operator maps our coefficient sequence at
D to the one we compute directly at D+2. If it does, we inherit the toolkit;
if not, it is a negative with a signature and gets dropped. Status: a
DIRECTION with a falsifier, not evidence for anything.

Also in this block: the foreign-engine judge (Z3) is running on the tightest
zone of the whole project -- branch k = 44..46 (lam about 26), levels 38..52,
even knives, where the margin is one percent and where our own earlier tools
were weakest. So far j = 4 and j = 6 are fully unsat (135 continuous cells,
zero alarms, zero unknowns).

## 2026-08-17 14:31 -- Negative #25: the naive dimension-walk test, and what the real one needs

First attempt at the Schoenberg direction. Reasoning: with mu = alpha + 1 the
Gegenbauer connection coefficient (alpha - mu)_k = (-1)_k vanishes for k >= 2,
so the relation between dimensions D and D+2 must be TWO-TERM. I tested

        P_j(D) = A P_j(D+2) + B P_{j+1}(D+2)

with A, B fixed per (n, j, lam): solve from two values of D, predict a third.
It fails in all 18 cells, with enormous residuals.

The test was badly posed and I should have seen it before running: in the
connection formula the coefficients depend on the Gegenbauer index alpha =
(D-3)/2, hence on D itself. So D-independent A, B were never going to work,
and conversely a version with free D-dependent coefficients is vacuous -- one
equation, two unknowns, always solvable.

What the real test needs, written down so the next attempt is not blind:
  1. the explicit connection coefficients c_0(l, alpha), c_1(l, alpha) from
     C_l^(alpha) = c_0 C_l^(alpha+1) + c_1 C_{l-2}^(alpha+1);
  2. our normalisation of the partial waves relative to the standard
     Gegenbauer basis -- P_j is the master-formula bracket, not a bare
     Schoenberg coefficient, and the normalisation is D-dependent;
  3. then the relation b_m^(alpha+1) = c_0(m) b_m^(alpha) + c_1(m+2)
     b_{m+2}^(alpha) becomes a PREDICTION with no free parameters, and it
     either holds exactly in rational arithmetic or it does not.

Note the direction of the walk: it expresses the coefficients at D+2 through
those at D, i.e. it moves toward HIGHER dimension, which is the direction in
which positivity is LOST. If the relation holds with signs of a definite
pattern, it would give exactly the kind of statement we want -- positivity at
D controlling positivity at D+2 -- uniformly in j.

Status: the direction survives (it was never tested here), the naive
shortcut is dead, and the honest next step is spelled out above.
