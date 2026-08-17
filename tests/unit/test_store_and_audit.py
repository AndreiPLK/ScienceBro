"""Store round-trip and evidence-audit tests."""

from datetime import date

import pytest

from sciencebro.evidence import audit_evidence
from sciencebro.schemas import Claim, ClaimState, EvidenceRecord, Hypothesis
from sciencebro.store import StoreError, load_yaml_model, save_yaml_model


def test_yaml_roundtrip(tmp_path):
    h = Hypothesis(
        id="H-1",
        statement="s",
        null_hypothesis="n",
        primary_metric="residual",
        status="proposed",
    )
    p = tmp_path / "h.yaml"
    save_yaml_model(p, h)
    loaded = load_yaml_model(p, Hypothesis)
    assert loaded == h


def test_malformed_yaml_raises_actionable_error(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("id: [unclosed", encoding="utf-8")
    with pytest.raises(StoreError):
        load_yaml_model(p, Hypothesis)


def test_missing_file_raises(tmp_path):
    with pytest.raises(StoreError, match="missing file"):
        load_yaml_model(tmp_path / "nope.yaml", Hypothesis)


def _ev(eid):
    return EvidenceRecord(
        id=eid,
        source={"type": "arxiv-paper", "identifier": "arXiv:2607.05489"},
        access={"full_text": True, "acquired_at": date(2026, 8, 11)},
        paraphrase="p",
    )


def test_audit_flags_unknown_evidence_and_duplicates():
    claims = [
        Claim(id="CL-1", statement="s", state=ClaimState.source_supported, evidence_ids=["EV-404"])
    ]
    evidence = [_ev("EV-1"), _ev("EV-1")]
    audit = audit_evidence(claims, evidence)
    assert not audit.ok
    assert any("unknown evidence" in f for f in audit.findings)
    assert any("duplicate" in f for f in audit.findings)


def test_audit_clean():
    claims = [
        Claim(id="CL-1", statement="s", state=ClaimState.source_supported, evidence_ids=["EV-1"])
    ]
    audit = audit_evidence(claims, [_ev("EV-1")])
    assert audit.ok
