"""ROLLING SADDLES -- testing the founder's cycloid reading of the depth curve.

He looked at the depth curve (article/visuals/side-view.png) and said it looks
like a point on the rim of a rolling wheel: a smooth arch, then a cusp where the
point momentarily stops and reverses. Rotation plus translation, not a bounce.

That reading is literally testable here. If the coefficient

    bracket = [x^N] P(x),   N = j - 1

is dominated by a CONJUGATE PAIR of saddle points x = rho e^{+-i theta}, then
their two contributions add to

    2 |C| rho^{-N} cos(N theta + arg C)

-- a rotating vector whose modulus drifts with j. Such a quantity has smooth
maxima and cusps where it passes through zero, cusps and maxima strictly
alternate, and whether the sign flips at a cusp depends on whether a
non-oscillating contribution (a real saddle) is larger than the oscillating
amplitude. All four of those features were measured tonight, including a cusp
at j = 88 where the sign touched zero and returned.

So this module measures, with no fitting:
  1. all critical points of the integrand, as CERTIFIED roots of
     x P'(x) - (N+1) P(x) = 0 via flint's complex_roots (the old module used
     numpy.roots on float coefficients, which is not usable at these degrees);
  2. the magnitude |P(x)| / |x|^{N+1} of each, which is the modulus of its
     saddle contribution;
  3. the top few by magnitude, their arguments, and whether the top pair is
     conjugate.

If the dominant pair is conjugate and its argument advances steadily with j,
the founder's wheel is the mechanism and the block structure is a consequence.
"""

from __future__ import annotations

import cmath
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contour_lib import build_P  # noqa: E402
from flint import acb, arb, ctx, fmpq, fmpq_poly  # noqa: E402

OUT = Path("/tmp/rolling_saddles.json")


def critical_points(j: int, n: int, lam: F, dps: int = 80):
    """Certified roots of x P'(x) = (N+1) P(x)."""
    ctx.dps = dps
    P = build_P(j, n, lam)
    N = j - 1
    lhs = [F(0)] * (len(P) + 1)
    for i in range(1, len(P)):
        lhs[i + 1] += P[i] * i
    for i, c in enumerate(P):
        lhs[i] -= (N + 1) * c
    while lhs and lhs[-1] == 0:
        lhs.pop()
    q = fmpq_poly([fmpq(c.numerator, c.denominator) for c in lhs])
    return [z for z, _ in q.complex_roots()], P, N


def ranked_saddles(j: int, n: int, lam: F, top: int = 40, dps: int = 80):
    """Critical points sorted by |P(x)| / |x|^{N+1}, largest first."""
    ctx.dps = dps
    roots, P, N = critical_points(j, n, lam, dps=dps)
    cs = [acb(str(c.numerator)) / acb(str(c.denominator)) for c in P]
    out = []
    for z in roots:
        if z.abs_lower() == 0:
            continue
        v = acb(0)
        for cc in reversed(cs):
            v = v * z + cc
        mag = v.abs_lower() / (z.abs_lower() ** (N + 1))
        if mag == 0 or not arb(mag).is_finite():
            continue
        out.append((float(arb(mag).log() / arb(10).log()), complex(z)))
    out.sort(key=lambda p: -p[0])
    return out[:top]


def main() -> int:
    js = list(range(40, 132, 2))
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for j in js:
        if str(j) in data:
            continue
        t0 = time.time()
        try:
            top = ranked_saddles(j, j + 4, F(1))
        except Exception as exc:  # report, never hide
            print(f"  j={j}: FAILED {type(exc).__name__}: {exc}", flush=True)
            continue
        data[str(j)] = [{"log10_mag": m, "re": z.real, "im": z.imag} for m, z in top]
        OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
        z0 = top[0][1]
        conj = len(top) > 1 and abs(top[1][1] - z0.conjugate()) < 1e-12 * max(1.0, abs(z0))
        print(
            f"  j={j:3d}  top |x|={abs(z0):.6f} arg={cmath.phase(z0):+.5f}  "
            f"log10mag={top[0][0]:.2f}  conjugate pair: {conj}  ({time.time() - t0:.0f}s)",
            flush=True,
        )
    print("done:", len(data), "->", OUT, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
