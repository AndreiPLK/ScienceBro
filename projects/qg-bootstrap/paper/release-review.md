# Release review — projects/qg-bootstrap/paper/main.tex

Reviewer: release-reviewer agent. v1 review 2026-08-14 (6 blockers); v2 re-review
2026-08-14 after fixes (paper recompiled: 6 pages, 2 figures).

## VERDICT (v2): all 6 blockers CLOSED (B4 conditionally). Release-ready
**contingent on** (a) the code/data package actually being assembled, published and
DOI-minted before submission (the paper now promises it in present tense), and
(b) human approval. Remaining items are warnings only. No agent submits anything.

---

## v2 PER-BLOCKER RE-CHECK

### B1 — CHR citation. CONFIRMED CLOSED.
\bibitem{CHR2024} now reads "Bootstrap Principle for the Spectrum and Scattering of
Strings," Phys. Rev. Lett. 133, 251601 (2024), arXiv:2406.02665 — matches arXiv API,
INSPIRE publication record, and the local fulltext. Correct.

### B2 — attainment overclaim. CONFIRMED CLOSED.
Abstract (i) is now exclusion-only: "nothing survives left of the line ... an
exclusion valid at every level and in every spacetime dimension D>3", with the
mu0<=0 attainment caveat ("extends up to this line in our scans") and the mu0>0
threshold note ("cut strictly inside it"). Figure captions use "exclusion edge" and
repeat the mu0>0 caveat. Residual nits (not blocking, logged as W12): "left edge
stays pinned" survives in abstract (iii) and Sec. 5, and fig_atlas's embedded title
says "left edge r=-(1+mu0)/2" — tolerable now that (i) fixes the exclusion sense,
but "exclusion edge stays pinned" would be cleaner.

### B3 — novelty scoping. CONFIRMED CLOSED.
Abstract now: "to our knowledge --- based on a survey of the works citing CHR
indexed in INSPIRE --- the w!=0 region has not been treated analytically before."
Matches the gate that actually exists (novelty radar, microproblem-cards.md,
INSPIRE citation count re-verified = 49 on 2026-08-14). Recommend adding the survey
date (W4).

