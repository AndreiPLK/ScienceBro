# Backlog

Work that is real but deliberately not being done now. Parked here so it stops
occupying either the active registries or my attention. Nothing is listed unless
I would actually do it.

North Star discipline: infrastructure gets at most 20 % of effort. Everything in
section 1 is infrastructure, which is why it is parked rather than scheduled.

Last reviewed: 18 August 2026.

---

## 1. From the system assessment (docs/SYSTEM_ASSESSMENT_2026-08-18.md)

### B1. Register `qg-bootstrap` in the governance system -- CRITICAL, ~3 h

The active program has no `project.yaml`, no claims, no evidence records, no
validation records, so the deterministic promotion gate has never been applied
to it. Needs: `project.yaml`, evidence records for the published papers,
experiment records for the certified runs, and the real claims entered at the
state the gate actually allows.

**Trigger: do this before the next paper goes out.** A public claim from an
unregistered project is exactly the failure the gate exists to prevent. Until
then the risk is contained, because nothing new is being published.

### B2. Classify the 82 `unreviewed` artefacts -- ~2 h

`results/MANIFEST.yaml` now indexes all 166 artefacts; 82 are `live`
(referenced somewhere), 2 are `retracted`, 82 are `unreviewed`. The index makes
the sediment *visible*, which was the urgent half. Draining it is not urgent.

**Trigger:** classify a file the moment it is consulted, not in one sitting.
An artefact nobody consults does not need a verdict.

### B3. Require a self-check in modules whose numbers reach a paper -- ~2 h

5 of 82 lab modules carry an explicit self-check, and those 5 produced the
load-bearing results. The rule that works -- *a fast path must reproduce a slow
path exactly on a grid before it is used* -- is habit, not a requirement.

Hard part: deciding mechanically which modules "reach a paper". Probably: any
module named in a `release/` package.

### B4. Move the nine untouched topics out of the active registry -- ~15 min

`sb topic list` shows ten topics in `needs setup` (eccentric surrogates, PTA,
GWTC-5, DESI, TESS, ...) that have never been worked, burying the one line that
matters. They are ambitions, and they belong here:

* eccentric-surrogate adversarial failure map
* PTA gravity spectrum overlap curve
* GWTC-5 posterior-aware anomaly catalog
* DESI dark-energy leave-one-dataset atlas
* TESS calibrated candidate ranking

(plus the remaining `needs setup` entries visible in `sb topic list`)

### B5. Watch the tracked media weight -- monitoring only

203 MB tracked, of which 108 MB is mp4 and 56 MB png. Fine today. If it doubles,
move video to release assets rather than the repository.

---

## 2. Engineering debt with a live guard

These already have a mechanical brake, so they can only shrink:

| register | count today | guard |
|---|---:|---|
| `tests/english_only_debt.txt` | 43 files | `tests/test_english_only.py` |
| `tests/fast_engine_debt.txt` | see file | `tests/test_fast_engine.py` |
| `tests/provenance_debt.txt` | 44 artefacts | `tests/test_results_manifest.py` |

Rule for all three: translate / port / stamp a file when you touch it anyway,
then delete its line. Do not schedule a sweep.

### B6. `lab/knife4_tails.py` hangs in `sympy.simplify`

Two runs produced zero output in two hours on 18 August and were killed. The
builder calls `sp.simplify` on a large multivariate expression -- the classic
hang, and against the fast-engine law. Rewrite the clearing step to cancel the
`(1-v)^d` factor by construction instead of asking sympy to discover it.

**This one blocks science** (the knife-4 tails are part of the proof), so it is
the first item to leave this file.

---

## 3. Publication pipeline

* Preprint "The Island Has Edges" -> arXiv (task #13)
* Article #5, The Binomial Collapse (task #18)
* Card B, Virasoro-Shapiro direction (task #14)

---

## 4. Language conversion

`tests/english_only_debt.txt` holds the 43 repository files that predate the
English-only rule. Outside the repository, roughly 50 skills (game, video,
Unreal) are still Russian; they belong to other projects and are converted when
those projects are next touched.
