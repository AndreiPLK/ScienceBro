"""Phase 3 acceptance: real citation verifies, fake citation is detected.

Requires network; skipped automatically when arXiv is unreachable.
"""

import pytest
import requests

from sciencebro.research.citations import verify_arxiv_id


def _network_available() -> bool:
    try:
        requests.head("https://export.arxiv.org", timeout=5)
        return True
    except requests.RequestException:
        return False


network = pytest.mark.skipif(not _network_available(), reason="arXiv unreachable")


@network
def test_real_arxiv_id_verifies():
    check = verify_arxiv_id("arXiv:2607.05489")
    assert check.status == "verified"
    assert check.title and "AInstein" in check.title


@network
def test_fake_arxiv_id_detected():
    check = verify_arxiv_id("arXiv:2607.99999")
    assert check.status in ("not-found", "invalid-id")


def test_garbage_id_rejected_offline():
    assert verify_arxiv_id("not-an-id").status == "invalid-id"
