# SELF-CHECK BEFORE ANY CONCLUSION

Built 2026-08-17 18:02 from mistakes actually made in this project, on the founder's
instruction: check myself immediately, before drawing a conclusion, so nothing
propagates. Each line below cost us real time on 2026-08-17.

Run this list BEFORE calling anything a result, a limit, or a discovery.

## 1. Am I generalising from too few cells?
Cost: claimed "one real root, always" after checking critical cells only --
the true count ranges 0..12.
CHECK: extend the grid by 10x AND hold out points to PREDICT, never fit-only.

## 2. Is the extremum sitting on the edge of my scan window?
Cost: ERR-0003. The shore was computed as a minimum over k <= 60, the true
minimiser grows like sqrt(3)*lam, so the shore was overestimated 6x at
lam = 1000 -- and it surfaced as a fake counterexample to the theorem.
CHECK: widen the window; a minimum attained at the edge is a bug report.

## 3. Does my cross-check exercise the FULL pipeline?
Cost: compared the fast and slow engines on the same single function, saw
agreement, and concluded "a real limit of the method". It was a porting bug
(tail+base lost).
CHECK: the reference must run the whole path, not the function I suspect.

## 4. Did a numerical coincidence get an exact confirmation?
Cost: numpy SVD "found" an order-1 recurrence; exact rational arithmetic showed
the ratios are huge irregular fractions.
CHECK: every numerical pattern is re-derived in exact arithmetic before it is
believed.

## 5. Are the values jumping around?
Cost: 1.23, 1.69, 1.51, 1.24, 2.05 looked like a violation of monotonicity; the
threshold finder was bisecting a polynomial with up to 9 sign changes and
returning a later root.
CHECK: implausible scatter means the instrument is wrong before the pattern is
real.

## 6. Is the failure a bug rather than a fact about the mathematics?
Cost: the biggest one of the day. A saddle sum off by 250 orders of magnitude
made me write "the Stokes topology is the obstacle" and abandon the correct
route for eight hours. It was a coding error; the route works to 1.2%.
CHECK: a catastrophic mismatch (many orders of magnitude) is a bug until
proven otherwise -- reimplement independently before drawing any conclusion.

## 7. Have I searched the literature IN THE SAME HOUR?
Cost: called the descent lemma the result of the day; it is Matheron's montee,
classical.
CHECK: any statement about to be called new gets a prior-art search
immediately, not the next morning.

## 8. Is my measured margin actually loose enough to matter?
Cost: called the j-ladder inequality "half the problem"; its margin is 1.0000
at the shore, i.e. it is logically equivalent to the theorem.
CHECK: measure the margin BEFORE promising that a reduction helps.

## 9. Are the derivatives / numerics stable?
Cost: finite differences on high-degree polynomials returned 2640 instead of
~1; float root-finding gave a fake outlier at j = 16.
CHECK: analytic derivatives where available; high precision (flint acb) when
degrees grow.

## 10. Would the deterministic gate accept this?
CHECK: artifact regenerated from a clean tree, dirty flag false, work counters
non-zero, coverage strings honest about what was NOT covered.
