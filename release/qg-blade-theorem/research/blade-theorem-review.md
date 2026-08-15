# Adversarial review: the BLADE THEOREM auto-proof (paper 4 candidate)

Date: 2026-08-15. Reviewer: domain-critic (adversarial, independent).
Objects: `lab/blade_proof.py` (claims exit 0, "ALL CERTIFIED"),
`results/blade_proof.json` (all_certified: true).
Attack script (written from scratch, imports nothing from `blade_proof.py`):
`lab/attack_blade_theorem.py`. Its artifact: `results/attack_blade.json`.
Per instructions, the j=3 bracket form itself is treated as GIVEN (it was
independently verified in `research/master-formula-review.md`); this review
attacks the proof built on top of it.

## Execution status - read this first

This critic session had NO shell/execution tool available.
`lab/attack_blade_theorem.py` is complete and ready but was NOT executed by
the critic. Every "machine battery" statement below is PENDING until someone
runs:

    C:\Users\user\ScienceBro\.venv\Scripts\python.exe projects/qg-bootstrap/lab/attack_blade_theorem.py

(optionally `--fast` for a smoke pass). Exit contract: 2 = theorem
counterexample found; 1 = no counterexample but re-certification incomplete;
0 = no counterexample AND all tail certificates independently rebuilt AND
every branch cell - including the gap cells below - independently
re-certified.

What is NOT pending: the static logic audit, including the coverage gap in
Finding 1. That finding follows from reading `lab/blade_proof.py` line 175
together with the executed cell list in `results/blade_proof.json`; no code
needs to run to verify it.

## Finding 1 (MAIN, deterministic): COVERAGE GAP in the executed proof

The branch loop escalates the tail start when the 2-variable certificate
fails, but only backfills ONE fixed-m cell per escalation:

    # lab/blade_proof.py:175
    for m0 in range(1 if m_start == 4 else m_start - 1, m_start):

Trace for any branch whose first tail attempt fails (e.g. k=7):
iteration 1: m_start=4, fixed cells m=1,2,3, tail m>=4 FAILS -> m_start=10;
iteration 2: fixed cells = range(9,10) = {9} ONLY, tail m>=10 succeeds.
Result: **m = 4,5,6,7,8 are covered by NO certificate at all** - not by any
fixed-m cell and not by any successful tail. `results/blade_proof.json`
confirms: branch k7 logs exactly cells k7_m1, k7_m2, k7_m3, k7_m9, then tail
m_start=10.

Uncovered (k, m) cells implied by the artifact (m_start per branch):

| branches   | m_start | uncovered m per branch                          | count |
|------------|---------|--------------------------------------------------|-------|
| k=4..6     | 4       | none                                             | 0     |
| k=7..13    | 10      | 4-8                                              | 5     |
| k=14..19   | 16      | 4-8, 10-14                                       | 10    |
| k=20..24   | 22      | + 16-20                                          | 15    |
| k=25..30   | 28      | + 22-26                                          | 20    |
| k=31..36   | 34      | + 28-32                                          | 25    |
| k=37..42   | 40      | + 34-38                                          | 30    |
| k=43..45   | 46      | + 40-44                                          | 40    |

Total: **740 branch cells (k, m) with no certificate**, spanning
lambda in [2.7, 26.1) and n = m+3 in {7..47}. Note that n=7 (m=4) - the
level with the historically tightest window-vs-shore margin (worst margin
2.1729 in `results/t2n6_window_vs_shore.json`) - is one of the skipped
values on every branch k>=7.

Consequences:
- "exit 0 / ALL CERTIFIED / all_certified: true" is FALSE as a statement of
  complete coverage. The proof as executed is INCOMPLETE.
- This does NOT refute the theorem. The skipped cells are very likely fine
  (for m<=8 the window tip sits near lambda ~ 0.29*m + O(1) < 2.7, so most
  gap cells should certify via "no window"), but likely is not proven.
