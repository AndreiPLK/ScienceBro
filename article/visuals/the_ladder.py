"""THE LADDER -- a plain-language picture of where the proof actually stands.

Not a scientific plot. The founder asked for something he can look at and
understand without the mathematics, so this shows the shape of the problem and
which parts are done, in words a person can read.

The problem really is a ladder. Each rung is one condition that must hold, and
they are ordered by depth -- how far down from the top of a family the condition
sits. The top rung was published a year ago. The second rung became provable
today. The deep rungs are still held by machine certificates rather than by an
argument, and the bottom is where the hard analysis lives.
"""

import sys
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image, ImageChops

BG = "#080b12"
WHITE = "#e8fdf6"
DIM = "#8ba1bd"

RUNGS = [
    ("THE TOP RUNG", "published a year ago — this is our own theorem", "SECURED", "#5fe0d8", 0.30),
    (
        "THE SECOND RUNG",
        "secured today: the whole check shrinks to two numbers",
        "SECURED TODAY",
        "#c9f7e8",
        0.34,
    ),
    (
        "THE NEXT RUNGS",
        "the same method should reach them — this is the next job",
        "IN REACH",
        "#9ff2e0",
        0.20,
    ),
    (
        "THE MIDDLE",
        "half a million checked by machine, not one failure",
        "MACHINE ONLY",
        "#d8b98a",
        0.20,
    ),
    ("THE BOTTOM", "where the hard part lives — still open", "STILL OPEN", "#8a6f5a", 0.18),
]

fig = go.Figure()
fig.update_xaxes(range=[0, 10], visible=False)
fig.update_yaxes(range=[0, 10], visible=False)

# ladder rails
for x in (1.15, 7.9):
    fig.add_shape(type="line", x0=x, x1=x, y0=1.9, y1=9.5, line=dict(color="#1d3350", width=7))

y = 8.95
for title, body, badge, col, alpha in RUNGS:
    fig.add_shape(
        type="rect",
        x0=1.15,
        x1=7.9,
        y0=y - 0.55,
        y1=y + 0.55,
        line=dict(color=col, width=3),
        fillcolor=col,
        opacity=alpha,
        layer="below",
    )
    fig.add_annotation(
        x=1.45,
        y=y + 0.22,
        text=f"<b>{title}</b>",
        showarrow=False,
        font=dict(color=WHITE, size=21),
        xanchor="left",
    )
    fig.add_annotation(
        x=1.45,
        y=y - 0.24,
        text=body,
        showarrow=False,
        font=dict(color=DIM, size=14),
        xanchor="left",
    )
    fig.add_annotation(
        x=7.72,
        y=y,
        text=f"<b>{badge}</b>",
        showarrow=False,
        font=dict(color=col, size=13),
        xanchor="right",
    )
    y -= 1.45

fig.add_annotation(
    x=8.55,
    y=2.1,
    ax=8.55,
    ay=8.95,
    xref="x",
    yref="y",
    axref="x",
    ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.4,
    arrowwidth=3.5,
    arrowcolor="#5fe0d8",
)
fig.add_annotation(
    x=8.75,
    y=8.1,
    text="we are<br>working<br>down",
    showarrow=False,
    font=dict(color="#5fe0d8", size=15),
    xanchor="left",
)
fig.add_annotation(
    x=8.75,
    y=2.9,
    text="the bottom<br>is the hard<br>part",
    showarrow=False,
    font=dict(color="#d8b98a", size=15),
    xanchor="left",
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    title=dict(
        text="WHERE WE ACTUALLY ARE"
        "<br><sup>The problem is a ladder. Every rung is one condition that must hold, "
        "and there are infinitely many of them.<br>We are securing them from the top "
        "down — and today one more rung stopped being a check and became a proof.</sup>",
        font=dict(color=WHITE, size=30),
        x=0.02,
        y=0.955,
    ),
    margin=dict(l=30, r=30, t=118, b=60),
    width=1500,
    height=930,
    showlegend=False,
)
fig.add_annotation(
    x=0.3,
    y=0.75,
    xref="x",
    yref="y",
    xanchor="left",
    showarrow=False,
    text="<b>What changed today:</b> checking the second rung used to mean testing every "
    "dimension one by one.<br>It turns out the quantity bends only one way — so two "
    "numbers settle it, for every case at once.",
    font=dict(color="#c9f7e8", size=15),
    align="left",
)

out = Path(__file__).resolve().parent / "the-ladder.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (8, 11, 18))
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
print("saved", out, Image.open(out).size, file=sys.stderr)
