# The knife is a quadratic form in the half-spectrum, and that is the bridge

*2026-08-30, working Step 1 of `THE_THEOREM.md`. The identity is exact and verified; the
sufficient condition built on it is refuted. Both are recorded.*

## The identity

    knife = SUM_t (-1)^t c_t e_t(b),    c_t = (r)_t (H-r)_t / [(n-1)_t (n-3/2)_t]

with falling factorials, so `c_t = 0` for `t > r` automatically.

Because the `b`-multiset is **doubled** (`b_k = b_{n-k}`, proved earlier the same day),

    SUM_t (-1)^t e_t(b) x^t = PROD_k (1 - x b_k) = g(x)^2,

a perfect square, with `g(x) = PROD_{half} (1 - x b_k)`. Matching coefficients,
`(-1)^t e_t = SUM_{i+j=t} g_i g_j`, and therefore

    knife = SUM_{i,j} c_{i+j} g_i g_j  =  g^T H g,     H_{ij} = c_{i+j}.

**The knife is a quadratic form with a Hankel matrix.** Verified exactly at 108 parameter
settings (`n = 9,13,21,31`; `j = 3,5,8`; three `D`; three `lambda`), zero mismatches.

Better still, `g` is the coefficient vector of a real-rooted polynomial with positive
roots, so `g_i = (-1)^i h_i` with `h_i = e_i(half spectrum) > 0`. Substituting,

    knife = h^T D h,     D_{ij} = (-1)^{i+j} c_{i+j},     h > 0 entrywise,

verified at every one of the 36 settings tested in that form.

## The sufficient condition, and its refutation

If `D` were **copositive** — nonnegative on the whole nonnegative orthant — the keystone
would follow at once, for every depth and every spectrum. Copositivity is much weaker than
positive semidefiniteness, which we already knew to be false (`DR-14`: the Hankel matrix of
`c_t` has negative minors at order 2).

`D` is not copositive either. Random `h > 0` produces negative values of `h^T D h` in every
one of the 36 settings, from `-5e-3` at `n = 21, j = 3` to `-2.2e3` at `n = 9, j = 8`.

## What that leaves, and why it is the useful part

The identity is exact, so the keystone is exactly the statement

> `h^T D h > 0` for the **specific** `h`, namely the elementary symmetric functions of the
> half spectrum.

Since `D` is indefinite and not copositive, no argument about `D` alone can work: **the
proof must use the structure of `h`.**

And that structure is precisely what this programme has spent its effort on. `h` is the
elementary symmetric sequence of the half spectrum, and about it we already know, exactly:

* it is a Pólya frequency sequence (real-rooted generating polynomial);
* its normalisation is ratio log-concave on the whole index range — measured at `m = 5..40`
  with zero failures, which is stronger than the doubled spectrum manages;
* it satisfies conjecture (B), proved for every `t <= 200`;
* its Jensen polynomials are hyperbolic through degree 8.

**So the keystone and (B) are not neighbours, they are the same object seen twice.** (B) is
a statement about `h`; the keystone is a quadratic form in `h`. That is the bridge the
programme has been looking for, and it is now an identity rather than an analogy.

## Honest status

* **Proved:** `knife = g^T H g = h^T D h`, exactly.
* **Refuted:** copositivity of `D`, hence the one-line route through it.
* **Open:** everything else. This does not prove the keystone; it says where the proof has
  to come from, and it connects the two halves of the programme by an identity.

Three routes died on the way to this, each in minutes: that the `tau_i` decrease, that
`phi` factors into absolutely monotone pieces, and that `c_t` is a positive moment sequence
(`DR-14`). The first two are in `LEG_A_REDUCED_TO_ONE_LEMMA.md`.
