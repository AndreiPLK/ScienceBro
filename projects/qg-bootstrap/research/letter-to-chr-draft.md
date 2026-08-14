# Draft letter to Cheung / Hillman / Remmen — send only after founder approval

**To:** Clifford Cheung (Caltech), Aaron Hillman (Princeton), Grant N. Remmen (NYU)
(адреса найдём на страницах институтов перед отправкой)
**Subject:** The positivity island of your bootstrap family: its boundary in closed form

---

Dear Professors Cheung, Hillman and Remmen,

Your bootstrap paper (PRL 133, 251601) left a question I could not stop thinking
about: what happens to the positivity island of the (q, r, w) family at infinite
level depth. I spent the last days on it and ended up with more than I expected,
so I wanted to share the results before doing anything louder with them.

Tracking the top coefficients of the level-n residue polynomial through the
partial-wave projection gives exact sign laws for the near-leading trajectories.
The main one: sgn a_{n,n-1} = sgn[ n(r + (1+mu0)/2) + w ], for every level, every
mass shift, and every D > 3 — so nothing survives left of r = -(1+mu0)/2, and the
finite-depth erosion of the island is explained cell by cell (the nine cells that
vanish between n<=10 and n<=20 die at exactly n = 10w+1). The rest of the boundary
reduces to a short list of explicit curves — conjecturally complete, verified on
11,994 exact-rational verdicts across seven mass shifts with zero unexplained
mismatches. For q > 1, the depth at which unitarity kills the deformation follows
n_crit ~ 1.1 (q-1)^{-1/2}, which quantifies the q-tolerance of any finite scan
(q - 1 < 0.012 at depth 10). On the w = 0 slice everything matches the
Mansfield-Spradlin asymptotics; the w != 0 region appears to be new.

The paper, all exact-arithmetic code, and an adversarial falsification suite are
public: https://github.com/AndreiPLK/qg-island-edges (PDF in /paper). I am an
independent researcher working with an AI assistant — disclosed in full in the
paper — and every claim is either derived and independently reviewed, or labeled
as a conjecture with its evidence.

Two things I would value enormously: any correction, if I have misread part of
your construction; and, if the work seems sound to you, an arXiv endorsement for
hep-th — this would be my first submission there.

Thank you for a beautiful paper to build on.

Best regards,
Andrey Pluzhnik
ORCID 0009-0005-5660-2603 · andreiplk.github.io

---

## Почему так (для основателя)
- Крючок в первой строке: МЫ ответили на ИХ открытый вопрос (их Fig. 1, n<=10).
- Все числа — из статьи, ничего нового не выдумано.
- Честно: independent researcher + AI, «поправьте если я неправ» — это открывает
  двери, а не закрывает.
- Просьба endorsement — прямая, одной строкой, после сути (как учили: без кринжа).
- Не прошу соавторства/одобрения — только correction и endorsement.
