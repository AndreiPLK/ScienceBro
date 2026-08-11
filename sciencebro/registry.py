"""Topic registry loader (roadmap §16)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, ValidationError
from ruamel.yaml import YAML

from sciencebro.store import StoreError

_yaml = YAML(typ="safe")

READINESS = ["ready", "needs setup", "needs domain collaborator", "blocked by data", "archived"]


class Topic(BaseModel):
    id: str
    rank: int
    domain: str
    question: str
    starting_point: str
    one_week_artifact: str
    compute: str = "home"
    readiness: str = "needs setup"
    scientific_ceiling: str = ""
    publication_path: str = ""
    required_upstreams: list[str] = Field(default_factory=list)


def load_topics(path: Path) -> list[Topic]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = _yaml.load(f) or {}
    except Exception as e:
        raise StoreError(f"cannot parse YAML {path}: {e}") from e
    try:
        topics = [Topic.model_validate(t) for t in data.get("topics", [])]
    except ValidationError as e:
        raise StoreError(f"invalid Topic in {path}:\n{e}") from e
    bad = [t.id for t in topics if t.readiness not in READINESS]
    if bad:
        raise StoreError(f"topics with invalid readiness state: {bad} (allowed: {READINESS})")
    return sorted(topics, key=lambda t: t.rank)
