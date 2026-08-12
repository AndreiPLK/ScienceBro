# FINAL letter — copy-paste into Gmail. Attach: article/visuals/seed-variability.png

**To:** ehirst@unicamp.br, tsg@math.uni-bonn.de, a.g.stapleton@qmul.ac.uk
**Subject:** Independent reproduction of AInstein (2607.05489) — may I evaluate your trained candidates?

---

Dear Dr. Hirst, Dr. Schettini Gherardini, and Dr. Stapleton,

I really enjoyed your AInstein black-hole paper and decided to reproduce it
independently — I think work like yours deserves a careful outside check, and I'd
like the check to be fair to you.

So far I have built an independent curvature evaluator (finite differences, float64,
no dependence on your training code) and validated it on analytic Schwarzschild and
Minkowski down to ~1e-8 in your own Penrose + stereographic coordinates. I then
retrained your committed `blackhole` configuration and evaluated the results on
hidden points. My re-training runs vary noticeably from seed to seed (see the
attached comparison against my reproduced Schwarzschild baseline), so I don't want
to judge the paper by my retraining luck.

Would you be willing to share the trained checkpoints (and exact configs/seeds)
behind the Petrov type-I candidates of Section IV.D? I would run them through the
same independent evaluation and send you the full results before making anything
public — hopefully a useful independent verification of your findings, and of course
I'd be happy to hear anything I've misread about your setup.

Best regards,
[ТВОЁ РЕАЛЬНОЕ ИМЯ]
[город, страна — по желанию]

---

*Attachment: seed-variability.png (baseline vs two retrained candidates, independent
hidden-point residuals).*
