"""Deterministic evidence/claim audit (roadmap §6 evidence rules)."""

from __future__ import annotations

from dataclasses import dataclass, field

from sciencebro.schemas import Claim, EvidenceRecord


@dataclass
class EvidenceAudit:
    findings: list[str] = field(default_factory=list)   # rule violations / blockers
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def audit_evidence(claims: list[Claim], evidence: list[EvidenceRecord]) -> EvidenceAudit:
    audit = EvidenceAudit()
    ev_ids = {e.id for e in evidence}

    seen: set[str] = set()
    for e in evidence:
        if e.id in seen:
            audit.findings.append(f"duplicate evidence id {e.id}")
        seen.add(e.id)
        if e.access.abstract_only and e.access.full_text:
            audit.findings.append(f"{e.id}: abstract_only and full_text are both true")
        if not e.paraphrase.strip():
            audit.findings.append(f"{e.id}: empty paraphrase")
        if e.access.full_text and not e.access.acquired_at:
            audit.warnings.append(f"{e.id}: full_text without acquired_at date")

    for c in claims:
        missing = [i for i in c.evidence_ids if i not in ev_ids]
        if missing:
            audit.findings.append(f"claim {c.id}: unknown evidence ids {missing}")
        if c.state.value not in ("speculative",) and not c.evidence_ids:
            audit.findings.append(f"claim {c.id}: state {c.state.value} but no evidence linked")

    # contradictions must stay visible (§6 rule 7)
    for c in claims:
        if c.contradicting_evidence_ids:
            audit.warnings.append(
                f"claim {c.id}: has contradicting evidence {c.contradicting_evidence_ids} (kept visible)"
            )
    return audit
