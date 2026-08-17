"""THE FLYING BLADES — volume/isosurface of the REAL knife-3 windows.

V(lam, D, n) = P_3 bracket (master formula, exact integer coefficients)
normalized per level. The V=0 isosurface is the actual fleet of "blades" —
forbidden-window walls sailing above the shore (blade theorem, paper 4).
The faint outer shell is the shore T_hat. No artistic license: every
surface is computed from the published master formula.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from knife_proof2 import Bj_coeffs  # noqa: E402
from PIL import Image  # noqa: E402


def T_n(n, lam):
    return 3 * (2 * n - 3) / (n * (n - 2)) * (lam**2 + (2 * n - 2) * lam + 1) + 2 * n


lam = np.linspace(0.3, 9, 64)
Dax = np.linspace(4, 420, 68)
ns = np.arange(5, 41)
L2, D2 = np.meshgrid(lam, Dax, indexing="ij")

vals = np.zeros((len(lam), len(Dax), len(ns)))
shore = np.zeros_like(vals)
for k, n in enumerate(ns):
    cf = Bj_coeffs(3, int(n) - 3)
    P = np.zeros_like(L2)
    for (p, q), c in cf.items():
        P += float(c) * L2**p * D2**q
    P /= np.abs(P).max()
    vals[:, :, k] = np.sign(P) * np.abs(P) ** 0.22  # растянуть контраст
    shore[:, :, k] = (T_n(n, L2) - D2) / T_n(n, L2)

X, Y, Z = np.meshgrid(lam, Dax, ns, indexing="ij")
fig = go.Figure()
fig.add_trace(
    go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=vals.flatten(),
        isomin=-0.001,
        isomax=0.001,
        surface_count=1,
        colorscale=[[0, "#ff2a6d"], [1, "#ff2a6d"]],
        opacity=0.72,
        caps=dict(x_show=False, y_show=False, z_show=False),
        showscale=False,
    )
)
fig.add_trace(
    go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=shore.flatten(),
        isomin=-0.001,
        isomax=0.001,
        surface_count=1,
        colorscale=[[0, "#0aa3c2"], [1, "#0aa3c2"]],
        opacity=0.10,
        caps=dict(x_show=False, y_show=False, z_show=False),
        showscale=False,
    )
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05030c",
    title=dict(
        text="THE FORBIDDEN WALL<br>"
        "<sup>pink = where knife 3 kills a theory (exact master "
        "formula); its serrated lower edge = the blade tips;<br>"
        "dark veil = the shore of allowed worlds. Our theorem: "
        "the teeth NEVER bite below the veil</sup>",
        font=dict(color="#e8e6f0", size=21),
        x=0.03,
    ),
    scene=dict(
        xaxis=dict(title="which theory (lambda)", color="#5c5870", gridcolor="#150e24"),
        yaxis=dict(title="dimensions D", color="#5c5870", gridcolor="#150e24"),
        zaxis=dict(title="level n", color="#5c5870", gridcolor="#150e24"),
        camera=dict(eye=dict(x=1.2, y=-1.35, z=0.45)),
    ),
    width=1600,
    height=1000,
    margin=dict(l=10, r=10, t=100, b=10),
)

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_b_raw.png"), scale=2)
Image.open(out / "_b_raw.png").resize((1600, 1000), Image.LANCZOS).save(out / "flying-blades.png")
(out / "_b_raw.png").unlink()
print("saved flying-blades.png")
