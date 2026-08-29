"""Build the children's page about the one block that points down.

House pattern: generated from the artefacts, every number computed here, and the
builder refuses to emit if the story it tells stops being true -- specifically, if
any measured depth has its negatives somewhere other than the J-2 block, or if the
certified run of depths is shorter than three.

Run: python lab/build_kids_viz.py -> outreach/one_block_down.html
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "outreach" / "one_block_down.html"


def load():
    cert, patt = [], []
    for f in glob.glob(str(RES / "repair_certificate_j*.json")):
        if "_v" in Path(f).stem:
            continue
        cert.append(json.loads(Path(f).read_text(encoding="utf-8")))
    for f in glob.glob(str(RES / "farbelow_negative_pattern_j*.json")):
        patt.append(json.loads(Path(f).read_text(encoding="utf-8")))
    cert.sort(key=lambda d: d["j"])
    patt.sort(key=lambda d: d["j"])
    return cert, patt


def blocks_svg(j: int) -> str:
    """A row of j blocks: all pointing up, the one at J-2 pointing down."""
    w, h, pad = 640, 190, 16
    bw = (w - 2 * pad) / j
    mid = h / 2
    parts = [f'<line class="ground" x1="{pad}" y1="{mid}" x2="{w - pad}" y2="{mid}"/>']
    for k in range(j):
        x = pad + k * bw + bw * 0.16
        bwid = bw * 0.68
        down = k == j - 2
        bh = 52 if not down else 44
        y = mid - bh if not down else mid
        cls = "down" if down else "up"
        parts.append(
            f'<rect class="blk {cls}" x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{bh}" rx="3"/>'
        )
        if down:
            parts.append(
                f'<text class="tag" x="{x + bwid / 2:.1f}" y="{mid + bh + 18:.1f}" '
                f'text-anchor="middle">this one</text>'
            )
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="a row of blocks, all pointing up except one">{"".join(parts)}</svg>'


PAGE = """<title>One Block Points Down</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Newsreader:opsz,wght@6..72,300;6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  --ink: #1b1b23; --soft: #5d5f70; --paper: #fbf7f0; --panel: #fffdf9;
  --rule: #e2dbcd; --up: #2e8b74; --down: #d1493f; --sun: #e8a020;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink: #f2eee6; --soft: #a8a6b4; --paper: #14141b; --panel: #1c1c25;
    --rule: #333140; --up: #58c3a8; --down: #f0776b; --sun: #f2b950;
  }
}
:root[data-theme="dark"] {
  --ink: #f2eee6; --soft: #a8a6b4; --paper: #14141b; --panel: #1c1c25;
  --rule: #333140; --up: #58c3a8; --down: #f0776b; --sun: #f2b950;
}
body { background: var(--paper); color: var(--ink); margin: 0; padding: 40px 22px 80px;
  font: 300 19px/1.7 "Newsreader", Georgia, serif; }
main { max-width: 60ch; margin: 0 auto; display: flex; flex-direction: column; gap: 26px; }
h1 { font: 800 clamp(34px, 7vw, 58px)/1.02 "Bricolage Grotesque", system-ui, sans-serif;
  margin: 0; letter-spacing: -0.02em; text-wrap: balance; }
h2 { font: 600 26px/1.2 "Bricolage Grotesque", system-ui, sans-serif; margin: 20px 0 0;
  text-wrap: balance; }
p { margin: 0; }
.big { font-size: 22px; }
.eyebrow { font: 500 12px/1 "IBM Plex Mono", monospace; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--soft); }
figure { margin: 0; background: var(--panel); border: 1px solid var(--rule);
  border-radius: 14px; padding: 18px; overflow-x: auto; }
svg { display: block; width: 100%; height: auto; min-width: 420px; }
.ground { stroke: var(--rule); stroke-width: 2; }
.blk.up { fill: var(--up); }
.blk.down { fill: var(--down); }
.tag { fill: var(--down); font: 500 12px "IBM Plex Mono", monospace; }
.controls { display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  font: 500 14px "IBM Plex Mono", monospace; color: var(--soft); }
input[type=range] { flex: 1 1 200px; accent-color: var(--sun); }
.seesaw { background: var(--panel); border: 1px solid var(--rule); border-radius: 14px;
  padding: 20px 18px; }
.rule { font: 500 17px/1.9 "IBM Plex Mono", monospace; color: var(--ink);
  background: transparent; text-align: center; }
.rule b { color: var(--up); }
.rule i { color: var(--down); font-style: normal; }
table { border-collapse: collapse; font: 400 15px "IBM Plex Mono", monospace;
  font-variant-numeric: tabular-nums; width: 100%; }
th, td { text-align: right; padding: 6px 10px 6px 0; border-bottom: 1px solid var(--rule); }
th:first-child, td:first-child { text-align: left; }
th { color: var(--soft); font-weight: 500; }
.zero { color: var(--up); font-weight: 500; }
footer { color: var(--soft); font-size: 15px; border-top: 1px solid var(--rule);
  padding-top: 18px; }
