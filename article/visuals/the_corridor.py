"""THE CORRIDOR -- why one fixed window of shore-levels works at every depth.

The height is T_k(lam): how high the ceiling on the spacetime dimension D sits
if you estimate it using level k. The true ceiling is the LOWEST point across
all levels -- the floor of the valley. Everything is exact rational arithmetic
from the closed form, evaluated in fmpq and converted to float only to draw.

The shape is the point. The surface is a valley, and its floor runs along a
straight ridge line. Our proof needs to pick, for every lam, an integer level
whose estimate is the true ceiling -- i.e. a level sitting on that floor. The
two glowing walls are the corridor [8/5 lam, 2 lam] that the proof actually
uses, chosen months earlier by measuring where the constraint stays positive,
with no knowledge of where the floor was. The floor runs down the middle of it.

That is the picture: the corridor was drawn blind, and the valley floor turned
out to be inside it, because the floor sits at sqrt(3)*lam = 1.732*lam and the
corridor is centred on 1.8*lam.
"""

import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from flint import fmpq

OUT = Path(__file__).resolve().parent / "the-corridor.png"


def T_k_exact(k: fmpq, lam: fmpq) -> fmpq:
    """T_k(lam) = 3(2k-3)/(k(k-2)) * (lam^2+(2k-2)lam+1) + 2k, exactly."""
    return fmpq(3) * (k * 2 - 3) / (k * (k - 2)) * (lam * lam + (k * 2 - 2) * lam + 1) + k * 2


# grid: lam along one axis, the RATIO v = k/lam along the other, so the valley
# floor becomes a straight line and the corridor becomes two straight walls.
lams = np.linspace(4.0, 60.0, 170)
vs = np.linspace(1.15, 2.75, 170)

# true ceiling per lam: the exact minimum over INTEGER levels
true_ceiling = {}
for lam in lams:
    lam_q = fmpq(int(round(lam * 64)), 64)
    best = None
    for k in range(3, int(4 * lam) + 4):
        t = T_k_exact(fmpq(k), lam_q)
        if best is None or t < best:
            best = t
    true_ceiling[float(lam)] = float(best)

Z = np.zeros((len(vs), len(lams)))
for i, v in enumerate(vs):
    for j, lam in enumerate(lams):
        lam_q = fmpq(int(round(lam * 64)), 64)
        k_q = fmpq(int(round(v * lam * 64)), 64)
        if k_q <= fmpq(5, 2):  # T_k blows up as k -> 2; outside the physical set
            Z[i, j] = np.nan
            continue
        t = T_k_exact(k_q, lam_q)
        # OVERSHOOT: how many times worse this level's estimate is than the truth.
        # The valley floor is then exactly 1.0 by construction, so the shape of
        # the valley IS the content -- which is what the CANYON standard asks for.
        Z[i, j] = float(t) / true_ceiling[float(lam)]

# exact integer minimiser per lam -> the yellow lane (the valley floor)
lane_lam, lane_v, lane_z = [], [], []
for lam in lams[::3]:
    lam_q = fmpq(int(round(lam * 64)), 64)
    best_k, best_T = None, None
    for k in range(3, int(4 * lam) + 4):
        t = T_k_exact(fmpq(k), lam_q)
        if best_T is None or t < best_T:
            best_T, best_k = t, k
    lane_lam.append(lam)
    lane_v.append(best_k / lam)
    lane_z.append(float(best_T) / true_ceiling[float(lam)] + 0.012)


# the two corridor edges, v = 8/5 and v = 2, traced ALONG THE SURFACE.
# Drawn as glass panels first: they read as an aquarium and hid the very thing
# the picture is about, that the yellow lane runs between them.
def surface_line(v_wall):
    zs = []
    for lam in lams:
        lam_q = fmpq(int(round(lam * 64)), 64)
        k_q = fmpq(int(round(v_wall * lam * 64)), 64)
        zs.append(float(T_k_exact(k_q, lam_q)) / true_ceiling[float(lam)] + 0.014)
    return zs


