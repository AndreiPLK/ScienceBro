# The depth kernel is totally positive on the physical domain: a proof

2026-08-28. Conjectured from 86 exact factorizations the same day
(results/kernel_minor_law.json), then proved by a two-line change of
variables. Machine-verified including the constant on all 86 cases
(lab/kernel_minor_identity.py).

## Statement

Let `H` be an indeterminate and

    B_{r,t} = C(r,t) * (H-r)_t * t!        ( (a)_t = a(a-1)...(a-t+1) )

be the depth kernel exposed by the binomial reorganization of the exact
knife sum (results/moment_kernel_probe.json): the knife of order `j = r+1`
is `K_r = sum_t (-1)^t B'_{r,t} ...` -- here we study the kernel itself.
For integers `q >= 1`, `r0 >= t0 + q - 1 >= 0`, the solid minor with rows
`r = r0..r0+q-1` and columns `t = t0..t0+q-1` satisfies the exact identity

    det[ B_{r0+a, t0+b} ]_{a,b=0}^{q-1}
      =  prod_{a=0}^{q-1} (H - r0 - a)_{t0}
       * prod_{a=0}^{q-1} (r0 + a)_{t0}
       * prod_{0<=a<b<=q-1} (b - a)
       * prod_{0<=a<b<=q-1} (H - 2 r0 - a - b).

**Corollary (total positivity).** On the physical domain of the knife
problem every row index satisfies `r <= n - 2`, and there
`H - (2r - 1) = (D-1)/2 + 2(n - 2 - r) >= (D-1)/2 > 0` for `D > 3`. Every
root of the identity's right side is `<= 2(r0 + q - 1) - 1 = 2 r_max - 1`
(the largest core root) or `<= r_max + t0 - 1 < 2 r_max - 1` (row factors),
so every factor is strictly positive there. Hence ALL solid minors of the
depth kernel are strictly positive on the physical domain: the kernel is
strictly totally positive there.

## Proof

Write `y_a = r0 + a` for the row values.

**Step 1 (row extraction).** For `t >= t0` the falling factorials split
exactly: `(H-r)_t = (H-r)_{t0} (H-r-t0)_{t-t0}` and
`C(r,t) t! = (r)_t = (r)_{t0} (r-t0)_{t-t0}`. Extracting the two
`t`-independent factors `(H-y_a)_{t0} (y_a)_{t0}` from row `a` leaves the
matrix with entries (writing `u = t - t0 = b`):

    E_{a,u} = (y_a - t0)_u * (H - t0 - y_a)_u
            = prod_{i=0}^{u-1} (y_a - t0 - i)(H - t0 - i - y_a).

**Step 2 (the quadratic collapse).** Each factor pair has roots
`t0 + i` and `H - t0 - i`, symmetric about `H/2`. Therefore

    (y - t0 - i)(H - t0 - i - y) = -( z + c_i ),
    z := y^2 - H y,   c_i := (t0 + i)(H - t0 - i),

with the SAME substitution `z` for every `i` and every row. Hence

    E_{a,u} = (-1)^u * prod_{i=0}^{u-1} (z_a + c_i),   z_a := y_a^2 - H y_a :

column `u` is a monic polynomial of degree `u` in `z`, times `(-1)^u`.

**Step 3 (generalized Vandermonde).** Pulling `(-1)^u` out of column `u`
gives the sign `(-1)^{q(q-1)/2}`, and the remaining matrix
`[ p_u(z_a) ]` with monic `deg p_u = u` reduces by elementary column
operations to `[ z_a^u ]`, whose determinant is the Vandermonde
`prod_{a<b} (z_b - z_a)`. Finally

    z_b - z_a = (y_b - y_a)(y_a + y_b - H) = -(y_b - y_a)(H - y_a - y_b),

so the product of the `q(q-1)/2` minus signs cancels the sign from the
columns, and with `y_b - y_a = b - a`:

    det E = prod_{a<b} (b - a) * prod_{a<b} (H - y_a - y_b),

which together with Step 1's extracted factors is the claimed identity
(`y_a + y_b = 2 r0 + a + b`).  QED.

## Verification

`lab/kernel_minor_identity.py` compares the symbolic determinant against
the closed form INCLUDING the constant: 86/86 exact matches over
`q <= 5`, `r0 <= 12`, `t0 <= 3` (results/kernel_minor_identity.json).
The fitted-law stage that led here, with its two wrong intermediate
guesses, is preserved in results/kernel_minor_law.json.

## What this does and does not give

It gives: strict total positivity of the depth kernel on the physical
domain, as a theorem. By the variation-diminishing property of TP
kernels, the number of sign changes of `t -> sum_b B_{r,t} x_b` is at
most that of `x`; the knife input carries the alternating weight
`(-1)^t M_t^(r)`, so TP alone does NOT settle `K_r >= 0` (the outside
report says the same). The open continuation is to pair this kernel
theorem with the exact affine depth recursion
`M_t^(r+1) = (1 - t/(H-r)) M_t^(r)` and the structure of `M` -- the naive
positive-measure hypothesis for `M` is already refuted at small `lam`
(results/moment_kernel_probe.json), so the pairing must use something
weaker than a Hausdorff measure.
