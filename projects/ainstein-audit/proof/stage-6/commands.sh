#!/bin/sh
set -e
uv sync --all-groups
uv run pytest -q
uv run sb verify-stage ainstein-audit stage-6
uv run python projects/ainstein-audit/verifier/make_selftest_artifact.py
uv run python projects/ainstein-audit/verifier/known_answer_4d.py
