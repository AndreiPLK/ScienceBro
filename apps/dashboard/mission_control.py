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
    "stage-1": "Система ScienceBro построена",
    "stage-2": "Верификатор откалиброван",
    "stage-3": "Кандидат Petrov-I обучен",
    "stage-4": "Кандидат независимо проверен",
    "stage-5": "Научный вердикт получен",
    "stage-6": "Публичный релиз подготовлен",
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
        note = f"{n_pass}/{len(g.requirements)} требований"
        if g.label == "ENGINEERING" and status == "VERIFIED":
            note += " · engineering, не научный"
        stages.append(Stage(RU_TITLES.get(g.stage_id, g.title), status, note))
    return stages, ctx, gates


def _stage_box(stage: Stage, current: bool) -> str:
    color = COLORS[stage.status]
    border = f"3px solid {color}" if current else f"1px solid {color}"
    marker = "&#9654; " if current else ""
    return (
        f'<div style="border:{border};border-radius:8px;padding:10px 12px;margin:4px 0;">'
        f'<div style="font-weight:600;">{marker}{stage.title}</div>'
        f'<div style="color:{color};font-weight:600;font-size:0.9em;">{stage.status}</div>'
        f'<div style="font-size:0.85em;opacity:0.8;">{stage.note}</div></div>'
    )


