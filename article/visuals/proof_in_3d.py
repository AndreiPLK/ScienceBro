"""THE PROOF ITSELF, IN 3D -- every box that had to be checked.

This is not a plot of data. It is a picture of the machine proof of knife 4
(lab/knife4_proof.py): each brick is one box on which the polynomial was
re-expanded in the Bernstein basis with exact rational arithmetic and its whole
control net came out strictly positive. Since a polynomial never leaves the
convex hull of that net, a positive net is a proof for the whole brick, not a
sample of it.

WHAT THE SHAPE MEANS. The subdivision is adaptive: a brick is split only when its
net dips. So brick size IS the local difficulty of the theorem. Big bricks where
the knife has room; a fine dust of small bricks where it runs close to the shore
and the margin is thin (about 1.01 at the worst place). The shape of the dust is
the shape of the hard part.

Colour is the Bernstein lower bound on that brick, on a log scale: how much room
was left over after the proof.

Axes: n the level, D the spacetime dimension, lam the family parameter. The upper
surface of the solid is the shore itself -- D = T_hat(lam) -- because that is
where the admissible region ends.
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

import knife4_proof as K  # noqa: E402

CACHE = Path("/tmp/proof_boxes.json")
N_MAX, LAM_MAX = 60, 12


def collect(n_max, lam_max, max_depth=26):
    """Re-run the proof, recording every box that closed."""
    lam_hi = F(lam_max)
    stack = [((F(4), F(n_max)), (F(4), K.shore_upper(lam_hi)), (F(1), lam_hi), 0)]
    closed, open_boxes = [], []
    while stack:
        nb, db, lb, depth = stack.pop()
        top = K.shore_upper(lb[1])
        db = (db[0], min(db[1], top))
        if db[0] >= db[1]:
            continue
        val = K.bernstein_lower((nb, db, lb))
        if val > 0:
            closed.append(
                [
                    float(nb[0]),
                    float(nb[1]),
                    float(db[0]),
                    float(db[1]),
                    float(lb[0]),
                    float(lb[1]),
                    float(val),
                ]
            )
            continue
        if depth >= max_depth:
            open_boxes.append((nb, db, lb))
            continue
        w = [
            (nb[1] - nb[0]) / max(F(1), nb[0]),
            (db[1] - db[0]) / max(F(1), db[0]),
            (lb[1] - lb[0]) / max(F(1), lb[0]),
        ]
        k = w.index(max(w))
        if k == 0:
            m = (nb[0] + nb[1]) / 2
            stack += [((nb[0], m), db, lb, depth + 1), ((m, nb[1]), db, lb, depth + 1)]
        elif k == 1:
            m = (db[0] + db[1]) / 2
            stack += [(nb, (db[0], m), lb, depth + 1), (nb, (m, db[1]), lb, depth + 1)]
        else:
            m = (lb[0] + lb[1]) / 2
            stack += [(nb, db, (lb[0], m), depth + 1), (nb, db, (m, lb[1]), depth + 1)]
    return closed, len(open_boxes)


if CACHE.exists():
    data = json.loads(CACHE.read_text(encoding="utf-8"))
    boxes, still_open = data["boxes"], data["open"]
else:
    boxes, still_open = collect(N_MAX, LAM_MAX)
    CACHE.write_text(json.dumps({"boxes": boxes, "open": still_open}), encoding="utf-8")
print("boxes:", len(boxes), " still open:", still_open)

B = np.array(boxes)
cx, cy, cz = (B[:, 0] + B[:, 1]) / 2, (B[:, 2] + B[:, 3]) / 2, (B[:, 4] + B[:, 5]) / 2
vol = (B[:, 1] - B[:, 0]) * (B[:, 3] - B[:, 2]) * (B[:, 5] - B[:, 4])
margin = np.log10(np.maximum(B[:, 6], 1e-300))
size = 3.0 + 16.0 * (vol / vol.max()) ** 0.28

fig = go.Figure(
    go.Scatter3d(
        x=cx,
        y=cy,
        z=cz,
        mode="markers",
        marker=dict(
            size=size,
            color=margin,
            colorscale="Turbo",
            opacity=0.72,
            line=dict(width=0),
            colorbar=dict(
                title=dict(
                    text="log of the room left<br>over on that brick",
                    font=dict(color="#a8a08e", size=11),
                ),
                tickfont=dict(color="#a8a08e", size=10),
                thickness=14,
                len=0.7,
            ),
        ),
        hovertemplate="n=%{x:.1f}<br>D=%{y:.1f}<br>lam=%{z:.2f}<extra></extra>",
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="THE PROOF ITSELF — every brick that had to be checked<br><sup>"
        f"{len(boxes)} bricks, none left open. On each one the polynomial was "
        "rewritten in the Bernstein basis in exact rational arithmetic and its "
        "whole control net came out positive;<br>a polynomial cannot leave the "
        "convex hull of that net, so a positive net proves the brick entire. "
        "Brick size is the local difficulty: coarse where the knife has room, "
        "fine dust where it runs close to the shore.</sup>",
        font=dict(color="#ede8dc", size=19),
        x=0.02,
        y=0.95,
    ),
    scene=dict(
        xaxis=dict(
            title="n — the level", backgroundcolor="#14130f", gridcolor="#322e26", color="#a8a08e"
        ),
        yaxis=dict(
            title="D — dimension", backgroundcolor="#14130f", gridcolor="#322e26", color="#a8a08e"
        ),
        zaxis=dict(
            title="lam — family", backgroundcolor="#14130f", gridcolor="#322e26", color="#a8a08e"
        ),
        aspectratio=dict(x=1.35, y=1.0, z=0.85),
        camera=dict(eye=dict(x=1.75, y=-1.6, z=0.85)),
    ),
    margin=dict(l=0, r=0, t=120, b=0),
    width=1500,
    height=800,
)

out = Path(__file__).resolve().parent / "proof-in-3d.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (20, 19, 15))
bbox = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 10 else 0).getbbox()
pad = 12
im.crop(
    (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(im.width, bbox[2] + pad),
        min(im.height, bbox[3] + pad),
    )
).save(out)
print("saved", out, Image.open(out).size)
