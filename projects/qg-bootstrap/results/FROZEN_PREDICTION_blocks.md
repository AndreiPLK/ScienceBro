# FROZEN PREDICTION -- failing-block positions at lam = 1 (CLOSED FORM)

Frozen 2026-08-17 21:37:10 (system clock). Supersedes the width-only version frozen at
21:36:27 today, which is kept below. No boundary beyond j = 72 has been
examined at freeze time: the running long scan (lab/long_scan.py) has shown
only that the minima at j = 54..72 are all negative.

## The closed form

Three observed blocks at lam = 1 (starts 10, 28, 54; widths 8, 14, >=12) fit

        block k occupies      j = 2k(2k+3)  ..  4k(k+3)
        width                 w_k = 6k + 2
        gap to the next       g_k = 2k + 8

Check on what was already known:
        k = 1:  10 .. 16   (observed 10..16)
        k = 2:  28 .. 40   (observed 28..40)
        k = 3:  54 .. 72   (observed to start at 54; still failing at 72)

Both endpoints are quadratic in k with integer coefficients, and the leading
coefficient of the start, 4, is twice the leading coefficient of the width
step, 6/... -- no, stated plainly: start ~ 4k^2, end ~ 4k^2, width ~ 6k. The
"integer quantity behind the step 6" the founder asked for is therefore the
BLOCK INDEX k itself: widths are 6k+2 and gaps 2k+8, so the period is 8k+10.

## Predictions (unmeasured, falsifiable to the single j)

        block 4:  j =  88 .. 112   (width 26)
        block 5:  j = 130 .. 160   (width 32)
        block 6:  j = 180 .. 216   (width 38)   -- beyond the current scan

The long scan runs to j = 160, so it tests block 4 completely and the start of
block 5. A single j out of place refutes the closed form.

## What it does NOT establish

Nothing here is derived. Even if all boundaries land exactly, this stays an
empirical regularity of ONE family (lam = 1) until either (a) it is derived
from the structure of P(x), or (b) the same closed form with lam-dependent
coefficients is confirmed in at least two more families. lam = 7 is in the
same scan and is the first independent test.

Note on parity: the scan steps by 2, so every measured width is even by
construction. The content of the law is the STEP, not the parity.

---

## Previous version (width-only), frozen 2026-08-17 21:36:27

Hypothesis: widths form an arithmetic sequence w_k = 8 + 6(k-1), so widths of
blocks 3, 4, 5 are 20, 26, 32. The closed form above contains this as its
width statement and adds the positions.
