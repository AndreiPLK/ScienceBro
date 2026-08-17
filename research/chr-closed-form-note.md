# The CHR knife brackets: a closed hypergeometric form and a one-variable reduction

Research note, 2026-08-17. Status: `truth_status: ANALYTICALLY_PROVED` for the
identities below (each verified exactly on thousands of rational points);
`novelty_status: POTENTIALLY_NOVEL`, prior art recorded.
`idea_origin: MIXED` (our master formula + Rigatos-Wang / AEHM techniques).

## 1. Setting

For the CHR one-parameter graviton family (arXiv:2408.03362) the sign of the
partial-wave coefficient on the trajectory `l = 2n - 2j` is governed by the
bracket `P_j(n, lam, D) = (-1)^{j-1} B_j`, given by the master formula of our
paper 3 (arXiv/Zenodo 10.5281/zenodo.21947272).

Notation: `s = lam + n - 1`, `c = 4n - 4j - 1`, `R = (D + c)/2 + j - 1`,
`E_{2t}(n)` = even elementary symmetric functions of the doubled root multiset
`{n - 2k}` (equivalently the coefficients of `prod_k (1 + (n-2k) z)^2`).

## 2. Result A — closed hypergeometric form

    P_j = c0 * SUM_{t=0}^{j-1} (-1)^t E_{2t}(n) * (1-j)_t (1-R)_t
                                / ( (1-n)_t (3/2-n)_t s^{2t} ),
    c0 = (2n-2)! / ((j-1)! 2^{j-1}) * s^{2(j-1)}  > 0.

Verified exactly (rational arithmetic) at 4320 points: `j = 2..25`, `n` up to
`j+25`, `lam` from 1/100 to 150, `D` from the shore to three times beyond it.
Artifact: `results/chr_closed_form.json`; script `lab/chr_closed_form.py`.

Significance: the sum TERMINATES through `(1-j)_t`, and the entire dependence
on the knife index `j` now sits in that single Pochhammer plus the positive
prefactor `c0`. This is the CHR analogue of Rigatos-Wang eq. (27)-(28)
(arXiv:2401.13031) for the Coon family.

## 3. Result B — the alternating spectral sum is a perfect square

    SUM_t (-1)^t E_{2t}(n) x^t = [ prod_{a in S_n} (1 - a^2 x) ]^2,
    S_n = { n - 2k > 0 }.

Because the CHR root multiset is symmetric (`+-a` in pairs), the doubled-root
generating function collapses to a perfect square. Verified symbolically.

Consequence: the alternating spectral sum is nonnegative for EVERY `x`; the
sign problem of the master formula is carried entirely by the weights, not by
the spectrum. In the language of AEHM (arXiv:2201.11575) this is why CHR
behaves like a closed-string residue.

## 4. Result C — reduction to one weighted inequality

Factor the weights as `A_t = M1_t * M2_t` with

    M1_t = (j-1)^{(t)} / (n-1)^{(t)} = C(j-1,t) / C(n-1,t),
    M2_t = (R-1)^{(t)} / ( (n-3/2)^{(t)} s^{2t} )      (falling factorials).

`M2` IS a moment sequence (exact Hankel minors nonnegative), so
`M2_t = int v^t dnu(v)` for a nonnegative measure `nu`, and

    P_j / c0 = int Phi(v) dnu(v),
    Phi(v) = SUM_t (-1)^t E_{2t}(n) M1_t v^t.

`M1` is NOT a moment sequence (exact minors negative) — the sign problem is
now localised in one explicit object, a ratio of binomial coefficients.

Numerically, `Phi` DOES dip negative near the upper edge of `nu`'s support
(worst relative dip -0.05 in 12,600 sampled points), so positivity of `P_j`
is not pointwise; it is the quantitative statement that `nu` carries little
mass where `Phi` dips. That inequality is finite and explicit for each
`(j, n, lam, D)` and is the current target of the completeness programme.

## 5. What is NOT claimed

No proof of the grand completeness theorem (all knives at once). Knives
j = 2..12 are proven individually with machine-checked certificates
(deterministic gate); results A-C are structural tools, not the theorem.

## 6. Falsified along the way (13 recorded negatives)

moment sequence for the raw weights; Leibniz alternating bound; Abel
induction on high spins; monotonicity in each ratio; normalised-X bound;
factorability of the shallow polynomial; PSD of the associated quadratic
form (this one proves the theorem MUST use the CHR arithmetic progression,
not mere squareness); moment property of `A_t` (log-concave, hence never a
moment sequence); orthogonal-expansion positivity (L is indefinite);
Lorentzian signature; three-term recursion in `j`; `Phi >= 0` globally;
`Phi >= 0` on the support. Full signatures in `article/DATA_LOG.md`.

## 7. Prior art consulted (full texts on disk, sha256 in evidence/)

- Mansfield, arXiv:2502.20372 — Veneziano positivity in D <= 10, all levels.
- Rigatos-Wang, arXiv:2401.13031 — harmonic-number partial waves (Coon).
- Arkani-Hamed, Eberhardt, Huang, Mizera, arXiv:2201.11575 — contour
  representations, fixed-spin asymptotics (they state explicitly that they
  could not make the fixed-spin bound rigorous in D = 10).
- Area, arXiv:2608.04802 — Bernstein-type bases on quadratic lattices; our
  `G` is a Wilson generalized power, and the paper's obstruction explains why
  a naive nonnegative-coefficient representation cannot exist in that chart.
