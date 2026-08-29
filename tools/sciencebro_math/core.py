"""The result envelope every sciencebro-math tool returns, and the exactness discipline.

Two rules are enforced here rather than left to good intentions.

**A tool never reports a proof.** `evidence_kind` has four values and none of them is
PROOF: `EXACT_FINITE` (an exact statement about finitely many cases), `CERTIFICATE`
(an exact positivity or sign certificate valid on a whole region), `SYMBOLIC` (an
identity produced by symbolic manipulation, pending independent verification) and
`NUMERIC` (floating point or fixed-precision). A claim in `research/claims/` may be
promoted to PROVED only by a human-readable argument, never by a tool result.

**Numeric results must carry their own health warning.** Any result built with
floating point records precision and is marked `exact = False`, so a downstream
reader cannot mistake it for exact evidence. Tools that could have been exact and
were not say so in `warnings`.

Every result carries provenance: git commit, dirty flag, engine versions, and the
exact inputs, so a number in a document can always be traced to the call that made it.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

EvidenceKind = Literal["EXACT_FINITE", "CERTIFICATE", "SYMBOLIC", "NUMERIC"]
Status = Literal["ok", "refuted", "inconclusive", "error"]

# What a tool result is allowed to support, at most. Nothing here reaches PROVED.
KIND_TO_MAX_CLAIM_STATUS: dict[str, str] = {
    "EXACT_FINITE": "COMPUTATIONALLY_VERIFIED",
    "CERTIFICATE": "CERTIFIED",
    "SYMBOLIC": "MEASURED",
    "NUMERIC": "MEASURED",
}


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=20
        ).stdout.strip()
    except Exception:
        return ""


def _engines() -> dict[str, str]:
    out = {"python": sys.version.split()[0], "platform": platform.platform()}
    for name in ("flint", "sympy", "mpmath", "numpy"):
        try:
            mod = __import__(name)
            out[name] = str(getattr(mod, "__version__", "present"))
        except Exception:
            out[name] = "absent"
    return out


def provenance() -> dict[str, Any]:
    dirty = _git("status", "--porcelain")
    return {
        "git": _git("rev-parse", "--short", "HEAD"),
        "git_full": _git("rev-parse", "HEAD"),
        "dirty": bool(dirty),
        "dirty_count": len(dirty.splitlines()) if dirty else 0,
        "engines": _engines(),
    }


@dataclass
class Result:
    """A machine-readable answer with its epistemic status attached."""

    tool: str
    inputs: dict[str, Any]
    status: Status
    evidence_kind: EvidenceKind
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    precision: str | None = None  # set whenever evidence_kind == "NUMERIC"
    runtime_s: float = 0.0
    prov: dict[str, Any] = field(default_factory=provenance)

    def __post_init__(self) -> None:
        if self.evidence_kind == "NUMERIC" and not self.precision:
            self.warnings.append(
                "NUMERIC result without a stated precision; treat as heuristic only"
            )

    @property
    def exact(self) -> bool:
        return self.evidence_kind in ("EXACT_FINITE", "CERTIFICATE")

    @property
    def supports_at_most(self) -> str:
        return KIND_TO_MAX_CLAIM_STATUS[self.evidence_kind]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["exact"] = self.exact
        d["supports_at_most"] = self.supports_at_most
        d["never"] = "no tool result upgrades a claim to PROVED"
        return d

    def json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


class timed:
    """Context manager that stamps a Result's runtime."""

    def __init__(self) -> None:
        self.t0 = time.time()

    def stop(self) -> float:
        return round(time.time() - self.t0, 4)
