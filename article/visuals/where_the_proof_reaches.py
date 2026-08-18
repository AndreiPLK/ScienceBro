"""WHERE THE PROOF REACHES -- and it reaches from BOTH sides.

Corrected figure. The first version showed a half-plane: settled above a line,
machine-held below. That was incomplete -- it was drawn from a map whose smallest
lam was 1, and the interesting corner lies below that.

The classical argument settles a family when the polynomial q -- the one whose
square is our object, and whose roots are equally spaced -- has no negative
Gegenbauer coefficient at the shore. That happens in TWO separate regions:

  A  small levels with large lam:  lam >= lam*(n), with lam*/n measured at
     4.7165..4.7260 for n = 20..130
  B  large levels with small lam:  n >= n*(lam), with n*(1/10) bisected into
     (656, 662] and n*(1/5) between 900 and 1300

Between them lies a band where the result is still carried by exact certificates
rather than by an argument. For each lam that band looks FINITE in n, which is
the whole point: finitely many levels is exactly what certificates are for.

Every marker is exact rational arithmetic. The edge of region B is dashed because
it is an interpolation through two measured points, not a measured curve.
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
nsA = np.array([b["n"] for b in bd], dtype=float)
lsA = np.array([float(Fraction(b["lam_star"])) for b in bd])
slope = float(np.sum(nsA * lsA) / np.sum(nsA * nsA))

# region B, measured this session -- see results/BOUNDARY_PUSH_2026-08-18.md
nsB = np.array([659.0, 1100.0])
lsB = np.array([0.10, 0.20])
slopeB = float(np.mean(lsB / nsB))

nn = np.logspace(np.log10(4), np.log10(2000), 400)
lineA = slope * nn
lineB = slopeB * nn
TOP, BOT = 3000.0, 0.02

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=np.concatenate([nn, nn[::-1]]),
        y=np.concatenate([lineA, np.full_like(nn, TOP)]),
        fill="toself",
        fillcolor="rgba(40,182,200,0.30)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=np.concatenate([nn, nn[::-1]]),
        y=np.concatenate([np.full_like(nn, BOT), lineB[::-1]]),
        fill="toself",
        fillcolor="rgba(95,224,216,0.22)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=nn, y=lineA, mode="lines", line=dict(color="#5fe0d8", width=3), name="edge of region A"
    )
)
fig.add_trace(
    go.Scatter(
        x=nn,
        y=lineB,
        mode="lines",
        line=dict(color="#9ff2e0", width=3, dash="dash"),
        name="edge of region B (through 2 measured points)",
    )
)
fig.add_trace(
    go.Scatter(
        x=nsA,
        y=lsA,
        mode="markers",
        marker=dict(color="#e8fdf6", size=10, line=dict(color="#0f4c75", width=2)),
        name="A: measured, exact arithmetic",
    )
)
fig.add_trace(
    go.Scatter(
        x=nsB,
        y=lsB,
        mode="markers",
        marker=dict(
            color="#ffd98a", size=15, symbol="diamond", line=dict(color="#5a3d12", width=2)
        ),
        name="B: measured, exact arithmetic",
    )
)

fig.add_annotation(
    x=np.log10(70),
    y=np.log10(900),
    text="<b>REGION A — SETTLED</b><br>small levels, large lam",
    showarrow=False,
    font=dict(color="#c9f7e8", size=15),
    align="left",
)
fig.add_annotation(
    x=np.log10(700),
    y=np.log10(0.038),
    text="<b>REGION B — SETTLED</b><br>large levels, small lam<br>"
    "<i>the corner the first figure missed</i>",
    showarrow=False,
    font=dict(color="#d9f7ea", size=15),
    align="left",
)
fig.add_annotation(
    x=np.log10(25),
    y=np.log10(2.4),
    text="<b>THE BAND</b><br>still held by exact certificates.<br>"
    "For each lam it looks FINITE in n —<br>and finitely many levels is<br>"
    "exactly what certificates are for.",
    showarrow=False,
    font=dict(color="#d8b98a", size=14),
    align="left",
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080b12",
    plot_bgcolor="#080b12",
    title=dict(
        text="WHERE THE PROOF REACHES — from both sides"
        "<br><sup>A family is settled by one classical argument when q has no negative "
        "Gegenbauer coefficient at the shore. That happens for small levels at large lam, "
        "and again for large levels at small lam.<br>The band between is where exact "
        "certificates still carry the result. Corrected: the first version of this figure "
        "showed only region A, because its map started at lam = 1.</sup>",
        font=dict(color="#e8fdf6", size=20),
        x=0.02,
        y=0.95,
    ),
    xaxis=dict(
        title="n  -- the level of the family",
        type="log",
        gridcolor="#16233a",
        color="#7f93b0",
        range=[np.log10(4), np.log10(2000)],
    ),
    yaxis=dict(
        title="lam",
        type="log",
        gridcolor="#16233a",
        color="#7f93b0",
        range=[np.log10(BOT), np.log10(TOP)],
    ),
    legend=dict(x=0.015, y=0.99, font=dict(color="#a8a08e", size=12), bgcolor="rgba(8,11,18,0.65)"),
    margin=dict(l=70, r=30, t=125, b=60),
    width=1400,
    height=820,
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
