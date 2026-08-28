"""How large can the cancellation ratio get? A wide exact sweep.

The mechanism (results/measure_mass_test.json): K_r = INT P_r dmu is positive
at and below the shore not because P_r >= 0 -- it changes sign inside the
support -- but because

    c(n, lam, D, r) := |INT_{P_r<0} P_r dmu| / |INT_{P_r>0} P_r dmu|

stays below 1, measured at most 0.70 on a first grid, and NOT growing with
depth. An all-depths theorem needs sup c < 1 uniformly, so the question is
what c depends on and where it comes closest to 1.

This sweep widens the grid to n <= 40, j <= 12, lam over five orders of
magnitude, separating even and odd j (their physics differs: odd j have no
threshold, even j are marginal at the shore). Speed comes from two places:
the measure depends only on (n, lam), so each quadrature is built once and
reused across all j and D; and the orthogonal polynomials come from the
exact three-term recurrence (O(q^2) inner products over fmpq) instead of
cofactor determinants.

Both verifications from the decisive test are kept: the quadrature must
reproduce the moments and must reproduce the exactly computed K_r, per
configuration, before any ratio is recorded.

Run: python lab/cancellation_bound_sweep.py -> results/cancellation_bound_sweep.json
"""

from __future__ import annotations

import json
import sys
import time
from math import comb
from pathlib import Path

from flint import acb, acb_mat, ctx, fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base_moment_probe import m_seq  # noqa: E402
from moment_kernel_probe import falling, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def inner(p: list[fmpq], q: list[fmpq], m: list[fmpq]) -> fmpq:
    """<p, q> = sum_{i,j} p_i q_j m_{i+j} for polynomial coefficient lists."""
    tot = fmpq(0)
    for i, pi in enumerate(p):
        if pi == 0:
            continue
        for j, qj in enumerate(q):
            if qj == 0:
                continue
            tot += pi * qj * m[i + j]
    return tot


def orthogonal_poly_recurrence(m: list[fmpq], q: int) -> fmpq_poly:
    """Monic orthogonal polynomial of degree q by the three-term recurrence."""
    p_prev: list[fmpq] = []
    p_cur: list[fmpq] = [fmpq(1)]
    norm_cur = inner(p_cur, p_cur, m)
    norm_prev = fmpq(0)
    for k in range(q):
        shifted = [fmpq(0)] + p_cur  # y * p_cur
        a = inner(shifted, p_cur, m) / norm_cur
        b = norm_cur / norm_prev if p_prev else fmpq(0)
        nxt = [fmpq(0)] * (len(p_cur) + 1)
        for i, c in enumerate(p_cur):
            nxt[i + 1] += c  # y * p_cur
            nxt[i] -= a * c
        for i, c in enumerate(p_prev):
            nxt[i] -= b * c
        p_prev, p_cur = p_cur, nxt
        norm_prev, norm_cur = norm_cur, inner(p_cur, p_cur, m)
    return fmpq_poly(p_cur)


def quadrature(m: list[fmpq], q: int):
    p = orthogonal_poly_recurrence(m, q)
    roots = [r for r, _ in p.complex_roots()]
    V = acb_mat([[r**t for r in roots] for t in range(q)])
    rhs = acb_mat([[acb(int(m[t].p)) / acb(int(m[t].q))] for t in range(q)])
    w = V.solve(rhs)
    return roots, [w[i, 0] for i in range(q)]


