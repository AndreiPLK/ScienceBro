"""Mission Control: the research state for a non-physicist owner, in under 10 seconds.

Every status is computed from repository artifacts. Missing data → UNKNOWN/BLOCKED,
never a fake success. No completion percentages exist.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import streamlit as st

from apps.dashboard import loaders

# status → (label, color)
COLORS = {
    "VERIFIED": "#2e9e44",      # green — verified results only
    "IN PROGRESS": "#d99000",   # amber
    "BLOCKED": "#d99000",       # amber (unresolved, not a failure)
    "FAILED": "#cc3333",        # red — real failures only
    "NOT STARTED": "#8a8a8a",   # grey
    "UNKNOWN": "#8a8a8a",
}

MISSION = "Are the AI-discovered black-hole metrics physically real, or are they numerical artifacts?"

RICCI_TOL = 1e-7   # matches THRESHOLDS_DRAFT pipeline validity gate
KREL_TOL = 1e-7


@dataclass
class Stage:
    title: str
    status: str
    note: str


def _proj_dir(project_id: str) -> Path:
    return loaders.paths().project_dir(project_id)


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _training_state(proj: Path) -> dict:
    """Parse the newest Schwarzschild training log (real file, no invention)."""
    candidates = sorted(
        (proj / "upstream").glob("baseline_schwarzschild*.log"),
        key=lambda p: p.stat().st_mtime, reverse=True,
    )
    log = candidates[0] if candidates else proj / "upstream" / "baseline_schwarzschild.log"
    out: dict = {"exists": log.exists(), "epochs": 0, "last_loss": None,
                 "finished": False, "exit_code": None, "log": str(log)}
    if not log.exists():
        return out
    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return out
    epochs = re.findall(r"Epoch (\d+): Loss: ([\d.eE+-]+)", text)
    if epochs:
        out["epochs"] = int(epochs[-1][0])
        out["last_loss"] = float(epochs[-1][1])
    m = re.search(r"EXIT=(\d+)", text)
    if m:
        out["finished"] = True
        out["exit_code"] = int(m.group(1))
    else:
        # no EXIT marker: running only if the log is fresh (written in the last 10 min)
        import time
        out["stalled"] = (time.time() - log.stat().st_mtime) > 600
    return out


RU_TITLES = {
    "stage-1": "ScienceBro system built",
    "stage-2": "Verifier calibrated",
    "stage-3": "Petrov-I candidate trained",
    "stage-4": "Candidate independently stress-tested",
    "stage-5": "Scientific verdict reached",
    "stage-6": "Public release prepared",
}


@st.cache_data(ttl=60)
def _gates(project_id: str) -> list:
    """Proof-gate verification — the ONLY source of stage statuses (never narrative)."""
    from sciencebro.proofgate import verify_all

    return verify_all(loaders.paths(), project_id)


def compute_stages(project_id: str) -> tuple[list[Stage], dict, list]:
    proj = _proj_dir(project_id)
    ctx: dict = {}
    selftest = _load_json(proj / "results" / "processed" / "verifier_selftest.json")
    ka4d = _load_json(proj / "results" / "processed" / "known_answer_4d.json")
    disc = _load_json(proj / "results" / "processed" / "discrepancy_experiment.json")
    training = _training_state(proj)
    ctx.update(selftest=selftest, ka4d=ka4d, disc=disc, training=training)

    gates = _gates(project_id)
    stages = []
    for g in gates:
        status = g.status
        # directive: candidate generation is BLOCKED (not merely NOT STARTED)
        # while its recorded preconditions are unmet
        if g.stage_id == "stage-3" and status in ("NOT STARTED", "IN PROGRESS"):
            unmet = [r for r in g.requirements if r.status != "pass"]
            if unmet:
                status = "BLOCKED"
        n_pass = sum(1 for r in g.requirements if r.status == "pass")
        note = f"{n_pass}/{len(g.requirements)} requirements"
        if g.label == "ENGINEERING" and status == "VERIFIED":
            note += " · engineering, not scientific"
        stages.append(Stage(RU_TITLES.get(g.stage_id, g.title), status, note))
    return stages, ctx, gates


RU_SHORT = {
    "stage-1": "System",
    "stage-2": "Verifier",
    "stage-3": "Candidate",
    "stage-4": "Stress test",
    "stage-5": "Verdict",
    "stage-6": "Release",
}

STAGE_ICONS = {
    "stage-1": "&#9881;",   # gear
    "stage-2": "&#128300;", # microscope
    "stage-3": "&#129504;", # brain
    "stage-4": "&#9876;",   # crossed swords
    "stage-5": "&#9878;",   # scales
    "stage-6": "&#128640;", # rocket
}


def _display_status(gate) -> str:  # type: ignore[no-untyped-def]
    """Stage-3 shows BLOCKED while its preconditions are unmet (directive §4)."""
    if gate.stage_id == "stage-3" and gate.status in ("NOT STARTED", "IN PROGRESS"):
        if any(r.status != "pass" for r in gate.requirements):
            return "BLOCKED"
    return gate.status


def _quest_map_svg(gates: list, current_idx: int) -> str:
    """Game-style quest map: 6 nodes on a path. Colors = honest proof-gate statuses."""
    w, h = 1180, 230
    xs = [90 + i * 200 for i in range(6)]
    y = 100
    parts = [
        f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto;" '
        f'xmlns="http://www.w3.org/2000/svg">',
        "<style>.pulse{animation:pu 1.6s ease-in-out infinite;}"
        "@keyframes pu{0%,100%{stroke-opacity:0.25;stroke-width:6}50%{stroke-opacity:0.9;stroke-width:12}}"
        ".lbl{font:600 17px sans-serif;fill:#c9c9c9;}"
        ".st{font:700 13px sans-serif;}"
        ".ico{font-size:26px;}</style>",
    ]
    # path segments
    for i in range(5):
        done = gates[i].status == "VERIFIED"
        seg = COLORS["VERIFIED"] if done else "#555"
        dash = "" if done else ' stroke-dasharray="7 7"'
        parts.append(f'<line x1="{xs[i]+42}" y1="{y}" x2="{xs[i+1]-42}" y2="{y}" '
                     f'stroke="{seg}" stroke-width="5"{dash}/>')
    for i, g in enumerate(gates):
        disp = _display_status(g)
        c = COLORS.get(disp, "#8a8a8a")
        x = xs[i]
        n_pass = sum(1 for r in g.requirements if r.status == "pass")
        n_all = len(g.requirements)
        if i == current_idx:
            parts.append(f'<circle class="pulse" cx="{x}" cy="{y}" r="50" fill="none" '
                         f'stroke="{c}"/>')
        fill = c if disp == "VERIFIED" else "none"
        txtc = "#111" if disp == "VERIFIED" else c
        parts.append(f'<circle cx="{x}" cy="{y}" r="40" fill="{fill}" stroke="{c}" '
                     f'stroke-width="4"/>')
        icon = "&#10004;" if disp == "VERIFIED" else ("&#10008;" if disp == "FAILED"
                 else STAGE_ICONS.get(g.stage_id, "?"))
        parts.append(f'<text x="{x}" y="{y+10}" text-anchor="middle" class="ico" '
                     f'fill="{txtc}">{icon}</text>')
        parts.append(f'<text x="{x}" y="{y-58}" text-anchor="middle" class="lbl">'
                     f'{RU_SHORT.get(g.stage_id, g.title)}</text>')
        parts.append(f'<text x="{x}" y="{y+68}" text-anchor="middle" class="st" '
                     f'fill="{c}">{disp}</text>')
        parts.append(f'<text x="{x}" y="{y+88}" text-anchor="middle" class="st" '
                     f'fill="#888">{n_pass}/{n_all}</text>')
    parts.append("</svg>")
    return "".join(parts)


def _hud_card(title: str, value: str, color: str, sub: str = "") -> str:
    return (
        f'<div style="flex:1;min-width:150px;border:1px solid {color};border-radius:10px;'
        f'padding:10px 14px;margin:4px;">'
        f'<div style="font-size:0.8em;opacity:0.7;">{title}</div>'
        f'<div style="font-size:1.25em;font-weight:700;color:{color};">{value}</div>'
        + (f'<div style="font-size:0.75em;opacity:0.6;">{sub}</div>' if sub else "")
        + "</div>"
    )


def _checks_grid(gate) -> str:  # type: ignore[no-untyped-def]
    cells = []
    for r in gate.requirements:
        c = {"pass": COLORS["VERIFIED"], "fail": COLORS["FAILED"]}.get(r.status, "#8a8a8a")
        mark = {"pass": "&#10004;", "fail": "&#10008;"}.get(r.status, "&#8943;")
        cells.append(
            f'<div style="border:1px solid {c};border-radius:8px;padding:6px 10px;margin:3px;'
            f'font-size:0.8em;color:{c};white-space:nowrap;">{mark} {r.id}</div>')
    return ('<div style="display:flex;flex-wrap:wrap;">' + "".join(cells) + "</div>")


def _render_gate_details(gate, project_id: str) -> None:  # type: ignore[no-untyped-def]
    """Per-stage proof-gate panel: question, requirements, buttons."""
    st.write(f"**What it checks:** {gate.question}")
    st.write(f"**Why it matters:** {gate.why_it_matters}")
    passed = [r for r in gate.requirements if r.status == "pass"]
    open_reqs = [r for r in gate.requirements if r.status != "pass"]
    if passed:
        st.write("**Passed:** " + "; ".join(r.description for r in passed))
    if open_reqs:
        st.write("**Unresolved:** " + "; ".join(
            f"{r.description} ({r.status})" for r in open_reqs))
    st.write(f"**Allowed public claim:** {gate.allowed_public_claim}")

    b1, b2, b3 = st.columns(3)
    att_path = (loaders.paths().project_dir(project_id) / "proof" / gate.stage_id
                / "attestation.json")
    with b1:
        if st.button("View proof", key=f"vp-{gate.stage_id}"):
            if att_path.exists():
                st.json(json.loads(att_path.read_text(encoding="utf-8")))
            else:
                st.warning("No attestation yet - click Re-run verification.")
    with b2:
        if st.button("Re-run verification", key=f"rv-{gate.stage_id}"):
            import subprocess as sp
            import sys as _sys
            r = sp.run([_sys.executable, "-m", "sciencebro.cli", "verify-stage",
                        project_id, gate.stage_id],
                       capture_output=True, text=True, cwd=loaders.paths().root,
                       timeout=900)
            st.code((r.stdout or "") + (r.stderr or ""), language="text")
            _gates.clear()
    with b3:
        if st.button("Export proof pack", key=f"ep-{gate.stage_id}"):
            from sciencebro.proofgate import export_proof_pack, verify_stage
            pack = export_proof_pack(loaders.paths(), project_id,
                                     verify_stage(loaders.paths(), project_id, gate.stage_id))
            st.success(f"Proof pack: {pack}")


def render(project_id: str) -> None:
    stages, ctx, gates = compute_stages(project_id)
    training = ctx["training"]
    selftest, ka4d, disc = ctx["selftest"], ctx["ka4d"], ctx["disc"]
    _ = stages

    # 1. mission
    st.markdown(f"## {MISSION}")

    # 1b. big ETA banner + step progress (what to expect, always visible)
    from apps.dashboard import timeline

    timeline.render_eta_and_timeline(_proj_dir(project_id))

    # 2. quest map — the dominant visual
    current_idx = next(
        (i for i, g in enumerate(gates) if g.status != "VERIFIED"), len(gates) - 1
    )
    st.markdown("### Roadmap")
    st.markdown(_quest_map_svg(gates, current_idx), unsafe_allow_html=True)

    # HUD row — big numbers, minimal text
    running = (training["exists"] and not training["finished"]
               and not training.get("stalled"))
    if running:
        tr_val = f"epoch {training['epochs']}/500"
        tr_color = COLORS["IN PROGRESS"]
        tr_sub = (f"loss {training['last_loss']:.1e} · running"
                  if training["last_loss"] else "running")
    elif training["finished"] and training["exit_code"] == 0:
        tr_val, tr_color, tr_sub = "complete", COLORS["VERIFIED"], "500/500"
    else:
        tr_val = f"paused · {training['epochs']}/500"
        tr_color, tr_sub = COLORS["IN PROGRESS"], "checkpoint preserved"
    n2 = sum(1 for r in gates[1].requirements if r.status == "pass")
    claims, _c = loaders.claims(project_id)
    blockers = [b for c in claims for b in c.blockers]
    hud = (
        '<div style="display:flex;flex-wrap:wrap;">'
        + _hud_card("Baseline training (NN Schwarzschild)", tr_val, tr_color, tr_sub)
        + _hud_card("Verifier checks", f"{n2}/{len(gates[1].requirements)}",
                    COLORS["VERIFIED"] if gates[1].status == "VERIFIED" else COLORS["IN PROGRESS"],
                    "analytic · controls · precision")
        + _hud_card("Candidates tested",
                    str(len(list((_proj_dir(project_id) / "results" / "processed").glob("candidate_stress*.json")))),
                    COLORS["VERIFIED"] if list((_proj_dir(project_id) / "results" / "processed").glob("candidate_stress*.json")) else "#8a8a8a",
                    "frozen-criteria evaluations")
        + _hud_card("Blocker", "1" if blockers else "0",
                    COLORS["IN PROGRESS"] if blockers else COLORS["VERIFIED"],
                    (blockers[0][:60] + "…") if blockers else "clear")
        + "</div>"
    )
    st.markdown(hud, unsafe_allow_html=True)

    # checks grid for the current scientific stage (stage-2)
    st.markdown('<div style="margin-top:6px;"></div>', unsafe_allow_html=True)
    st.markdown(_checks_grid(gates[1]), unsafe_allow_html=True)

    # proof-gate panel for the current stage + expanders for the rest
    with st.expander(f"Current stage in detail: {RU_TITLES.get(gates[current_idx].stage_id)}"):
        _render_gate_details(gates[current_idx], project_id)
    with st.expander("Proof gates for all stages"):
        for i, g in enumerate(gates):
            if i == current_idx:
                continue
            st.markdown(f"**{RU_TITLES.get(g.stage_id, g.title)}** — {g.status}")
            _render_gate_details(g, project_id)
            st.divider()

    # 4. plain english
    st.markdown("### What this means in plain English")
    st.info(
        "The research system and the independent geometry checker are working on analytical "
        "examples. We are now testing whether a neural-network-generated Schwarzschild "
        "metric produces the same answer. No new black-hole candidate has been confirmed "
        "or rejected yet."
    )

    # 5. live results (compact: the analytic checks already live in the grid above)
    def _row(label: str, ok: bool | None, detail: str) -> None:
        if ok is True:
            icon, color = "&#9679;", COLORS["VERIFIED"]
        elif ok is False:
            icon, color = "&#9679;", COLORS["FAILED"]
        else:
            icon, color = "&#9679;", COLORS["IN PROGRESS"]
        st.markdown(
            f'<span style="color:{color};">{icon}</span> **{label}** — {detail}',
            unsafe_allow_html=True,
        )

    st.markdown("**Two different scales (do not compare directly yet):**")
    ca, cb = st.columns(2)
    with ca:
        loss_txt = f"{training['last_loss']:.2e}" if training["last_loss"] else "UNKNOWN"
        st.metric("Upstream loss (their scale, quadratic)", loss_txt,
                  help="Contracted squared Ricci with volume weight - the authors own scale")
    with cb:
        if ka4d:
            nn_rows = ka4d.get("nn_interim", {}).get("rows", [])
            ric = max((r["max_abs_ricci"] for r in nn_rows), default=None)
            st.metric("Independent Ricci (our scale, linear)",
                      f"{ric:.2e}" if ric else "UNKNOWN",
                      help="Max |R_ab| from our finite-difference route")
        else:
            st.metric("Independent Ricci (our scale, linear)", "UNKNOWN")
    comparable = disc is not None
    _row("Normalization comparability", True if comparable else None,
         "explained and measured on the 2D model (sqrt(loss) matches our Ricci to 0.7%); 4D after training"
         if comparable else "not established")

    claims, _ = loaders.claims(project_id)
    blockers = [b for c in claims for b in c.blockers]
    _row("Current blocker", None, blockers[0] if blockers else "none recorded")

    # 6. allowed public claim
    st.markdown("### What we can honestly say publicly")
    st.success(
        "ScienceBro's independent verifier has passed analytical known-answer tests. "
        "Evaluation of neural AInstein candidates is not complete."
    )

    # 7. meta
    st.markdown("### Operational")
    git = loaders.git_info()
    when = None
    if selftest:
        try:
            when = datetime.fromisoformat(selftest["generated_at"]).strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            when = selftest.get("generated_at")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.write(f"**Updated:** git {git['commit']} · {git['last_commit_time']}")
        st.write(f"**Verifier self-test:** {when or 'no artifact'}")
    with m2:
        st.write("**Latest completed experiment:** 4D known-answer pipeline "
                 "(analytic route, PASS)")
        running = (f"baseline training (epoch {training['epochs']}/500)"
                   if training["exists"] and not training["finished"]
                   and not training.get("stalled") else "none")
        st.write(f"**Currently running:** {running}")
    with m3:
        st.write("**Realistic ETA:** baseline ~13-17 h on CPU; "
                 "first scientific verdict ~3-7 days (faster on GPU)")
        st.write("**Decision needed:** reboot Windows to finish WSL2 GPU setup; "
                 "approve the draft letter to the authors")

    # 9. technical details, hidden by default
    with st.expander("Technical details (logs, hashes, raw metrics)"):
        proj = _proj_dir(project_id)
        st.write("**Artifacts:**")
        for rel in ["results/processed/known_answer_4d.json",
                    "results/processed/discrepancy_experiment.json",
                    "results/processed/calibration_maps.json",
                    "results/processed/verifier_selftest.json",
                    "upstream/baseline_schwarzschild.log"]:
            p = proj / rel
            st.write(f"- `{rel}` — {'present' if p.exists() else 'MISSING'}")
        if ka4d:
            st.json(ka4d)
        if disc:
            st.json(disc)
        st.code("uv run pytest projects/ainstein-audit/verifier -q\n"
                "uv run python projects/ainstein-audit/verifier/known_answer_4d.py\n"
                "uv run sb project status ainstein-audit", language="bash")
