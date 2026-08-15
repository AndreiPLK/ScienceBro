# Adversarial review: the Master Positivity Formula (paper 3)

Date: 2026-08-15. Reviewer: domain-critic (adversarial, independent).
Objects: `research/master-formula.md`, `paper3/main.tex` (claimed counts
cross-checked against `results/master_completeness_scan.json`, git 9cba4a4).
Attack script (written from scratch, no imports from `lab/tj_bracket.py`,
`lab/t2n6_bracket.py`, `lab/grav_full_body.py`): `lab/attack_master.py`.

## Execution status — read this first

This critic session had NO shell/execution tool available. `lab/attack_master.py`
is complete and ready but was NOT executed by the critic. All "machine battery"
statements below are therefore PENDING until someone runs:

    C:\Users\user\ScienceBro\.venv\Scripts\python.exe projects/qg-bootstrap/lab/attack_master.py

Exit 0 <=> no falsification (contract in the script docstring; artifact
`results/attack_master.json`). What is NOT pending: the independent analytic
re-derivation and the hand-computed exact checks below, which I did from
scratch and show in full so they can be audited line by line.

## 1. The integral identity (task 1) — VERDICT: CORRECT

Claim: I(l+2u,l)/I(l,l) = (l+2u)! / (l! u! 4^u (alpha+l+1)_u), with
I(k,l) = int_{-1}^1 x^k C_l^(alpha)(x) (1-x^2)^(alpha-1/2) dx.

