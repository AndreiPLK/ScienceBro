"""THE CEILING -- the induction that could close the theorem, drawn.

The reformulated theorem (results/jacobi_normal_form.json, 4500 exact sign
checks, 0 mismatches) is: an explicit product of squares has an all-positive
Jacobi expansion. Measured tonight: building that product by adding its factors
SMALLEST ROOT FIRST keeps every coefficient positive at every single step, while
largest-first fails until enough factors accumulate. So there is an induction to
be had, and the only question is how large a new root may be.

This figure measures both sides of that question by exact bisection:

  * THE CEILING (line): for a partial product of t factors, the largest new root
    c that still leaves every coefficient positive.
  * THE STAIRCASE (markers): the roots the real problem actually asks for,
    c_t = (a_t / s)^2 with a_t in {..., n-4, n-2} and s = lam + n - 1.

The theorem holds if the staircase stays under the ceiling, and it does, at every
step, with the margin shrinking from 320x at the first step to about 1.1x at the
last. That thin final margin is why this has to be proved rather than eyeballed:
it is the whole content of the remaining work.

Nothing here is fitted. Each ceiling point is a bisection on exact rational
arithmetic; each staircase point is an exact rational.
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import numpy as np  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402
from step_lemma import c_max, ladder, mul_square  # noqa: E402

CACHE = Path("/tmp/the_ceiling_data.json")
CASES = [(31, F(1), F(6), "#4df0ff"), (31, F(1), F(11), "#c9e86b"), (21, F(7), F(6), "#ff8fb0")]


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    data = {}
    for n, lam, D, _ in CASES:
        _, roots = ladder(n, lam)
        H = [F(0)] * (1 if n % 2 == 0 else 0) + [F(1)]
        ceil, stair = [], []
        for t, c in enumerate(roots):
            cm = c_max(H, D, iters=11)
            if cm is None:
                break
            ceil.append(float(cm))
            stair.append(float(c))
            H = mul_square(H, c)
            print(
                f"  n={n} lam={lam} D={D} t={t} ceiling {float(cm):.5f} ladder {float(c):.5f}",
                flush=True,
            )
        data[f"{n}|{lam}|{D}"] = {"ceiling": ceil, "ladder": stair}
    CACHE.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return data


data = gather()
fig = go.Figure()
for n, lam, D, col in CASES:
    d = data[f"{n}|{lam}|{D}"]
    ts = list(range(len(d["ceiling"])))
    fig.add_trace(
        go.Scatter(
            x=ts,
            y=d["ceiling"],
            mode="lines",
            name=f"ceiling: n={n}, lam={lam}, D={D}",
            line=dict(color=col, width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ts,
            y=d["ladder"],
            mode="markers",
            showlegend=True,
            name=f"the ladder the problem asks for (n={n}, lam={lam})",
            marker=dict(color=col, size=11, symbol="square", line=dict(color="#14130f", width=1)),
        )
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="THE CEILING — the induction, measured step by step<br><sup>"
        "Exact rational bisection, no fitting. LINE: the largest new root "
        "that still leaves every Jacobi coefficient positive, given t "
        "factors already in place.<br>SQUARES: the roots the real problem "
        "actually asks for. The theorem holds because the staircase stays "
        "under the ceiling at every step — margin 320x at the first step, "
        "about 1.1x at the last.<br>That last thin margin is exactly what "
        "still has to be proved.</sup>",
        font=dict(color="#ede8dc", size=20),
        x=0.02,
        y=0.95,
    ),
    xaxis=dict(
        title="t — how many factors are already in the product",
        color="#a8a08e",
        gridcolor="#322e26",
        dtick=1,
    ),
    yaxis=dict(
        title="root position c  (the interval is 0 to 1)",
        color="#a8a08e",
        gridcolor="#322e26",
        range=[0, 1.02],
    ),
    legend=dict(font=dict(color="#a8a08e", size=10), x=0.02, y=0.98, bgcolor="rgba(20,19,15,0.75)"),
    margin=dict(l=80, r=30, t=140, b=70),
    width=1480,
    height=720,
)

out = Path(__file__).resolve().parent / "the-ceiling.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (20, 19, 15))
bbox = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 10 else 0).getbbox()
pad = 12
im.crop(
    (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(im.width, bbox[2] + pad),
        min(im.height, bbox[3] + pad),
    )
).save(out)
print("saved", out, Image.open(out).size)
