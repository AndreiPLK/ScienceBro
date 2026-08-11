# Upstream inspection: AInstein blackhole branch

Date: 2026-08-11
Commit: `54736e466e54d948bd509b072e4047cf98405064` (HEAD of `blackhole`, matches pin)
Checkout: `projects/ainstein-audit/upstream/checkout/` (gitignored; re-clone with the
command in this file).

```
git clone --branch blackhole https://github.com/xand-stapleton/ainstein projects/ainstein-audit/upstream/checkout
git -C projects/ainstein-audit/upstream/checkout checkout 54736e466e54d948bd509b072e4047cf98405064
```

## Facts (inspected, not assumed)

- **Framework: TensorFlow** (tf_keras/keras; NOT PyTorch). `dtype: float64` in configs.
- Python `>=3.12`; setuptools build; deps include tensorflow, tensorflow-probability, wandb.
- **License discrepancy**: repo `LICENSE` file is GPL-2.0, `pyproject.toml` says `license = "MIT"`.
  Recorded as an open question for the authors; until resolved we do NOT copy code out
  of the checkout (reading + running in place is fine).
- Entry point: `python run.py -c=<config>`; README references `hyperparameters/hps.yaml`
  which **does not exist**; actual configs:
  - `hps_local_lorentzian.yaml` (dim 2, 100 epochs, 10k samples) — smallest run;
  - `hps_schwarzschild.yaml` (500 epochs) — known-answer baseline training;
  - `hps_petrovI_vacuum.yaml`, `hps_petrovI_bh.yaml` — the novel-candidate searches;
  - `hps_sphere.yaml` (Riemannian legacy).
- `seed_models/` ships pre-trained supervised initialisation models: `AL_embed.keras`,
  `IL_embed.keras` (used for published results per README).
- Losses: vacuum Einstein residual, quadratic Weyl constraint, SO(3)/Killing symmetry,
  Petrov speciality index, horizon curvature anchor, trapped-surface constraint
  (matches the paper abstract).
- Testing/visualisation happens in `notebooks/examine_output_*.ipynb`; **no published
  trained candidate checkpoints** are in the repo (only supervised seed models) —
  candidates must be re-trained locally or requested from authors. This is a potential
  reproducibility blocker; recorded.
- Windows note: native Windows TensorFlow ≥2.11 is CPU-only; GPU would need WSL2.
  CPU is acceptable for the smallest baseline; longer training may need WSL2/Linux.

## Isolation

Separate uv-managed venv in `projects/ainstein-audit/upstream/` (`.venv-upstream`,
gitignored). ScienceBro core never imports from the checkout; the future validator
consumes only exported metric values through a documented interface.
