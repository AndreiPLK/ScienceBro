# Release review — projects/qg-bootstrap/paper4/main.tex

Reviewer: release-reviewer agent, 2026-08-15 (v1).
Scope: paper 4 ("The Blades Never Touch the Shore", 4 pp., fig_tangent.png +
fig_knives.png) against lab/blade_proof.py, lab/attack_blade_theorem.py,
research/blade-theorem-review.md (domain-critic), results/ artifacts, and the
binding rules (.claude/rules/claim-gates.md, evidence-contract.md,
experiment-contract.md). Compiled main.pdf builds clean (4 pages, no undefined
refs); main.tex carries no secrets or local paths.

**No agent publishes, pushes, or submits anything — publication is a human action.**

## VERDICT (v1): NOT release-ready. 7 blockers, 6 warnings.

The theorem itself is in strong shape: both gates passed and both were
REPRODUCED by this review from committed HEAD (f00f145) in an isolated copy —
`blade_proof.py` exit 0, ALL CERTIFIED, 1,047 logged cells, 81 s; the critic's
independent `attack_blade_theorem.py` exit 0, NO COUNTEREXAMPLE, all 1,038
branch cells (incl. the 740 formerly-uncovered ones) re-certified, tail lemmas
rebuilt over Q(√3), minimum exact margin 2.1574. The blockers are: the
headline closest-approach number is contradicted by the lab's own artifact
(2.17 at λ≈0.05 is a grid-edge artifact; the exact scans reach 2.157 at
λ=0.02 and the margin keeps shrinking toward λ→0), the strictness wording the
critic explicitly warned about, one unpersisted 60,000-point battery, a lemma
misattribution (√(5/3) is not what Lemma 2 proves), artifact-metadata defects
the critic flagged as "must fix before any write-up", the missing package, and
a figure with no persisted generator.

---

## BLOCKERS