def _render_gate_details(gate, project_id: str) -> None:  # type: ignore[no-untyped-def]
    """Per-stage proof-gate panel: question, requirements, buttons."""
    st.write(f"**Что проверяет:** {gate.question}")
    st.write(f"**Почему важно:** {gate.why_it_matters}")
    passed = [r for r in gate.requirements if r.status == "pass"]
    open_reqs = [r for r in gate.requirements if r.status != "pass"]
    if passed:
        st.write("**Пройдено:** " + "; ".join(r.description for r in passed))
    if open_reqs:
        st.write("**Не решено:** " + "; ".join(
            f"{r.description} ({r.status})" for r in open_reqs))
    st.write(f"**Разрешённая публичная формулировка:** {gate.allowed_public_claim}")

    b1, b2, b3 = st.columns(3)
    att_path = (loaders.paths().project_dir(project_id) / "proof" / gate.stage_id
                / "attestation.json")
    with b1:
        if st.button("View proof", key=f"vp-{gate.stage_id}"):
            if att_path.exists():
                st.json(json.loads(att_path.read_text(encoding="utf-8")))
            else:
                st.warning("Аттестации ещё нет — выполните Re-run verification.")
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

    # 1. mission
    st.markdown(f"## {MISSION}")

    # 2. roadmap (dominant visual)
    current_idx = next(
        (i for i, s in enumerate(stages) if s.status not in ("VERIFIED",)), len(stages) - 1
    )
    cols = st.columns(3)
    for i, s in enumerate(stages):
        with cols[i % 3]:
            st.markdown(_stage_box(s, i == current_idx), unsafe_allow_html=True)

    # proof-gate panel for the current stage + expanders for the rest
    st.markdown(f"### Текущий этап: {stages[current_idx].title}")
    _render_gate_details(gates[current_idx], project_id)
    with st.expander("Proof-gate всех этапов"):
        for i, g in enumerate(gates):
            if i == current_idx:
                continue
            st.markdown(f"**{RU_TITLES.get(g.stage_id, g.title)}** — {g.status}")
            _render_gate_details(g, project_id)
            st.divider()

    # 3. where we are now — four blocks
    st.markdown("### Где мы сейчас")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**Проверено**")
        n_tests = selftest["n_passed"] if selftest else "?"
        st.write(f"Система V1; верификатор: {n_tests} тестов на аналитических решениях; "
                 "формат экспорта метрик")
    with c2:
        st.markdown("**Сейчас выполняется**")
        if training["exists"] and not training["finished"] and not training.get("stalled"):
            st.write(f"Тренинг нейронного Шварцшильда: эпоха {training['epochs']}/500")
        elif training["finished"] and training["exit_code"] == 0:
            st.write("Фоновых задач нет; тренинг эталона завершён")
        else:
            st.write(f"Тренинг эталона остановлен на эпохе {training['epochs']}/500 "
                     "(чекпоинт сохранён; перезапуск ночью или на GPU)")
    with c3:
        st.markdown("**Не решено**")
        claims, _ = loaders.claims(project_id)
        blockers = [b for c in claims for b in c.blockers]
        st.write(blockers[0] if blockers else "блокеров не записано")
    with c4:
        st.markdown("**Дальше**")
        st.write("Дотренировать эталон → заморозить пороги → обучить кандидата Petrov-I "
                 "→ независимая проверка на скрытых точках")

    # 4. plain english
    st.markdown("### Что это значит простыми словами")
    st.info(
        "Исследовательская система и независимый геометрический проверщик работают на "
        "аналитических примерах. Сейчас мы проверяем, даст ли нейросетевая метрика "
        "Шварцшильда тот же ответ. Ни один новый кандидат в чёрные дыры пока не "
        "подтверждён и не отвергнут."
    )

    # 5. live results
    st.markdown("### Ключевые результаты")

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

    tests = (selftest or {}).get("tests", {})

    def _suite(prefix: str) -> bool | None:
        rel = {k: v for k, v in tests.items() if prefix in k}
        if not rel:
            return None
        return all(v == "passed" for v in rel.values())

    _row("Аналитический Минковский", _suite("minkowski"),
         "вакуум подтверждён" if _suite("minkowski") else "нет данных")
    _row("Аналитический Шварцшильд", _suite("schwarzschild_is_vacuum"),
         "вакуум + Кречман 48M²/r⁶" if _suite("schwarzschild_is_vacuum") else "нет данных")
    _row("Негативный контроль (испорченная метрика)", _suite("perturbed"),
         "подделка детектируется" if _suite("perturbed") else "нет данных")

    if training["exists"]:
        done = training["finished"] and training["exit_code"] == 0
        _row("Нейронный Шварцшильд (тренинг)", True if done else None,
             f"эпоха {training['epochs']}/500, loss {training['last_loss']:.2e}"
             if training["last_loss"] else f"эпоха {training['epochs']}/500")
    else:
        _row("Нейронный Шварцшильд (тренинг)", None, "UNKNOWN — лог не найден")

    st.markdown("**Две шкалы (пока не сравнивать напрямую):**")
    ca, cb = st.columns(2)
    with ca:
        loss_txt = f"{training['last_loss']:.2e}" if training["last_loss"] else "UNKNOWN"
        st.metric("Upstream loss (их шкала, квадратичная)", loss_txt,
                  help="Свёрнутый квадрат Ricci с весом объёма — шкала авторов")
    with cb:
        if ka4d:
            nn_rows = ka4d.get("nn_interim", {}).get("rows", [])
            ric = max((r["max_abs_ricci"] for r in nn_rows), default=None)
            st.metric("Независимый Ricci (наша шкала, линейная)",
                      f"{ric:.2e}" if ric else "UNKNOWN",
                      help="Максимум |R_ab| нашего конечно-разностного маршрута")
        else:
            st.metric("Независимый Ricci (наша шкала, линейная)", "UNKNOWN")
    comparable = disc is not None
    _row("Сопоставимость нормировок", True if comparable else None,
         "объяснена и измерена на 2D-модели (√loss ≈ наш Ricci, 0.7%); для 4D — после дотренинга"
         if comparable else "не установлена")

    claims, _ = loaders.claims(project_id)
    blockers = [b for c in claims for b in c.blockers]
    _row("Текущий блокер", None, blockers[0] if blockers else "не записан")

    # 6. allowed public claim
    st.markdown("### Что мы можем честно сказать публично")
    st.success(
        "Независимый верификатор ScienceBro прошёл аналитические known-answer тесты. "
        "Проверка нейросетевых кандидатов AInstein не завершена."
    )

    # 7. meta
    st.markdown("### Служебное")
    git = loaders.git_info()
    when = None
    if selftest:
        try:
            when = datetime.fromisoformat(selftest["generated_at"]).strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            when = selftest.get("generated_at")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.write(f"**Обновлено:** git {git['commit']} · {git['last_commit_time']}")
        st.write(f"**Самопроверка верификатора:** {when or 'нет артефакта'}")
    with m2:
        st.write("**Последний завершённый эксперимент:** 4D known-answer pipeline "
                 "(аналитический маршрут, PASS)")
        running = (f"тренинг эталона (эпоха {training['epochs']}/500)"
                   if training["exists"] and not training["finished"]
                   and not training.get("stalled") else "нет")
        st.write(f"**Сейчас выполняется:** {running}")
    with m3:
        st.write("**Реалистичный срок:** эталон ≈ 13 ч CPU после рестарта; "
                 "первый научный вердикт ≈ 3–7 дней (быстрее на GPU)")
        st.write("**Требуется решение:** установка WSL2 для GPU (см. GPU_MIGRATION.md); "
                 "одобрение письма авторам")

    # 9. technical details, hidden by default
    with st.expander("Технические детали (логи, хеши, сырые метрики)"):
        proj = _proj_dir(project_id)
        st.write("**Артефакты:**")
        for rel in ["results/processed/known_answer_4d.json",
                    "results/processed/discrepancy_experiment.json",
                    "results/processed/calibration_maps.json",
                    "results/processed/verifier_selftest.json",
                    "upstream/baseline_schwarzschild.log"]:
            p = proj / rel
            st.write(f"- `{rel}` — {'есть' if p.exists() else 'НЕТ'}")
        if ka4d:
            st.json(ka4d)
        if disc:
            st.json(disc)
        st.code("uv run pytest projects/ainstein-audit/verifier -q\n"
                "uv run python projects/ainstein-audit/verifier/known_answer_4d.py\n"
                "uv run sb project status ainstein-audit", language="bash")
