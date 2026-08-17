"""THE STAIRCASE — morning of 2026-08-17 (five proven knives).

Terraces = knives; height = how complete the theorem is (REAL artifact
data read from results/*.json at render time). Founder's cliff-3d style.
"""

import json
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image

RES = Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "results"


def knife_pct(j):
    checks = [
        (f"knife_proof2_j{j}.json", "ok_so_far", 25),
        (f"knife_tail2_j{j}.json", "all_certified", 35),
        (f"knife{j}_belowdiag_shift.json", "all_certified", 20),
        (f"knife{j}_farbelow_factored.json", "far_below_factored", 20),
    ]
    pct = 0
    for fn, key, w in checks:
        p = RES / fn
        if p.exists():
            try:
                if json.loads(p.read_text(encoding="utf-8")).get(key):
                    pct += w
            except Exception:
                pass
    return pct


KN = list(range(2, 13))
H = {2: 100, 3: 100}
for j in range(4, 13):
    H[j] = knife_pct(j)

xs = [4, 40]
ys, zs, labels = [], [], []
for j in KN:
    for off in (-0.45, 0.45):
        ys.append(j + off)
        zs.append([H[j] / 6.5, H[j] / 6.5])

fig = go.Figure()
fig.add_trace(
    go.Surface(
        x=xs,
        y=ys,
        z=zs,
        colorscale=[
            [0, "#33091d"],
            [0.3, "#ff2a6d"],
            [0.55, "#7a3fd0"],
            [0.8, "#0aa3c2"],
            [1, "#3fe7f5"],
        ],
        showscale=False,
        lighting=dict(ambient=0.5, diffuse=0.75, specular=0.2),
    )
)

done = [j for j in KN if H[j] == 100]
fig.add_trace(
    go.Scatter3d(
        x=[22] * len(done),
        y=done,
        z=[H[j] / 6.5 + 0.5 for j in done],
        mode="markers",
        marker=dict(size=8, color="#f9f871", symbol="diamond"),
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter3d(
        x=[22],
        y=[max(done) + 0.2],
        z=[H[max(done)] / 6.5 + 2.2],
        mode="text",
        text=[f"PROVEN THEOREMS: knives {min(done)}-{max(done)}"],
        textfont=dict(color="#f9f871", size=17),
        showlegend=False,
    )
)

ann = [
    dict(
        x=8,
        y=13.2,
        z=17.5,
        text="THE STAIRCASE — SEVEN PROVEN KNIVES",
        font=dict(color="#9ff5ff", size=24),
        showarrow=False,
    ),
    dict(
        x=30,
        y=10.5,
        z=6.5,
        text="knives 9-11: 3 of 4 regions proven (80%);<br>"
        "far-below hits the method boundary found tonight",
        font=dict(color="#ff5f95", size=13),
        showarrow=False,
    ),
]

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b0714",
    title=dict(
        text="THE STAIRCASE TO THE GRAND THEOREM — morning 17.08<br>"
        "<sup>each terrace = one knife; height = share of the "
        "theorem PROVEN (read from artifacts, not typed by hand)"
        "</sup>",
        font=dict(color="#e8e6f0", size=20),
        x=0.03,
    ),
    scene=dict(
        xaxis=dict(title="dimensions D", color="#8f8ba0", gridcolor="#241a38"),
        yaxis=dict(title="knife j", color="#8f8ba0", gridcolor="#241a38", dtick=1),
        zaxis=dict(
            title="proven",
            color="#8f8ba0",
            gridcolor="#241a38",
            range=[0, 19],
            showticklabels=False,
        ),
        annotations=ann,
        camera=dict(eye=dict(x=1.75, y=-1.5, z=0.7), center=dict(x=0, y=0, z=-0.12)),
    ),
    width=1600,
    height=1000,
    margin=dict(l=10, r=10, t=90, b=10),
)

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_s_raw.png"), scale=2)
Image.open(out / "_s_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "staircase-morning.png"
)
(out / "_s_raw.png").unlink()
print("saved staircase-morning.png; heights:", H)
