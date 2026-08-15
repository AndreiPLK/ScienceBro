# Release review — projects/qg-bootstrap/paper2/main.tex

Reviewer: release-reviewer agent, 2026-08-15 (v1).
Scope: paper 2 ("The Shore of Closed-String Gravity") against gravity-card.md
(slices 1-8, post-Pochhammer corrections, review fixes F1-F2), gravity-review.md,
and the results/ artifacts. Compiled main.pdf scanned (no local paths, no secrets,
empty Author/Title metadata — clean).

## VERDICT (v1): NOT release-ready. 6 blockers, 10 warnings.
The physics numbers are in excellent shape — every quantitative claim in the tex
traced to an artifact or was re-verified live by this review; zero numerical
discrepancies. The blockers are completeness (two placeholder sections), residual
F2 wording, missing citations/novelty gating, missing evidence records, one
screenshot-grade figure, and the unassembled code/data package.
**No agent publishes, pushes, or submits anything — publication is a human action.**

---

## BLOCKERS

### B1 — Placeholder sections in the shipped tex (Discussion; Reproducibility and AI disclosure)
Sections 6 and "Reproducibility and AI disclosure" are bracketed stubs
("[Dimension-graded rigidity...]", "[Same standard as companion: ...]").
The AI-assistance disclosure therefore does not exist in substance (project rule:
disclosure in full, as in the companion). Additionally the stub mischaracterizes
the bug: it says "sign-convention bug", but DATA_LOG 2026-08-14 records a
**Pochhammer increment-step bug** (the evaluator incremented
((1+λ)/2+λt)_{n-1} by λ instead of 1; λ=1 results unaffected, all λ≠1 results
voided and recomputed). The published disclosure must name the actual bug, that
it was found via the external CHR "D≥9" anchor (internal razors were circular),
and which results it did/did not affect. Write both sections before release.

### B2 — Review fix F2 ("shore of the near-leading trajectory") violated in the abstract and inside fig_shore.png
F2 (gravity-review.md item g.2; card "REVIEW ROUND CLOSED") requires "true
shore" to be scoped to the NEAR-LEADING trajectory; full-boundary completeness
is Conjecture 1. Violations:
- Abstract: "The true boundary is the envelope min_n T_n" — asserts as fact what
  the last abstract sentence and Section 5 correctly label a conjecture.
  Reword: "The boundary carved by this trajectory is the envelope min_n T_n".
