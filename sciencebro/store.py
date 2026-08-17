"""Read/write of scientific objects from repository files.

Files are the source of truth. Malformed files raise actionable errors —
they must never silently disappear (roadmap §20 Phase 6 acceptance).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML

from sciencebro.config import RepoPaths
from sciencebro.schemas import (
    Claim,
    EvidenceRecord,
    Experiment,
    Hypothesis,
    Project,
    ValidationResult,
)

_yaml = YAML(typ="rt")
_yaml.default_flow_style = False

T = TypeVar("T", bound=BaseModel)


class StoreError(RuntimeError):
    """Raised with an actionable message when a repository file is malformed."""


def load_yaml_model[T: BaseModel](path: Path, model: type[T]) -> T:
    if not path.exists():
        raise StoreError(f"missing file: {path}")
    try:
        with path.open("r", encoding="utf-8") as f:
            data = _yaml.load(f)
        return model.model_validate(data)
    except ValidationError as e:
        raise StoreError(f"invalid {model.__name__} in {path}:\n{e}") from e
    except Exception as e:  # ruamel parse errors
        raise StoreError(f"cannot parse YAML {path}: {e}") from e


def save_yaml_model(path: Path, obj: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        _yaml.dump(json.loads(obj.model_dump_json()), f)


def load_jsonl_models[T: BaseModel](path: Path, model: type[T]) -> list[T]:
    if not path.exists():
        return []
    out: list[T] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(model.model_validate_json(line))
        except ValidationError as e:
            raise StoreError(f"invalid {model.__name__} at {path}:{i}:\n{e}") from e
    return out


def append_jsonl_model(path: Path, obj: BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(obj.model_dump_json() + "\n")


# ------------------------------------------------------------ project-level API


class ProjectStore:
    def __init__(self, paths: RepoPaths, project_id: str) -> None:
        self.paths = paths
        self.project_id = project_id

    def project(self) -> Project:
        return load_yaml_model(self.paths.project_file(self.project_id), Project)

    def evidence(self) -> list[EvidenceRecord]:
        return load_jsonl_models(self.paths.evidence_records(self.project_id), EvidenceRecord)

    def claims(self) -> list[Claim]:
        path = self.paths.claims_file(self.project_id)
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8") as f:
                data = _yaml.load(f) or {}
        except Exception as e:
            raise StoreError(f"cannot parse YAML {path}: {e}") from e
        items = data.get("claims", []) if isinstance(data, dict) else data
        try:
            return [Claim.model_validate(c) for c in items]
        except ValidationError as e:
            raise StoreError(f"invalid Claim in {path}:\n{e}") from e

    def save_claims(self, claims: list[Claim]) -> None:
        path = self.paths.claims_file(self.project_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as f:
            _yaml.dump({"claims": [json.loads(c.model_dump_json()) for c in claims]}, f)

    def _load_dir(self, directory: Path, model: type[T]) -> list[T]:
        if not directory.is_dir():
            return []
        return [load_yaml_model(p, model) for p in sorted(directory.glob("*.yaml"))]

    def hypotheses(self) -> list[Hypothesis]:
        return self._load_dir(self.paths.hypotheses_dir(self.project_id), Hypothesis)

    def experiments(self) -> list[Experiment]:
        return self._load_dir(self.paths.experiments_dir(self.project_id), Experiment)

    def validations(self) -> list[ValidationResult]:
        return self._load_dir(self.paths.validations_dir(self.project_id), ValidationResult)

    def corpus(self) -> list[dict]:
        path = self.paths.corpus_file(self.project_id)
        if not path.exists():
            return []
        out = []
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise StoreError(f"invalid JSON at {path}:{i}: {e}") from e
        return out
