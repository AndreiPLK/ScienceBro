"""ONE CURVE -- every knife of the family vanishes on the same line.

Result of the night of 2026-08-17/18 (results/SCALING_LIMIT_THEOREM.md). In the
scaling limit n = rho lam, D = d lam, lam -> infinity at fixed j, the closed form
of knife j sums by Newton's binomial to

    knife_j  ->  (2 rho^2 + 12 rho + 6 - d rho)^(j-1) / (6 (rho+1)^2)^(j-1)

so EVERY knife vanishes on the single curve d = 2 rho + 12 + 6 / rho, and the
only difference between knives is the PARITY of the exponent:

  * odd j  -> even power  -> never negative; those knives cannot cut, whatever d;
  * even j -> odd power   -> the knife holds exactly below the curve.

The curve's minimum sits at rho = sqrt(3), where d = 12 + 4 sqrt(3) = 18.928...,
which is exactly the shore asymptote obtained earlier by a completely different
route. So the even knives are tangent to the shore, not crossing it.

Drawn here: the curve, its minimum, the shore asymptote, and the sign of the
leading term on both sides for an even and an odd knife. Nothing is fitted --
every line is the exact formula.
"""

import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageChops
from plotly.subplots import make_subplots

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))

rho = np.linspace(0.35, 6.0, 900)
curve = 2 * rho + 12 + 6 / rho
rho_star = np.sqrt(3.0)
d_star = 12 + 4 * np.sqrt(3.0)

fig = make_subplots(
    rows=1,
    cols=2,
    column_widths=[0.56, 0.44],
    horizontal_spacing=0.10,
    subplot_titles=(
        "the curve every knife vanishes on",
        "the leading term, on a slice through rho = sqrt(3)",
    ),
)

fig.add_trace(
    go.Scatter(
        x=rho,
        y=curve,
        mode="lines",
        name="d = 2rho + 12 + 6/rho",
        line=dict(color="#4df0ff", width=3),
    ),
    row=1,
    col=1,
)
fig.add_hline(y=d_star, line=dict(color="#f9f871", width=2, dash="dash"), row=1, col=1)
fig.add_trace(
    go.Scatter(
        x=[rho_star],
        y=[d_star],
        mode="markers+text",
        showlegend=False,
        marker=dict(color="#ff2a6d", size=14, symbol="diamond"),
        text=["  rho = sqrt(3),  d = 12 + 4sqrt(3)"],
        textposition="middle right",
        textfont=dict(color="#ff8fb0", size=13),
    ),
    row=1,
    col=1,
)
fig.add_annotation(
    x=4.6,
    y=d_star - 2.6,
    text="the shore asymptote — reached by a different route in the published work",
    showarrow=False,
    font=dict(color="#f9f871", size=12),
    row=1,
    col=1,
)
fig.add_annotation(
    x=4.6,
    y=32,
    text="above the curve: EVEN knives fail here",
    showarrow=False,
    font=dict(color="#ff8fb0", size=12),
    row=1,
    col=1,
)
fig.add_annotation(
    x=4.6,
    y=15.5,
    text="below: every knife holds",
    showarrow=False,
    font=dict(color="#8ff0ff", size=12),
    row=1,
    col=1,
)

d_line = np.linspace(12.0, 26.0, 600)
base = 2 * rho_star**2 + 12 * rho_star + 6 - d_line * rho_star
den = (6 * (rho_star + 1) ** 2) ** 1.0
for j, col in ((3, "#c9e86b"), (4, "#4df0ff"), (5, "#ff8fb0")):
    y = np.sign(base) * np.abs(base / den) ** (j - 1) * (1 if (j - 1) % 2 == 0 else 1)
    y = (base / den) ** (j - 1)
    fig.add_trace(
        go.Scatter(
            x=d_line,
            y=np.sign(y) * np.log10(1 + np.abs(y)),
            mode="lines",
            name=f"knife {j} ({'even' if (j - 1) % 2 == 0 else 'odd'} power)",
            line=dict(color=col, width=3),
        ),
        row=1,
        col=2,
    )
fig.add_vline(y0=0, x=d_star, line=dict(color="#f9f871", width=2, dash="dash"), row=1, col=2)
fig.add_hline(y=0, line=dict(color="#6a6252", width=1), row=1, col=2)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="ONE CURVE — every knife of the family vanishes on the same line"
        "<br><sup>Exact, not fitted. In the scaling limit the closed form of "
        "knife j sums by Newton's binomial to (2rho² + 12rho + 6 − d·rho)^(j−1), "
        "so all knives share one vanishing curve<br>and differ only by the parity "
        "of the exponent: odd j gives an even power that never turns negative, "
        "even j gives an odd power that does. The curve's minimum is exactly the "
        "shore.</sup>",
        font=dict(color="#ede8dc", size=20),
        x=0.02,
        y=0.95,
    ),
    xaxis=dict(title="rho = n / lam", color="#a8a08e", gridcolor="#322e26"),
    yaxis=dict(title="d = D / lam", color="#a8a08e", gridcolor="#322e26", range=[12, 40]),
    xaxis2=dict(title="d = D / lam", color="#a8a08e", gridcolor="#322e26"),
    yaxis2=dict(title="signed log of the leading term", color="#a8a08e", gridcolor="#322e26"),
    legend=dict(font=dict(color="#a8a08e", size=11), x=0.60, y=0.30, bgcolor="rgba(20,19,15,0.8)"),
    margin=dict(l=80, r=30, t=140, b=70),
    width=1560,
    height=680,
)

out = Path(__file__).resolve().parent / "one-curve.png"
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
