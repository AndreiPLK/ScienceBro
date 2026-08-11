# Experiment contract (binding)

- Freeze hypothesis and primary metric BEFORE examining final results.
- Preserve raw outputs as immutable artifacts under results/raw/ (never rewrite).
- Every run records: git commit, uv.lock hash, command, seed, hardware, precision, runtime.
- Exploratory and confirmatory analysis are separated (`exploratory: true` flag).
- Never select only successful seeds or visually attractive runs.
- Every experiment includes a negative control and a known-answer baseline.
- Numerical claims require convergence checks (resolution / tolerance / precision).
- Failures near boundaries, horizons, singularities are mapped explicitly.
- A run completing without an exception is NOT scientific validation.
