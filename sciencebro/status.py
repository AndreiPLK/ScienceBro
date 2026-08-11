"""Computed project status (roadmap §13 Page 1). No invented percentages."""

from __future__ import annotations

from dataclasses import dataclass, field

from sciencebro.config import RepoPaths
from sciencebro.schemas import Claim, ClaimState, ValidationDecision
from sciencebro.store import ProjectStore, StoreError


@dataclass
class ProjectStatus:
    project_id: str
    title: str = ""
    stage: str = ""
    question: str = ""
    evidence_total: int = 0
    evidence_full_text: int = 0
    claims_total: int = 0
    claims_supported: int = 0
    claims_unsupported: list[str] = field(default_factory=list)
    hypotheses: int = 0
    hypotheses_frozen: int = 0
    experiments: int = 0
    experiments_frozen: int = 0
    validations_pass: int = 0
    validations_fail: int = 0
    validations_inconclusive: int = 0
    validations_pending: int = 0
    blockers: list[str] = field(default_factory=list)
    next_action: str = ""
    errors: list[str] = field(default_factory=list)


def _claim_supported(c: Claim) -> bool:
    return c.state != ClaimState.speculative and bool(c.evidence_ids)


def compute_status(paths: RepoPaths, project_id: str) -> ProjectStatus:
    st = ProjectStatus(project_id=project_id)
    store = ProjectStore(paths, project_id)
    try:
        proj = store.project()
        st.title, st.stage, st.question = proj.title, proj.stage, proj.primary_question
    except StoreError as e:
        st.errors.append(str(e))
        return st

    try:
        evidence = store.evidence()
        st.evidence_total = len(evidence)
        st.evidence_full_text = sum(1 for e in evidence if e.access.full_text)
    except StoreError as err:
        st.errors.append(str(err))

    try:
        claims = store.claims()
        st.claims_total = len(claims)
        st.claims_supported = sum(1 for c in claims if _claim_supported(c))
        st.claims_unsupported = [c.id for c in claims if not _claim_supported(c)]
        for c in claims:
            st.blockers.extend(f"{c.id}: {b}" for b in c.blockers)
    except StoreError as err:
        st.errors.append(str(err))

    try:
        hyps = store.hypotheses()
        st.hypotheses = len(hyps)
        st.hypotheses_frozen = sum(1 for h in hyps if h.status == "frozen")
    except StoreError as err:
        st.errors.append(str(err))

    try:
        exps = store.experiments()
        st.experiments = len(exps)
        st.experiments_frozen = sum(1 for x in exps if x.status in ("frozen", "running", "completed"))
    except StoreError as err:
        st.errors.append(str(err))

    try:
        for v in store.validations():
            if v.decision == ValidationDecision.passed:
                st.validations_pass += 1
            elif v.decision == ValidationDecision.failed:
                st.validations_fail += 1
            elif v.decision == ValidationDecision.inconclusive:
                st.validations_inconclusive += 1
            else:
                st.validations_pending += 1
    except StoreError as err:
        st.errors.append(str(err))

    st.next_action = _next_action(st)
    return st


def _next_action(st: ProjectStatus) -> str:
    if st.errors:
        return "fix malformed repository files listed under errors"
    if st.evidence_total == 0:
        return "ingest primary sources and create evidence records"
    if st.claims_total == 0:
        return "extract claims from evidence"
    if st.hypotheses == 0:
        return "write a falsifiable hypothesis"
    if st.hypotheses_frozen == 0:
        return "freeze the hypothesis and protocol before the confirmatory run"
    if st.experiments == 0:
        return "create an experiment manifest"
    if st.validations_pass + st.validations_fail + st.validations_inconclusive == 0:
        return "run the experiment, then request independent validation"
    return "review validation results and update the claim ledger"
