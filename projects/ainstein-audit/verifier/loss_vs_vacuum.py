"""Does the reported training loss track independently measured vacuum quality?

Five seeds is a small sample, so this script exists to make the number checkable rather
than to settle the question: it writes the rank and linear correlations together with an
explicit caveat about n = 5.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

PROJ = Path(__file__).resolve().parents[1]
SWEEP = PROJ / "results" / "processed" / "seed_sweep.json"
OUT = PROJ / "results" / "processed" / "loss_vs_vacuum.json"

# final training loss per seed, read from the preserved training logs
FINAL_LOSS = {123: 0.0111, 124: 0.0118, 125: 0.0110, 126: 0.0132, 127: 0.0109}


def main() -> int:
    sweep = json.loads(SWEEP.read_text(encoding="utf-8"))
    rows = sorted(sweep["rows"], key=lambda r: r["seed"])
    losses = [FINAL_LOSS[r["seed"]] for r in rows]
    vac = [r["vacuum"]["median"] for r in rows]
    s_mid = [(r["petrov"]["S_min"] + r["petrov"]["S_max"]) / 2 for r in rows]

    rho, p_rho = stats.spearmanr(losses, vac)
    r_lin, p_lin = stats.pearsonr(losses, vac)

    out = {
        "n": len(rows),
        "spearman_rho": round(float(rho), 4),
        "spearman_p_two_sided": round(float(p_rho), 4),
        "pearson_r": round(float(r_lin), 4),
        "pearson_p_two_sided": round(float(p_lin), 4),
        "vacuum_spread_factor": round(max(vac) / min(vac), 3),
        "loss_spread_factor": round(max(losses) / min(losses), 3),
        "final_losses": {str(k): v for k, v in FINAL_LOSS.items()},
        "vacuum_medians": {str(r["seed"]): r["vacuum"]["median"] for r in rows},
        "speciality_index_relative_std_percent": round(
            float(np.std(s_mid) / np.mean(s_mid) * 100), 3
        ),
        "caveat": "n = 5. A rank correlation of this magnitude at n = 5 sits at the edge of "
        "significance, so this is reported as suggestive and not as an established "
        "relationship. It is stated because it is cheap for anyone to test with more "
        "seeds and because it is the failure mode an external instrument exists to catch.",
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
