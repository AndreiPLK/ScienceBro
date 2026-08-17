"""Generator of the paper-3 figure (B3 fix: persisted script).

Writes article/visuals/knives-above-shore.html (close-up) and
article/visuals/knives-zoomout.html (fleet zoom-out) from the CLOSED FORMS
(j=3 rung windows + the T_n shore). Render command (documented, headless
Chrome at 2x then LANCZOS downscale; the paper figure is the full panel,
axis labels uncropped):

  chrome --headless --disable-gpu --window-size=1280,800
    --force-device-scale-factor=2 --hide-scrollbars --virtual-time-budget=9000
    --screenshot=<out2x.png> <file:///...html>
"""

from __future__ import annotations

import json
import sys
from math import sqrt
from pathlib import Path

VIS = Path(__file__).resolve().parents[3] / "article" / "visuals"
BATTERY = "3,053,832"


def min_T(lam: float) -> float:
    return min(
        (3 * (2 * n - 3) / (n * (n - 2))) * (lam * lam + (2 * n - 2) * lam + 1) + 2 * n
        for n in range(3, 3000)
    )


def window(n: int, lam: float):
    m = n - 3
    s = lam + n - 1
    G = 2 * (m + 1) * (m + 3) / (3 * (2 * m + 3))
    al = (m + 3) * (5 * m**3 + 21 * m**2 + 19 * m + 15) / (45 * (2 * m + 1) * (2 * m + 3))
    b = 2 * al + G * s * s
    disc = b * b - 4 * al * s**4
    if disc <= 0:
        return None
    r = sqrt(disc)
    off = 4 * m + 1
    return (b - r) / (2 * al) - off, (b + r) / (2 * al) - off


PAGE = """<!DOCTYPE html><html><head><meta charset='utf-8'>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>body{{margin:0;background:radial-gradient(ellipse at 42% 6%,#1a1a3a 0%,#0a0a18 48%,#050510 82%);font-family:Consolas,monospace}}
.panel{{margin:14px;padding:10px;border:1px solid rgba(5,217,232,.3);border-radius:12px}}
h1{{color:#eafdff;font-size:22px;margin:8px 14px 2px;letter-spacing:.09em;text-shadow:0 0 16px #05d9e8}}
.sub{{color:#7f93bb;font-size:12.5px;margin:0 14px 6px}}</style></head><body>
<div class="panel"><h1>{title}</h1>
<p class="sub">{sub}</p>
<div id="p" style="width:1240px;height:690px"></div></div>
<script>
Plotly.newPlot('p', {traces},
{{paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(6,6,14,0.3)',
 xaxis:{{title:{{text:'lambda — how string-like the theory is',font:{{size:15}}}},color:'#7f93bb',gridcolor:'rgba(45,45,80,.35)',range:{xr}}},
 yaxis:{{title:{{text:'D — dimensions of space',font:{{size:15}}}},color:'#7f93bb',gridcolor:'rgba(45,45,80,.35)',range:{yr}}},
 annotations: {annos},
 margin:{{t:8,b:64,l:70,r:16}}}},{{displayModeBar:false}});
</script></body></html>"""


def band(n, lams, col):
    lo, hi, xs = [], [], []
    for x in lams:
        w = window(n, x)
        if w and w[1] > 4:
            xs.append(x)
            lo.append(max(w[0], 4))
            hi.append(w[1])
    if not xs:
        return None
    return {
        "x": xs + xs[::-1],
        "y": hi + lo[::-1],
        "fill": "toself",
        "fillcolor": col + "59",
        "line": {"color": col, "width": 1.8},
        "mode": "lines",
        "showlegend": False,
    }


