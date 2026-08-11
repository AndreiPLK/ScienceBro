# GPU через WSL2 — статус и точные команды

Проверено 2026-08-11: WSL присутствует как бинарник, но **дистрибутивов нет**
(`wsl --list` возвращает usage). GPU: RTX 4070 SUPER 12 GB, драйвер NVIDIA стоит
(nvidia-smi работает в Windows). TF ≥2.11 на native Windows — CPU-only, поэтому
тренинги кандидатов на GPU требуют WSL2.

## ТРЕБУЕТ РЕШЕНИЯ ОСНОВАТЕЛЯ

Установка WSL2 — админ-права и, возможно, перезагрузка:

```bash
wsl --install -d Ubuntu-24.04
```

(~5-10 мин + перезагрузка. Игры не пострадают: WSL2 берёт RAM/CPU по требованию,
GPU шарится с Windows.)

## После установки (готовые команды, выполню сам)

```bash
# внутри Ubuntu:
sudo apt update && sudo apt install -y python3-venv python3-pip
python3 -m venv ~/ainstein-gpu && source ~/ainstein-gpu/bin/activate
pip install "tensorflow[and-cuda]" tf_keras tensorflow-probability numpy pyyaml \
    jsonargparse jsonschema rich tqdm matplotlib wandb polars fsspec requests \
    tensorflow-datasets
# проверка GPU:
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
# запуск (репо уже доступно через /mnt/c):
cd /mnt/c/Users/user/ScienceBro/projects/ainstein-audit/upstream/checkout
WANDB_MODE=disabled python3 run.py -c=hyperparameters/hps_schwarzschild.yaml
```

## Текущее состояние CPU-рана

Schwarzschild 500-эпох CPU-ран остановлен на эпохе ~31 (checkpoint + манифест
сохранены в results/raw/schwarzschild-4d-interim-2026-08-11/). Возобновление:
либо ночной CPU-ран (~12-16 ч), либо GPU после установки WSL2 (ожидаемо в разы
быстрее). Upstream поддерживает старт от сохранённой модели
(model.saved_model_path в hps).
