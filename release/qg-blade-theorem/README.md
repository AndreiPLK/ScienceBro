# The Blades Never Touch the Shore

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21948833.svg)](https://doi.org/10.5281/zenodo.21948833)

**Paper:** `paper/main.pdf` (LaTeX source and figures alongside).
Sequel to [The Shore of Closed-String Gravity](https://doi.org/10.5281/zenodo.21944818)
and [A Master Positivity Formula](https://doi.org/10.5281/zenodo.21947272).

## The theorem

For the CHR graviton family, the second knife (the j=3 trajectory
a_{n,2n-6}) never cuts into the region allowed by the near-leading envelope
min_k T_k(λ): for every level n and every λ > 0, its negativity window —
when it exists — lies strictly above the shore. What was a 3-million-point
battery in the master-formula paper is now a proof.

## Why it is delicate

In the scaling limit the blade cone is EXACTLY tangent to the shore
asymptote D = (12+4√3)λ: the tangency discriminant of
6ρ² − (12+4√3)ρ + (8+4√3) vanishes identically at ρ* = 1+1/√3. The theorem
survives because windows only exist for ρ ≤ √(5/3), strictly inside the
tangency (`media/tangent-fleet.png`).

## The proof, mechanically

Several hundred positive-coefficient certificates in exact arithmetic
(`lab/blade_proof.py`, one command, per-cell log): envelope branches
k=3..45 for λ ≤ 26.1, and four lemmas for deep water (no shallow levels;
window containment s ≤ (4/3)(m+3); shore below the asymptote; asymptote
below the blades), the last two over Q(√3).

## Honest status and the bug the review caught

An independent adversarial review audited the full chain and found exactly
one defect: a coverage gap in the prover's escalation loop — 740 cells
skipped while the script reported success. The gap was fixed; the reviewer's
own battery (`lab/attack_blade_theorem.py`, sharing no code with the
prover) then re-certified every cell including the formerly uncovered ones:
exit 0, no counterexample. The lesson is preserved in the log: an exit code
proves what a script checked, not what it covered. Completeness for the
higher knives (j ≥ 4) remains a conjecture with a clean 3M-point battery.

## Reproduce

```
python lab/blade_proof.py            # the whole proof (ALL CERTIFIED, exit 0)
python lab/attack_blade_theorem.py   # the adversary's independent battery (exit 0)
python lab/bruteforce_recheck.py     # 60,000-point stress test (min margin 2.18)
```

## Explain it to anyone

The shore is where theories of gravity die; the blades are the extra danger
zones above it. We had checked three million points; checking is not
knowing. This is the proof: no blade, anywhere along the infinite coast,
ever touches the water — even though, infinitely far out, the fleet sails
exactly parallel to the shore, tangent to it, zero angle. Every actual ship
is confined strictly inside the wake. Closest pass: about two dimensions.

## AI disclosure

Research conducted by the author with an AI research assistant (Claude,
Anthropic); the proof was adversarially reviewed (one real coverage bug
found, fixed, and independently re-verified — `research/blade-theorem-review.md`).

## License

MIT (code and text). Figures and media: CC BY 4.0.
