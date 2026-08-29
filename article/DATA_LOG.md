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

## 2026-08-17 14:34 -- THE DESCENT LEMMA: the theorem collapses to a strip of width 2

This is the result of the shift. It is PROVED, not measured, and it is
uniform in the spin -- the thing every earlier route failed at.

**Statement.** If all partial waves of a level are nonnegative in dimension
D + 2, then all of them are nonnegative in dimension D.

**Proof, in full.** Partial waves are the coefficients b_l^(a) of the residue
in the Gegenbauer basis C_l^(a), a = (D-3)/2 (for a > 0 the physical
D-dimensional Gegenbauer is a positive multiple of C_l^(a), the convention
already used in paper 2 and in lab/attack_gravity.py). The classical
connection formula with mu = a+1 has coefficient (a - mu)_k = (-1)_k, which
VANISHES for k >= 2, so it truncates after two terms:

    C_l^(a) = c0(l,a) C_l^(a+1) + c1(l,a) C_{l-2}^(a+1),
    c0(l,a) = (a)_l (l+mu) / ((mu+1)_l mu),
    c1(l,a) = -(a)_{l-1} (l-2+mu) / ((mu+1)_{l-1} mu),  l >= 2.

Expanding one and the same residue in both bases gives the DIMENSION WALK

    b_m^(a+1) = c0(m,a) b_m^(a) + c1(m+2,a) b_{m+2}^(a).            (*)

For a > 0 every Pochhammer is positive, hence c0 > 0 and c1 < 0. Inverting
(*) downward in the spin,

    b_m^(a) = [ b_m^(a+1) + |c1(m+2,a)| b_{m+2}^(a) ] / c0(m,a),

which is a POSITIVE combination. Induction from the top spin downward gives
the lemma. QED.

**Verification.** results/keystone_dimension_walk.json: the forward relation
holds exactly in 120 of 120 cells, the inverse reconstruction reproduces our
independently computed partial waves exactly in 120 of 120, and the sign
statement (c0 > 0, c1 < 0) holds in every case. Exact rational arithmetic,
checked against our own partial-wave solver, which knows nothing about the
connection formula.

**Consequence -- this is the big one.** For any D in [4, T_hat] set
k = floor((T_hat - D)/2). Then D + 2k lies in (T_hat - 2, T_hat], and k
applications of the lemma carry positivity down to D. So the grand theorem
reduces from a region of width about 19 lam to

        A STRIP OF WIDTH 2 JUST BELOW THE SHORE.

Everything below the strip is free, for every knife at once. No certificate,
no cell-by-cell work, no bisection.

**Why it also explains the physics.** Schoenberg (1942): positive
definiteness on a sphere is equivalent to nonnegative Gegenbauer
coefficients, and the class of such functions SHRINKS as the dimension grows.
Relation (*) is the explicit shrinking map for our family, and the shore is
the critical dimension of that nesting. The existence of a shore needs no
amplitude physics at all -- it is sphere geometry.

**What is still open, stated plainly.** Positivity INSIDE the strip
(T_hat - 2, T_hat], for all spins. That is now the entire remaining task. It
is also exactly where the margin law says the action is: the tightest knives
sit within one percent of the shore, riding the very trajectory that defines
it.

Note also that this reframes the earlier work rather than discarding it: the
Beta reduction, the symbolic-lam certificate and the symbolic-n tail+base
certificate all still apply, and they now only ever need to be run inside a
width-2 strip instead of the whole stretch.

## 2026-08-17 14:49 -- Negative #26, and the shore inequality holds everywhere tested

Tried to shrink the strip to a single point: if J were monotone decreasing
across the strip, then positivity on the whole strip would follow from the
one inequality J(Q_shore) >= 0, and the theorem would reduce to the shore
itself.

  * J(Q_shore) >= 0 in ALL 840 cells tested (j = 2..21, many n, six lam) --
    the shore inequality itself never fails.
  * Monotonicity FAILS: in 156 of 840 cells the derivative changes sign
    somewhere inside the strip. Negative #26.

So the reduction to a single point does not go through. It is not needed:
the Polya certificate on the strip is MANIFEST anyway (depth zero on the
grid, and the symbolic-in-lam-and-n version is closing branch after branch,
through j = 10 as of this entry). Monotonicity would have been a shortcut,
not a requirement.

Worth keeping from this: the shore inequality J(Q_shore) >= 0 is now measured
across a wide grid with zero failures, and it is exactly the statement that
the fleet touches but never crosses -- the same tangency the first knife
theorem proved geometrically for j = 2.

## 2026-08-17 15:15 -- Negative #27: no local grouping proves the strip certificate

Step 2, attempt A. On the strip every coefficient of the certificate is
STRICTLY positive -- not one of them is even zero (135 coefficients at j = 3,
364 at j = 4, 765 at j = 5, all positive, both parities, several branches).
That raised the hope that positivity is LOCAL: if each adjacent pair of
summands were nonnegative by itself, the certificate would hold for every j at
once, with no induction and no cell-by-cell work.

Tested and dead:
  * pairs (0,1), (2,3), (4,5), ...: the FIRST pair always fails, later pairs
    pass -- so grouping from the bottom does not work;
  * shifted grouping, t = 0 alone then (1,2), (3,4), ...: t = 0 alone is
    nonnegative, but NO pair passes;
  * partial sums: from the top they only turn nonnegative near the middle
    (t = 2 at j = 4, t = 4 at j = 5 and 6).

