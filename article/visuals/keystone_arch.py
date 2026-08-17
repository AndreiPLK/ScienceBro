"""THE KEYSTONE ARCH — 3D visual of the keystone + collapse (real data).

Surface: safety ratio r(n, D) = P_{n+1} / (K0 * P_n) along the fixed-spin
diagonal l=6 (the WORST spin from the probe), lam=12 (worst lam). The floor
plane z=0 is the collapse line: the arch never touches it. Yellow lane =
worst ratio per level n; white diamond = global worst point (the ledge 0.29).
Style: cliff-3d standard (approved 2026-08-15).
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import plotly.graph_objects as go  # noqa: E402
from keystone_hunt import T_hat, eval_P  # noqa: E402
from knife_proof2 import Bj_coeffs, e_doubled_int  # noqa: E402
from PIL import Image  # noqa: E402


def fr(q):
    return Fraction(int(q.p), int(q.q))


def term0_ratio(n, l, D):
    j1, j2 = n - l // 2, n + 1 - l // 2
    E1, E2 = e_doubled_int(n)[j1 - 1], e_doubled_int(n + 1)[j2 - 1]
    c1, c2 = 4 * n - 4 * j1 - 1, 4 * (n + 1) - 4 * j2 - 1
    p1 = Fraction(1)
    for r in range(0, j1 - 1):
        p1 *= D + c1 + 2 * r
    p2 = Fraction(1)
    for r in range(0, j2 - 1):
        p2 *= D + c2 + 2 * r
    return Fraction(E2) * p2 / (Fraction(E1) * p1)


L, LAM = 6, Fraction(12)
Th = T_hat(LAM)
ns = list(range(6, 31))
fracs = [Fraction(i, 24) for i in range(25)]

Z, lane = [], []
worst = (None, None, None)
cache = {}
for n in ns:
    j1, j2 = n - L // 2, n + 1 - L // 2
    if n not in cache:
        cache[n] = Bj_coeffs(j1, n - 3)
    if n + 1 not in cache or (n + 1 - L // 2) != (n + 1) - L // 2:
        pass
    c1 = cache[n]
    c2 = Bj_coeffs(j2, n - 2)
    row = []
    best = None
    for f in fracs:
        D = Fraction(4) + (Th - 4) * f
        K0 = term0_ratio(n, L, D)
        r = float(fr(eval_P(c2, LAM, D)) / (K0 * fr(eval_P(c1, LAM, D))))
        row.append(r)
        if best is None or r < best[0]:
            best = (r, float(f))
        if worst[0] is None or r < worst[0]:
            worst = (r, n, float(f))
    Z.append(row)
    lane.append(best)

x = [float(f) for f in fracs]  # поперёк пояса: 0 = берег D=4, 1 = кромка T_hat
y = ns  # уровень n вдоль диагонали

COLORS = [
    [0.0, "#33091d"],
    [0.25, "#ff2a6d"],
    [0.5, "#7a3fd0"],
    [0.75, "#0aa3c2"],
    [1.0, "#3fe7f5"],
]

fig = go.Figure()
fig.add_trace(
    go.Surface(
        x=x,
        y=y,
        z=Z,
        colorscale=COLORS,
        showscale=False,
        cmin=0.1,
        cmax=1.7,
        lighting=dict(ambient=0.55, diffuse=0.7, specular=0.25, roughness=0.75),
    )
)
# пол z=0 — линия коллапса
fig.add_trace(
    go.Surface(
        x=x,
        y=[ns[0], ns[-1]],
        z=[[0, 0] * 1 for _ in range(2)],
        surfacecolor=[[0, 0], [0, 0]],
        colorscale=[[0, "#2a0a18"], [1, "#2a0a18"]],
        opacity=0.75,
        showscale=False,
    )
)
# жёлтая дорожка худшего запаса
fig.add_trace(
    go.Scatter3d(
        x=[b[1] for b in lane],
        y=ns,
        z=[b[0] + 0.02 for b in lane],
        mode="lines",
        line=dict(color="#f9f871", width=9),
        showlegend=False,
    )
)
# белый ромб в худшей точке
fig.add_trace(
    go.Scatter3d(
        x=[worst[2]],
        y=[worst[1]],
        z=[worst[0] + 0.03],
        mode="markers",
        marker=dict(size=9, color="white", symbol="diamond"),
        showlegend=False,
    )
)
ann = [
    dict(
        x=0.45,
        y=22,
        z=1.55,
        text="THE KEYSTONE ARCH",
        font=dict(color="#9ff5ff", size=26),
        showarrow=False,
    ),
    dict(
        x=worst[2],
        y=worst[1] + 7,
        z=worst[0] + 0.62,
        text="THE LEDGE: ratio 0.29 — lowest point, still above zero",
        font=dict(color="#ffe94a", size=15),
        showarrow=False,
    ),
    dict(
        x=0.35,
        y=7,
        z=0.07,
        text="ZERO FLOOR = COLLAPSE",
        font=dict(color="#ff5f95", size=16),
        showarrow=False,
    ),
]
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b0714",
    title=dict(
        text="THE KEYSTONE ARCH — one argument for ALL knives<br>"
        "<sup>height = safety ratio P(next level)/(kernel x P); "
        "floor 0 = collapse; yellow lane = thinnest margin; "
        "the arch NEVER touches the floor (worst spin l=6, "
        "lam=12, exact data)</sup>",
        font=dict(color="#e8e6f0", size=20),
        x=0.03,
    ),
    scene=dict(
        xaxis=dict(
            title="across the belt: shore D=4 -> edge T_hat", color="#8f8ba0", gridcolor="#241a38"
        ),
        yaxis=dict(
            title="level n (knife j = n-3 grows with n)", color="#8f8ba0", gridcolor="#241a38"
        ),
        zaxis=dict(title="safety ratio", color="#8f8ba0", gridcolor="#241a38", range=[0, 1.8]),
        annotations=ann,
        camera=dict(eye=dict(x=1.55, y=-1.3, z=0.62), center=dict(x=0, y=0, z=-0.12)),
    ),
    width=1600,
    height=1000,
    margin=dict(l=10, r=10, t=90, b=10),
)

out = Path(__file__).resolve().parent
fig.write_html(out / "keystone-arch.html", include_plotlyjs="cdn")
fig.write_image(str(out / "_ka_raw.png"), scale=2)
img = Image.open(out / "_ka_raw.png")
img.resize((1600, 1000), Image.LANCZOS).save(out / "keystone-arch.png")
(out / "_ka_raw.png").unlink()
print("saved keystone-arch.png; worst:", worst)
