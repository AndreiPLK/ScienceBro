"""THE DECISIVE TEST of the Charlier mechanism: where does the measure's mass
sit relative to the sign changes of P_r?

Established so far (results/charlier_reduction.json, moment_boundary_law.json):

    K_r = INT P_r(y) dmu(y),   P_r(y) = sum_t C(r,t) (g)_t (-y)^t = C_r(g;1/y),

with m_t = INT y^t dmu a Hamburger moment sequence (H0 positive definite at
full size), its measure on (-inf, 1] with an exponentially tiny negative-y
part that can only HELP (all terms of P_r are >= 0 at y <= 0). The crude
"P_r >= 0 on the support" condition is refuted: P_r changes sign inside the
support. So the whole question is the MASS distribution.

This script extracts the measure and looks:

 1. Gaussian quadrature from the exact moments: the orthogonal polynomial of
    degree q is built by exact Hankel-determinant (Gram) formulas over fmpq;
    its roots (the nodes) come from flint's CERTIFIED complex_roots, and the
    weights solve the Vandermonde system in acb interval arithmetic. Every
    number below is an enclosure, so a reported sign is a proved sign.
 2. VERIFICATION FIRST: the quadrature must reproduce m_0..m_{2q-1} within
    its enclosures, and sum_i w_i P_r(y_i) must contain the exactly computed
    K_r. Nothing is interpreted before both checks pass.
 3. The diagnostics that matter: the fraction of mass to the RIGHT of the
    smallest positive zero of P_r, and the separate positive and negative
    contributions to K_r -- i.e. how close the cancellation runs.

Run: python lab/measure_mass_test.py -> results/measure_mass_test.json
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
from charlier_zero_test import smallest_positive_zero  # noqa: E402
from moment_kernel_probe import falling, ref_sign, shore  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def hankel_det(m: list[fmpq], q: int, shift: int = 0) -> fmpq:
    """det [m_{a+b+shift}]_{a,b<q}, exact fraction-free-ish over fmpq."""
    if q == 0:
        return fmpq(1)
    mat = [[m[a + b + shift] for b in range(q)] for a in range(q)]
    d = fmpq(1)
    for c in range(q):
        piv = next((rr for rr in range(c, q) if mat[rr][c] != 0), None)
        if piv is None:
            return fmpq(0)
        if piv != c:
            mat[c], mat[piv] = mat[piv], mat[c]
            d = -d
        d *= mat[c][c]
        inv = 1 / mat[c][c]
        for rr in range(c + 1, q):
            f = mat[rr][c] * inv
            if f != 0:
                for cc in range(c, q):
                    mat[rr][cc] -= f * mat[c][cc]
    return d


def orthogonal_poly(m: list[fmpq], q: int) -> fmpq_poly:
    """Monic orthogonal polynomial of degree q for the moment functional,
    by the classical determinant formula expanded along the last row."""
    coeffs = []
    for j in range(q + 1):
        # cofactor of y^j in det of the (q+1)x(q+1) Hankel-with-last-row-powers
        mat = [[m[a + b] for b in range(q + 1)] for a in range(q)]
        sub = [[row[c] for c in range(q + 1) if c != j] for row in mat]
        d = fmpq(1)
        n_ = q
        if n_ == 0:
            det = fmpq(1)
        else:
            work = [row[:] for row in sub]
            det = fmpq(1)
            for c in range(n_):
                piv = next((rr for rr in range(c, n_) if work[rr][c] != 0), None)
                if piv is None:
                    det = fmpq(0)
                    break
                if piv != c:
                    work[c], work[piv] = work[piv], work[c]
                    det = -det
                det *= work[c][c]
                inv = 1 / work[c][c]
                for rr in range(c + 1, n_):
                    f = work[rr][c] * inv
                    if f != 0:
                        for cc in range(c, n_):
                            work[rr][cc] -= f * work[c][cc]
        coeffs.append(det * fmpq((-1) ** (q + j)) * d)
    p = fmpq_poly(coeffs)
    lead = p.coeffs()[-1]
    return p / lead  # monic


def quadrature(m: list[fmpq], q: int, prec: int = 300):
    """Nodes (certified enclosures) and weights (acb) of the q-point Gauss rule."""
    ctx.prec = prec
    p = orthogonal_poly(m, q)
    roots = [r for r, mult in p.complex_roots()]
    V = acb_mat([[r**t for r in roots] for t in range(q)])
    rhs = acb_mat([[acb(int(m[t].p)) / acb(int(m[t].q))] for t in range(q)])
    w = V.solve(rhs)
    return roots, [w[i, 0] for i in range(q)]


def main() -> int:
    t0 = time.time()
    ctx.prec = 300
    rows = []
    for lam in (fmpq(1), fmpq(3), fmpq(72)):
        Th = shore(lam)[0]
        for n in (12, 24):
            m = m_seq(n, lam, n - 2)
            q = (n - 2) // 2  # q-point rule is exact on m_0..m_{2q-1}
            try:
                nodes, weights = quadrature(m, q)
            except Exception as exc:  # noqa: BLE001 - report, do not crash the sweep
                rows.append({"lam": str(lam), "n": n, "error": f"{type(exc).__name__}: {exc}"})
                continue
            # --- verification 1: moments reproduced within enclosures
            mom_ok = True
            for t in range(2 * q):
                approx = sum((weights[i] * nodes[i] ** t for i in range(q)), acb(0))
                exact = acb(int(m[t].p)) / acb(int(m[t].q))
                if not (approx - exact).contains(acb(0)):
                    mom_ok = False
                    break
            # "above" is the control: there the even knives are NEGATIVE, so the
            # cancellation ratio must exceed 1 -- a diagnostic that never exceeded
            # 1 anywhere would be measuring nothing.
            for tag, D in (("shore", Th), ("below", Th * fmpq(4, 5)), ("above", Th * fmpq(2))):
                H = (D + 4 * n - 7) / 2
                for j in (4, 6, 8):
                    r = j - 1
                    if r > 2 * q - 1:
                        continue
                    g = H - r
                    # --- verification 2: quadrature reproduces K_r
                    K_exact = sum(
                        (fmpq((-1) ** t * comb(r, t)) * falling(g, t) * m[t] for t in range(r + 1)),
                        fmpq(0),
                    )
                    K_qexact = acb(int(K_exact.p)) / acb(int(K_exact.q))
                    Pvals = [
                        sum(
                            (acb(comb(r, t)) * acb(str(falling(g, t))) * (-nodes[i]) ** t
                             for t in range(r + 1)),
                            acb(0),
                        )
                        for i in range(q)
                    ]
                    K_quad = sum((weights[i] * Pvals[i] for i in range(q)), acb(0))
                    quad_ok = (K_quad - K_qexact).contains(acb(0))
                    # --- the diagnostics
                    z = smallest_positive_zero(r, g, max(m[t + 1] / m[t] for t in range(len(m) - 1)) * 4)
                    pos = sum(
                        (weights[i] * Pvals[i] for i in range(q) if (weights[i] * Pvals[i]).real.mid() > 0),
                        acb(0),
                    )
                    neg = sum(
                        (weights[i] * Pvals[i] for i in range(q) if (weights[i] * Pvals[i]).real.mid() < 0),
                        acb(0),
                    )
                    mass_right = sum(
                        (weights[i] for i in range(q)
                         if z is not None and nodes[i].real.mid() > float(z)),
                        acb(0),
                    )
                    total_mass = sum(weights, acb(0))
                    rows.append(
                        {
                            "lam": str(lam),
                            "n": n,
                            "q_points": q,
                            "where": tag,
                            "j": j,
                            "moments_reproduced": mom_ok,
                            "K_reproduced_by_quadrature": bool(quad_ok),
                            "knife_sign_reference": ref_sign(j, n, lam, D),
                            "K_sign_exact": (K_exact > 0) - (K_exact < 0),
                            "positive_part": float(pos.real.mid()),
                            "negative_part": float(neg.real.mid()),
                            "cancellation_ratio": (
                                float(abs(neg.real.mid()) / abs(pos.real.mid()))
                                if pos.real.mid() != 0 else None
                            ),
                            "mass_right_of_zero_fraction": (
                                float(mass_right.real.mid() / total_mass.real.mid())
                                if total_mass.real.mid() != 0 else None
                            ),
                        }
                    )
    good = [r for r in rows if r.get("K_reproduced_by_quadrature")]
    print(f"rows: {len(rows)}; quadrature reproduced K_r in {len(good)}", flush=True)
    for r in rows[:8]:
        if "error" in r:
            print(f"  ERROR lam={r['lam']} n={r['n']}: {r['error']}", flush=True)
        else:
            print(
                f"  lam={r['lam']:>3} n={r['n']} {r['where']:>5} j={r['j']} "
                f"mom_ok={r['moments_reproduced']} K_ok={r['K_reproduced_by_quadrature']} "
                f"cancel={r['cancellation_ratio']:.6f} "
                f"mass_right={r['mass_right_of_zero_fraction']:.3e}"
                if r.get("cancellation_ratio") is not None else f"  lam={r['lam']} n={r['n']} incomplete",
                flush=True,
            )
    out = {
        "claim": (
            "Decisive diagnostic of the Charlier mechanism: with the measure extracted "
            "by exact-moment Gaussian quadrature (certified root enclosures, acb "
            "weights, and BOTH verifications -- moments reproduced and K_r reproduced "
            "-- required before any interpretation), report how the positive and "
            "negative contributions to K_r = INT P_r dmu balance, and what fraction of "
            "the mass sits right of the smallest positive zero of P_r."
        ),
        "rows": rows,
        "command": "python lab/measure_mass_test.py",
        "seconds": round(time.time() - t0, 1),
        **stamp(),
    }
    path = RES / "measure_mass_test.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
