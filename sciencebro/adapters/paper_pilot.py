"""Paper Pilot adapter (optional donor: github.com/aytzey/paper-pilot).

V1 status: NOT installed. This is a documented stub with a filesystem fallback:
PDFs placed manually under projects/<id>/research/ are picked up by the corpus.
See vendor/upstream-manifest.yaml for the pinned reference.
"""

from __future__ import annotations


def available() -> bool:
    return False
