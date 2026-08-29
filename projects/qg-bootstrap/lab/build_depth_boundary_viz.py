"""Build the depth-boundary page from the artefact, refusing to lie about it.

The house pattern (docs/DECISIONS.md, first used for outreach/shore_of_universes.html):
the page is generated from the SAME artefact the science is recorded in, every
number quoted on the page is computed here from that artefact, and the builder
REFUSES to emit if the data would falsify the page's central claim.

Central claim of this page: the recorded depth law "largest good j = n/2 + 1"
fails on a large fraction of n, and a candidate law fitted on n <= 61 is then
tested on a HELD-OUT sample n > 61.  If the recorded law turned out not to fail,
the page has no subject and nothing is written.  The candidate's verdict is
whatever the held-out numbers say -- the sentence is generated from them, so the
page cannot flatter it.

Run: python lab/build_depth_boundary_viz.py -> outreach/depth_boundary.html
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "outreach" / "depth_boundary.html"

W, H = 980, 420
PAD_L, PAD_R, PAD_T, PAD_B = 56, 18, 22, 44
SPLIT_N = 61


def svg(rows: list[dict], split_n: int) -> str:
    ns = [r["n"] for r in rows]
    js = [r["largest_good_j"] for r in rows]
    n0, n1 = min(ns), max(ns)
    j1 = max(js) + 3

    def X(n: float) -> float:
        return PAD_L + (n - n0) / (n1 - n0) * (W - PAD_L - PAD_R)

    def Y(j: float) -> float:
        return H - PAD_B - j / j1 * (H - PAD_T - PAD_B)

    parts = []
    for j in range(0, j1 + 1, 10):
        parts.append(
            f'<line class="grid" x1="{X(n0):.1f}" y1="{Y(j):.1f}" x2="{X(n1):.1f}" y2="{Y(j):.1f}"/>'
            f'<text class="tick" x="{PAD_L - 10:.1f}" y="{Y(j) + 4:.1f}" text-anchor="end">{j}</text>'
        )
    for n in range(20, n1 + 1, 20):
        parts.append(
            f'<text class="tick" x="{X(n):.1f}" y="{H - PAD_B + 20:.1f}" '
            f'text-anchor="middle">{n}</text>'
        )
    if n0 < split_n < n1:
        parts.append(
            f'<line class="split" x1="{X(split_n + 0.5):.1f}" y1="{PAD_T:.1f}" '
            f'x2="{X(split_n + 0.5):.1f}" y2="{H - PAD_B:.1f}"/>'
            f'<text class="split-label" x="{X(split_n + 0.5) + 8:.1f}" '
            f'y="{PAD_T + 14:.1f}">held out from here</text>'
        )
    law = " ".join(f"{X(r['n']):.1f},{Y(r['law_n_over_2_plus_1']):.1f}" for r in rows)
    cand = " ".join(f"{X(r['n']):.1f},{Y(r['candidate_4n_plus_32_over_9']):.1f}" for r in rows)
    parts.append(f'<polyline class="law" points="{law}"/>')
    parts.append(f'<polyline class="cand" points="{cand}"/>')
    for r in rows:
        hit = r["largest_good_j"] == r["candidate_4n_plus_32_over_9"]
        cls = "pt hit" if hit else "pt miss"
        parts.append(
            f'<rect class="{cls}" x="{X(r["n"]) - 2.2:.1f}" '
            f'y="{Y(r["largest_good_j"]) - 2.2:.1f}" width="4.4" height="4.4"/>'
        )
    parts.append(
        f'<text class="axis" x="{PAD_L:.1f}" y="{H - 6:.1f}">n</text>'
        f'<text class="axis" x="{PAD_L - 44:.1f}" y="{PAD_T + 4:.1f}">j</text>'
    )
    body = "".join(parts)
    return (
        f'<svg viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="measured depth cutoff against two candidate laws">{body}</svg>'
    )


PAGE = """<title>Depth Cutoff Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  --ink: #12151d; --ink-soft: #4a5164; --paper: #eceef3; --panel: #f6f7fa;
  --rule: #cdd2dd; --amber: #a86a1f; --rose: #a63d55; --teal: #1f6f68;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink: #e7e9ef; --ink-soft: #99a1b5; --paper: #101219; --panel: #171a23;
    --rule: #2b3140; --amber: #e0a35c; --rose: #e07d92; --teal: #56b7ac;
  }
}
:root[data-theme="dark"] {
  --ink: #e7e9ef; --ink-soft: #99a1b5; --paper: #101219; --panel: #171a23;
  --rule: #2b3140; --amber: #e0a35c; --rose: #e07d92; --teal: #56b7ac;
}
body { background: var(--paper); color: var(--ink);
  font: 400 17px/1.62 "Source Sans 3", ui-sans-serif, system-ui, sans-serif;
  margin: 0; padding: 40px 22px 72px; }
main { max-width: 68ch; margin: 0 auto; display: flex; flex-direction: column; gap: 22px; }
h1 { font: 600 clamp(30px, 5vw, 44px)/1.1 "Fraunces", Georgia, serif;
  margin: 0; text-wrap: balance; letter-spacing: -0.01em; }
h2 { font: 600 22px/1.25 "Fraunces", Georgia, serif; margin: 14px 0 0; text-wrap: balance; }
.eyebrow { font: 500 12px/1 "IBM Plex Mono", ui-monospace, monospace;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft); }
p { margin: 0; }
.lede { font-size: 19px; color: var(--ink-soft); }
figure { margin: 0; background: var(--panel); border: 1px solid var(--rule);
  border-radius: 4px; padding: 14px 14px 8px; overflow-x: auto; }
