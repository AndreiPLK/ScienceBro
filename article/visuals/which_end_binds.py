"""WHICH END BINDS -- the weakest constraint switches between the two ends.

Exact rational arithmetic through lab/jacobi_normal_form.jacobi_coeff_fast,
which is the Saalschutz closed form and was checked against the slower verified
path on 891 exact comparisons with zero mismatches.

WHAT IS DRAWN. For each theory (lam) and dimension (D) below the shore, and at a
fixed level n, we compute EVERY knife of that level and ask which one sits
closest to violating positivity -- i.e. which Jacobi coefficient is smallest
relative to the largest of that level. Two answers compete:

  * the LEADING trajectory j = 2, the HIGHEST spin of the level (ell = 2n-4);
  * the far end m = 0, i.e. j = n, the LOWEST spin.

They are not the same region. The binding constraint switches along a boundary
running diagonally in (lam, D): the leading trajectory binds at small D, the
lowest spin binds at large D, and the switch happens later in D as lam grows.

WHY IT MATTERS. This programme already recorded that "low-spin dominance FAILS"
in this family (research/inventory-of-facts.md, C4). That statement is true in
the large region where the leading trajectory binds -- and it is FALSE in the
region mapped here, where the lowest spin is exactly the binding one. The
refinement is the point of this figure.

Note on labels: ell = 2n - 2j in this programme, so SMALL j is HIGH spin. An
earlier figure of mine had this backwards (docs/ERRATA.md, ERR-0004).
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from jacobi_normal_form import jacobi_coeff_fast  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402
from plotly.subplots import make_subplots  # noqa: E402

CACHE = Path("/tmp/which_end_binds.json")
LAMS = [F(1, 4), F(1, 2), F(1), F(2), F(3), F(5), F(7), F(10), F(14), F(20),
        F(26), F(40), F(60), F(100)]
DS = [F(3), F(4), F(5), F(6), F(8), F(11), F(16), F(23), F(32), F(40), F(60),
      F(90), F(120), F(180)]
LEVELS = [12, 24, 40]


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    out = {}
    for n in LEVELS:
        grid = []
        for lam in LAMS:
            sh = T_hat(float(lam))
            row = []
            for D in DS:
                if float(D) >= sh:
                    row.append(None)
                    continue
                vals = [float(F(-1) ** m * jacobi_coeff_fast(n - m, n, lam, D))
                        for m in range(n - 1)]
                top = max(vals)
                rel = [v / top for v in vals]
                i = rel.index(min(rel))
                row.append(2 if i == len(rel) - 1 else (0 if i == 0 else 1))
            grid.append(row)
            print("  n=%d lam=%s done" % (n, lam), flush=True)
        out[str(n)] = grid
    CACHE.write_text(json.dumps(out), encoding="utf-8")
    return out


d = gather()
fig = make_subplots(rows=1, cols=len(LEVELS),
                    subplot_titles=[f"level n = {n}" for n in LEVELS],
                    horizontal_spacing=0.045)

for col, n in enumerate(LEVELS, start=1):
    Z = [[np.nan if v is None else v for v in row] for row in d[str(n)]]
    fig.add_trace(go.Heatmap(
        x=[float(x) for x in DS], y=[float(x) for x in LAMS], z=Z,
        zmin=0, zmax=2, showscale=(col == len(LEVELS)),
        colorscale=[[0.0, "#ff2a6d"], [0.33, "#ff2a6d"],
                    [0.34, "#f9f871"], [0.66, "#f9f871"],
                    [0.67, "#4df0ff"], [1.0, "#4df0ff"]],
        colorbar=dict(tickvals=[0.33, 1.0, 1.67],
                      ticktext=["lowest spin binds", "an interior spin",
                                "leading trajectory binds"],
                      tickfont=dict(color="#a8a08e", size=10), thickness=13,
                      len=0.75)), row=1, col=col)

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#14130f", plot_bgcolor="#14130f",
    title=dict(
        text="WHICH END BINDS — the weakest constraint switches between the two "
             "ends of the spin spectrum<br><sup>Exact rational arithmetic, every "
             "knife of every level. Cyan: the LEADING trajectory j=2 (highest "
             "spin) is closest to violating positivity. Crimson: the LOWEST spin "
             "is.<br>Blank: above the shore, outside the claim. The boundary "
             "moves with the level, and it refines the recorded fact that "
             "low-spin dominance fails here — it fails in the cyan region and "
             "holds in the crimson one.</sup>",
        font=dict(color="#ede8dc", size=19), x=0.02, y=0.95),
    margin=dict(l=70, r=30, t=132, b=70), width=1620, height=620)
for i in range(1, len(LEVELS) + 1):
    fig.update_xaxes(title="D", type="log", color="#a8a08e",
                     gridcolor="#322e26", row=1, col=i)
    fig.update_yaxes(title="lam" if i == 1 else None, type="log",
                     color="#a8a08e", gridcolor="#322e26", row=1, col=i)

out = Path(__file__).resolve().parent / "which-end-binds.png"
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