- fig_shore.png embedded header: "true shore = envelope of ALL levels (general
  law T_n)" and legend "true shore (all levels)" — reads as a full-model
  statement. Regenerate the figure text ("near-leading shore" / "envelope of
  T_n over levels n").
The body text ("The boundary implied by Theorem 1...") is correctly scoped.

### B3 — Missing citations and ungated novelty framing
- Section 4 invokes "the finite-level D_crit(n) phenomenology known for
  Veneziano-type amplitudes" and "the deep asymptotic bounds of the literature"
  with NO citation. 2210.14920 (local PDF exists, used as the D-cliff anchor in
  the card) must be cited; the asymptotic-bounds sentence needs its source too.
- The abstract's implicit novelty claim ("positivity was known to bound λ ...
  numerically. We derive the boundary in closed form") is not yet gated: the
  card's novelty radar lists ADJACENT works that "must cite, differentiate, and
  read in full before any claim" — 2607.27300 (Shao-Vichi analytic boundaries
  via hidden zeros), 2606.19283, 2605.11084. None are cited; the Shao-Vichi
  full text is not in research/pdfs/ and gravity-review.md question 3 (does
  their method already yield T_n?) is unresolved. Required: read/differentiate
  Shao-Vichi at minimum, cite the adjacent works, and use the companion's
  INSPIRE-scoped form ("to our knowledge, based on a survey of works citing
  CHR (INSPIRE, August 2026), no closed-form boundary for the λ-family has
  been given"). The bibliography currently has only 3 entries.

### B4 — No evidence records for the CHR sources (binding evidence contract)
research/evidence-records.jsonl contains no record for arXiv:2408.03362 (the
paper's primary source: family definition Eqs. 4/6-7, p.6 positivity status,
onset D≥9) nor for 2406.02665 (already flagged as W5 in paper 1's review and
still absent). Add EV records with exact locations before release; both journal
refs were verified by this review against the arXiv API
(2408.03362 → Phys. Rev. D 111, 086034 (2025), DOI 10.1103/PhysRevD.111.086034;
2406.02665 → Phys. Rev. Lett. 133, 251601 (2024), DOI
10.1103/PhysRevLett.133.251601) — the tex bibitems are correct; record this as
verified_by.metadata in the EV records.

### B5 — fig_continent.png is a window screenshot
Visible grey window frame plus horizontal AND vertical scrollbars around the
plot. Embarrassing at peer review. Re-export the figure directly from the
plotting script (no viewer chrome). (fig_shore.png is a clean export.)

### B6 — Code/data package does not exist yet; three committed artifacts have no generators
The author footnote promises "Code and data to be released with this preprint"
and Section 2 says the falsification suite is "published with the code". No
paper2 release package is assembled (paper 1 precedent: release/qg-island-edges).
Additionally hunt_2n6.json, hunt_2n8.json and lowspin_stress.json were committed
as bare "[]" with no generating script in the repo and no run metadata (command,
depth, grid, commit) — an experiment-contract violation for card slice 8. The
paper does not currently cite these numbers (see W6), so this blocks the package,
not the tex; either recommit the hunt scripts + structured artifacts or do not
rely on slice 8 anywhere public.

---

## WARNINGS

- **W1 — asymptote endpoint numbers.** Tex: "D/λ_min rises 18.75→18.92 over
  D=60→10^4". Artifacts (attack_gravity.json A6): D=60 → 18.9576, D=100 →
  18.7444, D=10^4 → 18.9236 — the approach is non-monotone and the D=60 value
  is 18.96, not 18.75. Reword (e.g. "dips to 18.74 at D≈100, then climbs back
  to 18.92 by D=10^4 against 12+4√3=18.928...") or change the range to
  D=100→10^4. The O(1/λ) discrete-n oscillation caveat IS present — good.
- **W2 — "fractional dimensions D*=271/4 ... and D*=57".** 57 is an odd
  integer, not fractional. Say "at never-scanned dimensions, one fractional
  (D*=271/4) and one odd (D*=57)".
- **W3 — fig_shore caption omits depth.** The verdict dots come from
  grav_zoomout.json (λ 0.05..10, D 4..60, depth 12; DATA_LOG 2026-08-14).
  Caption says "exact verdicts" with no depth; fig_continent honestly says
  depth 14. State "exact-rational verdicts at truncation depth n≤12" (mixed
  depths across figures must stay visible).
- **W4 — doomed-cell executions have no dedicated persisted artifact.** The
  cells (λ,D)=(3/2,32) and (2,40) sit inside the model_test grid (agreement
  implicit in 494/494), but the "sign flip at n=4" per-cell record is nowhere.
  Re-verified live by this review with the corrected evaluator:
  first_negative=[4,4] at both; model kill n=4 (T_4(3/2)=30.97, T_4(2)=39.875).
  Add both cells to paper2_artifacts.json.
- **W5 — domain caveats from the review (f.2, f.3) not in the tex.** λ≥0 is
  stated as imported from CHR (good) and D>3 is in Theorem 1 (good), but: the
  λ→0 degeneration (μ(n)→∞; T_n(0) as a limit), the separately hand-checked
  n=2 level (never bites; why min over n≥3 is complete), and the inclusive
  boundary convention (a=0 allowed at D=T_n exactly) deserve one footnote.
- **W6 — "the ℓ=2n-6 trajectory ... is under derivation" is stale.** Slice 8
  already ran a clean numerical hunt (34 λ values, D windows hugging the
  boundary, n=4..14, zero alarms). Honest as written (the closed-form law is
  indeed underived), but either report the hunt (after fixing its artifact —
  see B6) or leave as is knowingly.
- **W7 — in-figure styling.** "THE CREATURE — COMPLETE" / "THE CONTINENT OF
  LIFE //" headers and dark neon theme: tolerated for arXiv per project
  precedent (paper 1 W14), but retitle the embedded headers to neutral wording
  for any journal version.
- **W8 — Theorem 1 ships as a compressed "Derivation".** The full independent
  hand-proof exists (gravity-review.md items a-d, general n). Consider an
  appendix, as recommended for paper 1 (W10).
- **W9 — tense of release promises.** "to be released with this preprint" /
  "(published with the code)" — keep synchronized with the actual package
  moment (paper 1 B4 lesson: closed on wording, open on substance until the
  DOI exists).
- **W10 — title nit.** "an Exact Unitarity Boundary" is defensible (indefinite
  article; the trajectory boundary is exact and proven), but "for the
  near-leading trajectory of the CHR graviton family" would forestall the
  referee's first objection.

---

## CLAIM-EVIDENCE LEDGER (task 1 — every number traced)

| Tex claim | Artifact | Status |
|---|---|---|
| T_n formula, verified n≤14 (12/12) | paper2_artifacts.json Tn_verified; attack A5 (symbolic n=3..8); review hand-proof general n | OK |
| D_n(1)=24, 23, 24, 51/2, 136/5 | paper2_artifacts.json Dn1 (n=3..14 listed) | OK |
| min D_n(1)=23 at n=4; continuous min n=2+√3 | Dn1_min "(23,4)"; review claim 2 hand-proven | OK |
| λ_min(23)=1 exactly | envelope[23]=1.0; attack A6 (n≤2000 + analytic) | OK |
| Asymptote D=(12+4√3)λ, n*≈√3λ | asymptote_slope 18.9282...; attack A6 envelope D=60..10^4 | OK |
| Onset (D,λ)=(9,0); T_3(0)=9 | onset_T3_at_0 "9"; external anchor CHR p.6 "D≥9" | OK |
| 494/494, zero alarms, depth 16, all even ℓ≤2n-2, λ∈[0.1,10], D∈[4,40] | model_test.json + lab/model_test.py (26 λ × 19 D = 494; NMAX=16; grav_full_body.first_negative scans ℓ≤2n-2) | OK |
| Razor zeros D*=271/4 (n=5,λ=7/2), D*=57 (n=6,λ=3), symbolic D, sign flips both sides | attack_gravity.json A3 | OK (wording W2) |
| Doomed executions (3/2,32),(2,40) → sign flip at n=4 | inside model_test grid; re-verified live this review: first_negative=[4,4] both | OK, persist (W4) |
| D=4: 40/40 to depth 14; trivial bound T_n≥9>4 | grav_full_body.json (nmax 14; D=4 rows 40/40 allowed); bound follows from T_n(0) min 9 | OK (F1 respected: rests on corrected artifacts + CHR anchor) |
| VS first negative (4,4) at D=24; D=22 clean to depth 40 | vs_d_clock.json (D=22 null @ nmax 40; D=24 → [4,4]) | OK |
| "seven attack batteries" | attack_gravity.json A0-A6, executed, 0 failures, NO FALSIFICATION | OK |
| D/λ_min 18.75→18.92 over D=60→10^4 | attack A6: 18.9576(60), 18.7444(100), 18.9236(10^4) | MISMATCH at D=60 endpoint → W1 |

## OVERCLAIM AUDIT (task 2)

- Theorem vs Conjecture: Theorem 1 label backed by independent hand re-derivation
  (gravity-review verdicts 1-2 "CORRECT hand-proven", general n) plus executed
  attack script; Conjecture 1 properly labelled, falsifiable, with kill protocol. OK.
- "proven here" (Sec. 4) refers to the finite-level D_n(1) statement — hand-proven
  gate passed. OK.
- "confirmed by direct evaluation" (abstract) — direct executions exist (ledger). OK.
- "first loses positivity ... at D=24" — ordinal usage, scan-verified. OK.
- No "discovered / novel / refuted" anywhere. OK.
- Pochhammer bug disclosure: stub + mischaracterized → B1.
- Discrete-n oscillation caveat for the asymptote: present. OK (numbers → W1).
- F2 wording: violated in abstract + fig_shore internals → B2.
- Novelty framing without adjacent-work gate → B3.

## CITATIONS (task 3)

- 2408.03362 = Phys. Rev. D 111, 086034 (2025) — VERIFIED via arXiv API
  (journal_ref + DOI 10.1103/PhysRevD.111.086034); tex bibitem correct.
- 2406.02665 = Phys. Rev. Lett. 133, 251601 (2024) — VERIFIED via arXiv API
  (DOI 10.1103/PhysRevLett.133.251601); tex bibitem correct.
- Companion: "The Island Has Edges", DOI 10.5281/zenodo.21934462 — matches
  paper/main.tex title and its self-DOI, and EV-CORR-0002. Correct.
- Missing: 2210.14920 and the adjacent analytic-boundary works → B3.

## ALLOWED PUBLIC WORDING (exact forms)

1. Trajectory law: "the near-leading even trajectory a_{n,2n-4} is non-negative
   iff D ≤ T_n(λ), proven for general n (independent re-derivation) and verified
   symbolically for n ≤ 14 (12/12)" — ALLOWED.
2. Envelope: "the boundary carved by this trajectory is the envelope min_{n≥3}
   T_n(λ)" — ALLOWED. "The true/complete boundary of the family is min_n T_n" —
   BLOCKED as fact; ALLOWED only as "we conjecture ... (Conjecture 1)".
3. Magic point: "λ_min(23)=1 exactly; the shore passes exactly through the
   Virasoro-Shapiro amplitude; on this trajectory pure VS first loses positivity
   at D=24 via the level-4 spin-4 wave (exact scans: D=22 clean to depth 40)" —
   ALLOWED.
4. Onset: "T_3(0)=9 reproduces, as a formula, the onset CHR observed numerically
   at D≥9" — ALLOWED.
5. Asymptote: "exact asymptote D=(12+4√3)λ with active level n*≈√3λ; finite-D
   ratios oscillate by O(1/λ) around 18.928 due to integer n*" — ALLOWED with
   corrected numbers (W1).
6. Battery: "494/494 agreements with exact full-spin scans (all even ℓ≤2n-2,
   depth 16), zero alarms of either type; two doomed-cell executions confirmed
   at the predicted level n=4" — ALLOWED (persist the two cells, W4).
7. D=4: "within CHR's closed-string bootstrap assumptions, the entire family
   survives our D=4 scans (40/40 at depth 14, all even spins) and the trivial
   bound T_n ≥ 9 > 4; four-dimensional gravity is not forced to be string-like
   at any depth we can reach ON THESE CONSTRAINTS" — ALLOWED. Unconditional
   "4D gravity is not string-like" — BLOCKED.
8. Completeness: only "conjectured, falsifiable, survived its battery" —
   any "the complete boundary is..." as fact — BLOCKED.
9. Novelty: only the INSPIRE-scoped "to our knowledge" form, after the
   Shao-Vichi check (B3). "First closed-form boundary" without that gate —
   BLOCKED.
10. Bug: "a Pochhammer increment-step bug in the evaluator was found and fixed;
    λ=1 results were unaffected; all λ≠1 results were recomputed" — REQUIRED
    wording in the disclosure (B1); "sign-convention bug" — BLOCKED (inaccurate).

## RELEASE CHECKLIST (templates/release-checklist.yaml)

```yaml
project_id: "qg-bootstrap-paper2"
clean_clone_test: pending      # run on the assembled public package (B6)
environment_lock: pass         # uv.lock; pure exact-rational stack (Fraction/sympy)
test_suite: pending            # uv run sb check on final package
citation_audit: fail           # B3: 2210.14920 + adjacent works missing; CHR refs verified OK
license_audit: pass            # own code MIT (companion precedent); no third-party code shipped
data_availability: fail        # B6: package unassembled; hunt/lowspin artifacts lack generators; W4
ai_use_disclosure: fail        # B1: placeholder section
figures_and_tables: fail       # B5 screenshot; B2 in-figure wording; W3 depth caption
repository_release: pending    # assemble + publish package, then real URL/DOI into footnote
doi: pending                   # mint with the package
preprint: pending              # human action only
journal_candidate: pending
human_approval: pending        # publication is always a deliberate human action
```

## PUBLICATION PACKAGE MANIFEST (to assemble for release)

Ship: paper2/main.tex + main.pdf + fig_shore.png + fig_continent.png (both
regenerated per B2/B5/W3/W7);
lab/grav_full_body.py, model_test.py, attack_gravity.py, grav_d4_lowspin.py,
vs_d_clock.py, grav_lambda_map.py (pre-bug artifact kept visible as the
corrected-vs-void record) + the missing generators for grav_zoomout.json,
hunt_2n6.json, hunt_2n8.json, lowspin_stress.json (recreate or drop those
artifacts — B6);
results/model_test.json, attack_gravity.json, paper2_artifacts.json (+ the two
doomed cells, W4), grav_full_body.json, grav_zoomout.json, vs_d_clock.json,
grav_d4_lowspin.json;
research/gravity-card.md, gravity-review.md, Tn_coeffs.txt, T2n6_coeffs.txt,
evidence-records.jsonl (+ EV records for 2408.03362 and 2406.02665, B4);
article/DATA_LOG.md (gravity sections incl. the bug entry);
README, LICENSE (MIT), CITATION.cff, AI_DISCLOSURE.md.
Exclude: research/pdfs/ (third-party PDFs), __pycache__, main.log|aux|out,
lowspin_scratch.txt (optional), personal data.
After publishing: real repo URL + DOI into the footnote and the Reproducibility
section, recompile, secret-scan the package, then the human submits.

**No part of this package is to be pushed, submitted, or published by an agent.**
