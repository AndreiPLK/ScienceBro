# System assessment, 18 August 2026

Every number below was measured on this commit, not recalled. Where a first
measurement was wrong it is stated, because a wrong measurement inside an
assessment is worse than no assessment.

The lab is one year of tooling and two weeks of a real research program. The
question this document answers is not "is it nice" but **where would this
system let a false result through**, and the answer is specific.

---

## 0. Verdict in one paragraph

The engineering layer is healthy and the science layer is productive, but they
are **not connected**. Every mechanical guard we own -- claim gates, evidence
records, experiment records, promotion rules -- is wired to the ARCHIVED project
(`ainstein-audit`), and the ACTIVE program that produced five papers and 525,346
certificates (`qg-bootstrap`) is registered nowhere. It has no `project.yaml`,
no claims, no evidence records, no validation records. `sb claim list
qg-bootstrap` answers `no claims recorded`. So the rules in `CLAUDE.md` protect
the work that is finished and do not touch the work that is live. That is
finding #1 and it outranks everything else in this document.

---

## 1. What was measured

| quantity | value |
|---|---|
| commits | 405 |
| tracked files / tracked bytes | 1051 / 202.7 MB |
| working tree | 3.2 GB (2.2 GB is the upstream venv, correctly git-ignored) |
| lab modules (`projects/*/lab/*.py`) | 82 |
| result artefacts (`qg-bootstrap/results`) | 163 JSON + Markdown |
| figures (`article/visuals/*.png`) | committed figure set + 5 video assets (108 MB) |
| papers | 5 (`paper` .. `paper5`), each with a built PDF |
| test functions / collected cases | 31 / 52 |
| `uv run sb check` | PASSES (ruff clean, mypy clean on 23 files, 52 tests, integrity ok) |

---

## 2. Findings, ranked by what they would cost us

### F1 -- CRITICAL. The active research program is outside the governance system

`projects/qg-bootstrap/` contains `lab/ results/ research/ evidence/ validation/
paper..paper5`. It does **not** contain `project.yaml`. Consequence chain:

* `sb project status qg-bootstrap` cannot run; `sb claim list qg-bootstrap`
  returns `no claims recorded`;
* the deterministic promotion gate `allowed_claim_promotion` -- which is
  correct, tested, and refuses to skip states, refuses abstract-only evidence,
  refuses `experimentally-supported` without a linked experiment, refuses
  `independently-validated` without a PASSING validation -- has **never been
  applied to a single statement in the QG program**;
* the evidence contract is enforced for six AInstein records and for zero QG
  records, while the QG papers make external factual claims;
* nothing mechanical distinguishes "525,346 certificates, zero failures" (an
  exhaustive machine check) from "measured at one value of D" (which produced
  two withdrawn claims this week).

This is exactly the class of failure the system was built to prevent, and the
system is pointed at the wrong project. **It is also the cheapest of the big
fixes**: the machinery exists and is tested; what is missing is the registration
and the records.

### F2 -- HIGH. 5 of 82 lab modules have a self-check (6 %)

Modules carrying an explicit `self_check` / `self_test` / `verify_against`:
`contour_lib`, `jacobi_normal_form`, `knife_closed_form`, `hp_scan`, `long_scan`.

It is not a coincidence that those five carry the load-bearing results, and it
is not an accident that the two withdrawn claims and the refuted lemma came from
elsewhere. But 77 modules emit numbers with nothing checking them, and several
of those numbers reached the founder.

The rule that works is already proven in the five: **a fast path must reproduce
a slow path exactly on a grid before it is used**. It is not written down as a
requirement anywhere.

### F3 -- HIGH. 96 of 163 result artefacts (59 %) are never referenced

They appear in no paper, no doc, no report. Some are superseded, some are dead
ends, some may be the only record of a real measurement. From the outside they
are indistinguishable, and "never delete raw results" (correct) has therefore
produced a sediment in which a wrong old file looks exactly like a right new
one. The missing half of the rule is: never delete, but always **mark**.

### F4 -- MEDIUM. 48 of 158 JSON results (30 %) carry no provenance

The experiment contract requires git commit, command, seed, runtime on every
run. `lab/provenance.py` implements this well -- it even records whether the
CODE tree was dirty while ignoring churn in `results/`, which is the right
distinction -- and 110 artefacts use it. The other 48 predate it or bypassed it.

*Correction to my own first measurement: I initially reported 158 of 163 as
unstamped, because I searched for a key named `git_commit` while `stamp()`
writes `git`. The real figure is 48.*

### F5 -- MEDIUM. 59 of 82 lab modules are one-shot scripts nobody imports

Only a handful (`contour_lib`, `jacobi_normal_form`, `knife_closed_form`,
`provenance`, `keystone_beta`) are libraries. The rest are scripts that were
written for one question and left. That is defensible for exploration and
indefensible as a permanent state: shared logic gets re-derived, and a fix in
one copy does not reach the others.

### F6 -- MEDIUM. The topic registry is aspiration, not state

