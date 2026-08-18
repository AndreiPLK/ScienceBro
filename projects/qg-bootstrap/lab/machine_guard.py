"""Never take the founder's machine down. Checked from inside the loop, not before it.

Paid for on 18 August 2026: a background threshold run walked up to degree ~2300
polynomials with exact rational coefficients and took free memory from 31 GB to
0.3 GB. The pre-flight check had passed -- because the job was small when it
STARTED. A one-shot check before launching is worthless for a job whose appetite
grows with the loop index.

So the guard lives inside the loop: every heavy step calls `check()` first, and
the job stops itself cleanly, having written its partial results, rather than
being killed from outside.
"""

from __future__ import annotations

import subprocess


class MachineBusy(RuntimeError):
    """Raised so a job can stop itself and save what it has."""


def free_gb() -> float:
    """Free physical memory in GB. Returns a large number if it cannot tell."""
    try:
        out = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-c",
                "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout.strip()
        return float(out.replace(",", "."))
    except (OSError, ValueError, subprocess.SubprocessError):
        return 999.0


def check(floor_gb: float = 6.0, what: str = "") -> None:
    """Stop the job if free memory has fallen below the floor.

    floor_gb = 6 leaves headroom for the founder to open a game or a browser
    while a night job runs. Raise it for jobs that allocate in big steps.
    """
    f = free_gb()
    if f < floor_gb:
        raise MachineBusy(
            f"free memory {f:.1f} GB is below the {floor_gb:.1f} GB floor"
            + (f" before {what}" if what else "")
            + " -- stopping and keeping partial results"
        )


def floor_for(size: int) -> float:
    """Headroom a job of this size should insist on, in GB.

    A FIXED floor is wrong in both directions, and I got it wrong on the first
    try: 4 GB blocked a 200-degree cross-check that needs megabytes, while the
    same 4 GB would be far too little for degree 10000. The requirement has to
    scale with the work, so small checks keep running while the founder's video
    encode holds memory, and only the genuinely large jobs stand aside.
    """
    return max(1.2, min(6.0, 1.2 + size / 2500.0))


def note(what: str = "") -> str:
    return f"[machine] free {free_gb():.1f} GB{(' before ' + what) if what else ''}"
