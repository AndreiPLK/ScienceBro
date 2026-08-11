"""Citation verification against public registries (roadmap §6 rule 5).

Network access is optional: on failure the result is `unverified`, never `verified`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import requests

ARXIV_ID_RE = re.compile(r"(?:arXiv:)?(\d{4}\.\d{4,5})(v\d+)?$", re.IGNORECASE)


@dataclass
class CitationCheck:
    identifier: str
    status: str          # "verified" | "not-found" | "unverified" | "invalid-id"
    title: str | None = None
    detail: str = ""


def verify_arxiv_id(identifier: str, timeout: float = 20.0) -> CitationCheck:
    """Check that an arXiv ID exists via the public export API and return its title."""
    m = ARXIV_ID_RE.search(identifier.strip())
    if not m:
        return CitationCheck(identifier, "invalid-id", detail="does not look like an arXiv id")
    arxiv_id = m.group(1)
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}&max_results=1"
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
    except requests.RequestException as e:
        return CitationCheck(identifier, "unverified", detail=f"network error: {e}")
    body = r.text
    # The Atom feed contains an <entry> with a <title> when found; an error entry otherwise.
    if "<entry>" not in body:
        return CitationCheck(identifier, "not-found", detail="no entry in arXiv response")
    titles = re.findall(r"<title>(.*?)</title>", body, re.DOTALL)
    # titles[0] is the feed title; the entry title follows.
    entry_title = titles[1].strip() if len(titles) > 1 else None
    if entry_title and "Error" in entry_title and "incorrect id" in body.lower():
        return CitationCheck(identifier, "not-found", detail=entry_title)
    return CitationCheck(identifier, "verified", title=entry_title)
