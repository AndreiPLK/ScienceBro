"""THE HUNT — the day's reasoning as a map (real data, cliff-3d palette).

Each ring = one hypothesis we tested; height = how deep it took us before
it died (measured by how much structure it revealed); colour = verdict.
Two survive at the top: the closed form and the square identity.
"""

from pathlib import Path
import plotly.graph_objects as go
from PIL import Image

# РЕАЛЬНЫЕ данные: гипотезы ночи и дня, в порядке проверки
H = [
    ("moments of c_t", 1, "dead"), ("Leibniz bound", 1, "dead"),
    ("Abel induction", 2, "dead"), ("monotone S", 1, "dead"),
    ("normalised X<1", 1, "dead"), ("factor P", 1, "dead"),
    ("PSD quadratic form", 3, "dead"), ("moments of A_t", 3, "dead"),
    ("orthogonal expansion", 3, "dead"), ("Lorentzian signature", 3, "dead"),
    ("three-term recursion", 2, "dead"), ("Phi >= 0 global", 2, "dead"),
    ("Phi >= 0 on support", 4, "dead"), ("Psi binomial >= 0", 4, "dead"),
    ("CLOSED FORM", 6, "alive"), ("SQUARE IDENTITY", 6, "alive"),
    ("weighted inequality", 5, "open"),
]

COL = {"dead": "#ff2a6d", "alive": "#3fe7f5", "open": "#f9f871"}
xs = list(range(len(H)))
fig = go.Figure()
for i, (name, depth, verdict) in enumerate(H):
    fig.add_trace(go.Scatter3d(
        x=[i, i], y=[0, 0], z=[0, depth], mode="lines",
        line=dict(color=COL[verdict], width=9), showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[i], y=[0], z=[depth], mode="markers",
        marker=dict(size=13 if verdict != "dead" else 7, color=COL[verdict],
                    symbol="diamond" if verdict == "alive" else "circle"),
        showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[i], y=[0], z=[depth + 0.45 + 0.5*(i % 3)], mode="text", text=[name],
        textfont=dict(color=COL[verdict],
                      size=13 if verdict != "dead" else 10),
        showlegend=False))

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0b0714",
    title=dict(text="THE HUNT — 17 ideas tested in one day<br><sup>pink = "
                    "falsified (each one narrowed the search), cyan = PROVED "
                    "and kept, yellow = the single open target left. Height = "
                    "how much structure the idea revealed before it died."
                    "</sup>",
               font=dict(color="#e8e6f0", size=20), x=0.03),
    scene=dict(
        xaxis=dict(title="", showticklabels=False, color="#8f8ba0",
                   gridcolor="#241a38"),
        yaxis=dict(title="", showticklabels=False, visible=False),
        zaxis=dict(title="depth reached", color="#8f8ba0",
                   gridcolor="#241a38", showticklabels=False, range=[0, 9]),
        camera=dict(eye=dict(x=0.15, y=-2.25, z=0.45),
                    center=dict(x=0, y=0, z=-0.15)),
        aspectmode="manual", aspectratio=dict(x=2.6, y=0.35, z=0.85)),
    width=1700, height=950, margin=dict(l=10, r=10, t=95, b=10))

out = Path(__file__).resolve().parent
fig.write_image(str(out / "_h_raw.png"), scale=2)
Image.open(out / "_h_raw.png").resize((1700, 950), Image.LANCZOS).save(
    out / "the-hunt.png")
(out / "_h_raw.png").unlink()
print("saved the-hunt.png")
