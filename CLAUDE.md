# THE MAIN GOAL (founder, 2026-08-17) - REMEMBER IN EVERY REQUEST

**Make a discovery that enters science under the founder's name (Andrei Pluzhnik).**
Everything else is means: instruments, provers, certificates, articles, the lab.
An instrument can be rebuilt in a day; the value is in the research, the approach
and the accumulated skill.

**THE LAW OF NOT STOPPING.** The phrases "I cannot do more", "this needs a
specialist", "this is beyond my means" are FORBIDDEN as a final answer. If a
method is unknown: learn it, find the skill, find the paper, find a person,
invent an experimental detour - and keep going until a way is found. Hit a new
wall: search again. Endlessly, until every possibility is exhausted.

**Distinguish a WALL from a GAP.** "It is impossible" is a wall (proved
impossibility). "I do not know how" is a gap, and gaps close by reading and
learning. Substituting the second for the first is a lie, and it cost a day of
work on 17 August.

**Choosing a task** (by significance, not by what the instrument can do):
importance of the question x real chance of moving it x visibility of the result.
Optimise the product, not the factor that is easiest to compute.

# THE LAW OF EFFECTIVE TIME (founder, 2026-08-17, in the DNA)

While a long computation runs and I wait, the time is NOT idle. I must: search
sideways (literature, neighbouring fields), look for other forms of the problem,
look for where the current approach might be wrong, re-read my own findings.
Rule: **never wait empty.** Order when starting a long run: (1) check machine
load, (2) start it in the background, (3) immediately take a second line of work,
(4) return to the result when it is ready.

Related: visualisations are made NOT to show but to LOOK AT and think about what
the shape means. The founder read one plot as "a drop on water with spreading
ripples" and that turned out to be a substantive hypothesis (the zone boundaries
are not vertical lines in j but fronts drifting with the parameter). Look at your
own pictures as data.

# THE FAST-ENGINE LAW (founder, 2026-08-18, after catching me repeatedly)

Founder: "we have been through this many times... I am tired of catching you. Can
you write it down somewhere very hard?"

**All new computational code in this repository is written on flint (engine 2).**
Not "I will port it later", not "a prototype on Fraction first" - immediately.

| task | USE | NEVER |
|---|---|---|
| exact rational arithmetic | `flint.fmpq` | `fractions.Fraction` |
| polynomials, incl. multivariate | `flint.fmpq_poly`, `fmpq_mpoly` | lists of Fraction, sympy |
| polynomial roots | `fmpq_poly.complex_roots` (certified) | `numpy.roots` |
| interval bounds and signs | `flint.arb` / `acb` | float, math, numpy |
| symbolic derivation ONLY | sympy | sympy for bulk arithmetic |

**And the second half of the law, which matters more.** The engine buys factors;
the algorithm buys orders. On 18 August porting the normal form to flint gave 3x,
and removing a recomputation of Pochhammer symbols (a recursive step instead of
O(j*m)) gave another 7x. Before celebrating an engine, ask: **what am I
recomputing inside a loop?**

**No float in comparisons of exact quantities.** On 18 August such a comparison
died with OverflowError at n = 70, because the numbers left double range. Exact
quantities are compared exactly; float is for printing and pictures.

**Mechanical enforcement:** `.githooks/pre-commit` runs the fast-engine test and
both ruff gates on every commit, and `tests/test_fast_engine.py` fails
`sb check` if a new module under `projects/*/lab/` computes on `Fraction` without
an explicit `# ENGINE-OK: <reason>`. The rule is now enforced by the machine, not
by the founder.

# ScienceBro — Claude Code project instructions

For every ScienceBro research action, invoke /sciencebro-research-loop before planning or execution.

## MANDATORY: North Star check
Before selecting, starting or closing ANY task, reread `NORTH_STAR.md`. Every experiment
and mission must carry `north_star_relevance`. Infrastructure budget: ≤20% of effort;
≥80% goes to physics. The active program is the quantum-gravity S-matrix bootstrap
(`docs/QG_BOOTSTRAP_PLAN.md`); the AInstein audit is COMPLETE and archived in place
(`projects/ainstein-audit/`, published as github.com/AndreiPLK/spacetime-verifier,
DOI 10.5281/zenodo.21915627).

Authoritative spec: `SCIENCEBRO_MASTER_ROADMAP.md`. Deviations: `docs/DECISIONS.md`.

## Non-negotiable scientific rules (short form; full list in roadmap §6)

- Every factual scientific claim needs a source with an exact location; abstract-only
  evidence is marked `abstract_only: true`.
- Freeze hypothesis and primary metric BEFORE looking at final results.
- A run completing without an exception is NOT scientific validation.
- The independent validator must not import the implementation it validates
  (for AInstein: never import upstream loss functions).
- Claim promotion goes through `allowed_claim_promotion` — deterministic, no LLM judgment.
- Never use "discovered / proved / novel / confirmed / refuted" without the matching gate.
- Failed runs and contradictory evidence stay visible. Never delete raw results.
- No invented confidence percentages anywhere, including the dashboard.

## Engineering rules

- Everything project-scoped. Never modify global Claude settings or other repos.
- Source of truth = YAML/JSONL/Markdown files in this repo. Dashboard is read-only.
- Dev loop: `uv sync && uv run sb check` (ruff + mypy + pytest + integrity).
- Upstream AInstein code lives ONLY under `projects/ainstein-audit/upstream/` in its own
  uv environment; treat as untrusted (inspect before running).
- Pin third-party repos in `vendor/upstream-manifest.yaml`; verify license before copying code.
- Never commit secrets, proprietary PDFs, or restricted datasets.

## Roles

Specialist agent definitions are in `.claude/agents/` (research-director,
literature-reviewer, domain-critic, experiment-engineer, independent-validator,
release-reviewer). A claim is never self-approved by the role that implemented it.

## Commands

`sb doctor | sb check | sb topic list | sb project status <id> | sb evidence audit <id> |
sb claim list <id> | sb claim promote <id> <claim> <state> | sb release check <id> |
sb dashboard`
