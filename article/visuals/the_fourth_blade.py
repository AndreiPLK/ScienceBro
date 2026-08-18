"""THE FOURTH BLADE -- how close the next knife comes to the shore.

Knife 2 is the published shore. Knife 3 is the published blade theorem, which is
delicate: in the scaling limit the blade cone is exactly tangent to the shore
asymptote. This figure asks the same question one knife further out, using
tonight's closed form (lab/knife_closed_form.py, verified against the exact
engine on 24 cells per knife with zero disagreements, and on 1120 cells below the
shore with zero failures).

The knife-j condition is a polynomial in (n, D, lam); for j = 4 it is cubic in D
with a negative leading coefficient, so each (n, lam) has a critical dimension
D*(n, lam) where the knife vanishes. The knife is safe below the shore exactly
when

        min over n of D*(n, lam)   >   T_hat(lam).

PLOTTED: that minimum against the shore, as a ratio, for both j = 3 (the
published case, as a control) and j = 4 (new). The ratio stays above 1
everywhere computed, and falls toward 1 as lam grows -- the same asymptotic
tangency the published blade theorem has.

The scan range in n must GROW with lam: the minimising level sits near 1.7 lam,
and an earlier version of this measurement capped n at 120 and produced a
spurious upturn at lam = 150 for exactly that reason. Here the range is tied to
lam and the minimising n is reported so the cap can be checked.

Roots are taken with flint's certified complex_roots, not numpy (CLAUDE.md, the
fast-engine law).
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "projects" / "qg-bootstrap" / "lab"))
import plotly.graph_objects as go  # noqa: E402
import sympy as sp  # noqa: E402
from flint import fmpq, fmpq_poly  # noqa: E402
from keystone_hunt import T_hat  # noqa: E402
from knife_closed_form import D as Dsym  # noqa: E402
from knife_closed_form import knife_polynomial, lam as lamsym, n as nsym  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

CACHE = Path("/tmp/fourth_blade.json")
LAMS = [F(1, 4), F(1, 2), F(1), F(2), F(3), F(5), F(7), F(10), F(14), F(20), F(26), F(40), F(60)]


def d_star(P, nv: int, lv: F):
    """Smallest root in D above 3, via certified roots on the exact polynomial."""
    poly = sp.Poly(P.subs({nsym: nv, lamsym: sp.Rational(lv.numerator, lv.denominator)}), Dsym)
    coeffs = [sp.Rational(c) for c in poly.all_coeffs()][::-1]
    q = fmpq_poly([fmpq(c.p, c.q) for c in coeffs])
    if q.degree() < 1:
        return None
    roots = []
    for z, _ in q.complex_roots():
        c = complex(z)
        if abs(c.imag) < 1e-9 and c.real > 3:
            roots.append(c.real)
    return min(roots) if roots else None


def gather():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    out = {}
    for j in (3, 4):
        P = knife_polynomial(j)
        series = []
        for lv in LAMS:
            top = max(60, int(4 * float(lv)) + 60)
            best = (None, None)
            for nv in range(5, top):
                d = d_star(P, nv, lv)
                if d is None:
                    continue
                if best[0] is None or d < best[0]:
                    best = (d, nv)
            if best[0] is None:
                continue
            shore = T_hat(float(lv))
            series.append([float(lv), best[0], shore, best[1], top - 1])
            print(
                f"  j={j} lam={lv}: D*={best[0]:.3f} at n={best[1]} "
                f"(scanned to {top - 1}), shore={shore:.3f}",
                flush=True,
            )
        out[str(j)] = series
    CACHE.write_text(json.dumps(out), encoding="utf-8")
    return out


d = gather()
fig = go.Figure()
for j, col, name in (
    (3, "#c9e86b", "knife 3 — the published blade theorem"),
    (4, "#4df0ff", "knife 4 — this work"),
):
    s = d[str(j)]
    fig.add_trace(
        go.Scatter(
            x=[r[0] for r in s],
            y=[r[1] / r[2] for r in s],
            mode="lines+markers",
            name=name,
            line=dict(color=col, width=3),
            marker=dict(size=9),
            customdata=[[r[3], r[4]] for r in s],
            hovertemplate="lam=%{x}<br>ratio=%{y:.4f}<br>minimising n=%{customdata[0]}"
            " (scanned to %{customdata[1]})<extra></extra>",
        )
    )
fig.add_hline(y=1.0, line=dict(color="#ff2a6d", width=2, dash="dash"))
fig.add_annotation(
    x=1.0,
    y=1.02,
    text="the shore — below this line the knife would cut",
    showarrow=False,
    font=dict(color="#ff8fb0", size=12),
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14130f",
    plot_bgcolor="#14130f",
    title=dict(
        text="THE FOURTH BLADE — how close the next knife comes to the shore"
        "<br><sup>Exact closed form, verified against the engine on 24 cells "
        "per knife (zero disagreements) and 1120 cells below the shore (zero "
        "failures).<br>Plotted: the smallest dimension at which the knife "
        "vanishes, divided by the shore. Above 1 means the knife never cuts "
        "into the allowed region.<br>Both knives stay above 1 and approach it "
        "as the family parameter grows — the fourth blade is as delicate as "
        "the published third one.</sup>",
        font=dict(color="#ede8dc", size=20),
        x=0.02,
        y=0.95,
    ),
    xaxis=dict(title="lam — family parameter", type="log", color="#a8a08e", gridcolor="#322e26"),
    yaxis=dict(
        title="min over levels of D* , divided by the shore", color="#a8a08e", gridcolor="#322e26"
    ),
    legend=dict(font=dict(color="#a8a08e", size=11), x=0.62, y=0.97, bgcolor="rgba(20,19,15,0.75)"),
    margin=dict(l=80, r=30, t=140, b=70),
    width=1440,
    height=680,
)

out = Path(__file__).resolve().parent / "fourth-blade.png"
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