- Minimal fix: replace the backfill range with
  `range(1 if m_start == 4 else m_start - 6, m_start)` so each escalation
  certifies ALL six skipped m values, then re-run. Alternatively, an exit-0
  run of `lab/attack_blade_theorem.py` independently re-certifies every
  m < m_start cell (including the 740 gap cells) plus rebuilt tails.

## Static logic audit of the architecture (items (a)-(e))

Verdict up front: apart from Finding 1, I found NO soundness break in the
proof architecture. Details, so they can be audited line by line:

(a) Coverage junctions - SOUND (given the cells actually certify).
  - lambda axis: k=3 covers (0, 2/3] via lam=(2/3)/(1+w), w>=0 (w=0 gives
    2/3 included, lam=0 correctly excluded). Branch k>=4 covers
    [mu_lo, mu_hi) with mu_lo=(3/5)(k-5/2) (k=4 overridden to 2/3),
    mu_hi=(3/5)(k-3/2); t=w/(1+w) reaches t=0 but not t=1, and the next
    branch's t=0 closes each right endpoint. Chain: (0,2/3] u [2/3,1.5) u
    ... u [25.5,26.1), tail [26,inf). Contiguous; branch/tail overlap on
    [26, 26.1). No gap.
  - m axis in the tail: T0 covers m=1..78; L2/L3 cover m>=79 (certificates
    in m=v+79 with v>=0 real, a superset of the integers). No gap.
  - lambda axis in the tail: L3's z in [0,1) covers 26 <= lam < (m+6)/3;
    the exact boundary lam=(m+6)/3 (s = (4/3)(m+3)) and everything beyond
    is covered by L2, because a nonempty window needs disc>0, i.e.
    s^2 < S^2_max <= (16/9)(m+3)^2 STRICTLY. Closed.
  - Defect (cosmetic): the docstring and the JSON "branches" field describe
    the intervals as [(2/3)(k-3),(2/3)(k-2)], but the code uses the
    3/5-spaced grid above. The artifact mis-describes its own coverage;
    fix the metadata.

(b) Strictness - SURVIVES under the per-point reading; wording caveat.
  Positive-coefficient certificates prove only >= 0. But with al>0 the
  bracket is an upward parabola in u; if Bhat(u_T)>=0 and u_T<=vertex then
  either disc<=0 (window empty - note disc=0 gives an EMPTY open window,
  not a degenerate violation) or u_T <= u_-, and every window point is
  STRICTLY > u_- >= u_T >= Tmin+4m+1. So "every D in the window satisfies
  D > min_k T_k" holds with non-strict certificates. Caveat: if the paper's
  "lies strictly above" is meant as inf(window) > envelope (a strict gap),
  the >= certificates do NOT deliver it at possible touching points; the
  paper should define the statement per-point, or add a strict-gap margin
  lemma. The attack script measures the actual minimal margin.

(c) Vertex-condition logic - SOUND, including degenerate cases.
  u_T <= vertex is encoded as G s^2 >= (T_k+4m)*2*al, which is exactly
  u_T <= 1 + G s^2/(2 al) = vertex. Case split: disc<=0 -> no window,
  vacuous; disc>0 and u_T=vertex is impossible together with Bhat(u_T)>=0
  (at the vertex Bhat = -disc/(4 al) < 0); disc>0, u_T<vertex,
  Bhat(u_T)>=0 -> u_T <= u_-. Note the proof only needs min_k T_k <= T_k
  (chosen branch k), which is trivially true - the argmin identity is
  never used. Correct.

(d) L2 squaring step - SOUND, and it silently carries the needed sign facts.
  disc = -beta s^4 + 4 al G s^2 + 4 al^2 with beta = 4 al - G^2. The chain
  S^2_max <= (16/9)(m+3)^2 <=> RHS := (16/9)(m+3)^2 beta - 2 al G >= 4 al^(3/2)
  <=> RHS >= 0 AND RHS^2 >= 16 al^3 is valid BOTH directions because both
  sides are nonnegative once RHS>=0. Two facts the code never states but
  needs: (i) beta>0 (parabola direction / division by beta) - it actually
  FOLLOWS from the RHS>=0 certificate since al,G>0; (ii) al>0 - clear from
  the factored form. I additionally derived by hand the factorization
    beta = 8(m+3)(m^3+3m^2+11m+15) / (45(2m+1)(2m+3)^2) > 0 for all m>=0,
  (identity re-checked symbolically in the attack script), so beta>0 is
  global, not just m>=79. The near-cancellation 4*al ~ G^2 at leading order
  (both ~ m^2/9) is exactly why the small-lambda/large-m zone is delicate -
  hence the dedicated exact scans in the attack script.

