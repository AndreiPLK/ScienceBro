"""Run the verifier known-answer suite and persist per-test outcomes as an artifact.

The dashboard reads this artifact (never runs tests itself). Refresh with:
  uv run python projects/ainstein-audit/verifier/make_selftest_artifact.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "results" / "processed" / "verifier_selftest.json"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sb-selftest-") as td:
        xml_path = Path(td) / "junit.xml"
        r = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(PROJ / "verifier"),
                "-q",
                f"--junitxml={xml_path}",
            ],
            capture_output=True,
            text=True,
            cwd=PROJ.parents[1],
        )
        tests: dict[str, str] = {}
        if xml_path.exists():
            for case in ET.parse(xml_path).getroot().iter("testcase"):
                name = case.get("name", "?")
                if case.find("failure") is not None or case.find("error") is not None:
                    outcome = "failed"
                elif case.find("skipped") is not None:
                    outcome = "skipped"
                else:
                    outcome = "passed"
                tests[name] = outcome
    artifact = {
        "generated_at": datetime.now(UTC).isoformat(),
        "pytest_exit_code": r.returncode,
        "n_passed": sum(1 for v in tests.values() if v == "passed"),
        "n_failed": sum(1 for v in tests.values() if v == "failed"),
        "n_skipped": sum(1 for v in tests.values() if v == "skipped"),
        "tests": tests,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in artifact.items() if k != "tests"}, indent=2))
    return 0 if r.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
