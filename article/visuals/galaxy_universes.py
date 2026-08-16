"""THE GALAXY OF SURVIVING UNIVERSES — cinematic starfield (NASA SVS style).

REAL DATA: each point is a candidate theory (lam, D) of the CHR family.
It shines as a star iff D <= T_hat(lam) (the proven shore law, paper 2);
brightness/height = safety margin. Dead theories = faint red embers below.
"""

import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import plotly.graph_objects as go  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from PIL import Image  # noqa: E402

random.seed(4)
xs, ys, zs, cols, sizes = [], [], [], [], []
dx, dy, dz = [], [], []
for i in range(2600):
    lam = Fraction(random.randint(1, 4500), 100)
    Th = T_hat(lam)
    D = Fraction(random.randint(3, max(4, int(float(Th) * 1.6))))
    margin = float((Th - D) / Th)
    x, y = float(lam), float(D)
    if margin >= 0:  # выживший мир — звезда
        xs.append(x); ys.append(y)
        zs.append(margin * 10 + random.uniform(-0.15, 0.15))
        cols.append(margin)
        sizes.append(2.2 + 7 * margin ** 1.5)
    else:            # мёртвый мир — тлеющий уголёк внизу
        dx.append(x); dy.append(y)
        dz.append(max(-6, margin * 6) + random.uniform(-0.2, 0.2))

STARS = [[0.0, "#7a3fd0"], [0.45, "#0aa3c2"], [0.8, "#3fe7f5"],
         [1.0, "#eafffe"]]
fig = go.Figure()
fig.add_trace(go.Scatter3d(x=dx, y=dy, z=dz, mode="markers",
                           marker=dict(size=1.6, color="#5c1330",
                                       opacity=0.5), showlegend=False))
fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="markers",
                           marker=dict(size=sizes, color=cols,
                                       colorscale=STARS, opacity=0.9,
                                       line=dict(width=0)),
                           showlegend=False))
# струна D=23, lam=1 — маяк
fig.add_trace(go.Scatter3d(x=[1], y=[23], z=[0.35], mode="markers+text",
                           marker=dict(size=9, color="#f9f871",
                                       symbol="diamond"),
                           text=["  THE STRING — on the very edge"],
                           textfont=dict(color="#f9f871", size=15),
                           textposition="middle right", showlegend=False))
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#05030c",
    title=dict(text="THE GALAXY OF SURVIVING UNIVERSES<br>"
                    "<sup>every star = a theory of gravity that passes our PROVEN shore law;<br>glow = safety margin; red embers = impossible worlds; diamond = the string, exactly on the edge</sup>",
               font=dict(color="#e8e6f0", size=21), x=0.03),
    scene=dict(
        xaxis=dict(title="which theory (lambda)", color="#5c5870",
                   gridcolor="#150e24", showbackground=False),
        yaxis=dict(title="dimensions of the world (D)", color="#5c5870",
                   gridcolor="#150e24", showbackground=False),
        zaxis=dict(title="", color="#5c5870", gridcolor="#150e24",
                   showbackground=False, showticklabels=False),
        camera=dict(eye=dict(x=1.05, y=-1.25, z=0.35),
                    center=dict(x=0, y=0, z=-0.05)),
    ),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_g_raw.png"), scale=2)
Image.open(out / "_g_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "galaxy-universes.png")
(out / "_g_raw.png").unlink()
print("saved galaxy-universes.png; stars:", len(xs), "embers:", len(dx))