Conclusion: the cancellation that makes the strip certificate work is GLOBAL
across the alternating sum, not pairwise and not tail-local. This is now the
fourth time this problem has said the same thing (negatives #19, #21, #23,
#27): positivity here never decomposes into positive pieces. Any proof
uniform in j has to respect that, which rules out the whole family of
"group the terms cleverly" arguments.

What survives from the attempt, and it is worth keeping: the strip
coefficients are strictly positive with no zeros at all, which means the
certificate has margin everywhere rather than sitting on a boundary. The
remaining routes for j are the two structural ones -- induction using
Q_{j+1}(t) = Q_j(t)/(j-t), and the dimension-walk apparatus that gave today's
descent lemma, which is the only tool so far that acted uniformly in the spin.

Meanwhile the strip certificate itself keeps closing: j = 13 done, 946 cells,
zero failures.

## 2026-08-17 15:40 -- PRIOR ART CORRECTION: the descent lemma is CLASSICAL, not ours

Searched the literature on the founder's instruction to look around. Result:
the lemma I proved and called "the result of the shift" is a known theorem.

**What the literature says.** Matheron (1965) introduced the operators MONTEE
and DESCENTE, which move positive definite functions between dimensions; the
sphere versions are standard, and the direction is stated plainly: the montee
operator "maps (strictly) positive definite functions for S^{d+2} to (strictly)
positive definite functions for S^d", and walks go in steps of +-2, exactly as
our relation does. References: "Dimension walks on hyperspheres", Comput. Appl.
Math. 41 (2022), doi:10.1007/s40314-022-01912-4; Gneiting, "From Fourier to
Gegenbauer: Dimension walks on spheres", arXiv:1303.6856; "Dimension hopping
and families of strictly positive definite zonal basis functions on spheres",
J. Approx. Theory (2017), doi:10.1016/j.jat.2017.03.002.

**So the status changes.** What I derived this afternoon is a rediscovery. I
found it independently, from the Gegenbauer connection formula, and verified it
exactly -- but the priority is not ours and the statement must never be
presented as new. Corrected in DATA_LOG, HANDOFF, research/keystone-plan.md
and article/SHIFT_REPORT_2026-08-17.md.

**What remains genuinely ours, as far as this search shows.**
  1. The explicit two-term form for the CHR graviton family, with the signs
     c0 > 0, c1 < 0 verified exactly (120+120 cells), which is what makes the
     induction constructive in our concrete setting.
  2. The APPLICATION: reducing the critical-dimension question for scattering
     amplitudes to a strip of width 2. Searches for "dimension walk" or
     "montee" together with partial-wave unitarity, S-matrix bootstrap or
     amplitude positivity returned NOTHING -- the amplitude literature does
     not appear to use this apparatus at all. Cross-searches for Schoenberg
     positive-definiteness applied to string partial waves likewise returned
     nothing.
  3. The identification of the shore as the critical dimension of Schoenberg's
     nesting, which explains why a shore must exist without any string physics.

If that holds up under closer reading, the contribution is a TRANSFER of a
classical tool from approximation theory and geostatistics into the amplitude
bootstrap -- which is a perfectly respectable contribution, but a different
claim from "we proved a new lemma", and it must be written that way.

**New tool spotted for the open problem.** "A Polya criterion for (strict)
positive definiteness on the sphere" (arXiv:1110.2437) gives Polya-type
sufficient conditions directly on the sphere. Our remaining task is exactly a
positivity statement on the strip, and our certificate is already Polya-type,
so this is the first thing to read next shift.

**Lesson recorded.** I should have run this search BEFORE calling the lemma the
result of the day -- the 360 rule exists precisely for this, and I applied it
to the Schoenberg framing but not to the lemma itself. Cost: nothing published,
because the check happened the same day. Rule for next time: any statement I am
about to call a result gets a prior-art search in the same hour, not the next
morning.

## 2026-08-17 15:58 -- Polya-on-the-sphere does not apply (negative #28), but the sign
## pattern of the residue explains why a shore exists at all

Read Beatson, zu Castell, Xu, "A Polya criterion for (strict) positive
definiteness on the sphere", arXiv:1110.2437, in full text (pages 1-5).

**Negative #28.** Their Polya-type criterion (their Thm 1.3) requires
supp(g) contained in [0, pi) -- the function must VANISH near theta = pi -- plus
convexity of a signed derivative. Our residue is a polynomial that vanishes
nowhere on the interval, so the criterion does not apply, and no amount of
rescaling fixes a support condition. Dead end, recorded.

**But their Thm 1.2 (Schoenberg) is directly useful.** f(cos.) is positive
definite on ALL spheres iff its expansion in POWERS of cos(theta) has
nonnegative coefficients. Since our shore exists -- positivity fails above some
dimension -- some coefficient of the residue in powers of cos(theta) must be
negative. Measured, and the pattern is perfectly clean:

    n = 4 : 0 0 + 0 - 0 +
    n = 5 : + 0 - 0 + 0 - 0 +
    n = 6 : 0 0 + 0 - 0 + 0 - 0 +
    n = 7 : + 0 - 0 + 0 - 0 + 0 - 0 +
    n = 8 : 0 0 + 0 - 0 + 0 - 0 + 0 - 0 +

Only every second power appears, and the signs STRICTLY ALTERNATE. The pattern
is identical for lam = 1, 3 and 26 -- it does not depend on lam at all.

**Why, structurally.** Strict alternation of a polynomial in y = cos^2(theta)
means (Descartes) that all of its roots in y are real and positive. That is
exactly our square identity seen from the other side: the residue is
prod_a (1 - a^2 y)^2 up to a positive factor, so its roots in y are the
squared inverse spectral values, all real and positive.

So the chain is now complete as an explanation:
  * residue = a polynomial in cos^2 with all roots real and positive
    => its coefficients in powers of cos strictly alternate
    => by Schoenberg's Thm 1.2 it is NOT positive definite on all spheres
    => there is a largest dimension where positivity survives: THE SHORE.
The existence of the shore is therefore forced by the root structure of the
spectrum, with no input from string physics. The shore's VALUE still needs the
full computation -- this explains existence, not location.

Two useful pieces of prior art for the writeup, both now read rather than
skimmed: their eq. (2.1) is exactly the projection form b_n =
int f(x) C_n^lambda(x) w_lambda(x) dx that research/closing-the-last-infinity.md
proposes to use, so that plan is standard machinery rather than an invention;
and their Prop. 1.5 shows how hard sharp positivity statements get even for
d = 4, 6, 8 (they needed extensive computer algebra), which is a fair warning
about the difficulty of the remaining strip problem.

## 2026-08-17 16:57 -- Strip certificate on ALL branches, and a correction to my own claim

**Result.** With the fast engine (native flint mpoly) the strip certificate now
closes 774 of 774 cells: j = 2..10, BOTH parities, and ALL shore branches
k = 3..45, i.e. every lam up to about 26.1 -- in 15 seconds where the old engine
needed hours. A larger run (j to 30) is under way.

**Correction to something I said an hour ago.** When the fast engine first
reported failures on far branches, I concluded it was "a real limit of the
method" and wrote that down. That was WRONG, and the way I checked it was
faulty: I compared the fast and slow engines on the same call
(cert_ok(build_N(...))), they agreed, and I took the agreement as evidence
about the method. It was only evidence that both engines computed the same
polynomial -- which they did.

The actual cause was my own porting bug: the TAIL + BASE structure was lost in
the port. Manifest positivity does not hold from the lowest level (the
D-threshold has an interior minimum in n, recorded earlier today), so the run
must search for the smallest shift M giving a manifest tail and leave the
finitely many levels below as the base. The slow engine did that; the fast one
did not. Restored, and the failures vanished entirely.

**Lesson, recorded.** When a faster reimplementation disagrees with the older
run, the first hypothesis is a porting bug, not a discovery about the
mathematics -- and a cross-check must exercise the FULL pipeline, not the one
function I happen to suspect. I had the discipline right this morning for the
far-below port (where the validation contract caught a non-uniform clearing)
and dropped it here.

Net position on coverage after this block:
  * lam: all branches k <= 45 (lam up to ~26.1), symbolically, on the strip;
  * n: all levels, via tail + base with the join condition checked;
  * D: the whole stretch below the shore, by the classical descent lemma;
  * j: finite -- 2..10 confirmed, larger run in progress. Still the only gap,
    together with lam beyond the last branch.

## 2026-08-17 17:21 -- THE LADDER IN THE KNIFE INDEX (new, and it explains the parity)

After six failed attempts on the last gap I stopped trying new tricks and asked
what the failures had in common. All six tried to TAKE THE SUM APART -- pairs,
tails, thresholds, external criteria. All died. What had ever worked in this
programme was of one kind only: tools that keep the whole structure intact, an
integral representation with a positive measure (the Beta reduction) and an
operator identity (the dimension walk). So I looked for a third tool of that
kind rather than a seventh way to split the sum.

**Found, and verified exactly.** The operator weight satisfies
Q_{j+1}(t) = Q_j(t)/(j-t), and on the summation range j - t >= 1, so 1/(j-t) is
not merely positive -- it is a MOMENT:

        1/(j - t) = INT_0^1 u^{j-t-1} du .

Hence the step from knife j to knife j+1 is an INTEGRAL OPERATOR WITH A
POSITIVE KERNEL. And because the weights enter the Beta reduction as
A_t/s^{2t}, dividing by u^t is the same as replacing s^2 by s^2 u: the
averaging runs over SMALLER values of the deformation lam.

**The one subtlety, and it is the good part.** At t = j the relation is 0/0
(Q_j(j) = 0 while Q_{j+1}(j) = (n-1-j)! is not), so the step is not pure
averaging -- it leaves a BOUNDARY TERM:

    bracket_{j+1} = SUM_{t<j} (-1)^t E_2t Q_j(t)/(j-t) A_t/s^{2t}
                    + (-1)^j E_2j (n-1-j)! A_j/s^{2j} .

Verified in 228 exact rational checks, zero failures
(results/keystone_j_ladder.json).

**This EXPLAINS the parity split we measured this morning.** The boundary term
carries (-1)^j. Measured on the same grid: it enters with a PLUS whenever the
next knife j+1 is odd, and with a MINUS whenever j+1 is even -- both statements
hold in every row. So odd knives inherit positivity for free from the averaging
plus a helping boundary term, while even knives face a negative boundary term,
which is exactly where a threshold can appear. Earlier today we PROVED the
parity fact from the leading coefficient; now we also understand its mechanism,
and the two accounts agree.

**Status.** The identity is proved. What is not proved is the estimate for the
even case: that the averaged part dominates the negative boundary term. That is
now ONE explicit comparison of two written-out quantities, and it is needed only
for even j+1 -- half of the remaining problem, in a form that respects the
global cancellation instead of fighting it.

**Three ladders now, and they cover the three parameters:**
  * dimension D: classical montee/descente (Matheron) -- gives everything below
    the width-2 strip;
  * level n: F_{n+2} = F_n (1 - n^2 y)^2 -- one new double root per level;
  * knife index j: this one -- averaging with a positive kernel plus a boundary
    term whose sign alternates.
The first two are known mathematics applied to a new object; the third I have
not found in the literature, and it will get a prior-art search before it is
called new -- the lesson from this afternoon.

## 2026-08-17 17:25 -- The j-ladder inequality is TIGHT: it is the theorem, not a step

Measured the tightness of the inequality the j-ladder leaves open -- averaged
part > |boundary term| for even next knife -- at the dangerous places (D just
below the shore, n near k(lam)):

    j+1 = 4, n = 44, lam = 26:  ratio 1.2184 at D = 0.50 shore,
                                ratio 1.0001 at D = 0.99 shore
    j+1 = 6, n = 41, lam = 26:  1.1063  ->  1.0000
    j+1 = 8, n = 44, lam = 26:  1.0411  ->  1.0000

So the two quantities become EQUAL at the threshold, by construction: the
inequality "averaged > |boundary|" is not a weak link that a crude estimate
could finish -- it is logically equivalent to "we are below the threshold",
i.e. to the theorem itself.

**Correction to what I said an hour ago.** I called this "one explicit
comparison, half the problem". That was too optimistic and I should have
measured the margin BEFORE promising it. The ladder did not simplify the
problem; it EXPLAINED it. Those are different things, and the difference is
exactly what the founder was pushing me on -- do not report a reformulation as
progress toward a proof.

**What the ladder does leave, and it is real:**
  * the mechanism of the parity split -- why odd knives can never cut and even
    ones must -- now derived, and agreeing with the independently proved
    leading-coefficient fact;
  * the structure "positive-kernel averaging + boundary term", which is the
    third exact ladder of the programme;
  * a characterisation of the THRESHOLD as the locus where the averaged part
    exactly equals the boundary term. That is an equation for the threshold,
    not an estimate -- possibly more useful than the inequality, since the
    margin law says that locus sits 2.4(j-2) dimensions above the shore.

**Why I am not going to force this tonight.** Proving positivity below the
shore from this identity requires comparing two quantities to better than one
percent, uniformly. That is the same obstacle that killed the analytic
derivation of the constant 2.398 this morning: the asymptotics of the full
alternating sum. Two independent routes have now hit the identical wall, which
is information: the remaining gap is not a missing trick, it is a genuine
asymptotic estimate that this programme has not yet earned.

## 2026-08-17 17:59 -- THE ASYMPTOTIC ROUTE WORKS. This morning's failure was a bug.

Following the inventory (every unused asset sits in the contour/saddle line),
I went back to it. Result: the route works, and the catastrophic failure of the
morning -- a saddle sum off by 250 orders of magnitude -- was an implementation
bug, not the Stokes phenomenon.

**The key simplification I had missed.** The bracket is a COEFFICIENT OF A
PRODUCT OF TWO POLYNOMIALS:

    SUM_t (-1)^t E_2t(n) A_t = [x^{j-1}] G2(x) * Psi_rev(x) ,

so the saddle points solve a POLYNOMIAL equation, x P'(x) = (N+1) P(x) with
N = j-1, and are computable exactly. No transcendental root-finding, no
guessing which critical points exist.

**All saddles are active.** Summing over ALL of them and comparing with the
exact coefficient:

    leading order only:  1.4166 (j=6), 1.3046 (j=8), 1.2405 (j=10),
                         1.1976 (j=12), 1.1678 (j=14)   [ratio to exact]

The ratio decreases steadily toward 1. So there is no Stokes subtlety here to
resolve -- the whole set of critical points contributes, and what looked like a
topology problem was simply a missing correction term plus, this morning, a
plain coding error.

**With the standard 1/N correction the agreement becomes good and IMPROVES with
the knife index:**

    with correction:     0.8961 (j=6), 0.9545 (j=8), 0.9790 (j=10),
                         0.9829 (j=12), 0.9877 (j=14)

i.e. the error falls to about 1.2% at j = 14 and keeps falling. Two technical
notes: the derivatives must be taken ANALYTICALLY (finite differences on
high-degree polynomials blew up, giving 2640 at j=14 -- pure numerical noise),
and the outlier at j=16 (0.9038) is float-precision loss in the complex root
finding, to be redone in high precision.

**Why this matters for the theorem.** The remaining gap is uniformity in j. The
margin to beat is about one percent in the tightest cells. The asymptotic error
is already at that level by j = 14 and shrinking, so the natural structure of a
proof is now visible:

    small j  ->  machine certificates (done: j = 2..17 so far, all branches,
                 all levels, everything below the shore);
    large j  ->  saddle asymptotics with an explicit remainder bound.

What is NOT yet done, stated precisely: a RIGOROUS bound on the remainder. The
numbers above are measured agreement, not an estimate with proven error
control. That is the standard, laborious part of steepest descent (Watson-type
lemmas with explicit constants), and it is now the single remaining task rather
than an open-ended search.

**Method lesson, recorded.** The inventory of our own facts was worth more than
eight new attempts: it pointed at the one line we owned and never finished. And
the reason we abandoned it was a bug we never diagnosed -- I wrote "Stokes
topology is the obstacle" in the morning on the strength of a number that was
simply wrong.

## 2026-08-17 18:09 -- WHERE THE ASYMPTOTIC ROUTE ACTUALLY ENDS (measured, not guessed)

Pushed the saddle route to its limit with certified roots
(fmpq_poly.complex_roots) and ball arithmetic. Result: it works in a WINDOW of
knife indices and fails beyond it, for a reason that is now measured rather
than suspected.

**Where it works.** Relative error of the saddle sum against the exact
coefficient, times j:

    j       6      8      10     12     14     16
    err*j   2.50   2.44   2.40   2.37   2.35   2.52

so the leading-order error obeys err = C/j with C = 2.4 to within a few
percent, and the standard 1/N correction brings the error down to ~1.2% at
j = 14. In this window the asymptotics is genuinely good.

**Where it ends, and why.** From j = 20 the naive sum diverges from the truth
(error 1.8 at j=20, 48 at j=24). This is NOT precision loss: dps = 300 and
dps = 2000 give bit-identical numbers. The cause is visible in the size of the
individual contributions relative to the answer:

    j                                   12      16      20      24
    largest single saddle / true       1.20    1.14    2.90    54.9

At large j each individual saddle contributes tens of times MORE than the
final answer, which exists only through precise mutual cancellation. A sum of
leading-order terms cannot survive that -- the leading orders cancel and the
answer lives in what is left.

**So my morning intuition was right in substance and wrong in scale.** I did
write "the cancellation between saddles is the obstacle" -- and then produced
10^254 from a coding bug, which discredited the whole line for eight hours.
Both halves of that were errors: the bug, and then abandoning a correct
diagnosis because the number attached to it was wrong.

**What this means for the theorem, precisely.** Three regimes:
  * j small (2..20 so far): machine certificates, exact, done;
  * j moderate (6..16): saddle asymptotics accurate to ~1%, matching the margin
    we need -- but this window overlaps the certified range, so it adds
    confidence, not coverage;
  * j large (>= 20): the answer is an exponentially small remainder after
    cancellation of much larger terms. Leading-order asymptotics is structurally
    inadequate here.

**The technique the last regime requires,** named honestly: this is the setting
of RESURGENCE / trans-series (Ecalle, Berry-Howls, Delabaere-Pham) -- asymptotic
analysis where the answer sits below the size of individual contributions and
one must track exponentially small corrections across Stokes lines. That is a
specialised body of technique, and I cannot construct a rigorous uniform bound
with it inside this programme's current means. Stating that plainly is the
endpoint the founder asked for: not "more iterations needed", but "this
specific method is required, and here is exactly why".

## 2026-08-17 18:56 -- THE CONTOUR ROUTE: sign-definite loops DO exist, above a threshold

Following the founder's instruction to hunt for the thing we do not understand
rather than to compute correctly, this line produced the most promising position
of the day, plus two anomalies that turned into findings.

**The idea.** The verdict is a contour integral of a polynomial over a power, so
by Cauchy it is the SAME on every closed loop around the origin -- the loop is
ours to choose. A loop on which the integrand keeps ONE SIGN proves positivity
immediately and uniformly in the constraint index. That is precisely the
uniformity the programme lacks, and it needs no asymptotics at all.

**Measured result.** Sign-definite loops exist above a threshold. On the grid
(j, n = j+4, lam), 13 of 24 cells admit a loop with no dip, and the pattern is
sharp: for j <= 16 there is always a dip; for j >= 18 the loop is sign-definite
(the single exception is j = 18 at lam = 26). Confirmed in 120-digit ball
arithmetic at lam = 1: negative for sure at j = 10..16, POSITIVE FOR SURE at
j = 18, 20. Artifact: keystone_contour_hunt.json.

Where a dip remains it is tiny: 1e-3 of the answer at moderate index, down to
1e-8 in places, and shape optimisation (13 Fourier parameters) shrinks it
further by factors of 1.5 to 6.

**Anomaly 1, caught by the new rule, and it was a bug.** Shape optimisation
appeared to make positive cases WORSE (+4.0e-6 -> +6.4e-7), which is impossible
when maximising a minimum. Cause: the circle scan and the shape scan measured
two different densities -- one included the contour element dx, the other did
not. Fixed; the numbers are now comparable and the optimiser never degrades a
cell.

**Anomaly 2, and it is real structure.** The optimal radius has a KINK. For
j <= 16 it sits still (0.032, 0.032, 0.034, 0.034); from j = 18 it falls
(0.032, 0.027, 0.024, 0.023), roughly like 0.55/j. The switch to
sign-definiteness happens exactly at that kink. Picture: the loop is a thread
threading between nails. While the constraints are few the nails are sparse and
the thread can keep one radius; past a point the nails crowd and the thread must
pull inward -- and in that pulled-in regime the integrand stops changing sign.
So sign-definiteness is not a property of an individual constraint but a marker
of which regime the loop is in.

**A hypothesis that FAILED, recorded.** I guessed the mechanism was root
counting -- that sign-definiteness switches on when the loop encloses a
particular number of roots relative to N = j-1. Measured: the difference
(roots inside) - N runs +1, -1, -1, 0, -1, -4, -1, 0. No clean law. Dropped.

**Why this matters more than the numbers.** The remaining gap has changed shape
twice today. It began as "estimate an oscillatory sum whose individual terms are
55x the answer" -- hopeless without resurgence. It is now "for constraints below
the threshold, show that a tiny negative part of one explicit function on one
explicit loop is dominated by its positive part", with everything above the
threshold already sign-definite and hence trivially positive. The certified
region (machine certificates, j <= 20 as of tonight) covers exactly the range
where dips still occur. The two halves are close to meeting.

## 2026-08-17 21:20 -- THE RIPPLE IS AIRY: block widths scale as 1.37 n^(2/3)

The founder looked at tonight's 3D plot and said it looks like a drop falling on
water -- ripples spreading from a centre -- and told me to stop treating pictures
as decoration and read them as data. That reframing produced the finding.

**What was measured.** Along a fixed deformation the loop alternates between
blocks where it dips and windows where it is sign-definite. Widths of the three
FULL dip blocks at lam = 1 (from the scan to j = 78): 8, 14, 20 knives, at levels
n = 14, 32, 58. Dividing by n^(2/3):

    8 / 14^(2/3)  = 1.3772
    14 / 32^(2/3) = 1.3890
    20 / 58^(2/3) = 1.3348

A constant to within 4 percent across three independent blocks. So

        block width  =  C n^(2/3),   C = 1.37 +- 0.03 .

**Why the exponent matters.** 2/3 is the AIRY scale -- the universal exponent
that appears where two saddle points merge (a caustic). Rainbow fringes in optics
have it, the Airy function's zeros space out with it, and every uniform
asymptotic treatment of a fold catastrophe produces it. So the ripple is not an
artefact of our loop: it is the fingerprint of two coalescing saddles, and the
windows are the intervals between the resulting oscillation's zeros. That also
explains, at last, why leading-order saddle asymptotics failed at large j -- near
a caustic the individual contributions blow up while their sum stays small, which
is exactly the 55x cancellation measured earlier.

**Hypotheses killed on the way to it (all recorded, in one evening):**
  * quadratic law for the boundaries (2k^2+7k+6 in the spectral count):
    predicted a dip-free stretch at j = 80..86, measured dip -- 6 misses of 9;
  * ripple carried by the ARGUMENT of the nearest complex root: 2pi/arg gives
    38, 26, 146, 118, 102, nothing like the widths 8, 14, 20;
  * ripple carried by the MODULUS of that root: it falls 200x while the optimal
    radius barely moves;
  * interference of the two dominant saddles computed in float: contributions
    reach 1e109 and the phases become numerical garbage (flagged by the
    self-check list rather than believed);
  * width ~ 2 sqrt(n): fits the first block, drifts on the later ones (ratios
    2.14, 2.47, 2.63), whereas n^(2/3) holds flat.

**What it buys us.** A quantitative law where before there was only "windows
drift and recur". Two consequences to chase: (a) if the windows are Airy zeros,
their positions are PREDICTABLE, which turns "certify until the dips stop" into
"certify the finitely many blocks below a computable index"; (b) uniform Airy
asymptotics (Chester-Friedman-Ursell) is the standard tool for exactly this
regime and replaces the naive saddle sum that failed.

Status: a measured scaling law with an explicit constant, three data points, and
a named mechanism. Not a theorem. The next test is whether the window boundaries
sit at Airy zeros in the rescaled variable -- the scaled spacings measured so far
(0.45, 0.12, 0.40, 0.085, 0.43, 0.062) alternate as they should but shrink faster
than Ai zeros do, so the correspondence is not yet clean.

## 2026-08-17 22:02 -- two arithmetic laws killed, one structural fact found

**Both of tonight's arithmetic readings are dead, killed by my own data.**

1. *Block widths step by 6.* Refuted. The widths 8, 14, 20 were an artefact of
   scanning only EVEN j. On the full integer grid at lam = 1 the failing blocks
   are 9..17, 26..42, 47..48, 52..75, 81..113 -- widths 9, 17, 2, 24, 33, with a
   two-knife block that the even grid could not see at all. The closed form
   frozen at 21:37 (`results/FROZEN_PREDICTION_blocks.md`, block k spans
   2k(2k+3)..4k(k+3)) predicted block 4 = 88..112; measured 81..113. The END
   matched on the even grid and that was luck: the true edge is odd.
2. *Peak positions follow a power law.* Not established. Valid estimators on the
   same 10 peaks give exponents 0.76, 0.99, 1.31, 1.40 depending on which
   subset is used. A single-phase fit over 16 well-separated extrema leaves
   residuals of 0.83 phase steps, where a genuine single phase would leave well
   under 0.5, and q = 1/2 versus q = 2/3 cannot be distinguished (R^2 0.9922 vs
   0.9931). No exponent is claimed.

**What did survive, and it is structural rather than numerological.** Along
lam = 1, j = 6..131, every sign PROVEN in ball arithmetic (verdict_hp, ball
radius ~1e-105):

* inside a failing block, log10 of the depth is a STRAIGHT LINE in j -- e.g.
  j = 88..101 rises from 1e-17.4 to 1e-12.9 at a constant 0.35 per knife;
* the straight pieces meet at CUSPS where the depth nearly touches zero
  (1e-21 at j = 118, against a ball radius of 1e-120);
* cusps and smooth peaks STRICTLY ALTERNATE: 21 extrema in a row,
  8C 12P 23C 24P 26C 29P 30C 35P 47C 48P 51C 58P 59C 71P 80C 86P 88C 104P
  118C 125P 129C, no repetition anywhere;
* the sign flips at some cusps and not others -- j = 88 touches zero and
  returns on the same side.

That is the behaviour of a quantity whose sign is decided by two competing
exponential contributions: the cusp is where their magnitudes cross. It makes
the block boundaries derived objects, not primitive ones -- they are the subset
of cusps at which the dominant contribution changed sign. Five closely spaced
extremum pairs (separation 1-2 knives) are at the grid resolution limit and may
also be the beat of two frequencies rather than one.

**Instrument fixed tonight (this is what made the above possible).** The float
scan reported dips of -1e-16 for j = 80..92 and exactly 0.0 from j = 94 at
lam = 1 -- noise, not data. Worse, `best_circle` then picks the radius FROM that
noise, and a rigorous check at that radius returned -3.75e+12, twelve orders of
magnitude wrong. Added `density_min_hp`, `best_circle_hp`, `verdict_hp` to
contour_lib (ball arithmetic from the radius search to the final sign) plus a
self-test check that the high-precision and float paths agree where float is
still reliable. Nothing beyond j ~ 78 from any earlier float scan may be used.

Certificates: j = 28 closed, 2322 cells, zero failures. Running to j = 30.

## 2026-08-17 22:44 -- THE JACOBI NORMAL FORM: the grand theorem is one positivity statement

Reformulation, every step exact and machine-checked (lab/jacobi_normal_form.py):

1. Hhat is an m-th derivative, m = n - j. With
   F(u) = u^{n-1} G2(1/(s^2 u)) = SUM_t (-1)^t E_2t(n) s^{-2t} u^{n-1-t},
   term-by-term differentiation multiplies term t by (n-1-t)...(n-m-t) =
   prod_{i=j}^{n-1}(i-t) = Q(t). One line, no numerics.
2. F is NONNEGATIVE and a genuine polynomial of degree n-1:
   F = u^eps prod_a (s^2 u - a^2)^2 / s^{4K}, a in {n-2, n-4, ...},
   eps = 1 for even n and 0 for odd n, K = #a, deg G2 = 2K <= n-1.
3. Rodrigues: d^m/du^m[u^p (1-u)^Q] = c_m u^alpha (1-u)^beta
   P_m^{(alpha,beta)}(1-2u) with alpha = p - m = -1/2 and
   beta = Q - m = D/2 - 2 -- exactly the problem's two exponents.
4. F has degree n-1, so orthogonality leaves ONE term:
       sign I = (-1)^m * sign of the m-th Jacobi coefficient of F.

VERIFIED: 4500 exact cells (n = 6..20, all j, five lam, five D), sign from the
normal form vs sign from keystone_beta.J_exact -- 0 mismatches.

Since j runs 2..n, m = n-j runs over EVERY index 0..n-2. Therefore

    GRAND THEOREM  <=>  below the shore, F has an ALL-POSITIVE expansion in
                        P_m^{(D/2-2, -1/2)}(2u-1).

VERIFIED: 7084 coefficients strictly below the shore T_hat(lam), ZERO
non-positive. Above the shore they genuinely turn negative (70 of 637 families
at D = 26, 60, always at the largest m, i.e. the smallest spin j = 2, 3) --
which is the shore doing exactly what it is supposed to do.

Why this matters: no contours, no asymptotics, no per-knife work, and the object
is classical (positive Jacobi expansions, Schoenberg / Askey-Gasper territory).

## Instrument results that led here, and two things I killed on the way

* The argument principle gives a PROVEN necessary condition for the contour
  route: if the density is >= 0 on |x| = r then P(x)/x^N stays in the right
  half-plane, so its winding number is 0, so the circle encloses EXACTLY
  N = j-1 roots of P. Measured: 7 of 7 dip-free knives have exactly N inside.
* Consequence: the admissible radius lies between the N-th and (N+1)-th root
  moduli. My old logspace radius scan ignored this and searched the wrong
  place -- searching the correct window PROVED j = 52, 82, 86 dip-free although
  they were recorded as dips. Part of the "comb" was my instrument, not physics.
* When |z_N| = |z_{N+1}| (a conjugate pair at equal modulus) no radius encloses
  exactly N roots, so NO sign-definite circle exists -- proven impossibility,
  found at j = 30, 33, 36, 60, 63, 66, 96..105. A deformed loop can separate
  such a pair, which is why deformation rescued j = 55 and 58.
* KILLED: the fold-caustic / Airy hypothesis in its stated form. The minimum
  separation between saddle points falls smoothly and monotonically
  (2.1e-5 -> 2.3e-6 across j = 44..94) with NO feature at block edges, and the
  near-pairs sit at |z| ~ 1e-4, far inside the loop. No coalescence, no Airy.
* KILLED: the conjugate-pair-of-saddles explanation of the oscillation. Its
  angle is constant to four digits, giving a fixed period of 14.87 knives,
  while the measured peak spacings GROW: 10, 13, 15, 18, 21.

## 2026-08-17 22:55 -- the normal form is also a FAST certificate, and it survives large n

* CONTROL: rebuilding F from its roots u_a = (a/s)^2, a in {n-2, n-4, ...},
  reproduces the exact signs in 12 of 12 configurations. The root picture is right.
* ROBUSTNESS: positivity is not a knife-edge coincidence. Any single root may be
  moved by +-10 percent, or halved, and every coefficient stays positive. It
  breaks only when the LARGEST root is pushed toward u = 1, i.e. out of the
  interval where the Jacobi weight lives.
* THE CONTROLLING QUANTITY is therefore u_max, the largest double root. Scaling
  all roots by rho, the break happens at u_max = 0.85..1.03 depending on D and n,
  and the threshold RISES with n (0.907 at n = 9, 1.027 at n = 18).
* THE RACE: the real u_max = ((n-2)/(lam+n-1))^2 also rises with n (0.81 at
  n = 20, 0.90 at n = 40, 0.96 at n = 100). Checked directly: n = 24, 30, 40,
  50, 60 at lam = 1 and 7, D = 6 and 11 -- ZERO negative coefficients, all m.
  So the threshold rises faster. No failure found at large level.
* PRACTICAL CONSEQUENCE: one exact run at n = 60 settles ALL 59 knives of that
  level in 35 seconds. The strip-certificate run needed 9941 s to reach j = 28.
  The normal form is not just a reformulation, it is a much cheaper certificate.
  (Not a replacement: the strip certificates cover RANGES of lam and D
  symbolically, this fixes one lam and one D per run.)
* WHAT IS NOT DONE: no proof. The refuted shortcuts are recorded: single factors
  (u-c)^2 do NOT have positive expansions (18 of 84 coefficients negative), so
  the Gasper-style factor-by-factor induction cannot work; positivity here is a
  COLLECTIVE property of the whole root set.

## 2026-08-17 23:34 -- the step lemma has a classical shape: the ceiling IS a Jacobi zero

The induction runs smallest-root-first (verified: every partial product is
all-positive at every step, while largest-first fails until enough factors
accumulate). Measuring the admissible step by exact bisection, 18 iterations:

    t (factors in place)   ceiling            largest zero of P_k^{(-1/2, D/2-2)}
     3                     0.8213234          0.8455426  (k=4)
     4                     0.8590775          0.8455426  (k=4)
     5                     0.8836708          0.8928346  (k=5)
     6                     0.9003677          0.8928346  (k=5)
     7                     0.9166565          0.9214753  (k=6)
     8                     0.9260788          0.9214753  (k=6)
     9                     0.9356689          0.9400622  (k=7)
    10                     0.9439964          0.9400622  (k=7)
    11                     0.9508476          0.9527821  (k=8)

EXACT INTERLACING over eight consecutive k: the largest zero of P_k lies between
ceiling(2k-5) and ceiling(2k-4). So the threshold is not an arbitrary curve -- it
is (bracketed by) the largest zero of a Jacobi polynomial of degree k ~ t/2 + 5/2,
and those zeros have classical bounds.

ASYMPTOTIC CHECK, and it is a PREDICTION that came out right:
  * measured 1 - u_max(k) = 2.051 k^(-1.824) over k = 4..21 (classical limit -2);
  * hence the ceiling gap at step t is about 7.2 t^(-1.82);
  * the ladder's top gap is 1 - ((n-2)/(lam+n-1))^2 ~ 4/n at lam = 1, and
    t_max ~ n/2, so the ladder gap ~ 2/t;
  * ratio ladder/ceiling ~ 0.28 t^0.82, which at n = 31 (t_max = 15) predicts a
    margin of 2.5x. MEASURED: 0.125 against 0.049, i.e. 2.5x.

So the margin does not close as the level grows -- it GROWS like n^0.82. That is
consistent with the direct checks at n = 60 and n = 80 finding no negative
coefficient.

WHAT REMAINS TO PROVE: exactly one statement -- why the admissible step is that
Jacobi zero. Everything else in the chain is either verified exactly or classical.
This is the smallest the keystone has ever been, and it is the first form of it
that is a candidate for Lean.

## 2026-08-17 23:39 -- the ceiling has an EXACT closed form; one inequality is all that is left

Multiplying an all-positive H by (u-c)^2 changes the m-th bracket to a quadratic
in c:

    bracket_m(c) = (-1)^m [ A_m - 2 c B_m + c^2 C_m ],
    A_m = INT H u^2 w P_m,   B_m = INT H u w P_m,   C_m = INT H w P_m,

with w = u^(-1/2)(1-u)^(D/2-2) and P_m = P_m^{(-1/2, D/2-2)}(1-2u). Therefore

    CEILING(H) = min over m of the smallest positive root of that quadratic.

VERIFIED: closed form vs 18-step bisection agrees to 3e-6, which IS the bisection
precision (2^-18 = 3.8e-6), at every t from 1 to 10. So the ceiling is not an
empirical curve any more; it is an explicit algebraic quantity.

Two structural facts measured on top of it:
* the binding index is LOW and grows like m ~ t/2 + 3/2 (measured 2,2,3,3,4,4,4,
  5,5,6,6 for t = 1..11), not the top index -- the top index gives a critical c
  above 1 and never binds beyond t = 0;
* Cauchy-Schwarz explains only the lowest indices. B_m^2 < A_m C_m holds for
  m <= 1..3 (growing slowly with t) and fails for the rest, so "the signed
  measure stays positive" is a real but INSUFFICIENT mechanism. Recorded as a
  partial idea, not as the answer.

WHAT REMAINS, stated exactly: prove c_{t+1} < CEILING(H_t) for the ladder
c_t = (a_t/s)^2. Supporting evidence that it is true and not marginal: the
ceiling interlaces with the largest zeros of P_k, k ~ t/2 + 5/2, exactly, over
eight consecutive k; those zeros satisfy 1 - u_max = 2.051 k^(-1.824)
(classical limit -2), giving a ceiling gap ~ 7.2 t^(-1.82) against a ladder gap
~ 2/t, i.e. a margin growing like t^0.82. That prediction was tested: at n = 31
it gives 2.5x, and the measured margin is 2.5x (0.125 against 0.049).

## 2026-08-17 23:41 -- CORRECTION: the Jacobi-zero identification of the ceiling is NOT a law

Checked the index relation k ~ (t+5)/2 at other D. It holds 7 of 9 steps at
D = 6 (where I found it) but only 4/9 at D = 4, 4/9 at D = 11 and 2/9 at D = 26:
the matching index grows with D. Worse, "the ceiling is near some Jacobi zero" is
close to vacuous, since every value in (0,1) has a nearest zero. So:

* WITHDRAWN: the statement that the ceiling IS (bracketed by) the largest zero of
  P_k with k ~ t/2 + 5/2. It was a D = 6 coincidence, and I should have varied D
  before writing it down. The consequence -- the asymptotic margin estimate
  ~ t^0.82 built on the classical zero asymptotics -- loses its support too, and
  the fact that its number matched the measured 2.5x at n = 31 does not rescue it:
  a right number from a wrong mechanism is still wrong.
* STANDS, because it is derived rather than fitted: the ceiling is exactly
      min over m of the smallest positive root of A_m - 2 c B_m + c^2 C_m,
  agreeing with 18-step bisection to 3e-6 = the bisection precision, and the
  binding index is low (m ~ t/2 + 3/2 at D = 6, also to be re-checked in D).
* STANDS: the direct measurements. Margin 2.5x at n = 31 (0.125 against 0.049);
  no negative coefficient at n = 24..80; 7084 coefficients below the shore clean;
  the growing certificate grid clean.

The honest way to ask the asymptotic question is to measure the margin of the
CLOSED FORM against the ladder as n grows, with no intermediate identification.
That is the next measurement.

## 2026-08-17 23:54 -- the induction is asymptotically TIGHT, and that is the real difficulty

Direct measurement, no intermediate identification (results/step_lemma.json):

    worst margin ceiling/ladder over all steps
    n:        11      15      21      31      41
    lam=1:   1.324   1.231   1.163   1.109   1.082
    lam=7:     -     2.371   1.898   1.566   1.414

The margin SHRINKS with the level. I wrote the opposite an hour ago, having only
measured at one n; that claim is withdrawn. The law is

    margin  ~  1 + C(lam)/n,   C(1) ~ 3.4,  C(7) ~ 17

since n(margin-1) = 3.56, 3.47, 3.42, 3.38, 3.36 for lam = 1 and 18.9, 17.5,
17.0 for lam = 7. C stays positive, so the inequality holds at every level
tested, but it is asymptotically tight rather than comfortable.

Note on interpretation: the partial products are scaffolding, not physics. Only
the full product is the physical object. If the margin ever crossed 1, the
INDUCTION would die, not the theorem.

HOW MUCH DOES THE CEILING DEPEND ON WHICH H? Little. At fixed degree, four
different ladders and a deliberately different geometric root set give c_max
within 0.7 to 4.5 percent of each other (spread grows with degree: 0.0075 at
t = 3 to 0.0269 at t = 6, D = 6). So a lemma stated in terms of (degree, beta)
alone is close to true.

AND HERE IS THE OBSTACLE, as arithmetic rather than intuition: the H-dependence
spread (a few percent, growing with degree) becomes comparable to the margin
(3.4/n) at around n ~ 100. A degree-only step lemma therefore cannot carry the
induction to arbitrary n; the proof has to use the ladder's own structure. That
is a precise statement of what makes this theorem hard, and it is the first time
the difficulty has been quantified rather than described.

## 2026-08-17 23:58 -- the crux is ONE inequality, and the assembly order is a red herring

Tested five assembly strategies on the same ladder (n = 15, 21, 31, lam = 1,
D = 6), measuring the worst margin over the whole assembly:

    smallest first (baseline)   1.231   1.163   1.109
    smallest first, in PAIRS    1.231   1.170   1.109
    middle out                  1.231   1.163   1.109
    largest first               fails
    alternating small/large     0.866 / fails

Every viable order gives the SAME worst margin, and in every case the worst step
is the LAST one (t = 9 at n = 21, t = 14 at n = 31, t = 19 at n = 41). So the
tightness is not an artefact of how the induction is organised, and no reordering
buys margin.

CONSEQUENCE -- the keystone is now one inequality about the physical object:

    (a_max/s)^2  <  CEILING( F divided by its last factor ),
    a_max = n-2,  s = lam + n - 1,

where CEILING is the explicit min-over-m smallest positive root of
A_m - 2 c B_m + c^2 C_m. The measured margin is 1 + C(lam)/n with C(1) ~ 3.4 and
C(7) ~ 17, i.e. true at every level tested and asymptotically tight.

This is the smallest the problem has ever been: everything else in the chain is
verified exactly or classical, the scaffolding is provably order-independent, and
what is left is a single explicit inequality with a measured margin law.

## 2026-08-18 00:04 -- WHICH knife holds the boundary: spin 2, exponentially tightly

Exact rational computation over every knife of every level n = 10..70 at
lam = 1, 7 and D = 6, 11 (`article/visuals/the_weakest_knife.py`):

* the weakest constraint is ALWAYS m = n-2, i.e. j = 2 -- at every level and
  every (lam, D) tested. CORRECTED (ERR-0004): j = 2 is the LEADING trajectory,
  ell = 2n-4, the HIGHEST spin of the level, since ell = 2n-2j. I first wrote
  "lowest spin", which is backwards;
* its size relative to the largest coefficient of the same level falls
  exponentially in n: 2.3e-2 (n=10), 1.7e-3 (14), 2.6e-5 (20), 3.6e-7 (26),
  1.1e-9 (34), 6.5e-13 (44), 8.4e-17 (56), 2.2e-21 (70) at lam = 1, D = 6;
* the rate is about 0.33 decades per unit n and DRIFTS: upward for lam = 1
  (0.286 -> 0.327) and downward for lam = 7 (0.412 -> 0.364), both heading toward
  roughly 0.33-0.36. A straight line in n leaves 0.18 dex of residual, a
  quadratic 0.05 -- so it is exponential with a slowly moving rate, not a clean
  exponential. Recorded as measured behaviour, not as a law.

CONSEQUENCE FOR THE PROOF. The margin the theorem holds by, at low spin, is
exponentially small in the level. So no crude bound can prove it: any argument
has to track an exponentially small quantity exactly. That is a concrete
explanation of the difficulty, replacing the earlier hand-waving.

CONSEQUENCE FOR THE PHYSICS. This family sits exponentially close to the
LEADING-trajectory positivity boundary as the level grows. The binding constraint
is the highest spin of each level, which is why low-spin dominance FAILS here
(C4 in research/inventory-of-facts.md).

Margin trend continues to hold up: at n = 51, worst margin 1.06637, so
n(margin-1) = 3.385 -- against 3.36 at n = 41 and 3.38 at n = 31. The constant is
stable near 3.36-3.39 rather than drifting to zero, so the induction's inequality
is not about to fail.

## 2026-08-18 00:21 -- END-TO-END VALIDATION: the new machinery reproduces the published shore

Working out knife j = 2 in the Jacobi normal form gives a two-term expression
(orthogonality leaves only q = n-2 and q = n-1), and with the Saalschutz closed
form for the moments (verified: 432 exact checks, 0 mismatches) it collapses to an
elementary condition. After correcting a hand-simplification slip -- my first
ratio was off by exactly (2n-3)/(2n-5), caught because the error was independent
of D, which no genuine D-dependent quantity could be -- the condition is

    knife j=2 holds  <=>  D  <  B(n,lam),
    B(n,lam) = [2n^3 - 4n^2 + 6n - 9 + 6 lam (2n^2 - 5n + 3)
                + 3 lam^2 (2n - 3)] / [n (n-2)]

Validated forward before any claim: 621 cells (n = 3..25, six lam, five D
including D just below the shore) -- predicted sign vs directly computed sign,
ZERO disagreements.

AND B(n,lam) IS IDENTICALLY T_n(lam), the trajectory law of the published shore
paper: expanding T_k = 3(2k-3)/(k(k-2)) (lam^2 + (2k-2) lam + 1) + 2k gives the
same numerator term by term. The shore paper DEFINES T_n by
a_{n,2n-4} >= 0 <=> D <= T_n(lam), so this is NOT a new theorem -- it is the
published result rederived from a completely different route (Beta reduction ->
Jacobi normal form -> Saalschutz), landing exactly on it.

WHY THAT MATTERS ANYWAY: it is the first end-to-end check of tonight's machinery
against an independently published result, and it passes exactly, on 621 cells
plus an algebraic identity. Everything downstream of the normal form now rests on
a chain that has been closed at one end.

REFRAMING OF WHAT IS OPEN. j = 2 is the shore (published). j = 3 is the blade
theorem (published, release/qg-blade-theorem). So the genuinely open part of the
keystone is j >= 4, and the normal form now settles all j of a level in one pass.

## 2026-08-18 03:16 -- the binding knife SWITCHES ENDS, and that refines a recorded fact

Instrument first: added `M_closed` (Saalschutz) and `jacobi_coeff_fast` to
lab/jacobi_normal_form.py. Knife j now costs j terms instead of an m-term sum, so
a whole level is O(n^2) rather than O(n^3). Verified against the slow path on
891 exact comparisons, 0 mismatches, 11.8x faster at n = 30. Without it the sweep
below timed out.

TESTED CLAIM: "within a level the smallest coefficient is always the last one
(m = n-2, the leading trajectory)". If true, the whole theorem would collapse to
the already-published shore. It is FALSE as stated: 103 of 1120 configurations
(levels 5..60, five lam, five D below the shore) have their minimum elsewhere,
and in every one of those the minimum sits at the OPPOSITE end, m = 0, the lowest
spin j = n.

So there are two competing candidates for "weakest knife", one at each end of the
spin spectrum, and which one wins depends on (lam, D):

              D:    3    4    5    6    8   11   16   23   40   60  120
    lam = 1/4       L    L    L    L    L    L    .    .    .    .    .
    lam = 2         L    L    L    L    L    L    L    Z    .    .    .
    lam = 5         L    L    L    L    L    L    L    L    Z    Z    .
    lam = 14        L    L    L    L    L    L    L    L    L    Z    Z
    lam = 60        L    L    L    L    L    L    L    L    L    L    L
    (L = leading trajectory binds, Z = lowest spin binds, . = above the shore)

Mapped properly in article/visuals/which-end-binds.png at n = 12, 24, 40: the
"lowest spin binds" region is a band hugging the shore, and it NARROWS as the
level grows.

WHY THIS MATTERS BEYOND THE PROOF. research/inventory-of-facts.md C4 records
"low spin dominance FAILS here" and uses it as a result contradicting a published
conjecture. That statement is now refined rather than overturned: it fails in the
large region where the leading trajectory binds, and it HOLDS in a band next to
the shore. The published claim should carry that qualifier.

Consequence for the keystone: the theorem does NOT reduce to the shore, because
the shore is the leading-trajectory condition and the leading trajectory is not
always the weakest. Both ends have to be controlled.

## 2026-08-18 03:33 -- two more routes closed, and a map of what is left

With the Saalschutz closed form the m-th coefficient is an explicit finite sum
c_m = SUM_{q=m}^{n-1} F_q M(q,m). Two natural shortcuts were tested and both fail.

1. TERM DOMINATION. Does the first term (q = m) exceed the rest, so that the sign
   is decided term by term? NO, and not marginally: sum|rest| / |first| reaches
   3.1e3 at n = 9 (lam = 1, D = 6), 1.5e10 at n = 21, 4.0e33 at n = 30 with
   lam = 26. The worst index is m = 0 or 1. Positivity therefore rests on a
   delicate cancellation between huge alternating terms -- exactly the
   exponential thinness measured earlier, now seen at the level of the summands.

2. CLOSED PRODUCT FORM. If c_m were a product of Gamma factors, its numerator
   would only contain primes bounded by the parameters. Factored exactly: the
   denominators are smooth (largest prime <= 4n, as Pochhammers must be) but the
   numerators are not -- 2.3e11 at n = 9, 6.3e13 at n = 12 lam = 7, 3.5e12 at
   n = 14. So there is NO closed product form for general m. The exceptions are
   the last indices, m = n-2 and n-3, where the sum has two or three terms; that
   is precisely the case already exploited to rederive the shore.

CONSEQUENCE: the theorem cannot come from an identity. It needs an inequality
argument that survives cancellation of relative size 1e33.

MAP OF ROUTES TRIED THIS NIGHT (all conclusions from our own data):
  * per-knife contour certificates -- works but does not scale, and part of the
    failure structure was the instrument (radius searched outside the admissible
    window; argument principle fixes that);
  * single-circle contour -- provably impossible for specific j (conjugate root
    pair at equal modulus), deformed loops rescue some of those (j = 55, 58);
  * Airy / fold caustic -- no saddle coalescence anywhere, dropped;
  * conjugate saddle pair -- gives a constant period 14.87 against measured
    growing spacings, dropped;
  * factor-by-factor (Gasper-style) induction -- single squares are not positive,
    dropped;
  * ladder induction smallest-first -- works at every step, but asymptotically
    tight (margin 1 + 3.38/n, confirmed to n = 81) and the degree-only version
    runs out of room near n ~ 100;
  * term domination -- fails by up to 33 orders;
  * closed product form -- excluded by prime factorisation.

WHAT IS LEFT, precisely: a bound on the alternating sum c_m that keeps the
(-1)^m sign, valid for all m, using the ladder structure of the roots
u_a = (a/s)^2 with a in {n-2, n-4, ...}. Every ingredient is now explicit and
exact; nothing in the chain is numerical any more except the verification.

## 2026-08-18 03:36 -- creative telescoping does not apply in the obvious variable

The letter's route (2) was: get a low-order recursion in j by creative
telescoping. With the terms now explicit this is directly testable, and the
answer is no in the obvious formulation.

* c_m = SUM_q F_q M(q,m). The ratio t(q+1)/t(q) at n = 14, lam = 1, D = 6, m = 4
  runs -33.248, -13.690, -7.456, -4.504, -2.838, -1.797, -1.102, -0.615, -0.263,
  and no rational function of q with numerator and denominator degree <= 4 fits
  it. The reason is structural: F_q are the elementary symmetric functions of the
  squares (a/s)^2, and those are not hypergeometric in their index.
* The natural repair -- read M(q,m) as a moment sequence in q and fold the sum
  back into a product -- closes on itself: the measure is w P_m du, and its sign
  changes ARE the difficulty. Circular, recorded so it is not tried again.

So a recursion, if one exists, has to be sought in n or m with the central
factorial numbers carried along, not in q. That is a heavier computation
(the E_2t satisfy their own recursion) and is the natural next attempt.

Also measured tonight: the "lowest spin binds" band shrinks with the level as a
power law rather than vanishing -- 27.3 percent of the cells below the shore at
n = 12, then 16.1, 11.8, 9.3 at n = 24, 40, 55, i.e. about n^-0.7. So it is a
genuine feature at every finite level, not a small-n artefact.

## 2026-08-18 03:38 -- the level recursion does NOT split into positivity-preserving steps

The established level recursion G2^(n+2) = G2^(n) (1 - n^2 y)^2 says the level
gains exactly one new double root, which looks like the ladder. But s = lam+n-1
changes too, so ALL the old roots move: (a/s)^2 -> (a/(s+2))^2, a SHRINK by
(s/(s+2))^2.

Tested whether a pure dilation preserves the all-positive property (60 cases,
n = 9..21, three (lam, D)):

  * SHRINKING breaks it -- 44 failures of 60. c = 9/10 survives everywhere,
    c = 1/2 already fails at lam = 1, and small c fails always. The extreme is
    understandable: as c -> 0 the polynomial degenerates to a constant, whose
    coefficients at m >= 1 are zero rather than positive.
  * STRETCHING preserves it in every case tested, up to c = 2, even though that
    pushes roots past u = 1 and outside the weight's support.

So the level recursion is the composition of a shrink (not positivity-preserving)
with a multiplication by the new factor. Both levels are positive, but neither
step is individually, so induction on levels in this form does not work.

Recorded also because it corrects an intuition: earlier I found that doubling the
LARGEST single root breaks positivity, and here doubling ALL roots does not.
Moving one root and moving all of them are genuinely different perturbations.

## 2026-08-18 03:42 -- a second, independent measure of how close the family is to failing

Since stretching all roots preserves positivity and shrinking eventually breaks
it, every configuration has a DILATION THRESHOLD c0: shrink all roots by c and
positivity survives exactly for c >= c0. The theorem holds because the real
configuration sits at c = 1.

Measured by bisection (exact arithmetic), lam = 1, D = 6:

    n      7      9     12     15     18     21     25     30     36     44
    c0   .627   .694   .759   .801   .830   .853   .874   .894   .910   .926
  n(1-c0) 2.61  2.76   2.89   2.99   3.06   3.09   3.15   3.19   3.24   3.28

So 1 - c0 ~ C/n with C still climbing at n = 44. The ladder-step margin measured
earlier gave 1 + 3.38/n with C stable at 3.36-3.39 from n = 31 to 81.

CAREFUL: these are close but NOT shown to be the same constant. At lam = 1 the
dilation constant is still rising (3.28) toward the step constant (3.38); at
lam = 7 they are further apart (11.9 rising, against about 17). Two independent
measures of the same margin agreeing to within this much is encouraging and is
the reason to record it, but calling them equal would be exactly the kind of
claim I had to withdraw twice tonight.

What is safe to say: however the distance to failure is measured, it shrinks like
a constant over the level, with the constant growing with lam. The CHR family
sits a relative distance of order a few / n from the positivity boundary.

Also: the "lowest spin binds" band continues its power-law decline -- 27.3, 16.1,
11.8, 9.3, 7.5 percent at n = 12, 24, 40, 55, 70.

## 2026-08-18 04:09 -- AN EXPLICIT CLOSED FORM FOR EVERY KNIFE, and the fourth knife measured

The Saalschutz moments turn each knife into a finite sum, and the ratios of
consecutive moments collapse to elementary products. Writing m = n - j, dividing
by the (positive) t = 0 term and verifying every step against the exact engine:

    knife j > 0   <=>   SUM_{t=0}^{j-1} (-1)^t E_2t(n) / s^(2t) * R_t  >  0

    R_t = [prod_{i=1..t} (j-i)] [prod_{i=1..t} (D + 4n - 2j - 5 - 2(i-1))]
          / ( [prod_{i=1..t} (n-i)] [prod_{i=1..t} (2n - 1 - 2i)] ),   R_0 = 1

with the central factorial numbers now explicit polynomials, each verified on
BOTH parities for n up to 59:

    E_2 = n(n-1)(n-2)/3
    E_4 = n(n-1)(n-2)(5n^3 - 24n^2 + 28n + 12)/90
    E_6 = n(n-1)(n-2)(n-3)(n-4)(35n^4 - 154n^3 + 172n^2 + 292n + 120)/5670

VERIFICATION: the closed form's sign agrees with the exact engine on 24 cells for
each of j = 2, 3, 4 (n from j+3 to j+18, lam = 1 and 7, D = 6, 11, 23), zero
disagreements. Two off-by-one slips in my own derivation of R_t were caught by
exactly this check before anything was concluded from them.

## The fourth knife

Clearing positive denominators gives P4(n, D, lam), degree 9 in n, 3 in D, 6 in
lam, whose positivity IS the fourth knife. Exact evaluation on 1736 cells below
the shore: zero failures.

Since P4 is cubic in D with a negative leading coefficient, there is a critical
D*(n, lam) where the knife vanishes, and the theorem to prove is D* > T_hat(lam).
Measured (minimum of D* over n = 5..120):

    lam      1/4     1/2       1       2       3       5       7      14      26      60
    D*/shore 1.316  1.252   1.220   1.163   1.142   1.116   1.062  1.0205  1.010  1.0042

So knife 4 never cuts into the allowed region in anything tested, and the margin
shrinks toward 1 as lam grows -- i.e. it appears ASYMPTOTICALLY TANGENT to the
shore, the same delicacy the published blade theorem has for knife 3.

NOTE, so the table is not over-read: the lam = 150 row (1.115) is an artefact of
capping the search at n = 120. The minimising level grows roughly like 1.7 lam
(n = 102 at lam = 60), so at lam = 150 the true minimum lies outside the range
scanned. That row should be recomputed with a wider n before it is used.

STATUS: this is an explicit, verified closed form and a measured statement, NOT a
proof. What would make it a theorem is showing D*(n, lam) > T_hat(lam) for all
n and lam -- now a finite algebraic question about one explicit polynomial,
which is exactly the shape the published blade theorem took for knife 3.

## 2026-08-18 04:17 -- the FOURTH knife is tighter than the third

With the n-range now tied to lam (the minimising level sits near 1.7 lam, and an
earlier cap at n = 120 produced a spurious upturn), the two knives behave
differently at large lam:

    lam        1/4    1/2      1      2      3      5      7     10     14     20     26     40     60
    knife 3   1.187  1.170  1.138  1.105  1.088  1.081  1.080  1.081  1.083  1.084  1.086  1.087  1.087
    knife 4   1.316  1.252  1.220  1.163  1.142  1.117  1.062  1.032  1.0205 1.013  1.010  1.0064 1.0042

(the number is min over levels of D*, divided by the shore; above 1 means the
knife never cuts into the allowed region)

So knife 3 -- the published blade theorem -- levels off at about 1.087, while
knife 4 keeps descending toward 1 and is at 1.0042 by lam = 60, with the
minimising level at n = 102. The FOURTH knife is therefore the tight one at large
lam, not the third.

That matters for the programme: the published blade theorem is delicate because
its cone is exactly tangent to the shore asymptote in the scaling limit; this
measurement says knife 4 approaches the shore even more closely at finite lam.
Whether it stays above 1 as lam grows is precisely the open question, and it is
the same shape of question the blade paper answered for knife 3.

Reproducible: lab/knife_closed_form.py (0 disagreements against the exact engine
on 24 cells per knife, 1120 cells below the shore with 0 failures) and
article/visuals/the_fourth_blade.py (certified flint roots, n-range reported per
point so the cap can be audited).

## 2026-08-18 04:26 -- knife 4 is SINGLED OUT, and it is not a trend in j

E_8(n) derived and verified on both parities to n = 54, which unlocks knife 5.
All of j = 2, 3, 4, 5 now have verified closed forms (24 cells each against the
exact flint engine, zero disagreements).

min over levels of D*, divided by the shore:

    lam         1/4    1/2      1      2      3      5      7     10     14     20     26     40     60
    knife 3    1.187  1.170  1.138  1.105  1.088  1.081  1.080  1.081  1.083  1.084  1.086  1.087  1.087
    knife 4    1.316  1.252  1.220  1.163  1.142  1.117  1.062  1.032  1.0205 1.013  1.010  1.0064 1.0042
    knife 5    1.385  1.333  1.275  1.212  1.179  1.158  1.112  1.072  1.0665 1.0655 1.0654 1.0653 1.0658

So the earlier reading -- "each further knife is tighter" -- is WRONG, and I am
glad the fifth was computed before that was written down as a trend. Knives 3 and
5 level off (near 1.087 and 1.066). Knife 4 alone keeps descending toward 1.

That is a sharper statement than a trend: the family has ONE distinguished tight
constraint, the fourth trajectory ell = 2n-8, and its neighbours on both sides
settle away from the shore. Whether knife 4 stays above the shore as lam grows is
the open question, and it is now a finite algebraic question about one explicit
polynomial P4 (degree 9 in n, 3 in D, 6 in lam).

The minimising level grows with lam roughly like 1.7 lam for knife 4 (n = 102 at
lam = 60) and like 3 lam for knife 5 (n = 179 at lam = 60); the scan range is
tied to lam and reported per point, after an earlier fixed cap at n = 120
produced a spurious upturn.

## 2026-08-18 04:42 -- THE SCALING LIMIT OF THE WHOLE FAMILY, IN CLOSED FORM

Taking n = rho lam, D = d lam and lam -> infinity at FIXED j, every term of the
closed form becomes (-1)^t C(j-1,t) x^t with x = rho(d+4rho)/(6(rho+1)^2), because
the t! comes from E_2t(n) = n^(3t)/(3^t t!) + ... and the falling factorial
(j-1)...(j-t) comes from R_t. Newton's binomial then sums it for every j at once:

    knife_j  ->  (2 rho^2 + 12 rho + 6 - d rho)^(j-1) / (6 (rho+1)^2)^(j-1)

Consequences, immediate:

* j ODD  -> even power -> never negative. The odd knives are safe at leading
  order. This is the recorded parity law, now with its mechanism.
* j EVEN -> odd power -> the knife holds exactly while d < 2 rho + 12 + 6/rho,
  whose minimum over rho is at rho = sqrt(3) and equals 12 + 4 sqrt(3) --
  EXACTLY the shore asymptote. The even knives are therefore exactly marginal
  against the shore in the scaling limit: tangent, not crossing.

That explains the finite-lam measurements without any fitting: knife 4 descends
to D*/shore = 1.0042 by lam = 60 while knives 3 and 5 level off at 1.087 and
1.066.

PREDICTION MADE AND THEN TESTED: the mechanism says knife 6 must carry an ODD
power of the bracket. Computed afterwards: -385 rho^5 (d rho - 2 rho^2 - 12 rho
- 6)^5. Power 5, odd, as predicted; its closed form also agrees with the exact
engine on 24 cells with zero disagreements. E_10(n) was derived and verified on
both parities to n = 49 to make that test possible.

LIMITATIONS, on the record: the limit is at FIXED j and is not uniform in j (the
approach E_2t -> n^(3t)/(3^t t!) is markedly slower for larger t: at n = 160 the
ratio is 0.98 for t = 1 but 0.62 for t = 8). It is a leading-order statement; ON
the curve the leading term vanishes and subleading terms decide, which is the
same delicacy the published blade theorem handles for j = 3. So this explains the
structure and identifies the marginal knives; it does not by itself close the
finite-lam theorem.

Written up as results/SCALING_LIMIT_THEOREM.md.

## 2026-08-18 04:46 -- the tangency is approached from the SAFE side (asymptotics closed)

The scaling-limit form says the even knives vanish exactly on
d = 2 rho + 12 + 6/rho, whose minimum over rho is the shore asymptote
12 + 4 sqrt(3) at rho* = sqrt(3). Two things finish the asymptotic question:

1. STRICTLY BELOW THE SHORE the leading term already settles it. For d < the
   curve, the bracket (d rho - 2 rho^2 - 12 rho - 6) is negative; knife 4 carries
   it to an ODD power with a minus sign in front, so the leading term is positive.
   Since the shore is the MINIMUM of the curve, d < shore implies d < curve(rho)
   for every rho, hence every knife is positive at leading order.

2. ON THE CURVE the leading term vanishes and the next order decides. Substituting
   D = (2 rho + 12 + 6/rho) lam exactly and expanding:

     j = 4: -12 rho (rho+1)^2 (128 rho^4 - 972 rho^3 + 810 rho^2 + 288 rho - 117)
     j = 6: 1584 rho^2 (rho+1)^4 (2 rho^2 - 6 rho - 3)
            (256 rho^4 - 1692 rho^3 + 738 rho^2 + 576 rho - 45)

   At the tangency rho = sqrt(3) these are exactly

     j = 4:  22896 sqrt(3) + 128952        = 1.68609e5   > 0
     j = 6:  1811652480 sqrt(3) + 3362078016 = 6.49995e9 > 0

   both strictly positive. Moreover the quartic for j = 4 has real roots at
   -0.439, 0.267, 1.182, 6.584, so the subleading term is positive on the whole
   interval rho in (1.182, 6.584) -- and rho* = sqrt(3) = 1.732 sits comfortably
   inside it, not on its edge.

CONCLUSION for the scaling limit: the even knives touch the shore asymptote from
the SAFE side. They do not cut into the allowed region even in the limit, and the
tangency is not a knife-edge in rho either.

That closes the asymptotic question I posed at the start of the night ("does the
fourth knife survive as lam grows?"). What remains is the finite-lam statement,
where the margin is 1 + C/n and the exponentially small quantities live.

## 2026-08-18 04:48 -- the second limit closes cleanly; joining it to the certificates does not (yet)

THE OTHER LIMIT. With lam and D held FIXED and n -> infinity, the leading
coefficient of the knife polynomial is a positive CONSTANT:

    j = 3: 20      j = 4: 280      j = 5: 2800      j = 6: 12320

So every knife is positive at large enough level for any fixed (lam, D). That is
the tail of the region the finite certificates cannot reach, and it suggests the
architecture the letter proposed: certificates close n <= n0, asymptotics close
n > n0.

WHAT DOES NOT WORK YET: the generic Cauchy root bound gives an n0 that is far too
crude to join the two --

    lam = 1,   D = 11:  n0 = 123      (certificates already reach n = 150, so this one closes)
    lam = 1,   D = 6:   n0 = 1189
    lam = 3:            n0 ~ 2e4 to 7e4
    lam = 7:            n0 ~ 1.7e7
    lam = 60:           n0 ~ 1.9e13

The reason is structural rather than technical: the coefficients carry powers of
lam, so a bound that ignores that scaling explodes, while the true threshold sits
at n of order lam (the scaling limit says the interesting region is n ~ rho lam
with rho = O(1)). Closing the gap therefore needs a bound written in n/lam, not a
generic one.

Worth recording that ONE cell does close completely by this route today:
lam = 1, D = 11, where n0 = 123 and the certificates run to n = 150. That is the
first (lam, D) for which knife 4 is settled for ALL levels, not just the tested
ones.

## 2026-08-18 04:51 -- the local expansion at the tangency, and a near-miss I caught in time

Writing b for the distance below the critical curve (the bracket equals -b, so
b > 0 is the allowed side) and expanding knife 4 at rho = sqrt(3):

    P / lam^9 = 105 sqrt(3) b^3
              + lam^-1 ( 41713.7 b - 2301.4 b^2 - 882 b^3 )
              + lam^-2 ( 168609 - 273716 b + 19313 b^2 + 1364.9 b^3 )
              + lam^-3 ( -421487 + 1044960 b - 70541 b^2 - 396 b^3 ) + ...

with the exact coefficients 105 sqrt(3), 18144 + 13608 sqrt(3),
22896 sqrt(3) + 128952, 555255 - 563922 sqrt(3), and so on.

Two readings, both useful:

* AT the tangency (b = 0) the series starts 168609/lam^2 - 421487/lam^3 + ...,
  positive as soon as lam exceeds about 2.5 to this order. That is the local
  statement that the even knife touches the shore from the safe side.
* MOVING BELOW the curve helps rather than hurts: the leading b-dependence is
  +41713.7 b / lam, positive.

A NEAR-MISS WORTH RECORDING. Before evaluating, I read the linear-in-b part of
A_1 by eye, saw its first monomial -504 b rho^6, and started an estimate that
concluded knife 4 FAILS at b ~ lam^(-1/2) for large lam -- which would have
contradicted every measurement of the night. Evaluating the whole coefficient at
rho = sqrt(3) gives 18144 + 13608 sqrt(3) = +41713.7, positive: the other four
monomials outweigh the first. The rule that saved it is the ordinary one --
evaluate the sum, never one term of it -- and it is the same rule that caught the
two off-by-one slips in R_t earlier tonight.

## 2026-08-18 10:11 -- KNIFE 4 PROVED on a compact region (machine proof, not a scan)

Method: exact Bernstein subdivision. On each box the polynomial is re-expanded in
the Bernstein basis with rational arithmetic; the minimum of those coefficients is
a rigorous lower bound by the convex-hull property, and a box is accepted only
when it is strictly positive, otherwise split. Subdivision tightens the bound
quadratically, so the recursion terminates when the statement is true with margin.

PROVED (no open boxes anywhere):

    lam in [1/10, 1],  4 <= n <= 200,  4 <= D <= shore(lam):     47 boxes
    lam in [1, 10],    4 <= n <=  50,  4 <= D <= shore(lam):  1 325 boxes
    lam in [1, 30],    4 <= n <= 200,  4 <= D <= shore(lam): 12 929 boxes

so knife 4 is proved for lam in [1/10, 30], n up to 200, D up to the shore.

The shore bound is exact per box: T_hat <= T_k for every k and each T_k increases
in lam, so min_k T_k(lam_hi) is a rational majorant valid on the whole box.

TWO WRONG METHODS, recorded rather than deleted:
* naive per-monomial interval arithmetic -- the dependency problem makes the
  enclosure useless here (103 monomials, heavy cancellation); it never closed a
  single region;
* "all coefficients non-negative after shifting to the corner" -- far too strong
  a test, it failed even on tiny boxes where the polynomial is obviously positive.
  The correct crude bound is c_0 plus the sum of negative coefficients; Bernstein
  is sharper still and closed n in [4,12], D in [4,24], lam in [1,2] in ONE box.

AND ONE WRONG DOMAIN: the first Bernstein run left 739 boxes open, all of them in
a slab ABOVE the shore (D = 191 at lam = 10, where the shore is 187.5), because I
had used the crude majorant 18.93 lam + 5. With the exact per-box shore bound the
same region closes completely. Third time this night that a wrong domain produced
a fake problem.

WHAT REMAINS for knife 4: lam > 30 and n > 200. Runs are in progress at
(n <= 400, lam <= 60) and (n <= 1000, lam <= 120); beyond them the two asymptotic
statements take over (n -> infinity at fixed lam, D has leading coefficient +280;
lam -> infinity is the scaling form with the tangency approached from the safe
side). Joining those to the box with explicit thresholds is the last gap.

## 2026-08-18 10:23 -- knife 4 proved up to lam = 60, n = 400

    lam in [1/10, 1],  n <= 200:      47 boxes, 0 open
    lam in [1, 10],    n <=  50:   1 325 boxes, 0 open
    lam in [1, 30],    n <= 200:  12 929 boxes, 0 open  (456 s)
    lam in [1, 60],    n <= 400:  39 970 boxes, 0 open  (1853 s)

so knife 4 is now PROVED on lam in [1/10, 60], 4 <= n <= 400, 4 <= D <= shore.

The cost grows the way the difficulty does: the box count roughly triples when
lam doubles, because the margin at the shore thins from 1.010 at lam = 26 to
1.0042 at lam = 60 and the subdivision has to follow it. That is visible directly
in article/visuals/proof-in-3d.png, where brick size IS local difficulty: coarse
bricks in the open, a fine dust along the shore.

Running: lam <= 120, n <= 1000. Beyond it the two asymptotic statements take over.

## 2026-08-18 10:40 -- E_2t DERIVED, not fitted: the weakest link in the chain is closed

Until now the central factorial polynomials were guessed from data and verified.
That was the most vulnerable point for publication -- verification is not
derivation, and it is the first thing a referee would ask about. It is now
derived from the definition:

1. The generating product is prod_{k=1}^{n-1} (1 + (n-2k) x)^2. The set
   {n-2k} is symmetric about zero, so in y = x^2 it is prod_{a>0} (1-a^2 y)^2
   with a = n-2, n-4, ... (verified directly against the integer sequence at
   n = 7, 8, 11, 12).
2. The power sums p_r = SUM_a a^{2r} have Faulhaber closed forms, and -- this is
   the structural point -- the odd-n and even-n formulas are THE SAME polynomial
   in n (checked for r = 1, 2, 3). That is why E_2t never depended on parity, a
   fact previously only observed.
3. Newton's identities turn the p_r into the elementary symmetric functions s_r.
4. E_2t is then a coefficient of (SUM_r (-1)^r s_r y^r)^2.

Carried out to t = 6, giving E_2, E_4, E_6, E_8, E_10 and the new E_12, each
verified against the exact integer sequence on both parities for n up to 39:
ZERO mismatches. E_12 also unlocks knife 7 for the closed form.

Effect on the programme: the chain from the CHR family to the knife condition is
now a derivation end to end -- Beta reduction, Jacobi normal form (4500 checks),
Saalschutz moments (432 checks), the moment recursion R_t (verified per knife),
and now E_2t. Nothing in it is fitted.

## 2026-08-18 11:00 -- the uniform-in-j route via a recursion is CLOSED, and a fake fit caught

The founder's point, and he is right: finishing knives one at a time is the trap
we already named, and the real target is a statement uniform in j. The natural
handle would be a linear recursion in j -- then positivity for all j follows by
induction from the first cases. Tested and it does not exist in usable form.

* K_j / K_{j-1} is NOT a rational function of j (no low-degree fit at three
  different (n, lam, D)), so the sequence is not hypergeometric and there is no
  first-order recursion.
* An honest search for sum_r c_r(j) K_{j+r} = 0 with order <= 3 and coefficient
  degree <= 3, fitted on a subset and VERIFIED ON HELD-OUT j: nothing survives.

NEAR-MISS WORTH RECORDING. The first search reported a recursion of order 4 with
degree-4 coefficients, "verified on j = 2..21". It was an artefact: 25 unknowns
against 21 equations, i.e. underdetermined, so the solver fitted all the data and
the verification was circular. The tell was the size of the coefficients
(hundreds of digits) -- a structural recursion does not look like that. The fix
is the standard one and is now the rule: fewer unknowns than fitting equations,
and always verify on held-out values.

WHERE THAT LEAVES THE UNIFORM PROBLEM. The scaling limit gives the mechanism for
every j at once, but only at leading order and at fixed j. A recursion in j is
now excluded at low order. What is left to try: creative telescoping in the
variable (t, j) at higher order, a generating function in j, or an argument
that bounds the whole family by the two extreme knives rather than treating them
separately.

## 2026-08-18 11:16 -- THE UNIFORM STATEMENT, and it reduces the whole family to TWO knives

After three routes to a uniform-in-j theorem were closed today, a fourth one
worked, and it is the one the founder pushed for: a single statement instead of a
family of them.

THE STRUCTURE:

  * ENDPOINT m = 0 (knife j = n) is positive AUTOMATICALLY, with no condition on
    D at all: c_0 = INT F u^alpha (1-u)^beta du with F >= 0 and the weight
    positive. Verified 64 of 64 as a sanity check, but it is a one-line argument.
  * ENDPOINT m = n-2 (knife j = 2) is exactly the shore condition D < T_n(lam),
    which is the PUBLISHED shore paper.
  * MEASURED: for n >= 14 the minimum of the coefficient sequence over m is
    always attained at one of those two endpoints. Zero violations over n = 14..60
    (46 configurations per level, eight lam from 1/10 to 80, seven D below the
    shore). The eight violations found at all are at n = 6 and n = 8 only.
  * MEASURED: log-concavity c_m^2 >= c_(m-1) c_(m+1) holds for every n >= 24,
    zero violations. Log-concavity implies unimodality, which implies the minimum
    is at an endpoint -- so it is a sufficient mechanism for the statement above.

CONSEQUENCE. If "no interior minimum for n >= 14" is proved, then every knife of
every level follows from the two endpoints, one of which is trivial and the other
published. The infinite family collapses to two cases. Small levels (n <= 12) are
a finite set already covered by the 525,346 certified knives.

WHAT IS NOW THE SINGLE OPEN LEMMA:

    for n >= 14, the sequence (-1)^m c_m has no interior local minimum
    (sufficient: it is log-concave, which is measured to hold for n >= 24)

That is a classical kind of statement: log-concavity of a coefficient sequence
follows from real-rootedness of the generating polynomial by Newton's
inequalities. So the target is now named and standard, rather than open-ended.

A false start worth recording: I first tested log-CONVEXITY, which fails
everywhere -- the profiles rise then fall, so the property that matters is
concavity. Checking the wrong direction cost one run.

## 2026-08-18 11:19 -- three mechanisms for the single lemma, all excluded

The lemma left standing is: for n >= 14 the coefficient sequence has no interior
minimum (sufficient: log-concavity, measured to hold for n >= 24). Three standard
mechanisms were tried today and none of them supplies it.

1. REAL-ROOTEDNESS. If the generating polynomial SUM_m c_m x^m had only real
   roots, Newton's inequalities would give log-concavity for free. It does not:
   certified roots show ALL roots complex, at every level tested (n = 14, 18, 24,
   30, 40; degree 12 to 38; zero real roots in every case).
2. A CLOSED FORM FOR THE RATIO. Log-concavity is exactly "r_m = c_m/c_(m-1) is
   decreasing". The ratios ARE beautifully monotone -- e.g. at n = 24, lam = 1,
   D = 6 they run 1.909, 1.379, 1.180, ..., 0.174, 0.118, decreasing throughout,
   with nearly constant differences in the tail -- but no rational function of m
   of degree <= 3/3 reproduces them (fitted on a subset, checked on held-out m).
3. LOG-CONVEXITY. Fails everywhere; it was the wrong direction to begin with,
   since the profiles rise and then fall.

So the lemma is empirically very solid and mechanically unexplained. What is left
to try, in order of promise: total positivity of the underlying moment matrix
(log-concavity would follow from a 2x2 minor condition); a direct positive
representation of c_m^2 - c_(m-1) c_(m+1) as an integral; or the observation that
the ratio's tail is almost linear in m, which suggests an asymptotic argument for
large m plus a finite check for small m.

Status of the day, stated plainly: the grand theorem was NOT proved. What changed
is its shape -- from an infinite family with no uniform handle to a single lemma
with two trivial endpoints, plus a list of mechanisms that are now ruled out.

## 2026-08-18 11:32 -- two more mechanisms for the lemma closed (total positivity, Newton via F)

* KARLIN / TOTAL POSITIVITY. If the kernel (-1)^m P_m^(alpha,beta)(1-2u) were
  TP2, the basic composition formula would make the Jacobi coefficients of ANY
  positive measure log-concave. It is not: 37 to 47 percent of the 2x2 minors are
  negative (51,480 tested at each of D = 6, 11, 23). In hindsight it had to fail,
  since it would prove far more than is true.
* STIELTJES MOMENTS. Such sequences are log-CONVEX by Cauchy-Schwarz, the
  opposite of what we see, so C_m is not one and the Hankel route is closed.
* NEWTON VIA F. C_m is an integral of F^(m) against a weight concentrating at
  u = 1/2, and F is real-rooted, so its Taylor coefficients there are log-concave
  (verified, zero violations). But C_m does not track them: signs agree on only
  4-9 of 23 indices, because F^(m) oscillates and the integral averages it.

Five mechanisms for the single lemma are now excluded. The lemma itself remains
solid empirically (no interior minimum for every n >= 14, log-concave for every
n >= 24) and unexplained. A self-contained brief for outside help is in
docs/BRIEF_FOR_OUTSIDE_HELP.md, with all ten dead ends listed so they are not
retried and five untried directions named.

## 2026-08-18 11:34 -- the asymptotic route needs a real derivation, not a fit

Log-concavity is exactly "r_m = C_m/C_(m-1) is decreasing". The differences of
r_m are negative everywhere and behave very regularly: about -0.51, -0.18, -0.10,
-0.069, -0.052 at the head, decaying like 1/m^2, and settling to a nearly
constant -0.023 in the tail (n = 60, lam = 1, D = 6).

That suggests the shape r_m = a + b/m + c m, which would give log-concavity
outright, since its derivative -b/m^2 + c is negative identically when b > 0 and
c < 0. Fitted on the first half and checked on the HELD-OUT second half:

    n = 40, lam = 1 : held-out error 28 percent of scale
    n = 60, lam = 1 : 33 percent
    n = 40, lam = 7 : 2.9 percent

So the shape is a decent approximation, better at larger lam, but NOT the true
form. A fit cannot close this; what is needed is a genuine asymptotic evaluation
of C_m for large m -- steepest descent on
C_m proportional to INT F^(m)(u) u^(alpha+m) (1-u)^(beta+m) du, whose weight
concentrates near u = 1/2 while F^(m) oscillates. That is a well-defined piece of
work rather than a search, and it is the honest next step on this route.

STATE OF THE LEMMA at the end of the day: empirically solid (no interior minimum
for every n >= 14, log-concave for every n >= 24, across hundreds of
configurations), and six mechanisms excluded -- real-rootedness, closed-form
ratio, log-convexity, total positivity, Stieltjes moments, Newton via F. The
brief for outside help lists all of them so the search is not repeated.

## 2026-08-18 11:44 -- THE SADDLE ROUTE WORKS: the lemma becomes "the saddle moves right"

The steepest-descent analysis was carried out and, unlike the five earlier
mechanisms, it holds up against exact values.

SETUP. Rodrigues plus Cauchy turn the coefficient into a double integral whose
exponent is large in both variables (the m! from Rodrigues cancels the m! from
Cauchy):

    C_m = const * (1/2 pi i) CONTOUR INT F(z) u^(m+alpha) (1-u)^(m+beta)
                                     / (z-u)^(m+1)  du dz
    Phi(u,z) = log F(z) + (m+alpha) log u + (m+beta) log(1-u) - (m+1) log(z-u)

Saddle equations:

    1/u - 1/(1-u) + 1/(z-u) = 0
    L(z) = m/(z-u),      L(z) = F'(z)/F(z) = sum_a 2/(z-r_a) + eps/z

VERIFIED. The saddle is real and moves smoothly; Newton needs continuation in m
(a cold start converges only near the top of the range). Including the Gaussian
prefactor 1/sqrt(det Hessian), the predicted log r_m matches the EXACT rational
value to 0.05 at m = 6 and to 0.0007-0.003 for m >= 18, at n = 40 and 60.

THE REDUCTION. By the envelope theorem d(log C_m)/dm = G(u*,z*) with
G = log[u(1-u)/(z-u)]. Differentiating the saddle equations and substituting the
FIRST of them (which says 1/u - 1/(1-u) = -1/(z-u)) collapses almost everything:

    dG/dm = - z' / (z - u)

and z - u > 0 on the whole path. So, since log-concavity is exactly "G
decreasing":

    LOG-CONCAVITY  <=>  z'(m) > 0,  the saddle point z moves RIGHT as m grows.

Explicitly, differentiating the pair gives

    z' = 1 / [ (z-u) ( L'(z) + m (1 - kappa) / (z-u)^2 ) ],
    kappa = 1 / [ A (z-u)^2 ],   A = 1/(z-u)^2 - 1/u^2 - 1/(1-u)^2

