# A Master Positivity Formula for the CHR Graviton Family

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21947272.svg)](https://doi.org/10.5281/zenodo.21947272)

**Paper:** `paper/main.pdf` (LaTeX source and figure alongside).
Companion works: [The Island Has Edges](https://doi.org/10.5281/zenodo.21934462)
(open string), [The Shore of Closed-String Gravity](https://doi.org/10.5281/zenodo.21944818)
(closed string; this paper is its direct sequel).

## The result in one line

For every trajectory l = 2n−2j of the CHR graviton family:

sign a_{n,2n−2j} = (−1)^{j−1} · sign Σᵢ (−1)ⁱ Ê_{2(j−1−i)}(n) · (2n−2j+2i)!/(i!·2ⁱ) · s^{2i} · Π_{r=i}^{j−2}(D+4n−4j−1+2r)

with s = λ+n−1 and Ê the doubled-root symmetric integers. The published
T_n law is rung j=2; rung j=3 cuts finite *windows* of dimensions (for the
string the first window is D∈(26.2, 30.3) at level 7 — confirmed by exact
evaluation); all rungs verified.

## Honest status

- The formula is **derived** (residue roots + exact monomial–Gegenbauer
  integral), not fitted, and passed: 21/21 symbolic bracket matches (j≤5),
  702/702 sign grid incl. the never-extracted j=6, and an independent
  adversarial review with its own from-scratch evaluator: 4,060/4,060 signs
  incl. odd and non-integer D (`lab/attack_master.py`, exit 0).
- Completeness of the j=2 envelope remains a **conjecture**; it now survives
  3,053,832 exact verdicts over every trajectory constraint (l≥2) at every
  integer D inside the conjectured-allowed region (n≤40, λ≤50).

## What is here

- `lab/` — bracket extractor (`tj_bracket.py`), law checkers, the
  completeness sweep, and the independent critic's attack suite
  (`attack_master.py`, written without access to the lab code).
- `results/` — all artifacts with run metadata (brackets, checks, sweeps).
- `research/` — the derivation note and the adversarial review verdict.
- `media/` — the blades figures (close-up and zoom-out).

## Reproduce

```
python lab/attack_master.py            # independent falsification suite (exit 0)
python lab/t2n6_law_check.py           # blind check of rung j=3 (2052/2052)
python lab/master_completeness_scan.py # the 3M-point completeness sweep
```

## Explain it to anyone

Our previous paper found the cliff where theories of gravity die as you add
dimensions. This paper finds the formula for every other way to fall — and
shows each one is a "window" that hangs strictly above the cliff line, like
blades floating over a shore, never cutting into the living land. Three
million exact checks; not one trapdoor on the safe side.

## AI disclosure

Research conducted by the author with an AI research assistant (Claude,
Anthropic); the derivation passed an independent adversarial review
(`research/master-formula-review.md`) whose attack code was executed with
exit 0. See `AI_DISCLOSURE.md`.

## License

MIT (code and text). Figures and media: CC BY 4.0.
