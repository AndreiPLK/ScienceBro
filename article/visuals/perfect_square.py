"""THE SQUARE — night's structural discovery, visualised (cliff-3d style).

REAL DATA: F_n(x) = sum_t (-1)^t E_2t(n) x^t, computed exactly, plotted for
a range of levels n. The night's theorem: F_n(x) = G_n(x)^2 — a PERFECT
SQUARE, hence never negative. The surface therefore never dips below zero:
the sign problem of the master formula lives entirely in the weights.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from knife_proof2 import e_doubled_int  # noqa: E402
from PIL import Image  # noqa: E402

ns = list(range(5, 19))
xs = np.linspace(0, 0.06, 220)
Z, floor_touch = [], []
for n in ns:
    e = e_doubled_int(n)
    row = []
    for x in xs:
        v = sum(((-1) ** t) * float(e[t]) * x ** t for t in range(len(e)))
        row.append(np.sign(v) * abs(v) ** 0.12)          # сжать динамику
    Z.append(row)
    a = [n - 2 * k for k in range(1, n) if n - 2 * k > 0]
    floor_touch += [(1.0 / (ai ** 2), n) for ai in a if 1.0 / (ai ** 2) <= xs[-1]]

fig = go.Figure()
fig.add_trace(go.Surface(
    x=xs, y=ns, z=Z,
    colorscale=[[0, "#33091d"], [0.25, "#ff2a6d"], [0.5, "#7a3fd0"],
                [0.78, "#0aa3c2"], [1, "#3fe7f5"]],
    showscale=False,
    lighting=dict(ambient=0.5, diffuse=0.75, specular=0.3, roughness=0.6)))
fig.add_trace(go.Scatter3d(
    x=[p[0] for p in floor_touch], y=[p[1] for p in floor_touch],
    z=[0.02] * len(floor_touch), mode="markers",
    marker=dict(size=4, color="#f9f871"), showlegend=False))

ann = [dict(x=0.012, y=17.5, z=3.4, text="THE PERFECT SQUARE",
            font=dict(color="#9ff5ff", size=25), showarrow=False),
       dict(x=0.030, y=7.5, z=1.15,
            text="yellow dots = the double roots (1/a^2):<br>"
                 "the surface KISSES zero and turns back — never crosses",
            font=dict(color="#ffe94a", size=14), showarrow=False),
       dict(x=0.048, y=13.5, z=0.06, text="ZERO FLOOR",
            font=dict(color="#ff5f95", size=15), showarrow=False)]

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0714",
    title=dict(text="THE PERFECT SQUARE — why the sign problem is NOT in the "
                    "spectrum<br><sup>height = the alternating spectral sum "
                    "of level n (real exact data, compressed scale). Tonight "
                    "we proved it equals G(x)^2 — a perfect square, so it can "
                    "touch zero but never go below</sup>",
               font=dict(color="#e8e6f0", size=19), x=0.03),
    scene=dict(
        xaxis=dict(title="x", color="#8f8ba0", gridcolor="#241a38"),
        yaxis=dict(title="level n", color="#8f8ba0", gridcolor="#241a38"),
        zaxis=dict(title="", color="#8f8ba0", gridcolor="#241a38",
                   showticklabels=False),
        camera=dict(eye=dict(x=1.7, y=-1.5, z=0.7),
                    center=dict(x=0, y=0, z=-0.1))),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_sq_raw.png"), scale=2)
Image.open(out / "_sq_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "perfect-square.png")
(out / "_sq_raw.png").unlink()
print("saved perfect-square.png")
