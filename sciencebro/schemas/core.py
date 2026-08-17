"""Core scientific objects (roadmap §5, §11) and the claim-promotion gate (§6, rule 28).

Design principles:
- states are explicit enums, not free text;
- promotion is a deterministic function of evidence + validation, never of narrative;
- schemas reject invalid promotion (Phase 1 acceptance criterion).
"""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------- project


class ComputeBudget(BaseModel):
    device: str = "auto"
    max_single_run_hours: float = 12
    max_parallel_runs: int = 2


class Project(BaseModel):
    id: str
    title: str
    domain: str
    stage: Literal[
        "intake",
        "research",
        "evidence",
        "hypothesis",
        "implementation",
        "experiment",
        "validation",
        "claim-promotion",
        "release",
    ] = "intake"
    owner: str
    primary_question: str
    created_at: date
    compute_budget: ComputeBudget = Field(default_factory=ComputeBudget)
    release_targets: list[str] = Field(default_factory=list)
    status_source: Literal["computed"] = "computed"

    @field_validator("id")
    @classmethod
    def _id_slug(cls, v: str) -> str:
        if not v or not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError("project id must be a slug (alnum, - or _)")
        return v


# ---------------------------------------------------------------- evidence


class SourceRef(BaseModel):
    type: Literal[
        "arxiv-paper",
        "journal-paper",
        "preprint",
        "code-repository",
        "dataset",
        "documentation",
        "webpage",
        "book",
        "author-correspondence",  # приватная переписка с автором (EV-CORR-*)
    ]
    identifier: str  # DOI, arXiv ID, URL, or repo@commit
    url: str | None = None
    title: str | None = None


class SourceLocation(BaseModel):
    section: str | None = None
    equation: str | None = None
    figure: str | None = None
    table: str | None = None
    pages: str | None = None
    code_lines: str | None = None


class AccessInfo(BaseModel):
    full_text: bool = False
    abstract_only: bool = False
    acquired_at: date | None = None
    local_file: str | None = None
    file_sha256: str | None = None


class VerifiedBy(BaseModel):
    metadata: bool = False
    content: bool = False
    second_reader: bool = False


class EvidenceRecord(BaseModel):
    id: str
    claim_id: str | None = None
    source: SourceRef
    location: SourceLocation = Field(default_factory=SourceLocation)
    access: AccessInfo = Field(default_factory=AccessInfo)
    paraphrase: str
    support: Literal["supporting", "contradicting", "context"] = "context"
    strength: str = "unclassified"
    limitations: list[str] = Field(default_factory=list)
    verified_by: VerifiedBy = Field(default_factory=VerifiedBy)


# ---------------------------------------------------------------- claims


class ClaimState(StrEnum):
    speculative = "speculative"
    source_supported = "source-supported"
    experimentally_supported = "experimentally-supported"
    independently_validated = "independently-validated"
    refuted = "refuted"
    inconclusive = "inconclusive"
    release_ready = "release-ready"


class Claim(BaseModel):
    id: str
    statement: str
    state: ClaimState = ClaimState.speculative
    evidence_ids: list[str] = Field(default_factory=list)
    contradicting_evidence_ids: list[str] = Field(default_factory=list)
    experiment_ids: list[str] = Field(default_factory=list)
    validation_ids: list[str] = Field(default_factory=list)
    allowed_public_wording: str | None = None
    blockers: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------- hypotheses


class Hypothesis(BaseModel):
    id: str
    statement: str
    null_hypothesis: str
    predictions: list[str] = Field(default_factory=list)
    falsification: list[str] = Field(default_factory=list)
    confounders: list[str] = Field(default_factory=list)
    primary_metric: str
    status: Literal["proposed", "frozen", "tested", "retired"] = "proposed"


# ---------------------------------------------------------------- experiments


