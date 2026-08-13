"""Author-response upgrade: vacuum leg re-evaluated on a large hidden test set.

Dr. Hirst (email 2026-08-13): 24 hidden points is too few for statistical
statements; the paper uses 2000. This script re-runs ONLY the vacuum leg for
every available seed checkpoint with N_POINTS hidden points (default 2000),
same frozen thresholds, same evaluator, same hidden-seed derivation from the
checkpoint sha256 — nothing else changes.

FROZEN BEFORE RUNNING (2026-08-13, prior to any large-N result):
  H1: seed-124 median residual stays <= MEDIAN_LIMIT at N=2000.
  H2: seed-123 median residual stays  > MEDIAN_LIMIT at N=2000.
  Primary metric: median |R_ab| over hidden points vs frozen MEDIAN_LIMIT.

Run: .venv/Scripts/python.exe -u vacuum_deep.py   (env N_POINTS, default 2000)
Output: results/processed/vacuum_deep_N{N}.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier import known_answer_4d as ka  # noqa: E402
from verifier.candidate_stress import (  # noqa: E402
    MEDIAN_LIMIT,
    P95_LIMIT,
)
from verifier.geometry import ricci_tensor  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
OUT_DIR = PROJ / "results" / "processed"
RAW = PROJ / "results" / "raw"
H = 3e-3
N_POINTS = int(os.environ.get("N_POINTS", "2000"))
CHUNK = 100  # progress + partial medians every CHUNK points

SEEDS = {
    123: RAW / "petrovI-bh-run1",
    124: RAW / "petrovI-bh-run2",
    125: RAW / "petrovI-bh-seed125",
    126: RAW / "petrovI-bh-seed126",
    127: RAW / "petrovI-bh-seed127",
}


def hidden_points(seed: int, n: int) -> list[np.ndarray]:
    """Same distribution as candidate_stress.hidden_points_for, size n."""
    rng = np.random.default_rng(seed)
    pts: list[np.ndarray] = []
    while len(pts) < n:
        t = rng.uniform(-0.25, 0.25)
        x = rng.uniform(0.40, 0.75)
        if np.cos(2 * t) / np.cos(2 * x) <= 1.05:
            continue
        q1, q2 = rng.uniform(-0.4, 0.4, 2)
        pts.append(np.array([t, x, q1, q2]))
    return pts


def main() -> int:
    rows = []
    for seed, run_dir in SEEDS.items():
        ckpt = run_dir / "final_model.keras"
        if not ckpt.exists():
            print(f"seed {seed}: checkpoint missing, skipped", flush=True)
            continue
        sha = hashlib.sha256(ckpt.read_bytes()).hexdigest()
        hidden_seed = int(sha[:8], 16) % 2**31
        pts = hidden_points(hidden_seed, N_POINTS)
        t0 = time.time()
        residuals: list[float] = []
        sig_flags: list[bool] = []
        for i in range(0, len(pts), CHUNK):
            chunk = pts[i:i + CHUNK]
            # same primitives as candidate_stress.ricci_stats (H == bs.H frozen)
            ka.SNAPSHOT = str(ckpt)
            stencil4 = ka.stencil_for(chunk)
            pts5 = np.hstack([stencil4, np.zeros((len(stencil4), 1))])
            values = ka.export(pts5, analytic=False)
            cache = {tuple(np.round(p, 12)): values[k]
                     for k, p in enumerate(stencil4)}

            def g(x: np.ndarray) -> np.ndarray:
                return cache[tuple(np.round(x, 12))]

            for x in chunk:
                residuals.append(float(np.max(np.abs(ricci_tensor(g, x, h=H)))))
                gm = g(x)
                eig = np.linalg.eigvalsh(gm)
                sig_flags.append(bool(np.linalg.det(gm) < 0 and (eig < 0).sum() == 1))
            done = min(i + CHUNK, len(pts))
            part = float(np.median(residuals))
            print(f"seed {seed}: {done}/{len(pts)} pts, running median "
                  f"{part:.4f}, {time.time()-t0:.0f}s", flush=True)
        arr = np.array(residuals)
        med, p95, mx = (float(np.median(arr)), float(np.percentile(arr, 95)),
                        float(arr.max()))
        sig = float(np.mean(sig_flags))
        row = {"seed": seed, "model_sha256": sha[:16], "hidden_seed": hidden_seed,
               "n_points": N_POINTS,
               "median": med, "p95": p95, "max": mx, "signature_ok_fraction": sig,
               "pass_frozen": bool(med <= MEDIAN_LIMIT and p95 <= P95_LIMIT),
               "runtime_s": round(time.time() - t0, 1)}
        rows.append(row)
        print(f"seed {seed}: median={med:.4f} p95={p95:.4f} max={mx:.3g} "
              f"{'PASS' if row['pass_frozen'] else 'FAIL'} "
              f"({row['runtime_s']}s)", flush=True)

    out = {"date": "2026-08-13", "n_points": N_POINTS,
           "frozen_limits": {"median": MEDIAN_LIMIT, "p95": P95_LIMIT},
           "context": "author-response upgrade: Dr. Hirst noted 24 pts too few; "
                      "paper standard is 2000",
           "rows": rows}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"vacuum_deep_N{N_POINTS}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"written {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
