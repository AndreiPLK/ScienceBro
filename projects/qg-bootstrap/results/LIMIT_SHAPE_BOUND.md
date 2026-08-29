# The limit-shape bound f(theta) < 2, proved

2026-08-29. Machine checks: `lab/limit_shape_check.py` ->
`results/limit_shape_check.json`.

## What is proved

With `theta(u) = 1 - arctan(u)/u` for `u > 0` and

    f(theta) = (2/u) / (dtheta/du) - 1/theta - 1/(1-theta),
    dtheta/du = arctan(u)/u^2 - 1/(u(1+u^2)),

the statement is

    f(theta) < 2   for all 0 < theta < 1/2.

This is the asymptotic half of the lemma that a depth-uniform (R) needs
(`FARBELOW_NEGATIVE_PATTERN.md`): `f` is the limit shape of `(excess - 1) n` for
the Newton excess of the central factorial family.

## Provenance, and the correction

The proof came from a second assistant, in a PDF the founder relayed
(`Analytic_Proofs_f_theta_and_nJ.pdf`, 29 Aug). **Untrusted input by the
repository's rule**, so every step was checked here — and one step needed
repair.

**Verified as printed:** the reformulation
`f = 2/(t-c) - 1/(1-t) - 1/t` with `t = arctan(u)/u = 1-theta`, `c = 1/(1+u^2)`
(matches the direct computation to 30 digits at `u` = 0.5, 1, 2, 2.33); the
equivalence `f < 2 <=> c < Phi(t)` with

    Phi(t) = t(-1 + 4t - 2t^2) / (1 + 2t - 2t^2);

the monotonicity step `Phi'(t) = (4t^4 - 8t^3 + 8t - 1)/(1+2t-2t^2)^2 > 0`, whose
numerator at `t = 1/2 + y` is `4y^4 + 2y(2-3y) + 9/4 > 0` on `0 < y < 1/2`; and
the Shafer–Fink route giving `z = 1/sqrt(1+u^2) > 14/37` from `t > 1/2` and
`pi < 22/7`.

A pleasing internal check: `c < Phi(t)` fails exactly at `u = 2.6586`, which is
where `f = 2` — the crossing this repository had already located independently.

**The one step that did not reproduce** is the factorisation of
`Phi(3z/(z+2)) - z^2`. As printed it evaluates NEGATIVE (−0.011 at `z = 0.4`,
−0.104 at `z = 0.707`) while the true value is positive (+0.0067, +0.0304). The
cause is a missing square. Deriving it here: with `w = 3z/(z+2)`,

    -1 + 4w - 2w^2 = (-7z^2 + 20z - 4)/(z+2)^2,
     1 + 2w - 2w^2 = (-11z^2 + 16z + 4)/(z+2)^2,
    Phi(w) = 3z(-7z^2+20z-4) / [(z+2)(-11z^2+16z+4)],

so `Phi(w) - z^2` has numerator `3z(-7z^2+20z-4) - z^2(z+2)(-11z^2+16z+4)
= z(11z^4 + 6z^3 - 57z^2 + 52z - 12)`, and `z = 1` is a DOUBLE root of that
quartic:

    11z^4 + 6z^3 - 57z^2 + 52z - 12 = (z-1)^2 (11z^2 + 28z - 12).

Hence

    Phi(3z/(z+2)) - z^2  =  z (z-1)^2 (11z^2 + 28z - 12) / [(z+2)(-11z^2+16z+4)],

which is the printed expression with `(z-1)` replaced by `(z-1)^2`. Checked
against the direct evaluation at `z` = 0.38, 0.4, 0.5, 0.7071, 0.9, 0.99: it
reproduces at every one, to 22 digits.

**With the square, the printed sign argument goes through verbatim**, and it is
the argument that carries the proof: `11z^2 + 28z - 12 > 0` for `z > 14/37`
(value `232/1369` at the endpoint, increasing), `-11z^2 + 16z + 4 > 0` on
`0 < z < 1`, and `(z-1)^2 > 0`, so the whole expression is positive. Therefore
`Phi(3z/(z+2)) > z^2 = c`, and since `Phi` is increasing and `t > 3z/(z+2)`,
`c < Phi(t)`. That is `f < 2`. QED

## What this closes, and what it does not

**Closed:** the asymptotic half. `f(theta) < 2` on `(0, 1/2)`, proved, not
sampled — and with room, since `f` reaches 2 only at `theta = 0.5445`.

**Not closed:** the lemma as the certificate actually uses it is the FINITE
statement `p_t^2/(p_{t-1}p_{t+1}) <= 1 + 2/n` for `n >= 44`. Passing from the
limit shape to finite `n` needs an effective error bound — the measured excess
approaches `f` from above, with the gap at `n = 240` running 0.006 to 0.012. What
is measured on the used range is a maximum constant of 1.8393 (at `n = 44`,
`t = 21`) against the 2 allowed. So: asymptotics proved, finite range measured,
and the bridge between them is the remaining work.

The companion rational inequality in `(n, J)` from the same PDF was also checked:
its `Delta` formula reproduces over 6555 pairs and its `a, b` substitution
`Q = 2a^2b + 9a^2 + 2ab^2 + 19ab + 57a + 2b^2 + 13b + 48` over 1600 — both exact,
0 mismatches. That half had already been proved here by a shorter cancellation
argument; two independent proofs now agree.
