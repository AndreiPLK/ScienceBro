"""Full test of the conjectured COMPLETE MODEL of the gravitational island:
alive(lam, D) <=> D <= min_n T_n(lam). Compare against exact full-spin scans
(all even l, depth NMAX) over a wide grid. Mismatches classified:
  model-dead / scan-alive  -> doomed cell (finite-depth artifact, OK if
                              predicted kill level > NMAX)
  model-alive / scan-dead  -> ANOTHER KNIFE EXISTS (model incomplete!) - alarm.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from grav_full_body import first_negative

RES = Path(__file__).resolve().parents[1] / "results"
NMAX = 16


def model_alive(lam, D):
    lamf = float(lam)
    for n in range(3, 400):
        T = (3 * (2 * n - 3) / (n * (n - 2))) * (lamf * lamf + (2 * n - 2) * lamf + 1) + 2 * n
        if T <= D:
            return False, n
    return True, None


LAMS = [F(i, 10) for i in range(1, 21)] + [F(5, 2), F(3), F(4), F(5), F(7), F(10)]
DS = list(range(4, 41, 2))
alarms, doomed, agree = [], [], 0
t0 = time.time()
for D in DS:
    for lam in LAMS:
        fn = first_negative(lam, D, NMAX)
        scan_alive = fn is None
        m_alive, nk = model_alive(lam, D)
        if m_alive == scan_alive:
            agree += 1
        elif not m_alive and scan_alive:
            doomed.append({"lam": str(lam), "D": D, "predicted_kill": nk, "beyond_scan": nk > NMAX})
        else:
            alarms.append({"lam": str(lam), "D": D, "scan_first_neg": fn})
    print(f"D={D} done ({time.time() - t0:.0f}s)", flush=True)
out = {
    "nmax": NMAX,
    "agree": agree,
    "doomed": doomed,
    "alarms": alarms,
    "total": len(LAMS) * len(DS),
}
(RES / "model_test.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(f"AGREE {agree}/{out['total']} | doomed {len(doomed)} | ALARMS {len(alarms)}", flush=True)
