# Draft reply to Dr. Hirst (2026-08-13) — send only after founder approval

**To:** Edward Hirst (reply-all: tsg, a.g.stapleton)
**Subject:** Re: Independent check of your AInstein results

---

Dear Ed,

Thank you for the warm and fast reply — and for the point about the test set. You
were right to push on it, so I redid it properly before answering.

I re-ran the vacuum evaluation with 2000 hidden points (your paper's standard)
instead of 24, same evaluator and thresholds, for five retrained seeds. Every
verdict stayed the same as in the small sample: seeds 124 and 126 come out
approximately Ricci-flat (medians 0.222 and 0.187 against my Schwarzschild-derived
threshold 0.286), seeds 123, 125 and 127 do not (0.96, 0.38, 1.18). So across five
seeds: 2 of 5 converge on the vacuum measure, and the spread sits almost entirely
in that measure — the Petrov type-I and trapped-surface targets are hit by all
five. That matches your description of the method as statistical, and I now have
it quantified.

Everything (evaluator, configs, seeds, raw results) is public, in case it is
useful to you or your students: github.com/AndreiPLK/spacetime-verifier,
DOI 10.5281/zenodo.21915627.

And I take your point about other Petrov classes — that direction tempts me too.
If the Section IV.D checkpoints ever become easy to share, I would still be glad
to run them through the same pipeline; my retrained seeds are the only thing
standing between my numbers and your actual results.

Best,
Andrey

---

## Почему так (для основателя)
- Отвечаем ДЕЛОМ на его единственную критику: 24 → 2000 точек, вердикты не
  изменились — это сильнейший ход, он показывает уровень.
- «2 of 5 converge... quantified» — вежливо фиксируем нашу главную находку
  (нестабильность по сидам) как согласованный факт, его же словами («statistical»).
- Ссылка на репо+DOI: пусть смотрят сами, это и есть PR.
- Просьба о чекпоинтах повторена мягко, одной строкой, без давления.
- Никакого кринжа, ни слова про лицензии, коротко.
