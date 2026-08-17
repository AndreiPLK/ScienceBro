"""ALMOST POSITIVE — the exact shape of where the proof is stuck.

Real exact data. The quantity that decides whether a constraint cuts is a
contour integral, and the integral is the same on ANY closed contour around
the origin (the integrand is a polynomial divided by a power). So the contour
is ours to choose.

On the best contour found so far the density is positive almost everywhere and
dips below zero by less than a quarter of one percent. If a contour with NO dip
exists, positivity is immediate and uniform in the constraint index -- the whole
remaining gap of the programme closes at once.

The picture shows the density along the contour for several constraint indices,
normalised by the answer, with the zero line marked. The dip is the enemy.
"""

import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402
from keystone_saddles import build_P, coeff  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

CASES = [(10, 14, 0.031942), (12, 16, 0.032765), (14, 18, 0.033457), (16, 20, 0.034083)]
COLORS = ["#4df0ff", "#8ff0ff", "#f9f871", "#ff8fb0"]

fig = make_subplots(
    rows=1,
    cols=2,
    column_widths=[0.56, 0.44],
    horizontal_spacing=0.09,
    subplot_titles=(
        "the whole loop: one big positive hump",
        "zoom on the dip: this is the entire problem",
    ),
)
for (j, n, r), col in zip(CASES, COLORS):
    P = build_P(j, n, F(1))
    N = j - 1
    true = float(coeff(P, N))
    pf = np.polynomial.Polynomial([float(c) for c in P])
    t = np.linspace(0, 2 * np.pi, 3000)
    dens = (pf(r * np.exp(1j * t)) * np.exp(-1j * N * t) / r**N).real / abs(true)
    fig.add_trace(
        go.Scatter(
            x=t / np.pi,
            y=dens,
            mode="lines",
            name=f"constraint j = {j}",
            line=dict(color=col, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=t / np.pi, y=dens, mode="lines", showlegend=False, line=dict(color=col, width=2)
        ),
        row=1,
        col=2,
    )

fig.add_hline(y=0, line=dict(color="#ff2a6d", width=2, dash="dash"), row=1, col=1)
fig.add_hline(y=0, line=dict(color="#ff2a6d", width=2, dash="dash"), row=1, col=2)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b0714",
    plot_bgcolor="#0b0714",
    title=dict(
        text="ALMOST POSITIVE — where the proof is stuck<br><sup>The verdict "
        "is an integral around a closed loop, and the loop is ours to "
        "choose. On the best loop found so far<br>the density is one big "
        "positive hump that dips below zero by two ten-thousandths. A loop "
        "with no dip proves the theorem outright.</sup>",
        font=dict(color="#e8e6f0", size=21),
        x=0.03,
        y=0.94,
    ),
    xaxis=dict(
        title="position along the loop (multiples of pi)",
        gridcolor="#2a2140",
        color="#b9b4cc",
        zeroline=False,
    ),
    yaxis=dict(title="density / answer", gridcolor="#2a2140", color="#b9b4cc", zeroline=False),
    xaxis2=dict(
        title="position along the loop (multiples of pi)",
        range=[0, 0.55],
        gridcolor="#2a2140",
        color="#b9b4cc",
        zeroline=False,
    ),
    yaxis2=dict(
        title="density / answer  (x1000)",
        range=[-0.0006, 0.0004],
        gridcolor="#2a2140",
        color="#b9b4cc",
        zeroline=False,
    ),
    legend=dict(font=dict(color="#b9b4cc"), bgcolor="rgba(0,0,0,0)", x=0.02, y=0.98),
    margin=dict(l=70, r=30, t=118, b=60),
    width=1480,
    height=600,
)

out = Path(__file__).resolve().parent / "almost-positive.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (11, 7, 20))
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
