"""THE HEART OF THE LAW — volume/isosurface style (medical-imaging look).

REAL DATA: F(lam, D, n) = (T_n(lam) - D) / T_n(lam) — the shore law from
paper 2 (T_n(lam) = 3(2n-3)/(n(n-2))*(lam^2+(2n-2)lam+1)+2n). The outer
translucent shell is the SHORE itself (F=0): the boundary between possible
and impossible. The glowing core (F=0.55) is the deep-safe heart where
gravity theories live with a wide margin.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image  # noqa: E402


def T_n(n, lam):
    return (3 * (2 * n - 3) / (n * (n - 2))
            * (lam ** 2 + (2 * n - 2) * lam + 1) + 2 * n)


lam = np.linspace(0.2, 12, 44)
D = np.linspace(4, 260, 48)
n = np.linspace(3, 40, 44)
L, Dv, N = np.meshgrid(lam, D, n, indexing="ij")
T = T_n(N, L)
F = (T - Dv) / T

fig = go.Figure(go.Isosurface(
    x=L.flatten(), y=Dv.flatten(), z=N.flatten(), value=F.flatten(),
    isomin=0.0, isomax=0.55, surface_count=2,
    colorscale=[[0.0, "#ff2a6d"], [0.5, "#7a3fd0"], [1.0, "#3fe7f5"]],
    opacity=0.35, caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False))
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#05030c",
    title=dict(text="THE HEART OF THE LAW<br>"
                    "<sup>the pink translucent shell = the SHORE (proven "
                    "boundary of possible gravity);<br>the cyan core = the "
                    "safe heart where theories live with a wide margin — "
                    "real formula, no artistic license</sup>",
               font=dict(color="#e8e6f0", size=21), x=0.03),
    scene=dict(
        xaxis=dict(title="which theory (lambda)", color="#5c5870",
                   gridcolor="#150e24"),
        yaxis=dict(title="dimensions D", color="#5c5870",
                   gridcolor="#150e24"),
        zaxis=dict(title="level n (particle ladder)", color="#5c5870",
                   gridcolor="#150e24"),
        camera=dict(eye=dict(x=1.45, y=-1.5, z=0.65)),
    ),
    width=1600, height=1000, margin=dict(l=10, r=10, t=100, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_h_raw.png"), scale=2)
Image.open(out / "_h_raw.png").resize((1600, 1000), Image.LANCZOS).save(
    out / "heart-of-law.png")
(out / "_h_raw.png").unlink()
print("saved heart-of-law.png")
