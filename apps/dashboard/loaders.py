"""Read-only loaders for the dashboard. Repository files are the only truth."""

from __future__ import annotations

import subprocess
from pathlib import Path

import streamlit as st

from sciencebro.config import RepoPaths
from sciencebro.registry import Topic, load_topics
from sciencebro.schemas import Claim, EvidenceRecord, Experiment, Hypothesis, ValidationResult
from sciencebro.status import ProjectStatus, compute_status
from sciencebro.store import ProjectStore, StoreError


def paths() -> RepoPaths:
    return RepoPaths(Path(__file__).resolve().parents[2])


@st.cache_data(ttl=10)
def project_ids() -> list[str]:
    return paths().list_projects()


@st.cache_data(ttl=10)
def status(project_id: str) -> ProjectStatus:
    return compute_status(paths(), project_id)


def _store(project_id: str) -> ProjectStore:
    return ProjectStore(paths(), project_id)


@st.cache_data(ttl=10)
def evidence(project_id: str) -> tuple[list[EvidenceRecord], list[str]]:
    try:
        return _store(project_id).evidence(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=10)
def claims(project_id: str) -> tuple[list[Claim], list[str]]:
    try:
        return _store(project_id).claims(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=10)
def hypotheses(project_id: str) -> tuple[list[Hypothesis], list[str]]:
    try:
        return _store(project_id).hypotheses(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=10)
def experiments(project_id: str) -> tuple[list[Experiment], list[str]]:
    try:
        return _store(project_id).experiments(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=10)
def validations(project_id: str) -> tuple[list[ValidationResult], list[str]]:
    try:
        return _store(project_id).validations(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=10)
def corpus(project_id: str) -> tuple[list[dict], list[str]]:
    try:
        return _store(project_id).corpus(), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=30)
def topics() -> tuple[list[Topic], list[str]]:
    try:
        return load_topics(paths().registry / "topics.yaml"), []
    except StoreError as e:
        return [], [str(e)]


@st.cache_data(ttl=30)
def git_info() -> dict[str, str]:
    root = paths().root
    out = {}
    for key, args in [("commit", ["rev-parse", "--short", "HEAD"]),
                      ("last_commit_time", ["log", "-1", "--format=%ci"])]:
        try:
            r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=10)
            out[key] = r.stdout.strip() if r.returncode == 0 else "n/a"
        except Exception:
            out[key] = "n/a"
    return out