VERIFIED: this closed formula for z' matches the numerical derivative of the
saddle path to 3-4 digits, and the identity dG/dm = -z'/(z-u) likewise, at
n = 40 and 60, lam = 1 and 7. And z' > 0 at every point computed (z runs from
1.002 to 1.645 at n = 40, from 1.001 to 2.100 at n = 60).

WHAT REMAINS. Prove L'(z) + m(1-kappa)/(z-u)^2 > 0 along the saddle path. L' is
explicit and negative (a sum of -2/(z-r_a)^2), so the content is that the
m-term beats it. That is a concrete inequality about an explicit expression --
the first time this lemma has had that form.

## ERR-0005 (2026-08-18 11:49) -- the endpoint lemma is FALSE. Counterexample confirmed.

WHAT I CLAIMED (today, hours ago): that for n >= 14 the minimum of the sequence
C_m is always at an endpoint, so the whole knife family reduces to two cases; and
that log-concavity holds for n >= 24. I called it "the uniform statement" and
recorded it as the sharpest form of the problem.

IT IS FALSE. An outside check produced a counterexample and my own exact engine
reproduces it digit for digit:

    n = 24, lam = 10, D = 177   (the shore is 187.541, so this is admissible)
    C_m/C_0: 1.000000, 0.568188, 0.470609, ..., 0.308001, 0.305587, 0.312789, ...
    global minimum at m = 10, strictly interior
    log-concavity violated at m = 1..16, e.g. C_0 C_2 / C_1^2 = 1.4577

