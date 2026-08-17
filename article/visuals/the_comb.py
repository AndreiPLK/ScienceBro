"""THE COMB — tonight's finding, in 3D.

Real exact data via lab/contour_lib.py (the vetted implementation).

For each knife j and each deformation lam we find the best loop and record the
minimum of the integrand along it, normalised by the answer. Two things happen:

  * where the minimum is >= 0 the loop is SIGN-DEFINITE and positivity of that
    knife is immediate -- no asymptotics, no certificates;
  * where it dips below zero the loop fails and the knife needs machine work.

Plotting that minimum as a relief over (j, lam) shows the structure we did not
expect: the safe regions are WINDOWS, they drift with lam, and along any fixed
lam they recur -- while the failing blocks grow in width by exactly 6 knives
each time (measured at lam = 1: widths 8, 14, 20). A comb whose teeth widen.

Height is a signed logarithmic scale so that dips of 1e-3 and 1e-11 are both
visible: sign(m) * log10(1 + |m| / 1e-12).
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from contour_lib import best_circle  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

JS = list(range(8, 61, 2))
LAMS = [F(1, 2), F(1), F(3), F(7), F(14), F(26), F(60), F(150)]
CACHE = Path(__file__).resolve().parent / "the_comb_data.json"


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    data = {}
    for lam in LAMS:
        for j in JS:
            r, m = best_circle(j, j + 4, lam)
            if m is None:
                continue
            data[f"{j}_{lam}"] = m
            print(f"  j={j} lam={lam}: {m:+.3e}", flush=True)
    CACHE.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return data


data = gather()


def h(m):
    if m is None:
        return np.nan
    return np.sign(m) * np.log10(1 + abs(m) / 1e-12)


Z = [[h(data.get(f"{j}_{lam}")) for j in JS] for lam in LAMS]
lam_f = [float(x) for x in LAMS]

fig = go.Figure()
fig.add_trace(
    go.Surface(
        x=JS,
        y=list(range(len(LAMS))),
        z=Z,
        showscale=False,
        cmid=0.0,
        colorscale=[
            [0.0, "#8a1f52"],
            [0.45, "#ff2a6d"],
            [0.5, "#1d0d2b"],
            [0.55, "#12648f"],
            [1.0, "#4df0ff"],
        ],
        lighting=dict(ambient=0.66, diffuse=0.66, specular=0.15, roughness=0.75),
        contours=dict(z=dict(show=True, start=-12, end=12, size=2, color="#0b0714", width=1)),
    )
)

ann = [
    dict(
        x=JS[len(JS) // 2],
        y=len(LAMS) - 1,
        z=11,
        text="CYAN = a sign-definite loop exists<br>positivity is immediate here",
        font=dict(color="#8ff0ff", size=14),
        showarrow=False,
    ),
    dict(
        x=JS[3],
        y=1,
        z=-11,
        text="CRIMSON = the loop dips<br>this knife needs machine certificates",
        font=dict(color="#ff8fb0", size=14),
        showarrow=False,
    ),
]

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="THE COMB — where a single loop already proves positivity<br>"
        "<sup>Exact data. Height is the signed depth of the integrand's "
        "minimum on the best loop (log scale, so 1e-3 and 1e-11 are both "
        "visible).<br>Cyan regions need no proof at all; crimson blocks do. "
        "The safe regions are WINDOWS that drift with the deformation and "
        "recur, while<br>the failing blocks widen by exactly 6 knives each "
        "time (8, 14, 20 at lam = 1). That arithmetic is the clue we are "
        "chasing.</sup>",
        font=dict(color="#ede8dc", size=20),
        x=0.025,
        y=0.965,
    ),
    scene=dict(
        xaxis=dict(
            title="j — which knife", backgroundcolor="#14130f", gridcolor="#322e26", color="#a8a08e"
        ),
        yaxis=dict(
            title="lam — family of theories",
            tickvals=list(range(len(LAMS))),
            ticktext=[str(x) for x in LAMS],
            backgroundcolor="#14130f",
            gridcolor="#322e26",
            color="#a8a08e",
        ),
        zaxis=dict(
            title="signed depth (log)",
            backgroundcolor="#14130f",
            gridcolor="#322e26",
            color="#a8a08e",
        ),
        aspectratio=dict(x=1.7, y=1.15, z=0.7),
        annotations=ann,
        camera=dict(eye=dict(x=1.55, y=-1.5, z=0.75), center=dict(x=0, y=0, z=-0.08)),
    ),
    margin=dict(l=0, r=0, t=132, b=0),
    width=1500,
    height=760,
)

out = Path(__file__).resolve().parent / "the-comb.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (20, 19, 15))
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
print("saved", out, Image.open(out).size)
