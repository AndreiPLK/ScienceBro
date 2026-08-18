"""THE STEP LEMMA: measuring the induction that could close the theorem.

Tonight's reformulation says the grand theorem is: the explicit nonnegative
polynomial

    F(u) = u^eps prod_a (u - (a/s)^2)^2,   a in {n-2, n-4, ...},  s = lam + n - 1

has an all-positive Jacobi expansion (sign (-1)^m on the m-th coefficient,
alpha = -1/2, beta = D/2 - 2). Measured facts that suggest an induction:

  * adding the ladder factors SMALLEST FIRST keeps every coefficient positive at
    every step; largest first fails until enough factors accumulate;
  * the largest admissible new root c grows with the number of factors already
    present, and the real ladder always stays below it (margin 320x at the first
    step, 1.11x at the last, n = 31).

So the candidate lemma is

    STEP LEMMA. If H has an all-positive expansion and c is small enough given
    (degree of H, beta), then H(u) (u - c)^2 also has an all-positive expansion.

For that to be a LEMMA rather than an observation, the threshold must depend on
H only through data we control. This module tests exactly that: it measures
c_max for DIFFERENT H of the SAME degree -- ladder products from different
(n, lam), and deliberately different root sets -- and compares.

  * If c_max depends only on (degree, beta), the lemma is clean and the induction
    closes the theorem for every n at once.
  * If c_max depends on which H, the lemma needs a stronger hypothesis, and the
    module says so instead of pretending.

Run: python lab/step_lemma.py -> results/step_lemma.json
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jacobi_normal_form import _fact, poch, sign_of  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def all_positive(poly: list[F], D: F, upto: int | None = None) -> bool:
    """Are all (-1)^m x (m-th Jacobi coefficient) strictly positive?

    upto defaults to deg(poly), i.e. every m that the physical problem uses
    (m runs 0..n-2 while deg F = n-1).
    """
    a, b = F(-1, 2), F(D, 2) - 2
    top = len(poly) - 1 if upto is None else upto
    for m in range(top):
        pref = poch(a + 1, m) / F(_fact(m))
        tot = F(0)
        for k in range(m + 1):
            ck = poch(F(-m), k) * poch(F(m) + a + b + 1, k) / (poch(a + 1, k) * F(_fact(k)))
            if ck == 0:
                continue
            inner = F(0)
            for lpow, fl in enumerate(poly):
                if fl:
                    inner += fl * poch(a + 1, k + lpow) / poch(a + b + 2, k + lpow)
            tot += ck * inner
        if sign_of(F(-1) ** m * pref * tot) <= 0:
            return False
    return True


def mul_square(p: list[F], c: F) -> list[F]:
    """p(u) * (u - c)^2."""
    for _ in range(2):
        q = [F(0)] * (len(p) + 1)
        for k, x in enumerate(p):
            q[k] += -c * x
            q[k + 1] += x
        p = q
    return p


def c_max(H: list[F], D: F, iters: int = 14) -> F | None:
    """Largest c keeping all-positivity, by bisection on (0, 1)."""
    lo, hi = F(0), F(1)
    if not all_positive(mul_square(H, F(1, 10000)), D):
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2
        if all_positive(mul_square(H, mid), D):
            lo = mid
        else:
            hi = mid
    return lo


def ladder(n: int, lam: F, count: int | None = None) -> tuple[list[F], list[F]]:
    """(partial product of the first `count` ladder factors, the ladder roots)."""
    s = F(lam) + n - 1
    aa = sorted([n - 2 * k for k in range(1, n) if n - 2 * k > 0])
    roots = [F(a * a, 1) / s**2 for a in aa]
    eps = 1 if n % 2 == 0 else 0
    p = [F(0)] * eps + [F(1)]
    for c in roots[: count if count is not None else len(roots)]:
        p = mul_square(p, c)
    return p, roots


def main() -> int:
    t0 = time.time()
    out: dict = {"same_degree_different_H": [], "ladder_vs_threshold": []}

    # (1) does the threshold depend on WHICH H, at fixed degree and beta?
    print("(1) same degree, different H -- is c_max a function of degree alone?", flush=True)
    for t in (2, 3, 4, 5, 6):
        for D in (F(6), F(11)):
            row = {"t": t, "D": str(D), "cases": []}
            cases = [
                ("ladder n=15 lam=1", ladder(15, F(1), t)[0]),
                ("ladder n=21 lam=1", ladder(21, F(1), t)[0]),
                ("ladder n=21 lam=7", ladder(21, F(7), t)[0]),
                ("ladder n=31 lam=1", ladder(31, F(1), t)[0]),
            ]
            # a deliberately different root set of the same size: geometric
            g = [F(1, 3 ** (k + 2)) for k in range(t)]
            p = [F(1)]
            for c in sorted(g):
                p = mul_square(p, c)
            cases.append(("geometric roots", p))
            for name, H in cases:
                if not all_positive(H, D):
                    row["cases"].append(
                        {"H": name, "c_max": None, "note": "H itself not all-positive"}
                    )
                    continue
                cm = c_max(H, D)
                row["cases"].append(
                    {"H": name, "degree": len(H) - 1, "c_max": float(cm) if cm else None}
                )
            spread = [c["c_max"] for c in row["cases"] if c.get("c_max")]
            row["spread"] = (max(spread) - min(spread)) if len(spread) > 1 else None
            out["same_degree_different_H"].append(row)
            shown = ", ".join(
                f"{c['H'].split()[0][:4] + str(c.get('degree', ''))}={c['c_max']:.4f}"
                for c in row["cases"]
                if c.get("c_max")
            )
            print(
                f"   t={t} D={str(D):<3s}  c_max: {shown}   spread {row['spread'] or 0.0:.4f}",
                flush=True,
            )

    # (2) the ladder against its own threshold, for several n
    print(flush=True)
    print("(2) does the real ladder ever reach the threshold?", flush=True)
    for n in (15, 21, 31, 41):
        for lam, D in ((F(1), F(6)), (F(1), F(11)), (F(7), F(6))):
            _, roots = ladder(n, lam)
            H = [F(0)] * (1 if n % 2 == 0 else 0) + [F(1)]
            worst = None
            for t, c in enumerate(roots):
                cm = c_max(H, D)
                if cm is None:
                    worst = ("H not extendable", t)
                    break
                ratio = float(cm / c)
                if worst is None or ratio < worst[0]:
                    worst = (ratio, t)
                H = mul_square(H, c)
            ok = all_positive(H, D)
            out["ladder_vs_threshold"].append(
                {
                    "n": n,
                    "lam": str(lam),
                    "D": str(D),
                    "worst_margin_ratio": worst[0] if worst else None,
                    "at_step": worst[1] if worst else None,
                    "full_product_all_positive": ok,
                }
            )
            print(
                f"   n={n:2d} lam={str(lam):<2s} D={str(D):<3s} worst margin "
                f"{worst[0]:.3f}x at step {worst[1]}   full product all-positive: {ok}",
                flush=True,
            )

    out.update(
        {
            "lemma_under_test": "if H is all-positive and c <= c_max(H, beta) then"
            " H(u)(u-c)^2 is all-positive; the question is"
            " whether c_max depends on H only through its degree",
            "command": "python lab/step_lemma.py",
            **stamp(),
            "runtime_s": round(time.time() - t0, 1),
        }
    )
    (RES / "step_lemma.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("\nwritten results/step_lemma.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