class Experiment(BaseModel):
    id: str
    hypothesis_id: str
    status: Literal["draft", "frozen", "running", "completed", "failed"] = "draft"
    code_commit: str | None = None
    upstream_commit: str | None = None
    environment_lock_hash: str | None = None
    command: str | None = None
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    seeds: list[int] = Field(default_factory=lambda: [0])
    precision: str = "float64"
    hardware: str = "auto"
    primary_metric: str
    threshold: dict = Field(default_factory=dict)
    analysis_plan: str | None = None
    exploratory: bool = False

    def freeze_blockers(self) -> list[str]:
        """A protocol may be frozen only when reproduction fields are filled (§6 rule 11)."""
        missing = []
        if not self.command:
            missing.append("command is not set")
        if not self.code_commit:
            missing.append("code_commit is not set")
        if not self.analysis_plan:
            missing.append("analysis_plan is not set")
        if not self.primary_metric:
            missing.append("primary_metric is not set")
        return missing


# ---------------------------------------------------------------- validation


class ValidationDecision(StrEnum):
    pending = "pending"
    passed = "pass"
    failed = "fail"
    inconclusive = "inconclusive"


class ValidationResult(BaseModel):
    id: str
    experiment_id: str
    validator: str
    independence_level: Literal[
        "separate-formulation",
        "separate-implementation",
        "shared-dependency-documented",
    ]
    checks: dict[str, str] = Field(default_factory=dict)
    decision: ValidationDecision = ValidationDecision.pending
    allowed_claim_state: ClaimState = ClaimState.speculative
    blockers: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------- promotion gate

_ORDER = [
    ClaimState.speculative,
    ClaimState.source_supported,
    ClaimState.experimentally_supported,
    ClaimState.independently_validated,
    ClaimState.release_ready,
]


def allowed_claim_promotion(
    claim: Claim,
    target: ClaimState,
    evidence: list[EvidenceRecord],
    validations: list[ValidationResult],
) -> list[str]:
    """Return the list of blockers preventing promotion of `claim` to `target`.

    Empty list == promotion allowed. Deterministic; no LLM judgment (§6 rules 20-23).
    `refuted` and `inconclusive` are terminal downgrade states and are always allowed
    (evidence of failure must never be blocked from recording).
    """
    if target in (ClaimState.refuted, ClaimState.inconclusive, ClaimState.speculative):
        return []

    blockers: list[str] = []
    ev_by_id = {e.id: e for e in evidence}
    linked = [ev_by_id[i] for i in claim.evidence_ids if i in ev_by_id]
    missing_ev = [i for i in claim.evidence_ids if i not in ev_by_id]
    if missing_ev:
        blockers.append(f"evidence ids not found: {missing_ev}")

    if target in _ORDER and claim.state in _ORDER:
        if _ORDER.index(target) - _ORDER.index(claim.state) > 1:
            blockers.append(f"cannot skip states: {claim.state.value} -> {target.value}")

    if target in _ORDER and _ORDER.index(target) >= _ORDER.index(ClaimState.source_supported):
        if not linked:
            blockers.append("no linked evidence records")
        elif all(e.access.abstract_only for e in linked):
            blockers.append("all linked evidence is abstract_only (§6 rule 4)")

    if target in (
        ClaimState.experimentally_supported,
        ClaimState.independently_validated,
        ClaimState.release_ready,
    ):
        if not claim.experiment_ids:
            blockers.append("no linked experiment")

    if target in (ClaimState.independently_validated, ClaimState.release_ready):
        passed = [
            v
            for v in validations
            if v.id in claim.validation_ids and v.decision == ValidationDecision.passed
        ]
        if not passed:
            blockers.append("no passing independent validation")

    if target == ClaimState.release_ready:
        if not claim.allowed_public_wording:
            blockers.append("allowed_public_wording is not set")
        unverified = [e.id for e in linked if not e.verified_by.metadata]
        if unverified:
            blockers.append(f"evidence metadata not verified: {unverified}")

    return blockers
