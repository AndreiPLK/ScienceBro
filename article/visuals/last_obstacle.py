"""THE LAST OBSTACLE — the single thing between us and the grand theorem.

REAL DATA: Phi(v) (the one-variable function our reduction produced) across
the support of the measure nu, for a family of knives. Positive almost
everywhere (cyan plateau); it dips just below zero at the far edge (pink
notch) — and the measure puts almost no weight there. That gap is the whole
remaining problem, in one picture.
"""

import sys
from pathlib import Path
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from knife_proof2 import e_doubled_int
from keystone_hunt import T_hat


def M1f(j, n, t):
    v = 1.0
    for r in range(t):
        v *= (j - 1 - r) / (n - 1 - r)
    return v


LAM = Fraction(1)
Th = T_hat(LAM)
D = 4 + (Th - 4)
js, Z = [], []
frs = np.linspace(0, 1, 160)
for j in range(5, 19):
    n = j + 6
    e = e_doubled_int(n)
    c = 4 * n - 4 * j - 1
    s = float(LAM) + n - 1
    R = (float(D) + c) / 2 + j - 1
    vmax = (R - 1) / ((n - 1.5) * s * s)
    row = []
    for fr in frs:
        v = vmax * fr
        val = sum(((-1) ** t) * float(e[t]) * M1f(j, n, t) * v ** t
                  for t in range(min(j, len(e))))
        row.append(np.sign(val) * abs(val) ** 0.25)   # сжать масштаб, знак сохранить
    Z.append(row)
    js.append(j)

fig = go.Figure()
fig.add_trace(go.Surface(
    x=frs, y=js, z=Z, showscale=False, cmid=0,
    colorscale=[[0.0, "#ff2a6d"], [0.42, "#7a3fd0"], [0.5, "#2a1040"],
                [0.62, "#0aa3c2"], [1.0, "#3fe7f5"]],
    lighting=dict(ambient=0.55, diffuse=0.75, specular=0.25)))
fig.add_trace(go.Surface(
    x=frs, y=[js[0], js[-1]], z=[[0] * len(frs)] * 2,
    surfacecolor=[[0] * len(frs)] * 2, opacity=0.35, showscale=False,
    colorscale=[[0, "#f9f871"], [1, "#f9f871"]]))

ann = [
    dict(x=0.30, y=js[-1] - 1, z=1.35,
         text="EVERYTHING HERE IS POSITIVE — the theorem holds easily",
         font=dict(color="#3fe7f5", size=15), showarrow=False),
    dict(x=0.90, y=js[len(js) // 2], z=-0.62,
         text="THE NOTCH: dips below zero at the very edge<br>"
              "(the measure puts almost no weight here)",
         font=dict(color="#ff5f95", size=14), showarrow=False),
    dict(x=0.06, y=js[0] + 1, z=0.22, text="ZERO (yellow sheet)",
         font=dict(color="#f9f871", size=13), showarrow=False),
]
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0714",
    title=dict(text="THE LAST OBSTACLE — one picture, one problem left<br>"
                    "<sup>the function our reduction produced, across every "
                    "knife: positive on the whole plateau, and only at the "
                    "far edge does it dip under the yellow zero-sheet. "
                    "Proving that the dip cannot win IS the grand theorem."
                    "</sup>",
               font=dict(color="#e8e6f0", size=20), x=0.03),
    scene=dict(
        xaxis=dict(title="across the support of the measure  ->  edge",
                   color="#8f8ba0", gridcolor="#241a38"),
        yaxis=dict(title="knife j", color="#8f8ba0", gridcolor="#241a38",
                   dtick=2),
        zaxis=dict(title="", showticklabels=False, color="#8f8ba0",
                   gridcolor="#241a38"),
        annotations=ann,
        camera=dict(eye=dict(x=1.55, y=-1.55, z=0.62),
                    center=dict(x=0, y=0, z=-0.08))),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_lo_raw.png"), scale=2)
Image.open(out / "_lo_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "last-obstacle.png")
(out / "_lo_raw.png").unlink()
print("saved last-obstacle.png")
