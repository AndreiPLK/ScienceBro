"""THE WATERFALL -- the fourth knife's margin, sheet by sheet, going over the edge.

Real numbers, drawn to be looked at. Each sheet is one family (one lam): the
height is how much room the fourth knife has left before it would cut, over the
plane of level n and dimension D. Every sheet ends at its own shore -- the
dimension where the family stops being allowed -- and that is where the water
goes over.

Why it looks like a waterfall rather than a hill: the margin is enormous deep
inside the allowed region and collapses toward the shore, and the shore itself
moves outward as lam grows. So the sheets stack into a cascade whose lip traces
the shore curve.

Height is a signed logarithm of the knife polynomial, so ten orders of magnitude
fit in one picture; the water is cyan where there is room and turns dark at the
lip. Nothing is fitted and nothing is smoothed: every value is the exact
polynomial of lab/knife_closed_form.py evaluated on the grid.
"""

import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import sympy as sp  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from knife_closed_form import D as Dsym  # noqa: E402
from knife_closed_form import knife_polynomial, lam as lamsym, n as nsym  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

P4 = sp.lambdify((nsym, Dsym, lamsym), knife_polynomial(4), "numpy")
LAMS = [F(1), F(2), F(3), F(5), F(8), F(12), F(18), F(26), F(38), F(55)]

fig = go.Figure()
pal = ["#0b2c4a", "#0f4c75", "#1682a8", "#28b6c8", "#5fe0d8", "#9ff2e0", "#c9f7e8", "#e8fdf6"]

for idx, lv in enumerate(LAMS):
    shore = T_hat(float(lv))
    nn = np.linspace(4, 90, 170)
    # x is the fraction of the way to that family's own shore, so every sheet
    # ends at exactly 1 and the lips line up into a single wall of water
    frac = np.linspace(0.02, 0.999, 190)
    dd = 4 + frac * (shore - 4)
    N, Dg = np.meshgrid(nn, dd, indexing="ij")
    V = np.maximum(P4(N, Dg, float(lv)), 1e-300)
    # FALL relative to the start of the sheet: 0 at D = 4, plunging at the lip.
    # The first attempt plotted the raw logarithm and the sheets came out flat
    # and overlapping -- the variation across a sheet is dwarfed by the variation
    # between families, so it has to be measured within each sheet.
    H = np.log10(V) - np.log10(V[:, :1])
    # the lip: fade the sheet out exactly at the shore
    fig.add_trace(
        go.Surface(
            x=frac,
            y=np.full_like(frac, float(lv)),
            z=H.T,
            surfacecolor=H.T,
            showscale=(idx == len(LAMS) - 1),
            colorscale=[
                [0.0, "#101a2b"],
                [0.25, "#123a5c"],
                [0.5, "#1682a8"],
                [0.75, "#57dcd2"],
                [1.0, "#e8fdf6"],
            ],
            opacity=0.93,
            lighting=dict(ambient=0.55, diffuse=0.75, specular=0.35, roughness=0.45),
            contours=dict(z=dict(show=True, start=-30, end=0, size=2, color="#04070d", width=1)),
            colorbar=dict(
                title=dict(text="room left<br>(log scale)", font=dict(color="#a8a08e", size=11)),
                tickfont=dict(color="#a8a08e", size=10),
                thickness=14,
                len=0.7,
            ),
            name=f"lam = {lv}",
        )
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080b12",
    plot_bgcolor="#080b12",
    title=dict(
        text="THE WATERFALL — the fourth knife's margin going over the edge"
        "<br><sup>One sheet per family. Along each sheet the dimension runs from "
        "4 up to that family's own shore, and the height is how many orders of "
        "magnitude the margin has fallen since the start.<br>Every sheet plunges "
        "at the same place — the lip is the shore — and the fall gets steeper for "
        "larger families. That cliff is why the proof needed a fine dust of boxes "
        "along the edge and coarse ones everywhere else.</sup>",
        font=dict(color="#e8fdf6", size=20),
        x=0.02,
        y=0.95,
    ),
    scene=dict(
        xaxis=dict(
            title="how far to that family's shore  (1 = the lip)",
            backgroundcolor="#080b12",
            gridcolor="#16233a",
            color="#7f93b0",
        ),
        yaxis=dict(
            title="lam — the family",
            backgroundcolor="#080b12",
            gridcolor="#16233a",
            color="#7f93b0",
            type="log",
        ),
        zaxis=dict(
            title="how far the margin has fallen (orders of magnitude)",
            backgroundcolor="#080b12",
            gridcolor="#16233a",
            color="#7f93b0",
        ),
        aspectratio=dict(x=1.3, y=1.25, z=0.95),
        camera=dict(eye=dict(x=-1.75, y=-1.55, z=0.72), center=dict(x=0, y=0, z=-0.05)),
    ),
    margin=dict(l=0, r=0, t=118, b=0),
    width=1560,
    height=860,
)

out = Path(__file__).resolve().parent / "the-waterfall.png"
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
print("saved", out, Image.open(out).size)
