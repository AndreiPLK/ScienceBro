"""sciencebro-math as an MCP server: the lab's exact operations as stable tools.

The point is that an agent should stop rewriting the same experiment. Every tool here
is deterministic, takes explicit inputs, returns a machine-readable `Result` with an
`evidence_kind`, and never claims a proof.

Two of these tools exist to enforce discipline rather than to compute: `claims_status`
makes the registry readable before a status is asserted, and `dead_route_check` makes
it cheap to notice that an idea is already dead before spending a night on it.

Run: uv run python -m sciencebro_math.server   (PYTHONPATH=tools)

Built against the mcp 2.x API (`MCPServer`); the 1.x name `FastMCP` no longer exists.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

from . import moments, positivity, sequences
from .battery import anomaly_scan as _anomaly_scan
from .battery import scan_family_centered as _scan_family
from .families import centered_squares, deformed_grid, half_spectrum, normalized_means

ROOT = Path(__file__).resolve().parents[2]
mcp = MCPServer("sciencebro-math")


def _out(r: Any) -> str:
    return r.json() if hasattr(r, "json") else json.dumps(r, indent=2, default=str)


def _family(name: str, n: int, z: str | None = None) -> list:
    """Resolve a named family to its normalized elementary means p_t."""
    if name == "centered_squares":
        return normalized_means(centered_squares(n))
    if name == "half_spectrum":
        return normalized_means(half_spectrum(n))
    if name == "deformed_grid":
        from flint import fmpq

        num, _, den = (z or "0").partition("/")
        zz = fmpq(int(num), int(den) if den else 1)
        return normalized_means(deformed_grid(zz, n))
    raise ValueError(f"unknown family {name!r}; use centered_squares, half_spectrum, deformed_grid")


@mcp.tool()
def family_sequence(family: str, n: int, z: str | None = None) -> str:
    """p_t = e_t/C(N,t) for a named exact family, as exact rationals.

    family: centered_squares | half_spectrum | deformed_grid (z = 'a/b' for j(j+z)).
    """
    p = _family(family, n, z)
    return json.dumps({"family": family, "n": n, "z": z, "p": [str(x) for x in p]}, indent=2)


@mcp.tool()
def anomaly_scan(
    family: str | None = None,
    n: int | None = None,
    values: list[str] | None = None,
    rmax: int = 8,
    z: str | None = None,
) -> str:
    """Run the whole battery on a sequence and rank what is UNUSUAL about it.

    Give either a named family with n, or an explicit list of exact rationals as
    strings. Never pass floats. Covers log-difference hierarchy, ratio log-concavity,
    Turan, Hankel/Toeplitz minors, Hausdorff and Stieltjes signatures, real-rootedness.
    """
    seq = _family(family, n, z) if family else values
    return _out(_anomaly_scan(seq, rmax=rmax))


@mcp.tool()
def scan_family(n_values: list[int], rmax: int = 8) -> str:
    """The battery across several sizes of the physical centred family at once."""
    return _out(_scan_family(n_values, rmax=rmax))


@mcp.tool()
def log_difference_hierarchy(
    values: list[str] | None = None,
    family: str | None = None,
    n: int | None = None,
    rmax: int = 8,
    window_must_fit_in: int | None = None,
) -> str:
    """Signs of Delta^r log p_t, exactly, for r = 2..rmax.

    No logarithm is evaluated: each sign is decided by comparing two products of
    rationals. `window_must_fit_in` bounds the LAST index the window may touch -- set
    it to the domain the claim is actually made on, or the answer is about a larger
    domain than anyone claimed.
    """
    seq = _family(family, n) if family else values
    return _out(sequences.log_difference_hierarchy(seq, rmax, window_must_fit_in))


@mcp.tool()
def ratio_log_concavity(
    values: list[str] | None = None,
    family: str | None = None,
    n: int | None = None,
    upto: int | None = None,
) -> str:
    """p_{t+1}^3 p_{t-1} >= p_t^3 p_{t+2}, exactly, on an explicit index range."""
    seq = _family(family, n) if family else values
    return _out(sequences.ratio_log_concavity(seq, upto))


@mcp.tool()
def hankel_minors(values: list[str], max_order: int = 6, shift: int = 0) -> str:
    """Leading Hankel minors: the Hamburger (shift 0) and Stieltjes (shift 1) signature."""
    return _out(sequences.hankel_minors(values, max_order, shift))


@mcp.tool()
def toeplitz_minors(values: list[str], max_order: int = 4) -> str:
    """All Toeplitz minors up to an order; a negative one refutes Polya-frequency."""
    return _out(sequences.toeplitz_minors(values, max_order))


@mcp.tool()
def hausdorff_conditions(values: list[str], max_order: int = 10) -> str:
    """Complete monotonicity, forward AND reversed -- the reversal is often the only
    orientation that can carry a positive measure."""
    return _out(sequences.hausdorff_conditions(values, max_order))


@mcp.tool()
def log_moment_signature(
    values: list[str] | None = None,
    family: str | None = None,
    n: int | None = None,
    max_order: int = 6,
) -> str:
    """Can A_t = -Delta^2 log p_t come from a positive measure? Hankel signature of A.

    A is transcendental, so this is NUMERIC at two precisions and reports inconclusive
    when the signs disagree. Use it as a FALSIFIER: a stable negative minor kills the
    representation; passing minors never establish one.
    """
    seq = _family(family, n) if family else values
    return _out(moments.log_moment_signature(seq, max_order=max_order))


@mcp.tool()
def verify_polynomial_positive(
    coefficients: list[str], lo: str = "0", hi: str = "1", subdivisions: int = 4
) -> str:
    """Escalate manifest monomial signs -> Bernstein -> subdivided Bernstein.

    Returns the cheapest level that certified. Failing to certify is `inconclusive`,
    never `refuted`: not proving positivity is not the same as disproving it.
    """
    return _out(positivity.verify_polynomial_positive(coefficients, lo, hi, subdivisions))


@mcp.tool()
def sturm_sign(coefficients: list[str], lo: str = "0", hi: str = "1") -> str:
    """Exact: does the polynomial keep one sign on the interval? Via a Sturm root count."""
    return _out(positivity.sturm_sign(coefficients, lo, hi))


@mcp.tool()
def bernstein_certificate(coefficients: list[str], lo: str = "0", hi: str = "1") -> str:
    """Bernstein coefficients on a box; all nonnegative certifies nonnegativity there."""
    return _out(positivity.bernstein_certificate(coefficients, lo, hi))


@mcp.tool()
def real_rootedness(coefficients: list[str]) -> str:
    """Certified root isolation: is the generating polynomial real-rooted? Root mesh too."""
    return _out(sequences.real_rootedness(coefficients))


@mcp.tool()
def claims_status(claim_id: str | None = None) -> str:
    """Read the claim registry. Check this BEFORE asserting any status in prose.

    Statuses never merge: PROVED / CERTIFIED / COMPUTATIONALLY_VERIFIED / MEASURED /
    CONJECTURED / HEURISTIC / DISPROVED / DEAD_ROUTE.
    """
    d = ROOT / "research" / "claims"
    if not d.exists():
        return json.dumps({"error": "no registry"})
    if claim_id:
        f = d / f"{claim_id}.md"
        return (
            f.read_text(encoding="utf-8") if f.exists() else json.dumps({"error": "no such claim"})
        )
    rows = []
    for f in sorted(d.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        rows.append(
            {
                "id": f.stem,
                "status": (re.search(r"^status:\s*(\S+)", t, re.M) or [None, "?"])[1],
                "statement": (re.search(r"^statement:\s*(.+)$", t, re.M) or [None, ""])[1],
                "domain": (re.search(r"^domain:\s*(.+)$", t, re.M) or [None, ""])[1],
            }
        )
    return json.dumps(rows, indent=2)


@mcp.tool()
def dead_route_check(query: str) -> str:
    """Search the negative-result log before proposing a route. Cheap; skipping it is not.

    Returns the matching entries in full, including what killed each one and whether a
    weaker variant survived.
    """
    f = ROOT / "research" / "dead_routes.md"
    if not f.exists():
        return json.dumps({"error": "no dead_routes.md"})
    text = f.read_text(encoding="utf-8")
    blocks = re.split(r"\n---\n", text)
    terms = [w for w in re.split(r"\W+", query.lower()) if len(w) > 3]
    hits = [b for b in blocks if sum(1 for w in terms if w in b.lower()) >= max(1, len(terms) // 3)]
    return json.dumps(
        {
            "query": query,
            "matches": len(hits),
            "entries": hits[:5] or ["no match -- but the log is short; read it in full"],
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
