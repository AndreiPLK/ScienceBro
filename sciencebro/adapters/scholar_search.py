"""Broad scholarly search adapter (optional donor: scholar-megasearch).

V1 status: NOT installed. Native minimal search goes through the public arXiv
API (see sciencebro.research.citations); broad multi-source search is deferred.
"""

from __future__ import annotations


def available() -> bool:
    return False