`sb topic list` shows ten topics in `needs setup` (eccentric surrogates, PTA,
GWTC-5, DESI, TESS ...) that have never been worked. They are ambitions parked
in a status table, so the one line that matters -- the active program -- is
buried among nine that are not.

### F7 -- OK. Repository hygiene is sound

203 MB tracked across 1051 files; the 2.2 GB upstream venv and the 90 MB
upstream checkout are both correctly ignored. The tracked weight is media
(108 MB of mp4, 56 MB of png) -- appropriate for a lab whose output includes
figures, though it is worth watching.

### F8 -- OK. The mechanical guards work, and two of them are new this week

* `uv run sb check` is green end to end.
* `.githooks/pre-commit` (with `core.hooksPath` set) runs the guards on every
  commit and has already blocked a bad one.
* `tests/test_fast_engine.py` fails the build when a NEW computational module
  uses the slow engine without an `# ENGINE-OK` justification; its debt register
  may shrink, never grow. Verified by planting a deliberate violation.
* `tests/test_english_only.py` (added today) does the same for language:
  43 pre-existing files are in the register, and any new Cyrillic fails the
  build.

The shape is the right one and should be the template for F2 and F4: **a rule
that is not a test is a wish.**

---

## 3. State of the science, stated honestly

**Proved, machine-checkable:**

* knife 4 is positive on `4 <= n <= 1000`, `1/10 <= lam <= 120`,
  `4 <= D <= shore` by exact Bernstein subdivision (128,514 boxes, 0 open, 6949 s
  -- this run finished while the assessment was being written and supersedes the
  earlier 400/60 figure). The unbounded tails are NOT closed: the two runs
  attempting them produced zero output in two hours and were killed, because
  `lab/knife4_tails.py` hangs in `sympy.simplify` (backlog B6). The earlier
  single-box closure of the n-tail for `lam <= 30` stands.
* closed forms per knife verified against the exact engine, j = 2..6;
* the Jacobi normal form reproduces the independent exact value on 4500 cells,
  0 mismatches; every fast path reproduces the slow one on 891 cells, 0
  mismatches;
* 525,346 individual coefficients computed exactly, 0 negatives.

**Open:** the uniform-in-j theorem. My route to it (the endpoint lemma) is
**dead** -- refuted by an outside reader with a counterexample at
`n = 24, lam = 10, D = 177`, reproduced digit for digit by our own engine
(`docs/ERRATA.md`, ERR-0005). Ten mechanisms are recorded closed in
`results/OPEN_PROBLEM.md`.

**Live route:** prove non-negativity only AT the shore and descend in dimension.
Consistency checks so far: 0 negative Gegenbauer coefficients from 20 % to 100 %
of the shore across three `(n, lam)`; connection coefficients positive, 180
checked, 0 negative. Neither is a proof; both are the right kind of evidence.

**The methodological lesson, already priced:** my grid was ABSOLUTE (D from 4 to
70) under a boundary that moves (187.5 at that lam), so every test sat below
40 % of the boundary and the counterexample lives at 94 %. Standing rule now:
under a moving boundary, sample in FRACTIONS of that boundary and include 0.99.

---

## 4. What I recommend, in order

Ranked by (risk removed) / (hours). I have not executed these -- they change the
structure of the repository and that is the founder's call.

| # | action | cost | removes | state |
|---|---|---|---|---|
| 1 | register `qg-bootstrap`: `project.yaml`, evidence records, experiment records, and the real claims entered at the state the gate allows | ~3 h | F1 -- the whole overclaim surface on the live program | BACKLOG B1, trigger: before the next paper goes out |
| 2 | index every artefact and require provenance on new ones | ~40 min | F4 + F3, permanently | **DONE** -- `results/MANIFEST.yaml`, `tools/results_manifest.py`, `tests/test_results_manifest.py` |
| 3 | classify the 82 `unreviewed` artefacts | ~2 h | the remaining sediment | BACKLOG B2, on contact |
| 4 | promote "fast path must reproduce the slow path" from habit to a required `self_check` | ~2 h | F2, the class that produced the withdrawn claims | BACKLOG B3 |
| 5 | move the nine untouched topics into `docs/BACKLOG.md` | ~15 min | F6 | BACKLOG B4 |

Item 2 was done immediately because it was cheap and because it is a test, and
this week has shown twice that only tests survive contact with a working night.
The design point worth keeping: the status of an artefact lives in an index
BESIDE the results, never inside them -- editing 163 raw files to add a field
would violate the immutability rule the index exists to serve. My own first plan
got this wrong.

Everything else is parked in `docs/BACKLOG.md` with an explicit trigger, because
the North Star caps infrastructure at 20 % of effort and the theorem is open.

---

## 5. What I am NOT recommending

* **Do not retrofit provenance into the 48 unstamped artefacts.** They were
  produced by commits we can still identify from git history; rewriting them now
  would be manufacturing provenance rather than recording it. Mark them
  `provenance: absent` and leave them.
* **Do not refactor the 59 one-shot scripts into libraries.** Most answered a
  question that is now closed. Extract only when a second caller actually
  appears.
* **Do not delete anything.** Every finding above is solved by marking, not by
  removing.
