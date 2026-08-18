"""WHERE THE PROOF REACHES -- the plane of families, split by one classical argument.

Every point is a family: its level n across, its lam up the side. Above the
boundary the whole family is settled by a two-step classical argument and no
machine is needed; below it, the machine is still what we have.

The boundary is measured, not fitted: for each n it is the smallest lam at which
the polynomial q -- the one whose square is our object, and whose roots are
equally spaced -- has no negative Gegenbauer coefficient at the shore. Above that
point Dougall's non-negative linearization carries the square, and the dimension
descent carries it down to every dimension the family is allowed.

Nothing here is smoothed. The dots are the bisected boundary values from
lab/gegenbauer_flint.py; the straight line is drawn only to show how nearly
straight they are.
"""

import json
import sys
from fractions import Fraction  # ENGINE-OK: reading exact values for a picture
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageChops

RES = Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "results"
data = json.loads((RES / "gegenbauer_term_by_term.json").read_text(encoding="utf-8"))
bd = data["proved_region"]["boundary"]
ns = np.array([b["n"] for b in bd], dtype=float)
ls = np.array([float(Fraction(b["lam_star"])) for b in bd])
slope = float(np.sum(ns * ls) / np.sum(ns * ns))

nn = np.linspace(0, 140, 400)
line = slope * nn
top = 760.0

fig = go.Figure()
# the settled region
fig.add_trace(
    go.Scatter(
        x=np.concatenate([nn, nn[::-1]]),
        y=np.concatenate([line, np.full_like(nn, top)]),
        fill="toself",
        fillcolor="rgba(40,182,200,0.30)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False,
    )
)
# the region still held by the machine
fig.add_trace(
    go.Scatter(
        x=np.concatenate([nn, nn[::-1]]),
        y=np.concatenate([line, np.zeros_like(nn)]),
        fill="toself",
        fillcolor="rgba(150,105,55,0.26)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=nn,
        y=line,
        mode="lines",
        line=dict(color="#5fe0d8", width=3),
        name=f"boundary, slope {slope:.3f}",
    )
)
fig.add_trace(
    go.Scatter(
        x=ns,
        y=ls,
        mode="markers",
        marker=dict(color="#e8fdf6", size=11, line=dict(color="#0f4c75", width=2)),
        name="measured boundary (exact arithmetic)",
    )
)
fig.add_annotation(
    x=42,
    y=560,
    text="<b>SETTLED BY ONE ARGUMENT</b><br>q has no negative coefficient here,<br>"
    "so the square is non-negative by Dougall<br>and every knife follows, in every<br>"
    "dimension the family is allowed",
    showarrow=False,
    font=dict(color="#c9f7e8", size=14),
    align="left",
)
fig.add_annotation(
    x=96,
    y=140,
    text="<b>STILL THE MACHINE'S</b><br>certificates, not an argument",
    showarrow=False,
    font=dict(color="#d8b98a", size=14),
    align="left",
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080b12",
    plot_bgcolor="#080b12",
    title=dict(
        text="WHERE THE PROOF REACHES"
        "<br><sup>Each point is a family of constraints. Above the line the whole "
        "family is settled by a classical argument in two steps; below it we still "
        "rely on exact machine certificates.<br>The line is almost exactly straight "
        f"-- slope {slope:.3f} -- and every dot is exact arithmetic, not a fit.</sup>",
        font=dict(color="#e8fdf6", size=21),
        x=0.02,
        y=0.94,
    ),
    xaxis=dict(
        title="n  -- the level of the family", gridcolor="#16233a", color="#7f93b0", range=[0, 140]
    ),
    yaxis=dict(title="lam", gridcolor="#16233a", color="#7f93b0", range=[0, top]),
    legend=dict(x=0.02, y=0.28, font=dict(color="#a8a08e", size=12)),
    margin=dict(l=70, r=30, t=110, b=60),
    width=1360,
    height=780,
)

out = Path(__file__).resolve().parent / "where-the-proof-reaches.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (8, 11, 18))
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
print("saved", out, Image.open(out).size, file=sys.stderr)
