"""Is the log-concavity excess harmonically additive under independent sums?

An UPPER bound on the Newton excess is what the programme needs and what
real-rootedness alone cannot give (`SELFCONV_PRESERVATION.md`, `THEOREM_STATE.md`).
Since the excess behaves like `1/sigma^2` and variances ADD, the natural candidate is

    (H)   1/L_{X+Y} >= 1/L_X + 1/L_Y,     L_f(t) = log[ f(t)^2 / (f(t-1) f(t+1)) ].

It is false, and the data says so in a useful way.

Two things had to be right before the answer meant anything:

* **the correspondence.** For independent X, Y the tilted sum at tilt z is the sum
  of the tilted parts at the SAME z, so the points must be matched at a common
  tilt: `a = mean_X(z)`, `b = mean_Y(z)`, `t = a + b`. A first version matched
  arbitrary pairs and duly "refuted" (H) on 59% of them, which meant nothing.
* **the regime.** At 4-10 summands the excess is ~0.6, nowhere near the
  `1/sigma^2` regime the idea comes from. Here each side carries 30-70 summands.

Result: in its own regime the inequality holds UNIFORMLY IN THE OTHER DIRECTION --
`1/L` is subadditive, and very nearly additive. So this route bounds the excess of a
sum from BELOW, which is the direction already available from Newton, and not the
one needed.

That is not a surprise once seen: `1/L = sigma^2 (1 - c/n + ...)` by the Edgeworth
identification (`edgeworth_prediction.json`), and `sigma^2` is exactly additive, so
the defect measured here IS that correction in another guise.

Run: python lab/excess_subadditivity.py -> results/excess_subadditivity.json
"""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path("lab").resolve()))
from flint import fmpq
from mpmath import mp, mpf, log
mp.dps = 40

def pmf(ws):
    f = [fmpq(1)]
    for w in ws:
        g = [fmpq(0)]*(len(f)+1)
        for i, v in enumerate(f):
            g[i] += v*(1-w); g[i+1] += v*w
        f = g
    return f

def L(f, t):
    if t-1 < 0 or t+1 >= len(f) or f[t-1] == 0 or f[t+1] == 0: return None
    r = f[t]*f[t]/(f[t-1]*f[t+1])
    v = log(mpf(int(r.numer()))/int(r.denom()))
    return v if v > 0 else None

def tmean(ws, z):
    s = mpf(0)
    for w in ws:
        p = mpf(int(w.numer()))/int(w.denom())
        s += p*z/(1-p+p*z)
    return s

rng = random.Random(23)
sup = sub = tested = 0
worst_sup = worst_sub = None
for trial in range(40):
    nx, ny = rng.randint(30, 70), rng.randint(30, 70)
    wx = [fmpq(rng.randint(2, 18), 20) for _ in range(nx)]
    wy = [fmpq(rng.randint(2, 18), 20) for _ in range(ny)]
    fx, fy, fz = pmf(wx), pmf(wy), pmf(wx+wy)
    for z in (mpf("0.4"), mpf(1), mpf("2.5")):
        ai, bi = int(round(float(tmean(wx, z)))), int(round(float(tmean(wy, z))))
        la, lb, lz = L(fx, ai), L(fy, bi), L(fz, ai+bi)
        if None in (la, lb, lz): continue
        tested += 1
        lhs, rhs = 1/lz, 1/la + 1/lb
        rel = float((lhs-rhs)/rhs)
        if lhs < rhs:
            sup += 1
            if worst_sup is None or -rel > worst_sup[0]: worst_sup = (round(-rel,4), ai, bi)
        else:
            sub += 1
            if worst_sub is None or rel > worst_sub[0]: worst_sub = (round(rel,4), ai, bi)
import json, time
from provenance import stamp
RES = Path(__file__).resolve().parents[1] / "results"
out = {
    "question": "does 1/L (the reciprocal log-concavity excess) add under independent sums?",
    "candidate": "1/L_{X+Y} >= 1/L_X + 1/L_Y, matched at a common tilt",
    "verdict": "FALSE -- and uniformly so: 1/L is SUBadditive, hence this bounds the "
               "excess of a sum from below, the direction Newton already gives",
    "summands_per_side": "30..70",
    "tested": tested,
    "subadditive_cases": sup,
    "superadditive_cases": sub,
    "worst_relative_shortfall": worst_sup,
    "note": "at 4-10 summands the same test is meaningless (excess ~0.6, far from the "
            "1/sigma^2 regime); and matching arbitrary point pairs instead of a common "
            "tilt refutes nothing",
    **stamp(),
}
(RES / "excess_subadditivity.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"tested {tested}: 1/L_sum < 1/L_x + 1/L_y in {sup}, >= in {sub}")
print("  worst shortfall:", worst_sup, "  worst excess:", worst_sub)
