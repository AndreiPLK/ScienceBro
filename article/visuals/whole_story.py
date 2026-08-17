"""THE WHOLE STORY IN ONE PICTURE — cliff-3d style, real exact data.

For the founder: everything this programme has established, on one terrain.

The trick that makes it readable: the vertical axis is the dimension
MEASURED AGAINST THE SHORE, D / T_hat(lam). Then the shore is always exactly
1.0, whatever the family, and the picture becomes a plateau with a cliff.

  * PLATEAU (flat, height 0): D below the shore -- allowed, consistent
    gravity theories live here.
  * CLIFF (the wall): D above the shore -- forbidden.
  * YELLOW EDGE at 1.0: the shore itself, T_hat(lam) = min over
    trajectories, which grows as (12 + 4 sqrt 3) lam.
  * WHITE DIAMOND: the string, at lam = 1, D = 23 -- standing exactly on the
    edge (paper 2).
  * RED MARKERS: where the knives actually start cutting, D*(j, lam)/T_hat.
    They sit ABOVE 1.0 always -- the blades never reach the plateau.
  * CYAN BAND just under the edge: the width-2 strip. Today's descent lemma
    proved everything below this band follows for free, so the band is all
    that is still open.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from keystone_hunt import T_hat, T_k  # noqa: E402
from keystone_lowspin import threshold_D  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

LAMS = [Fraction(x) for x in (1, 2, 3, 5, 7, 10, 14, 18, 22, 26, 30)]
lam_f = [float(x) for x in LAMS]
shore = {x: T_hat(x) for x in LAMS}

# vertical: ratio r = D / shore ; height = how far into forbidden land
rs = np.linspace(0.25, 1.30, 160)
Z = [[max(0.0, (r - 1.0)) * 320 for _ in lam_f] for r in rs]

fig = go.Figure()
fig.add_trace(
    go.Surface(
        x=lam_f,
        y=rs,
        z=Z,
        showscale=False,
        colorscale=[[0.0, "#123a52"], [0.02, "#1b6f9e"], [0.35, "#7a1f4f"], [1.0, "#ff2a6d"]],
        lighting=dict(ambient=0.66, diffuse=0.66, specular=0.15, roughness=0.75),
        contours=dict(z=dict(show=True, start=0, end=100, size=12, color="#0b0714", width=1)),
    )
)

# the shore: ratio exactly 1
fig.add_trace(
    go.Scatter3d(
        x=lam_f,
        y=[1.0] * len(lam_f),
        z=[1.2] * len(lam_f),
        mode="lines",
        line=dict(color="#f9f871", width=11),
        showlegend=False,
    )
)

# the width-2 strip, in ratio units it is 2/shore -- thin, and thinner with lam
fig.add_trace(
    go.Scatter3d(
        x=lam_f,
        y=[1.0 - 2.0 / float(shore[x]) for x in LAMS],
        z=[0.8] * len(lam_f),
        mode="lines",
        line=dict(color="#4df0ff", width=8),
        showlegend=False,
    )
)

# the string: lam = 1, D = 23, exactly on the shore
fig.add_trace(
    go.Scatter3d(
        x=[1.0],
        y=[1.0],
        z=[3.0],
        mode="markers",
        marker=dict(size=16, color="#ffffff", symbol="diamond"),
        showlegend=False,
    )
)

# the knives
kx, ky, kz = [], [], []
for lam in (
    Fraction(3),
    Fraction(7),
    Fraction(10),
    Fraction(14),
    Fraction(18),
    Fraction(22),
    Fraction(26),
    Fraction(30),
):
    sh = T_hat(lam)
    k = min(range(3, int(3 * float(lam)) + 61), key=lambda kk: T_k(kk, lam))
    for j in (4, 6, 8, 10):
        best = None
        for n in range(max(4, k - 4), k + 4):
            t = threshold_D(j, n, lam)
            if t is None:
                continue
            if best is None or t < best:
                best = t
        if best is not None:
            r = float(best / sh)
            if r > 1.28:  # outside the drawn range
                continue
            kx.append(float(lam))
            ky.append(r)
            kz.append((r - 1.0) * 320 + 2.0)
fig.add_trace(
    go.Scatter3d(
        x=kx,
        y=ky,
        z=kz,
        mode="markers",
        marker=dict(size=6, color="#ff2a6d", line=dict(color="#ffd0dd", width=1)),
        showlegend=False,
    )
)

ann = [
    dict(
        x=22,
        y=0.45,
        z=6,
        text="ALLOWED<br>gravity theories live here",
        font=dict(color="#8ff0ff", size=16),
        showarrow=False,
    ),
    dict(
        x=24, y=1.24, z=76, text="FORBIDDEN", font=dict(color="#ff8fb0", size=17), showarrow=False
    ),
    dict(
        x=8,
        y=1.02,
        z=30,
        text="THE SHORE — consistency ends here",
        font=dict(color="#ffe94a", size=15),
        showarrow=False,
    ),
    dict(
        x=1,
        y=1.0,
        z=54,
        text="THE STRING — exactly on the edge, 23 dimensions",
        font=dict(color="#ffffff", size=14),
        showarrow=False,
    ),
    dict(
        x=29,
        y=1.10,
        z=42,
        text="the knives cut only here, above the edge",
        font=dict(color="#ff8fb0", size=14),
        showarrow=False,
    ),
    dict(
        x=14,
        y=0.80,
        z=-9,
        text="cyan band = all that is left to prove",
        font=dict(color="#4df0ff", size=14),
        showarrow=False,
    ),
]

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b0714",
    title=dict(
        text="WHAT WE FOUND<br><sup>The floor is where consistent gravity "
        "lives; the wall is forbidden. The yellow line is the edge.<br>"
        "The string stands exactly on it at 23 dimensions. The red "
        "blades cut only above it, never on the floor.<br>Today we "
        "proved everything below the cyan band comes for free — so only "
        "that band is left.</sup>",
        font=dict(color="#e8e6f0", size=21),
        x=0.025,
        y=0.955,
    ),
    scene=dict(
        xaxis=dict(
            title="lam — which family of theories",
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        yaxis=dict(
            title="dimension, measured against the shore",
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        zaxis=dict(
            title="how far into forbidden land",
            showticklabels=False,
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        aspectratio=dict(x=1.6, y=1.2, z=0.85),
        annotations=ann,
        camera=dict(eye=dict(x=1.5, y=-1.45, z=0.66), center=dict(x=0, y=0, z=-0.08)),
    ),
    margin=dict(l=0, r=0, t=120, b=0),
    width=1460,
    height=700,
)

out = Path(__file__).resolve().parent / "whole-story.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (11, 7, 20))
bbox = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 10 else 0).getbbox()
pad = 14
im.crop(
    (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(im.width, bbox[2] + pad),
        min(im.height, bbox[3] + pad),
    )
).save(out)
print("saved", out, Image.open(out).size)
