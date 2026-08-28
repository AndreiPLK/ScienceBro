"""Machine verification of the depth-kernel minor identity, constant included.

The identity (proof in results/KERNEL_TP_THEOREM.md):

    det[ B_{r0+a, t0+b} ]_{a,b=0}^{q-1}
      =  prod_a (H-r0-a)_{t0} * prod_a (r0+a)_{t0}
       * prod_{a<b} (b-a) * prod_{a<b} (H - 2r0 - a - b),

with B_{r,t} = C(r,t)(H-r)_t t!. This script compares the symbolically
expanded determinant against the closed form as POLYNOMIALS in H (exact
fmpq_poly equality, not evaluation), over q <= 5, r0 <= 12, t0 <= 3.

Run: python lab/kernel_minor_identity.py -> results/kernel_minor_identity.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kernel_minor_law import solid_minor  # noqa: E402
from provenance import stamp  # noqa: E402

RES = Path(__file__).resolve().parents[1] / "results"


def predicted(r0: int, t0: int, q: int) -> fmpq_poly:
    x = fmpq_poly([0, 1])
    p = fmpq_poly([1])
    const = fmpq(1)
    for a in range(q):
        for i in range(t0):
            p = p * (x - (r0 + a) - i)  # (H-r0-a)_{t0}
        f = fmpq(1)
        for i in range(t0):
            f *= (r0 + a) - i  # (r0+a)_{t0} falling
        const *= f
    for a in range(q):
        for b in range(a + 1, q):
            const *= b - a
            p = p * (x - 2 * r0 - a - b)
    return p * const


def main() -> int:
    t0_ = time.time()
    tot, bad = 0, []
    for q in (2, 3, 4, 5):
        for r0 in (4, 5, 6, 8, 10, 12):
            for toff in (0, 1, 2, 3):
                if toff + q - 1 > r0:
                    continue
                tot += 1
                if solid_minor(r0, toff, q) != predicted(r0, toff, q):
                    bad.append((q, r0, toff))
    print(f"identity incl. constant: {tot - len(bad)}/{tot} exact polynomial matches", flush=True)
    out = {
        "claim": (
            "PROVED IDENTITY (proof: results/KERNEL_TP_THEOREM.md): the solid q x q "
            "minor of the depth kernel B_{r,t} = C(r,t)(H-r)_t t! equals "
            "prod_a (H-r0-a)_{t0} * prod_a (r0+a)_{t0} * prod_{a<b}(b-a) * "
            "prod_{a<b}(H-2r0-a-b). Corollary: the depth kernel is strictly totally "
            "positive on the physical domain (every root <= 2 r_max - 1 < H there)."
        ),
        "tested": tot,
        "mismatches": bad,
        "verified": not bad,
        "command": "python lab/kernel_minor_identity.py",
        "seconds": round(time.time() - t0_, 1),
        **stamp(),
    }
    path = RES / "kernel_minor_identity.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}", flush=True)
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
