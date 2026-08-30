# (B) is a 2x2 minor: an exact determinant representation, derived not borrowed

*2026-08-30. Artefact: `results/minor_representation.json`.*

## The identity

Let `T_t = p_t^2 - p_{t-1} p_{t+1}` be the Turán determinant. Then

    H_{N,t} = p_{t+1}^3 p_{t-1} - p_t^3 p_{t+2}
            = p_t^2 T_{t+1} - p_{t+1}^2 T_t
            = det [ p_t^2    p_{t+1}^2 ]
                  [ T_t      T_{t+1}   ].

**Proof.** `p_{t+1} p_{t-1} = p_t^2 - T_t` and `p_t p_{t+2} = p_{t+1}^2 - T_{t+1}` by
definition, so

    H = p_{t+1}^2 (p_t^2 - T_t) - p_t^2 (p_{t+1}^2 - T_{t+1}) = p_t^2 T_{t+1} - p_{t+1}^2 T_t. ∎

Three lines, and it needs nothing about our particular spectrum — it holds for any positive
sequence. Verified against the direct expression at **860 `(n,t)` pairs over `n = 6..45`,
zero mismatches**.

## What it says

Form the `2 x N` matrix

    M = [ p_1^2  p_2^2  p_3^2  ... ]
        [ T_1    T_2    T_3    ... ].

Then **(B) is exactly the statement that the consecutive `2x2` minors of `M` are
nonnegative** — equivalently that `T_t / p_t^2` is increasing, which is the Newton excess
increasing, which is (B) in its original form.

Measured, and stronger than needed: **every** `2x2` minor of `M` on the first half is
nonnegative, not only the consecutive ones — 274 tested at `n = 11, 15, 21, 27, 33`, zero
negative. So `M` is totally positive of order 2 there.

## Why this is worth having

The recent-literature brief proposed two routes whose whole point was to express `H_{N,t}`
as a minor — Fan–Wang's higher-Laguerre determinants, and Díaz–Mainar's Schur-function
expansions of initial minors — so that positivity would follow from total-positivity
machinery instead of from direct algebra on a giant polynomial.

The minor is right here, and it took three lines. Whatever machinery gets applied next now
has a target of the right shape: a `2 x N` matrix built from `p^2` and the Turán
determinants, whose `2x2` minors are exactly the quantity to be signed.

## Honest limits

This is a **reformulation, not a proof**. `H = det[...]` is an identity; that the
determinant is nonnegative is precisely (B), and remains open in general (proved rung by
rung for `t <= 200`). Nothing here decides it.

It also does not contradict `THEOREM_NO_POLYA_FREQUENCY.md`. That theorem is about the
Toeplitz array of `p` itself, which is provably not totally positive. `M` is a different
matrix — two rows, built from `p^2` and `T` — and its `2x2` positivity is a separate
question.
