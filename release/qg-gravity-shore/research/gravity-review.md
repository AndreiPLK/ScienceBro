# Adversarial review: gravity card, slices 1-6 (corrected post-Pochhammer)

Reviewer: domain-critic agent, 2026-08-14.
Scope: the four claims of the gravity card against arXiv:2408.03362 (CHR,
PRD 111 086034), full-text extract read. Method: (i) independent hand
re-derivation in exact arithmetic (this file, checkable line by line);
(ii) an independent attack script, `projects/qg-bootstrap/lab/attack_gravity.py`.

**TRANSPARENCY: the attack script was WRITTEN but NOT EXECUTED in this review
session (the review agent had no code-execution tool). Every verdict below is
marked either HAND-PROVEN (derivation reproduced independently in this file,
exact algebra, no numerics needed) or PENDING-SCRIPT. Do not promote any claim
on the strength of PENDING-SCRIPT items until the script has been run.**
Run: `C:/Users/user/ScienceBro/.venv/Scripts/python.exe projects/qg-bootstrap/lab/attack_gravity.py`
(exit 0 = no falsification; artifact `results/attack_gravity.json`).

## Verdict table

| # | Claim | Verdict |
|---|-------|---------|
| 1 | a_{n,2n-4} >= 0 <=> D <= T_n(lam), T_n = 3(2n-3)/(n(n-2))(lam^2+(2n-2)lam+1)+2n | **CORRECT — independently re-derived by hand for general n** (see proof below); script razors PENDING as belt-and-braces |
| 2 | D_n(1) = 2(n^2+4n-9)/(n-2), min 23 at n=4 | **CORRECT — hand-proven** (algebraic identity with T_n(1); integer min at n=4 since continuous min is at n = 2+sqrt(3)) |
| 3 | Shore = min_n T_n; lam_min(23)=1; asymptote D -> (12+4sqrt3)lam, n* = sqrt(3)lam | **CORRECT as a statement about this trajectory family** — magic point hand-proven for ALL n (not just n<=400); asymptote hand-derived as a limit; convergence-rate caveat below |
| 4 | Complete model: alive <=> D <= min_n T_n ("no other knives") | **CONJECTURE — not established.** Falsifiable (protocol below), honestly labelled in the card as pending, but slice-3's D=4 headline needs demotion/annotation (see g) |

No counterexamples were found by hand. The reviewer independently re-derived
claims 1-3 from scratch and got identical formulas — this is the strongest
outcome an adversarial review can produce without execution.

## (a) Kinematic substitution — CORRECT (hand-proven)

Massless externals, s+t+u=0. On the level-n pole s = mu(n), with
x = cos(theta) = 1 + 2t/mu(n): t = -mu(n)(1-x)/2, u = -mu(n)(1+x)/2. Standard
and correct. Useful exact identity (basis of the attack script):
lam*(t - xi(k)) = [(n+lam-1)x + (2k-n)]/2, so up to the positive constant
2^{2-2n} * ((1+3lam)/2)_{n-1}^{-2},
R(n,t(x)) = P(x) = [prod_{k=1}^{n-1} ((n+lam-1)x + 2k-n)]^2.
The dropped prefactor is positive for all lam >= 0 (Pochhammer of (1+3lam)/2
>= 1/2 > 0) — sign analysis unaffected. Script A0 cross-checks this identity
against the paper's Eq. (7) at random exact points (PENDING).

## (b) rho(l,D) — CORRECT (hand-derived independently)

From the standard expansion x^m = (m!/2^m) sum_k (a+m-2k)/(k! (a)_{m+1-k})
C^a_{m-2k}, a = (D-3)/2 (verified by hand at m=2 and m=3 against explicit
Gegenbauer polynomials):
  rho(l,D) := [coeff of C_l in x^{l+2}] / [coeff of C_l in x^l]
            = (l+1)(l+2) / (4(a+l+1)) = (l+1)(l+2) / (2(D+2l-1)).
Exactly the card's formula. Note domain: a > 0 requires **D > 3**; at D = 3
the basis degenerates (C_1^0 = 0) and the sign statements are meaningless.

## (c) Odd trajectories vanish — CORRECT (hand-proven, exact identity)

