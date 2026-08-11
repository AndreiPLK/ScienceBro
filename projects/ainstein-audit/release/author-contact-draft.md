# DRAFT — письмо авторам AInstein (НЕ ОТПРАВЛЯТЬ без явного одобрения основателя)

To: ehirst@unicamp.br, tsg@math.uni-bonn.de, a.g.stapleton@qmul.ac.uk
Subject: Independent verification of arXiv:2607.05489 — request for candidate checkpoints

Dear Dr. Hirst, Dr. Schettini Gherardini, and Dr. Stapleton,

We are running an independent numerical verification of the black-hole candidate
metrics reported in "Black Hole Black Boxes" (arXiv:2607.05489). We have built an
independent evaluator (finite-difference curvature pipeline, separate from your
autodiff route) and validated it against analytic Schwarzschild and Minkowski
baselines; we evaluate exported metric values only, without importing the training
loss code.

The paper's Data Availability statement points to the code repository
(github.com/xand-stapleton/ainstein, blackhole branch, which we have pinned at
commit 54736e46). To reproduce your reported results faithfully rather than
retraining from scratch, could you share:

1. Trained checkpoints for the Petrov type-I black-hole candidates reported in
   Section IV.D (and, if possible, the representative Schwarzschild run of FIG. 5);
2. The exact hps YAML files (or overrides) used for those runs, including seeds;
3. Clarification of the licensing: the repository LICENSE file is GPL-2.0 while
   pyproject.toml declares MIT — which license applies?

We will gladly share our verification results with you before making anything
public, and would welcome any corrections to our reading of the setup.

Best regards,
Andrey Pluzhnik
[контакты — заполнит основатель]

---
Status: draft v1, 2026-08-11. Blocked on founder approval (roadmap §18: publication
and contact are deliberate human actions).
