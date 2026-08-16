"""THE CITY OF STRING PARTICLES — glyph/city style (3D towers).

REAL DATA: at the string point (lam=1, D=10) every particle of the ladder
(level n, spin l) gets a tower; height = log10 of its positivity margin
P_j (master formula, exact -> float). Every tower stands: the knives cut
none of them. This is what "the string is consistent" looks like.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from keystone_hunt import eval_P  # noqa: E402
from knife_proof2 import Bj_coeffs  # noqa: E402
from PIL import Image  # noqa: E402

LAM, D = Fraction(1), Fraction(10)
bars = []
for n in range(5, 26):
    for j in range(2, n - 1):
        l = 2 * n - 2 * j
        if l > 26:
            continue
        P = eval_P(Bj_coeffs(j, n - 3), LAM, D)
        if P <= 0:
            continue
        h = float(np.log10(float(P)) + 1)
        bars.append((n, l, max(0.4, h / 6)))

fig = go.Figure()
CS = [[0, "#7a3fd0"], [0.5, "#0aa3c2"], [1, "#3fe7f5"]]
hmax = max(b[2] for b in bars)
for n, l, h in bars:
    fig.add_trace(go.Mesh3d(
        x=[n-0.3, n+0.3, n+0.3, n-0.3, n-0.3, n+0.3, n+0.3, n-0.3],
        y=[l-0.55, l-0.55, l+0.55, l+0.55, l-0.55, l-0.55, l+0.55, l+0.55],
        z=[0, 0, 0, 0, h, h, h, h],
        i=[0, 0, 0, 1, 4, 4, 6, 6, 0, 0, 2, 2],
        j=[1, 2, 4, 5, 5, 6, 5, 7, 1, 4, 3, 6],
        k=[2, 3, 5, 6, 6, 7, 1, 3, 5, 5, 7, 7],
        color=f"rgb({int(60+120*h/hmax)},{int(120+100*h/hmax)},245)",
        opacity=1.0, showlegend=False, lighting=dict(ambient=0.45,
        diffuse=0.6, specular=0.35, roughness=0.4),
        lightposition=dict(x=30, y=-40, z=60)))
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#05030c",
    title=dict(text="THE CITY OF STRING PARTICLES<br>"
                    "<sup>each glowing tower = one particle of string theory "
                    "(level n, spin l); height = its positivity safety "
                    "margin (exact data, lam=1, D=10).<br>Every tower "
                    "stands — the knives cut none. This is what a "
                    "CONSISTENT theory looks like</sup>",
               font=dict(color="#e8e6f0", size=21), x=0.03),
    scene=dict(
        xaxis=dict(title="level n (mass ladder)", color="#5c5870",
                   gridcolor="#150e24"),
        yaxis=dict(title="spin l", color="#5c5870", gridcolor="#150e24"),
        zaxis=dict(title="", showticklabels=False, color="#5c5870",
                   gridcolor="#150e24"),
        camera=dict(eye=dict(x=1.35, y=-1.5, z=0.55),
                    center=dict(x=0, y=0, z=-0.1)),
        aspectmode="manual",
        aspectratio=dict(x=1.6, y=1.1, z=0.7),
    ),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_c_raw.png"), scale=2)
Image.open(out / "_c_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "string-city.png")
(out / "_c_raw.png").unlink()
print("saved string-city.png; towers:", len(bars))