### B4 — repro link. CONDITIONALLY CLOSED.
The wrong spacetime-verifier link is gone; footnote now promises an "ancillary
package (repository and DOI to accompany this preprint)". Honest as a forward
commitment. BUT the Reproducibility section still speaks in present tense ("the
repository contains...", "outputs are published") — true only once the package
ships. Release gate: assemble + publish the package (manifest below) and insert the
real repo URL + DOI before any submission. Until then this blocker is closed on
wording, open on substance.

### B5 — unpersisted numbers. CONFIRMED CLOSED.
New artifact results/paper_artifacts.json (generator lab/artifacts_battery.py,
imports the two-route-validated evaluator) verified value-by-value against the
paper, and spot-reproduced by re-execution (census, q=1.1 clock entry, k=3
threshold signs, fixed-spin n=200 point — all reproduced exactly):
- Killer census: 714 excluded cells, 27 distinct killers, machine-checked that
  every killer satisfies (n<=5) OR (l=n-1 ladder, entries (4,3)...(17,16)) OR
  domain — exactly the paper's trichotomy.
- Stack comparison: total_points=11,994; 30 coarse discrepancies, ALL
  map-allowed/analytic-doomed (9/9/9 at mu0=-9/5,-6/5,-3/5, 3 at mu0=3/5; r values
  0.3/0.0/-0.3/-0.9 = exactly 0.1 left of the shifted edges); fine_mismatches=0.
  Backs "11,994 exact verdicts with zero unexplained mismatches" as now worded.
- Dichotomy: k=1..7 at n=41..47 — odd beyond-edge negative, even positive, all
  inside positive; thresholds: k=3 at (r,w)=(-13/25,1)= (-0.52,1) sign +@55/-@59
  (paper: "predicts n=57...measured between 55 and 59" — now artifact-backed,
  coordinates included); k=1 at w=17/10 sign +@84/-@86 (predicted 85).
- q-clock: first negatives at n=34/15/11/8/5/4 for q-1=0.001...0.1 (plus extra q
  values), killers at l in {0,1} as claimed; q=1 control clean to n=25;
  g/n^2 = 0.56->0.29 over n=5..30, consistent with "~0.3 n^2".
- D-universality: a_{10,9}=0 exactly and a_{11,10}<0 at D=6 and D=10 (symbolic
  Gegenbauer route).
- Fixed-spin: positivity at n=50/100/200, l=0,2, at 4 representative points incl.
  near-edge — backs the new n=200 wording.
Residuals (W13): the "(2l+1) agrees to three digits" figure is still note-only
(battery records signs, not ratios); the note's fuller "10/10 at D=6,10" set is
persisted only as the 2 zero-checks (paper wording is covered).

### B6 — fixed-spin wording. CONFIRMED CLOSED.
Now: "(2l+1) scaling agrees to three digits between l=0 and l=2 in exact numerics,
with positivity checked up to n=200 at representative points" — accurate to the
artifacts and honestly labeled "heuristic-plus-numeric". "Confirmed exactly" gone.

Also verified in v2: "zero unexplained mismatches" wording present with the correct
accounting sentence (30 doomed = finite-depth artifacts, 4 directly verified);
q-clock derivative now "computed as an exact finite difference at step 10^-6";
figures fig_atlas.png / fig_edge.png exist, are included in the compiled PDF
(pages 4-5 of 6), captions are exclusion-correct, in-figure numbers self-consistent
(2411 = 1145+1090+176; atlas panels match map artifacts 399/504/615/655/605/455/302);
compiled PDF re-scanned: no local paths, no secrets, no stale spacetime-verifier link.

---

## WARNINGS (open; none blocking)

- **W2.** Abstract dichotomy sentence still unscoped: "every odd near-leading
  trajectory eventually turns negative at a threshold our closed forms predict
  exactly" — body says (correctly) empirical for k<=7, closed-form thresholds only
  k<=3, general-k open. Add "(observed for k<=7)" to the abstract.
- **W4.** Date-stamp the INSPIRE survey: "49 works citing CHR (INSPIRE, August 2026)"
  — the count is a moving number (re-verified 49 on 2026-08-14).
- **W5.** evidence-records.jsonl still lacks an EV record for CHR 2406.02665
  (only EV-QG-0002/MS exists). Add EV-QG-0001 before release.
- **W6.** MS bibitem still lacks the journal reference: JHEP 02 (2025) 145
  (INSPIRE-verified). CHR is fixed; do the same for MS.
- **W9.** Abstract (iii) still reads as established completeness ("the remaining
  boundary is cut by an explicit finite set of low-level algebraic curves") —
  insert "conjecturally" (the body/Conjecture 1/Discussion are correctly labeled).
- **W10.** Theorem 1 ships as "proof sketch" only; the full short proof exists
  (left-edge-theorem.md, independently reviewed) — put it in an appendix.
- **W12.** "left edge stays pinned" (abstract (iii), Sec. 5) and fig_atlas's
  embedded title "left edge r=-(1+mu0)/2" — prefer "exclusion edge" for
  consistency with the corrected abstract (i).
- **W13.** "(2l+1) to three digits" rests on the research note; persist the ratio
  data (one small addition to artifacts_battery.py). The battery's analytic verdict
  also includes an "r=edge and w<0 -> excluded" clause that Conjecture 1 does not
  state (review E4 showed it redundant — the n=1 block kills those points); verify
  redundancy in code or align the predicate exactly with the conjecture text.
- **W14 (new, figures).** fig_edge.png contains viewer scrollbar artifacts (right +
  bottom edges) — crop. Both figures are dark neon-styled; fine for arXiv, but
  print/journal versions usually want light background. Atlas mixes depths across
  panels (mu0=0 at N>=20 -> 655, others N=10) — say so in the caption.
- **W15.** Reproducibility section present tense ("outputs are published") — becomes
  true only when the B4 package ships; keep in sync with the actual release moment.

---

## OK-LIST (v1 verifications that remain valid)

- MS 2409.09561 title/authors verified (arXiv API); Theorem 11 / Eq. (5.16) odd-Delta
  factor (2r+m^2+1) verified in the downloaded PDF (p.27); w=0 edge-line agreement
  claim correct, asymptotic-only/w=0-only caveats correct.
- CHR Eq. (16) residue verified in local fulltext; paper Eq. (1) is its correct q->1
  reduction; Fig. 1 depth n<=10 D=4, threshold caveat mu(n)>=4mu0, q>1 asymptotic
  exclusion all match reading notes.
- 11,994 = 7x1369 + 2411; fig1_map_*.json totals 1369 each; fine 2411; 176 removed
  (1321->1145); 9 casualties (664->655, r=-3/5, n=10w+1); 42 boundary cells stable
  at depth 80; 8 razor zeros accounting (4 at D=4/mu0 variants + 4 at D=6,10);
  6/6 attack script (lab/attack_left_edge.py) exit 0 on record.
- k=2 identity proven all n (reviewer's polynomial identity, constant 24(2n-1)/(n-1));
  k=3 bracket character-identical to the note, verified n=4..9; domain/E2/E3/E4
  review fixes present; Conjecture properly labeled in body; fixed-spin labeled
  heuristic; "proven" used only where gates passed; no "discovered/refuted/novel".
- AI disclosure present; ORCID correct; license posture fine (MIT own code; cited
  formulas fine; don't ship third-party arXiv PDFs in the package).

## ALLOWED PUBLIC WORDING — unchanged from v1 (section retained)

1. Edge law: exclusion proven (every level, every D>3); attainment empirical at
   mu0<=0; threshold constraints cut inside the line at mu0>0. No "the left edge IS
   the line" without this split.
2. Completeness: "conjecturally complete"; "11,994 exact verdicts, zero unexplained
   mismatches (30 doomed cells predicted by the ladder, 4 verified directly)".
3. k=2 identity: "proven for all n" — allowed.
4. Dichotomy: "observed for k<=7; general-k proof open".
5. q-clock: "measured, consistent with 1.1(q-1)^{-1/2}; exponent explained at first
   order via finite-difference log-derivative g(n)~0.3n^2".
6. Novelty: only the INSPIRE-scoped "to our knowledge" form (now in the paper).
7. Fixed-spin: "heuristic-plus-numeric; three-digit (2l+1) agreement; positivity
   checked to n=200" — as now worded.
8. MS relation: "our exact finite-n law reduces on the w=0 slice to their asymptotic
   critical line" — allowed.

## RELEASE CHECKLIST (templates/release-checklist.yaml, v2)

```yaml
project_id: "qg-bootstrap"
clean_clone_test: pending     # run on the assembled public package
environment_lock: pass        # uv.lock; pure exact-rational stack
test_suite: pending           # uv run sb check on final package
citation_audit: pass          # B1 fixed; W6 (MS journal ref) cosmetic
license_audit: pass
data_availability: pass       # paper_artifacts.json + battery close B5 (W13 minor)
ai_use_disclosure: pass
figures_and_tables: pass      # two figures in PDF; W14 polish items
repository_release: pending   # B4 condition: assemble + publish package
doi: pending                  # mint with the package
preprint: pending             # human action only
journal_candidate: pending
human_approval: pending       # publication is always a deliberate human action
```

## PUBLICATION PACKAGE MANIFEST (unchanged scope, updated for new files)

Ship: paper/main.tex + main.pdf + fig_atlas.png + fig_edge.png;
lab/repro_r1_crossing.py, repro_r4_positivity_spot.py, fig1_island_map.py,
fine_grid_boundary.py, boundary_n80.py, n2_fixed_spin.py, attack_left_edge.py,
**artifacts_battery.py**; results/fig1_map_*.json (9 files), boundary_N80_mu0.json,
fine_boundary_mu0_N20{,_corrected}.json, n2_fixed_spin.json,
**paper_artifacts.json**; research/left-edge-theorem.md,
left-edge-theorem-review.md, 2406.02665-notes.md, microproblem-cards.md,
evidence-records.jsonl (+EV-QG-0001); article/DATA_LOG.md (QG sections);
README, LICENSE (MIT), CITATION.cff, AI_DISCLOSURE.md.
Exclude: research/pdfs/, __pycache__, main.log|aux|out, personal data.
After publishing: put the real repo URL + DOI into the footnote and the
Reproducibility section, recompile, then human submits.

**No part of this package is to be pushed, submitted, or published by an agent.**
