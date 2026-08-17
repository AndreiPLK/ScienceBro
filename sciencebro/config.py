"""Repository layout and path resolution.

The repository files (YAML/JSONL/Markdown) are the source of truth.
This module only locates them; it never invents state.
"""

from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from `start` (or cwd) until a directory containing pyproject.toml
    with the sciencebro package is found. Falls back to cwd."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "sciencebro").is_dir():
            return candidate
    return cur


class RepoPaths:
    """All well-known paths, derived from the repo root."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = find_repo_root(root)

    @property
    def projects(self) -> Path:
        return self.root / "projects"

    @property
    def registry(self) -> Path:
        return self.root / "registry"

    @property
    def templates(self) -> Path:
        return self.root / "templates"

    @property
    def vendor(self) -> Path:
        return self.root / "vendor"

    @property
    def docs(self) -> Path:
        return self.root / "docs"

    def project_dir(self, project_id: str) -> Path:
        return self.projects / project_id

    def project_file(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "project.yaml"

    def evidence_records(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "evidence" / "records.jsonl"

    def claims_file(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "evidence" / "claims.yaml"

    def hypotheses_dir(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "hypotheses"

    def experiments_dir(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "experiments"

    def validations_dir(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "validations"

    def corpus_file(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "research" / "corpus.jsonl"

    def list_projects(self) -> list[str]:
        if not self.projects.is_dir():
            return []
        return sorted(p.name for p in self.projects.iterdir() if (p / "project.yaml").exists())