A second one also confirmed: n = 14, lam = 2, D = 39 (shore 39.4), interior local
minimum at m = 8.

WHY I MISSED IT -- the mechanism, which matters more than the fact. My D-grids
were ABSOLUTE: 4, 5, 7, 11, 19, 35, 70. At lam = 10 the shore is 187.5, so every
test I ran there sat below 40 percent of the shore, and the counterexample lives
at 94 percent of it. I varied D, so my own rule "vary every parameter" was
formally satisfied -- but the parameter that matters is D RELATIVE TO THE SHORE,
and on that scale I never left the deep interior at large lam. A grid that looks
wide in absolute terms can be systematically blind.

NEW RULE, added to the scientist skill: when a region has a moving boundary,
sample RELATIVE to that boundary (fractions of the shore), never on an absolute
grid.

WHAT DIES WITH IT:
* the endpoint-minimum lemma and everything built on it;
* log-concavity of C_m;
* today's saddle-point reduction "log-concavity <=> z' > 0". The machinery itself
  reproduces the exact ratios to 0.003 at n = 40, but at the counterexample it
  reports z' > 0 everywhere while log-concavity actually fails by 3 percent --
  i.e. the asymptotics does not resolve the term that decides the question. An
  asymptotic proof there would have been a proof of a false statement.

