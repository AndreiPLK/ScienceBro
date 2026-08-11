"""Standalone doctor entry (equivalent to `uv run sb doctor`)."""

from sciencebro.cli import doctor

if __name__ == "__main__":
    doctor(as_json=False)