xi(k) + xi(n-k) = -(2n+2lam-2)/(2lam) = -mu(n) exactly. So the residue root
set is invariant under t -> -mu(n) - t = u; equivalently, in x the roots are
x_k = (n-2k)/(n+lam-1), k = 1..n-1 — a set symmetric under x -> -x. Hence
Q(-x) = (-1)^{n-1} Q(x), P = Q^2 is even, and all odd-l partial waves vanish
identically (matching the paper's "a_{n,l} = 0 for l odd"). Script A2
re-checks symbolically (PENDING).

## (d) Squared-polynomial bookkeeping — CORRECT, with a sharp structural fact

The worry was cross terms in the x^{2n-4} coefficient of Q^2:
C = q_{n-2}^2 + 2 q_{n-1} q_{n-3}. By the parity of Q (item c),
**q_{n-2} = 0 identically**, so C = 2 q_{n-1} q_{n-3} is PURE cross term —
had the derivation squared only leading coefficients term-by-term, it would
have gotten C = 0 and no edge at all. The card's result is only right if the
cross term was included; it evidently was, because:
  e_2(roots) = -(1/2) sum x_k^2 = -n(n-1)(n-2)/(6(n+lam-1)^2)
  (using sum_{k=1}^{n-1} (n-2k)^2 = n(n-1)(n-2)/3, checked at n=3: 2, n=4: 8),
so A/(-C) = q_{n-1}/(-2 q_{n-3}) = 3(lam+n-1)^2/(n(n-1)(n-2)) with C < 0 for
ALL lam >= 0, n >= 3 (inequality direction never flips). The positivity
condition C + A*rho(2n-4,D) >= 0 with denominator D+4n-9 > 0 then gives
  D <= (n-1)(2n-3) A/(-C) - (4n-9) = 3(2n-3)(lam+n-1)^2/(n(n-2)) - (4n-9),
and using (lam+n-1)^2 = lam^2+(2n-2)lam+1 + n(n-2) plus 3(2n-3)-(4n-9) = 2n
this is ALGEBRAICALLY IDENTICAL to the card's T_n. Additionally hand-checked
end-to-end at n=3 (Q ∝ w^2x^2-1, threshold 3w^2-3 = T_3, w = lam+2) and n=4
(Q ∝ x(w^2x^2-4), threshold 15w^2/8-7 = T_4, w = lam+3). Because only
x^{2n-2} and x^{2n-4} can feed G_{2n-4} (parity kills x^{2n-3}), the
"top-3" method is EXACT for this trajectory, not an approximation.
Script A5 re-verifies symbolically for n = 3..8 (PENDING).

## (e) Asymptote — CORRECT as a limit; convergence caveat

Minimizing T_n over continuous n at large lam with n = nu*lam:
T ≈ lam(6/nu + 12 + 2nu), minimized at nu = sqrt(3), giving
D -> (12+4sqrt3) lam and n* = sqrt(3) lam. Hand-checked. Validity of the
continuous-n step: legitimate asymptotically since n* -> infinity and the
integer-rounding penalty is O(1/lam) in D/lam — which is exactly why the
card's own measured ratios OSCILLATE (18.96, 18.75, 18.76, 18.83 at D=60..400
around 18.928) instead of converging monotonically. The card's phrasing
("closes onto an exactly straight asymptotic edge") is acceptable but should
state the O(1/lam) discrete-n oscillation explicitly before publication.
Reviewer also re-derived by hand all five slice-5 surds (D = 10, 12, 16, 20,
26) and the n=3 -> n=4 handover between D=16 and 20 — all correct.

## (f) Domain caveats (must appear in any paper)

1. **D > 3** required: at D <= 3 the Gegenbauer basis/positivity statement
   degenerates. All "for all D" statements mean D > 3 (physically D >= 4).
2. **lam >= 0** is an assumption imported from CHR (spinning tachyons at
   lam < 0), not derived here. At lam = 0 the family degenerates
   (mu(n) -> infinity); T_n(0) values are lam -> 0+ limits.
3. **n = 2 is outside the T_n formula** (n(n-2) denominator). Hand-checked
   separately: Q ∝ x for n=2, so a_{2,2} > 0 and a_{2,0} ∝ 1/(D-1) > 0 —
   level 2 never bites; n=0,1 trivially safe. The formula's n >= 3 domain is
   therefore complete for this trajectory.
4. Dropped positive prefactors: c(n) > 0 for lam > 0 and
   ((1+3lam)/2)_{n-1} > 0 for lam >= 0 — verified; sign analysis safe.
5. Boundary is inclusive: at D = T_n exactly, a_{n,2n-4} = 0, which unitarity
   allows. "Dies at D > T_n", not "at D = T_n".

## (g) Claim 4 — falsifiable? honestly labelled?