### B1 — The closest-approach claim "2.17 dimensions, at λ≈0.05" is wrong per the lab's own artifacts
Appears in the abstract ("The closest approach in all of parameter space is
2.17 dimensions, at λ≈0.05"), Sec. 2 ("2.17 dimensions at λ=0.05, level 6"),
and the fig:knives caption ("closest approach 2.17 dimensions").
- Source of 2.17: results/t2n6_window_vs_shore.json, worst_margin 2.1729 at
  λ=0.05, n=6 — but that grid STARTS at λ=0.05; the worst point is the grid
  edge (this artifact was already flagged in the paper-3 review as B6).
- The critic's battery went finer: results/attack_blade.json min_margins
  records EXACT margins down to 2.157391581 at λ=1/50 (=0.02), m=3 (n=6) —
  again the minimum sits at the scan's lower edge.
- This review re-checked the trend live (exact closed forms, float64 eval):
  margin(n=6) = 2.1990 (λ=0.1), 2.1729 (λ=0.05), 2.1574 (λ=0.02), 2.1522
  (λ=0.01), 2.1496 (λ=0.005), 2.1475 (λ=0.001); the λ→0 limit is ≈2.1471
  (window exists in the limit; shore →9, window edge →≈11.147). The margin is
  monotone decreasing toward λ→0: there is no interior minimum at λ≈0.05 and
  the infimum is ≈2.147, approached (not attained) as λ→0 at level 6.
- Also note: "in all of parameter space" states a measured scan result as a
  global fact; certificates prove only margin ≥ 0 (see B2). No certified
  positive lower bound on the gap exists.
Required: persist an exact closest-approach scan that covers λ→0 (extend
attack's closest part or tools/night_queue.py's task below λ=0.01, or add the
exact λ→0 limit computation), then reword everywhere, e.g.: "the measured
closest approach shrinks toward small λ at level 6: exact-scan minimum 2.157
dimensions at λ=0.02, with infimum ≈2.147 as λ→0; the certified statement is
only that the margin never reaches zero." The fig:knives caption and abstract
must carry the corrected number.

### B2 — Strictness wording: the theorem claims more than the certificates deliver
Critic finding (b) and expert question Q3, verbatim warning: ">= certificates
do NOT deliver [a strict inf-gap] at possible touching points; the paper
should define the statement per-point." The tex still says:
- Theorem 1: "its lower edge exceeds T̂(λ)" — strict inequality of the edge
  itself = the inf-gap reading; the certificates give B̂(T_k) ≥ 0 and the
  vertex condition, i.e. edge ≥ T̂, with strictness only for points INSIDE the
  open window.
- Abstract: "lies strictly above the shore" — undefined; allowed only under
  the per-point reading.
Required rewording (allowed forms in the wording section below): state the
theorem per-point — "every dimension D inside a negativity window satisfies
D > T̂(λ); consequently a_{n,2n−6} ≥ 0 everywhere in D ≤ T̂(λ)" — and change
"its lower edge exceeds" to "its lower edge is at least T̂(λ), so every point
of the (open) window strictly exceeds it". The "Consequently a_{n,2n−6}≥0..."
sentence is exactly right and stays.

### B3 — The 60,000-point stress test has NO persisted script or artifact (paper-3 precedent B1/B6)
Verification section: "60,000 random points across all regimes ... found
minimum margin 2.18 dimensions and no counterexample." This exists only as
DATA_LOG.md prose (2026-08-16 entry, "min margin 2.18 dims"); commit a305742
shipped no scan script and no results/*.json for it. An exit code that was
never persisted cannot be audited — the same lesson the paper itself preaches
in its AI-disclosure section.
Mitigation (substance is covered by persisted batteries): attack_blade.json
float_scans = 13,349 points, float_min_margin 2.1789, suspects re-checked
exactly (40); exact_scans = 28,680 exact checks (21,438 with windows);
closest_approach_exact.json = 24,375 exact checks, 0 alarms (generator
persisted: tools/night_queue.py task_closest_approach_exact, λ∈[0.01,0.40],
D 4..39, n 4..29, j∈{3,4,5}).
Required: either persist the 60k script + artifact (with run metadata) and
keep the sentence, or reword the Verification section to the persisted
batteries (recommended; exact wording below). Note 2.18 also becomes stale
once B1's finer scans are quoted.

### B4 — √(5/3) is attributed to Lemma 2, which proves 4/3
Sec. "The exact tangency": "windows only exist for ρ≤√(5/3)<ρ* (Lemma 2)".
Lemma 2 (window containment) proves s ≤ (4/3)(m+3), i.e. ρ = s/m ≤ (4/3)(1+3/m)
→ 4/3 ≈ 1.333 — NOT √(5/3) ≈ 1.291. √(5/3) is the sharp asymptotic window-tip
ratio, derived by the critic (review, expert question Q1: from the
leading-order cancellation 4α ~ G² ~ m²/9) and asserted directionally by the
attack script (the ρ* = 1+1/√3 direction lies outside the window region); it
is not a certified lemma. The proof chain is UNAFFECTED: 4/3 < ρ* = 1.577
already closes the argument. The abstract's "windows only exist up to
ρ=√(5/3), strictly inside" has the same problem unattributed.
Required: cite Lemma 2 for the certified ρ ≤ (4/3)(1+3/m) bound and present
√(5/3) as the sharp asymptotic value (derived + machine-checked, not part of
the certificate chain), e.g.: "windows are confined to ρ ≤ (4/3)(1+3/m)
(Lemma 2) — asymptotically to ρ ≤ √(5/3) — both strictly inside ρ*."

### B5 — Artifact metadata defects the critic flagged are still unfixed
1. blade_proof.json "branches" field claims "k>=4 on [(2/3)(k-3),(2/3)(k-2)]"
   while the code (and the artifact's own cells) use the 3/5-spaced grid
   mu_lo=(3/5)(k−5/2) — critic secondary defect 2, verbatim: "The artifact
   mis-describes its own coverage; fix the metadata ... Must be fixed before
   any write-up." Still at lab/blade_proof.py line 277.
2. blade_proof.json records git 4ff67cb, but the coverage fix (line 175) was
   only committed in bf9913d — the artifact was generated from a dirty tree,
   so its recorded SHA does not contain the code that produced it
   (experiment-contract: every run records its git commit — reproducibly).
3. attack_blade.json records NO git commit and NO command at all (compare
   attack_master.json's meta block) — experiment-contract violation.
Mitigation: this review re-ran both scripts from committed HEAD in an isolated
copy; both reproduce exactly (exit 0 / exit 0, ALL CERTIFIED / NO
COUNTEREXAMPLE, same 1,047 cells, same min margin 2.1574). The substance is
sound; this is bookkeeping.
Required: fix the branches metadata string and add git+command meta to the
attack artifact writer, then regenerate both artifacts by re-running their
scripts from a clean committed tree (never edit artifacts by hand).

### B6 — fig_tangent.png has no persisted generator (paper-3 precedent B3)
article/visuals/tangent-fleet.html is generated OUTPUT (inline data arrays
with float artifacts, committed as 18 lines in 4ff67cb), not source: no script
in the repo produces it, and no scripted HTML→PNG step is recorded for
fig_tangent.png (fig_knives.py documents its headless-chrome render command;
tangent has nothing). The figure's content is purely analytic (6ρ², the line
(12+4√3)ρ−(8+4√3), ρ*=1+1/√3, the √(5/3) shaded zone), so regeneration is
trivial — which is exactly why the generator must exist.
Required: write the generator (fig_tangent section in fig_knives.py or a
lab/fig_tangent.py) with the render command documented, regenerate, ship both.
fig_knives.png itself is fine: lab/fig_knives.py is persisted with the render
command and the caption (levels 6, 8, 11; diamond at D=23; battery count
3,053,832) matches the generator and artifacts — but its caption's "closest
approach 2.17" falls under B1.

### B7 — Release package does not exist; footnote tense
release/qg-blade-theorem/ is unassembled while the author footnote says "Code
and data released with this preprint" and the Reproducibility section says
"one script ... released with this paper" (present tense). Same as paper-3 B7
(paper1/paper2 lesson W9). Assemble per the manifest below, clean-clone test,
secret-scan; the tense becomes true only after the human creates the repo and
mints the DOI.

---

## WARNINGS

- **W1 — "several hundred certificates" and "every certificate is a polynomial
  with manifestly nonnegative coefficients".** The artifact logs 1,047 cells:
  993 are no-window cells proved by univariate root isolation + positive
  sample (NOT positive-coefficient certificates), 42 tail certificates, 3 B&V,
  2 N=0, plus the four deep-water lemma certificates over Q(√3). So (i) the
  count is ~a thousand, not several hundred; (ii) Sec. 2's "every certificate
  is a polynomial with manifestly nonnegative coefficients" contradicts the
  same paragraph's own "univariate root isolation" route. Say: "1,047 logged
  certificate cells — positive-coefficient certificates plus exact univariate
  no-window checks (root isolation)".
- **W2 — Discussion, j≥4: "the master formula gives the same ladder structure,
  the same asymptotic cone".** The ladder structure is the proven master
  formula and the 3,053,832 battery covers all j — fine; "the same asymptotic
  cone" for j≥4 is asserted as fact with no artifact or derivation on record.
  Hedge it ("appears to give the same asymptotic cone"); the rest of the
  paragraph is properly conjectural ("natural next step", "appear to be").
- **W3 — "danger zones we discovered with the master formula" (Explain
  section).** The windows' existence passed its gates in paper 3 (independent
  review + exact evaluation, published, DOI 10.5281/zenodo.21947272), so the
  word is defensible — but paper 3 itself deliberately avoided "discovered"
  everywhere. Recommend "found" for consistency with the program's own
  wording discipline.
- **W4 — prover internals: nsimplify split points and unproven denominator
  signs (critic secondary defects 3 and 4) are still in blade_proof.py.**
  Soundness is carried by the attack script, which re-certifies every cell
  with exact rational separators and proves denominator positivity explicitly
  at each use. Acceptable for release IF the package README states that the
  independent battery, not the prover alone, is the load-bearing verification
  of those two steps. Cleaner: apply the critic's two fixes.
- **W5 — abstract "envelope branches for λ≤26" vs body/code (0, 26.1].**
  Cosmetic; branches cover to 26.1 and overlap the tail on [26, 26.1). Use
  26.1 in both places (the overlap is a feature — say so).
- **W6 — "60,000 random points ... levels to n=5000" (Verification).** If B3
  is resolved by rewording to the persisted batteries, note their actual
  ranges: attack float recon reaches m ≤ 10^5 (large-m strip) and deep water
  λ ≤ 2000 with n ≤ 6λ; exact junction scans reach m ≤ 1000, closest-zone
  m ≤ 3000. Do not quote n=5000 unless a persisted artifact records it.

---

## CLAIM-EVIDENCE LEDGER (task 1 — every number traced)

| Tex claim | Artifact / source | Status |
|---|---|---|
| 740 uncovered (k,m) cells | blade-theorem-review.md Finding-1 table (sums: 7·5+6·10+5·15+6·20+6·25+6·30+3·40 = 740 — re-verified); pre-fix artifact preserved at commit a305742; attack_blade.json coverage_gap parser + m_start map (n_uncovered now 0 post-fix) | OK — traceable |
| "several hundred certificates" | blade_proof.json: 1,047 logged cells (993 no-window + 42 tail + 3 B&V + 2 N=0 + lemmas); attack re-certified 1,038 branch cells | **W1** — say ~1,047 |
| closest approach 2.17 at λ≈0.05, level 6 | t2n6_window_vs_shore.json 2.1729@λ=0.05 (grid EDGE, grid starts at 0.05); attack_blade.json exact 2.157391581@λ=1/50; live re-check: monotone ↓ toward λ→0, infimum ≈2.1471 | **B1** — number wrong |
| min margin 2.18, 60,000 random points, n to 5000, λ to 1500 | DATA_LOG prose only; no script, no artifact (commit a305742 shipped neither) | **B3** (+ **W6**) |
| 24,375 exact checks (not cited in tex) | closest_approach_exact.json (checks 24375, alarms [], git e0d896c); generator persisted: tools/night_queue.py task_closest_approach_exact | OK — ship as supporting |
| 3,053,832 points (Verification + Discussion) | master_completeness_scan.json (checks 3053832, alarms [], nmax 40, git 761f6e8) | OK |
| tangency quadratic 6ρ²−(12+4√3)ρ+(8+4√3), discriminant ≡ 0, ρ*=1+1/√3 | re-verified by hand: (12+4√3)²−24(8+4√3) = 192+96√3−192−96√3 = 0; root (12+4√3)/12 = 1+1/√3; attack rebuilds L1/L3 over Q(√3) (L1_rebuild 18 monomials 0 bad; L3a 120/0; L3b 42/0), critic audit (e) | OK |
| windows only up to ρ=√(5/3) "(Lemma 2)" | Lemma 2 / L2 certs prove s ≤ (4/3)(m+3) (16/9)(m+3)² bound); √(5/3) is the critic's asymptotic derivation + attack directional assertion | **B4** — misattributed |
| branches k=3..45, rational breakpoints, cover (0, 26.1] | blade_proof.py (mu_hi(45)=261/10=26.1); critic audit (a): junctions contiguous, tail overlap [26,26.1); repro run branch k=45 [51/2,261/10] OK | OK (artifact metadata field wrong — **B5.1**) |
| m ≤ 78 no window at λ≥26 / m ≥ 79 tail | blade_proof.py T0 (range 1..79) + L2/L3 (m=v+79); attack T0_rebuild m1..78, L2/L3 rebuilds; critic audit m-axis: no gap | OK |
| S²max ≤ (16/9)(m+3)², β=4α−G²>0 | blade_proof.py L2 certs e1/e2; attack L2_rebuild + beta_identity_and_positivity (β factorization re-checked symbolically) + explicit denominator-sign proofs | OK |
| shore asymptote D=(12+4√3)λ, witness k=⌊√3λ⌋+2 | blade_proof.py L1 cert over Q(√3); attack L1_rebuild from scratch; critic audit (e): constant is the TIGHT asymptote, floor bookkeeping sound | OK |
| ALL CERTIFIED exit 0 / attack exit 0 | blade_proof.json all_certified true; attack_blade.json verdict NO COUNTEREXAMPLE, counterexamples [], negative_control_ok true; BOTH reproduced by this review from HEAD f00f145 (isolated copy, exit 0/0, same cells, same min margin) | OK (meta defects — **B5**) |
| levels 6, 8, 11 + diamond D=23 (fig:knives) | fig_knives.py (persisted, render command documented); D=23 = min T_k(1), paper-2 shore | OK (caption 2.17 → **B1**) |
| 75 s prover runtime | blade_proof.json runtime_s 74.8; DATA_LOG "75s" — NOT cited in the paper | irrelevant to tex; OK |
| G_m, α_m, B̂_n, sign a_{n,2n−6}=sign B̂_n | master formula, paper 3 (independently re-derived, published DOI 10.5281/zenodo.21947272); treated as GIVEN per critic's scope note | OK |

## OVERCLAIM AUDIT (task 2)

- **Theorem label: JUSTIFIED.** Two independent verifications exist and both
  are green post-fix: (i) the fixed prover, ALL CERTIFIED exit 0 with
  per-cell auditable coverage (the critic's coverage parser confirms 0
  uncovered cells); (ii) the critic's independent battery (imports nothing
  from the prover, own exact evaluator with a documented IFF violation test,
  negative control fired), executed by the lab: exit 0, NO COUNTEREXAMPLE,
  all four tail lemmas rebuilt from scratch over Q(√3). The critic's static
  logic audit found the chain sound (junctions, vertex logic incl. degenerate
  discriminants, L2 squaring, L1 floor). This review reproduced both runs
  from committed HEAD. Per claim-gates, "prove/proof/theorem" is allowed —
  CONDITIONAL on B2 (what is proven is the per-point statement) and B4 (the
  lemma attribution must match what was certified).
- **Strictness: as currently worded, overclaims.** See B2. The critic's
  per-point reading is the certified one; the inf-gap reading is not.
- **"in all of parameter space" (abstract): overclaims a scan as a global
  measurement** — see B1; the certified global statement is only margin > 0
  per-point.
- **j≥4 Discussion: properly conjectural overall** ("natural next step",
  "appear to be the only two facts", "would then rest") — with the single
  as-fact assertion "the same asymptotic cone" (**W2**).
- **Gated words sweep:** "prove/proof/proves" — allowed (gates passed, see
  above, conditional on B2/B4). "discovered with the master formula"
  (Explain) — defensible via paper 3's gates, recommend "found" (**W3**).
  DATA_LOG's "KEY discovery" (tangency) does not appear in the tex — the
  abstract's "the fact that..." wording is correct. No "novel", "first",
  "confirmed", "refuted" anywhere in main.tex — verified. The AI-disclosure
  section's honest-failure narrative (two dead prover architectures, the
  740-cell catch, "an exit code proves what a script checked, not what it
  covered") is accurate per DATA_LOG and the review — exemplary; keep it.
- **Negative results visible:** the coverage-gap story is IN the paper
  (Verification + AI disclosure) with the correct count and the pre-fix
  artifact is preserved in git history (a305742) — satisfies "failures stay
  visible". The two failed prover architectures are recorded in DATA_LOG
  (2026-08-15/16 entry). OK.

## CITATIONS (task 3 — all 3 bibitems)

- CHR2024b: arXiv:2408.03362 = Phys. Rev. D 111, 086034 (2025), Cheung,
  Hillman, Remmen — matches EV-QG-0003 (verified_by metadata+content: true)
  and the paper-3 review's arXiv-API check (DOI 10.1103/PhysRevD.111.086034).
  CORRECT.
- shore: "The Shore of Closed-String Gravity", DOI 10.5281/zenodo.21944818 —
  matches DATA_LOG (DOI minted 2026-08-15), release/qg-gravity-shore,
  paper-3 bibliography. CORRECT.
- master: "A Master Positivity Formula...", DOI 10.5281/zenodo.21947272 —
  matches DATA_LOG (paper 3 published 2026-08-15) and
  release/qg-master-formula README badge. CORRECT.
- Footnote companion attribution (21944818 = shore, 21947272 = master formula)
  — CORRECT. Footnote tense — **B7**.

## ALLOWED PUBLIC WORDING (exact forms, per claim-gates)

1. Theorem headline: "we prove that for every level n≥4 and every λ>0, every
   dimension D inside a negativity window of a_{n,2n−6} strictly exceeds the
   near-leading envelope min_k T_k(λ); equivalently, a_{n,2n−6} ≥ 0
   everywhere in the region D ≤ min_k T_k(λ)" — ALLOWED (both gates passed).
   "its lower edge exceeds T̂(λ)" / any inf-gap ("strict gap", "bounded away
   from") phrasing — BLOCKED until a strict-gap margin lemma is certified
   (critic finding (b)).
2. Verification story: "the proof was adversarially reviewed; the review
   found exactly one defect — a coverage gap of 740 branch cells behind a
   reported 'all certified' — which was fixed; the full prover re-run logs
   every cell (1,047), and the reviewer's independent battery (no shared
   code, own exact evaluator, negative control) re-certified every branch
   cell including the 740, rebuilt all four tail lemmas over Q(√3), and
   found no counterexample (exit 0)" — ALLOWED.
3. Tangency: "the blade cone is exactly tangent to the shore asymptote
   D=(12+4√3)λ: the comparison quadratic 6ρ²−(12+4√3)ρ+(8+4√3) has
   identically vanishing discriminant, double root ρ*=1+1/√3" — ALLOWED
   (identity re-verified by hand and by certificate).
4. Containment: "windows are confined to s ≤ (4/3)(m+3) (Lemma 2), and
   asymptotically to ρ ≤ √(5/3) ≈ 1.291 — strictly inside the tangency
   ρ* ≈ 1.577" — ALLOWED. "windows only exist up to ρ=√(5/3) (Lemma 2)" —
   BLOCKED as attributed (B4).
5. Closest approach: "the measured margin shrinks toward small λ at level 6:
   exact-scan minimum 2.157 dimensions at λ=0.02, infimum ≈2.147 as λ→0;
   certificates guarantee only that it never reaches zero" — ALLOWED after
   B1's persisted scan exists. "The closest approach in all of parameter
   space is 2.17 dimensions, at λ≈0.05" — BLOCKED (contradicted by
   attack_blade.json).
6. Batteries: "24,375 exact checks in the closest-approach zone, 0 alarms;
   28,680 exact scan checks and 13,349-point float reconnaissance with all
   40 suspects re-checked exactly (independent battery); 3,053,832-point
   master-formula battery" — ALLOWED (all persisted). "60,000 random points
   ... minimum margin 2.18" — BLOCKED until script+artifact are persisted
   (B3).
7. Upgrade claim: "this upgrades the j=3 sector of the completeness
   conjecture from a 3-million-point battery to a theorem" — ALLOWED (scoped
   to j=3; the conjecture itself stays a conjecture). Any "the envelope IS
   the boundary" as fact — BLOCKED (conjecture gate not passed; unchanged
   from paper-3 review item 7).
8. j≥4: "the master formula gives the same ladder structure and a
   3-million-point clean battery; lifting the certificate architecture to
   general j appears to require generalizing only the containment lemma and
   the exact tangency" — ALLOWED. "gives ... the same asymptotic cone" as
   fact — BLOCKED until derived/persisted (W2).
9. Popular section: "no blade, of any size, anywhere along the infinite
   coast, ever touches the water" — ALLOWED (it is the per-point theorem in
   pictures). "closest any blade ever comes: about two dimensions of
   clearance" — ALLOWED (safe under both 2.17 and 2.147). "danger zones we
   discovered" — prefer "found" (W3).
10. "discovered / proved / novel / first / confirmed / refuted" beyond the
    instances above: BLOCKED (no matching gates).

## RELEASE CHECKLIST (templates/release-checklist.yaml, filled)

```yaml
project_id: "qg-bootstrap-paper4"
clean_clone_test: pending      # run on the assembled release/qg-blade-theorem; this review's isolated-copy rerun of prover+attack passed (exit 0/0) — the package version must repeat it
environment_lock: pass         # uv.lock; exact-rational stack (Fraction + sympy), no GPU, no seeds needed (deterministic)
test_suite: pending            # uv run sb check after B1–B6 fixes land
citation_audit: pass           # all 3 bibitems verified (EV-QG-0003; both Zenodo DOIs cross-checked)
license_audit: pass            # own code only; MIT per package precedent; no third-party code shipped
data_availability: fail        # B3 (60k battery unpersisted), B1 (closest-approach scan missing below λ=0.02), B6 (fig_tangent generator), B5 (artifact metadata)
ai_use_disclosure: pass        # substantive, names the 740-cell catch and the two dead architectures; matches DATA_LOG
figures_and_tables: fail       # B6 (no fig_tangent generator); fig:knives caption number under B1
repository_release: pending    # assemble manifest below; then real URL/DOI, recompile
doi: pending                   # minted with the package — by the human
preprint: pending              # human action only
journal_candidate: pending
human_approval: pending        # publication is always a deliberate human action
```

## PUBLICATION PACKAGE MANIFEST — release/qg-blade-theorem/ (to assemble)

Precedent: release/qg-master-formula (README + LICENSE + CITATION.cff +
AI_DISCLOSURE + lab/ + results/ + research/ + paper/ + media/).

- README.md — claims → scripts → artifacts map; the honest review story (740
  cells, fixed, doubly re-verified); companion DOIs 21944818 / 21947272; how
  to re-run: `python lab/blade_proof.py` (≈80 s, exit 0) and
  `python lab/attack_blade_theorem.py` (≈35 s, exit 0); W4's note that the
  independent battery carries the nsimplify/denominator steps.
- LICENSE (MIT), CITATION.cff (self-DOI once minted; related identifiers to
  both companions), AI_DISCLOSURE.md (mirrors the tex section).
- paper/: main.tex, main.pdf, fig_tangent.png, fig_knives.png (all post-fix
  recompile).
- lab/: blade_proof.py (metadata fixed, B5.1), attack_blade_theorem.py (meta
  block added, B5.3) — both REQUIRED per task; window_vs_shore.py,
  fig_knives.py (+ new fig_tangent generator, B6), master_checks.py and
  master_completeness_scan.py (imported by the night task and the battery),
  PLUS the new deliverables: the closest-approach scan covering λ→0 (B1) and
  the 60k stress script if that sentence stays (B3), and a standalone
  closest_approach_exact.py extracted from tools/night_queue.py (so the
  24,375 artifact's generator ships without the queue machinery).
- results/: blade_proof.json + attack_blade.json (both regenerated from clean
  HEAD, B5.2), closest_approach_exact.json, t2n6_window_vs_shore.json,
  master_completeness_scan.json, plus the new B1/B3 artifacts. Never rewrite
  existing artifacts except by re-running their scripts.
- research/: blade-theorem-review.md (the adversarial review ships with the
  paper — its PENDING-execution caveat is answered by attack_blade.json and
  by this review's clean-HEAD reproduction), this release-review.md,
  evidence-records.jsonl, DATA_LOG excerpt (append-only; must include the
  95%-then-complete entries, the two dead prover architectures, the 740-cell
  catch and fix — failures stay visible).
- media/: tangent-fleet.png, knives-above-shore.png (from the persisted
  generators).
- Exclude: research/pdfs/ (third-party), __pycache__, main.aux/log/out,
  Blades-Theorem-DRAFT.pdf, letter drafts, tools/night_queue.py internals,
  anything personal.
- After assembly: clean-clone run of both gate scripts (exit 0/0 required),
  uv run sb check, secret scan, then the HUMAN creates the repo, mints the
  DOI, the footnote's present tense becomes true, recompile, and the human
  submits. **No part of this is an agent action.**

---
Reproduction evidence for this review (isolated copies, no repo artifacts
touched): session scratchpad repro/ — prover exit 0, "ALL CERTIFIED", 1,047
cells, 81 s; attack exit 0, "NO COUNTEREXAMPLE", min exact margin
2.157391581038169, 35 s; both from committed HEAD f00f145.
