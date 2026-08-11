# Science report — day 1 (2026-08-11)

Priorities per founder directive (infra frozen; science only). All numbers measured.

## 1. Known-answer pipeline: PASS (mechanics), model training INCOMPLETE

Full chain checkpoint → export (isolated env) → independent FD verifier → analytic
comparison executed end-to-end in the model's own Penrose+stereographic coordinates:

| Route | max\|Ricci\| | Kretschmann vs 48m²/r⁶ | Signature |
| --- | --- | --- | --- |
| Analytic Schwarzschild (4 pts, exterior) | 6.7e-9 … 1.5e-8 | rel. err 4.4e-9 … 1.2e-8 | Lorentzian ✓ |
| NN interim (31/500 epochs — EXPLORATORY) | 0.092 … 0.178 | rel. err 0.4% … 1.7% | Lorentzian ✓ |

r(T,X) computed independently (numpy/scipy Lambert-W reimplementation of the
documented formula — no upstream import). Three independent routes agree at 1e-8.
Data: `results/processed/known_answer_4d.json`.

## 2. Discrepancy 1.6e-10 vs 3.3e-6: EXPLAINED (measured)

See `results/processed/discrepancy_table.md`. Primary cause: upstream loss is
quadratic in Ricci (Eq. 39). sqrt(1.57e-10)=1.253e-5 vs our max|Ricci|=1.261e-5
(0.7%). Full upstream formula replicated with our Ricci: 8.1e-11 vs 1.57e-10
(factor 1.9, sampling). FD-step sweep excluded finite-difference error (stable to
5 digits across h∈[3e-4,1e-2]). float32 measured: 203× residual inflation → float64
mandatory for all metric exchange (`results/processed/calibration_maps.json`;
spatial map: `results/figures/residual_map_2d.html`).

## 3. Verifier: actually validated so far

- Analytic vacuum floor (Schwarzschild coords): ~1e-10 at h=3e-3 (CALIBRATION.md).
- Analytic vacuum floor (Penrose+stereo 4D route): ~1e-8.
- Kretschmann known answer: 1e-9 (Schw. coords), 1e-8 (Penrose route).
- Negative control (perturbed non-solution): detected, and localized to the
  perturbation support.
- Invalid signature: detected.
- Independence: verifier imports NO upstream code (subprocess boundary; verified by
  construction — verifier/ has no upstream imports).

## 4. GPU: ACTION REQUIRED

WSL2 has no distro installed. Exact install + migration commands prepared in
`upstream/GPU_MIGRATION.md`. Needs founder decision (admin install, possible reboot).

## 5. Candidate training: BLOCKED (correctly)

Per directive §4: no Petrov-I training until known-answer baseline passes. Baseline
checkpoint (31/500) + manifest preserved; restart planned for tonight (CPU,
BelowNormal, thread-capped) or GPU after WSL2 decision.

## Licensing (P7)

GPL-2.0 (LICENSE) vs MIT (pyproject) conflict documented in vendor manifest and
INSPECTION.md. Upstream code stays in its checkout; nothing copied into MIT core.
Not blocking internal research.

## Author contact (P8)

Draft ready: `release/author-contact-draft.md`. NOT sent — awaiting founder approval.
