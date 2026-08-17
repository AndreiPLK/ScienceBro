"""THE SLIDING SPOTLIGHT — the keystone mechanism, real exact data.

What the picture shows (wave-relief style, one quantity across a family):

  * The bracket that decides whether a knife cuts is EXACTLY
        I(D) = integral of Hhat(u) * u^p * (1-u)^Q du   over u in (0,1),
    with Q = D/2 + n - j - 2.
  * Hhat is the same fixed shape for every dimension D — it does not
    depend on D at all: one positive hill and one negative dip.
  * D only changes the WEIGHT u^p (1-u)^Q — a spotlight that slides.
    Small D lights the whole interval; large D squeezes the light towards
    u -> 0, where the shape is negative.

Parameters are the tightest measured case (knife j=4, level n=14,
lam = 7): the shore sits at D = 131.10 and the verdict flips only at
D = 139.69 — the knife starts biting 6.5% ABOVE the shore, never below.

Data: exact rational Hhat coefficients from lab/keystone_beta.py; floats
are used only for drawing.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from keystone_beta import Hhat_coeffs  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from PIL import Image  # noqa: E402

J, N, LAM = 4, 14, Fraction(7)
TH = float(T_hat(LAM))

desc = [float(c) for c in Hhat_coeffs(J, N, LAM)]
us = np.linspace(0.002, 0.998, 240)
Hh = np.array([sum(c * u ** (J - 1 - t) for t, c in enumerate(desc))
               for u in us])

Ds = np.linspace(4.0, TH * 1.30, 160)
p = N - J - 0.5
Z, verdict = [], []
for D in Ds:
    w = us ** p * (1 - us) ** (D / 2 + N - J - 2)
    integ = Hh * w
    m = np.max(np.abs(integ))
    Z.append(integ / m if m > 0 else integ)
    verdict.append(np.trapezoid(integ, us))
verdict = np.array(verdict)
flip = float(Ds[np.argmax(verdict <= 0)]) if (verdict <= 0).any() else None

fig = go.Figure()
fig.add_trace(go.Surface(
    x=us, y=Ds, z=Z, showscale=False, cmid=0.0,
    colorscale=[[0.0, "#ff2a6d"], [0.40, "#8a1f52"], [0.5, "#1d0d2b"],
                [0.60, "#12648f"], [1.0, "#4df0ff"]],
    lighting=dict(ambient=0.62, diffuse=0.68, specular=0.2, roughness=0.7)))

# the shore (yellow) and where the knife actually starts biting (white)
fig.add_trace(go.Scatter3d(
    x=us, y=[TH] * len(us), z=[0.008] * len(us), mode="lines",
    line=dict(color="#f9f871", width=9), showlegend=False))
if flip is not None:
    fig.add_trace(go.Scatter3d(
        x=us, y=[flip] * len(us), z=[0.008] * len(us), mode="lines",
        line=dict(color="#ffffff", width=5), showlegend=False))

ann = [
    dict(x=0.99, y=TH, z=0.62, text="THE SHORE — D = 131.1",
         font=dict(color="#ffe94a", size=15), showarrow=False,
         xanchor="left"),
    dict(x=0.99, y=flip if flip else TH, z=-0.75,
         text="the knife finally bites — D = 139.7",
         font=dict(color="#ffffff", size=15), showarrow=False,
         xanchor="left"),
    dict(x=0.30, y=Ds[2], z=1.22, text="POSITIVE HILL",
         font=dict(color="#8ff0ff", size=15), showarrow=False),
    dict(x=0.05, y=Ds[-2], z=-1.05, text="NEGATIVE DIP",
         font=dict(color="#ff8fb0", size=15), showarrow=False)]

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0714", plot_bgcolor="#0b0714",
    title=dict(
        text="WHY DIMENSION DECIDES<br><sup>The shape never changes — only "
             "the light moves. Exact data, knife j=4 at level n=14.<br>"
             "The spotlight is the positive weight; the dimension D is the "
             "only thing that slides it. The verdict flips<br>where the light "
             "leaves the hill — and that happens ABOVE the shore, never "
             "below.</sup>",
        font=dict(color="#e8e6f0", size=23), x=0.025, y=0.965),
    scene=dict(
        xaxis=dict(title="u — position inside the bracket",
                   backgroundcolor="#0b0714", gridcolor="#2a2140",
                   color="#b9b4cc"),
        yaxis=dict(title="D — dimensions of spacetime",
                   backgroundcolor="#0b0714", gridcolor="#2a2140",
                   color="#b9b4cc"),
        zaxis=dict(title="what gets integrated", showticklabels=False,
                   backgroundcolor="#0b0714", gridcolor="#2a2140",
                   color="#b9b4cc"),
        aspectratio=dict(x=1.45, y=1.7, z=0.72),
        annotations=ann,
        camera=dict(eye=dict(x=1.45, y=-1.55, z=0.72),
                    center=dict(x=0, y=0, z=-0.06))),
    margin=dict(l=0, r=0, t=126, b=0), width=1520, height=860)

out = Path(__file__).resolve().parent / "sliding-spotlight.png"
fig.write_image(str(out), scale=2)
im = Image.open(out)
im.thumbnail((1800, 1800))
im.save(out)
print("saved", out, im.size, "| shore", round(TH, 2),
      "| flips at D =", None if flip is None else round(flip, 2))