walls = [
    go.Scatter3d(
        x=lams,
        y=[v_wall] * len(lams),
        z=surface_line(v_wall),
        mode="lines",
        line=dict(color="#7ef9ff", width=6),
        hoverinfo="skip",
        showlegend=False,
    )
    for v_wall in (1.6, 2.0)
]
wall_top = float(np.nanmax(Z))

fig = go.Figure(
    [
        go.Surface(
            x=lams,
            y=vs,
            z=Z,
            colorscale=[
                [0.0, "#ffb347"],
                [0.10, "#e8743b"],
                [0.22, "#a8437a"],
                [0.42, "#4a52a8"],
                [0.62, "#1682a8"],
                [0.82, "#12617f"],
                [1.0, "#0a3450"],
            ],
            opacity=0.98,
            lighting=dict(ambient=0.72, diffuse=0.45, specular=0.06, roughness=0.95, fresnel=0.05),
            lightposition=dict(x=-120, y=60, z=400),
            contours=dict(
                z=dict(show=True, start=1.0, end=2.0, size=0.04, color="#020509", width=1),
            ),
            colorbar=dict(
                title=dict(text="times worse", font=dict(color="#a8b8cc", size=13)),
                tickfont=dict(color="#a8b8cc", size=11),
                thickness=16,
                len=0.60,
            ),
        ),
        *walls,
        go.Scatter3d(
            x=lane_lam,
            y=lane_v,
            z=lane_z,
            mode="lines",
            line=dict(color="#f9f871", width=9),
            hoverinfo="skip",
            showlegend=False,
        ),
    ]
)

fig.add_trace(
    go.Scatter3d(
        x=[lams[len(lams) // 2]],
        y=[1.42],
        z=[1.075],
        mode="text",
        text=["true ceiling lives here: sqrt(3)"],
        textfont=dict(color="#ffe94a", size=15),
        showlegend=False,
        hoverinfo="skip",
    )
)
fig.add_trace(
    go.Scatter3d(
        x=[lams[12]],
        y=[2.34],
        z=[1.056],
        mode="text",
        text=["the window we chose blind"],
        textfont=dict(color="#7ef9ff", size=17),
        showlegend=False,
        hoverinfo="skip",
    )
)

fig.update_layout(
    title=dict(
        text="CORRIDOR",
        x=0.035,
        y=0.982,
        font=dict(color="#eaf6ff", size=36, family="Arial Black"),
    ),
    annotations=[
        dict(
            text="valley floor = the true limit on spacetime dimension · yellow = where it lives · cyan = the window we picked blind, before we knew",
            x=0.035,
            y=0.918,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(color="#8fa6bd", size=13),
            xanchor="left",
        )
    ],
    scene=dict(
        xaxis=dict(
            title=dict(text="deformation", font=dict(color="#8fa6bd", size=13)),
            backgroundcolor="#05080d",
            gridcolor="#132234",
            color="#7d92a8",
        ),
        yaxis=dict(
            title=dict(text="which level you pick", font=dict(color="#8fa6bd", size=13)),
            backgroundcolor="#05080d",
            gridcolor="#132234",
            color="#7d92a8",
        ),
        zaxis=dict(
            title=dict(text="times worse", font=dict(color="#8fa6bd", size=13)),
            backgroundcolor="#05080d",
            gridcolor="#132234",
            color="#7d92a8",
        ),
        camera=dict(eye=dict(x=-1.50, y=-1.30, z=0.55), center=dict(x=0, y=0, z=-0.06)),
        aspectratio=dict(x=1.55, y=1.10, z=0.80),
    ),
    paper_bgcolor="#05080d",
    width=1500,
    height=860,
    margin=dict(l=0, r=0, t=58, b=10),
)

fig.write_image(str(OUT), scale=2)
print(f"written {OUT}")
print(f"overshoot range: {np.nanmin(Z):.4f} .. {np.nanmax(Z):.4f}  (floor should be 1.0)")
print(f"lane v range: {min(lane_v):.4f} .. {max(lane_v):.4f}  (corridor is 1.6 .. 2.0)")