(e) L1 floor parametrization - SOUND.
  lam=(K+theta)/sqrt3, K=floor(sqrt3*lam), theta in [0,1). lam>=26 =>
  sqrt3*26 ~ 45.033 => K>=45; the certificate proves the inequality for all
  REAL K>=45 and theta in [0,1) (w/(1+w) covers [0,1) exactly - matching,
  no [0,1] mismatch), a superset of what is needed; k=K+2>=47 is an
  admissible envelope index. Hand-check of the constant: minimizing
  T_k ~ 12 lam + 6 lam^2/k + 2k over k gives k* ~ sqrt3 lam and
  min_k T_k -> (12+4 sqrt3) lam exactly. So L1's constant is the TIGHT
  asymptote with zero slack at infinity - the certificate is genuinely
  load-bearing, which is why the attack script rebuilds it from scratch
  over Q(sqrt3) rather than trusting the lab's expansion.

## Secondary defects / risks (none observed to break soundness)

1. (Finding 1 is the only coverage defect.)
2. Metadata mismatch: docstring + JSON claim (2/3)-spaced branch intervals;
   code uses 3/5-spaced ones (see (a)). Must be fixed before any write-up.
3. `cell_fixed_m` runs `sp.nsimplify` on CRootOf disc roots to build split
   points. nsimplify can return a nearby WRONG exact number. Soundness
   survives only because the subintervals are re-verified independently and
   still tile [0,1]; but the log's claim that cells are split "at disc
   roots" is not guaranteed. Replace with exact rational separators.
4. `sp.fraction(sp.together(...))[0]` is used throughout without verifying
   the denominator sign. All denominators are built from manifestly
   positive factors (45, 2m+1, 2m+3, k(k-2), (1+w)^j), so this is almost
   surely fine, but it is an unproven step of every certificate. The attack
   script proves denominator positivity explicitly at each use.
5. Certificates prove >= not >; see (b) for why the theorem survives and
   what wording the paper needs.
6. T0's accept path "some coefficient negative, but no real roots >= 0 and
   positive sample" is sound (sign constant on a root-free ray); no issue.

## The independent machine attack (PENDING execution)

`lab/attack_blade_theorem.py` - fully independent rebuild: own Fraction
bracket/envelope, own exact per-point violation test (an IFF, documented in
the docstring, so a clean pass is meaningful), own certificate machinery.
Parts:
- Coverage-gap parser: recomputes Finding 1 from the artifact.
- Certificate rebuilds: T0 (m=1..78), L1 and L3 over Q(sqrt3), L2 (both
  inequalities + exact numeric containment spot-checks), the k=3 branch,
  the beta identity, all with explicit denominator-sign proofs.
- Exact rational scans: junction zones lam ~ 2/3 and lam ~ 26..26.1
  (m up to 1000), closest-approach zone lam in [0.02, 0.1] (m up to 3000).
- Float reconnaissance + exact recheck of every suspect: window tips
  (disc ~ 0, m<=200), large-m strip m up to 1e5 including the hinted
  s/m ~ 1+1/sqrt3 direction (which my asymptotics place OUTSIDE the window
  region - the script asserts that), deep water lam in [26, 2000] with
  n up to 6*lam.