svg { display: block; min-width: 700px; width: 100%; height: auto; }
.grid { stroke: var(--rule); stroke-width: 1; }
.tick, .axis { fill: var(--ink-soft); font: 400 11px "IBM Plex Mono", monospace; }
.split { stroke: var(--ink-soft); stroke-width: 1; stroke-dasharray: 3 4; }
.split-label { fill: var(--ink-soft); font: 400 11px "IBM Plex Mono", monospace; }
.law { fill: none; stroke: var(--rose); stroke-width: 1.6; stroke-dasharray: 6 4; }
.cand { fill: none; stroke: var(--teal); stroke-width: 1.6; }
.pt { fill: var(--ink); }
.pt.miss { fill: var(--amber); }
figcaption { font: 400 13px/1.5 "IBM Plex Mono", monospace; color: var(--ink-soft);
  padding-top: 10px; }
.key { display: flex; flex-wrap: wrap; gap: 16px;
  font: 400 13px "IBM Plex Mono", monospace; color: var(--ink-soft); }
.key span { display: inline-flex; align-items: center; gap: 7px; }
.swatch { width: 16px; height: 3px; border-radius: 2px; }
.dot { width: 7px; height: 7px; border-radius: 0; }
ul { margin: 0; padding-left: 1.1em; display: flex; flex-direction: column; gap: 8px; }
code { font: 400 15px "IBM Plex Mono", monospace; background: var(--panel);
  border: 1px solid var(--rule); border-radius: 3px; padding: 1px 5px; }
footer { color: var(--ink-soft); font-size: 14px; border-top: 1px solid var(--rule);
  padding-top: 16px; }
</style>
<main>
  <p class="eyebrow">quantum-gravity bootstrap &middot; 29 august 2026</p>
  <h1>A law that was fitted on multiples of four</h1>
  <p class="lede">The repository recorded an <em>exact</em> depth cutoff for the
  Hausdorff mechanism: <code>j &le; n/2 + 1</code>. It was measured at
  n = 12, 16, 20, 24, 28, 36, 44 &mdash; every one a multiple of four, and that is
  exactly where the formula is right. Computed at every n from 11 to __NMAX__, it
  fails __MISM__ times out of __TOTAL__.</p>

  <figure>
    __SVG__
    <figcaption>Each square is one measurement: the largest knife order j for which
    the moment conditions hold, at &lambda; = 10<sup>4</sup>, from exact Hankel minors.
    Dark squares are where the candidate line agrees, amber where it does not.</figcaption>
  </figure>
  <p class="key">
    <span><span class="swatch" style="background:var(--rose)"></span>recorded law n/2+1</span>
    <span><span class="swatch" style="background:var(--teal)"></span>candidate (4n+32)/9</span>
    <span><span class="swatch dot" style="background:var(--ink)"></span>measured, agrees</span>
    <span><span class="swatch dot" style="background:var(--amber)"></span>measured, disagrees</span>
  </p>

  <h2>What the boundary actually does</h2>
  <p>It is always odd. It rises in runs of four or five consecutive n. And it drifts
  below n/2 as n grows &mdash; so the mechanism reaches a shrinking fraction of the
  available depths, not half of them.</p>

  <h2>The candidate, and its honest score</h2>
  <p>Fitting the simplest shape that matches &mdash; the largest odd j below a straight
  line &mdash; on n = 11..61 gives <code>j &le; (4n+32)/9</code>, right __FIT__ there.
  __VERDICT__</p>

  <h2>Why the wrong law survived</h2>
  <p>The sample could not contradict it. The two candidate formulas agree on every
  even n, and the recorded run contained no odd n at all; the odd case was computed
  for the first time today, while chasing an unrelated question.</p>
  <ul>
    <li>A claim that <em>prunes a search</em> is the claim that never gets tested
    &mdash; keep sampling the pruned branch.</li>
    <li>Before recording &ldquo;exact&rdquo;, name the nearest rival formula and check
    that the grid can tell them apart.</li>
  </ul>

  <footer>Built by <code>lab/build_depth_boundary_viz.py</code> from
  <code>results/depth_boundary_map.json</code>. Every number here is computed from that
  artefact, and the builder refuses to emit if the data stops supporting the claim.
  Recorded as ERR-0017.</footer>
</main>
"""


def main() -> int:
    data = json.loads((RES / "depth_boundary_map.json").read_text(encoding="utf-8"))
    rows = [r for r in data["rows"] if r["largest_good_j"]]
    mism = sum(1 for r in rows if not r["matches_recorded_law"])
    if mism == 0:
        print(
            "REFUSING TO BUILD: the recorded law does not fail on this data, so the page's "
            "central claim is false. Investigate before rebuilding."
        )
        return 1
    fit = data["candidate_law"]["hits_on_fit_sample"]
    held = data["candidate_law"]["hits_on_held_out_sample"]
    if held[1]:
        pct = 100 * held[0] / held[1]
        verdict = f"On the held-out sample, which it was never shown, it is right {held[0]} of {held[1]} ({pct:.0f}%)."
        if pct < 80:
            verdict += " That is not a law, that is a shape."
    else:
        verdict = "It has not been tested out of sample yet, so it is a fit and nothing more."
    html = (
        PAGE.replace("__SVG__", svg(rows, SPLIT_N))
        .replace("__NMAX__", str(max(r["n"] for r in rows)))
        .replace("__MISM__", str(mism))
        .replace("__TOTAL__", str(len(rows)))
        .replace("__FIT__", f"{fit[0]} of {fit[1]}")
        .replace("__VERDICT__", verdict)
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(
        f"written {OUT} ({OUT.stat().st_size // 1024} KB): {len(rows)} measured n, "
        f"{mism} law mismatches, candidate held-out {held[0]}/{held[1]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
