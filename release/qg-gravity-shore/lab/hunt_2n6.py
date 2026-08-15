"""Hunt for the a_{n,2n-6} knife inside the conjectured model boundary.
Persisted lab version of the 2026-08-15 inline hunt (same logic, same output).
Run: .venv/Scripts/python.exe -u projects/qg-bootstrap/lab/hunt_2n6.py
Output: results/hunt_2n6.json (list of alarms; empty = clean)."""
from __future__ import annotations
import json, sys, time
from fractions import Fraction as F
from math import comb
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import gegen_coeffs, mono_int
RES = Path(__file__).resolve().parents[1] / "results"

def a_l(n, l, lam, D):
    mu = (n + lam - 1) / lam
    A = lam * mu / 2
    poly = [F(1)]
    for k in range(1, n):
        b = (1 + lam) / 2 + (k - 1) - A
        new = [F(0)] * (len(poly) + 1)
        for i, c in enumerate(poly):
            new[i] += c * b
            new[i + 1] += c * A
        poly = new
    P = [F(0)] * (2 * len(poly) - 1)
    for i, a_ in enumerate(poly):
        for j, b_ in enumerate(poly):
            P[i + j] += a_ * b_
    mW = (D - 4) // 2
    w = [F(0)] * (2 * mW + 1)
    for j in range(mW + 1):
        w[2 * j] = F((-1) ** j * comb(mW, j))
    Pw = [F(0)] * (len(P) + len(w) - 1)
    for i, c in enumerate(P):
        if c == 0:
            continue
        for jw, cw in enumerate(w):
            if cw:
                Pw[i + jw] += c * cw
    cl = gegen_coeffs(l, D - 3)
    b = F(0)
    for i, ci in enumerate(cl):
        if ci == 0:
            continue
        for k2, ck in enumerate(Pw):
            if ck:
                b += ci * ck * mono_int(i + k2)
    return b

def minT(lamf):
    return min((3 * (2 * n - 3) / (n * (n - 2))) * (lamf * lamf + (2 * n - 2) * lamf + 1) + 2 * n
               for n in range(3, 300))

def main():
    import subprocess
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    alarms = []
    lams = [F(i, 10) for i in range(1, 31)] + [F(4), F(5), F(7), F(10)]
    t0 = time.time()
    for lam in lams:
        Dtop = int(minT(float(lam)))
        for D in range(max(4, Dtop - 3), Dtop + 1):
            if D % 2:
                continue
            for n in range(4, 15):
                if a_l(n, 2 * n - 6, lam, D) < 0:
                    alarms.append({"lam": str(lam), "D": D, "n": n})
                    break
        print(f"lam={lam} ok ({time.time()-t0:.0f}s)", flush=True)
    out = {"alarms": alarms, "n_lambdas": len(lams), "n_range": "4..14",
           "window": "[minT-3, minT] even D", "git": commit}
    (RES / "hunt_2n6.json").write_text(json.dumps(out, indent=1))
    print(f"DONE: {len(alarms)} alarms")
    return 0

if __name__ == "__main__":
    sys.exit(main())
