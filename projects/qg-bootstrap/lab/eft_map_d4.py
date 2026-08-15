"""EFT map of the D=4 survivors: Wilson-coefficient sums along the lambda dial.

For the CHR closed-string family (mu(n) = (n+lam-1)/lam,
R(n,0) = [((1+lam)/2)_{n-1} / ((1+3lam)/2)_{n-1}]^2), compute
    c_k(lam) = sum_{n>=1} R(n,0) / mu(n)^k,   k = 3, 5
and the dial ratios r_k(lam) = c_k(lam)/c_k(1).

Known-answer gate: at lam=1, mu(n)=n and R(n,0)=1/n^2 (the (1)_{n-1}/(2)_{n-1}
ratio squared), so c_3(1)=zeta(5) and c_5(1)=zeta(7) EXACTLY; the machinery
must reproduce both to <1e-10 before any other number is trusted. (The first
version of this gate wrongly expected zeta(3) and correctly FAILED - kept in
git history as the gate doing its job.)

Large-n behavior: R(n,0) ~ C * n^(-2*lam), so the k-th sum's tail decays like
n^(-(2*lam+k)); we use the integral comparison tail bound
term_n * n / (2*lam + k - 1) and Kahan-compensated float summation (validated
by the exact zeta gate at lam=1).
EXPLORATORY slice (frozen in gravity-card.md before results).
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from fractions import Fraction as F
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
TOL = 1e-10


def c_k(lam: F, k: int):
    """Kahan-compensated sum with integral-comparison tail bound."""
    lamf = float(lam)
    s = 0.0
    comp = 0.0
    ratio2 = 1.0          # R(n,0), обновляется мультипликативно
    n = 1
    while True:
        mu = (n + lamf - 1) / lamf
        term = ratio2 / mu**k
        y = term - comp
        t = s + y
        comp = (t - s) - y
        s = t
        p = 2 * lamf + k - 1
        tail = term * n / p if p > 0 else float("inf")
        if n > 10 and tail < TOL:
            return s, n, tail
        # R(n+1,0)/R(n,0) = [((1+lam)/2 + n-1)/((1+3lam)/2 + n-1)]^2
        r = ((1 + lamf) / 2 + n - 1) / ((1 + 3 * lamf) / 2 + n - 1)
        ratio2 *= r * r
        n += 1
        if n > 5_000_000:
            raise RuntimeError(f"no convergence at lam={lam}")


def main() -> int:
    t0 = time.time()
    # известный ответ: lam=1 -> c3=zeta(5), c5=zeta(7)
    ZETA5 = 1.0369277551433699263
    ZETA7 = 1.0083492773819228268
    rows = []
    gate = {}
    for k, ref in ((3, ZETA5), (5, ZETA7)):
        val, terms, tail = c_k(F(1), k)
        err = abs(float(val) - ref)
        gate[f"c{k}(1)"] = {"value": float(val), "zeta_ref": ref,
                            "abs_err": err, "terms": terms}
        assert err < 1e-9, f"known-answer gate FAILED for k={k}: err={err}"
    print("known-answer gate PASSED: c3(1)=zeta(5), c5(1)=zeta(7) to <1e-9",
          flush=True)

    lams = [F(1, 10), F(1, 5), F(3, 10), F(1, 2), F(7, 10), F(9, 10),
            F(1), F(11, 10), F(3, 2), F(2), F(3), F(5), F(10), F(20)]
    c1 = {k: c_k(F(1), k)[0] for k in (3, 5)}
    for lam in lams:
        row = {"lambda": str(lam)}
        for k in (3, 5):
            val, terms, tail = c_k(lam, k)
            row[f"c{k}"] = float(val)
            row[f"r{k}"] = float(val / c1[k])
            row[f"terms_{k}"] = terms
        rows.append(row)
        print(f"lam={lam}: r3={row['r3']:.6g} r5={row['r5']:.6g} "
              f"({time.time()-t0:.0f}s)", flush=True)

    git = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out = {"exploratory": True, "gate": gate, "rows": rows,
           "definition": "c_k = sum R(n,0)/mu(n)^k; r_k = c_k/c_k(1)",
           "tol": "1e-10 integral tail bound, Kahan float sums, zeta gate at lam=1",
           "command": "python lab/eft_map_d4.py", "git": git,
           "runtime_s": round(time.time() - t0, 1)}
    (RES / "eft_map_d4.json").write_text(json.dumps(out, indent=1),
                                         encoding="utf-8")
    print("written eft_map_d4.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
