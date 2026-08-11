"""Schema and claim-gate unit tests (Phase 1 acceptance)."""

from datetime import date

import pytest
from pydantic import ValidationError

from sciencebro.schemas import (
    Claim,
    ClaimState,
    EvidenceRecord,
    Project,
    ValidationDecision,
    ValidationResult,
    allowed_claim_promotion,
)


def make_evidence(eid="EV-1", full_text=True, abstract_only=False, meta_verified=True):
    return EvidenceRecord(
        id=eid,
        source={"type": "arxiv-paper", "identifier": "arXiv:2607.05489"},
        access={"full_text": full_text, "abstract_only": abstract_only,
                "acquired_at": date(2026, 8, 11)},
        paraphrase="Authors report Ricci-flat non-Schwarzschild candidates.",
        verified_by={"metadata": meta_verified, "content": False, "second_reader": False},
    )


def make_validation(vid="VAL-1", decision=ValidationDecision.passed):
    return ValidationResult(
        id=vid, experiment_id="EXP-1", validator="independent-validator",
        independence_level="separate-formulation", decision=decision,
    )


def test_project_rejects_bad_id():
    with pytest.raises(ValidationError):
        Project(id="bad id!", title="t", domain="d", owner="o",
                primary_question="q", created_at=date(2026, 8, 11))


def test_claim_cannot_skip_to_release_ready():
    claim = Claim(id="CL-1", statement="s", state=ClaimState.speculative)
    blockers = allowed_claim_promotion(claim, ClaimState.release_ready, [], [])
    assert blockers  # must be blocked


def test_source_supported_requires_full_text_evidence():
    ev = make_evidence(full_text=False, abstract_only=True)
    claim = Claim(id="CL-1", statement="s", evidence_ids=["EV-1"])
    blockers = allowed_claim_promotion(claim, ClaimState.source_supported, [ev], [])
    assert any("abstract_only" in b for b in blockers)


def test_source_supported_passes_with_full_text():
    ev = make_evidence()
    claim = Claim(id="CL-1", statement="s", evidence_ids=["EV-1"])
    assert allowed_claim_promotion(claim, ClaimState.source_supported, [ev], []) == []


def test_independently_validated_requires_passing_validation():
    ev = make_evidence()
    claim = Claim(
        id="CL-1", statement="s", state=ClaimState.experimentally_supported,
        evidence_ids=["EV-1"], experiment_ids=["EXP-1"], validation_ids=["VAL-1"],
    )
    failed = make_validation(decision=ValidationDecision.failed)
    assert allowed_claim_promotion(claim, ClaimState.independently_validated, [ev], [failed])
    passed = make_validation(decision=ValidationDecision.passed)
    assert allowed_claim_promotion(claim, ClaimState.independently_validated, [ev], [passed]) == []


def test_refuted_and_inconclusive_never_blocked():
    claim = Claim(id="CL-1", statement="s", state=ClaimState.independently_validated)
    assert allowed_claim_promotion(claim, ClaimState.refuted, [], []) == []
    assert allowed_claim_promotion(claim, ClaimState.inconclusive, [], []) == []


def test_release_ready_requires_wording_and_verified_metadata():
    ev = make_evidence(meta_verified=False)
    claim = Claim(
        id="CL-1", statement="s", state=ClaimState.independently_validated,
        evidence_ids=["EV-1"], experiment_ids=["EXP-1"], validation_ids=["VAL-1"],
    )
    blockers = allowed_claim_promotion(
        claim, ClaimState.release_ready, [ev], [make_validation()]
    )
    assert any("wording" in b for b in blockers)
    assert any("metadata" in b for b in blockers)
