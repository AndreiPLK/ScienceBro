"""THE CRITICAL ZONE — where the grand theorem is hard (real margin map).

REAL DATA: results/keystone_margin_map.json — margin(j, lam) = 1 - |dip| /
plateau for the reduced inequality. Cyan highlands = the theorem holds with
room to spare. The pink canyon = the critical zone where the margin collapses
to 0.0002. The canyon drifts to larger lam as the knife index grows.
"""

import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

RES = Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "results"
d = json.loads((RES / "keystone_margin_map.json").read_text(encoding="utf-8"))
lams, js, M = d["lams"], d["js"], np.array(d["margins"], dtype=float)

Z = np.log10(np.clip(M, 1e-4, 1.0))          # логарифм: видно и 1, и 2e-4

fig = go.Figure()
fig.add_trace(go.Surface(
    x=np.log10(lams), y=js, z=Z, showscale=False,
    colorscale=[[0.0, "#ff2a6d"], [0.35, "#7a3fd0"], [0.7, "#0aa3c2"],
                [1.0, "#3fe7f5"]],
    lighting=dict(ambient=0.55, diffuse=0.75, specular=0.25)))

# дно канона: минимум по каждому j
xs, ys, zs = [], [], []
for i, j in enumerate(js):
    k = int(np.nanargmin(M[i]))
    xs.append(np.log10(lams[k])); ys.append(j); zs.append(Z[i, k] + 0.06)
fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines+markers",
                           line=dict(color="#f9f871", width=8),
                           marker=dict(size=5, color="#f9f871"),
                           showlegend=False))

ann = [
    dict(x=np.log10(300), y=js[-2], z=0.15,
         text="EASY: margin ~ 1 (theorem holds with room)",
         font=dict(color="#3fe7f5", size=14), showarrow=False),
    dict(x=np.log10(9), y=js[len(js)//2], z=-4.35,
         text="THE CRITICAL CANYON — margin 0.0002<br>"
              "this is where the grand theorem is decided",
         font=dict(color="#ffe94a", size=14), showarrow=False),
    dict(x=np.log10(1.1), y=js[0], z=-0.55,
         text="small lambda: comfortable",
         font=dict(color="#9ff5ff", size=13), showarrow=False),
]
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0714",
    title=dict(text="THE CRITICAL CANYON — where the last theorem lives<br>"
                    "<sup>height = safety margin of the reduced inequality "
                    "(log scale, real computed data). Highlands: the theorem "
                    "is easy. The yellow line traces the canyon floor — it "
                    "drifts to larger lambda as the knife index grows.</sup>",
               font=dict(color="#e8e6f0", size=20), x=0.03),
    scene=dict(
        xaxis=dict(title="log10(lambda)", color="#8f8ba0",
                   gridcolor="#241a38"),
        yaxis=dict(title="knife j", color="#8f8ba0", gridcolor="#241a38",
                   dtick=2),
        zaxis=dict(title="log10(margin)", color="#8f8ba0",
                   gridcolor="#241a38"),
        annotations=ann,
        camera=dict(eye=dict(x=1.6, y=-1.5, z=0.75),
                    center=dict(x=0, y=0, z=-0.1))),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_cc_raw.png"), scale=2)
Image.open(out / "_cc_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "critical-canyon.png")
(out / "_cc_raw.png").unlink()
print("saved critical-canyon.png")