WHAT SURVIVES, and it is most of the work:
* every C_m in BOTH counterexamples is still POSITIVE -- the physics claim is
  untouched;
* the Jacobi normal form, the closed forms per knife, the Saalschutz moments, the
  scaling limit and the parity mechanism, the knife-4 box proof -- all of these
  are statements about SIGNS, and signs do not depend on the normalisation.

ALSO CORRECTED, from the same outside check:
* My C_m are RAW integrals, not Jacobi expansion coefficients: the true
  coefficient is I_m / h_m with an m-dependent h_m (DLMF 18.18.1). Signs are
  unaffected, but any statement about log-concavity or the location of the
  minimum is normalisation-dependent, and I had not said which normalisation I
  meant. That alone made the lemma ill-posed.
* Strict positivity ON the shore is impossible: at D = T_k(lam) with k the
  minimising level, that coefficient VANISHES (verified exactly: 0 at lam = 1 and
  lam = 2). The correct statement is D < shore implies C_m > 0, and D = shore
  implies C_m >= 0.

## 2026-08-24 17:08 -- ERR-0013: the odd-depth jam was a FALSE STATEMENT, not cancellation; window refuted, repair route found

Session goal was the odd-depth blocker (depths 3, 5) per HANDOVER.md. The
recorded plan -- factorisation first, then SOS in the Jacobi basis -- died in
its first hour, and what it died of rewrote the problem.

1. FACTORISATION PROBE (`lab/odd_depth_factor.py`,
   `results/odd_depth_factor.json`). H factors at every depth as
   (linear-in-K factors) x (one irreducible core); the core carries the full
   corner margin unchanged (7.86e-05 at depth 3). Route as imagined: dead.
   But the probe measured margins ACROSS depths at the same corner:
   2.2e-3 / 7.8e-5 / 3.1e-6 / 1.1e-7 for depths 2 / 3 / 4 / 5. Monotone in
   depth, NO parity structure. Depth 4 is 25x worse-conditioned than depth 3
   and certifies in 1369 boxes. The cancellation diagnosis could not be the
   even/odd discriminator.

2. ZERO HUNT. Odd depths have real zeros in v bracketing the window (even
   depths: none anywhere in [0.5, 4]) -- the margin law's thresholds (even
   j = d+1 must have one). Following the zero surface: at c = 2/3 it
   converges to v = 2 with clearance exactly ~ 1/K, and the K->infinity
   leading form P_A VANISHES at (c=2/3, v=2). Then the decisive find: P_A
   changes SIGN along both window edges in a c-band my own morning grid had
   stepped over (ERR-0005, third occurrence, this time against me
   within the same session).

3. REFUTATION (`lab/odd_depth_window_refuted.py`,
   `results/odd_depth_window_refuted.json`). The step-(a) fixed-window
   statement is FALSE at odd depths. Six exact witnesses inside the certified
   box, EACH confirmed by build_branch and the exact reference engine
   independently: smallest is depth 3, K=54 (n=109), c=239/400, v=2, knife
   negative; depth 5 from K=111. The Bernstein runs never jammed -- they
   correctly refused to prove a false claim, for three sessions, while the
   diagnosis blamed their arithmetic. Z3's `unknown` was the honest answer.

4. PHYSICS INTACT. At every witness point the knife is POSITIVE at the true
   shore T_hat (integer argmin), both engines. The falsity is pure method
   overshoot -- the ERR-0010 mechanism again: at odd depths, T_{v*lam} for v
   away from the argmin ratio overshoots the threshold once lam is large.

5. WHAT DIES: fixed-window step (a) at all odd depths; the SOS route AS AIMED
   AT THAT STATEMENT (a basis change cannot rescue a false inequality); the
   keystone property "one window, every depth". WHAT SURVIVES: even-depth
   certificates 2/4/6 (thresholdless knives -- true statements, honestly
   certified), step (b) as proved, step (c), and the physical claim.

6. REPAIR ROUTE, concrete. Measured: the positivity room around the integer
   argmin is ~sqrt(lam) in k-units (16 at lam=72, 261 at lam=3600) -- the
   needed width is 2. So the true odd-depth statement is positivity on a
   FIXED-width k-window around the critical level k*(lam). The critical curve
   dT/dk = 0 is quadratic in lam with discriminant
   3 k^2 (k-2)^2 (4k^2 - 12k + 3): non-square part QUADRATIC, so the curve is
   a conic with rational point (k, w) = (3, 3) -- explicitly rationally
   parametrizable. Substituting lam = lam(t), k = k(t) + delta,
   delta in [-3/2, 3/2] makes the odd-depth claim polynomial in (t, delta, K):
   the existing Bernstein pipeline applies. Derivation is the next iteration.

Checkpoint (research-loop format):
RESULT: odd-depth diagnosis overturned; fixed-window step (a) refuted at odd
  depths with exact two-engine witnesses; physics verified intact at those
  points; rational-conic repair route established.
EVIDENCE: results/odd_depth_factor.json, results/odd_depth_margin_scan.json,
  results/odd_depth_window_refuted.json; corrections appended to
  ODD_DEPTH_DIAGNOSIS.md and UNGLUED_KEYSTONE.md; ERR-0013.
STATUS: refutation = experimentally-supported (exact witnesses, two engines);
  repair route = speculative until derived.
NOVELTY: internal to the project (method repair), NOVELTY_UNCHECKED.
TIME: predicted UNKNOWN (calibration slice); actual ~2h agent time.
LEARNED: (a) a diagnosis must vary the discriminating variable -- margins were
  never compared across depths before blaming cancellation; (b) grid blindness
  now three occurrences: clean-region claims need optimizer-driven hunts of
  the complement, not denser grids; (c) "certificate fails to converge" has
  TWO hypotheses, and "the statement is false" must be tested before "the
  method is weak".
NEXT: derive the rational parametrization of the conic dT/dk = 0 explicitly,
  build H in (t, delta, K) coordinates from the validated build_branch by
  substitution (ERR-0012 discipline: substitute, never re-derive), self-check
  against the reference engine including points where the reference is
  negative, then Bernstein depth 3.

## 2026-08-26 09:45 -- DEPTH 3 CLOSED: the repaired odd-depth statement is CERTIFIED

The k-window form of step (a) -- the ERR-0013 repair -- is now a theorem-grade
certificate at depth 3, and the road there taught two more lessons.

1. THE CONSTRUCTION. G = A + B*w in (K, k, delta, w), w^2 = 12k^2-36k+9,
   built by pure substitution from the validated build_branch (nothing
   re-derived, ERR-0012 discipline), self-checked at rational points of the
   conic dT/dk = 0 against the exact reference engine: 296 trials per depth,
   0 mismatches, 21/14 genuinely negative reference signs (non-vacuous),
   depths 3 AND 5. Artifact: results/odd_depth_kwindow_selfcheck.json.

2. TWO JAMS, BOTH INSTRUCTIVE.
   a) delta-window slack: the first runs used |delta| <= 3/2 "for safety";
      all 156+58 open boxes sat at delta in [1.31, 1.5] -- slack the argument
      never needed (step (b) gives |argmin - k*| < 1 strictly). Narrowed to
      9/8 with a 1/8 margin.
   b) The remaining open boxes crowded the corner where K and k grow
      TOGETHER, with A, B, G all POSITIVE there and G/max(|A|,|Bw|) ~ 1:
      not cancellation of the object, degeneration of the Bernstein
      coefficients at a double face -- the UNGLUED two-variable degeneration,
      third appearance. Same cure: rho = k/(2K) makes the corner an ordinary
      point. Piece 1 (rho >= 2, an exponent remap) closed in ONE box; piece 2
      (rho <= 2, wedge K = (6+rho z)/rho) in 11 boxes.

3. THE RESULT. Depth 3, BOTH parities: proved, 1 + 11 boxes each, 0 open,
   ~2.5 min per parity, coverage ALL K >= 3 and ALL k >= 12 (both infinities
   compactified -- the old "finite in K" caveat is GONE for this piece).
   delta in [-9/8, 9/8]; lam*(12) < 7 overlaps the fixed-k_s band below.
   Artifact: results/odd_depth_kwindow_cert_d3.json (stamp bbe7b04, clean).
   Depth 5 is running now with the same machinery.

4. WHAT REMAINS for the full odd-depth chain: depth 5 run (in progress);
   the lam in [5/2, 7] band at odd depths currently rests on the measured
   fixed-k_s = 8 trials (1085, 0 negatives) -- needs its own 2-variable
   certificate; unimodality of dT/dk on the window is still measured, not
   proved; and step (c) monotonicity is certified at depths 2-6 as before.

Checkpoint:
RESULT: repaired step (a) certified at depth 3, both parities, full range.
EVIDENCE: odd_depth_kwindow_cert_d3.json, odd_depth_kwindow_selfcheck.json.
STATUS: experimentally-supported (exact Bernstein certificate; premises:
  measured unimodality for step (b), measured k_s=8 band).
NOVELTY: internal repair; the rho-degeneration lesson is a reusable rule.
TIME: predicted UNKNOWN (calibration), actual ~3h agent time from constructor
  to certificate, of which ~2h went to the two wrong window/coordinate
  configurations.
LEARNED: slack you do not need is surface you cannot defend; a jammed
  certificate points either at a false statement (ERR-0013) or at the wrong
  coordinates (this entry) -- measure WHICH before adding compute.
NEXT: depth 5 with the same two pieces; then the odd-depth lam in [5/2,7]
  band certificate.

## 2026-08-26 13:45 -- ODD-DEPTH CHAIN CLOSED: three certificates in one day

The ERR-0013 repair is complete for both odd depths. Everything the chain
needed below and above lam = 7 is now a Bernstein certificate, not a
measurement.

1. DEPTH 5 k-WINDOW (results/odd_depth_kwindow_cert_d5.json). Same two
   rho-pieces as depth 3: piece1 in ONE box, piece2 in 11, per parity,
   0 open, covering ALL K >= 3 and ALL k >= 12, delta in [-9/8, 9/8].
   Getting there took infrastructure the environment forced on us: the
   container kills background processes every few minutes, so the certifier
   grew G/Gw caches keyed by the constructor's sha256 (a stale cache is the
   ERR-0011 shape), per-piece frontier checkpoints with resume, fmpq_mat
   matrix engines for grids and de Casteljau splits (6-8x), and an in-place
   accumulation fix in the constructor (the quadratic `total = total + term`
   was 40% of the depth-5 odd build). Every change was regression-gated on
   depth 3's exact box counts (1 + 11) and the 296-trial self-check.

2. THE lam IN [5/2, 7] BAND (results/odd_depth_band_cert.json). The k_s = 8
   band -- until now 1085 measured trials -- certified for depths 3 and 5:
   build_small_lam (the validated k_s = 4 code path) at KS_SMALL = 8,
   self-checked non-vacuously (22/24 negative refs outside the band),
   11 boxes per parity per depth.

3. UNIMODALITY -> CONVEXITY (results/unimodality_cert.json). Step (b)'s
   bracketing theorem needed "dT/dk changes sign once on the window",
   previously a 400-point sweep. Certified strictly stronger: T'' * U^3 > 0
   on k in [8/5 lam, 2 lam], lam >= 7 -- ONE box. Cross-checked by exact
   VALUE equality against an independent fmpq_poly quotient-rule route;
   probes at k < 2, where T is genuinely concave, keep the check honest.

STATE OF THE ODD DEPTHS, honestly. Depths 3 and 5 now rest on certificates
for: step (a) in k-window form (all K, all k on the curve, |delta| <= 9/8),
the integer argmin inside the delta window (coefficient-sign pairs, lam >= 7,
with unimodality now certified), the [5/2, 7] band at k_s = 8, the small-lam
piece at k_s = 4 (from keystone_unglued), and step (c) monotonicity
(certified at depths 2-6 earlier). Still measured anywhere in the chain:
the k_s = 4 piece's lam <= 5/2 region uses keystone_unglued's certified
small piece -- certificate; nothing else at these depths. Depth 7+ remains
open (the machinery now exists end to end).

Checkpoint:
RESULT: odd depths 3 and 5 fully certificate-backed; three new artifacts.
EVIDENCE: odd_depth_kwindow_cert_d5.json, odd_depth_band_cert.json,
  unimodality_cert.json (+ d3 regenerated on the final code).
STATUS: experimentally-supported, gates passed; no self-approval beyond that.
NOVELTY: internal to the programme; the rho-coordinate cure and the
  convexity reduction are reusable rules.
TIME: the odd-depth repair, ERR-0013 to closed chain: ~2 days of sessions;
  this closing day ~5h agent time, half of it environment survivability.
LEARNED: an environment that kills processes is a constraint to engineer
  around (cache + checkpoint + resume beats hoping), and every speed or
  robustness change to proof code must be regression-gated on exact
  certificate outputs, not on "it still runs".
NEXT: depth 7 with the same pipeline as a uniformity test of the machinery;
  then the j-infinity question (one argument for all depths) with the
  k-window form as the base case shape.

## 2026-08-28 12:07 -- OUTSIDE REPORT TESTED THE SAME DAY: one route killed exactly, one route promoted

An outside AI report (research/reading-notes/keystone-outside-report-2026-08-28.pdf,
produced from our BRIEF_KEYSTONE_FOR_OUTSIDE_HELP.md) proposed reorganizing the
exact closed sum into an alternating binomial transform
K_r = SUM_t (-1)^t C(r,t) M_t^(r), r = j-1, with a normalized sequence
M_t^(r) = t! (H-r)_t E_{2t}(n) / [s^{2t} (n-1)_t (n-3/2)_t], H = (D+4n-7)/2,
an exact depth recursion M_t^(r+1) = (1 - t/(H-r)) M_t^(r), a
Hausdorff-moment hypothesis (M_t moments of a positive measure on [0,1],
which would explain the parity law instantly), and a depth kernel
B_{r,t} = C(r,t)(H-r)_t t! with provably positive adjacent 2x2 minors.
All four claims were tested exactly within hours (lab/moment_kernel_probe.py,
results/moment_kernel_probe.json):

1. NORMALIZATION CONFIRMED -- with a correction. The report's own page-7
   display has R_t inverted relative to the repository's closed form; deriving
   from the repository formula, the reconstruction matches the exact reference
   engine on 450/450 sign trials including 15 genuinely negative references.

