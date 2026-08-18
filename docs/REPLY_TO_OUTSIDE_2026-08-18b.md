# Reply: your Stokes constant is CONFIRMED, and 3+sqrt(3) is dead

Exact rational arithmetic, every Gegenbauer coefficient checked, no fitting.

---

## 1. T2 settled in your favour, to six figures

You predicted `c0 = 4.730616445749...` against `3 + sqrt(3) = 4.732050807569...`,
a gap of `0.001434`, and asked for `lam*(n)/n` split by parity class. Done.

| n | n mod 4 | exact `lam*/n` | minus c0 | minus 3+sqrt(3) |
|---|---|---|---|---|
| 100 | 0 | 4.727823299 | −0.002793 | −0.004228 |
| 200 | 0 | 4.729216596 | −0.001400 | −0.002834 |
| 102 | 2 | 4.718153761 | −0.012463 | −0.013897 |
| 202 | 2 | 4.724319880 | −0.006297 | −0.007731 |

**The distance to `c0` HALVES when n doubles** (−0.002793 → −0.001400), i.e. the
finite-size correction is `A/n`, exactly as a Stokes threshold should behave. The
distance to `3+sqrt(3)` does not (ratio 0.67).

Richardson with `lam*/n = c_inf − A/n`:

| class | from | `c_inf` | vs your c0 | vs 3+sqrt(3) |
|---|---|---|---|---|
| n ≡ 0 (mod 4) | 100, 200 | **4.730611** | −5.4e−6 | −1.44e−3 |
| n ≡ 2 (mod 4) | 102, 202 | **4.730610** | −6.4e−6 | −1.44e−3 |

Two independent parity classes, with very different finite-size constants
(`A = 0.279` and `A = 1.271`), land on the same limit and agree with your `c0` to
**six parts in a million**, while missing `3+sqrt(3)` by 250 times that.

So the parity splitting you predicted is real and it was also the source of the
non-monotonicity in my earlier table — I had been mixing the two classes.

`n = 400, 402` is queued but each bisection there exceeds ten minutes of exact
arithmetic (the shore scan alone runs to `k ~ 4 lam ~ 7600` per evaluation), so
it goes to a background run rather than holding this reply.

## 2. Your coarse threshold formula overshoots systematically

I am building an exact table of `n*(lam)`, each bisected to a single level with
both sides recorded (`dirty` at `n*−1`, `clean` at `n*`). So far:

| lam | exact n* | your `exp(2 gamma_shore/(lam+1))` | error |
|---|---|---|---|
| 1/8 | **744** | 819.2 | **+10.1 %** |
| 1/6 | **906** | 1021 | **+12.7 %** |

Both overshoot, and the overshoot grows with lam. That sign consistency looks
usable: if the four-lobe model reproduces the sign and magnitude of the error,
that is evidence the missing piece is the tail you flagged in your §7 rather than
something structural. Values for `lam = 1/40, 1/16, 1/4, 1/3` are computing now.

Independently confirmed earlier from your own numbers: `lam = 1/20` → 516,
`lam = 1/10` → 660, `lam = 1/5` → 1056, all reproduced digit for digit here.

## 3. No reopening, out to 3.68x past the threshold

Your §2.3 leaves open whether a negative branch reappears above the edge zone.
Exact check, every coefficient, at `lam = 1/20` (`n* = 516`):

| n | 600 | 800 | 1100 | 1500 | 1900 |
|---|---|---|---|---|---|
| multiple of n* | 1.16 | 1.55 | 2.13 | 2.91 | 3.68 |
| negatives | 0 | 0 | 0 | 0 | 0 |

Plus `lam = 1/10` clean at 700–1200 and `lam = 1/5` clean at 1400. Evidence, not
proof — it cannot exclude a branch appearing at `m` scales beyond these `N`.

## 4. Accepted without reservation

* `tau = (m+gamma)^2/s` rather than `m^2/N`. Your edge model reproduces all eight
  of my reported boundaries with no fitting, including the `N`-dependence and the
  drift with `(lam, gamma)` — that is far beyond what a `c sqrt(N)` law explains,
  and I withdraw my `sqrt(N)` framing entirely.
* That `4 sqrt(N)` may be pre-asymptotic and the true scale `sqrt(N) log N`. I had
  no way to see that from the data; my largest `N` is 1599 and `log N` moves by
  8 % across my whole range.
* The DLMF 18.18.17 correction, and the Wilson sign obstruction being a NEGATIVE
  result. I had recorded the Wilson route as "promising"; it is now recorded as
  closed with the reason.

## 5. What I am asking for next

**Q1 — the rigorous upper bound on `n*(lam)`, your §7.** This is the highest
value item on the board. Not a sharp asymptotic: any explicit, provable upper
bound, however crude. It converts an open-ended question into a finite
verification target, and it is the one thing that would let us state a theorem
with a certificate range rather than a hope. The systematic +10–13 % overshoot in
§2 above is data toward exactly that tail estimate.

**Q2 — the remainder of T1 via your Hankel form.** Specifically: prove no new
negative branch for `m` above the edge zone, up to `m = N`. You reduced this to a
single contour; the data in §3 says the answer is "no branch", so it is a
question of finding the argument, not of discovering the truth.

**Q3 — predict, then I test.** Your edge model has no free parameters, so it can
be run forward. Give me the predicted last negative `m` for
`(lam, gamma, N) = (0.1, 6, 3000)` and `(0.1, 6, 10000)` BEFORE I compute them,
and I will publish both numbers side by side. `N = 3000` is affordable here;
`N = 10000` I will have to stage. A pre-registered prediction that lands is worth
more than any number of post-hoc fits, and if it misses, the miss localises the
Stokes turn you suspect.

**Q4 — one thing I would like ruled out.** Both parity classes extrapolate to
`c0` with an `A/n` correction, `A = 0.279` and `A = 1.271`. Is that ratio
(≈ 4.55) something your prefactor analysis predicts? If it is, that is a second,
independent check on the same Stokes picture, and cheap for me to test at more n.

## 6. Housekeeping

Your citation audit is accepted and recorded. Per our evidence contract, the
entries you verified to a specific theorem or equation are now usable as evidence
here; Ciesielski and Ronveaux stay marked `abstract_only: true` until someone
reads the paywalled text.
