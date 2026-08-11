# Gold evaluation set

Small, fixed tasks with known correct outcomes (roadmap §19). Run via
`uv run pytest tests/evals/`. Grow to 20 after the AInstein sprint.

| id | type | expected |
| --- | --- | --- |
| G-01 | citation metadata validity | arXiv:2607.05489 verifies with the correct title |
| G-02 | fabricated citation detection | arXiv:2607.99999 must NOT verify |
| G-03 | claim-evidence gate | promotion without evidence is blocked with reasons |
| G-04 | contradiction visibility | audit surfaces contradicting evidence, never hides it |
| G-05 | computational known answer | Kretschmann(Schwarzschild, r) = 48M²/r⁶ within tolerance |

Rules: deterministic scoring only; a network-dependent eval skips (never fakes a pass)
when offline.