2. DEPTH RECURSION CONFIRMED EXACTLY: 0 violations across depths 2..6,
   lam in {3, 50}, n in {12, 30}. This affine one-step structure is real.

3. NAIVE MOMENT HYPOTHESIS KILLED, with structure. At lam = 3 the truncated
   Hankel minors go NEGATIVE at and below the shore for j = 6, 7, 8 (exact
   rationals, e.g. H0 2nd minor < 0 at lam=3, j=6, n=12, D=T_hat) -- so
   "M_t are moments of a positive measure on [0,1] throughout the physical
   region" is FALSE as stated. The failures concentrate at small lam and
   small n: at lam = 72 and 650/3 with n = 40 every tested minor is
   nonnegative, consistent with the scaling collapse M_t -> x^t. The route
   died exactly as designed ("it can fail quickly and exactly"); any revival
   must target a modified representation, not this one.

4. KERNEL TOTAL-POSITIVITY PROMOTED. All 27 solid q x q minors (q = 2, 3, 4)
   of the depth kernel B_{r,t}, computed symbolically in H, factor COMPLETELY
   into positive integer constants times products of linear factors (H - c)
   with integer c <= 2 r_max - 1. Since H - (2r-1) >= (D-1)/2 > 0 on the
   physical domain (r <= n-2), every tested solid minor is strictly positive
   there: the depth kernel looks totally positive on the physical region,
   now as a precise factorization conjecture with explicit integer roots --
   a theorem candidate, not an analogy. (TP alone does not close the theorem:
   the input carries (-1)^t; per the report this needs pairing with structure
   of the M-sequence.)

Checkpoint:
RESULT: exact reorganization verified; naive measure route refuted with exact
  counterexamples; kernel minor factorization promoted to theorem candidate.
EVIDENCE: results/moment_kernel_probe.json (450 sign trials, recursion checks,
  Hankel tables, 27 symbolic factorizations).
STATUS: reorganization + recursion: verified identities. Measure hypothesis:
  refuted as stated. Kernel factorization: measured pattern, unproved.
NOVELTY: the depth-index kernel structure was not previously explored here;
  outside literature pointers (Mansfield 2502.20372, Koornwinder, Hahn class,
  Curto-Fialkow) recorded in the report.
TIME: report analysis to banked verdicts: ~1.5h agent time.
LEARNED: the outside-brief loop works -- a fresh reorganization suggested by
  an external reader produced one exact kill and one new theorem candidate in
  a single session; the brief's dead-routes list successfully prevented
  rehashing.
NEXT: (a) conjecture and prove the explicit minor factorization of B (roots
  look like consecutive integers tied to 2r-1); (b) probe what replaces the
  naive measure at small lam -- e.g. signed measure with controlled negative
  part, or a different normalization absorbing (H-r)_t differently; depth-7
  certificate continues in parallel.

## 2026-08-28 13:05 -- KERNEL MINOR LAW: a double-Vandermonde closed form, 86/86

Following the same-day probe, the depth-kernel minor factorization is now a
precise conjecture (results/kernel_minor_law.json): the solid q x q minor of
B_{r,t} = C(r,t)(H-r)_t t! (rows r0..r0+q-1, cols t0..t0+q-1) equals

    (positive integer) * prod_{a=0}^{q-1} (H-r0-a)_{t0}
                       * prod_{0<=a<b<=q-1} (H - 2r0 - a - b),

verified in exact symbolic arithmetic on 86/86 cases (q <= 5, r0 <= 12,
t0 <= 3; the multiplicity of root 2r0+s is the number of index pairs a < b
with a+b = s). Two wrong guesses (a t0-shifted trapezoid, then an unshifted
trapezoid) were killed by the exact sweep before this form; the pair-count
multiplicity pattern is what identified the product structure. Max root is
exactly 2 r_max - 1 < H on the whole physical domain, so PROVING this one
determinant identity proves the depth kernel totally positive there. The
shape (binomial times falling-factorial kernel, Vandermonde-type product)
points at Lindstrom-Gessel-Viennot / known binomial determinant identities.
NEXT: prove the identity (row operations reducing to a pure binomial
determinant, or LGV paths), then attack what TP + the exact affine depth
recursion M_t^(r+1) = (1-t/(H-r)) M_t^(r) yield jointly for K_r >= 0.

## 2026-08-28 13:30 -- THEOREM: the depth kernel is strictly totally positive

The 86-case law of the morning is now a PROVED identity with a two-line
mechanism (full proof: results/KERNEL_TP_THEOREM.md; machine verification
including the constant: results/kernel_minor_identity.json, 86/86 exact
polynomial comparisons):

    det[B_{r0+a,t0+b}] = prod_a (H-r0-a)_{t0} * prod_a (r0+a)_{t0}
                         * prod_{a<b}(b-a) * prod_{a<b}(H-2r0-a-b).

Mechanism: the paired roots t0+i and H-t0-i of each column factor are
symmetric about H/2, so ONE quadratic substitution z = y^2 - Hy (y the row
variable) makes every column a monic polynomial in z of degree u -- a
generalized Vandermonde -- and z_b - z_a = -(b-a)(H - y_a - y_b) delivers
the product law, signs cancelling exactly. Corollary: every solid minor of
the depth kernel is strictly positive on the physical domain (all roots
<= 2 r_max - 1 < H there): STRICT TOTAL POSITIVITY of the depth kernel, as
a theorem. This is the first uniform-in-depth structural theorem of the
programme -- it holds for ALL r, i.e. all knife orders at once.

What it does not yet give: K_r >= 0, because the knife input carries the
alternating weight; TP must be paired with structure of M_t^(r) (naive
positive measure refuted at small lam earlier today). The exact affine
recursion M_t^(r+1) = (1 - t/(H-r)) M_t^(r) plus this kernel theorem is now
the sharpest coherent toolset the depth direction has ever had.

RESULT: first all-depths theorem (kernel TP) proved and machine-verified.
EVIDENCE: KERNEL_TP_THEOREM.md, kernel_minor_identity.json,
  kernel_minor_law.json (the discovery trail with its two dead guesses).
STATUS: proved identity (elementary, self-contained) + exact verification.
NOVELTY: NOVELTY_UNCHECKED as literature (binomial-determinant identities
  are a classical genre; the specific pairing with this kernel and domain
  is ours). LITERATURE task queued before any external claim.
TIME: conjecture to proved theorem: ~4 hours within one session.
NEXT: (a) literature check of the identity family before any novelty
  wording; (b) pair TP + affine recursion against K_r: e.g. characterize
  the cone of sequences M with K_r >= 0 for all r under the recursion.

## 2026-08-28 15:05 -- Depth 7: measured compute wall in this environment, stated honestly

Depth 7 is NOT closed. Its certificate is compute-bound here, with numbers
rather than impressions (all measured today):

* piece-1 polynomials at depth 7 have degrees (131, 118, 21) after
  compactification -> Bernstein root grids of 345 576 exact rationals each
  (~350 MB serialized per grid, A and B).
* one de Casteljau split of such a grid along the widest axis: 19 s; a box
  therefore costs ~38 s (A and B), and restoring a frontier box at tree
  depth 6 costs ~230 s of splits.
* the container kills long processes after roughly 180 s, so a restart
  cannot even rebuild one frontier box before dying: banked progress stands
  at 24 boxes, 0 open, 15 pending, and does not advance.

Infrastructure built while establishing this (all committed, all regression-
gated on depth 3's exact 1 + 11 box counts): constructor build checkpoints,
caches for G, the wedge polynomial Gw, the compactified A/B pairs and the
root grids, frontier checkpoints, and frontier restore by split-tree descent
with shared prefixes. Depths 2-6 remain fully certified; depth 7 was always
a uniformity TEST of the machinery, not a link in the chain, so nothing in
the proved statements depends on it.

What would unblock it, in order of cost: a machine that does not kill
processes (the run needs hours, not minutes); or splitting along the
cheapest axis (delta, degree 21: ~3 s per split instead of 19 s) at the cost
of more boxes; or a positivity test that does not carry full grids.

LEARNED: measure the unit cost before assuming an environment can be
engineered around. Five successive survivability layers each looked like
the last one needed; the arithmetic (230 s of restore vs a 180 s process
lifetime) settles it in one line and should have been done first.

## 2026-08-28 15:40 -- CHARLIER REDUCTION: the depth index becomes a classical orthogonal family

The outside report's moment route is not dead -- it was aimed at the wrong
sequence, and the correction changes its character (all verified exactly,
results/charlier_reduction.json, results/base_moment_probe.json):

1. THE SPLIT (144 trials, 0 violations).  M_t^(r) = (H-r)_t * m_t with

       m_t = t! E_{2t}(n) / [ s^{2t} (n-1)_t (n-3/2)_t ],   s = lam+n-1,

   INDEPENDENT of both the depth r and the dimension D. Every trace of r
   in the reorganized knife sum is a single falling factorial. That is
   exactly why a fixed Hausdorff hypothesis for M_t^(r) was ill-posed: the
   sequence tested changes with r, this one does not.

2. THE CHARLIER FORM (45 recurrence trials, 0 violations; 108 sign trials
   against the reference engine, 0 mismatches, 8 negative references).
   With g = H - r,

       K_r = sum_t (-1)^t C(r,t) (g)_t m_t,
       P_r(y) := sum_t C(r,t) (g)_t (-y)^t  =  C_r(g ; 1/y),

   the CHARLIER polynomial (verified against the standard three-term
   recurrence). So a Hausdorff representation of m gives

       K_r = INT_0^1 C_r(H-r ; 1/y) dmu(y),

   turning all-depths positivity into a zero/positivity question for a
   classical orthogonal family IN THE DEPTH INDEX -- with a century of
   zero bounds available, uniform in r by construction. This is the first
   time the depth direction has landed on a named classical family.

3. THE REGIME, measured and sharp. m_t IS a Hausdorff moment sequence for
   t up to about n/2 and fails beyond; the boundary is INDEPENDENT of lam
   at every n tested, over five orders of magnitude (lam = 1/10 to 5000).
   The failure is therefore intrinsic to the central factorial numbers
   E_{2t}(n), not to the amplitude parameter. Concretely the clean range
   is tmax/n ~ 0.47-0.6 while the admissible range is t <= n-2, so as it
   stands the route covers knives with j-1 <~ n/2, not all j.

Checkpoint:
RESULT: exact split + Charlier identification + measured moment regime.
EVIDENCE: charlier_reduction.json, base_moment_probe.json.
STATUS: (1),(2) verified identities; (3) measured, lam-independence is a
  strong structural signal but not a proof.
NOVELTY: NOVELTY_UNCHECKED -- Charlier/2F0 identifications are classical;
  what is ours is the identification of THIS knife family's depth index
  with that structure.
TIME: ~40 min from the failed M-hypothesis to the corrected reduction.
LEARNED: when a hypothesis about a sequence fails, check first whether the
  sequence was even well-defined for the question -- here the tested object
  moved with the very index the hypothesis quantified over. Splitting off
  the r-dependence took one line and changed the verdict.
NEXT: (a) why does the moment property break at t ~ n/2? (the boundary is
  lam-free, so it is a statement about E_{2t}(n) alone -- likely provable);
  (b) for j-1 <~ n/2, push the Charlier route to an actual positivity
  statement via classical zero bounds (largest zero of C_r(.;a) vs g);
  (c) the complementary regime j-1 > n/2 has small m = n-j and may want a
  moment structure in m instead.

## 2026-08-28 16:05 -- The crude Charlier criterion is dead; the tightness is structural

I proposed a sufficient condition for the whole depth family and killed it
the same hour (results/charlier_zero_test.json). If m is a moment sequence
on [0, Y], then K_r = INT_0^Y P_r(y) dmu(y) with P_r = C_r(g;1/y), so
"P_r >= 0 on [0, Y]" would settle every depth at once. Measured exactly:

* max_t m_{t+1}/m_t is a LOWER bound on Y (the ratios increase to sup supp);
* the smallest positive zero of P_r, bracketed by exact rational bisection,
  sits at 0.63-1.06 times that lower bound;
* so P_r changes sign strictly INSIDE the support in 56 of 84 at-or-below-
  shore configurations, while the knives there are positive.

The route is dead as stated, and it had to be: at the shore the even knives
are marginal by construction (the shore IS their threshold), so no argument
comparing a support to a zero can decide them -- only one that uses where
the measure's MASS sits. That is a sharper description of the difficulty
than the project had before: the obstruction is not conditioning, not
coordinates, and not the depth index; it is that the true statement is
tight at the boundary, so every sufficient condition must be tight too.

RESULT: one more exact kill, with the margin quantified (0.63-1.06).
EVIDENCE: results/charlier_zero_test.json.
STATUS: refuted route, recorded; the Charlier reduction itself stands.
LEARNED: when a claim is marginal at its boundary by design, sufficient
  conditions that ignore the boundary geometry cannot close it -- test the
  margin ratio early, it costs minutes and predicts the outcome.
NEXT: use the mass, not the support: (a) get the actual measure for m in the
  regime where it exists (Hankel-based quadrature gives the atoms exactly),
  then evaluate INT P_r dmu directly as a check of the mechanism; (b) the
  complementary regime t > n/2 where m stops being a moment sequence.

## 2026-08-28 16:35 -- The moment "failure" is a harmless tail: the base sequence IS Hamburger

The t ~ n/2 breakdown of the base sequence turns out to be far weaker than
"m is not a moment sequence" (results/moment_boundary_law.json, fine sweep
n = 8..44 at lam = 3):

1. The ONLY condition that ever fails is H1 = [m_{a+b+1}], i.e. support in
   [0, infinity): 37 of 37 first failures, never H0, never the [0,1]
   localizer.
2. H0 = [m_{a+b}] is POSITIVE DEFINITE at full size N and N+1 (N = number of
   DISTINCT squares in the E-multiset, since k <-> n-k doubles every value).
   So m is a genuine Hamburger moment sequence, not a rank-deficient
   finite-atom one -- the natural first guess, and it is wrong.
3. The H1 failures are exponentially tiny in normalized terms: 7.5e-11 at
   n = 8 down to 1.7e-65 at n = 44, shrinking monotonically with n.

So the representing measure lives on (-infinity, 1] with an exponentially
small part at NEGATIVE y. And that part is HARMLESS for the knife:
P_r(y) = sum_t C(r,t)(g)_t(-y)^t has every term nonnegative for y <= 0
(because g = H - r > r on the physical domain), so mass at negative y
contributes POSITIVELY to K_r = INT P_r dmu.

The open question therefore narrows sharply: not the negative tail, not the
existence of the measure, but the MASS DISTRIBUTION on [0, Y] against the
sign changes of P_r -- which is exactly what the crude support test could
not see this morning.

RESULT: the moment structure survives in the form that matters; the defect
  is identified, quantified, and shown harmless.
EVIDENCE: results/moment_boundary_law.json (rank reports, first-failure
  families and magnitudes over n = 8..44).
STATUS: measured; the "harmless" step is a one-line proof (all terms of
  P_r are nonnegative at y <= 0 when g > r), the rest is measurement.
LEARNED: a failing test can fail in a direction that does not matter --
  check WHICH condition breaks and what its sign means for the target
  before discarding a route. This one looked dead twice today and is not.
NEXT: extract the measure's mass distribution (Jacobi matrix from the
  Hankel data gives nodes and weights exactly), then evaluate INT P_r dmu
  directly against the reference knife sign; that is the decisive test of
  the whole Charlier mechanism.

## 2026-08-28 17:05 -- THE MECHANISM, QUANTIFIED: a bounded cancellation, uniform in depth

The decisive test of the Charlier route is done (results/measure_mass_test.json).
The measure behind the base sequence is extracted from the exact moments by
Gaussian quadrature -- orthogonal polynomial from exact Hankel determinants,
nodes as CERTIFIED root enclosures, weights solved in acb interval
arithmetic -- and nothing was interpreted until both verifications passed in
all 54 rows: the quadrature reproduces m_0..m_{2q-1}, and it reproduces the
exactly computed K_r.

WHAT THE MECHANISM IS. K_r = INT P_r dmu is positive NOT because P_r >= 0 on
the support -- it is not, and up to 98% of the mass can sit where P_r < 0 --
but because the negative contribution is bounded by a fixed fraction of the
positive one:

    |negative part| / |positive part|  <=  0.70   at and below the shore
    (max 0.70, 0.62, 0.66 at depths j = 4, 6, 8 -- NOT growing with depth),

over lam = 1, 3, 72 and n = 12, 24, both at the shore and at 80% of it.

CONTROL (the part that makes it evidence rather than decoration). Above the
shore, where even knives are genuinely negative, the same ratio EXCEEDS 1 in
9 of 9 negative-knife rows -- from 1.07 up to 2.9e4 -- and the quadrature
sign agrees with the reference engine in all 54 rows. A diagnostic that
never crossed 1 anywhere would have been measuring nothing.

THE THEOREM SHAPE IS NOW EXPLICIT. An all-depths proof needs:
  (i)  m_t is a Hamburger moment sequence with measure on (-inf, 1]
       (measured: H0 positive definite at full size; the negative-y part is
       exponentially tiny and provably HELPS, since P_r >= 0 there);
  (ii) a bound |INT_{P_r<0} P_r dmu| <= c |INT_{P_r>0} P_r dmu| with c < 1
       UNIFORM IN r, valid exactly on D <= T_hat.
Step (ii) is where the shore must enter, and the control above shows it
enters correctly: the bound fails precisely when the physics fails.

RESULT: the mechanism of knife positivity is identified and quantified.
EVIDENCE: results/measure_mass_test.json (54 rows, both verifications, the
  above-shore control).
STATUS: measured, with certified enclosures; (i) and (ii) are unproved.
NOVELTY: NOVELTY_UNCHECKED.
TIME: from the crude criterion's death to the quantified mechanism: ~1h.
LEARNED: when a sufficient condition dies, do not abandon the
  representation -- measure HOW it dies. The gap between "P_r changes sign
  in the support" and "the knife is still positive" was the whole content,
  and it turned out to be a stable 0.7 rather than a near-miss.
NEXT: attack (ii) directly -- the positive part is dominated by the mass
  near the smallest nodes, so bound the ratio by the first few Christoffel
  weights against the tail; and check whether c can be taken independent of
  n and lam as the data suggest.

## 2026-08-28 17:40 -- My own theorem shape challenged within the hour

The step (ii) I wrote down at 17:05 -- "a bound |negative| <= c |positive|
with c < 1 UNIFORM IN r" -- does not survive its own widening test
(results/cancellation_bound_sweep.json, 486 verified rows):

* on the wider grid (n <= 40, j <= 12, lam over five orders) the worst
  cancellation ratio is 0.912, not 0.70;
* the ratio does not grow monotonically in depth: at n = 40, lam = 7 it
  rises to 0.954 at j = 14 and falls back to 0.54 by j = 24, so the worst
  case sits at INTERMEDIATE depth;
* and the peak GROWS WITH THE LEVEL: 0.68, 0.80, 0.89, 0.95 at
  n = 14, 20, 28, 40 (lam = 7), i.e. 1 - peak = 0.34, 0.20, 0.11, 0.046.

All 486 rows keep both verifications (moments and K_r reproduced) and the
quadrature sign agrees with the reference engine everywhere, so the
measurement is sound; and the peaks are LOWER bounds, because the
quadrature rule is capped at 12 points (j <= 24).

HONEST VERDICT. The mechanism is real but ASYMPTOTICALLY TIGHT in n: a
proof cannot fix a constant c < 1 and must instead track how the two parts
approach each other, or pair terms rather than bound groups. That is a
harder theorem than the one I proposed, and knowing it now is worth more
than an hour of building on a false shape. It also explains, independently,
why every earlier route died at large n and near the shore: the object is
marginal there in TWO directions at once.

RESULT: proposed theorem shape refuted by its own measurement; the
  asymptotic tightness in n quantified (1 - peak ~ 0.34 -> 0.046).
EVIDENCE: results/cancellation_bound_sweep.json (486 verified rows plus the
  peak trend).
STATUS: measured; the trend is a lower bound, so the true behaviour may be
  worse, not better.
LEARNED: measure a proposed constant's DEPENDENCE before building on it --
  the first grid said 0.70 and looked like a margin; three parameters later
  it reads as an approach to 1. Sample the direction a constant could
  degrade in, not just the region it was found in.
NEXT: since c -> 1, look for the exact pairing instead of a bound: adjacent
  quadrature nodes whose contributions cancel in pairs would give the
  positivity structurally; also test whether 1 - c has a clean law in n
  (the data suggest a power decay), which would itself be the theorem's
  quantitative core.

## 2026-08-28 18:10 -- Three constant-free routes tested and refuted; the line closes

Because the cancellation ratio approaches 1 with the level, a proof cannot
fix a constant and would have to obtain positivity structurally. Three
natural structures were tested exactly on the ordered quadrature
contributions c_i = w_i P_r(y_i) (results/pairing_structures_probe.json):

