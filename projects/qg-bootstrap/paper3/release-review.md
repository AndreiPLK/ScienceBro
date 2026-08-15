# Release review — projects/qg-bootstrap/paper3/main.tex

Reviewer: release-reviewer agent, 2026-08-15 (v1).
Scope: paper 3 ("A Master Positivity Formula for the Cheung–Hillman–Remmen
Graviton Family", 4 pp.) against research/master-formula.md,
research/master-formula-review.md (domain-critic), results/ artifacts, and the
binding rules (.claude/rules/claim-gates.md, evidence-contract.md,
experiment-contract.md). Compiled main.pdf builds clean (no undefined refs);
tex and log carry no secrets or local paths.

**No agent publishes, pushes, or submits anything — publication is a human action.**

## VERDICT (v1): NOT release-ready. 7 blockers, 8 warnings.

The mathematics is in excellent shape. This review independently re-verified
the load-bearing claims live (script preserved in the session scratchpad;
results reproduced below): master ladder vs both persisted bracket files 12/12,
j=2 root ≡ published T_n symbolically for n=3..11, the j=3 rung ≡ the
(G_m, α_m) quadratic symbolically for n=3..14, discriminant < 0 for n≤6 at
λ=1, first window at n=7 with exact edges (26.176, 30.378). Zero numerical
contradictions found. The blockers are traceability (three headline counts have
no persisted script or artifact), two stale numbers left over from the pre-fix
1,538,164 scan, one conjecture-as-fact sentence, and the unassembled package.

---

## BLOCKERS

### B1 — The verification battery's headline counts (21/21, sixteen monomials, 702/702) have NO persisted script or artifact
The Reproducibility section promises "the master-formula checkers (symbolic and
sign-grid) ... are released with this paper", but no such scripts exist in
lab/ and no results/*.json records these three counts. They appear only in
research/master-formula.md and article/DATA_LOG.md (log prose, not artifacts).
Additionally the arithmetic of "21" is inconsistent with the stated ranges:
j=2 (n=3..11) = 9, j=3 (n=4..9) = 6, j=4 (n=5..10) = 6, j=5 (n=6) = 1 —
that is 22 cases, not 21. And the j=5, n=6 bracket underlying the
"sixteen monomial identities" was never persisted (no T2n10_brackets.json).
Required: write lab/master_symbolic_check.py (ladder vs T2n6/T2n8 brackets,
j=2 vs T_n, j=5 n=6 bracket extraction + 16-monomial overdetermination) and
lab/master_sign_grid.py (the 702-point grid incl. blind j=6), run them, persist
artifacts with run metadata, reconcile 21 vs 22, and update the tex numbers.
Mitigation from this review (so the fix is bookkeeping, not doubt): live
re-verification confirms j=3 brackets 6/6 and j=4 brackets 6/6 proportional to
the ladder with sign (−1)^{j−1}; j=2 root ≡ T_n for n=3..11; the five j=5,n=6
ladder coefficients equal the DATA_LOG-recorded fitted a_i = (4096, 15360,
23760, 16800, 4725) up to one positive constant (factor 2). The 702-grid's
substance (incl. blind j=6) is independently covered by attack_master.json
(4,060/4,060, j≤11, n≤12). The claims are true; they are just not traceable.

### B2 — Stale count in "Explain it to anyone": "one and a half million points"
Leftover from the superseded even-D scan (1,538,164). The current artifact
(results/master_completeness_scan.json, git 761f6e8) records 3,053,832.
Abstract and figure caption already say ~3 million; this sentence must match.

### B3 — fig_knives.png is stale and has no generator
The embedded yellow annotation reads "(1,538,164 exact checks, 0 hits)" — the
pre-fix count; must be 3,053,832 (caption correctly says "3-million-point").
The bottom axis label is cropped by the image edge. No fig_knives generator
script exists anywhere in the repo (experiment-contract + paper2 precedent B5/
B6: figures re-exported from a persisted plotting script). Write the generator,
regenerate, ship both.

### B4 — Conjecture asserted as fact in the popular section
"The cliff we published is the real edge — and now we know it not from one
measurement, but from the complete anatomy of every way to fall." This states
Conjecture 1 of [shore] as established (same class as paper2 blocker B2), and
"every way to fall" ignores the ℓ=0/fixed-spin carve-out that Secs. 4–5
correctly state. Reword scoped, e.g.: "every trapdoor of this kind that we
scanned — three million exact checks — stays on the far side of the cliff; the
cliff line has survived its hardest test yet."

### B5 — 2052/2052 misattributed to the blind levels only
Tex: "A blind check of this rung on levels the fit never saw (n=10..12) gave
2052/2052 sign agreements." Artifacts (t2n6_law_check.json;
t2n6_window_vs_shore.json blind_check) say the 2052 grid spans n=4..12
(9 levels × 19 even D in 4..40 × 12 λ in 0.1..20), of which the fit used
n=4..9; the never-seen subset is 684 points. Allowed rewording: "2052/2052
sign agreements over n=4..12, including the never-fitted levels n=10..12."

### B6 — t2n6_window_vs_shore.json has no generating script, and "λ up to 10^3 and n up to 4λ" is not what it records
The artifact's command field says "python (dip scan inline, persisted here)" —
the dip-scan code was never persisted (experiment-contract violation; paper2
precedent B6). The paper cites this artifact for the 2.17 margin and for the
trace "for λ up to 10^3 and n up to 4λ"; the artifact records the dense grid as
"lam 0.05..100 (dense to 20), n 4..300" plus tail λ ∈ {200, 500, 1000}
(worst margin 336.05 at λ=200, n=687) — the tail's n-range is not recorded, and
n≤300 < 4λ for 75<λ≤100 on the dense grid. Required: recreate the dip-scan
script, regenerate the artifact with explicit grids, or reword the tex to the
recorded coverage ("λ≤100 with n≤300, plus λ=200, 500, 1000 tails").

### B7 — Release package does not exist; footnote tense
release/qg-master-formula/ is unassembled while the author footnote says "Code
and data released with this preprint" (present tense) and the Reproducibility
section lists deliverables that partly do not exist (B1, B3, B6). Assemble per
the manifest below, clean-clone test it, secret-scan it; only after repo+DOI
exist is the present tense true (paper1/paper2 lesson W9).

---

## WARNINGS

- **W1 — "a new phenomenon" (abstract).** Novelty-adjacent wording with no
  literature gate for the window phenomenon. The body's "invisible at j=2"
  (novel relative to our own j=2 law) is the defensible reading; prefer that
  wording, or add the INSPIRE-scoped "to our knowledge" form used in paper 2.
- **W2 — window upper edge "30.3".** Exact edges are 26.176 and 30.378; "30.3"
  is an inward truncation, standard rounding gives 30.4. Either print
  "(26.18, 30.38)" or "(26.2, 30.4)". Same truncation lives in the artifact's
  prose field; harmless there, but the paper should not understate its own
  window. (Integer confirmations are unaffected: 27–30 negative, 26 and ≥31
  positive — attack_master.json rows.)
- **W3 — abstract "j≥2" lacks the j≤n−1 cap.** Theorem 1 states 2≤j≤n−1
  correctly; "near-leading" gestures at it, but one token fixes it.
- **W4 — "reproduces the trajectory law ... exactly, for all n".** Verified
  symbolically for n≤11 (this review) and via 24/24 exact root-zeros n≤10
  (attack). The general-n identity is one line of algebra given the critic's
  general-n derivation; either include that line or scope the claim.
- **W5 — "an independent adversarial review ... ran its own from-scratch
  evaluator".** The critic authored attack_master.py but had no execution tool;
  the lab executed it (exit 0, artifact git 761f6e8; DATA_LOG 2026-08-15).
  Deterministic exact-rational code, so the force is intact, but consider
  "whose from-scratch evaluator, executed against the formula, returned
  4,060/4,060" to keep agency accurate.
- **W6 — T2n8_brackets.json metadata says command "python lab/t2n6_bracket.py".**
  It was produced by lab/tj_bracket.py with TJ_J=4 (the command string is
  hard-coded). Fix the script's metadata line when persisting B1's artifacts.
- **W7 — in-figure neon styling / headline caps.** Tolerated for arXiv per
  project precedent (paper 1 W14, paper 2 W7); retitle for any journal version.
- **W8 — unused \newtheorem{conjecture}; ℓ=0 extension.** The conjecture
  environment is defined and never used (harmless). The critic's informational
  j=n (ℓ=0) extrapolation agreed 96/96, suggesting the Discussion's "ℓ=0 ...
  lives outside the trajectory scaling" may be strengthenable for free — a
  candidate remark, not required.

---

## CLAIM-EVIDENCE LEDGER (task 1 — every number traced)

| Tex claim | Artifact | Status |
|---|---|---|
| 21/21 symbolic matches, j≤5 | NONE persisted (master-formula.md + DATA_LOG prose only); ranges sum to 22 | **B1**; substance re-verified live 12/12 + 9/9 + coeffs |
| j=5, n=6: 5 coefficients vs 16 monomial identities | NONE persisted; DATA_LOG 2026-08-15 records a_i values | **B1**; ladder coeffs match logged a_i × 2 (live) |
| 702/702, j≤6, n≤10, λ∈[¼,7], D≤36, blind j=6 | NONE persisted | **B1**; superseded in substance by attack 4,060/4,060 |
| 4,060/4,060 incl. odd D, non-integer D (7/2, 53/7), λ=10⁻²/10², n=15 | attack_master.json: total 4060, mismatches 0; tallies odd 2028, even 2004, non-int 28, λ-extreme 1368, deep 72; git 761f6e8, falsified false | OK |
| integral identity "45 exact α values, 3465 checks" | attack_master.json identity.checks=3465; script alphas = 40 (k/7) + 5 extras = 45 distinct; 77 (l,u) pairs × 45 | OK |
| j=2 root exact zero of amplitude, 24/24 | attack_master.json j2_root cases=24, failures [] | OK |
| 2052/2052 "on levels the fit never saw (n=10..12)" | t2n6_law_check.json: checks 2052, fitted n=4..9, blind n=10..12; window_vs_shore blind_check: grid n=4..12 | **B5** — 2052 spans n=4..12; blind subset 684 |
| 3,053,832 exact verdicts, 0 violations; n≤40, all j, every integer D ≤ exact ⌊min T_n⌋, 68 λ in [0.05,50] | master_completeness_scan.json (checks 3053832, alarms [], nmax 40, region "ALL integer D ... exact floor", git 761f6e8) + script (60+8 = 68 λ; exact-rational floor per critic defect 2 fix) | OK |
| "3-million-point battery" (caption) | 3,053,832 | OK |
| figure-internal "(1,538,164 exact checks, 0 hits)" | superseded artifact count | **B3** stale |
| "one and a half million points" (Explain) | superseded artifact count | **B2** stale |
| window (26.2, 30.3) at n=7, λ=1 | window_vs_shore string_window_n7; live exact edges 26.176 / 30.378 | OK (**W2** rounding) |
| a_{7,8} < 0 at D=28,30; > 0 at D=26,32 | window_vs_shore + attack window rows (also 27,29 neg; 31 pos) | OK |
| discriminant < 0 for n≤6 at λ=1; first window at level 7 | no dedicated artifact; live re-check: disc = −572/9, −19456/405, −526076/11025, −345344/11025 (n=3..6), +5960164/245025 (n=7) | TRUE; persist inside B1's checker |
| G_m, α_m closed forms | window_vs_shore "law" field; live symbolic ladder ≡ Bhat, n=3..14, positive constant | OK |
| closest margin 2.17 at λ=0.05 | window_vs_shore dip_scan worst_margin 2.1729 at λ=0.05, n=6 | OK (artifact has no script — **B6**) |
| "λ up to 10³ and n up to 4λ" | dip grid n≤300 (λ≤100), tail λ∈{200,500,1000} n-range unrecorded | **B6** mismatch |
| blades n=6,8,11; string diamond at D=23 (figure) | figure levels 6/8/11 match caption; D=23 consistent with paper 2 shore (min T_n(1)=23 at n=4; EV-CORR-0003) | OK |
| "every ... T_n reproduced for all n" (j=2 rung) | symbolic n≤11 (live) + attack roots n≤10 | OK scoped (**W4**) |

## OVERCLAIM AUDIT (task 2)

- **Theorem label: JUSTIFIED.** master-formula-review.md §2 records a complete
  independent end-to-end re-derivation ("VERDICT: CORRECT (analytic)", incl.
  hand-verified n=3 j=2 and n=4 j=3 rungs and a no-sign-flip argument on the
  claimed domain), and its condition — machine confirmation via
  attack_master.py — is now satisfied (executed, exit 0, artifact falsified:
  false, git 761f6e8). Both critic defects in the tex (sign typo in the
  generating identity; abstract exhaustiveness wording) are verified fixed:
  Sec. 2 now prints ∑_t Ê_{2t}(−z²)^t, and the abstract/Sec. 4 state finite
  ranges, ℓ≥2, and the formula-dependency of the sweep.
- **Conjecture scoping: OK in the scientific sections.** No new conjecture is
  asserted; Conjecture 1 of [shore] is referenced, the sweep is presented as
  "within these ranges", and Sec. 4 states "its force rests on the formula's
  independent verification" (critic defect 4 fixed). Violation only in the
  popular section (**B4**).
- **"every"/"all" wording:** abstract "every trajectory constraint (ℓ≥2)" and
  "every knife in these ranges" are scoped by the parenthetical finite ranges —
  OK. "every near-leading partial wave, j≥2" lacks j≤n−1 (**W3**). Discussion
  "any level, any near-leading trajectory, any dimension" is the theorem's
  actual domain (D>3) — OK.
- **ℓ=0 / fixed-spin carve-out: PRESENT** (Sec. 4 sentence + Discussion next
  steps), and truthful: paper 2's direct scans (grav_full_body 494/494, all
  even ℓ≤2n−2) cover those waves.
- **Gated words:** "proved"/"re-proved" appear for (i) the paper-2 T_n law
  (gate passed: hand-proof + released) and (ii) the integral identity's
  mechanical interpolation proof (executed, 3465 checks) — both allowed.
  "confirmed by exact evaluation" — artifacts exist — allowed. "first such
  window" — ordinal within the level sequence, machine-verified — allowed.
  No "discovered/novel/refuted" anywhere. "new phenomenon" — **W1**.
- **eft_map_d4.json (exploratory) is NOT cited in paper 3 — verified.** The AI
  disclosure's known-answer-gate anecdote refers to it only via the public log,
  keeping the failure visible without promoting the exploratory result. Correct
  handling.

## CITATIONS (task 3 — all four bibitems)

- CHR2024b: arXiv:2408.03362 = Phys. Rev. D 111, 086034 (2025) — matches
  EV-QG-0003 (verified_by metadata+content true) and paper 2's arXiv-API check
  (DOI 10.1103/PhysRevD.111.086034). CORRECT.
- CHR2024: arXiv:2406.02665 = Phys. Rev. Lett. 133, 251601 (2024) — matches
  EV-QG-0004; arXiv-API-verified in paper 2 review. CORRECT.
- shore: "The Shore of Closed-String Gravity", 10.5281/zenodo.21944818 —
  matches paper2/main.tex self-DOI, release/qg-gravity-shore/CITATION.cff, and
  DATA_LOG (DOI minted 2026-08-15). CORRECT.
- island: "The Island Has Edges", 10.5281/zenodo.21934462 — matches
  paper/main.tex self-DOI and DATA_LOG 2026-08-14. CORRECT.
- Footnote attribution "21934462 (open string), 21944818 (closed string)" —
  correct (island = Veneziano/open, shore = closed/graviton).

## ALLOWED PUBLIC WORDING (exact forms, per claim-gates)

1. Master formula: "derived, not fitted (residue roots + an exact
   monomial–Gegenbauer integral); independently re-derived end-to-end by an
   adversarial review and confronted with its from-scratch exact evaluator:
   4,060/4,060 sign agreements including odd and non-integer D" — ALLOWED
   (with W5's agency tweak recommended).
2. Integral identity: "proved mechanically by rational-function interpolation
   at 45 exact α values (3,465 checks, l≤10, u≤6)" — ALLOWED.
3. j=2 rung: "reproduces the trajectory law a_{n,2n−4}≥0 ⟺ D≤T_n(λ) of
   [shore]" — ALLOWED; add scope per W4.
4. Windows: "each level cuts a finite window of dimensions and re-releases at
   large D; for the string the first window opens at level 7, edges 26.18 and
   30.38; exact signs: negative at D=27–30, positive at D=26 and D≥31" —
   ALLOWED.
5. Battery counts "21/21", "sixteen monomial identities", "702/702" — BLOCKED
   until B1's scripts+artifacts exist and the 21-vs-22 count is reconciled;
   thereafter ALLOWED with the corrected number.
6. Blind j=3 check: "2052/2052 sign agreements over n=4..12, including the
   never-fitted levels n=10..12" — ALLOWED. "2052/2052 on levels the fit never
   saw" — BLOCKED (B5).
7. Completeness: "3,053,832 exact verdicts at every integer D inside the
   conjectured-allowed region (j=3..n−1, n≤40, 68 values of λ∈[0.05,50],
   exact-rational floor), zero violations; the sweep evaluates the master
   formula, whose force rests on its independent verification" — ALLOWED.
   "The envelope IS the boundary", "the cliff we published is the real edge",
   any completeness-as-fact or "confirmed the conjecture" — BLOCKED
   (conjecture gate not passed; human-approved conjecture wording only).
8. Margin trace: "the lower window edge stays above the envelope everywhere on
   the scanned grids (λ≤100 with n≤300, plus λ=200, 500, 1000 tails), closest
   approach 2.17 dimensions at λ=0.05" — ALLOWED after B6's script/artifact
   fix; "λ up to 10³ and n up to 4λ" — BLOCKED as currently unrecorded.
9. Popular section: "not a single trapdoor opens on the safe side [in three
   million exact checks]" — ALLOWED; "the cliff we published is the real
   edge" — BLOCKED (B4).
10. "discovered / proved / novel / first / confirmed / refuted" beyond the
    instances in items 1–4: BLOCKED (no matching gates).

## RELEASE CHECKLIST (templates/release-checklist.yaml, filled)

```yaml
project_id: "qg-bootstrap-paper3"
clean_clone_test: pending      # run on the assembled release/qg-master-formula package (B7)
environment_lock: pass         # uv.lock; pure exact-rational stack (Fraction + sympy)
test_suite: pending            # uv run sb check after B1/B3/B6 scripts land
citation_audit: pass           # all 4 bibitems verified (IDs, journal refs, both Zenodo DOIs)
license_audit: pass            # own code, MIT per package precedent; no third-party code shipped
data_availability: fail        # B1 (21/21, 16, 702/702 unpersisted), B6 (dip-scan script), B7 (no package)
ai_use_disclosure: pass        # substantive section; names the KA-gate event; matches DATA_LOG slice 10
figures_and_tables: fail       # B3: stale in-figure count, no generator, cropped axis label
repository_release: pending    # assemble manifest below; then real URL/DOI, recompile
doi: pending                   # minted with the package — by the human
preprint: pending              # human action only
journal_candidate: pending
human_approval: pending        # publication is always a deliberate human action
```

## PUBLICATION PACKAGE MANIFEST — release/qg-master-formula/ (to assemble)

Precedent: release/qg-gravity-shore (README + LICENSE + CITATION.cff +
AI_DISCLOSURE + lab/ + results/ + research/ + paper/).

- README.md — claims → scripts → artifacts map; companion DOIs 21934462 /
  21944818; how to re-run every battery; exploratory-vs-confirmatory note.
- LICENSE (MIT), CITATION.cff (self-DOI once minted; related identifiers to
  both companion DOIs), AI_DISCLOSURE.md (mirrors the tex section, incl. the
  known-answer-gate event).
- paper/: main.tex, main.pdf, fig_knives.png (regenerated per B3).
- lab/: tj_bracket.py, t2n6_bracket.py, t2n6_law_check.py, attack_master.py
  (the critic's script — required), master_completeness_scan.py,
  grav_full_body.py + hunt_2n8.py (imported by tj_bracket.py — package must be
  runnable), PLUS the new deliverables: master_symbolic_check.py and
  master_sign_grid.py (B1), the window-vs-shore dip-scan script (B6), and the
  fig_knives generator (B3).
- results/: T2n6_brackets.json, T2n8_brackets.json, t2n6_law_check.json,
  t2n6_window_vs_shore.json (regenerated with recorded grids, B6),
  attack_master.json, master_completeness_scan.json, plus the new B1 artifacts.
  Never rewrite the existing ones except by re-running their scripts.
- research/: master-formula.md, master-formula-review.md (the adversarial
  review ships with the paper — its execution caveat is answered by
  attack_master.json), evidence-records.jsonl, DATA_LOG excerpt (append-only;
  must include the master-formula entries, the KA-gate failure, and the
  1,538,164 → 3,053,832 re-run history — failures stay visible). Optional:
  eft_map_d4.json + lab/eft_map_d4.py if the log excerpt references them,
  shipped with their `exploratory: true` flag intact.
- Exclude: research/pdfs/ (third-party), __pycache__, main.aux/log/out,
  Master-Formula-DRAFT.pdf, letter drafts, anything personal.
- After assembly: clean-clone run of every script (clean_clone_test), uv run
  sb check, secret scan, then the HUMAN creates the repo, mints the DOI, the
  footnote's "released with this preprint" becomes true, recompile, and the
  human submits. **No part of this is an agent action.**

---
Independent re-verification script used by this review (not part of the repo):
session scratchpad release_check_paper3.py; outputs quoted in the ledger above.
