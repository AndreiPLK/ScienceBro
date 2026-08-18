"""THE SIDE VIEW -- the depth curve, which is where the mechanism became visible.

Every number here is a PROVEN sign: computed by contour_lib.verdict_hp in ball
arithmetic (radius search included), typical ball radius 1e-105, so a plotted
sign is a theorem about the sampled points and not a floating-point opinion.
This matters because the float scan lied about exactly this range: it reported
dips of -1e-16 for j = 80..92 and exactly 0.0 from j = 94, all of it noise.

WHAT THE CURVE SHOWS. Height is log10 of the depth of the integrand's minimum on
the best loop; colour is its sign (cyan = the loop already proves that knife
positive, crimson = it does not). Two features:

  * inside a crimson block the curve is a STRAIGHT LINE in j, over 14 knives at
    a time -- an exponential in disguise;
  * the straight pieces meet at CUSPS where the depth nearly touches zero
    (j = 80, 88, 118: down to 1e-21 against a ball radius of 1e-120).

At some cusps the sign flips and at others it does not (j = 88 touches and
returns). That is the signature of two competing exponential contributions:
the cusp is where their magnitudes cross, and whichever dominates sets the
sign. It means the block boundaries are not primitive objects -- they are the
subset of cusps at which the sign happened to change.

Two earlier arithmetic readings of this picture are now DEAD, and are named here
so they are not resurrected: block widths do not step by 6 (that was an artefact
of scanning only even j -- on the full integer grid the widths are 9, 17, 2, 24,
33), and the peak positions do not follow a power law (valid estimators on the
same data range from 0.76 to 1.40).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

RAW = Path("/tmp/full_int_scan.json")
d = json.loads(RAW.read_text(encoding="utf-8"))
js = sorted(int(k) for k in d)
mid = np.array([d[str(j)].get("mid", 0.0) for j in js])
lg = np.array([np.log10(abs(m)) if m else np.nan for m in mid])
pos = mid > 0

blocks, cur = [], None
for j, m in zip(js, mid, strict=False):
    if m < 0:
        cur = [j, j] if cur is None else [cur[0], j]
    elif cur is not None:
        blocks.append(tuple(cur))
        cur = None
if cur is not None:
    blocks.append(tuple(cur))

cusps = [js[i] for i in range(1, len(js) - 1) if lg[i] < lg[i - 1] and lg[i] < lg[i + 1]]

fig = go.Figure()
for a, b in blocks:
    fig.add_vrect(x0=a - 0.5, x1=b + 0.5, fillcolor="#ff2a6d", opacity=0.09, line_width=0)
fig.add_trace(
    go.Scatter(
        x=js,
        y=lg,
        mode="lines",
        line=dict(color="#6a6252", width=1),
        showlegend=False,
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter(
        x=[j for j, p in zip(js, pos, strict=False) if p],
        y=[v for v, p in zip(lg, pos, strict=False) if p],
        mode="markers",
        name="one loop already proves it",
        marker=dict(color="#4df0ff", size=8, line=dict(color="#14130f", width=1)),
    )
)
fig.add_trace(
    go.Scatter(
        x=[j for j, p in zip(js, pos, strict=False) if not p],
        y=[v for v, p in zip(lg, pos, strict=False) if not p],
        mode="markers",
        name="the loop dips -- needs certificates",
        marker=dict(color="#ff2a6d", size=8, line=dict(color="#14130f", width=1)),
    )
)
for c in cusps:
    fig.add_annotation(
        x=c,
        y=lg[js.index(c)] - 0.9,
        text="cusp",
        showarrow=False,
        font=dict(color="#f9f871", size=10),
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="THE SIDE VIEW — straight lines meeting at cusps<br><sup>"
        "Every sign PROVEN in ball arithmetic (radius search included), "
        "ball radius ~1e-105. Height = log10 depth of the minimum on the "
        "best loop; colour = its sign.<br>Inside a crimson block the "
        "curve is a straight line in j — an exponential. The straight "
        "pieces meet at cusps where the depth nearly touches zero, and "
        "the sign flips at some cusps but not all<br>(j = 88 touches and "
        "returns). Two competing exponentials do exactly this: the block "
        "edges are just the cusps where the dominant one changed sign."
        "</sup>",
        font=dict(color="#ede8dc", size=20),
        x=0.02,
        y=0.955,
    ),
    xaxis=dict(title="j — which knife", color="#a8a08e", gridcolor="#322e26", dtick=10),
    yaxis=dict(title="log10 |depth of the minimum|", color="#a8a08e", gridcolor="#322e26"),
    legend=dict(font=dict(color="#a8a08e", size=11), x=0.01, y=0.06, bgcolor="rgba(20,19,15,0.7)"),
    margin=dict(l=80, r=30, t=132, b=70),
    width=1520,
    height=680,
)

out = Path(__file__).resolve().parent / "side-view.png"
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
print(
    "saved", out, Image.open(out).size, "| cells:", len(js), "| blocks:", blocks, "| cusps:", cusps
)
