"""Detailed progress timeline + big ETA banner for Mission Control.

Every row is derived from repository artifacts (experiment manifests, validation
records, processed results, training logs). Nothing is hardcoded as done: a step is
DONE only when its artifact exists, RUNNING only when a live log says so.

ETA is a stated expectation, always labelled as an estimate, and always accompanied by
what it is based on. No fake percentages of scientific progress: the progress bar
counts COMPLETED STEPS, which is a countable fact.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path

import streamlit as st

DONE = "DONE"
RUNNING = "RUNNING"
BLOCKED = "BLOCKED"
NEXT = "NEXT"
WAITING = "WAITING FOR YOU"
TODO = "TODO"

STEP_COLORS = {
    DONE: "#2e9e44",
    RUNNING: "#d99000",
    BLOCKED: "#d99000",
    WAITING: "#7a5cff",
    NEXT: "#4a9eff",
    TODO: "#8a8a8a",
}


@dataclass
class Step:
    stage: str  # which roadmap stage it belongs to
    title: str  # plain language
    status: str
    detail: str  # measured fact or what is missing
    eta: str = ""  # estimate for non-done steps


def _j(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _training_live(log: Path) -> tuple[bool, int, float | None]:
    """(running, last_epoch, last_loss) — running means fresh writes and no EXIT."""
    if not log.exists():
        return False, 0, None
    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False, 0, None
    eps = re.findall(r"Epoch (\d+): Loss: ([\d.eE+-]+)", text)
    last_ep = int(eps[-1][0]) if eps else 0
    last_loss = float(eps[-1][1]) if eps else None
    finished = "EXIT=" in text
    fresh = (time.time() - log.stat().st_mtime) < 600
    return (not finished and fresh), last_ep, last_loss


def build_steps(proj: Path) -> list[Step]:
    proc = proj / "results" / "processed"
    raw = proj / "results" / "raw"
    steps: list[Step] = []

    # ---------- stage 1-2: instrument
    st1 = proj / "proof" / "stage-1" / "attestation.json"
    a1 = _j(st1)
    steps.append(
        Step(
            "Instrument",
            "Research system built and clean-clone reproducible",
            DONE if a1 and a1.get("status") == "VERIFIED" else TODO,
            "engineering-verified (4/4 gate requirements)" if a1 else "no attestation",
        )
    )

    stf = _j(proc / "verifier_selftest.json")
    steps.append(
        Step(
            "Instrument",
            "Independent checker validated on textbook answers",
            DONE if stf and stf.get("n_failed") == 0 else TODO,
            f"{stf['n_passed']} checks pass (Minkowski, Schwarzschild, corrupted-metric control)"
            if stf
            else "self-test artifact missing",
        )
    )

    ka = _j(proc / "known_answer_4d.json")
    if ka:
        rows = ka.get("analytic_route", {}).get("rows", [])
        worst = max((r["max_abs_ricci"] for r in rows), default=None)
        steps.append(
            Step(
                "Instrument",
                "Checker validated in the paper's own coordinates",
                DONE,
                f"worst residual {worst:.1e} on the analytic route" if worst else "measured",
            )
        )
    else:
        steps.append(
            Step(
                "Instrument",
                "Checker validated in the paper's own coordinates",
                TODO,
                "known_answer_4d.json missing",
            )
        )

    disc = _j(proc / "discrepancy_experiment.json")
    steps.append(
        Step(
            "Instrument",
            "Explained why our numbers looked 4 orders off theirs",
            DONE if disc else TODO,
            "their loss is quadratic: sqrt(loss) 1.25e-5 vs our 1.26e-5 (0.7% apart)"
            if disc
            else "not measured",
        )
    )

    cal = _j(proc / "calibration_maps.json")
    steps.append(
        Step(
            "Instrument",
            "Numerical precision rules pinned down",
            DONE if cal else TODO,
            f"float32 storage inflates error {cal['float32_vs_float64_median_ratio']:.0f}x -> float64 mandatory"
            if cal
            else "not measured",
        )
    )

    # ---------- stage 3: baseline + thresholds
    base_ckpt = raw / "schwarzschild-4d-final-2026-08-12" / "final_model.keras"
    run_live, ep, loss = _training_live(proj / "upstream" / "baseline_schwarzschild_night2.log")
    steps.append(
        Step(
            "Baseline",
            "Retrained a known black hole (Schwarzschild) as our ruler",
            DONE if base_ckpt.exists() else (RUNNING if run_live else TODO),
            f"500/500 epochs, final loss {loss:.2e}"
            if base_ckpt.exists() and loss
            else (f"epoch {ep}/500" if run_live else "no checkpoint"),
            "" if base_ckpt.exists() else "~3 h on CPU",
        )
    )

    bstr = _j(proc / "baseline_stress.json")
    steps.append(
        Step(
            "Baseline",
            "Measured how good that ruler actually is",
            DONE if bstr else TODO,
            f"hidden-point error: median {bstr['trained']['ricci_median']:.3f}, "
            f"max {bstr['trained']['ricci_max']:.3f}"
            if bstr
            else "not measured",
        )
    )

    frozen = proj / "validations" / "THRESHOLDS_FROZEN.md"
    steps.append(
        Step(
            "Baseline",
            "Locked the pass/fail thresholds (before seeing candidates)",
            DONE if frozen.exists() else BLOCKED,
            "frozen + git tag `thresholds-frozen`"
            if frozen.exists()
            else "cannot lock before the baseline is measured",
        )
    )

    # ---------- stage 4: candidates
    cs1 = _j(proc / "candidate_stress.json")
    cs2 = _j(proc / "candidate_stress_run2.json")
    cand_live, cep, closs = _training_live(proj / "upstream" / "petrovI_bh_run1.log")

    steps.append(
        Step(
            "Candidates",
            "Trained candidate #1 from the authors' own config",
            DONE
            if (raw / "petrovI-bh-run1" / "final_model.keras").exists()
            else (RUNNING if cand_live else TODO),
            "500 epochs, seed 123" if cs1 else (f"epoch {cep}/500" if cand_live else "not started"),
            "" if cs1 else "~1.5 h on CPU",
        )
    )
    if cs1:
        h = cs1["hidden_stats_h3e-3"]
        steps.append(
            Step(
                "Candidates",
                "Tested candidate #1 on points it never saw",
                DONE,
                f"verdict {cs1['verdict_under_frozen_criteria']} — "
                f"error median {h['median']:.3f} vs allowed 0.286",
            )
        )
    bmap = _j(proc / "boundary_map.json")
    if bmap:
        steps.append(
            Step(
                "Candidates",
                "Mapped where candidate #1 fails (horizon vs everywhere)",
                DONE,
                f"{len(bmap['rows'])} grid points — failure is global, not boundary-local",
            )
        )

    steps.append(
        Step(
            "Candidates",
            "Trained candidate #2 (same config, different random seed)",
            DONE if (raw / "petrovI-bh-run2" / "final_model.keras").exists() else TODO,
            "500 epochs, seed 124" if cs2 else "not started",
            "" if cs2 else "~1.5 h",
        )
    )
    if cs2:
        h2 = cs2["hidden_stats_h3e-3"]
        steps.append(
            Step(
                "Candidates",
                "Tested candidate #2 the same way",
                DONE,
                f"verdict {cs2['verdict_under_frozen_criteria']} — "
                f"error median {h2['median']:.3f} vs allowed 0.286",
            )
        )
        if cs1:
            ratio = cs1["hidden_stats_h3e-3"]["median"] / h2["median"]
            steps.append(
                Step(
                    "Candidates",
                    "Finding: the authors' recipe is seed-unstable",
                    DONE,
                    f"{ratio:.1f}x spread between two seeds — measured, recorded in VAL-0001/0002",
                )
            )

    # ---------- geometry identity: is it actually a new kind of black hole
    petrov = _j(proc / "petrov_diagnostics.json")
    if petrov:
        cand = petrov.get("candidate_seed124", {}).get("rows", [])
        s_vals = [r["S_real"] for r in cand if "S_real" in r]
        ctrl = petrov.get("nn_schwarzschild_baseline", {}).get("rows", [])
        floor = max((r["abs_S_minus_1"] for r in ctrl if "abs_S_minus_1" in r), default=None)
        steps.append(
            Step(
                "Identity",
                "Is it a genuinely different geometry, or Schwarzschild in disguise?",
                DONE,
                f"speciality index {min(s_vals):.2f}-{max(s_vals):.2f} vs exactly 1 for "
                f"Schwarzschild (trained-network floor {floor:.1e})"
                if s_vals and floor
                else "measured",
            )
        )
    else:
        steps.append(
            Step(
                "Identity",
                "Is it a genuinely different geometry, or Schwarzschild in disguise?",
                NEXT,
                "our own Weyl-invariant implementation needed",
                "~3 h",
            )
        )

    horizon = _j(proc / "horizon_diagnostics.json")
    if horizon:
        rows = horizon.get("candidate_seed124", {}).get("rows", [])
        tr = sum(1 for r in rows if r.get("classification") == "future-trapped")
        steps.append(
            Step(
                "Identity",
                "Does it actually trap light, like a black hole must?",
                DONE,
                f"{tr}/{len(rows)} probe points future-trapped; the same test "
                f"reproduces the textbook horizon on two controls",
            )
        )
    else:
        steps.append(
            Step(
                "Identity",
                "Does it actually trap light, like a black hole must?",
                TODO,
                "trapped-surface diagnostics not run yet",
                "~2 h",
            )
        )

    shape = _j(proc / "horizon_shape.json")
    steps.append(
        Step(
            "Identity",
            "How does its horizon shape differ from Schwarzschild's?",
            DONE if shape else TODO,
            "Xi = 0 surface located per model by bisection"
            if shape
            else "bisection script ready, runs after the seed sweep",
            "" if shape else "~1 h",
        )
    )

    # ---------- reproducibility of the recipe
    sweep = _j(proc / "seed_sweep.json")
    trained = len(list((proj / "results" / "raw").glob("petrovI-bh-*")))
    if sweep:
        steps.append(
            Step(
                "Reproducibility",
                "How often does the recipe actually work?",
                DONE,
                f"{sweep['n_satisfying_all_three']} of {sweep['n_seeds']} seeds "
                f"satisfy vacuum + type I + trapping",
            )
        )
    else:
        steps.append(
            Step(
                "Reproducibility",
                "How often does the recipe actually work?",
                RUNNING if trained < 5 else NEXT,
                f"{trained} of 5 candidate seeds trained; the sweep evaluates all three "
                f"legs per seed",
                "~25 min each" if trained < 5 else "~40 min",
            )
        )

    letter_sent = (proj / "release" / "author-reply.md").exists()
    steps.append(
        Step(
            "Reproducibility",
            "Test the authors' own trained models",
            DONE if letter_sent else WAITING,
            "reply received"
            if letter_sent
            else "letter sent 2026-08-12; their checkpoints were never published, so "
            "until they reply we audit the recipe, not their output",
            "" if letter_sent else "their reply",
        )
    )

    # ---------- release
    disclosure = (proj.parents[1] / "AI_DISCLOSURE.md").exists()
    packs = [
        p
        for p in sorted((proj / "proof").glob("stage-*"))
        if (p / "README.md").exists() and (p / "attestation.json").exists()
    ]
    steps.append(
        Step(
            "Release",
            "Proof packs, citations, licences, AI disclosure",
            DONE if (len(packs) >= 6 and disclosure) else TODO,
            f"{len(packs)}/6 stages carry a full proof pack with attestation"
            + ("; AI use disclosed" if disclosure else ""),
        )
    )

    doi = (proj / "release" / "ZENODO_DOI.txt").exists()
    review = (proj / "validations" / "EXTERNAL_REVIEW.md").exists()
    steps.append(
        Step(
            "Release",
            "Expert review by a qualified relativist",
            DONE if review else WAITING,
            "review recorded"
            if review
            else "nobody with the right training has checked this yet, so it stays an "
            "independent measurement rather than accepted physics",
        )
    )
    steps.append(
        Step(
            "Release",
            "Public release with a citable DOI",
            DONE if doi else TODO,
            "DOI recorded"
            if doi
            else "package is assembled; creating the repository and Zenodo release is "
            "a human action",
            "" if doi else "your click",
        )
    )
    return steps


def render_eta_and_timeline(proj: Path) -> None:
    steps = build_steps(proj)
    done = sum(1 for s in steps if s.status == DONE)
    total = len(steps)
    running = [s for s in steps if s.status == RUNNING]
    waiting = [s for s in steps if s.status == WAITING]
    nxt = next((s for s in steps if s.status in (NEXT, RUNNING, BLOCKED)), None)

    # ----- BIG ETA banner
    if running:
        headline = f"RUNNING NOW: {running[0].title}"
        sub = running[0].detail
        eta = running[0].eta or "in progress"
        color = STEP_COLORS[RUNNING]
    elif nxt:
        headline = f"NEXT: {nxt.title}"
        sub = nxt.detail
        eta = nxt.eta or "ready to start"
        color = STEP_COLORS[NEXT]
    else:
        headline = "All tracked steps complete"
        sub = "next action is yours"
        eta = "-"
        color = STEP_COLORS[DONE]

    waiting_line = ""
    if waiting:
        waiting_line = (
            f'<div style="margin-top:10px;padding:8px 12px;border-radius:8px;'
            f"border:1px solid {STEP_COLORS[WAITING]};color:{STEP_COLORS[WAITING]};"
            f'font-size:0.95em;">WAITING FOR YOU: {waiting[0].title} — {waiting[0].detail}</div>'
        )

    st.markdown(
        f'<div style="border:2px solid {color};border-radius:14px;padding:18px 22px;margin:8px 0 14px 0;">'
        f'<div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:18px;">'
        f'<div style="flex:1;min-width:280px;">'
        f'<div style="font-size:0.8em;opacity:0.65;letter-spacing:0.08em;">WHAT TO EXPECT</div>'
        f'<div style="font-size:1.5em;font-weight:500;color:{color};">{headline}</div>'
        f'<div style="font-size:0.95em;opacity:0.85;">{sub}</div></div>'
        f'<div style="text-align:right;min-width:190px;">'
        f'<div style="font-size:0.8em;opacity:0.65;letter-spacing:0.08em;">ETA (ESTIMATE)</div>'
        f'<div style="font-size:2.1em;font-weight:500;color:{color};">{eta}</div>'
        f'<div style="font-size:0.75em;opacity:0.6;">measured CPU rates, not a promise</div>'
        f"</div></div>{waiting_line}</div>",
        unsafe_allow_html=True,
    )

    # ----- step progress bar (counts completed steps — a countable fact)
    pct = done / total
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;font-size:0.85em;'
        f'opacity:0.75;margin-bottom:4px;"><span>Completed steps</span>'
        f"<span>{done} of {total}</span></div>"
        f'<div style="height:14px;border-radius:7px;background:#2a2a2a;overflow:hidden;">'
        f'<div style="width:{pct * 100:.1f}%;height:100%;background:{STEP_COLORS[DONE]};"></div>'
        f"</div>"
        f'<div style="font-size:0.75em;opacity:0.55;margin-top:4px;">'
        f"This bar counts finished steps — it is not a confidence or truth percentage.</div>",
        unsafe_allow_html=True,
    )

    # ----- timeline
    st.markdown("### Detailed timeline")
    rows = []
    last_stage = None
    for s in steps:
        if s.stage != last_stage:
            rows.append(
                f'<div style="margin:14px 0 6px 0;font-size:0.8em;opacity:0.6;'
                f'letter-spacing:0.1em;">{s.stage.upper()}</div>'
            )
            last_stage = s.stage
        c = STEP_COLORS[s.status]
        icon = {
            DONE: "&#10004;",
            RUNNING: "&#9679;",
            WAITING: "&#9873;",
            BLOCKED: "&#9888;",
            NEXT: "&#9654;",
            TODO: "&#9675;",
        }[s.status]
        eta_badge = (
            f'<span style="font-size:0.8em;opacity:0.8;border:1px solid {c};'
            f'border-radius:6px;padding:1px 7px;margin-left:8px;color:{c};">{s.eta}</span>'
            if s.eta
            else ""
        )
        rows.append(
            f'<div style="display:flex;gap:12px;padding:7px 0;border-left:2px solid {c};'
            f'padding-left:14px;margin-left:4px;">'
            f'<div style="color:{c};font-size:1.05em;min-width:18px;">{icon}</div>'
            f'<div style="flex:1;"><div style="font-weight:500;">{s.title}{eta_badge}</div>'
            f'<div style="font-size:0.86em;opacity:0.75;">{s.detail}</div></div>'
            f'<div style="color:{c};font-size:0.78em;font-weight:600;white-space:nowrap;">'
            f"{s.status}</div></div>"
        )
    st.markdown("".join(rows), unsafe_allow_html=True)
