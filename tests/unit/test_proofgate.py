"""Proof-gate unit tests: statuses computed from artifacts, never from narrative."""

from sciencebro.proofgate import GateResult, Requirement


def _gate(reqs):
    return GateResult(
        stage_id="stage-x",
        title="t",
        label="SCIENTIFIC",
        question="q",
        why_it_matters="w",
        allowed_public_claim="c",
        requirements=reqs,
    )


def test_all_missing_is_not_started_never_verified():
    g = _gate([Requirement("a", "d", "missing"), Requirement("b", "d", "missing")])
    assert g.status == "NOT STARTED"


def test_any_fail_is_failed():
    g = _gate([Requirement("a", "d", "pass"), Requirement("b", "d", "fail")])
    assert g.status == "FAILED"


def test_partial_pass_is_in_progress_not_verified():
    g = _gate([Requirement("a", "d", "pass"), Requirement("b", "d", "missing")])
    assert g.status == "IN PROGRESS"


def test_all_pass_is_verified():
    g = _gate([Requirement("a", "d", "pass"), Requirement("b", "d", "pass")])
    assert g.status == "VERIFIED"


def test_empty_gate_is_not_started():
    assert _gate([]).status == "NOT STARTED"


def test_attestation_integrity_detects_change(tmp_path):
    import json

    from sciencebro.proofgate import check_attestation_integrity

    art = tmp_path / "data.json"
    art.write_text('{"v": 1}', encoding="utf-8")
    import hashlib

    att = tmp_path / "attestation.json"
    att.write_text(
        json.dumps({"artifact_hashes": {str(art): hashlib.sha256(art.read_bytes()).hexdigest()}}),
        encoding="utf-8",
    )
    assert check_attestation_integrity(att) == []
    art.write_text('{"v": 2}', encoding="utf-8")
    problems = check_attestation_integrity(att)
    assert problems and "CHANGED" in problems[0]
