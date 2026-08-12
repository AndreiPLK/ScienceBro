---
title: 'ScienceBro: an independent curvature verifier and proof-gate workbench for machine-learned spacetimes'
tags:
  - Python
  - general relativity
  - physics-informed neural networks
  - reproducibility
  - independent verification
  - Petrov classification
authors:
  - name: Andrey Pluzhnik
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Independent researcher
    index: 1
date: 12 August 2026
bibliography: paper.bib
---

# Summary

Neural networks are now routinely used to produce approximate solutions of the Einstein field
equations, and the quality of those solutions is normally reported using the very loss function
that was optimised to produce them. `ScienceBro` provides the missing outside instrument. Given
any callable that returns a metric $g_{\mu\nu}$ at a point, it computes the Christoffel symbols,
Riemann and Ricci tensors and the Kretschmann scalar by nested central differences in float64;
it forms the Weyl tensor, an orthonormal Lorentzian frame and the complex Weyl operator to
obtain the Petrov speciality index $S = 27J^2/(4I^3)$; and it classifies trapped surfaces from
the areal-radius gradient in a 2+2 split. It shares no code with the systems it audits: metric
values cross the boundary as plain arrays produced by a subprocess in an isolated environment.

The package also contains the discipline that makes such an audit checkable rather than
assertable. Stage statuses are computed by deterministic gates from artifacts with recorded
SHA-256 digests, never asserted in prose; validation thresholds are derived from a reproduced
known-answer baseline and then version-tagged before the results they judge exist; attestations
record the git commit, the environment lock hash and per-artifact digests, and invalidate
themselves automatically when an artifact changes. Failed runs are preserved alongside
successful ones.

# Statement of need

Verifying that a machine-learned metric solves the field equations means differentiating the
network output twice and evaluating curvature invariants — work that is rarely repeated by
anyone other than the authors of the model. Three practical hazards follow from
self-reporting. A reported residual is typically a sample average of a squared, weighted
contraction, so it can be small while pointwise curvature errors are not. It is computed with
the same differentiation kernel that shaped the optimisation, so implementation bugs cancel
rather than surface. And it is evaluated on the training sampling distribution. An external
evaluator with a *published* error floor removes all three hazards at once.

`ScienceBro` was built to make that evaluation cheap enough to be routine. Its floor is
measured and stated before use: Ricci residuals of order $10^{-10}$ on analytic Schwarzschild
in Schwarzschild coordinates and $10^{-8}$ in Penrose plus stereographic coordinates, a
speciality index of 1 to within $4\times10^{-16}$ on a type-D metric and to $1.7\times10^{-6}$
on a *trained network* imitating one, exact recovery of the Schwarzschild apparent horizon on
both an analytic and a trained control, detection and localisation of deliberately corrupted
metrics, a finite-difference step chosen by convergence sweep, and a measured requirement that
metric components be exchanged in float64 (float32 storage inflates the residual by a factor
203).

The first audit performed with it is included as a worked case study against the AInstein
black-hole search [@ainstein2026]. Five retrainings of the published configuration differing
only in random seed show that the algebraic type and the trapped region reproduce in five runs
of five, with the speciality index reproducible to 0.43 %, while the vacuum condition holds in
two of five with the independent residual spanning a factor 4.8 against a reported
training-loss spread of 1.21. That contrast is the concrete argument for the package: the
quantity a model reports about itself and the quantity an outside instrument measures were not
interchangeable in this case.

Existing tools in this space either belong to the systems being evaluated or target symbolic
general relativity rather than callable numerical metrics; `ScienceBro` is intended to sit
outside any of them, so that a claim about a learned spacetime can be checked by someone who
did not train it.

# Functionality

- `verifier.geometry` — Christoffel, Riemann, Ricci, Kretschmann, Einstein residual and
  signature checks from a metric callable, with an explicit step-size parameter.
- `verifier.petrov` — Weyl tensor, orthonormal tetrad, Weyl operator, algebraic invariants and
  the speciality index.
- `verifier.horizon` — areal radius, $\Xi$, null expansions and trapped-surface
  classification, reporting the time orientation as ambiguous where the coordinate time is
  spacelike rather than guessing it.
- `verifier.interface` — the isolation boundary: stencil recording, batched export of metric
  values from a foreign environment, and a tabulated metric callable built from the result.
- `sciencebro.proofgate` and the `sb` command line — stage verification from hashed artifacts,
  attestations, proof-pack export and integrity re-checking.
- A read-only dashboard that renders only what the repository files support.

# Quality control

The package ships known-answer tests against analytic Minkowski and Schwarzschild, negative
controls with deliberately corrupted metrics, cross-checks between independent formulations
(for example the areal radius read from the metric against an independent Lambert-W computation
of $r(T,X)$), a finite-difference convergence sweep, a precision comparison, and a gold
evaluation set covering citation verification and claim-gate behaviour. `uv run sb check` runs
linting, type checking, the full test suite and a repository integrity check.

# AI use disclosure

An AI agent wrote the code and executed the experiments under the author's direction. The
author set the research question, imposed the constraint that the agent may never mark its own
scientific work as verified, required that discrepancies be resolved by measurement rather than
explanation, and performed all external communication. The deterministic gates and the
preserved artifacts, not the agent's assertions, are what make the results checkable. The full
statement is in `AI_DISCLOSURE.md`.

# Acknowledgements

The audited upstream code is used under its own licence and kept isolated; its authors are
thanked for publishing it.

# References
