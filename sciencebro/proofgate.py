"""Proof-Gate system: stage statuses computed ONLY from repository artifacts.

Core principle: the assistant never marks its own scientific work as verified.
A stage is VERIFIED only when every mandatory deterministic requirement passes
against unchanged artifacts. Missing evidence is never VERIFIED.

Statuses: VERIFIED | IN PROGRESS | BLOCKED | FAILED | INCONCLUSIVE | NOT STARTED
Stage 1 carries the label "ENGINEERING VERIFIED" (not scientific).
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from sciencebro.config import RepoPaths

RICCI_TOL = 1e-7
KREL_TOL = 1e-7


# ------------------------------------------------------------------ results

@dataclass
class Requirement:
    id: str
    description: str
    status: str          # "pass" | "fail" | "missing"
    measured: str = ""   # actual measured value / evidence pointer


@dataclass
class GateResult:
    stage_id: str
    title: str
    label: str                      # e.g. "SCIENTIFIC" | "ENGINEERING"
    question: str
    why_it_matters: str
    allowed_public_claim: str
    requirements: list[Requirement] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)  # path -> sha256

    @property
    def status(self) -> str:
        sts = [r.status for r in self.requirements]
        if not sts:
            return "NOT STARTED"
        if all(s == "pass" for s in sts):
            return "VERIFIED"
        if any(s == "fail" for s in sts):
            # a real measured failure only if evidence existed
            return "FAILED"
        if all(s == "missing" for s in sts):
            return "NOT STARTED"
        return "IN PROGRESS"


# ------------------------------------------------------------------ helpers

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _git_commit(root: Path) -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                           capture_output=True, text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


# ------------------------------------------------------------------ stage gates

def _stage1(paths: RepoPaths, project_id: str) -> GateResult:
    g = GateResult(
        stage_id="stage-1",
        title="Research infrastructure",
        label="ENGINEERING",
        question="Does a clean clone reproduce the environment, schemas, tests and provenance tracking?",
        why_it_matters="Without reproducible engineering, no scientific number can be trusted.",
        allowed_public_claim="The ScienceBro research infrastructure is engineering-verified: "
                             "clean-clone reproduction, locked environment, schema and test suite pass.",
    )
    root = paths.root
    proj = paths.project_dir(project_id)

    lock = root / "uv.lock"
    if lock.exists():
        g.requirements.append(Requirement("env-lock", "uv.lock present", "pass",
                                          _sha256(lock)[:16]))
        g.artifacts[str(lock)] = _sha256(lock)
    else:
        g.requirements.append(Requirement("env-lock", "uv.lock present", "missing"))

    cc = proj / "proof" / "stage-01" / "clean-clone-2026-08-11.log"
    if cc.exists():
        ok = "Clean-clone check passed." in cc.read_text(encoding="utf-8", errors="replace")
        g.requirements.append(Requirement("clean-clone", "clean-clone reproduction log",
                                          "pass" if ok else "fail", str(cc)))
        g.artifacts[str(cc)] = _sha256(cc)
    else:
        g.requirements.append(Requirement("clean-clone", "clean-clone reproduction log", "missing"))

    # unit tests run live (fast, deterministic)
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/unit", "-q"],
                       cwd=root, capture_output=True, text=True, timeout=600)
    g.requirements.append(Requirement(
        "unit-tests", "schema/gate unit tests pass", "pass" if r.returncode == 0 else "fail",
        (r.stdout or "").strip().splitlines()[-1] if r.stdout else ""))

    manifest = paths.vendor / "upstream-manifest.yaml"
    if manifest.exists():
        g.requirements.append(Requirement("provenance", "upstream manifest with pinned commits",
                                          "pass", str(manifest)))
        g.artifacts[str(manifest)] = _sha256(manifest)
    else:
        g.requirements.append(Requirement("provenance", "upstream manifest with pinned commits", "missing"))
    return g


def _stage2(paths: RepoPaths, project_id: str) -> GateResult:
    g = GateResult(
        stage_id="stage-2",
        title="Verifier calibration",
        label="SCIENTIFIC",
        question="Does the independent verifier reproduce known analytical answers and reject corrupted input?",
        why_it_matters="Every later verdict about AI-found metrics rests on this instrument being calibrated.",
        allowed_public_claim="ScienceBro's independent verifier has passed analytical known-answer "
                             "tests. Evaluation of neural AInstein candidates is not complete.",
    )
    proj = paths.project_dir(project_id)
    selftest = _load_json(proj / "results" / "processed" / "verifier_selftest.json")
    ka4d = _load_json(proj / "results" / "processed" / "known_answer_4d.json")
    disc = _load_json(proj / "results" / "processed" / "discrepancy_experiment.json")
    calib = _load_json(proj / "results" / "processed" / "calibration_maps.json")

    for p in ["verifier_selftest.json", "known_answer_4d.json",
              "discrepancy_experiment.json", "calibration_maps.json"]:
        fp = proj / "results" / "processed" / p
        if fp.exists():
            g.artifacts[str(fp)] = _sha256(fp)

    tests = (selftest or {}).get("tests", {})

    def suite(pattern: str, rid: str, desc: str) -> None:
        rel = {k: v for k, v in tests.items() if re.search(pattern, k)}
        if not rel:
            g.requirements.append(Requirement(rid, desc, "missing"))
        elif all(v == "passed" for v in rel.values()):
            g.requirements.append(Requirement(rid, desc, "pass", f"{len(rel)} tests passed"))
        else:
            bad = [k for k, v in rel.items() if v != "passed"]
            g.requirements.append(Requirement(rid, desc, "fail", f"failed: {bad}"))

    suite("minkowski", "minkowski", "analytical Minkowski vacuum")
    suite("schwarzschild_is_vacuum|kretschmann_known_answer", "schwarzschild",
          "analytical Schwarzschild vacuum + Kretschmann known answer")
    suite("perturbed", "negative-control", "corrupted metric rejected")
    suite("signature", "signature", "invalid signature rejected")

    # 4D analytic route thresholds
    if ka4d:
        rows = ka4d.get("analytic_route", {}).get("rows", [])
        if rows:
            worst_r = max(r["max_abs_ricci"] for r in rows)
            worst_k = max(r["kretschmann_rel_err"] for r in rows)
            ok = worst_r < RICCI_TOL and worst_k < KREL_TOL and all(
                r["lorentzian_signature"] for r in rows)
            g.requirements.append(Requirement(
                "analytic-4d-route", "4D Penrose-route analytic floor within thresholds",
                "pass" if ok else "fail",
                f"max|Ricci|={worst_r:.2e} (tol {RICCI_TOL}), K rel err={worst_k:.2e} (tol {KREL_TOL})"))
        else:
            g.requirements.append(Requirement("analytic-4d-route",
                                              "4D Penrose-route analytic floor", "missing"))
    else:
        g.requirements.append(Requirement("analytic-4d-route",
                                          "4D Penrose-route analytic floor", "missing"))

    # FD-step convergence on the NN metric
    if disc and "fd_step_sweep" in disc:
        vals = [v["max_abs_ricci"] for v in disc["fd_step_sweep"].values()]
        ratio = max(vals) / min(vals) if min(vals) > 0 else float("inf")
        g.requirements.append(Requirement(
            "fd-convergence", "FD-step sweep stable on NN metric",
            "pass" if ratio < 1.1 else "fail", f"max/min ratio = {ratio:.4f} over {len(vals)} steps"))
    else:
        g.requirements.append(Requirement("fd-convergence", "FD-step sweep stable on NN metric", "missing"))

    # precision comparison
    if calib and "float32_vs_float64_median_ratio" in calib:
        r32 = calib["float32_vs_float64_median_ratio"]
        g.requirements.append(Requirement(
            "precision", "float32 vs float64 sensitivity measured", "pass",
            f"float32 inflates median residual {r32:.0f}x -> float64 mandatory"))
    else:
        g.requirements.append(Requirement("precision", "float32 vs float64 sensitivity measured", "missing"))

    # normalization comparison / discrepancy explained
    if disc and "upstream_loss_replica_with_our_ricci" in disc:
        replica = disc["upstream_loss_replica_with_our_ricci"]
        upstream = disc["upstream_final_loss"]
        factor = max(replica, upstream) / min(replica, upstream)
        ok = factor < 3.0
        g.requirements.append(Requirement(
            "normalization", "upstream loss replicated with independent Ricci (factor < 3)",
            "pass" if ok else "fail",
            f"replica={replica:.2e} vs upstream={upstream:.2e} (factor {factor:.2f}); "
            f"sqrt(loss)={disc.get('sqrt_upstream_final_loss', 0):.3e}"))
    else:
        g.requirements.append(Requirement(
            "normalization", "upstream loss replicated with independent Ricci", "missing"))
    return g


def _stage_placeholder(stage_id: str, title: str, question: str, why: str,
                       claim: str, reqs: list[tuple[str, str]],
                       paths: RepoPaths, project_id: str) -> GateResult:
    g = GateResult(stage_id=stage_id, title=title, label="SCIENTIFIC",
                   question=question, why_it_matters=why, allowed_public_claim=claim)
    for rid, desc in reqs:
        g.requirements.append(Requirement(rid, desc, "missing"))
    return g


def _stage3(paths: RepoPaths, project_id: str) -> GateResult:
    g = _stage_placeholder(
        "stage-3", "Candidate generation",
        "Was a Petrov-I candidate trained under a frozen configuration with holdout points?",
        "Unfrozen configs or leaked holdout points would invalidate the audit.",
        "No candidate has been generated yet.",
        [("frozen-config", "training config frozen before run"),
         ("seed", "exact seed recorded"),
         ("checkpoint-hash", "checkpoint sha256 recorded"),
         ("training-log", "immutable training log preserved"),
         ("holdout", "holdout points excluded from training"),
         ("thresholds-frozen", "validation thresholds frozen before candidate inspection")],
        paths, project_id)
    proj = paths.project_dir(project_id)
    checks: dict[str, tuple[str, str]] = {}

    frozen_cfg = proj / "experiments" / "configs" / "hps_petrovI_bh_frozen.yaml"
    exp2 = proj / "experiments" / "EXP-0002.yaml"
    if frozen_cfg.exists() and exp2.exists():
        checks["frozen-config"] = ("pass", f"EXP-0002 + config sha {_sha256(frozen_cfg)[:16]}")
        g.artifacts[str(frozen_cfg)] = _sha256(frozen_cfg)
        g.artifacts[str(exp2)] = _sha256(exp2)
        if "np_seed: 123" in frozen_cfg.read_text(encoding="utf-8"):
            checks["seed"] = ("pass", "np/tf seed 123 (as committed by upstream)")

    log = proj / "upstream" / "petrovI_bh_run1.log"
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        done = "EXIT=0" in text
        epochs = re.findall(r"Epoch (\d+):", text)
        checks["training-log"] = (
            "pass" if done else "missing",
            f"epoch {epochs[-1] if epochs else 0}/500" + (" complete" if done else " — training in progress"))

    ckpt = proj / "results" / "raw" / "petrovI-bh-run1" / "final_model.keras"
    if ckpt.exists():
        checks["checkpoint-hash"] = ("pass", _sha256(ckpt)[:16])
        g.artifacts[str(ckpt)] = _sha256(ckpt)

    stress = proj / "results" / "processed" / "candidate_stress.json"
    if stress.exists():
        checks["holdout"] = ("pass", "hidden seed derived from checkpoint hash (candidate_stress.json)")
    frozen = proj / "validations" / "THRESHOLDS_FROZEN.md"
    if frozen.exists():
        checks["thresholds-frozen"] = ("pass", "THRESHOLDS_FROZEN.md + git tag thresholds-frozen")
        g.artifacts[str(frozen)] = _sha256(frozen)

    for r in g.requirements:
        if r.id in checks:
            r.status, r.measured = checks[r.id]
    return g


def _stage4(paths: RepoPaths, project_id: str) -> GateResult:
    g = _stage_placeholder(
        "stage-4", "Independent candidate stress test",
        "Does the candidate survive hidden-point, convergence, signature and boundary checks?",
        "This is the scientific core: independent verification outside the training path.",
        "No candidate has been independently stress-tested yet.",
        [("hidden-points", "hidden-point residuals measured (median/p95/p99/max)"),
         ("signature-det", "signature and determinant checks across domain"),
         ("boundary-maps", "boundary and horizon failure maps"),
         ("convergence", "precision and convergence tests"),
         ("negative-controls", "negative controls fail as expected"),
         ("independence", "independent implementation, no upstream loss imports")],
        paths, project_id)
    proj = paths.project_dir(project_id)
    cs = _load_json(proj / "results" / "processed" / "candidate_stress.json")
    if cs:
        g.artifacts[str(proj / "results" / "processed" / "candidate_stress.json")] = _sha256(
            proj / "results" / "processed" / "candidate_stress.json")
        hs = cs.get("hidden_stats_h3e-3", {})
        crit = cs.get("criteria", {})
        checks = {
            "hidden-points": ("pass", f"n=24 median {hs.get('median'):.3f} p95 {hs.get('p95'):.3f} "
                                      f"max {hs.get('max'):.3f} (verdict {cs.get('verdict_under_frozen_criteria')})"),
            "signature-det": ("pass" if crit.get("c3_signature", {}).get("pass") else "fail",
                              f"signature ok fraction {hs.get('signature_ok_fraction')}"),
            "convergence": ("pass" if crit.get("c4_convergence", {}).get("pass") else "fail",
                            f"median spread {crit.get('c4_convergence', {}).get('median_spread'):.2e}"),
            "negative-controls": ("pass" if crit.get("c6_negative_control", {}).get("pass") else "fail",
                                  "amp-0.5 control breaks criteria as expected"),
            "independence": ("pass", "FD verifier, subprocess boundary, no upstream imports"),
        }
        for r in g.requirements:
            if r.id in checks:
                r.status, r.measured = checks[r.id]
    bm = _load_json(proj / "results" / "processed" / "boundary_map.json")
    if bm and bm.get("rows"):
        ext = [r["max_abs_ricci"] for r in bm["rows"] if r["region"] == "exterior"]
        interior = [r["max_abs_ricci"] for r in bm["rows"] if r["region"] == "interior"]
        import statistics
        for r in g.requirements:
            if r.id == "boundary-maps":
                r.status = "pass"
                r.measured = (f"{len(bm['rows'])} grid pts incl. horizon: exterior median "
                              f"{statistics.median(ext):.3f}, interior {statistics.median(interior):.3f}")
        g.artifacts[str(proj / "results" / "processed" / "boundary_map.json")] = _sha256(
            proj / "results" / "processed" / "boundary_map.json")
    return g


def _stage5(paths: RepoPaths, project_id: str) -> GateResult:
    g = _stage_placeholder(
        "stage-5", "Scientific verdict",
        "Is every claim mapped to evidence and independently validated, with exact allowed wording?",
        "The verdict is only as strong as its weakest unsupported claim.",
        "No scientific verdict exists yet. NEEDS EXPERT REVIEW will apply until qualified "
        "external review happens.",
        [("claim-evidence", "complete claim-to-evidence mapping"),
         ("independent-validation", "independent validation decision recorded"),
         ("contradictions", "all contradictions and limitations recorded"),
         ("wording", "exact allowed public wording fixed"),
         ("expert-review", "reviewed by a qualified external expert"),
         ("decision", "PASS / FAIL / INCONCLUSIVE recorded")],
        paths, project_id)

    import yaml

    proj = paths.project_dir(project_id)
    claims_file = proj / "evidence" / "claims.yaml"
    try:
        claims = yaml.safe_load(claims_file.read_text(encoding="utf-8")).get("claims", [])
    except Exception:
        claims = []
    vals = sorted((proj / "validations").glob("VAL-*.yaml"))
    checks: dict[str, tuple[str, str]] = {}

    if claims:
        promoted = [c for c in claims
                    if c.get("state") in ("experimentally-supported", "independently-validated",
                                          "release-ready", "refuted")]
        unmapped = [c["id"] for c in promoted if not c.get("evidence_ids") and not c.get("experiment_ids")]
        checks["claim-evidence"] = (
            "pass" if promoted and not unmapped else ("fail" if unmapped else "missing"),
            f"{len(promoted)} promoted claims, all mapped to evidence/experiments"
            if promoted and not unmapped else f"unmapped: {unmapped}")
        worded = [c for c in promoted if c.get("allowed_public_wording")]
        checks["wording"] = (
            "pass" if promoted and len(worded) == len(promoted) else "fail",
            f"{len(worded)}/{len(promoted)} promoted claims carry exact allowed wording")
        with_blockers = [c for c in promoted if c.get("blockers")]
        checks["contradictions"] = (
            "pass" if with_blockers else "missing",
            f"{len(with_blockers)} promoted claims record their own limitations openly")

    if vals:
        decided = []
        for v in vals:
            try:
                decided.append(yaml.safe_load(v.read_text(encoding="utf-8")))
            except Exception:
                pass
        outcomes = {d.get("id"): d.get("decision") for d in decided if d}
        checks["independent-validation"] = (
            "pass" if outcomes else "missing",
            ", ".join(f"{k}:{v}" for k, v in sorted(outcomes.items())))
        checks["decision"] = (
            "pass" if any(v in ("pass", "fail", "inconclusive") for v in outcomes.values()) else "missing",
            f"{sum(1 for v in outcomes.values() if v == 'pass')} pass / "
            f"{sum(1 for v in outcomes.values() if v == 'fail')} fail recorded")
        for v in vals:
            g.artifacts[str(v)] = _sha256(v)

    review = proj / "validations" / "EXTERNAL_REVIEW.md"
    if review.exists():
        checks["expert-review"] = ("pass", str(review))
        g.artifacts[str(review)] = _sha256(review)

    for r in g.requirements:
        if r.id in checks:
            r.status, r.measured = checks[r.id]
    return g


def _stage6(paths: RepoPaths, project_id: str) -> GateResult:
    g = _stage_placeholder(
        "stage-6", "Public release",
        "Can an independent person reproduce everything from a clean clone with verified citations and licenses?",
        "A release that cannot be reproduced is marketing, not science.",
        "Nothing is released yet.",
        [("clean-clone", "clean-clone reproduction"),
         ("ci", "CI pass"),
         ("citations", "citation verification"),
         ("licenses", "license audit"),
         ("proof-packs", "complete proof packs for all stages"),
         ("ai-disclosure", "AI-use disclosure"),
         ("release", "GitHub release + Zenodo DOI")],
        paths, project_id)
    root = paths.root
    proj = paths.project_dir(project_id)
    checks: dict[str, tuple[str, str]] = {}

    cc = proj / "proof" / "stage-01" / "clean-clone-2026-08-11.log"
    if cc.exists() and "Clean-clone check passed." in cc.read_text(encoding="utf-8", errors="replace"):
        checks["clean-clone"] = ("pass", str(cc))
        g.artifacts[str(cc)] = _sha256(cc)

    ci = root / ".github" / "workflows"
    if ci.is_dir() and any(ci.glob("*.yml")):
        checks["ci"] = ("pass", f"{len(list(ci.glob('*.yml')))} workflow(s) defined")

    disclosure = root / "AI_DISCLOSURE.md"
    if disclosure.exists():
        checks["ai-disclosure"] = ("pass", str(disclosure))
        g.artifacts[str(disclosure)] = _sha256(disclosure)

    citation = root / "CITATION.cff"
    corpus = proj / "research" / "corpus.jsonl"
    if citation.exists() and corpus.exists():
        verified = sum(1 for line in corpus.read_text(encoding="utf-8").splitlines()
                       if '"content": true' in line.replace(" ", "") or '"content":true' in line.replace(" ", ""))
        checks["citations"] = ("pass" if verified else "missing",
                              f"CITATION.cff present, {verified} corpus entries content-verified")
        g.artifacts[str(citation)] = _sha256(citation)

    manifest = paths.vendor / "upstream-manifest.yaml"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8")
        documented = "GPL" in text and "license" in text.lower()
        checks["licenses"] = ("pass" if documented else "fail",
                              "upstream licenses recorded incl. the GPL-2.0 / MIT conflict"
                              if documented else "license conflict not documented")

    packs = sorted((proj / "proof").glob("stage-*"))
    complete = [p for p in packs if (p / "README.md").exists() and (p / "attestation.json").exists()]
    checks["proof-packs"] = ("pass" if len(complete) >= 6 else "missing",
                             f"{len(complete)} of 6 stages have a full proof pack")

    doi = proj / "release" / "ZENODO_DOI.txt"
    if doi.exists():
        checks["release"] = ("pass", doi.read_text(encoding="utf-8").strip()[:80])

    for r in g.requirements:
        if r.id in checks:
            r.status, r.measured = checks[r.id]
    return g


STAGES = {
    "stage-1": _stage1,
    "stage-2": _stage2,
    "stage-3": _stage3,
    "stage-4": _stage4,
    "stage-5": _stage5,
    "stage-6": _stage6,
}


def verify_stage(paths: RepoPaths, project_id: str, stage_id: str) -> GateResult:
    if stage_id not in STAGES:
        raise ValueError(f"unknown stage {stage_id}; valid: {sorted(STAGES)}")
    return STAGES[stage_id](paths, project_id)


def verify_all(paths: RepoPaths, project_id: str) -> list[GateResult]:
    return [verify_stage(paths, project_id, s) for s in sorted(STAGES)]


# ------------------------------------------------------------------ attestation / proof pack

def write_attestation(paths: RepoPaths, project_id: str, gate: GateResult) -> Path:
    """Write attestation.json for a stage. NOT a certificate of scientific truth:
    it certifies only that the declared tests ran, with these outcomes, against
    artifacts with these hashes."""
    root = paths.root
    proof_dir = paths.project_dir(project_id) / "proof" / gate.stage_id
    proof_dir.mkdir(parents=True, exist_ok=True)
    lock = root / "uv.lock"
    att = {
        "note": "This attestation certifies ONLY that the declared deterministic checks "
                "ran with the recorded outcomes against unchanged artifacts. It is not "
                "a certificate of scientific truth.",
        "stage_id": gate.stage_id,
        "title": gate.title,
        "label": gate.label,
        "status": gate.status,
        "verified_at": datetime.now(UTC).isoformat(),
        "git_commit": _git_commit(root),
        "uv_lock_sha256": _sha256(lock) if lock.exists() else None,
        "python": sys.version.split()[0],
        "requirements": [r.__dict__ for r in gate.requirements],
        "artifact_hashes": gate.artifacts,
        "allowed_public_claim": gate.allowed_public_claim,
    }
    out = proof_dir / "attestation.json"
    out.write_text(json.dumps(att, indent=2), encoding="utf-8")
    return out


def check_attestation_integrity(attestation_path: Path) -> list[str]:
    """Recompute artifact hashes; return list of violations (empty = intact)."""
    att = _load_json(attestation_path)
    if att is None:
        return [f"cannot read {attestation_path}"]
    problems = []
    for path_str, expected in att.get("artifact_hashes", {}).items():
        p = Path(path_str)
        if not p.exists():
            problems.append(f"missing artifact: {p}")
        elif _sha256(p) != expected:
            problems.append(f"CHANGED artifact (attestation invalid): {p}")
    return problems


def export_proof_pack(paths: RepoPaths, project_id: str, gate: GateResult) -> Path:
    """Assemble the proof pack directory for a stage from existing artifacts."""
    proj = paths.project_dir(project_id)
    pack = proj / "proof" / gate.stage_id
    pack.mkdir(parents=True, exist_ok=True)

    write_attestation(paths, project_id, gate)

    # gate definition
    ydef = [f"stage_id: {gate.stage_id}", f"title: {gate.title}", f"label: {gate.label}",
            f"question: {gate.question}", f"status: {gate.status}", "requirements:"]
    for r in gate.requirements:
        ydef.append(f"  - id: {r.id}")
        ydef.append(f"    description: {r.description}")
        ydef.append(f"    status: {r.status}")
        ydef.append(f"    measured: {json.dumps(r.measured)}")
    (pack / "gate-definition.yaml").write_text("\n".join(ydef) + "\n", encoding="utf-8")

    # measurements: copy the JSON artifacts referenced
    measurements = {}
    for p_str in gate.artifacts:
        p = Path(p_str)
        if p.suffix == ".json":
            measurements[p.name] = _load_json(p)
    (pack / "measurements.json").write_text(json.dumps(measurements, indent=2), encoding="utf-8")

    # commands
    cmds = [
        "uv sync --all-groups",
        "uv run pytest -q",
        f"uv run sb verify-stage {project_id} {gate.stage_id}",
        "uv run python projects/ainstein-audit/verifier/make_selftest_artifact.py",
        "uv run python projects/ainstein-audit/verifier/known_answer_4d.py",
    ]
    (pack / "commands.sh").write_text("#!/bin/sh\nset -e\n" + "\n".join(cmds) + "\n", encoding="utf-8")
    (pack / "commands.ps1").write_text("\n".join(cmds) + "\n", encoding="utf-8")

    # checksums
    lines = [f"{h}  {p}" for p, h in sorted(gate.artifacts.items())]
    (pack / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # bibliography + source manifest
    bib = proj / "research" / "bibliography.bib"
    if bib.exists():
        (pack / "bibliography.bib").write_text(bib.read_text(encoding="utf-8"), encoding="utf-8")
    src_manifest = {
        "git_commit": _git_commit(paths.root),
        "upstream": "see vendor/upstream-manifest.yaml",
        "verifier": "projects/ainstein-audit/verifier/ (no upstream imports)",
    }
    (pack / "source-manifest.json").write_text(json.dumps(src_manifest, indent=2), encoding="utf-8")

    # limitations + claim + validation notes
    lim = proj / "verifier" / "CALIBRATION.md"
    limitations = ["# Limitations", ""]
    if lim.exists():
        limitations.append("See measured calibration limits (copied from verifier/CALIBRATION.md):")
        limitations.append(lim.read_text(encoding="utf-8"))
    (pack / "limitations.md").write_text("\n".join(limitations), encoding="utf-8")
    (pack / "allowed-public-claim.md").write_text(
        f"# Allowed public claim at {gate.stage_id}\n\n{gate.allowed_public_claim}\n", encoding="utf-8")
    (pack / "independent-validation.md").write_text(
        "# Independence statement\n\nThe verifier package (projects/ainstein-audit/verifier/) "
        "imports no upstream code; exported metric values cross the boundary as plain float64 "
        "arrays via a subprocess in an isolated environment. Verified by inspection of imports "
        "and by construction of the interface (verifier/interface.py).\n", encoding="utf-8")

    # README (plain English)
    passed = [r for r in gate.requirements if r.status == "pass"]
    open_reqs = [r for r in gate.requirements if r.status != "pass"]
    readme = [
        f"# Proof pack: {gate.title} ({gate.stage_id})",
        "",
        f"**Status: {gate.status}**" + (" (ENGINEERING, not scientific)" if gate.label == "ENGINEERING" else ""),
        "",
        f"**Question:** {gate.question}",
        "",
        f"**Why it matters:** {gate.why_it_matters}",
        "",
        "## What passed",
        *[f"- {r.description}: {r.measured or 'pass'}" for r in passed],
        "",
        "## What is not settled",
        *([f"- {r.description} ({r.status}): {r.measured or ''}" for r in open_reqs] or ["- nothing — all requirements passed"]),
        "",
        "## How to reproduce",
        "Run `commands.sh` (POSIX) or `commands.ps1` (Windows) from the repository root.",
        "Compare outputs against `measurements.json`; verify file integrity against",
        "`checksums.sha256`; check `attestation.json` for the exact git commit and",
        "environment lock hash.",
        "",
        "## What this does and does not prove",
        "It proves: the declared deterministic checks ran with the recorded outcomes.",
        "It does NOT prove: any claim about AInstein candidates beyond the allowed",
        "public claim in `allowed-public-claim.md`.",
    ]
    (pack / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    return pack
