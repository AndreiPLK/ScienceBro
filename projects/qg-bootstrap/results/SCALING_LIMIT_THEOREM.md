# The scaling limit of the whole knife family, in closed form

Derived and machine-checked on the night of 2026-08-17/18. Every step below is
either exact algebra or a verification run that is named, so it can be repeated.

## Statement

Fix the knife index j >= 2. In the scaling limit

    n = rho * lam,   D = d * lam,   lam -> infinity   (rho, d fixed)

the knife-j condition of the CHR graviton family becomes

        knife_j  ->  ( 2 rho^2 + 12 rho + 6 - d rho )^{j-1} / ( 6 (rho+1)^2 )^{j-1}

so, since the denominator is positive:

* **j odd** (j-1 even): the expression is a perfect even power, hence never
  negative. The odd knives are safe at leading order for every d and rho, and
  vanish only ON the curve.
* **j even** (j-1 odd): the sign is that of 2 rho^2 + 12 rho + 6 - d rho, so the
  knife holds exactly while

        d  <  2 rho + 12 + 6 / rho .

  The minimum of the right-hand side over rho is at rho = sqrt(3) and equals

        12 + 2 sqrt(12)  =  12 + 4 sqrt(3)  =  18.92820...

  which is exactly the shore asymptote of the published shore paper.

So in the scaling limit the even knives are EXACTLY marginal against the shore
asymptote -- tangent, not crossing -- and the odd knives keep clear of it. That
is the mechanism behind the recorded parity law ("odd knives never cut") and it
explains the finite-lam measurements: knife 4 approaches D*/shore = 1 (1.0042 at
lam = 60) while knives 3 and 5 level off at about 1.087 and 1.066.

## Proof

Start from the closed form derived tonight (lab/knife_closed_form.py):

    knife j > 0  <=>  SUM_{t=0}^{j-1} (-1)^t E_2t(n) s^{-2t} R_t > 0,   s = lam+n-1

    R_t = [prod_{i=1..t} (j-i)] [prod_{i=1..t} (D + 4n - 2j - 5 - 2(i-1))]
          / ( [prod_{i=1..t} (n-i)] [prod_{i=1..t} (2n-1-2i)] ).

Two leading-order inputs:

1. **The central factorial numbers.** E_2t(n) = n^{3t} / (3^t t!) + lower order.
   Verified exactly for t = 1..5 from the closed polynomial forms (each of which
   was itself checked against the integer sequence on both parities up to
   n = 59), and numerically for t = 1..8: E_2t(n)/n^{3t} divided by 1/(3^t t!)
   gives 0.981, 0.952, 0.913, 0.866, 0.812, 0.752, 0.688, 0.622 at n = 160,
   rising toward 1 as n grows at fixed t.

2. **The moment ratios.** With n = rho lam and D = d lam, R_t contributes the
   falling factorial (j-1)(j-2)...(j-t) and a factor [rho (d + 4 rho)]^t
   / [2 rho^2 (rho+1)^0 ...]^t; combined with s^{-2t} = [lam(rho+1)]^{-2t} the
   whole term becomes

        (-1)^t * C(j-1, t) * x^t,      x = rho (d + 4 rho) / (6 (rho+1)^2),

   the binomial coefficient arising as (j-1)!/(t! (j-1-t)!): the t! from E_2t,
   the falling factorial from R_t.

Newton's binomial then sums the series for every j at once:

    SUM_t (-1)^t C(j-1,t) x^t = (1 - x)^{j-1},
    1 - x = (2 rho^2 + 12 rho + 6 - d rho) / (6 (rho+1)^2),

which is the statement.

## Verification actually performed

* The closed form of each knife was checked against the exact flint engine on 24
  cells for each of j = 2, 3, 4, 5, 6 -- zero disagreements
  (results/knife_closed_form.json).
* The leading scaling coefficients were computed symbolically and factor exactly
  as the theorem predicts:

      j = 3:  + 5   rho^2 (d rho - 2 rho^2 - 12 rho - 6)^2
      j = 4:  - 35  rho^3 (d rho - 2 rho^2 - 12 rho - 6)^3
      j = 5:  + 175 rho^4 (d rho - 2 rho^2 - 12 rho - 6)^4
      j = 6:  - 385 rho^5 (d rho - 2 rho^2 - 12 rho - 6)^5

* Knife 6 was computed AFTER the mechanism was stated, as a prediction: the
  parity argument says its bracket must appear to an ODD power. It does (power
  5), and its closed form agrees with the engine on 24 cells.

## Limitations, stated plainly

* The limit is taken at FIXED j. The convergence E_2t(n) -> n^{3t}/(3^t t!) is
  slower for larger t (at n = 160 the ratio is 0.98 for t = 1 but 0.62 for
  t = 8), so the result is NOT uniform in j and says nothing about j growing with
  lam.
* It is a statement about the LEADING order in lam. On the curve itself the
  leading term vanishes and the sign is decided by subleading terms; that is
  exactly the delicacy the published blade theorem had to handle for j = 3, and
  it is untouched here.
* It therefore does not by itself prove the finite-lam theorem. What it does is
  explain the structure, fix the parity mechanism, and identify the even knives
  as the marginal ones.

## 2026-08-18 04:46 -- the tangency is approached from the SAFE side (asymptotics closed)

The scaling-limit form says the even knives vanish exactly on
d = 2 rho + 12 + 6/rho, whose minimum over rho is the shore asymptote
12 + 4 sqrt(3) at rho* = sqrt(3). Two things finish the asymptotic question:

1. STRICTLY BELOW THE SHORE the leading term already settles it. For d < the
   curve, the bracket (d rho - 2 rho^2 - 12 rho - 6) is negative; knife 4 carries
   it to an ODD power with a minus sign in front, so the leading term is positive.
   Since the shore is the MINIMUM of the curve, d < shore implies d < curve(rho)
   for every rho, hence every knife is positive at leading order.

2. ON THE CURVE the leading term vanishes and the next order decides. Substituting
   D = (2 rho + 12 + 6/rho) lam exactly and expanding:

     j = 4: -12 rho (rho+1)^2 (128 rho^4 - 972 rho^3 + 810 rho^2 + 288 rho - 117)
     j = 6: 1584 rho^2 (rho+1)^4 (2 rho^2 - 6 rho - 3)
            (256 rho^4 - 1692 rho^3 + 738 rho^2 + 576 rho - 45)

   At the tangency rho = sqrt(3) these are exactly

     j = 4:  22896 sqrt(3) + 128952        = 1.68609e5   > 0
     j = 6:  1811652480 sqrt(3) + 3362078016 = 6.49995e9 > 0

   both strictly positive. Moreover the quartic for j = 4 has real roots at
   -0.439, 0.267, 1.182, 6.584, so the subleading term is positive on the whole
   interval rho in (1.182, 6.584) -- and rho* = sqrt(3) = 1.732 sits comfortably
   inside it, not on its edge.

CONCLUSION for the scaling limit: the even knives touch the shore asymptote from
the SAFE side. They do not cut into the allowed region even in the limit, and the
tangency is not a knife-edge in rho either.

That closes the asymptotic question I posed at the start of the night ("does the
fourth knife survive as lam grows?"). What remains is the finite-lam statement,
where the margin is 1 + C/n and the exponentially small quantities live.