def closeup():
    lams = [0.05 * i for i in range(1, 141)]
    shore = [min_T(x) for x in lams]
    traces = [
        {
            "x": lams + lams[::-1],
            "y": shore + [0] * len(lams),
            "fill": "toself",
            "fillcolor": "rgba(10,163,194,0.13)",
            "line": {"width": 0},
            "mode": "lines",
            "showlegend": False,
        }
    ]
    for n, col in ((6, "#ff2a6d"), (8, "#c86bd8"), (11, "#5a78e8")):
        b = band(n, lams, col)
        if b:
            traces.append(b)
    traces.append(
        {
            "x": lams,
            "y": shore,
            "mode": "lines",
            "line": {"color": "#3fe7f5", "width": 6},
            "showlegend": False,
        }
    )
    traces.append(
        {
            "x": [1],
            "y": [23],
            "mode": "markers",
            "showlegend": False,
            "marker": {
                "color": "#ffffff",
                "size": 14,
                "symbol": "diamond",
                "line": {"color": "#f9f871", "width": 4},
            },
        }
    )
    annos = [
        {
            "x": 4.6,
            "y": 30,
            "text": "<b>LIVING LAND</b><br>allowed theories of gravity<br>(below the shore)",
            "showarrow": False,
            "font": {"color": "#9ff5ff", "size": 17},
            "align": "center",
        },
        {
            "x": 1.05,
            "y": 100,
            "text": "<b>DEAD LAND</b><br>already excluded by the shore",
            "showarrow": False,
            "font": {"color": "#7f93bb", "size": 17},
            "align": "center",
        },
        {
            "x": 2.45,
            "y": 62,
            "text": "<b>THE BLADES</b><br>extra kill-windows"
            " found by the master formula:<br>level 6 (pink), 8 (violet),"
            " 11 (blue) — and so on",
            "showarrow": False,
            "font": {"color": "#ff5f95", "size": 15},
            "align": "center",
        },
        {
            "x": 3.6,
            "y": 83.5,
            "text": "every blade floats ABOVE the shore"
            " —<br>none ever cuts into the living land<br>(" + BATTERY + " exact checks, 0 hits)",
            "showarrow": False,
            "font": {"color": "#f9f871", "size": 15},
            "align": "center",
        },
        {
            "x": 1.35,
            "y": 17.5,
            "text": "<b>the string</b> — on the shore at D=23",
            "showarrow": False,
            "font": {"color": "#f9f871", "size": 15},
            "align": "center",
        },
        {
            "x": 1,
            "y": 23,
            "ax": 40,
            "ay": 28,
            "text": "",
            "showarrow": True,
            "arrowcolor": "#f9f871",
            "arrowwidth": 2,
        },
    ]
    title = "THE BLADES NEVER TOUCH THE SHORE"
    sub = (
        "one picture of the whole result: the shore (cyan) divides living"
        " land from dead land &middot; the master formula reveals extra"
        " kill-windows (&laquo;blades&raquo;) &middot; all of them hang"
        " strictly above the shore &middot; every curve exact"
    )
    html = PAGE.format(
        title=title,
        sub=sub,
        traces=json.dumps(traces),
        xr="[0,6.2]",
        yr="[4,115]",
        annos=json.dumps(annos, ensure_ascii=False),
    )
    (VIS / "knives-above-shore.html").write_text(html, encoding="utf-8")


def zoomout():
    lams = [0.25 * i for i in range(1, 201)]
    shore = [min_T(x) for x in lams]
    traces = [
        {
            "x": lams + lams[::-1],
            "y": shore + [0] * len(lams),
            "fill": "toself",
            "fillcolor": "rgba(10,163,194,0.13)",
            "line": {"width": 0},
            "mode": "lines",
            "showlegend": False,
        }
    ]
    cols = {
        6: "#ff2a6d",
        11: "#c86bd8",
        20: "#7a5ae0",
        35: "#4a78e8",
        60: "#2aa3c8",
        100: "#2ac8a8",
        160: "#5fe08f",
    }
    for n, col in cols.items():
        b = band(n, lams, col)
        if b:
            traces.append(b)
    traces.append(
        {
            "x": lams,
            "y": shore,
            "mode": "lines",
            "line": {"color": "#3fe7f5", "width": 5},
            "showlegend": False,
        }
    )
    traces.append(
        {
            "x": [1],
            "y": [23],
            "mode": "markers",
            "showlegend": False,
            "marker": {
                "color": "#ffffff",
                "size": 10,
                "symbol": "diamond",
                "line": {"color": "#f9f871", "width": 3},
            },
        }
    )
    annos = [
        {
            "x": 40,
            "y": 280,
            "text": "<b>LIVING LAND</b><br>below the shore",
            "showarrow": False,
            "font": {"color": "#9ff5ff", "size": 18},
            "align": "center",
        },
        {
            "x": 8,
            "y": 880,
            "text": "<b>DEAD LAND</b>",
            "showarrow": False,
            "font": {"color": "#7f93bb", "size": 18},
            "align": "center",
        },
        {
            "x": 22,
            "y": 700,
            "text": "the fleet of blades — levels 6, 11,"
            " 20, 35, 60, 100, 160 —<br>sails parallel to the shore, always"
            " above it,<br>drifting further away as λ grows",
            "showarrow": False,
            "font": {"color": "#ff8fb5", "size": 15},
            "align": "center",
        },
        {
            "x": 42,
            "y": 862,
            "text": "the shore straightens onto<br>D = (12+4√3)·λ (paper 2)",
            "showarrow": False,
            "font": {"color": "#3fe7f5", "size": 14},
            "align": "center",
        },
        {
            "x": 5.2,
            "y": 62,
            "text": "the string, D=23",
            "showarrow": False,
            "font": {"color": "#f9f871", "size": 13},
            "align": "center",
        },
        {
            "x": 1.2,
            "y": 26,
            "ax": 40,
            "ay": -14,
            "text": "",
            "showarrow": True,
            "arrowcolor": "#f9f871",
            "arrowwidth": 1.6,
        },
    ]
    title = "ZOOM OUT: THE FLEET OF BLADES"
    sub = (
        "the same picture from far away: lambda to 50, dimensions to"
        " ~1000 &middot; the fleet of kill-windows sails parallel to the"
        " shore and never lands &middot; every curve exact"
    )
    html = PAGE.format(
        title=title,
        sub=sub,
        traces=json.dumps(traces),
        xr="[0,51]",
        yr="[4,1000]",
        annos=json.dumps(annos, ensure_ascii=False),
    )
    (VIS / "knives-zoomout.html").write_text(html, encoding="utf-8")


def main() -> int:
    closeup()
    zoomout()
    print("written knives-above-shore.html, knives-zoomout.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
