"""THE MARGIN LAW — the fleet closes in but never lands (wave-relief style).

Real exact data. For each even knife j and each deformation lam we compute
the exact D-threshold (where the knife starts cutting) by rational bisection
on the univariate polynomial J(Q), and plot

        height = D_threshold(j, lam) - shore(lam)

as a relief over (lam, j). The measured law is that this height SATURATES:

        D_threshold - shore  ->  C (j - 2),   C = 2.398 +- 0.002 ,

so the surface flattens into a staircase of terraces in j, independent of
lam. Meanwhile the shore itself runs away linearly, shore ~ 18.93 lam, so in
RELATIVE terms the fleet gets ever closer to shore -- which is why large lam
is the hard region -- while in absolute terms it never lands.

Points are computed once and cached next to this script.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from keystone_hunt import T_hat, T_k  # noqa: E402
from keystone_lowspin import threshold_D  # noqa: E402
from PIL import Image  # noqa: E402

JS = [4, 6, 8, 10, 12]
LAMS = [20, 40, 60, 90, 130, 175, 250]
CACHE = Path(__file__).resolve().parent / "margin_law_data.json"


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    data = {}
    for j in JS:
        for lam_i in LAMS:
            lam = Fraction(lam_i)
            shore = T_hat(lam)
            k = min(range(3, 3 * lam_i + 61), key=lambda kk: T_k(kk, lam))
            best = None
            for n in range(max(4, k - 6), k + 6):
                thr = threshold_D(j, n, lam)
                if thr is None:
                    continue
                if best is None or thr < best:
                    best = thr
            if best is not None:
                data[f"{j}_{lam_i}"] = float(best - shore)
                print(f"  j={j} lam={lam_i}: gap={float(best - shore):.4f}", flush=True)
    CACHE.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return data


data = gather()
Z = [[data.get(f"{j}_{lam}", np.nan) for lam in LAMS] for j in JS]

fig = go.Figure()
fig.add_trace(
    go.Surface(
        x=LAMS,
        y=JS,
        z=Z,
        showscale=False,
        colorscale=[[0.0, "#241033"], [0.35, "#155f8a"], [0.7, "#3fe7f5"], [1.0, "#f9f871"]],
        lighting=dict(ambient=0.6, diffuse=0.7, specular=0.2, roughness=0.7),
        contours=dict(z=dict(show=True, start=0, end=26, size=2.4, color="#0b0714", width=1)),
    )
)

# the predicted terraces: 2.398 (j - 2), flat in lam
for j in JS:
    fig.add_trace(
        go.Scatter3d(
            x=LAMS,
            y=[j] * len(LAMS),
            z=[2.398 * (j - 2)] * len(LAMS),
            mode="lines",
            line=dict(color="#ff2a6d", width=5),
            showlegend=False,
        )
    )

ann = [
    dict(
        x=LAMS[-1],
        y=12,
        z=2.398 * 10 + 3.4,
        text="red lines = 2.398 (j - 2)<br>the measured law",
        font=dict(color="#ff8fb0", size=14),
        showarrow=False,
    ),
    dict(
        x=LAMS[2],
        y=4,
        z=7.5,
        text="knife j = 4 stays closest to the shore",
        font=dict(color="#9ff5ff", size=13),
        showarrow=False,
    ),
]

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b0714",
    title=dict(
        text="THE FLEET CLOSES IN BUT NEVER LANDS<br><sup>Exact data. Height "
        "= how many dimensions of clearance the knife leaves above the "
        "shore.<br>The terraces are flat in lam: the absolute clearance "
        "SATURATES at about 2.4 per two knives, while the shore itself "
        "runs away as 18.93 lam.<br>So the closer you look, the thinner "
        "the relative margin — and it never reaches zero.</sup>",
        font=dict(color="#e8e6f0", size=20),
        x=0.025,
        y=0.955,
    ),
    scene=dict(
        xaxis=dict(
            title="lam — deformation of the amplitude",
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        yaxis=dict(
            title="j — which knife",
            dtick=2,
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        zaxis=dict(
            title="clearance above the shore (dimensions)",
            backgroundcolor="#0b0714",
            gridcolor="#2a2140",
            color="#b9b4cc",
        ),
        aspectratio=dict(x=1.6, y=1.25, z=0.6),
        annotations=ann,
        camera=dict(eye=dict(x=1.55, y=-1.35, z=0.62), center=dict(x=0, y=0, z=-0.12)),
    ),
    margin=dict(l=0, r=0, t=104, b=0),
    width=1480,
    height=600,
)

out = Path(__file__).resolve().parent / "margin-law.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
from PIL import ImageChops  # noqa: E402

bg = Image.new("RGB", im.size, (11, 7, 20))
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
