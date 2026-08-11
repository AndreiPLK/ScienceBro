"""The `sb` command-line interface (roadmap §12).

Rules honored: --help everywhere (Typer default), non-zero exit on failed gates,
mutating commands print changed files, no fabricated data.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from sciencebro.config import RepoPaths
from sciencebro.doctor import run_doctor
from sciencebro.evidence import audit_evidence
from sciencebro.registry import load_topics
from sciencebro.schemas import ClaimState, allowed_claim_promotion
from sciencebro.status import compute_status
from sciencebro.store import ProjectStore, StoreError, save_yaml_model

app = typer.Typer(help="ScienceBro: local-first computational research workbench.", no_args_is_help=True)
topic_app = typer.Typer(help="Research topic registry.", no_args_is_help=True)
project_app = typer.Typer(help="Project operations.", no_args_is_help=True)
evidence_app = typer.Typer(help="Evidence operations.", no_args_is_help=True)
hypothesis_app = typer.Typer(help="Hypothesis operations.", no_args_is_help=True)
claim_app = typer.Typer(help="Claim ledger operations.", no_args_is_help=True)
release_app = typer.Typer(help="Release gate.", no_args_is_help=True)
app.add_typer(topic_app, name="topic")
app.add_typer(project_app, name="project")
app.add_typer(evidence_app, name="evidence")
app.add_typer(hypothesis_app, name="hypothesis")
app.add_typer(claim_app, name="claim")
app.add_typer(release_app, name="release")

console = Console()


def _paths() -> RepoPaths:
    return RepoPaths()


# ---------------------------------------------------------------- doctor

@app.command()
def doctor(as_json: bool = typer.Option(False, "--json", help="JSON output for CI")) -> None:
    """Diagnose the environment. Fails (exit 1) when a required check fails."""
    rep = run_doctor()
    if as_json:
        print(json.dumps([c.__dict__ for c in rep.checks], indent=2))
    else:
        table = Table(title="sb doctor")
        table.add_column("check")
        table.add_column("status")
        table.add_column("detail")
        for c in rep.checks:
            mark = "[green]ok[/green]" if c.ok else ("[red]FAIL[/red]" if c.required else "[yellow]missing[/yellow]")
            table.add_row(c.name, mark, c.detail)
        console.print(table)
        if not rep.ok:
            console.print("[red]Blockers:[/red]")
            for b in rep.blockers:
                console.print(f"  - {b}")
    raise typer.Exit(0 if rep.ok else 1)


# ---------------------------------------------------------------- topics

@topic_app.command("list")
def topic_list() -> None:
    """List research topics from registry/topics.yaml."""
    topics = load_topics(_paths().registry / "topics.yaml")
    if not topics:
        console.print("[yellow]no topics found in registry/topics.yaml[/yellow]")
        raise typer.Exit(1)
    table = Table(title="Research opportunity backlog")
    for col in ("rank", "id", "domain", "readiness", "one-week artifact"):
        table.add_column(col)
    for t in topics:
        table.add_row(str(t.rank), t.id, t.domain, t.readiness, t.one_week_artifact)
    console.print(table)


@topic_app.command("show")
def topic_show(topic_id: str) -> None:
    """Show one topic in full."""
    topics = {t.id: t for t in load_topics(_paths().registry / "topics.yaml")}
    if topic_id not in topics:
        console.print(f"[red]unknown topic {topic_id}[/red]")
        raise typer.Exit(1)
    console.print_json(topics[topic_id].model_dump_json(indent=2))


# ---------------------------------------------------------------- project

@project_app.command("status")
def project_status(
    project_id: str,
    as_json: bool = typer.Option(False, "--json", help="JSON output for CI"),
) -> None:
    """Show the computed, file-derived status of a project."""
    st = compute_status(_paths(), project_id)
    if as_json:
        print(json.dumps(st.__dict__, indent=2, default=str))
        raise typer.Exit(1 if st.errors else 0)
    console.print(f"[bold]{st.title or st.project_id}[/bold]  stage: {st.stage}")
    console.print(f"question: {st.question}")
    table = Table(show_header=False)
    table.add_column("k")
    table.add_column("v")
    table.add_row("evidence", f"{st.evidence_total} total / {st.evidence_full_text} full-text")
    table.add_row("claims", f"{st.claims_total} total / {st.claims_supported} supported")
    table.add_row("hypotheses", f"{st.hypotheses} total / {st.hypotheses_frozen} frozen")
    table.add_row("experiments", f"{st.experiments} total / {st.experiments_frozen} frozen+")
    table.add_row(
        "validation",
        f"pass {st.validations_pass} / fail {st.validations_fail} / "
        f"inconclusive {st.validations_inconclusive} / pending {st.validations_pending}",
    )
    console.print(table)
    if st.claims_unsupported:
        console.print(f"[yellow]unsupported claims:[/yellow] {', '.join(st.claims_unsupported)}")
    for b in st.blockers:
        console.print(f"[yellow]blocker:[/yellow] {b}")
    for e in st.errors:
        console.print(f"[red]error:[/red] {e}")
    console.print(f"[bold cyan]next action:[/bold cyan] {st.next_action}")
    raise typer.Exit(1 if st.errors else 0)


@project_app.command("list")
def project_list() -> None:
    """List projects."""
    for pid in _paths().list_projects():
        console.print(pid)


# ---------------------------------------------------------------- evidence

@evidence_app.command("audit")
def evidence_audit(project_id: str) -> None:
    """Audit evidence/claims consistency. Non-zero exit when rules are violated."""
    store = ProjectStore(_paths(), project_id)
    try:
        audit = audit_evidence(store.claims(), store.evidence())
    except StoreError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1) from None
    for f in audit.findings:
        console.print(f"[red]finding:[/red] {f}")
    for w in audit.warnings:
        console.print(f"[yellow]warning:[/yellow] {w}")
    if audit.ok:
        console.print("[green]evidence audit passed[/green]")
    raise typer.Exit(0 if audit.ok else 1)


# ---------------------------------------------------------------- hypotheses

@hypothesis_app.command("list")
def hypothesis_list(project_id: str) -> None:
    """List hypotheses with freeze state."""
    store = ProjectStore(_paths(), project_id)
    for h in store.hypotheses():
        console.print(f"{h.id} [{h.status}] metric={h.primary_metric}: {h.statement[:90]}")


@hypothesis_app.command("freeze")
def hypothesis_freeze(project_id: str, hypothesis_id: str) -> None:
    """Freeze a hypothesis (mutating; prints the changed file)."""
    paths = _paths()
    store = ProjectStore(paths, project_id)
    hs = store.hypotheses()
    target = next((h for h in hs if h.id == hypothesis_id), None)
    if target is None:
        console.print(f"[red]unknown hypothesis {hypothesis_id}[/red]")
        raise typer.Exit(1)
    if target.status == "frozen":
        console.print("already frozen")
        raise typer.Exit(0)
    target.status = "frozen"
    path = paths.hypotheses_dir(project_id) / f"{hypothesis_id}.yaml"
    save_yaml_model(path, target)
    console.print(f"changed: {path}")


# ---------------------------------------------------------------- claims

@claim_app.command("list")
def claim_list(project_id: str) -> None:
    """List claims with states and blockers."""
    store = ProjectStore(_paths(), project_id)
    claims = store.claims()
    if not claims:
        console.print("no claims recorded")
        return
    evidence = store.evidence()
    validations = store.validations()
    table = Table(title=f"Claim ledger: {project_id}")
    for col in ("id", "state", "evidence", "next-state blockers"):
        table.add_column(col)
    order = [
        ClaimState.source_supported,
        ClaimState.experimentally_supported,
        ClaimState.independently_validated,
        ClaimState.release_ready,
    ]
    for c in claims:
        # next target = the state after the current one in canonical order
        values = [s.value for s in order]
        idx = values.index(c.state.value) if c.state.value in values else -1
        target = order[idx + 1] if 0 <= idx < len(order) - 1 else order[0] if idx == -1 else ClaimState.release_ready
        blockers = allowed_claim_promotion(c, target, evidence, validations)
        table.add_row(c.id, c.state.value, ",".join(c.evidence_ids) or "-",
                      f"→{target.value}: " + ("; ".join(blockers) if blockers else "none"))
    console.print(table)


@claim_app.command("promote")
def claim_promote(project_id: str, claim_id: str, target_state: str) -> None:
    """Promote a claim through the deterministic gate. Fails closed."""
    store = ProjectStore(_paths(), project_id)
    claims = store.claims()
    claim = next((c for c in claims if c.id == claim_id), None)
    if claim is None:
        console.print(f"[red]unknown claim {claim_id}[/red]")
        raise typer.Exit(1)
    try:
        target = ClaimState(target_state)
    except ValueError:
        console.print(f"[red]invalid state {target_state}; allowed: {[s.value for s in ClaimState]}[/red]")
        raise typer.Exit(1) from None
    blockers = allowed_claim_promotion(claim, target, store.evidence(), store.validations())
    if blockers:
        console.print("[red]promotion blocked:[/red]")
        for b in blockers:
            console.print(f"  - {b}")
        raise typer.Exit(1)
    claim.state = target
    store.save_claims(claims)
    console.print(f"changed: {_paths().claims_file(project_id)}")
    console.print(f"[green]{claim_id} → {target.value}[/green]")


# ---------------------------------------------------------------- release

@release_app.command("check")
def release_check(project_id: str) -> None:
    """Dry-run the release gate: lists exact blockers, exit 1 while any remain."""
    paths = _paths()
    store = ProjectStore(paths, project_id)
    blockers: list[str] = []
    try:
        claims = store.claims()
        evidence = store.evidence()
        validations = store.validations()
    except StoreError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1) from None
    release_claims = [c for c in claims if c.state == ClaimState.release_ready]
    if not release_claims:
        blockers.append("no claim has reached release-ready")
    for c in claims:
        bs = allowed_claim_promotion(c, ClaimState.release_ready, evidence, validations)
        if bs and c.state != ClaimState.refuted:
            blockers.append(f"{c.id}: " + "; ".join(bs))
    for fname in ("README.md", "LICENSE", "CITATION.cff"):
        if not (paths.root / fname).exists():
            blockers.append(f"missing {fname}")
    proj_dir = paths.project_dir(project_id)
    for sub in ("reports", "results"):
        if not (proj_dir / sub).is_dir():
            blockers.append(f"missing {proj_dir / sub}")
    if blockers:
        console.print("[red]release blocked:[/red]")
        for b in blockers:
            console.print(f"  - {b}")
        raise typer.Exit(1)
    console.print("[green]release gate passed (human approval still required to publish)[/green]")


# ---------------------------------------------------------------- proof gates

proof_app = typer.Typer(help="Proof packs and attestations.", no_args_is_help=True)
app.add_typer(proof_app, name="proof")


def _print_gate(gate) -> None:  # type: ignore[no-untyped-def]
    color = {"VERIFIED": "green", "FAILED": "red"}.get(gate.status, "yellow")
    label = " (ENGINEERING)" if gate.label == "ENGINEERING" else ""
    console.print(f"[bold]{gate.stage_id}: {gate.title}[/bold] — [{color}]{gate.status}[/{color}]{label}")
    for r in gate.requirements:
        mark = {"pass": "[green]PASS[/green]", "fail": "[red]FAIL[/red]",
                "missing": "[yellow]MISSING[/yellow]"}[r.status]
        console.print(f"  {mark} {r.description}" + (f" — {r.measured}" if r.measured else ""))


@app.command("verify-stage")
def verify_stage_cmd(project_id: str, stage_id: str) -> None:
    """Verify one proof-gate stage against repository artifacts. Exit 1 unless VERIFIED."""
    from sciencebro.proofgate import verify_stage, write_attestation

    gate = verify_stage(_paths(), project_id, stage_id)
    _print_gate(gate)
    path = write_attestation(_paths(), project_id, gate)
    console.print(f"attestation: {path}")
    raise typer.Exit(0 if gate.status == "VERIFIED" else 1)


@app.command("verify-all")
def verify_all_cmd(project_id: str) -> None:
    """Verify every stage. Exit 1 if any mandatory stage-1/2 requirement fails."""
    from sciencebro.proofgate import verify_all, write_attestation

    gates = verify_all(_paths(), project_id)
    for g in gates:
        _print_gate(g)
        write_attestation(_paths(), project_id, g)
    bad = [g for g in gates if g.status == "FAILED"]
    raise typer.Exit(1 if bad else 0)


@proof_app.command("show")
def proof_show(project_id: str, stage_id: str) -> None:
    """Show the stored attestation for a stage."""
    path = _paths().project_dir(project_id) / "proof" / stage_id / "attestation.json"
    if not path.exists():
        console.print(f"[red]no attestation at {path}[/red]")
        raise typer.Exit(1)
    console.print_json(path.read_text(encoding="utf-8"))


@proof_app.command("export")
def proof_export(project_id: str, stage_id: str) -> None:
    """Export the proof pack for a stage (works even when status is not VERIFIED)."""
    from sciencebro.proofgate import export_proof_pack, verify_stage

    gate = verify_stage(_paths(), project_id, stage_id)
    pack = export_proof_pack(_paths(), project_id, gate)
    console.print(f"proof pack: {pack} (status: {gate.status})")
    for f in sorted(pack.iterdir()):
        console.print(f"  {f.name}")


@proof_app.command("verify-integrity")
def proof_verify_integrity(proof_pack: str) -> None:
    """Recompute artifact hashes of a proof pack's attestation. Exit 1 on any change."""
    from sciencebro.proofgate import check_attestation_integrity

    att = Path(proof_pack)
    if att.is_dir():
        att = att / "attestation.json"
    problems = check_attestation_integrity(att)
    if problems:
        for p in problems:
            console.print(f"[red]{p}[/red]")
        raise typer.Exit(1)
    console.print("[green]attestation intact: all artifact hashes match[/green]")