* adjacent pairing, c_i + c_{i+1} >= 0:            holds in 1 of 9;
* nonnegative partial sums from the left:          5 of 9; from the right: 1 of 9
  -- this was the most interesting candidate, because it is exactly the
  variation-diminishing shape a total-positivity argument delivers, and it
  would have connected the day's kernel TP theorem to the knife itself;
* Leibniz alternating tail (monotone magnitudes):  6 of 9.

All three are refuted. The only property holding in all 9 configurations is
no stronger than the ratio already measured: the head block at the smallest
nodes exceeds the tail, with |tail|/head between 0.00 and 0.79.

So this line is closed for now, with a precise statement of what is missing:
the positivity of K_r is a genuinely quantitative balance that tightens with
n, and neither pairwise cancellation, nor sign-regularity of the partial
sums, nor an alternating-series bound explains it.

RESULT: three candidate mechanisms refuted; the sign pattern of the
  contributions (a positive head then an alternating tail) documented.
EVIDENCE: results/pairing_structures_probe.json.
STATUS: refuted routes, recorded as such.
LEARNED: a theorem elsewhere in the same session (kernel TP) does not imply
  a usable route here -- the variation-diminishing shape it would give is
  exactly the one the data refuse. Test the shape a theorem would need
  BEFORE building a bridge to it.
NEXT (for a fresh session, in order of promise): (a) the asymptotic route --
  since the tightness grows with n, expand K_r around the scaling limit
  where the leading behaviour is known exactly in closed form, and control
  the correction uniformly in j; (b) literature check of the kernel identity
  (Krattenthaler, Advanced Determinant Calculus) before any novelty wording;
  (c) revisit whether the shore condition can be injected earlier -- every
  route so far imposes D <= T_hat only at the end, whereas the measured
  control shows the bound failing exactly when the physics does, so the
  shore may belong inside the representation itself.

## 2026-08-28 18:30 -- Novelty gate applied to the day's theorem: POSSIBLY_KNOWN

Before any outward wording, the kernel identity was checked against the
determinant-evaluation literature. The verdict is that its MECHANISM is
classical: the polynomial-alternant fact (monic columns of degrees 0..q-1
give the Vandermonde outright) is textbook, and determinant evaluations of
binomial/factorial kernels are a developed genre -- Krattenthaler's
*Advanced Determinant Calculus* (Sem. Lothar. Combin. 42 (1999), B42q) and
its *Complement* (Linear Algebra Appl. 411 (2005) 68-166), with
Lindstrom-Gessel-Viennot as the combinatorial route. A targeted search did
not surface this exact kernel, but absence in a search is not absence in the
literature.

So results/KERNEL_TP_THEOREM.md now carries an explicit prior-art section
and the status POSSIBLY_KNOWN. What is ours is narrower and stated as such:
the observation that the column factors have roots symmetric about H/2 (so
one quadratic substitution linearizes all columns), and that the resulting
root bound 2 r_max - 1 falls below H exactly on the physical domain, which
is what converts the identity into strict total positivity where the knife
problem needs it.

LEARNED: run the novelty gate on the same day as the theorem, while the
proof is fresh -- the honest scope ("the technique is classical, the
identification is ours") is easy to write now and painful to retrofit into
a preprint later.

## 2026-08-28 19:05 -- THE ASYMPTOTIC ROUTE: a corner where ALL depths follow from one classical theorem

The route the handover put first has produced its first concrete result
(results/asymptotic_regime_probe.json).

THE IDEA, from the scaling limit. With n = rho*lam, D = d*lam and
lam -> infinity, the normalized sequence collapses to a single geometric
mode, M_t^(r) -> x^t, so the measure becomes ONE Dirac atom and
K_r -> (1-x)^r, with the shore condition being exactly x <= 1. Away from the
limit the atom spreads -- but if the finite sequence M_t^(r) is still a
HAUSDORFF moment sequence, then by Hausdorff's theorem every alternating
difference is nonnegative, i.e. K_r = (-1)^r Delta^r M_0 >= 0 for EVERY
depth at once. No depth induction, no uniform constant: one classical
theorem covers the whole family.

WHERE IT HOLDS -- two sharp boundaries, both measured at the shore:

1. A LAM THRESHOLD WITH BOUNDED RATIO. lam*(n, j)/n stays between 1.33 and
   2.86 as n runs 12, 20, 28, 40, 60 (grid of powers of two, so lam* is
   located to a factor of 2): the property switches on around lam ~ 2n and
   stays on.
2. AN EXACT DEPTH BOUNDARY. At lam = 10^4 the largest depth with the
   property is j = n/2 + 1 -- exactly, in every case tested: 7, 9, 11, 13,
   15, 19, 23 at n = 12, 16, 20, 24, 28, 36, 44. This is the same n/2
   boundary the base sequence m showed earlier today, now sharp rather than
   approximate.

WHAT IT IS AND IS NOT. It is the first statement in the programme covering
ALL depths at once in an unbounded region, by a named classical theorem
rather than a per-depth certificate. It is NOT a finish: the complementary
region (lam below ~2n, or j above n/2 + 1) is itself unbounded, so it cannot
be handed to the compact-region machinery the way lam <= 7 was.

RESULT: an explicit corner -- lam ~> 2n and j <= n/2 + 1 -- where knife
  positivity for all depths follows from complete monotonicity.
EVIDENCE: results/asymptotic_regime_probe.json (thresholds per (n, j), the
  exact depth law, consistency spot-checks in the implication direction).
STATUS: measured. Two things would make it a theorem: proving M is
  completely monotone in that corner, and sharpening lam* (the grid is
  coarse by a factor of 2).
NOVELTY: the mechanism is Hausdorff's theorem, entirely classical; what is
  ours is the identification of the corner. NOVELTY_UNCHECKED beyond that.
LEARNED: the scaling limit was treated for a year as an asymptotic FACT;
  read as a statement about the MEASURE (one atom) it becomes a hypothesis
  about finite n that is exactly testable -- and true in a describable
  region. Re-read old limits as structural claims, not just as numbers.
NEXT: (a) prove complete monotonicity in the corner -- with the measure a
  perturbed single atom there, a Hausdorff criterion via the explicit
  E_{2t}(n) structure looks reachable; (b) locate lam* sharply (bisect
  rather than the power-of-two grid) and test whether lam*/n has a limit;
  (c) the complementary region needs a different idea -- the j > n/2 + 1
  half may want the m = n - j variable instead, where the roles invert.

## 2026-08-28 — Outreach: the shore landscape, drawn from the exact engine

WHAT. `lab/shore_landscape_data.py` exports three already-established objects on
a display grid — the level surface `T_k(lam)` (73x73), the shore
`T_hat(lam) = min_k T_k(lam)` at 241 values of lam with its 18 integer-level
handovers, and the exact knife sign field on a 41x41 `(lam, D)` grid at knife
orders j = 4 and j = 5, n = 12, from the same reference engine
(`jacobi_normal_form.jacobi_coeff_rec`) the certificates use. Artifact:
`results/shore_landscape_data.json`. `lab/build_shore_viz.py` injects it into
`outreach/shore_of_universes.html`, a 3D scrollable explainer written for
children (founder's request).

NO NEW SCIENCE, and the artifact says so in its own `claim` field. What it does
carry is a self-check with teeth: of 3362 exactly evaluated knife signs, 401 are
negative and **0 of those sit below the shore**. The builder REFUSES to produce
the page if that count is ever nonzero, because the page's central sentence to a
child ("not one red dot is under the water") would then be false. A picture that
can state a falsehood is a picture with a gate on it.

The prose counts (dots, negatives, handovers) are computed by the builder from
the data rather than typed, so the text cannot drift from the picture.

HONEST LIMITS stated on the page itself: the back plateau is a display clamp at
T = 140, not physics; the ghost walls are the unproved depths; the last chapter
says the keystone is open and that depths 2-6 are certified while 7 is only
banked. No claim-promotion words appear.

NEXT: back to the asymptotic route (the corner theorem), per the previous entry.

## 2026-08-28 — The B-form, the derivative form, and the first PROVED all-depths positivity

THE MOVE. Two elementary substitutions change the character of the exact knife
sum. `C(r,t) t! = (r)_t` absorbs the binomial into a falling factorial, and
`E_{2t}(n)` IS by definition the t-th elementary symmetric function of
`{(n-2k)^2}`, so `E_{2t}(n)/s^{2t} = e_t(b)` with `b_k = (n-2k)^2/s^2`. Hence

    K_r = sum_t (-1)^t c_t e_t(b),  c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t].

Every `b_k` is below 1 for every `lam > 0` (`max_k b_k = (n-2)^2/s^2`, and
`s = lam+n-1 > n-2`), uniformly in n and lam — and `c_t` carries no lam at all.
The earlier moment route produced a measure whose support was the obstruction;
here the variables are inside the unit interval by construction.

THE THEOREM. `T_t = c_t e_t(b) > 0` on the physical domain, and if `T_{t+1} <= T_t`
the sum groups as `(T_0-T_1) + (T_2-T_3) + ...` — Leibniz, and it does not care
about the parity of r, so the criterion is uniform in DEPTH. Newton's
inequalities (the b's are nonnegative, so `prod(1+b_k x)` is real-rooted) bound
`e_{t+1}/e_t <= bbar (n-1-t)/(t+1)` with `bbar = n(n-2)/(3s^2)`, and the
resulting `f(t)` is decreasing, so ONE inequality suffices:
`r(H-r) n(n-2) <= (3n-9/2) s^2`. `r(H-r)` increases in r on `r <= n-2` (because
`H/2 > n-2` exactly when `D > 3`), so the worst depth is `r = n-2` and

    D <= D*(n,lam) = (6n-9)s^2/(n(n-2)^2) - 2n + 3  ==>  EVERY knife positive.

No search, no per-depth ladder. `results/BFORM_POSITIVITY_THEOREM.md`.

THE DERIVATIVE FORM. The lam-free factor `w_t = (r)_t/(n-1)_t` equals
`C(N-t,N-r)/C(N,r)` (N = n-1), a polynomial in t that VANISHES for t > r — the
depth truncation is automatic, not imposed. So the sum may be run to t = N, and
since `x^{N-t}` differentiated m = N-r times at x = 1 gives `(N-t)_m` exactly,
the whole sum is an m-th derivative; homogeneity in y then removes y from the
roots. Result: `K_r = sum_t (-1)^t d_t e_t(eta) = INT_1^inf prod_i (1 - eta_i y)
dsigma(y)`, with eta the roots of the m-th derivative of `prod_k (u - b_k)` (all
real in [0, B] by Rolle) and sigma an explicit Beta-type density. The
alternating sum is GONE: r real linear factors against one density on one
variable. `results/bform_derivative_form.json`.

VERIFICATION, all non-vacuous. B-form vs the reference engine: 870 trials, 0
mismatches, including 37 points where the reference knife is NEGATIVE. D-form vs
both: 870 trials, 0 disagreements. `w_t` identity: 18200 checks, 0 violations.
eta real and inside [0,B] by certified enclosures: 0 violations / 45 cases. The
sigma representation by interval arithmetic on the Gamma ratio: 0 violations.
Both implications (closed form => Leibniz => K_r >= 0): 612 cases, 0 violations
either way — either would have broken the proof.

THE HONEST SIZE, and it is the important part. `D*` reaches the shore at
lam = 127, 340, 654, 1069, 2202, 4659, 10773, 30572 for n = 8..100, i.e.
lam ~> 3 n^2 (ratio still drifting up at n=100). The MEASURED Hausdorff corner
(results/asymptotic_regime_probe.json) already covers all depths from lam ~> 2n.
So: proved region lam ~> 3n^2, measured region lam ~> 2n. The proved one is much
smaller. It is progress only in the sense that it rests on no search.

AND THE GAP IS NOT SLACK. The binding step is `T_1 <= T_0`, where Newton's
inequality is an EQUALITY (`p_1/p_0 = bbar` exactly) — so the closed form is
essentially Leibniz's first step, not a lossy weakening of it. On the 612-case
grid the closed form and full Leibniz hold in exactly the same 265 cases.
Closing the gap needs a route that is not term-by-term monotonicity. That is
what the derivative form is for.

TWO SELF-CAUGHT ERRORS. (1) The sigma/Gamma check first reported 91 violations;
the identity was fine, my comparison went through `float`, producing a point
value with no error bars — fixed to exact fmpq -> arb enclosures, 0 violations.
(2) `lam_theorem` hung: it called the linear-scan shore at lam ~ 10^7, which
costs O(lam). Replaced by a ternary search justified by the project's own
convexity certificate (results/unimodality_cert.json), regression-checked
against the scan on lam = 1/2..300, 0 disagreements.

CLAIM STATE: source-supported by internal derivation and machine verification;
NOT independently validated. Ingredients (Newton, Rolle/Gauss-Lucas, the Beta
integral, the binomial identity) are all classical, and the m-th-derivative
operation is exactly finite free probability's object (Marcus-Spielman-
Srivastava). Novelty status POSSIBLY_KNOWN for the technique. Independent
validator and domain critic passes are queued.

NEXT: the derivative form is the live front. sigma has unbounded support, so
positivity of the integrand on `y < 1/max(eta)` does not close the argument —
the question is a tail bound on sigma against the measured root contraction
(max(eta)/B = 0.448 at r=2 rising to 1.000 at r=n-2, n=20, lam=7).

## 2026-08-28 — The J-form: the same theorem, with the factor of n recovered

THE FIX. The derivative form left `K_r = INT_1^inf prod_i (1 - eta_i y)
dsigma(y)` over an UNBOUNDED ray, and that unboundedness was the whole reason it
would not close. It was removable by writing sigma in its original variable and
substituting `w = 1 - v`:

    K_r = [1/B(eps,C+1)] INT_0^1 w^{a-1}(1-w)^{b-1} prod_i (w - eta_i) dw,
    a = n - 1/2 - r,   b = D/2 + (n - 2 - r).

The knife is a JACOBI (Beta) MOMENT of a real-rooted polynomial over the COMPACT
interval [0,1], all of whose roots lie in [0, B], B = (n-2)^2/s^2 < 1. Splitting
at eta = max eta_i and bounding both pieces (on [eta,1] each factor is at least
w-eta; on [0,eta] each is at most eta in absolute value, and b >= 1 makes
(1-w)^{b-1} <= 1) gives the sufficient condition

    a (1 - eta)^{a+b+r-1} B(a+r, b) >= eta^{a+r}.

WHAT IT BUYS, measured. The Leibniz route proves positivity for lam ~> 3 n^2.
This one, on the same object, reaches lam ~> 32 n:

  n:      6    20    40    60   100   160   260   420
  lam:   83   531  1179  1824  3112  5040  8249 13380
  lam/n: 13.8 26.6  29.5  30.4  31.1  31.5  31.7  31.9

`lam/n` plateaus near 32 while `lam/(n ln n)` keeps FALLING (7.7 -> 5.3), so the
growth is linear in n, not n log n — I checked that specifically rather than
calling a rising ratio "linear". At n = 60 the new bound needs lam = 1824 where
Leibniz needs 10773, and the ratio grows with n because one region is linear and
the other quadratic. Against the measured (unproved) Hausdorff corner at
lam ~> 2n, the proved region is now within a constant factor of about 16 instead
of a factor growing like n.

SOUNDNESS. 1239 cases against the exact reference engine; the hypothesis fired
469 times and in 0 of those was the knife non-positive. Every inequality is
decided on a certified arb enclosure in log form, accepted only when the
enclosure of the difference is strictly positive — never on a midpoint. Using
the exact eta_max instead of the uniform bound B closed 0 extra of 16 cases, so
B is not the bottleneck and the loss is elsewhere.

WHY THE EARLIER ROUTE LOST THE FACTOR. Leibniz's binding step is `T_1 <= T_0`,
where Newton's inequality is an EQUALITY, so no sharpening of constants could
have helped; the whole loss was term-by-term monotonicity itself. Recording this
because it is the reusable lesson: when the binding step of a bound is tight,
the bound is not the thing to improve — the decomposition is.

STILL A CORNER. All three statements (Leibniz 3n^2 proved, J-form 32n proved,
Hausdorff 2n measured) cover only large lam. The region below the shore at small
lam — where the physics actually is — remains open, and none of this touches it.

NEXT: the J-form's loss is now in the split at w = eta: both bounds are crude
(the [0,eta] piece uses |prod| <= eta^r, ignoring all cancellation). A sharper
treatment of the small-w piece, or injecting the shore condition into b (which
grows with D, sharpening the weight exactly when the physics tightens), is where
the next factor should come from.

## 2026-08-28 — Where the J-form bound loses, and two fixes killed

A useful accident makes Theorem 9's two sides directly comparable with the truth:
`a + r = n - 1/2 = C + 1` ALWAYS, so `B(a+r,b)` is the J-form's own normaliser
and dividing through leaves `K_r >= POS - NEG` with
`POS = (1-eta)^{n-3/2+b}` and `NEG = eta^{n-1/2}/[a B(n-1/2,b)]`.

MEASURED (results/bform_gap_diagnosis.json). NEG is the binding side by a wide
margin — it spans fourteen orders of magnitude across the grid and explodes below
the threshold (3.1e14 against a true K_r of 1.9e-3 at n=20, lam=30, r=18). POS
stays within a factor 1.2 to 29 of the true K_r, so POS is lossy too and
increasingly so with depth — I first wrote "single-digit factor" and the numbers
say 29x at n=20, r=18; corrected before banking. But the threshold is set by NEG:
the single step `|prod_i (w - eta_i)| <= eta^r` on `[0, eta]`, which throws away
the fact that the integrand VANISHES at each of the r roots.

TWO FIXES KILLED, both cheap to test and both dead:

1. THE TRIANGLE INEQUALITY. `|prod (w-eta_i)| <= sum_t e_t(eta) w^{r-t}`
   integrates in closed form, so it looked like a free upgrade. It is WORSE in
   24/24 cases, by up to 21.7x. Reason: dropping the signs destroys exactly the
   cancellation that makes the piece small — `sum_t e_t(eta) eta^{r-t} =
   prod_i (eta + eta_i) >= eta^r`. A bound that discards oscillation cannot beat
   one that at least caps the envelope.

2. A PER-INSTANCE CERTIFIED QUADRATURE of the integral's sign. Abandoned before
   being built, after writing it: it is CIRCULAR. For given (n, r, lam, D) the
   sign of the integral IS the sign of K_r, which this repository already
   computes exactly, so no per-instance certificate can add information. Only an
   all-n bound can. Recording this because the module was written and deleted,
   and because the same trap will look attractive again.

WHERE THE SHORE ENTERS — and this answers a question the programme has been
carrying since the moment routes began. Every route so far imposed `D <= T_hat`
only at the very end. The J-form says where it belongs: the weight is
`Beta(a, b)` with `b = D/2 + (n-2-r)`, so its mean
`a/(a+b) = (n-1/2-r)/(D/2+2n-5/2-2r)` shrinks as D grows — raising D slides the
weight's mass toward w = 0, which is exactly where the roots sit and where the
integrand oscillates. Both the mean and eta_max shrink as lam grows, but at
different rates, and the RATIO is what matters: at n=20, r=18 it climbs
0.04 -> 0.15 -> 0.28 -> 1.00 at lam = 30, 272, 531, 2000. So in this
representation the shore condition is not an afterthought — it is the statement
that the weight's mass stays clear of the roots.

NEXT: the remaining factor is a bound on the oscillating integral over [0, eta]
that is valid for ALL n. The naive envelopes are exhausted (both above); what is
needed is a handle on `max_{[0,eta]} |prod_i (w - eta_i)|` for the roots of the
m-th derivative of `prod_k (u - b_k)` — which is a finite free probability
object (Marcus-Spielman-Srivastava), and is exactly what the domain-critic pass
was asked to place in the literature.

## 2026-08-28 — Two independent review passes on the positivity theorems

Neither pass was run by the role that wrote the proofs, per the standing rule.

INDEPENDENT VALIDATOR: **PASS** (validation/VAL-BFORM-0001.yaml,
lab/validator_bform_check.py). It rebuilt the closed form from
lab/jacobi_normal_form.py alone, never importing the modules under review, and
hunted 13380 adversarially chosen points with the hypothesis (*) true — at
equality in (*), at D = 3 + 1e-9, n = 4..60, lam = 1e-3..1e15 — finding NO
counterexample. It also confirmed each monotonicity factor of Theorem 5
separately over 3952 cells, every step of Theorem 7 exactly, and §4b's J-form
and (**). Non-vacuity: 77 of 544 probes just outside (*) carry a NEGATIVE
reference knife, so the hypothesis is not describing a trivially safe region.

TWO ARITHMETIC SLIPS, both mine, both found by BOTH passes independently and in
algebraically identical forms (ERR-0014). My Lemma 3 identity was wrong by 2 and
my Theorem 6 parenthetical claimed an equivalence threshold of D > 3 where it is
D > -1. Both conservative, so no conclusion moved — which is exactly why every
machine check I had built passed over them. The rule I failed to apply is the
repository's own ERR-0012: a check that cannot fail is not a check. I verified
the THEOREMS and never verified the hand-derived intermediate IDENTITIES
separately. Two writing gaps also fixed: Theorem 9's substitution needs a >= 1
(true, unstated), and Theorems 5/6 must not be quoted at j = n, where
e_{n-1}(b) = 0 for even n breaks the Newton step.

DOMAIN CRITIC: the verdict is "present as STRUCTURAL progress; the coverage
number must not be the headline", and three of its findings changed the file.

1. THEOREM 6 IS VACUOUS WHERE WE ACTUALLY WORK. D* must exceed 3 to say
   anything, and D*(12, lam) = -13.44, -11.43, -3.99 at lam = 1, 5/2, 7 — every
   value used in the project's own sweeps. At lam = 1 (Virasoro-Shapiro) it is
   empty for every n >= 6. Verified exactly. This now sits in the statement.
2. THE ALL-DEPTHS NUMBER UNDERSELLS THE THEOREM BY A FACTOR OF n. Condition (*)
   is depth-resolved and Theorem 6 quotes only its worst case r = n-2. At FIXED
   depth the threshold is LINEAR in n: lam*/(r n) = 2.13..2.90, flat in n across
   n = 12, 24, 48. The honest form is lam* ~ c r n per depth.
3. THE REPRESENTATION EXPLAINS THE PARITY DICHOTOMY IN ONE LINE. As D -> inf the
   Beta mass goes to 0, so the w -> 0 end dominates and
   sign(K_r) -> (-1)^r = (-1)^{j-1}: odd j never turns negative, even j must.
   Verified at n=12, lam=7: j=3,5 stay +1 through D = 2e5, while j=4,6 flip to
   -1 by D = 500. The programme has MEASURED that asymmetry for months; here it
   is derived.

AND A THIRD DEAD END, measured. The obvious repair to Theorem 9 — replacing
|prod (w-eta_i)| <= eta^r by the true envelope max_{[0,eta]}|prod| — was tested.
The envelope is scale-invariant in lam, hence a pure function of (n,r), and it
is much smaller: about 2.4^{-r}, e.g. 3.96e-7 at n=20, r=18. Substituting it
moves the threshold by 1.1x-1.2x. ONLY. The reason closes the route: NEG carries
eta^{n-1/2} with eta ~ 1/lam^2, so NEG ~ lam^{-(2n-1)} and a gain of factor G
buys G^{1/(2n-1)} in lam — a 2.5-million-fold gain at n=20 is 1.45x. No constant,
and no factor exponential in r, can move this threshold. Reaching lam ~ 2n needs
a different decomposition, not a better bound inside this one. That is three
dead ends on the same split (triangle inequality, per-instance quadrature,
envelope), all measured rather than guessed.

The critic also notes the deepest knife is structurally immune to root
contraction: b_1 = b_{n-1} = B is a DOUBLE root of prod_k (u - b_k), so one
differentiation leaves it and eta_max = B exactly at r = n-2. That is why the
measurement read 1.0000 there — exact, not rounding.

CLAIM STATE moved to independently-validated for the mathematics of Theorems
1-9 as sufficient conditions on the stated domain. NOT validated for novelty:
no literature pass has been done, and the critic would strengthen
POSSIBLY_KNOWN to LIKELY KNOWN, naming Malo-Schur-Szego composition,
Polya-Schur multiplier sequences (Aissen-Schoenberg-Whitney, Borcea-Branden),
the Askey-Gasper method, and finite free probability as the places to look.
It ran no search; that is a to-do list, not a finding.

## 2026-08-29 — THE LITERATURE PASS: our transform is a century old, and it hands us a new criterion

The to-do list at the end of the 28 August entry was executed. The answer to
"is the B-form transform new" is NO, and it is not close: multiplying e_t by a
Pochhammer ratio is the finite free multiplicative convolution BOX_n, which
Martinez-Finkelshtein, Morales and Perales (arXiv:2309.10970, sec. 1) name in
passing as "also known as Schur-Szego composition". The zero-preservation
results attached to it are Szego 1922 and Walsh 1922. The critic's guess
(Malo-Schur-Szego, Polya-Schur multiplier sequences) was the right genre — the
same paper remarks that BOX_n sits in the framework of finite multiplier
sequences.

IDENTIFIED, NOT ASSUMED. K_r = (p BOX_{n-1} q)(1) with p = prod_k (x - b_k) and
e_t(q) = (r)_t (H-r)_t / [t! (n-3/2)_t]: 336 cases, 0 sign mismatches against
the reference engine, 65 of them with a NEGATIVE reference knife, so the check
cannot be vacuous (lab/ffp_convolution_check.py, results/ffp_convolution_check.json).
BFORM_POSITIVITY_THEOREM.md sec. 7 moved POSSIBLY_KNOWN -> KNOWN for the
technique. Sec. 1, 4 and 4b introduce no new operation; what is ours is the
identification of the CHR knife with such a composition, and the two region
theorems proved for it.

THE ROUTE IT OPENED, CLOSED THE SAME DAY. The reason to care was the
Szego-Walsh preservation theorem: if q were in P(R>=0), then p BOX q would be
real-rooted and positivity would reduce to theta_max < 1 with NOTHING thrown
away — unlike Theorem 9, whose loss sec. 6c proves no constant can repair. But q
has genuinely complex zeros in 336 of 336 cases, and rigorously so: the arb
enclosure of the imaginary part EXCLUDES zero (at n=12, j=6, lam=7, D=30 the
zeros are 3.7358 and 3.2986 +/- 1.3805i and 2.0954 +/- 2.2525i). p BOX q itself
is real-rooted in only 93 of 336. That is exactly the exclusion direction the
same authors use. Route closed for a stated reason, not abandoned.

AND WHAT FELL OUT OF IT — CRITERION S. Write the reduced composition
P(x) = sum_t (-1)^t c_t e_t(b) x^{r-t} and expand at x = 1:
P(1+y) = sum_m A_m y^m with A_0 = K_r. If every A_m > 0 then P has no real zero
on [1, inf), so P keeps its sign at +inf, which is +, so K_r > 0. Descartes on
the shift; exact in fmpq; sufficient, not necessary.

Measured: 3094 of 3094 points below the shore, n = 6, 12, 20, 28, 40, EVERY
depth 3 <= j <= n-1, lam in {1/10, 1/2, 1, 5/2, 7, 30, 300}, D/T_hat in
{1/4, 1/2, 9/10, 99/100, 1}. Negative control at D = 40 T_hat: 26 negative
knives seen, criterion fired on 0 of them. Beside Theorem 6 (lam ~> 3n^2) and
Theorem 9 (lam ~> 32n), both corners, this is the first candidate all-depths
criterion whose tested region is the physical domain itself.

IT IS A MEASUREMENT. No A_m with m > 0 is proved; n <= 40 is not all n; and
ERR-0013 killed a statement that had certified at three depths, so a sweep is
not a proof in this repository. Next target: A_m > 0 by downward induction from
A_r = 1.

Also recorded: INSPIRE title searches for "Schur-Szego composition" and
"finite free convolution" return 0 records, with the control query returning
the expected papers — weak evidence that the framing is absent from the
amplitude literature, and labelled weak in results/FFP_LITERATURE_PASS.md.

### 2026-08-29, same day — CORRECTION: criterion S was circular; the identity behind it is not

An hour after committing the pass I asked what `A_m` actually is, and the answer
killed the criterion and paid for itself twice over.

    A_m = C(r,m) * K_{r-m} evaluated at H -> H - m, i.e. at D -> D - 2m.

Exact: 1236 ad-hoc checks and then 1696 inside the artefact, 0 mismatches.
Proof is one line: (r)_t (r-t)_m = (r)_m (r-m)_t turns the C(r-t,m) weight into
the c-sequence with r -> r-m and (H-r) untouched.

At m = 0 that reads A_0 = K_r. So "all A_m > 0 implies K_r > 0" has the
conclusion sitting inside the hypothesis — true, and empty. ERR-0015 records it.
The sweep is not wrong, it just measured something else: the whole DIAGONAL
STAIRCASE (j,D) -> (j-m, D-2m) is positive at all 3094 points below the shore,
and intact at 0 of the 26 negative knives above it.

WHAT THIS BUYS. The Taylor coefficients of the knife polynomial at x = 1 are
knives again, lower depth and lower dimension. Two consequences:
  * the family is self-similar along that diagonal, which no route so far used;
  * the non-circular direction is theta_max(p BOX_N q) < 1 ==> the entire
    diagonal positive at once, with no knife value known in advance. Bounding
    the largest root of a Schur-Szego composition is a studied problem (the
    S-transform bounds of Marcus-Spielman-Srivastava). That is the live route.

Caught by asking what the object was, not by a check — ERR-0012's lesson again,
one level up: before measuring a criterion, expand its hypothesis at the trivial
index and see whether the conclusion is already there.

### 2026-08-29, later — how much room the root bound has, and a fourth dead end

The live route after ERR-0015 is theta_max(p BOX_N q) < 1, which would give the
whole diagonal at once. Two measurements on it, both exact.

ROOM. For each (n, r, lam) at the shore, the smallest c for which the exact
Descartes test certifies no real zero in [c, inf). Worst margin 1 - c* over
depths: .111/.061/.053/.045/.036/.031/.029 at lam = 1 for n = 6..80, and
essentially FLAT near .04 at lam = 5/2 and 7 (log-log slopes -0.44, -0.04,
+0.04). 36 rows, 0 depths left uncertified. So a bound may waste a few percent,
roughly uniformly in n — unlike Theorem 9, whose slack section 6c proved no
constant could recover. Caveat: above n = 28 only five depths per row are
tested, so the worst case may be optimistic.

DEAD END 4. Classical magnitude bounds cannot close it. Fujiwara
2 max_t (c_t e_t)^{1/t} and Cauchy 1 + max_t c_t e_t both need to be < 1 and
come out at 2.8-49 and up to 1.4e7. They discard signs, and the cancellation is
the whole phenomenon — the same wall as the Bernstein jam at odd depth and the
same reason Theorem 5 cannot be sharpened. A usable bound must use the structure
of the composition, not coefficient sizes.

### 2026-08-29, evening — the reformulation: one scalar crossing, and it is tight

Chaining today's identity with step (c): A_m = C(r,m) K_{r-m}(D-2m), every knife
decreases in D, so the diagonal staircase can switch off only once as D grows.
Measured: 0 monotonicity violations in 1920 steps. Hence a single crossing
D_cross where the composition's largest real zero passes 1, and

    every knife positive below the shore  <==>  D_cross >= T_hat.

D_cross/T_hat >= 1 in 120 of 120 rows (n = 6..60, three depths, lam = 1, 5/2, 7,
30, 300). Worst 1.008 at n=60, r=2, lam=30. Descartes under-estimates the
crossing, so every ratio is a lower bound on the truth.

AND THE PRICE. The reformulation is exact but TIGHT: 0.8% at the worst tested
point. Two more bounds died against that today -- Grace-Szego-Walsh product of
extreme zeros (2 to 7.7, needs < 1) and Fujiwara/Cauchy magnitudes (2.8 to 49).
Five measured dead ends now sit on the same wall: anything that spends a constant
factor cannot pass. Measuring the room BEFORE hunting the bound is the lesson
section 6c taught the expensive way.

### 2026-08-29 — one hypothesis killed in ten minutes: the zeros are not on the T ladder

Since the shore is T_hat = min_k T_k, the cheap hope was that the first zero of
K_r in D sits ON that ladder, which would turn the keystone into an inequality
between explicit rational functions. It does not. Measured gaps to the nearest
T_k are 0.05 to 0.98 at lam = 1 and 7, n = 12..40 -- and the ladder is DENSE at
those k, so "nearest" carries no information: proximity there is arithmetic, not
structure. Killed, ten minutes, no code kept.

What the same run did give, and it matters more: every first zero sits ABOVE the
shore, ratio D0/T_hat from 1.062 (n=12, lam=7, j=4) to 39. And only EVEN knife
orders have a zero at all, exactly as the Beta-weight parity argument of sec. 6b
predicts -- the first three attempts found "no zero" purely because I had picked
even r, i.e. odd j. The parity derivation is now doing predictive work rather
than describing an old measurement.

### 2026-08-29, night — the shore gap, and a parity claim of mine refuted

THE GAP. results/shore_gap_scan.json: the first zero D0 of the knife in D,
against the shore, over n = 6..40, lam = 1/10..300, EVERY knife order. 928 rows,
and D0/T_hat >= 1 in every one. Closest approach 1.0188 at n = 40, j = 4,
lam = 30; closest among odd j is 1.146 at n = 8, j = 3, lam = 1. So the physical
claim holds with 2% to spare at the tightest point found, and the extremal corner
is SHALLOW depth at moderate lam -- not the deep knives the programme has spent
most of its effort on.

ERR-0016, mine, found by the same scan. Section 6b of BFORM_POSITIVITY_THEOREM
said "odd j never turns negative; even j must", called it derived, and used it as
the explanation of the long-measured parity asymmetry. Half of it is derived. The
D -> infinity limit forbids an odd-j knife from ENDING negative; it says nothing
about a dip at finite D, and odd knives DO dip: n = 6, j = 3, lam = 1/10 is + at
D = 12, - at D = 13, + again from D = 20, on BOTH engines. 72 such cases, all at
small lam (22 at 1/10, 19 at 1/2, 19 at 1, 11 at 5/2, 1 at 7, none above), spread
over j = 3..17. All above the shore, so no theorem moves.

The lesson is sharper than the error. My FIRST version of the scan skipped odd j
"because 6b says so" and would have found nothing. A derivation that prunes a
search is exactly the claim that never gets tested -- so the pruned branch must
still be sampled. That is ERR-0012's rule (a check that cannot fail is not a
check) applied to search space instead of to assertions.

