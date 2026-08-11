"""Inspect AI adapter (optional donor: github.com/UKGovernmentBEIS/inspect_ai).

V1 status: NOT installed. Agent-behavior evals live in tests/evals as plain
pytest until Inspect is introduced (roadmap §19).
"""

from __future__ import annotations


def available() -> bool:
    return False
