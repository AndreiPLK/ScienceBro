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