Independent derivation (not reusing the lab's beta-function route): the
classical monomial-to-ultraspherical expansion (DLMF 18.18.17)

    x^m = (m!/2^m) * sum_k [ (alpha+m-2k) / (k! (alpha)_{m-k+1}) ] C_{m-2k}^(alpha)(x)

gives I(l+2u,l) = coeff(m=l+2u, k=u) * ||C_l||^2 and I(l,l) = coeff(m=l, k=0) * ||C_l||^2, so

    I(l+2u,l)/I(l,l) = [(l+2u)!/l!] * 2^{-2u} * (alpha)_{l+1} / (u! (alpha)_{l+u+1})
                     = (l+2u)! / (l! u! 4^u (alpha+l+1)_u).

I verified the expansion constant at m=1 (x = C_1/(2 alpha)) and m=2
(x^2 = [C_2 + alpha]/(2 alpha (alpha+1)) reassembled exactly) by hand — both
exact. The 4^u comes from the 2^{-m} in the expansion; the whole D-dependence
sits in (alpha+l+1)_u, as claimed. Part A of `attack_master.py` additionally
proves the identity mechanically for every l<=10, u<=6: exact equality at 45
distinct rational alpha (including 1/100, 5/2, 100, 999/7) exceeds the degree
bound 2l+2u of the cross-multiplied difference, hence a genuine
rational-function identity per (l,u) once run.

## 2. The master formula (task 3: derivation attack) — VERDICT: CORRECT (analytic)

I re-derived the formula end-to-end without consulting the lab's extractor code.

(i) Kinematics/roots. On the level-n pole, t = -(mu/2)(1-x) with
mu = (n+lam-1)/lam. Substituting into ((1+lam)/2 + lam t + k), k = 0..n-2,
gives exactly [s x + (2(k+1)-n)]/2 with s = lam+n-1. So the residue is a
positive constant times Q(x)^2, Q = prod_{k=1}^{n-1} (s x + 2k - n); roots
x_k = (n-2k)/s, symmetric. Coefficient of x^{2n-2-2t} in prod(x-x_k)^2 is
(-1)^t E_{2t}(n) s^{-2t} (pairing r with -r makes e_{2t} = (-1)^t |e_{2t}|).
Ingredient (i) of the paper: confirmed.

(ii) Contribution window. I(k,l)=0 for k<l (orthogonality to lower degrees),
so with l = 2n-2j only t = 0..j-1 contribute; u = j-1-t. Confirmed.

(iii) Clearing. Multiply the sum by the strictly positive factor
s^{2(j-1)} * l! * 4^{j-1} * (alpha+l+1)_{j-1} (positive for lam>0, D>3).
Using (alpha+l+1)_{j-1}/(alpha+l+1)_i = (alpha+l+1+i)_{j-1-i} and

    alpha + l + 1 + i = (D + 4n - 4j - 1 + 2i)/2,

each half-integer Pochhammer factor yields one ladder factor
(D + 4n - 4j - 1 + 2r), r = i..j-2, and one factor of 2; the powers of two
collect into a global positive 2^{j-1} times the claimed per-term 2^{-i}.
The signs give (-1)^t = (-1)^{j-1} (-1)^i. Result: EXACTLY the claimed
formula — factorial weights (2n-2j+2i)!/(i! 2^i), s^{2i}, ladder
prod_{r=i}^{j-2}(D+4n-4j-1+2r), prefactor (-1)^{j-1}. I found NO error.
(For honesty: my first pass had an index slip u<->t giving a wrong ladder
base; redoing it with u=i reproduced the claim exactly. This is why the
machine battery matters.)

Hand-verified special cases (exact, auditable):
- n=3, j=2: master gives sign a_{3,2} = sign[3s^2 - 3 - D] i.e.
  a>=0 iff D <= 3lam^2+12lam+9, which is exactly the published T_3.
  Direct integral at lam=1, D=4 (alpha=1/2, Legendre): value 48/7 > 0. Both
  encoded as known-answer controls in the script.
- n=4, j=3: master gives 32(D+3)(D+5) - 96 s^2 (D+5) + 90 s^4, which equals
  90*[alpha_1 u(u-2) - G_1 u s^2 + s^4] with u=D+5, G_1=16/15, alpha_1=16/45 —
  exactly the paper's j=3 rung at m=1. Independent match of the "windows" law.

Sign-convention flip check (task 3): analytically impossible on the claimed
domain — the cleared factor is s^{2(j-1)} l! 4^{j-1} (alpha+l+1)_{j-1} times
the positive Gegenbauer/weight norms, and every piece is strictly positive for
lam>0, D>3. The D>3 restriction is NECESSARY: for D<=3, (alpha+l+1)_{j-1} and
the norms can vanish/flip, and the claim correctly excludes that region. The
empirical flip check across regimes (odd D, non-integer D, lam=1/100 and 100,
n=14,15, l=2 edge, j=2 and j=n-1 edges) is in parts C of the script.

Boundary case j=n (l=0), task 3: the paper claims only 2<=j<=n-1. My
derivation contains nothing that breaks at j=n — all n monomials contribute
(t<=n-1), the ladder factors D-1+2r stay positive, and for even n the top term
simply drops (E_{2(n-1)}=0 since 0 is a root). Prediction: the formula EXTENDS
to j=n. Part E of the script tests this (informational, not a falsification
either way). If confirmed, the paper's Discussion sentence that l=0 "lives
outside the trajectory scaling" is too pessimistic and the theorem can be
strengthened for free; if refuted, there is a subtlety at l=0 worth a remark.

## 3. Defects found (adversarial findings)

1. SIGN TYPO in paper3/main.tex, Sec. 2 (generating identity): it prints
   prod_k (1+(n-2k)z)^2 = sum_t (-1)^t E-hat_{2t} (-z^2)^t. As printed the
   right side equals sum_t E-hat_{2t} z^{2t} (all-positive coefficients),
   which is FALSE: for n=3 the left side is (1-z^2)^2 = 1 - 2z^2 + z^4, so
   coeff(z^2) = -2, not +2. Correct display: sum_t E-hat_{2t} (-z^2)^t
   (drop the extra (-1)^t). Harmless to the theorem (E-hat is defined as
   absolute values, and master-formula.md words it correctly), but the printed
   equation is internally inconsistent and must be fixed before submission.
2. FLOAT-DERIVED REGION BOUNDARY in the completeness sweep
   (lab/master_completeness_scan.py): Dtop = int(min_T(float(lam))) uses
   floating point to decide region membership, then truncates. If min_n T_n
   is exactly (or within float error of) an even integer at some rational
   lam, a marginal boundary point can be silently included or dropped. The
   1,538,164 verdicts are exact; the REGION is not exactly determined. Fix:
   exact-rational T_n and an exact floor.
3. COVERAGE NARROWER THAN THE ABSTRACT'S WORDING. The sweep covers even D
   only, j>=3 with l>=2 (l=0 excluded), n<=40, lam<=50 on a 68-point grid.
   The abstract's "all trajectory constraints at once" and the Discussion's
   "every knife the family owns" overstate this: odd D is entirely untested
   in the battery (the theorem claims all D>3), and l=0/fixed-spin waves are
   excluded (admitted in the Discussion, not in the abstract). Recommend
   "every near-leading trajectory constraint (l=2n-2j, 2<=j<=n-1) at every
   even D in the region", and an odd-D pass — it is cheap.
4. The completeness sweep evaluates the MASTER FORMULA, not the underlying
   partial waves. Legitimate only because the formula is independently
   verified; the paper should state this dependency explicitly in Sec. 4.
5. Paper counts vs artifacts: 1,538,164 checks / 0 alarms match
   results/master_completeness_scan.json (git 9cba4a4). The n=7 window
   statement matches results/t2n6_window_vs_shore.json (worst margin 2.1729).

## 4. Verdicts (task 4, per claim-gates)

(a) Integral identity: CORRECT. Independent analytic re-derivation from the
    classical DLMF 18.18.17 expansion, base cases verified exactly by hand;
    plus a finite mechanical proof (interpolation over exact rationals) coded
    in attack_master.py part A, pending execution.

(b) Master formula as stated (2<=j<=n-1, D>3, lam>0): CORRECT on analytic
    grounds — complete independent re-derivation reproduces the exact
    statement, and two rungs were re-verified by hand against T_3 and the
    j=3 quadratic. No silent sign flip is possible on the claimed domain
    (strictly positive cleared factor). Caveat, stated plainly: the critic's
    from-scratch numerical battery (odd/non-integer D, extreme lambda, deep
    n, edges j=2 and j=n-1, exact-zero proportionality at the j=2 root) is
    written but UNEXECUTED in this session. Under the lab's proof-gate
    discipline, machine confirmation (exit 0 of attack_master.py) should be
    recorded before claim promotion; if the lab requires that gate strictly,
    read this verdict as CORRECT (analytic) / pending (machine).

(c) Completeness-battery interpretation in the paper: INCONCLUSIVE as
    currently worded. The computation itself is very likely sound and the
    counts match the artifact, but (i) the region boundary is float-derived
    (defect 2), (ii) coverage is even-D, l>=2, finite ranges while the
    abstract implies exhaustiveness (defect 3), (iii) the dependency on the
    master formula is implicit (defect 4). With the wording fixes and an
    exact-rational boundary (plus optionally an odd-D pass) this becomes
    CORRECT-with-stated-scope. Nothing found suggests the conclusion (no
    j>=3 knife cuts the conjectured region in the scanned ranges) is wrong.

## 5. Questions for an external expert

1. Is there a clean closed-form argument that every j>=3 ladder polynomial is
   positive whenever D < min_n T_n (turning the finite sweep into a theorem
   for the near-leading sector)? The ladder structure looks amenable to a
   Descartes/interlacing argument in D.
2. Does the j=n (l=0) extension hold, and if so does the l=0 wave ever bind
   before the shore anywhere in (lam, D)? The paper currently excludes it.
3. For non-integer D (continued alpha), is positivity even the physically
   meaningful requirement, or should the claim be restricted to integer D>3?
   The formula is stated for real D>3; the paper should say which is meant.
