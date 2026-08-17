# How to close the last infinity (written 2026-08-17 15:17, for the next shift)

## The reframing

We have been saying "j is unbounded, that is the last gap". In the Gegenbauer
language that statement dissolves, and it is worth being precise about why.

The theorem is really: for every level n and every dimension D below the
shore, ALL partial waves b_l of the residue are nonnegative. At a FIXED level
n the number of partial waves is FINITE (spins l <= 2n - 4). So j is not
independently infinite -- the only genuine infinity is the level n.

Our certificates are organised the other way round: for a FIXED knife j we
cover all levels n symbolically. That is why j looks unbounded: we sliced the
(n, j) plane along the wrong axis. Both slicings are legitimate, but they
leave different remainders:

  * slice by j (what we did): each slice closes all n, but slices are
    infinite in number;
  * slice by n: each slice is FINITE (all spins at that level), but the
    slices are infinite in number.

Neither alone finishes. What finishes is a statement uniform in one of them.
The descent lemma is exactly that kind of statement -- uniform in the spin --
which is why it worked where everything else failed.

## The concrete route

At fixed spin l the partial wave has a projection form,

    b_l = INT_{-1}^{1} R_n(x) C_l^(a)(x) (1 - x^2)^{a - 1/2} dx ,

with a = (D-3)/2. Here C_l^(a) is a FIXED polynomial (l is fixed, and it does
not grow with n), while R_n is the residue, an explicit product. The sum over
t that grows with j never appears. So positivity at fixed spin becomes a
question about how the oscillations of one fixed Gegenbauer polynomial sit
against an explicit product -- a classical shape of problem, and one where the
n-dependence enters through R_n only.

Measured support for this being the right corner: at fixed spin there is NO
threshold at all, up to 40x the shore, for every spin and level tested
(recorded earlier today). So the fixed-spin direction is the safe direction,
and the projection form is the natural tool for proving it.

## Order of work for the next shift

1. Write the projection form explicitly for our residue and verify it against
   partial_waves() in exact arithmetic (cheap, and it must match).
2. At fixed spin, try to prove positivity for all n from the projection form
   (the integrand is explicit; the residue's roots are known).
3. Combine: fixed-spin positivity (all n, step 2) + the descent lemma
   (all D below the strip) + the strip certificate (all lam on branches)
   -> the remaining hole is only the pairs (n, j) not covered by either
      slicing, which should be a bounded set and hence finite work.
4. Only then: the lam tail above the last branch.

## Warning to my next self

Four independent attempts have now failed by assuming positivity decomposes
into positive pieces (negatives #19, #21, #23, #27). Do not try a fifth. Any
argument must be one that tolerates GLOBAL cancellation: an integral
representation with a positive measure, or an operator identity like the
dimension walk. Those are the only two things that have ever worked here.
