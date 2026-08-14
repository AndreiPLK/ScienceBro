# Release review — projects/qg-bootstrap/paper/main.tex

Reviewer: release-reviewer agent, 2026-08-14.
Scope: claim-evidence alignment, overclaim check, citation verification (arXiv API +
INSPIRE + local fulltexts + downloaded MS PDF), completeness, peer-review risk.
Verdict: **NOT RELEASE-READY — 6 blockers.** All are fixable; none invalidates the
underlying mathematics (every derivation-level claim traced clean).

---

## BLOCKERS

### B1. Wrong title in the CHR citation (bibliography, \bibitem{CHR2024})
main.tex cites arXiv:2406.02665 as "Uniqueness Criteria for the Veneziano Amplitude".
The actual title — verified 2026-08-14 against the arXiv API, INSPIRE, and the local
fulltext `research/2406.02665_fulltext.txt` (page 1) — is:
**"Bootstrap Principle for the Spectrum and Scattering of Strings"**,
C. Cheung, A. Hillman, G. N. Remmen, arXiv:2406.02665, **Phys. Rev. Lett. 133, 251601 (2024)**.
Citing the anchor paper of the entire work under an invented title is an instant
credibility kill at review. Fix title + add journal reference.

### B2. Attainment overclaim in the abstract (result (i)) and "pinned" phrasing
Abstract: "the island's left edge **is** the line r=-(1+mu0)/2, exactly, at every level
and in every spacetime dimension D>3". What is proven (Theorem 1) is one-sided:
**exclusion** of r < -(1+mu0)/2 (w>0). Attainment is (a) empirical-only at mu0<=0
(depth-80 scans), and (b) **false at mu0>0 by our own data**: DATA_LOG 2026-08-13
("For mu0 > 0 the island is cut tighter than the theorem line... Theorem is one-sided
(outer bound)") and the atlas note ("mu0>0 gap = threshold scalar"). The independent
review (left-edge-theorem-review.md, Overclaim check) explicitly required splitting
"analytic exclusion bound" from "empirical attainment"; the fix was applied in the
research note but NOT carried into the paper's abstract. Same issue in abstract (iii)
and Sec. 5: "its left edge stays pinned at -(1+mu0)/2 in every dimension".
Allowed wording: see W-section "Allowed public wording", claim 1.

### B3. "charted here for the first time" (abstract, last sentence) — "first" gate not passed at that scope
The only novelty gate on record is the frozen novelty radar (microproblem-cards.md,
2026-08-13): no treatment of w != 0 found **among the 49 INSPIRE-citing works of CHR**.
That gate supports a scoped statement, not an unqualified "for the first time".
Required rewording: "the w != 0 region, which is not treated in [MS2024] and, among
the works citing CHR (INSPIRE, August 2026), has no dedicated analysis we are aware of."
(Sec. 7's phrasing "Within the 49 works citing CHR we found no other treatment" is
already correctly scoped — mirror it in the abstract.)

### B4. Repro link points to the wrong repository; no public code/data/DOI for this project
Footnote: "Code and data: github.com/AndreiPLK/spacetime-verifier". Verified via GitHub
API 2026-08-14: that repo is the **AInstein audit** ("An independent curvature evaluator
for machine-learned spacetimes"; contents: verifier/, audit/, proof/ ...). It contains
**none** of the qg-bootstrap island code or data. The Reproducibility section promises
"the two-route evaluator, all maps and scans, the razor tests, the independent
reviewer's attack script, and the append-only research log" — currently published
nowhere. Required: publish the qg-bootstrap package (new repo, or a clearly separated
subtree) + Zenodo DOI, and point the footnote there. Publication itself = human action.

### B5. Paper numbers with no preserved artifact under results/ (experiment-contract gap)
Backed only by prose in DATA_LOG.md / left-edge-theorem.md, with no script in lab/ and
no results/*.json:
- **q-clock table** 34/15/11/8/5/4 and the constant 1.1 (Sec. 6) — no scan script, no artifact;
- **g(n) ~ 0.3 n^2 log-derivative** (Sec. 6) — no artifact;
- **odd/even dichotomy, k=1..7** incl. the n=57 measurement and the test point
  (r,w)=(-0.52,1) — the (r,w) attribution for the k=3 test appears ONLY in main.tex
  (notes/log record "predicted 57, measured 55..59" without coordinates) — unverifiable;
- **killer census over 714 excluded cells** (Sec. 5) — no artifact;
- **stack-wide 11,994-point comparison** (the headline number) — component maps exist
  (7 x 1369 + 2411 = 11,994 checks out) but the comparison run itself has no artifact;
- **D=6,10 checks** ("10/10 incl. four exact zeros") — no artifact;
- **doomed-cell deep verifications** (4 of 30) — no artifact;
- **fixed-spin n=200 spot checks** — artifact n2_fixed_spin.json stops at n=100.
Required before release: commit the scripts + raw outputs (results/raw/, immutable) for
each, or delete/downgrade the corresponding numbers. This is also what makes B4's
"all maps and scans" sentence true.

### B6. "the (2l+1) scaling is confirmed exactly in numerics up to n=200" (Sec. 5, fixed-spin) — contradicts the artifact
results/n2_fixed_spin.json reaches n=100; the night-N2 note records "l=0 vs l=2 ratios
coincide **to 3 digits**" and C drifting logarithmically (0.27..0.86 at n=200).
"Confirmed exactly" fails the confirmation gate (3-digit agreement is not exact; the
n=200 points are unpreserved). Allowed wording: "consistent with (2l+1) scaling to
three digits in exact-arithmetic scans up to n=100 (spot checks to n=200); the constant
converges only logarithmically." The paragraph's closing label "heuristic-plus-numeric"
is good — keep it.

---

## WARNINGS

- **W1. "zero mismatches" accounting (abstract (iv) + Sec. 5).** Against the raw N=10
  mu0!=0 maps there are exactly 30 disagreements; all are theorem-predicted doomed
  cells, but only 4/30 were verified by direct deep evaluation (with exact marginal
  zeros). Say "zero unexplained mismatches" and state that 26/30 doomed verdicts rest
  on the proven ladder law rather than direct evaluation.
- **W2. Abstract dichotomy sentence unscoped.** "every odd near-leading trajectory
  eventually turns negative at a threshold our closed forms predict exactly" — the body
  is honest (empirical for k<=7; closed forms only k<=3; general-k open); the abstract
  should carry "(observed for k<=7)".
- **W3. "exact logarithmic derivative" (Sec. 6).** DATA_LOG 2026-08-14: it is a
  **finite difference at h=1e-6** (computed in exact arithmetic). Reword. Also the
  exponent "derivation" is first-order (predicts constant 1.8 vs measured 1.1; note
  says "higher orders kill sooner" and "analytic derivation open") — add one clause
  ("at first order" / "mechanistic"), and keep abstract's "derive the -1/2 exponent"
  only if that clause is present.
- **W4. "49 works citing CHR".** Re-verified 2026-08-14 via INSPIRE: citation_count=49
  today — but it is a moving number. Date-stamp it: "the 49 citing works (INSPIRE,
  August 2026)".
- **W5. No evidence record for CHR.** evidence-records.jsonl contains only EV-QG-0002
  (Mansfield-Spradlin). Add EV-QG-0001 for 2406.02665 (local PDF sha256 is already in
  the reading notes header).
- **W6. Bibliography lacks journal references.** CHR = Phys. Rev. Lett. 133, 251601
  (2024); MS = JHEP 02 (2025) 145 (INSPIRE-verified). Cite published versions.
- **W7. Conjecture window under-specified (Sec. 5).** The stack-wide analytic verdict
  used the window n_min <= n <= n_min+4 (research note); the paper says only "binding
  window taken at the first above-threshold levels". State the window; also state that
  the six mu0!=0 maps are depth N=10 (artifacts confirm nmax=10).
- **W8. No figures at all.** graphicx is loaded but unused; the island atlas / edge-map
  visuals exist (article/visuals/). A numerics-heavy bootstrap paper with zero figures
  will read as unfinished; include at least the mu0-stack atlas with the edge law
  overlaid and the q-clock log-log fit.
- **W9. Abstract result (iii) reads as established completeness.** "the remaining
  boundary is cut by an explicit finite set of low-level algebraic curves" — the
  completeness of that finite set is Conjecture 1. Insert "conjecturally" (the body and
  Discussion label it correctly; the abstract must too).
- **W10. Theorem 1 ships only a "proof sketch".** The full derivation exists and passed
  independent review + 6/6 adversarial attacks; for a theorem carrying the paper, put
  the complete (short) proof in an appendix. Cheap insurance at review.
- **W11. "island" is our coinage** — current text does not attribute it to CHR (good);
  keep it that way in press materials too.

---

## OK-LIST (verified claim-by-claim)

Citations and attributions:
- arXiv:2409.09561 = "On Unitarity of the Hypergeometric Amplitude", Gareth Mansfield,
  Marcus Spradlin — title and authors VERIFIED (arXiv API, 2026-08-14). 38 pp as in EV-QG-0002.
- MS Theorem 11 / Eq. (5.16): odd-Delta factor (2r + m^2 + 1) — VERIFIED directly in the
  downloaded arXiv PDF (p.27); matches EV-QG-0002 and the paper's Sec. 7 usage; the
  w=0 edge-line agreement claim is correct, and the paper correctly says their result
  is asymptotic-only and w=0-only.
- CHR Eq. (16) = level-n residue R(n,t) in q-Pochhammer form — VERIFIED in the local
  fulltext; the paper's Eq. (1) is its correctly stated q->1 reduction (matches the
  two-route-validated form in lab/repro_r4_positivity_spot.py).
- CHR Fig. 1 depth n<=10, D=4; threshold caveat mu(n)>=4mu0; q>1 asymptotic exclusion;
  "region diminishes for D>4" — all match the reading notes.

Numbers with artifact/log support:
- 11,994 = 7x1369 + 2411 — arithmetic and components check (fig1_map_*.json all
  total=1369; fine_boundary_mu0_N20.json points=2411).
- 1369/1369 coarse (N=40) and boundary re-test at depth 80: boundary_N80_mu0.json —
  42 boundary cells, fell_at_N80=[], stable=true.
- 176 false positives removed: fine_boundary_mu0_N20_corrected.json,
  theorem_correction.false_positives_removed=176; allowed 1321 -> 1145.
- 9 casualties: N=10 664 -> N=20 655 (artifacts), all at r=-3/5, kill law n=10w+1
  consistent with r+1/2=-1/10; (11,10)...(19,18) matches the note.
- 30 doomed cells = 9+9+9 (mu0=-9/5,-6/5,-3/5) + 3 (mu0=3/5); "four verified directly"
  matches the note (artifact gap -> B5).
- 714 excluded cells = 1369 - 655 (consistent with N=40 map).
- 8 razor zeros = 4 (mu0 = 0 twice incl. off-grid (-13/25,1/2) n=25; mu0=+-3/5 at
  n=20/15) + 4 at D=6,10 — documented in the note (D=6/10 artifact gap -> B5).
- 6/6 attacks, exit 0: script exists (lab/attack_left_edge.py), run recorded in note
  header + DATA_LOG; includes route1-vs-route2 at mu0!=0 (closes review gap E1).
- Thresholds: k=3 predicted 57, measured 55..59; k=1 at w=17/10 predicted 85, measured
  +84/-86 — note-supported (paper cites only 57; coordinates issue -> B5).
- q-clock 34/15/11/8/5/4 consistent with 1.1(q-1)^{-1/2} (checked: 34.8/15.6/11/7.8/4.9/3.5);
  q=1 control clean to n=25; killer l=0,1; tolerance (1.1/10)^2 ~ 0.012 — all
  note-supported (artifact gap -> B5).
- n_min = 2,4,6 for mu0=3/5,6/5,9/5; threshold scalar curve incl. mu0=2/3 factorization
  (3r+4)(3r+3w+1)/9 — match the note.
- a_{2,0}: 3(1+r)(r+w)+1; a_{3,0} cubic; twenty n<=5 curves; a_{2,0} D-form
  (1+r)(r+w)+1/(D-1); k=2 constant 24(2n-1)/(n-1); k=3 bracket — all character-for-
  character consistent with note + review.

Overclaim hygiene (where it is already right):
- Conjecture 1 is a labeled \conjecture; Discussion calls it "one conjectural
  completeness statement"; "What remains unproven..." paragraph present.
- "proven" used exactly twice-worth: Theorem 1 (reviewed, attacked, survived) and the
  k=2 all-n identity (reviewer's polynomial-identity proof) — both gates passed.
- k=3 honestly labeled "verified against brute force n=4..9".
- Fixed-spin section explicitly labeled "heuristic-plus-numeric".
- E2 (n=3mu0 identically-zero case), E3 (explicit domain), E4 (redundant clause
  removed) — all review fixes present in the paper.
- Two-route evaluator description ("up to a positive l-dependent normalization") honest.
- "discovered/refuted/novel" — not used. "confirmed" used only for deterministic exact
  checks (except B6).

Completeness/security:
- AI disclosure present and accurate (Reproducibility and AI disclosure section).
- Compiled main.pdf scanned: no local paths, no usernames, no secrets, no temp paths;
  only links = GitHub footnote (wrong target -> B4) + ORCID (correct: 0009-0005-5660-2603).
- License: quoting equations/results from arXiv papers with citation is fine; own code
  MIT; arXiv PDFs under research/pdfs/ are working copies, not for redistribution in
  the release package.

---

## ALLOWED PUBLIC WORDING (per claim, after fixes)

1. **Edge law**: "We prove that positivity fails for all r < -(1+mu0)/2, w > 0, at every
   level n > w/|r+(1+mu0)/2|, in every dimension D > 3 — an exact, dimension-universal
   exclusion bound. At mu0 <= 0 the observed island reaches this bound (empirically, to
   depth 80); at mu0 > 0 threshold constraints cut strictly inside it."
   NOT allowed: "the island's left edge **is** the line ... exactly" / "pinned" without
   the exclusion-vs-attainment split.
2. **Completeness**: "conjecturally complete characterization; consistent with 11,994
   exact-rational verdicts with zero unexplained mismatches (30 finite-depth map
   disagreements are all theorem-predicted doomed cells, 4 verified by deep evaluation)."
   NOT allowed: completeness as fact; unqualified "zero mismatches".
3. **k=2 identity**: "proven for all n" — allowed (gate passed).
4. **k=3 / dichotomy**: "verified n=4..9" / "observed for k <= 7; general-k proof open"
   — allowed only with scope.
5. **q-clock**: "measured exact exclusion depths, consistent with 1.1 (q-1)^{-1/2};
   the -1/2 exponent explained at first order by the finite-difference log-derivative
   g(n) ~ 0.3 n^2 (constant not reproduced at first order)."
   NOT allowed: "exact logarithmic derivative"; "derived" without the first-order caveat.
6. **Novelty**: "no dedicated analysis of the w != 0 region among the 49 works citing
   CHR (INSPIRE, August 2026)". NOT allowed: unscoped "for the first time".
7. **Fixed-spin tails**: "heuristic-plus-numeric; (2l+1) scaling consistent to three
   digits up to n=100". NOT allowed: "confirmed exactly".
8. **MS relation**: "our exact finite-n law reduces on the w=0 slice to the same
   critical line as their asymptotic Theorem 11" — allowed (verified against their PDF).

---

## RELEASE CHECKLIST (templates/release-checklist.yaml, filled)

```yaml
project_id: "qg-bootstrap"
clean_clone_test: fail        # no public package exists for this project yet (B4)
environment_lock: pass        # uv.lock in repo; exact-rational stack, no GPU deps
test_suite: pending           # run `uv run sb check` on the final package
citation_audit: fail          # B1 (CHR title wrong); W6 (journal refs missing)
license_audit: pass           # MIT own code; cited formulas fine; don't ship arXiv PDFs
data_availability: fail       # B5 (q-clock, dichotomy, census, 11994 comparison, D=6/10 unarchived)
ai_use_disclosure: pass
figures_and_tables: fail      # W8 (no figures); q-clock table lacks artifact (B5)
repository_release: fail      # B4 (wrong repo link; nothing published)
doi: fail                     # none minted for this project
preprint: pending             # human action only — do not submit
journal_candidate: pending
human_approval: pending       # publication is always a deliberate human action
```

---

## PUBLICATION PACKAGE MANIFEST (what must ship, once blockers close)

Existing (repo paths relative to C:\Users\user\ScienceBro\projects\qg-bootstrap\):
- paper/main.tex (+ compiled main.pdf) — after B1-B6/W fixes
- lab/repro_r1_crossing.py, lab/repro_r4_positivity_spot.py (two-route evaluator)
- lab/fig1_island_map.py, lab/fine_grid_boundary.py, lab/boundary_n80.py,
  lab/n2_fixed_spin.py, lab/attack_left_edge.py (adversarial script)
- results/fig1_map_mu{-9_5,-6_5,-3_5,0_1,3_5,6_5,9_5}.json, fig1_map_mu0_1_{N20,N40}.json,
  boundary_N80_mu0.json, fine_boundary_mu0_N20.json, fine_boundary_mu0_N20_corrected.json,
  n2_fixed_spin.json
- research/left-edge-theorem.md, research/left-edge-theorem-review.md,
  research/2406.02665-notes.md, research/microproblem-cards.md,
  research/evidence-records.jsonl (+ new EV-QG-0001)
- article/DATA_LOG.md (append-only log, QG sections)

To create before release (closes B5/B4):
- lab/q_clock.py + results/q_clock.json (table + local exponents + g(n) data)
- lab/dichotomy_scan.py + results/dichotomy_k1_7.json (incl. the k=3 point coordinates)
- lab/killer_census.py + results/killer_census_N40.json (714 cells)
- lab/stackwide_verdict.py + results/stackwide_11994.json (incl. 30 doomed cells,
  4 deep verifications)
- lab/gegenbauer_D.py + results/edge_D6_D10.json (10/10 checks, 4 zeros)
- README.md, LICENSE (MIT), CITATION.cff, AI_DISCLOSURE.md for the public repo
- New public repository (do NOT reuse spacetime-verifier) + Zenodo DOI; update footnote

Excluded from package: research/pdfs/ (third-party arXiv PDFs), lab/__pycache__/,
paper/main.log|aux|out, any founder-personal data.

**No part of this package is to be pushed, submitted, or published by an agent.
Every publication step is a deliberate human action (founder).**
