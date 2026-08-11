"""ScienceBro dashboard — an instrument panel over repository files (roadmap §13).

Read-only. Never invents progress. No overall-confidence percentage exists anywhere.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps.dashboard import loaders  # noqa: E402

st.set_page_config(page_title="ScienceBro", page_icon="🔬", layout="wide")

ids = loaders.project_ids()
if not ids:
    st.error("No projects found under projects/. Create one with `sb project init` or see README.")
    st.stop()

with st.sidebar:
    st.title("🔬 ScienceBro")
    project_id = st.selectbox("Project", ids, index=0)
    page = st.radio("Page", [
        "1 · Mission Control", "2 · Evidence", "3 · Hypotheses & Experiments",
        "4 · Validation", "5 · Claims", "6 · Opportunity backlog", "7 · Release",
    ])
    st.caption("Dashboard reads repository files only. It cannot invent progress.")

status = loaders.status(project_id)
git = loaders.git_info()


def show_errors(errors: list[str]) -> None:
    for e in errors:
        st.error(e)


# ---------------------------------------------------------------- page 1

if page.startswith("1"):
    st.header(status.title or project_id)
    st.subheader("Research question")
    st.write(status.question)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Evidence coverage",
                  f"{status.claims_supported}/{status.claims_total}",
                  help="Supported factual claims / all factual claims. Computed from claims.yaml, not invented.")
    with c2:
        st.metric("Full-text sources", f"{status.evidence_full_text}/{status.evidence_total}",
                  help="Evidence records with acquired full text (abstract-only is not full evidence).")
    with c3:
        total_v = status.validations_pass + status.validations_fail + status.validations_inconclusive
        st.metric("Validation",
                  f"✅{status.validations_pass} ❌{status.validations_fail} ❓{status.validations_inconclusive}",
                  help=f"pass/fail/inconclusive; {status.validations_pending} pending. "
                       "'Not started' is an honest state." if total_v == 0 else None)

    st.markdown(f"**Stage:** `{status.stage}` &nbsp;&nbsp; **Git:** `{git['commit']}` "
                f"({git['last_commit_time']})")
    st.markdown(f"**Next required action:** {status.next_action}")

    if status.blockers:
        st.subheader("Blockers")
        for b in status.blockers:
            st.warning(b)
    if status.errors:
        st.subheader("Repository file errors")
        show_errors(status.errors)
    if not status.blockers and not status.errors:
        st.success("No blockers recorded.")

# ---------------------------------------------------------------- page 2

elif page.startswith("2"):
    st.header("Evidence")
    corpus, errs = loaders.corpus(project_id)
    show_errors(errs)
    if corpus:
        st.subheader("Corpus")
        st.dataframe(corpus, use_container_width=True)

    records, errs = loaders.evidence(project_id)
    show_errors(errs)
    claims, errs2 = loaders.claims(project_id)
    show_errors(errs2)

    st.subheader("Evidence records")
    if not records:
        st.info("No evidence records yet.")
    for r in records:
        flags = []
        if r.access.abstract_only:
            flags.append("⚠️ abstract-only")
        if not r.verified_by.metadata:
            flags.append("⚠️ metadata unverified")
        if r.support == "contradicting":
            flags.append("🔴 contradicting")
        label = f"{r.id} · {r.source.identifier} · {r.support}" + (" · " + " ".join(flags) if flags else "")
        with st.expander(label):
            st.write(f"**Paraphrase:** {r.paraphrase}")
            loc = {k: v for k, v in r.location.model_dump().items() if v}
            st.write(f"**Location:** {loc or 'not specified'}")
            st.write(f"**Access:** full_text={r.access.full_text}, abstract_only={r.access.abstract_only}, "
                     f"acquired={r.access.acquired_at}")
            if r.limitations:
                st.write("**Limitations:**")
                for lim in r.limitations:
                    st.write(f"- {lim}")
            st.write(f"**Verified:** metadata={r.verified_by.metadata}, content={r.verified_by.content}, "
                     f"second_reader={r.verified_by.second_reader}")

    st.subheader("Claim ↔ source mapping")
    ev_ids = {r.id for r in records}
    for c in claims:
        missing = [i for i in c.evidence_ids if i not in ev_ids]
        if not c.evidence_ids:
            st.warning(f"{c.id}: UNSUPPORTED — no evidence linked. «{c.statement[:120]}»")
        elif missing:
            st.error(f"{c.id}: broken links {missing}")
        else:
            st.write(f"✅ {c.id} ← {', '.join(c.evidence_ids)}")
        if c.contradicting_evidence_ids:
            st.error(f"{c.id}: contradicting evidence {c.contradicting_evidence_ids} (kept visible)")

# ---------------------------------------------------------------- page 3

elif page.startswith("3"):
    st.header("Hypotheses & Experiments")
    hyps, errs = loaders.hypotheses(project_id)
    show_errors(errs)
    if not hyps:
        st.info("No hypotheses yet.")
    for h in hyps:
        frozen = "🧊 frozen" if h.status == "frozen" else f"🟡 {h.status}"
        with st.expander(f"{h.id} · {frozen} · metric: {h.primary_metric}", expanded=True):
            st.write(f"**Hypothesis:** {h.statement}")
            st.write(f"**Null:** {h.null_hypothesis}")
            if h.predictions:
                st.write("**Predictions:** " + "; ".join(h.predictions))
            if h.falsification:
                st.write("**Falsified if:** " + "; ".join(h.falsification))
            if h.confounders:
                st.write("**Confounders:** " + "; ".join(h.confounders))
        st.caption("What does this mean? A frozen hypothesis cannot be changed after seeing "
                   "results — that is what makes the test honest.")

    exps, errs = loaders.experiments(project_id)
    show_errors(errs)
    st.subheader("Experiment runs")
    if not exps:
        st.info("No experiments yet. The manifest is created before the run and frozen before "
                "looking at final results.")
    for x in exps:
        with st.expander(f"{x.id} · {x.status} · metric: {x.primary_metric}"):
            st.json(x.model_dump())

# ---------------------------------------------------------------- page 4

elif page.startswith("4"):
    st.header("Validation")
    vals, errs = loaders.validations(project_id)
    show_errors(errs)
    if not vals:
        st.info("Validation not started. This is an honest state, not a failure.")
    for v in vals:
        icon = {"pass": "✅", "fail": "❌", "inconclusive": "❓", "pending": "⏳"}.get(v.decision.value, "⏳")
        with st.expander(f"{v.id} · {icon} {v.decision.value} · independence: {v.independence_level}",
                         expanded=True):
            st.write("**Checks:**")
            for name, state in v.checks.items():
                mark = {"pass": "✅", "fail": "❌", "pending": "⏳", "inconclusive": "❓"}.get(state, state)
                st.write(f"- {name}: {mark}")
            if v.blockers:
                for b in v.blockers:
                    st.warning(b)
            st.write(f"**Allowed claim state:** `{v.allowed_claim_state.value}`")
    st.caption("What does this mean? The validator recomputes results with an independent "
               "implementation, on hidden points, with negative controls — it does not trust "
               "the experiment's own code.")

# ---------------------------------------------------------------- page 5

elif page.startswith("5"):
    st.header("Claims ledger")
    claims, errs = loaders.claims(project_id)
    show_errors(errs)
    records, _ = loaders.evidence(project_id)
    vals, _ = loaders.validations(project_id)
    from sciencebro.schemas import ClaimState, allowed_claim_promotion  # noqa: E402

    if not claims:
        st.info("No claims recorded.")
    order = [ClaimState.source_supported, ClaimState.experimentally_supported,
             ClaimState.independently_validated, ClaimState.release_ready]
    for c in claims:
        with st.expander(f"{c.id} · state: {c.state.value}", expanded=True):
            st.write(f"**Statement:** {c.statement}")
            st.write(f"**Supporting evidence:** {', '.join(c.evidence_ids) or 'none'}")
            if c.contradicting_evidence_ids:
                st.error(f"Contradicting evidence: {', '.join(c.contradicting_evidence_ids)}")
            st.write(f"**Experiments:** {', '.join(c.experiment_ids) or 'none'} · "
                     f"**Validations:** {', '.join(c.validation_ids) or 'none'}")
            st.write(f"**Allowed public wording:** {c.allowed_public_wording or '—'}")
            values = [s.value for s in order]
            idx = values.index(c.state.value) if c.state.value in values else -1
            target = order[idx + 1] if 0 <= idx < len(order) - 1 else order[0] if idx == -1 else None
            if target:
                blockers = allowed_claim_promotion(c, target, records, vals)
                st.write(f"**Promotion to `{target.value}` blocked by:**" if blockers
                         else f"**Promotion to `{target.value}`: allowed** (human approval still required)")
                for b in blockers:
                    st.warning(b)
            for b in c.blockers:
                st.warning(b)

# ---------------------------------------------------------------- page 6

elif page.startswith("6"):
    st.header("Opportunity backlog")
    topics, errs = loaders.topics()
    show_errors(errs)
    st.caption("Readiness states are explicit facts, not probabilities.")
    st.dataframe(
        [{"rank": t.rank, "id": t.id, "domain": t.domain, "readiness": t.readiness,
          "one-week artifact": t.one_week_artifact, "compute": t.compute,
          "ceiling": t.scientific_ceiling, "publication": t.publication_path,
          "upstreams": ", ".join(t.required_upstreams)} for t in topics],
        use_container_width=True,
    )

# ---------------------------------------------------------------- page 7

elif page.startswith("7"):
    st.header("Release readiness")
    root = loaders.paths().root
    proj = loaders.paths().project_dir(project_id)
    checks = [
        ("README.md", (root / "README.md").exists()),
        ("LICENSE", (root / "LICENSE").exists()),
        ("CITATION.cff", (root / "CITATION.cff").exists()),
        ("uv.lock (environment lock)", (root / "uv.lock").exists()),
        ("CI workflow", (root / ".github" / "workflows" / "ci.yml").exists()),
        ("reports/ exists", (proj / "reports").is_dir()),
        ("results/ exists", (proj / "results").is_dir()),
        ("release checklist", any((proj / "release").glob("*.yaml")) if (proj / "release").is_dir() else False),
    ]
    for name, ok in checks:
        st.write(("✅ " if ok else "❌ ") + name)
    claims, _ = loaders.claims(project_id)
    from sciencebro.schemas import ClaimState  # noqa: E402
    rr = [c.id for c in claims if c.state == ClaimState.release_ready]
    if rr:
        st.success(f"Release-ready claims: {', '.join(rr)}")
    else:
        st.warning("No claim has reached release-ready. Publishing now would be overclaiming.")
    st.caption("Run `uv run sb release check " + project_id + "` for the full gate. "
               "Publication is always a deliberate human action.")
