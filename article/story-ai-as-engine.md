# Story A — The AI as an engine (draft)

*Framing: the human researcher did the science; the AI was the machinery that executed
it. Same facts as story B, different lens.*

---

On a Monday in August I decided to independently audit a striking claim: a neural
network that allegedly finds new black-hole geometries (the AInstein project,
arXiv:2607.05489). I did not have a lab. I had a gaming PC, one afternoon, and a
code-generation engine.

I wrote a specification: a research workbench with evidence ledgers, frozen
experiment protocols, deterministic claim gates, and an independent verifier that is
forbidden from importing the code it audits. Then I pointed the engine at it.

By 14:00 the scaffold existed: schemas, CLI, tests, a dashboard. I did not review
every line — I reviewed every *number*. The engine's job was to produce artifacts;
my job was to distrust them. That is why the first rule I gave it was: never mark
your own work as verified. Verification belongs to deterministic checks: analytic
Schwarzschild must come out vacuum to 1e-10, a deliberately corrupted metric must
fail, a fabricated citation must be caught. All of that runs in CI, not in anyone's
head.

The engine surfaced an anomaly within the first hour: the upstream training loss was
1.6e-10 while an independent curvature check of the same network said 3.3e-6 — four
and a half orders of magnitude apart. A lesser workflow would have shipped one of
those numbers. I ordered a measured decomposition instead of an explanation in prose.
The table came back: the upstream loss is *quadratic* in the residual; on a common
linear scale the two numbers agree to 0.7%. Not fraud — units. The audit instrument
was now calibrated, and the calibration is a reproducible proof pack, not a promise.

By evening the machine had: a verifier validated on known solutions through two
independent coordinate routes, a measured proof that float32 checkpoints inflate
curvature error 203-fold, and a frozen protocol for the real test — retraining the
authors' Schwarzschild baseline and stress-testing their Petrov type-I candidates on
hidden points. The engine also noticed, in passing, that the paper's supervised seed
model — trained to imitate the metric pointwise — has *worse* curvature than a
partially-trained physics-informed network. Fitting the values of a function is not
the same as fitting its second derivatives. That observation cost me nothing; the
engine made it while waiting for a training run.

What did the engine not do? It did not choose the target, did not decide what counts
as evidence, did not approve any claim, and cannot publish anything. Every VERIFIED
badge on my dashboard is backed by a SHA-256 attestation that dies automatically if
an artifact changes. The engine is powerful, tireless, and — by construction —
never trusted.

*(Status honesty: as of this draft, no AInstein candidate has been confirmed or
rejected. The verifier passed analytical known-answer tests; candidate evaluation is
not complete.)*
