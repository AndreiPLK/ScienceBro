"""Gold evaluation set G-01..G-05 (see evals/gold/README.md)."""

import sys
from datetime import date
from pathlib import Path

import numpy as np
import pytest
import requests

from sciencebro.evidence import audit_evidence
from sciencebro.research.citations import verify_arxiv_id
from sciencebro.schemas import Claim, ClaimState, EvidenceRecord, allowed_claim_promotion

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "projects" / "ainstein-audit"))


def _network() -> bool:
    try:
        requests.head("https://export.arxiv.org", timeout=5)
        return True
    except requests.RequestException:
        return False


@pytest.mark.skipif(not _network(), reason="offline — eval skips, never fakes a pass")
def test_g01_citation_metadata_validity():
    check = verify_arxiv_id("arXiv:2607.05489")
    assert check.status == "verified"
    assert check.title is not None and "AInstein" in check.title


@pytest.mark.skipif(not _network(), reason="offline — eval skips, never fakes a pass")
def test_g02_fabricated_citation_detected():
    assert verify_arxiv_id("arXiv:2607.99999").status in ("not-found", "invalid-id")


def test_g03_claim_evidence_gate_blocks_unsupported():
    claim = Claim(id="CL-X", statement="unsupported")
    blockers = allowed_claim_promotion(claim, ClaimState.source_supported, [], [])
    assert blockers, "gate must block promotion without evidence"
    assert any("evidence" in b for b in blockers)


def test_g04_contradiction_stays_visible():
    ev = EvidenceRecord(
        id="EV-A",
        source={"type": "arxiv-paper", "identifier": "arXiv:2607.05489"},
        access={"full_text": True, "acquired_at": date(2026, 8, 11)},
        paraphrase="p", support="contradicting",
    )
    claim = Claim(id="CL-Y", statement="s", state=ClaimState.source_supported,
                  evidence_ids=["EV-A"], contradicting_evidence_ids=["EV-A"])
    audit = audit_evidence([claim], [ev])
    assert any("contradicting" in w for w in audit.warnings)


def test_g05_computational_known_answer():
    from verifier.geometry import kretschmann_scalar
    from verifier.known_metrics import kretschmann_schwarzschild_analytic, schwarzschild

    x = np.array([0.0, 12.0, 1.0, 0.5])
    k = kretschmann_scalar(schwarzschild, x)
    k_true = kretschmann_schwarzschild_analytic(12.0)
    assert abs(k - k_true) / k_true < 1e-7