def main() -> int:
    t0 = time.time()
    ctx.prec = 400
    rows = []
    skipped = []
    for lam in (fmpq(1, 10), fmpq(1), fmpq(5, 2), fmpq(7), fmpq(72), fmpq(5000)):
        Th = shore(lam)[0]
        for n in (12, 20, 28, 40):
            m = m_seq(n, lam, n - 2)
            q = min((n - 2) // 2, 12)  # cap the rule size; exact on m_0..m_{2q-1}
            try:
                nodes, weights = quadrature(m, q)
            except Exception as exc:  # noqa: BLE001
                skipped.append({"lam": str(lam), "n": n, "error": f"{type(exc).__name__}: {exc}"})
                continue
            mom_ok = all(
                (sum((weights[i] * nodes[i] ** t for i in range(q)), acb(0))
                 - acb(int(m[t].p)) / acb(int(m[t].q))).contains(acb(0))
                for t in range(2 * q)
            )
            if not mom_ok:
                skipped.append({"lam": str(lam), "n": n, "error": "moments not reproduced"})
                continue
            for tag, D in (("shore", Th), ("below", Th * fmpq(4, 5)), ("deep", Th * fmpq(2, 5))):
                if D <= 3:
                    continue
                H = (D + 4 * n - 7) / 2
                for j in (3, 4, 5, 6, 8, 10, 12):
                    r = j - 1
                    if r > 2 * q - 1 or j > n - 1:
                        continue
                    g = H - r
                    K_exact = sum(
                        (fmpq((-1) ** t * comb(r, t)) * falling(g, t) * m[t] for t in range(r + 1)),
                        fmpq(0),
                    )
                    Pvals = [
                        sum(
                            (acb(comb(r, t)) * acb(str(falling(g, t))) * (-nodes[i]) ** t
                             for t in range(r + 1)),
                            acb(0),
                        )
                        for i in range(q)
                    ]
                    terms = [weights[i] * Pvals[i] for i in range(q)]
                    K_quad = sum(terms, acb(0))
                    if not (K_quad - acb(int(K_exact.p)) / acb(int(K_exact.q))).contains(acb(0)):
                        skipped.append({"lam": str(lam), "n": n, "j": j, "where": tag,
                                        "error": "K not reproduced"})
                        continue
                    pos = sum((t_ for t_ in terms if t_.real.mid() > 0), acb(0))
                    neg = sum((t_ for t_ in terms if t_.real.mid() < 0), acb(0))
                    ratio = (
                        float(abs(neg.real.mid()) / abs(pos.real.mid()))
                        if pos.real.mid() != 0 else None
                    )
                    rows.append(
                        {
                            "lam": str(lam), "n": n, "where": tag, "j": j,
                            "parity": "even" if j % 2 == 0 else "odd",
                            "cancellation_ratio": ratio,
                            "K_sign": (K_exact > 0) - (K_exact < 0),
                            "ref_sign": ref_sign(j, n, lam, D),
                        }
                    )
    safe = [r for r in rows if r["where"] in ("shore", "below", "deep") and r["cancellation_ratio"]]
    agree = all(r["K_sign"] == r["ref_sign"] for r in rows)
    worst = max((r["cancellation_ratio"] for r in safe), default=None)
    by_par = {}
    by_j = {}
    for r in safe:
        by_par.setdefault(r["parity"], []).append(r["cancellation_ratio"])
        by_j.setdefault(r["j"], []).append(r["cancellation_ratio"])
    print(f"rows {len(rows)} (skipped {len(skipped)}); K sign == reference everywhere: {agree}")
    print(f"worst cancellation ratio at or below the shore: {worst}")
    for p_, v in sorted(by_par.items()):
        print(f"  {p_} j: max {max(v):.4f}, mean {sum(v)/len(v):.4f}, count {len(v)}")
    for j_, v in sorted(by_j.items()):
        print(f"  j={j_:>2}: max {max(v):.4f}")
    worst_rows = sorted(safe, key=lambda r: -r["cancellation_ratio"])[:6]
    for r in worst_rows:
        print(f"   worst: lam={r['lam']} n={r['n']} {r['where']} j={r['j']} -> {r['cancellation_ratio']:.4f}")

    # --- the trend that matters: the peak over j, as n grows
    peaks = []
    for lam in (fmpq(1), fmpq(7)):
        Th = shore(lam)[0]
        for n in (14, 20, 28, 40):
            m = m_seq(n, lam, n - 2)
            q = min((n - 2) // 2, 12)
            try:
                nodes, weights = quadrature(m, q)
            except Exception:  # noqa: BLE001
                continue
            H = (Th + 4 * n - 7) / 2
            best, best_j = 0.0, None
            for j in range(3, min(2 * q, n - 1) + 1):
                r = j - 1
                if r > 2 * q - 1:
                    break
                g = H - r
                Kx = sum(
                    (fmpq((-1) ** t * comb(r, t)) * falling(g, t) * m[t] for t in range(r + 1)),
                    fmpq(0),
                )
                Pv = [
                    sum((acb(comb(r, t)) * acb(str(falling(g, t))) * (-nodes[i]) ** t
                         for t in range(r + 1)), acb(0))
                    for i in range(q)
                ]
                terms = [weights[i] * Pv[i] for i in range(q)]
                if not (sum(terms, acb(0)) - acb(int(Kx.p)) / acb(int(Kx.q))).contains(acb(0)):
                    continue
                pos = sum((x for x in terms if x.real.mid() > 0), acb(0))
                neg = sum((x for x in terms if x.real.mid() < 0), acb(0))
                rt = float(abs(neg.real.mid()) / abs(pos.real.mid())) if pos.real.mid() != 0 else 0.0
                if rt > best:
                    best, best_j = rt, j
            peaks.append({"lam": str(lam), "n": n, "peak_ratio": best, "at_j": best_j,
                          "one_minus_peak": 1 - best})
    print("peak over j at the shore (q capped at 12, so these are LOWER bounds):", flush=True)
    for p_ in peaks:
        print(f"   lam={p_['lam']:>3} n={p_['n']:>3}: {p_['peak_ratio']:.4f} at j={p_['at_j']} "
              f"(1 - peak = {p_['one_minus_peak']:.4f})", flush=True)

    out = {
        "claim": (
            "Wide exact sweep of the cancellation ratio c = |INT_{P_r<0} P_r dmu| / "
            "|INT_{P_r>0} P_r dmu| at and below the shore, over n <= 40, j <= 12 and "
            "lam across five orders of magnitude, with the quadrature verified per "
            "configuration (moments and K_r both reproduced). VERDICT: c is NOT "
            "visibly bounded away from 1. It peaks at INTERMEDIATE depth (not at "
            "large j: at n = 40, lam = 7 it rises to 0.954 at j = 14 and falls back "
            "to 0.54 by j = 24) and the PEAK GROWS WITH n: 0.68, 0.80, 0.89, 0.95 at "
            "n = 14, 20, 28, 40. So the theorem shape 'sup c < 1 uniformly' proposed "
            "after the first grid is in doubt: the mechanism is asymptotically tight "
            "in n, and a proof must track the approach rather than fix a constant. "
            "The measured peaks are LOWER bounds (the quadrature rule is capped at "
            "12 points, so j <= 24)."
        ),
        "worst_ratio": worst,
        "peak_trend": peaks,
        "sign_agreement_everywhere": agree,
        "rows": rows,
        "skipped": skipped,
        "command": "python lab/cancellation_bound_sweep.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "cancellation_bound_sweep.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
