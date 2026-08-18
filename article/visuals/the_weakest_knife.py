"""THE WEAKEST KNIFE -- which constraint actually holds the boundary, and how thin.

All numbers exact (Fractions) via lab/jacobi_normal_form.py, whose sign was
verified against the independently computed value on 4500 cells with zero
mismatches. Knife j enters only through m = n - j, so one polynomial per level
carries every knife.

TWO FACTS, both measured rather than argued:

1. The weakest constraint is ALWAYS the LEADING trajectory, j = 2, i.e. the
   HIGHEST spin ell = 2n-4 of that level (m = n - 2), at every
   every level from n = 10 to n = 70 and every lam and D tested. NOTE: in this
   programme ell = 2n - 2j, so small j is HIGH spin. An earlier version of this
   file called j = 2 the lowest spin, which is backwards (docs/ERRATA.md,
   ERR-0004); it is also consistent with the known fact that low-spin dominance
   FAILS in this family.

2. Its size relative to the largest coefficient falls EXPONENTIALLY with the
   level: from 2.3e-2 at n = 10 to 2.2e-21 at n = 70 for lam = 1, D = 6. The rate
   is about 0.33 decades per unit of n and drifts slowly (upward for lam = 1,
   downward for lam = 7, both toward roughly 0.33 to 0.36) -- a straight line in n
   leaves residuals of 0.18 dex, a quadratic 0.05, so it is exponential with a
   slowly growing rate rather than a clean exponential.

WHY IT MATTERS. The theorem holds everywhere we have checked, but on the leading
trajectory it holds by an exponentially thin margin. Any proof therefore has to control an
exponentially small quantity: no crude bound can work, which is a concrete
explanation of why this has been hard rather than an excuse. And physically it
says this family of theories sits exponentially close to the LEADING-trajectory
positivity boundary as the level grows -- and that boundary is exactly the
published shore, which tonight's machinery reproduces independently.
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from jacobi_normal_form import jacobi_moment  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402

CACHE = Path("/tmp/weakest_knife_fig.json")
LEVELS = [10, 14, 20, 26, 34, 44, 56, 70]
PROFILE_LEVELS = [14, 26, 44, 70]


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    out = {"profiles": {}, "weakest": {}}
    for lam, D in ((F(1), F(6)), (F(7), F(6))):
        key = f"lam{lam}"
        out["weakest"][key] = []
        for n in LEVELS:
            vals = [float(F(-1) ** m * jacobi_moment(n - m, n, lam, D))
                    for m in range(n - 1)]
            top = max(abs(v) for v in vals)
            rel = [v / top for v in vals]
            out["weakest"][key].append([n, float(np.log10(min(rel)))])
            if lam == F(1) and n in PROFILE_LEVELS:
                out["profiles"][str(n)] = rel
            print("  lam=%s n=%d done" % (lam, n), flush=True)
    CACHE.write_text(json.dumps(out), encoding="utf-8")
    return out


d = gather()
fig = make_subplots(rows=1, cols=2, column_widths=[0.52, 0.48],
                    horizontal_spacing=0.11,
                    subplot_titles=("every knife of a level, relative size",
                                    "the weakest knife against the level"))

pal = ["#7df3ff", "#4df0ff", "#58d3be", "#c9e86b"]
for (n, rel), col in zip(sorted(d["profiles"].items(), key=lambda kv: int(kv[0])), pal):
    ms = list(range(len(rel)))
    fig.add_trace(go.Scatter(
        x=[m / (int(n) - 2) for m in ms],
        y=[np.log10(max(r, 1e-300)) for r in rel],
        mode="lines", name=f"n = {n}", line=dict(color=col, width=2)), row=1, col=1)
fig.add_annotation(x=1.0, y=-3, text="leading trajectory j=2 (highest spin)", showarrow=True,
                   arrowhead=2, ax=-70, ay=-30, font=dict(color="#ff8fb0", size=12),
                   arrowcolor="#ff8fb0", row=1, col=1)

for (key, pts), col, name in zip(sorted(d["weakest"].items()),
                                 ("#4df0ff", "#ff8fb0"),
                                 ("lam = 1", "lam = 7")):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers",
                             name=f"weakest coefficient, {name}",
                             line=dict(color=col, width=3),
                             marker=dict(size=9)), row=1, col=2)

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#14130f", plot_bgcolor="#14130f",
    title=dict(
        text="THE WEAKEST KNIFE — the boundary is held by the LEADING "
             "trajectory, exponentially tightly<br><sup>Exact rational arithmetic. Left: "
             "the relative size of every knife of a level, plotted against its "
             "position; the curve falls off a cliff at the leading trajectory j=2.<br>"
             "Right: that weakest coefficient against the level — a straight "
             "line on a log scale, from 2.3e-2 at n = 10 to 2.2e-21 at n = 70. "
             "The theorem holds, but on the leading trajectory it holds by an "
             "exponentially thin margin,<br>which is exactly why no crude bound can prove it."
             "</sup>",
        font=dict(color="#ede8dc", size=20), x=0.02, y=0.95),
    xaxis=dict(title="m / (n-2)   — 1 is the LEADING trajectory j=2, 0 is spin zero",
               color="#a8a08e", gridcolor="#322e26"),
    yaxis=dict(title="log10 of size relative to the largest knife",
               color="#a8a08e", gridcolor="#322e26"),
    xaxis2=dict(title="n — the level", color="#a8a08e", gridcolor="#322e26"),
    yaxis2=dict(title="log10 of the weakest coefficient", color="#a8a08e",
                gridcolor="#322e26"),
    legend=dict(font=dict(color="#a8a08e", size=10), x=0.01, y=-0.16,
                orientation="h", bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=80, r=30, t=140, b=100), width=1540, height=680)

out = Path(__file__).resolve().parent / "weakest-knife.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (20, 19, 15))
bbox = ImageChops.difference(im, bg).convert("L").point(
    lambda v: 255 if v > 10 else 0).getbbox()
pad = 12
im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
         min(im.width, bbox[2] + pad),
         min(im.height, bbox[3] + pad))).save(out)
print("saved", out, Image.open(out).size)