Falsifiable: YES, cleanly. Kill protocol: exhibit ONE exact negative a_{n,l}
at any (lam, D) with D <= min_n T_n(lam), D > 3. The script's A4 hunts at six
such points chosen adversarially (near the D=9 onset; D<9 where the model
predicts total safety; the large-lam flank lam=10, D=180 where lower
trajectories are most plausibly dangerous; VS exactly at its cliff D=23; both
D=4 extremal corners lam=1/100 and lam=100 at ALL l — a post-bugfix re-check
of the slice-3 artifact). Plus two dead-controls that must show the predicted
knives ((3,2) at lam=1/20, D=10; (4,4) at lam=1, D=24). PENDING execution.

Labelling: the card mostly behaves — slice 6 says "independent review
pending", and completeness is listed under "Next". Two exceptions to fix:
1. **Slice 3's "combined headline"** ("string gravity is NOT forced in D=4")
   rests on (i) a lemma derived from the PRE-BUG brackets (admitted void) and
   (ii) an l <= 8, n <= 60 scan whose artifact may predate the evaluator fix.
   The statement is probably still true (CHR themselves state D=4 positivity
   for all lam >= 0, to n = 30), but the card's own evidence for it is
   currently a scan of unclear provenance plus a void lemma. Action: re-run
   post-fix (A4 covers the corners at all l), and cite CHR p.6 as the
   external anchor, or demote the headline.
2. **"TRUE shore = min over n"** (slice 6) reads as a full-model statement
   but is proven only for the a_{n,2n-4} trajectory. Rename to "shore of the
   near-leading trajectory" until claim 4 passes its scans.
Also honest and worth preserving: the card's own razor lesson — the slice-1
"razor" shared the evaluator with the bracket and was circular; the fresh
razors in this review are solved from the direct projection with symbolic D
(non-circular) at never-tested points (n=5, lam=7/2, D* = 271/4 — fractional
D, outside anything the even-D scanners could ever touch; n=6, lam=3,
D* = 57).

## What would still make claim 4 fail (reviewer's candidate knives)

- Next-next even trajectory a_{n,2n-6}: same method needs top-5 coefficients
  (with q_{n-2} = q_{n-4}... parity zeros, so C' = q_{n-3}^2 + 2q_{n-1}q_{n-5}
  plus the rho-cascade from BOTH x^{2n-2} and x^{2n-4}). Nobody has shown its
  threshold lies above min_n T_n everywhere. This is the most likely knife if
  one exists, especially at large lam and D where many levels are near-critical.
- Fixed low spin (l = 0, 2) at deep n: tails could in principle turn negative
  at very large n without any near-leading warning. CHR only verified n <= 30.
- Recommended next slice: derive the a_{n,2n-6} law with the same machinery
  and compare envelopes; that either proves a piece of claim 4 or breaks it.

## Known-answer tests the result already passes (independent anchors)

- T_n(1) reproduces the measured VS D-cliff (D=24 first negative via (4,4),
  D=22 clean) and the 2210.14920 D_crit sequence — external data.
- T_3(0) = 9 reproduces CHR's stated "when D >= 9" onset (2408.03362, p.6,
  Positivity paragraph) — external, textual, non-circular anchor.
- lam -> 0 / lam -> infinity corners agree with CHR Eqs. (25)-(26) physics
  (scalar-exchange and stu-pole extremal amplitudes).

## Questions for external experts

1. Does anyone know CHR's Fig. 1 boundary NUMERICALLY (not just the D >= 9
   onset)? A quantitative overlay of lam_min(D) = root of min_n T_n = D
   against their n = 30 finite-depth curve is the decisive external check.
2. Is there a structural argument (interlacing/total-positivity of the
   squared residues) that the near-leading even trajectory is always the
   FIRST to fail, which would promote claim 4 from conjecture to theorem?
3. Shao-Vichi 2607.27300 (hidden-zeros analytic boundaries) — full text must
   be read before any novelty claim: does their method, applied to the CHR
   lambda-family, already yield T_n or its envelope?
4. Is non-integer D in these positivity statements physically meaningful for
   the intended swampland audience, or should published statements be
   restricted to integer D with continuous-D as a technical tool?
5. For identical external bosons, are the marginal cases a_{n,l} = 0 on the
   boundary acceptable as "alive" (our inclusive convention), or does any
   stronger unitarity requirement (strict positivity of some waves) apply?

## Reviewer's certification limits

I am an AI reviewer, not an accredited physicist. The hand derivations above
are complete and exact, and I re-derived rather than trusted the card's
algebra; nevertheless the standard ScienceBro gates apply: this review does
NOT promote any claim. Required before promotion: (1) run attack_gravity.py
and archive the JSON artifact; (2) re-run/replace the slice-3 D=4 artifact
post-bugfix; (3) claim 4 stays "speculative/conjectured" until the full-(n,l)
scans pass and question 2 or an equivalent argument is settled.
