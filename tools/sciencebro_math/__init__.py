"""sciencebro-math: a stable, exact tool layer for the lab's recurring questions.

Import surface is deliberately small; see `cli.py` for the command-line form and
`server.py` for the MCP form. Every entry point returns a `core.Result`, whose
`evidence_kind` is the only thing that may be quoted as the strength of the evidence.
"""

from .battery import anomaly_scan, scan_family_centered
from .core import Result
from .families import centered_squares, deformed_grid, half_spectrum, normalized_means
from .positivity import (
    bernstein_certificate,
    sturm_roots,
    sturm_sign,
    verify_polynomial_positive,
)
from .sequences import (
    hankel_minors,
    hausdorff_conditions,
    log_difference_hierarchy,
    ratio_log_concavity,
    real_rootedness,
    stieltjes_conditions,
    toeplitz_minors,
    turan,
)

__all__ = [
    "Result",
    "anomaly_scan",
    "scan_family_centered",
    "centered_squares",
    "deformed_grid",
    "half_spectrum",
    "normalized_means",
    "log_difference_hierarchy",
    "ratio_log_concavity",
    "turan",
    "hankel_minors",
    "toeplitz_minors",
    "hausdorff_conditions",
    "stieltjes_conditions",
    "real_rootedness",
    "sturm_sign",
    "sturm_roots",
    "bernstein_certificate",
    "verify_polynomial_positive",
]
