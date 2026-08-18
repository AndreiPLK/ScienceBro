"""THE RIPPLE FROM ABOVE — 580 exact cells, the founder's requested top view.

Data: lab/contour_lib.py over a 20-family x 29-knife grid (580 cells), each cell
the minimum of the integrand on the best loop, normalised by the answer.

Read it as a map: cyan = a single loop already proves that constraint positive,
crimson = it does not. The question this view answers is what SHAPE the
boundaries have -- straight columns would mean the effect depends on the knife
index alone; curved fronts mean it depends on a combination, which is what the
founder guessed when he read the earlier plot as ripples from a drop.

Deliberately no fitted curves are drawn on top: the exponent that would justify
them is not established (my earlier collapse metric was invalid, since absolute
spread shrinks mechanically as the exponent grows). This is the raw map.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

RAW = Path("/tmp/ripple_map.json")
d = json.loads(RAW.read_text(encoding="utf-8"))
cells = {}
for k, v in d.items():
    j_s, lam_s = k.split("|")
    cells[(int(j_s), lam_s)] = v
js = sorted({j for j, _ in cells})
lams = sorted({lam for _, lam in cells}, key=lambda s: float(eval(s)))


def h(m):
    if m is None:
        return np.nan
    return float(np.sign(m) * np.log10(1 + abs(m) / 1e-12))


Z = [[h(cells.get((j, lam))) for j in js] for lam in lams]

fig = go.Figure(go.Heatmap(
    x=js, y=[float(eval(s)) for s in lams], z=Z, zmid=0,
    colorscale=[[0.0, "#7a1f45"], [0.42, "#ff2a6d"], [0.5, "#241a12"],
                [0.58, "#12648f"], [1.0, "#7df3ff"]],
    colorbar=dict(title=dict(text="signed depth<br>(log)",
                             font=dict(color="#a8a08e", size=11)),
                  tickfont=dict(color="#a8a08e", size=10), thickness=14,
                  len=0.8)))

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#14130f", plot_bgcolor="#14130f",
    title=dict(
        text="THE RIPPLE FROM ABOVE — 580 exact cells<br><sup>Cyan: one loop "
             "already proves that constraint positive. Crimson: it does not. "
             "The bands are not straight columns — the fronts bend as the "
             "family parameter grows,<br>which is what makes this one "
             "phenomenon rather than twenty. No fitted curves are drawn: the "
             "scaling exponent is measured but NOT yet established.</sup>",
        font=dict(color="#ede8dc", size=20), x=0.02, y=0.95),
    xaxis=dict(title="j — which knife", color="#a8a08e",
               gridcolor="#322e26"),
    yaxis=dict(title="lam — family of theories (log)", type="log",
               color="#a8a08e", gridcolor="#322e26"),
    margin=dict(l=80, r=20, t=118, b=70), width=1420, height=700)

out = Path(__file__).resolve().parent / "ripple-top.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (20, 19, 15))
bbox = ImageChops.difference(im, bg).convert("L").point(
    lambda v: 255 if v > 10 else 0).getbbox()
pad = 12
im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
         min(im.width, bbox[2] + pad),
         min(im.height, bbox[3] + pad))).save(out)
print("saved", out, Image.open(out).size, "| cells:", len(cells))