- Full re-certification of every branch cell m=1..m_start-1 for k=4..45
  (this INCLUDES all 740 gap cells) by an exact univariate decision
  procedure (root isolation + rational separators; the case analysis at
  breakpoints is written out in `decide_cell`'s docstring), plus rebuilt
  2-var tail certificates with the t=1 endpoint closed exactly.
- Negative control: the violation detector is pointed at the interior of a
  real window (the vertex, where disc>0 forces Bhat<0) and must fire - a
  battery that cannot fail is not a test.
- Reports the global minimum margin D_- - Tmin found (worst 25 points,
  high-precision evalf for the smallest).

## Verdicts (per claim-gates)

(1) BLADE THEOREM proof as executed by `lab/blade_proof.py` (git a931784
    era artifact): **GAP FOUND**. Exact gap: line 175 escalation bug leaves
    740 (k, m) branch cells - k=7..45, m in {4..8, 10..14, ..., m_start-2}
    per the table above - with no certificate, while the run still printed
    "ALL CERTIFIED" and wrote all_certified: true. The claim "for every
    level n>=4..." is therefore NOT proven by this artifact. Under
    claim-gates the theorem must not be promoted on this run.

(2) Proof ARCHITECTURE (branch decomposition + T0/L1/L2/L3 tail):
    NO OTHER DEFECT FOUND in the static audit; items (a)-(e) all check out
    analytically, with the wording caveat in (b) and the metadata fix in
    (a). I am explicit about uncertainty: the certificate computations
    themselves (coefficient signs of large expansions) were NOT re-executed
    in this session; their independent rebuild is coded and pending.

(3) THEOREM itself: NOT REFUTED. No counterexample is known to me; the
    asymptotics I derived by hand (envelope slope 12+4sqrt3, window-tip
    ratio s/(m+3) -> sqrt(5/3) ~ 1.291 < 4/3) are consistent with the
    theorem holding with margin. Status: INCONCLUSIVE pending (i) the fix
    of Finding 1 + re-run of blade_proof.py, or (ii) an exit-0 run of
    lab/attack_blade_theorem.py, either of which closes the gap cells.

## Plain-language brief (for the founder)

The lab's auto-prover says "ALL CERTIFIED", but its bookkeeping has a hole:
whenever its first attempt to certify "all levels above n=7 at once" failed,
it bumped the threshold up by six and forgot to go back and check five of
the levels it skipped - including n=7, historically the closest call in
this family. About 740 such (branch, level) squares were never checked, yet
the run still stamped itself fully certified. Everything else in the proof
design survived a hostile audit: the interval junctions meet, the clever
square-root and floor tricks in the far-field certificates are used
legitimately, and the "greater-or-equal" certificates do imply the strict
statement in the sensible reading. I wrote an independent checker that
re-proves every skipped square and re-derives all far-field certificates
from scratch, and also hunts for counterexamples in the delicate corners.
It has not been run yet in this session (I had no execution tool); until
it, or a fixed re-run of the original prover, exits clean, the theorem is
"very likely true, not yet proven".

## Questions for an external expert

1. The window-existence boundary satisfies s/(m+3) -> sqrt(5/3) as
   m -> inf (from beta's leading-order cancellation 4*al ~ G^2 ~ m^2/9).
   Is there a structural reason the bootstrap produces exactly sqrt(5/3),
   and does it suggest a cleaner closed-form containment than the (4/3)
   bound used in L2?
2. L1 uses the exact asymptote (12+4 sqrt3) lam with zero slack at
   infinity. Is there a slack-bearing envelope bound (e.g.
   (12+4 sqrt3) lam - c for some c>0) that would make the tail
   certificates robust to future perturbations of the family?
3. For the strictness question in (b): is the intended published statement
   per-point ("every negative D exceeds the envelope") or a uniform gap
   (inf window - envelope >= delta(lam, n) > 0)? The current certificates
   support only the former without extra work.

## How to reproduce every claim in this review

- Finding 1: read `lab/blade_proof.py:172-195` and grep
  `results/blade_proof.json` for `"cell": "k7_m` and `"m_start"`.
- Everything else: run the attack script (command at the top); it writes
  `results/attack_blade.json` with per-part logs, the uncovered-cell map,
  minimum margins, and the exit-coded verdict.