### 2026-08-29, late — the far-below failure has an address, and a closed form

The y-expansion criterion (knife_farbelow2) proves knives 4..8 by manifest
positivity and breaks at j = 9. The counts said 11, 30, 41, 71 negative monomials
out of 54k..179k -- two parts in ten thousand. Rebuilt on the fast engine
(lab/farbelow_negative_pattern.py, Q3Poly via knife_tail2.build_P, no new
derivation) the exceptions turn out to lie on a LINE:

  j=9 : 11 negatives, ALL at y-degree 7 = J-2, thL=0, K3=0, v=0..10
  j=10: 30 negatives, ALL at y-degree 8 = J-2, thL=0, K3=0, v=0..29
  j=11: 41 negatives, ALL at y-degree 9 = J-2, thL=0, K3 in {0,1}, v=0..37

One coefficient out of J, in one corner. And the reason is structural: in

  [y^k] N = (-1)^{J-1+k} den^k SUM_{i<=J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i} den^i e_{J-1-i-k}(A)

the coefficient k = J-1 has ONE term and k = J-2 has exactly TWO of opposite
sign -- it is the first difference in the family. Closed form, verified against
the assembled polynomial (j=6: 735 monomials; j=9: 1752; 0 mismatches both):

  c_{J-2} = den^{J-2} [ poch_1 s^2 den E_{J-2} - E_{J-1}(J-1)(tk_num + den(c+J-2)) ],
  poch_1 = (2n-2J+1)(2n-2J+2)/2.

So its sign is one explicit inequality, and the breakdown at j=9 needs no
computation to explain: the left side carries (2n-2J)^2 and shrinks as J -> n
while the right carries (J-1) and grows. The only non-elementary piece is
E_{J-1}/E_{J-2}, which Newton bounds -- the same tool as Theorem 5.

This is the first time the obstruction to uniformity in depth has an ADDRESS
rather than a size. Next: the natural repair is the pair
y^{J-2}(c_{J-1} y + c_{J-2}) >= 0, whose threshold in y is now writable in closed
form; whether it falls inside the physical range is unmeasured.

### 2026-08-29 — the repair candidate: one negative coefficient absorbed by its neighbours

With every y-coefficient nonnegative except c_{J-2}, N(y) > 0 on y >= 0 follows
from c_{J-3} + c_{J-2} y + c_{J-1} y^2 >= 0, i.e. c_{J-2}^2 <= 4 c_{J-1} c_{J-3}.
Measured at j = 9 over 512 region points: 6 have c_{J-2} < 0, and at all 6 BOTH
the discriminant form and the stronger log-concave form c_{J-2}^2 <= c_{J-1}c_{J-3}
hold. The log-concave form fails at 18 other points, all of them with
c_{J-2} >= 0, where there is nothing to repair.

So the far-below uniformity target is now two explicit polynomial statements:
(1) every c_k with k != J-2 is manifestly nonnegative; (2) where c_{J-2} < 0,
c_{J-2}^2 <= 4 c_{J-1} c_{J-3}. c_{J-1} and c_{J-2} are already in closed form.

MACHINE RULE, honoured: j = 10, 11, 12 were queued and I killed the run at 16:20
when free memory fell to 6.9 GB with cod26-cod (a game, windowed, 1.8 GB) and the
Firebird editor running. The founder's session comes first; the queue resumes
when the machine is free. Nothing is claimed from the unrun depths.

### 2026-08-29 — the general y-coefficient, verified, and why J-2 is the weak link

[y^k] N = (-1)^{J-1+k} den^k SUM_{i=0}^{J-1-k} (-1)^i E_{J-1-i} poch_i s^{2i} den^i
                                               e_{J-1-i-k}(A_i..A_{J-2})

checked against the assembled polynomial for EVERY k at j = 6: 3186, 2528, 1890,
1292, 735, 231 monomials at k = 0..5, 0 mismatches throughout.

And it explains the weak link without further computation. The highest power of s
sits at i = J-1-k, and that term's total sign is (-1)^{J-1+k}(-1)^{J-1-k} = +1:
the DOMINANT term is always positive. Manifest positivity is then "the dominant
term swamps the alternating rest", which is strongest at small k (it carries
s^{2(J-1-k)} with s ~ lam) and weakest at k = J-2, where it carries only s^2
against a term with none. k = J-1 is a single term and trivially safe.

So the two targets are not arbitrary: (1) "the dominant term wins" for k <= J-3 --
a ratio chain of the Theorem 5 kind -- and (2) the neighbour repair at k = J-2.

### 2026-08-29 — my own explanation refuted within the hour: no term dominates

I wrote that manifest positivity of c_k is the highest-s term swamping the rest,
which would have made the uniform proof a decay estimate. lab/dominant_term_probe.py
measured it as certified arb numbers and killed it: SUM_{i<J-1-k} T_i / T_{J-1-k}
runs from 3 to 3.2e8 for k <= J-3. The "dominant" term is usually the SMALLEST.

Why, once measured: each step in i gains s^2 den and loses one factor
A ~ T_cap den ~ lam^2 den -- the same size. The terms are comparable, so manifest
positivity is cancellation among comparable terms, not dominance.

The measurement paid anyway. At the weak link k = J-2 that ratio is 0.9997 to
1.0164: the two terms are equal to within a percent. That is exactly why this one
coefficient changes sign while the longer sums do not -- it is a difference of two
same-size quantities, with nothing else in the sum to absorb the swing.

Write-up corrected in place (FARBELOW_NEGATIVE_PATTERN.md), not deleted.

### 2026-08-29 — the repair holds at three depths

j = 10 and j = 11 landed after the machine freed up. The localisation holds --
every negative monomial at y-degree J-2 (30 at j=10, 41 at j=11) -- the closed
form for c_{J-2} checks with 0 mismatches at both, and the neighbour repair
c_{J-2}^2 <= 4 c_{J-1} c_{J-3} holds at every point where the coefficient dips:

  j=9: 6 negative points, 0 failures     j=10: 7, 0     j=11: 20, 0

33 points in all, and the stronger log-concave form holds at every one of them
too. Still not a proof, and j=12 is still unrun.

### 2026-08-29 — the parallel chat's answer: verified, useful, and it stops at the same wall

The founder put the root-bound question to a second assistant. Its answer is the
circular-region form of Grace-Szego, which does NOT need q real-rooted:
theta_max(p BOX q) <= B max Re zeta over the zeros of q, B = (n-2)^2/s^2 -- only
the rightmost REAL PART matters. Plus an explicit spectral-abscissa bound via the
Jacobi three-term recurrence (the Jacobi matrix has A_{k-1}C_k < 0, so the
Hermitian part is a real diagonal and the numerical range bounds Re y).

VERIFIED HERE, because untrusted input: (A) 0 violations in 144 cases; (C) 0
violations wherever eta < 1; and their control example reproduces to the digit
(eta = 0.03295786, lam > 6.886 at n=20, r=8, D=4).

WHAT IT BUYS. At the shore, (E) holds from lam/n = 7.75, 7.50, 7.50, 7.53 at
r = 2 for n = 8, 12, 20, 40 -- FOUR TIMES better than Theorem 9's 32n, by a
different mechanism. At r = n/4 it is 12-15n, still better.

WHERE IT STOPS. eta -> 1 as D grows, and eta < 1 at large D iff r < (2n+1)/4.
Past that depth the hypothesis is empty at every lam. So the deep knives -- where
uniformity in depth actually lives -- are untouched. Same wall, better corner.

Also: their (U) is exactly our Theorem 5 condition rederived from the coefficient
side, and their (W) is the criterion we already filed as circular in ERR-0015.
Their (Y) is not circular and is a small genuine relaxation; their Routh-Hurwitz
route (AC) is the strongest item and is untested.