# ---------------------------------------------------------------- check / dashboard

@app.command()
def check() -> None:
    """Aggregate check: lint, types, tests, schema/project integrity (roadmap §21)."""
    root = _paths().root
    failures: list[str] = []

    def run(name: str, cmd: list[str]) -> None:
        console.print(f"[bold]== {name}[/bold]: {' '.join(cmd)}")
        r = subprocess.run(cmd, cwd=root)
        if r.returncode != 0:
            failures.append(name)

    run("ruff", [sys.executable, "-m", "ruff", "check", "."])
    run("mypy", [sys.executable, "-m", "mypy", "sciencebro"])
    run("pytest", [sys.executable, "-m", "pytest"])

    console.print("[bold]== project integrity[/bold]")
    paths = _paths()
    try:
        load_topics(paths.registry / "topics.yaml")
        console.print("topics.yaml: ok")
    except StoreError as e:
        console.print(f"[red]{e}[/red]")
        failures.append("topics")
    for pid in paths.list_projects():
        st = compute_status(paths, pid)
        if st.errors:
            for msg in st.errors:
                console.print(f"[red]{pid}: {msg}[/red]")
            failures.append(f"project:{pid}")
        else:
            console.print(f"project {pid}: ok")

    if failures:
        console.print(f"[red]sb check FAILED:[/red] {', '.join(failures)}")
        raise typer.Exit(1)
    console.print("[green]sb check passed[/green]")


@app.command()
def dashboard() -> None:
    """Start the local Streamlit dashboard."""
    root = _paths().root
    app_path = root / "apps" / "dashboard" / "app.py"
    if not app_path.exists():
        console.print(f"[red]dashboard not found at {app_path}[/red]")
        raise typer.Exit(1)
    raise typer.Exit(
        subprocess.call([sys.executable, "-m", "streamlit", "run", str(app_path)], cwd=root)
    )


def main() -> None:  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
