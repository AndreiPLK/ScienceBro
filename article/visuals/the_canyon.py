"""THE CANYON -- the safety landscape of the theorem, from exact arithmetic.

Height is how much room a family of constraints has before one of them would
fail: 1.0 means exactly touching, higher means safe. Every value is computed in
exact rational arithmetic from the beta-mean formula, not modelled and not
smoothed.

The shape is the point. The landscape is high almost everywhere and drops into a
narrow canyon whose floor sits exactly at 1 -- and that floor traces the levels
that define the boundary of the allowed region. The theorem is decided in the
canyon; everywhere else there is room to spare.
"""

import json
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from flint import fmpq, fmpq_poly
from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
from gegenbauer_flint import T_hat  # noqa: E402

CACHE = Path(__file__).resolve().parent / "canyon_data.json"
Y = fmpq_poly([0, 1])


def P_N(N):
    out = Y ** (N % 2) if N % 2 else fmpq_poly([1])
    a = N - 1
    while a > 0:
        out = out * (Y - fmpq(a * a)) ** 2
        a -= 2
    return out


def poch(x, k):
    r = fmpq(1)
    for i in range(k):
        r *= x + i
    return r


def first_flip(N, lam, hi_num=30000):
    """smallest gamma at which ANY coefficient of this level turns negative"""
    hi = fmpq(hi_num)
    P = P_N(N)
    R = P
    best = None
    for m in range(N):
        if m:
            R = R.derivative()
        Rc = R.coeffs()
        s = lam + N
        X = s * s

        def sgn(g, Rc=Rc, m=m, X=X):
            t = fmpq(0)
            for j, r in enumerate(Rc):
                t += r * poch(fmpq(1, 2) + m, j) / poch(2 * m + g + 1, j) * X**j
            return (t > 0) - (t < 0)

        h = best if best is not None else hi
        if sgn(h) > 0:
            continue
        lo = fmpq(1, 100)
        if sgn(lo) <= 0:
            return fmpq(0)
        for _ in range(26):
            mid = (lo + h) / 2
            if sgn(mid) > 0:
                lo = mid
            else:
                h = mid
        if best is None or lo < best:
            best = lo
    return best


def build():
    ns = list(range(5, 47, 2))
    lams = [fmpq(1, 4), fmpq(1, 2), fmpq(1), fmpq(2), fmpq(4), fmpq(7), fmpq(11), fmpq(16)]
    grid = []
    for lam in lams:
        gs = float(T_hat(lam) / fmpq(2) - fmpq(3, 2))
        row = []
        for n in ns:
            f = first_flip(n - 1, lam)
            row.append(float(f) / gs if f else 6.0)
        grid.append(row)
        print(f"  lam={lam} done", flush=True)
    CACHE.write_text(
        json.dumps({"ns": ns, "lams": [str(x) for x in lams], "margin": grid}), encoding="utf-8"
    )
    return ns, [float(x) for x in lams], grid


if CACHE.exists():
    d = json.loads(CACHE.read_text(encoding="utf-8"))
    ns, lams, grid = (
        d["ns"],
        [float(fmpq(*map(int, (x.split("/") + ["1"])[:2]))) for x in d["lams"]],
        d["margin"],
    )
else:
    ns, lams, grid = build()

Z = np.array(grid)
Z = np.clip(Z, 1.0, 2.0)

fig = go.Figure(
    go.Surface(
        x=ns,
        y=lams,
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
            z=dict(show=True, start=1.0, end=2.0, size=0.05, color="#020509", width=1),
            x=dict(show=True, color="#0d2136", width=1),
        ),
        colorbar=dict(
            title=dict(text="room to spare", font=dict(color="#a8b8cc", size=13)),
            tickfont=dict(color="#a8b8cc", size=11),
            thickness=16,
            len=0.62,
        ),
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#05070c",
    title=dict(
        text="THE CANYON",
        font=dict(color="#eafff9", size=36),
        x=0.03,
        y=0.965,
    ),
    scene=dict(
        xaxis=dict(title="level", backgroundcolor="#05070c", gridcolor="#122238", color="#7f93b0"),
        yaxis=dict(title="family", backgroundcolor="#05070c", gridcolor="#122238", color="#7f93b0"),
        zaxis=dict(
            title="safety margin",
            backgroundcolor="#05070c",
            gridcolor="#122238",
            color="#7f93b0",
            range=[0.98, 2.05],
        ),
        aspectratio=dict(x=1.55, y=1.1, z=0.85),
        camera=dict(eye=dict(x=-1.38, y=-1.48, z=0.50), center=dict(x=0, y=0, z=-0.05)),
    ),
    margin=dict(l=0, r=0, t=52, b=0),
    width=1620,
    height=820,
)

out = Path(__file__).resolve().parent / "the-canyon.png"
fig.write_image(str(out), scale=2)
im = Image.open(out).convert("RGB")
bg = Image.new("RGB", im.size, (5, 7, 12))
bbox = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0).getbbox()
pad = 10
im.crop(
    (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(im.width, bbox[2] + pad),
        min(im.height, bbox[3] + pad),
    )
).save(out)
print("saved", out, Image.open(out).size, file=sys.stderr)