</style>
<main>
  <p class="eyebrow">a note for the children &middot; 29 august 2026</p>
  <h1>One block points down</h1>
  <p class="big">We wanted to know if something in nature can ever go wrong. Not
  once, not a hundred times &mdash; <em>never</em>, in infinitely many cases at once.
  Here is how the question turned into a row of blocks, and how the row was made
  safe.</p>

  <h2>The row</h2>
  <p>Every question of ours can be written as a long row of blocks. Each block
  pushes the answer <span style="color:var(--up)">up</span> or
  <span style="color:var(--down)">down</span>. If every block pushes up, the answer
  is safe and we are done.</p>
  <p>They almost all push up. <strong>Exactly one</strong> pushes down &mdash; always
  the same one, the second from the end. We measured it at __NDEPTHS__ different
  sizes of the row and it was always that one, never another.</p>

  <figure>
    __BLOCKS__
    <div class="controls">
      <label for="jj">row length</label>
      <input id="jj" type="range" min="6" max="16" value="__JDEF__" step="1">
      <span id="jout">__JDEF__ blocks</span>
    </div>
  </figure>

  <h2>The trick: two friends and a heavy stone</h2>
  <p>You cannot remove the bad block. But you can stop looking at it alone. Take it
  together with the two blocks on either side of it &mdash; three blocks, like two
  friends on a seesaw holding up one heavy stone in the middle.</p>
  <div class="seesaw">
    <p class="rule">4 &times; <b>left friend</b> &times; <b>right friend</b> &nbsp;&gt;&nbsp;
    <i>stone</i> &times; <i>stone</i></p>
  </div>
  <p>If that is true, the three of them together never fall &mdash; no matter how the
  row is stretched or squeezed. It is the same rule that decides whether a
  <em>y = ax&sup2; + bx + c</em> curve ever dips below zero, which you will meet in
  school as the discriminant.</p>

  <h2>What we did today</h2>
  <p>We did not test the rule with numbers. We wrote the whole thing out as one
  giant sum &mdash; thousands of pieces &mdash; and checked that <strong>not a single
  piece is negative</strong>. When nothing is negative and nothing you plug in is
  negative either, the answer cannot be negative. That is not a test. That is a
  proof.</p>
  <table>
    <tr><th>row length</th><th>pieces in the sum</th><th>negative pieces</th></tr>
    __CERT_ROWS__
  </table>
  <p>Zero, every time, from __CLO__ all the way to __CHI__.</p>

  <h2>Why it matters</h2>
  <p>Each row length is one more case where a rule of nature is safe forever. We
  used to need a heavy machine, running for hours, to settle a single one. Now
  three blocks and one line of school algebra settle it.</p>

  <footer>Built by <code>lab/build_kids_viz.py</code> from the same files the
  mathematics lives in. Every number here was computed from them, and the page
  refuses to be built if they stop saying so.</footer>
</main>
<script>
  const rows = __ROWS_JSON__;
  const slider = document.getElementById('jj');
  const out = document.getElementById('jout');
  const fig = document.querySelector('figure svg');
  function draw(j) {
    const w = 640, h = 190, pad = 16, bw = (w - 2*pad)/j, mid = h/2;
    let s = `<line class="ground" x1="${pad}" y1="${mid}" x2="${w-pad}" y2="${mid}"/>`;
    for (let k = 0; k < j; k++) {
      const x = pad + k*bw + bw*0.16, bwid = bw*0.68, down = (k === j-2);
      const bh = down ? 44 : 52, y = down ? mid : mid - bh;
      s += `<rect class="blk ${down ? 'down' : 'up'}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bwid.toFixed(1)}" height="${bh}" rx="3"/>`;
      if (down) s += `<text class="tag" x="${(x+bwid/2).toFixed(1)}" y="${(mid+bh+18).toFixed(1)}" text-anchor="middle">this one</text>`;
    }
    fig.innerHTML = s;
    out.textContent = j + ' blocks';
  }
  slider.addEventListener('input', e => draw(+e.target.value));
</script>
"""


def main() -> int:
    cert, patt = load()
    if not cert or not patt:
        print("REFUSING TO BUILD: artefacts missing.")
        return 1
    for d in patt:
        degs = list(d["by_y_degree"])
        if len(degs) != 1 or int(degs[0]) != d["j"] - 2:
            print(
                f"REFUSING TO BUILD: at j={d['j']} the down-block is not the second from the end."
            )
            return 1
    run = []
    for c in cert:
        if c["negative_monomials"] == 0:
            run.append(c)
        else:
            break
    if len(run) < 3:
        print("REFUSING TO BUILD: the certified run is too short to tell this story.")
        return 1
    rows = "\n    ".join(
        f'<tr><td>{c["j"]}</td><td>{c["monomials"]}</td><td class="zero">0</td></tr>' for c in run
    )
    html = (
        PAGE.replace("__BLOCKS__", blocks_svg(11))
        .replace("__JDEF__", "11")
        .replace("__NDEPTHS__", str(len(patt)))
        .replace("__CERT_ROWS__", rows)
        .replace("__CLO__", str(run[0]["j"]))
        .replace("__CHI__", str(run[-1]["j"]))
        .replace("__ROWS_JSON__", json.dumps([c["j"] for c in run]))
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(
        f"written {OUT} ({os.path.getsize(OUT) // 1024} KB): {len(patt)} measured depths, "
        f"certified run {run[0]['j']}..{run[-1]['j']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
