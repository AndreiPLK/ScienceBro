# Release note — what is being released, and what is not

**Version:** v0.1.0 — instrument and case study
**Date:** 2026-08-12

## What this release is

A **software and data release**, not a scientific claim release.

1. **An independent verifier for machine-learned spacetimes**
   (`projects/ainstein-audit/verifier/`): finite-difference Ricci and Kretschmann from a
   metric callable, the Weyl operator and Petrov speciality index, trapped-surface
   diagnostics, and an isolation boundary so it never imports the code it audits.
   Calibrated on analytic Minkowski and Schwarzschild, with negative controls, a
   finite-difference convergence sweep, and a measured precision requirement.

2. **A proof-gate workbench** (`sciencebro/`): stage statuses computed from artifacts with
   recorded SHA-256 checksums, validation thresholds that are frozen and version-tagged
   before the results they judge exist, and attestations that invalidate themselves when an
   artifact changes.

3. **A completed case study** (`projects/ainstein-audit/`): the first independent audit run
   with it, against arXiv:2607.05489, including every failed run.

## What this release is NOT

- **Not a peer-reviewed result.** No qualified relativist has reviewed it.
- **Not a scientific verdict on the audited paper.** Its trained candidates were never
  published, so only the published configuration could be audited. `sb release check`
  refuses to mark any claim release-ready, and that refusal is correct: the gate requires
  validation by a party independent of the authors of this repository, which has not happened.
- **Not a discovery.** All three properties measured in the candidates are explicit training
  targets of the audited objective.

## The measurements a reader can check

- Instrument floor: ~1e-10 on analytic Schwarzschild in Schwarzschild coordinates, ~1e-8 in
  the audited paper's own coordinates, with the speciality index reading 1 to 4e-16 on a
  type-D metric and to 1.7e-6 on a *trained network* imitating one.
- Five retrains of the published black-hole configuration differing only in random seed:
  2 of 5 satisfy vacuum, Petrov type I and trapping simultaneously; type I and trapping
  reproduce 5 of 5 (speciality index reproducible to 0.43 %); the vacuum residual spans a
  factor 4.8 while the reported training loss spans 1.21.
- An exploratory, not pre-registered observation, recorded as a lead: across those five runs
  the reported loss ranks the runs in the opposite order to independently measured vacuum
  quality (Spearman −0.90, two-sided p = 0.037, n = 5).

Full report: `projects/ainstein-audit/reports/RELEASE_REPORT.md`.
Plain-language summary: `article/one-pager.html`.
AI use: `AI_DISCLOSURE.md`.

## Licensing

This repository is MIT. The audited upstream code is GPL-2.0 by its LICENSE file while its
`pyproject.toml` declares MIT; the conflict is documented in `vendor/upstream-manifest.yaml`
and the upstream checkout is kept isolated. No upstream code is copied into this repository.

## How to publish it (human actions, deliberately not automated)

```bash
uv run sb check                       # lint, types, tests, integrity
uv run sb verify-all ainstein-audit   # stage statuses from hashed artifacts
git log --oneline | head -20          # review what is being made public
```

Then create the GitHub repository, push, connect Zenodo, cut a release, and write the
resulting DOI into `projects/ainstein-audit/release/ZENODO_DOI.txt`. Metadata for the
Zenodo form is prepared in `projects/ainstein-audit/release/ZENODO_METADATA.json`.
