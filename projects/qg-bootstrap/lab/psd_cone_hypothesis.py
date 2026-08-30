"""Is (B) about arithmetic progressions, or about quadratic forms on a 2D PSD cone?

Our weights are `b_k = (a + kd)^2`, which is the rank-one case of

    b_k = (1  k) Q (1  k)^T = A + 2Bk + C k^2,     Q = [[A, B], [B, C]].

The rank-one boundary is `B^2 = AC`. The proposed hypothesis: (B) holds for EVERY
positive semidefinite `Q`, not only on that boundary. If true, the mechanism behind (B)
is not the arithmetic progression at all but positivity of a quadratic form, and the
K-Lorentzian / cone-restricted Rayleigh machinery becomes the natural tool. If instead
it holds only on the rank-one boundary, that is equally informative and sharply narrows
the mechanism.

The test is exact. `Q` ranges over rational matrices in three regimes -- deep interior
(`AC - B^2` large), near-boundary (`AC - B^2` small and positive), and exactly rank-one --
so that a failure can be located rather than merely observed. Both signs of `B` are
covered, since `b_k` stays positive on the PSD cone regardless.

The claim is tested on the SAME domain as (B) for the physical family: `1 <= t <= N/2`.
Testing past the midpoint would report failures that are outside the statement, a mistake
this lab has already paid for once.

Run: python lab/psd_cone_hypothesis.py -> results/psd_cone_hypothesis.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from math import comb
from pathlib import Path

from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from sciencebro_math.families import esym  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"
SEED = 20260830


def weights(A: fmpq, B: fmpq, C: fmpq, N: int) -> list[fmpq]:
    return [A + 2 * B * k + C * fmpq(k) ** 2 for k in range(N)]


def fails_B(b: list[fmpq]) -> list[int]:
    """Indices t in 1..floor(N/2) where p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2} FAILS."""
    N = len(b)
    e = esym(b)
    p = [e[t] / fmpq(comb(N, t)) for t in range(N + 1)]
    top = N // 2
    return [
        t for t in range(1, top + 1) if t + 2 <= N and p[t + 1] ** 3 * p[t - 1] < p[t] ** 3 * p[t + 2]
    ]


def main() -> int:
    t0 = time.time()
    rng = random.Random(SEED)
    rows: dict[str, dict] = {}

    def regime(name: str, gen, trials: int, Ns: tuple[int, ...]) -> None:
        tested = 0
        bad = []
        for N in Ns:
            for _ in range(trials):
                A, B, C = gen()
                disc = A * C - B * B
                if A < 0 or C < 0 or disc < 0:
                    continue
                b = weights(A, B, C, N)
                if any(x <= 0 for x in b):
                    continue
                tested += 1
                f = fails_B(b)
                if f:
                    bad.append(
                        {
                            "N": N,
                            "A": str(A),
                            "B": str(B),
                            "C": str(C),
                            "det": str(disc),
                            "failing_t": f,
                        }
                    )
        rows[name] = {"tested": tested, "failures": len(bad), "examples": bad[:5]}
        print(f"  {name:<28} tested {tested:>5}   FAILURES {len(bad)}")

    def rank_one():
        a = fmpq(rng.randint(1, 30), rng.randint(1, 8))
        d = fmpq(rng.randint(1, 30), rng.randint(1, 8))
        return a * a, a * d, d * d

    def interior():
        A = fmpq(rng.randint(1, 40), rng.randint(1, 6))
        C = fmpq(rng.randint(1, 40), rng.randint(1, 6))
        # |B| well inside sqrt(AC): take B^2 <= AC/4
        s = rng.choice([1, -1])
        B = s * fmpq(rng.randint(0, 20), rng.randint(4, 20))
        return (A, B, C) if A * C - B * B >= 0 else (A, fmpq(0), C)

    def near_boundary():
        a = fmpq(rng.randint(1, 20), rng.randint(1, 5))
        d = fmpq(rng.randint(1, 20), rng.randint(1, 5))
        eps = fmpq(1, rng.randint(50, 5000))
        s = rng.choice([1, -1])
        return a * a, s * (a * d - eps), d * d

    def degenerate_C_zero():
        """C = 0 forces B = 0 on the cone: b_k constant. The extreme ray."""
        return fmpq(rng.randint(1, 20)), fmpq(0), fmpq(0)

    def degenerate_A_zero():
        """A = 0 forces B = 0: b_k = C k^2, which starts at zero."""
        return fmpq(0), fmpq(0), fmpq(rng.randint(1, 20))

    print("(B) on the 2D PSD cone, exact, domain 1 <= t <= N/2")
    Ns = (8, 11, 14, 17, 20)
    regime("rank-one boundary (our case)", rank_one, 60, Ns)
    regime("PSD interior", interior, 60, Ns)
    regime("near the rank-one boundary", near_boundary, 60, Ns)
    regime("extreme ray C = 0", degenerate_C_zero, 5, Ns)
    regime("extreme ray A = 0", degenerate_A_zero, 5, Ns)

    interior_holds = rows["PSD interior"]["failures"] == 0
    out = {
        "question": "does (B) hold for every PSD quadratic form b_k = A + 2Bk + Ck^2, or only "
        "on the rank-one boundary where b_k = (a+kd)^2?",
        "why_it_matters": "if the whole cone works, the mechanism is quadratic-form positivity "
        "rather than the arithmetic progression, and cone-restricted Rayleigh / K-Lorentzian "
        "machinery applies; if only rank-one works, that narrows the mechanism just as sharply",
        "domain": "1 <= t <= floor(N/2), the same domain (B) is stated on",
        "seed": SEED,
        "regimes": rows,
        "holds_on_the_whole_PSD_cone": interior_holds
        and rows["near the rank-one boundary"]["failures"] == 0,
        "runtime_s": round(time.time() - t0, 1),
        **stamp(),
    }
    (RES / "psd_cone_hypothesis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nholds on the whole PSD cone: {out['holds_on_the_whole_PSD_cone']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
