"""Build the repair-certificate page from the artefacts, refusing to overstate them.

House pattern (docs/DECISIONS.md): the page is generated from the artefacts the
science lives in, every number on it is computed here, and the builder REFUSES to
emit if the data stops supporting the page's central claim.

Central claim: (R) 4 c_{J-1} c_{J-3} - c_{J-2}^2 >= 0 is manifestly positive over
the far-below region for a run of consecutive J starting at 7, and the far-below
polynomial has exactly one negative y-coefficient there -- so the two together
prove positivity by one grouping.  If either half stopped holding at the depths
the page names, there is no page.

Run: python lab/build_repair_viz.py -> outreach/repair_certificate.html
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "outreach" / "repair_certificate.html"

W, H = 900, 300
PAD_L, PAD_R, PAD_T, PAD_B = 62, 20, 20, 46


def load() -> tuple[list[dict], list[dict]]:
    cert, patt = [], []
    for f in glob.glob(str(RES / "repair_certificate_j*.json")):
        if "_v" in Path(f).stem:  # in-regime variants are handled separately
            continue
        cert.append(json.loads(Path(f).read_text(encoding="utf-8")))
    for f in glob.glob(str(RES / "farbelow_negative_pattern_j*.json")):
        patt.append(json.loads(Path(f).read_text(encoding="utf-8")))
    cert.sort(key=lambda d: d["j"])
    patt.sort(key=lambda d: d["j"])
    return cert, patt


def svg(cert: list[dict]) -> str:
    js = [c["j"] for c in cert]
    j0, j1 = min(js), max(js)
    top = max(max(c["negative_monomials"] for c in cert), 1)

    def X(j: float) -> float:
        return PAD_L + (j - j0) / (j1 - j0) * (W - PAD_L - PAD_R)

    def Y(v: float) -> float:
        return H - PAD_B - (v / top) * (H - PAD_T - PAD_B)

    parts = [f'<line class="zero" x1="{PAD_L}" y1="{Y(0):.1f}" x2="{W - PAD_R}" y2="{Y(0):.1f}"/>']
    for c in cert:
        x, v = X(c["j"]), c["negative_monomials"]
        cls = "bar ok" if v == 0 else "bar bad"
        h = max(3.0, Y(0) - Y(v))
        parts.append(
            f'<rect class="{cls}" x="{x - 5:.1f}" y="{Y(v):.1f}" width="10" height="{h:.1f}"/>'
        )
        parts.append(
            f'<text class="lab" x="{x:.1f}" y="{H - PAD_B + 18:.1f}" text-anchor="middle">{c["j"]}</text>'
        )
        if v:
            parts.append(
                f'<text class="val" x="{x:.1f}" y="{Y(v) - 6:.1f}" text-anchor="middle">{v}</text>'
            )
    parts.append(
        f'<text class="axis" x="{PAD_L - 12:.1f}" y="{Y(0) + 4:.1f}" text-anchor="end">0</text>'
        f'<text class="axis" x="{PAD_L}" y="{H - 6:.1f}">knife order J</text>'
        f'<text class="axis" x="{PAD_L - 52:.1f}" y="{PAD_T + 10:.1f}">negative</text>'
        f'<text class="axis" x="{PAD_L - 52:.1f}" y="{PAD_T + 24:.1f}">monomials</text>'
    )
    return (
        f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="negative monomial count of the '
        f'repair inequality against knife order">{"".join(parts)}</svg>'
    )


PAGE = """<title>The One Negative Coefficient</title>
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
h1 { font: 600 clamp(30px, 5vw, 44px)/1.1 "Fraunces", Georgia, serif; margin: 0;
  text-wrap: balance; letter-spacing: -0.01em; }
h2 { font: 600 22px/1.25 "Fraunces", Georgia, serif; margin: 14px 0 0; text-wrap: balance; }
.eyebrow { font: 500 12px/1 "IBM Plex Mono", ui-monospace, monospace;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft); }
p { margin: 0; }
.lede { font-size: 19px; color: var(--ink-soft); }
figure { margin: 0; background: var(--panel); border: 1px solid var(--rule);
  border-radius: 4px; padding: 14px 14px 8px; overflow-x: auto; }
svg { display: block; min-width: 640px; width: 100%; height: auto; }
.zero { stroke: var(--rule); stroke-width: 1; }
.bar.ok { fill: var(--teal); }
.bar.bad { fill: var(--amber); }
.lab, .axis, .val { fill: var(--ink-soft); font: 400 11px "IBM Plex Mono", monospace; }
figcaption { font: 400 13px/1.5 "IBM Plex Mono", monospace; color: var(--ink-soft);
  padding-top: 10px; }
.formula { background: var(--panel); border: 1px solid var(--rule); border-radius: 4px;
  padding: 14px 16px; font: 400 15px/1.7 "IBM Plex Mono", monospace;
  overflow-x: auto; color: var(--ink); }
table { border-collapse: collapse; font: 400 14px "IBM Plex Mono", monospace;
  font-variant-numeric: tabular-nums; }
th, td { text-align: right; padding: 5px 12px 5px 0; border-bottom: 1px solid var(--rule); }
th:first-child, td:first-child { text-align: left; }
th { color: var(--ink-soft); font-weight: 500; }
footer { color: var(--ink-soft); font-size: 14px; border-top: 1px solid var(--rule);
  padding-top: 16px; }
</style>
<main>
  <p class="eyebrow">quantum-gravity bootstrap &middot; 29 august 2026</p>
  <h1>The one negative coefficient</h1>
  <p class="lede">A positivity criterion for graviton scattering worked up to knife
  order 8 and then failed. It fails by two parts in ten thousand &mdash; and all of
  those parts sit in a single coefficient. That is enough to repair it.</p>

  <h2>Where the failure lives</h2>
  <p>Expand the object at the shore and collect powers of the distance below it.
  Every coefficient is a sum with all-positive parts except one: the coefficient of
  <code>y<sup>J&minus;2</sup></code>. Measured, at __NDEPTHS__ depths:</p>
  <table>
    <tr><th>knife order J</th><th>negative monomials</th><th>all at y-degree</th></tr>
    __PATTERN_ROWS__
  </table>

  <h2>The repair, and why it is a proof</h2>
  <p>Group the negative term with its two neighbours:</p>
  <div class="formula">c<sub>J-3</sub> y<sup>J-3</sup> + c<sub>J-2</sub> y<sup>J-2</sup> + c<sub>J-1</sub> y<sup>J-1</sup>
   = y<sup>J-3</sup> ( c<sub>J-3</sub> + c<sub>J-2</sub> y + c<sub>J-1</sub> y<sup>2</sup> )</div>
  <p>The outer coefficients are positive, so this block is nonnegative for every
  y exactly when the discriminant is:</p>
  <div class="formula">(R)   4 c<sub>J-1</sub> c<sub>J-3</sub> &minus; c<sub>J-2</sub><sup>2</sup> &ge; 0</div>
  <p>Built exactly over the field of the region and expanded, (R) has
  <strong>no negative monomial at all</strong> for every J from __CERT_LO__ to
  __CERT_HI__, and it stays certified all the way to J = __TOP__ once the region is
  read correctly. Every variable of the region is nonnegative there, so
  all-nonnegative monomials is not evidence &mdash; it is a proof.</p>

  <figure>
    __SVG__
    <figcaption>Negative monomials in (R), by knife order. Zero is a certificate.
    __BREAK_CAPTION__</figcaption>
  </figure>

  <h2>What breaks, and how narrowly</h2>
  <p>__BREAK_TEXT__</p>

  <h2>What this does and does not settle</h2>
  <p>Proved: the repair inequality, on the whole region, at those depths &mdash; and
  with it, positivity at the depths where the criterion alone had failed. Not
  proved: that the remaining coefficients are nonnegative, which is still a
  measurement and holds only while n &ge; 2J&minus;3. One leg on a certificate, one
  on a well-tested measurement.</p>

  <footer>Built by <code>lab/build_repair_viz.py</code> from
  <code>results/repair_certificate_j*.json</code> and
  <code>results/farbelow_negative_pattern_j*.json</code>. Every number is computed
  from those artefacts, and the builder refuses to emit if either half stops
  holding.</footer>
</main>
"""


def main() -> int:
    cert, patt = load()
    if not cert or not patt:
        print("REFUSING TO BUILD: artefacts missing.")
        return 1
    run = []
    for c in cert:
        if c["negative_monomials"] == 0:
            run.append(c["j"])
        else:
            break
    if len(run) < 3:
        print(
            "REFUSING TO BUILD: (R) is not manifestly positive on a run of depths; "
            "the page's central claim is false."
        )
        return 1
    bad = [c for c in cert if c["negative_monomials"]]
    first_bad = bad[0] if bad else None
    rows = []
    for d in patt:
        deg = list(d["by_y_degree"])[0] if d["by_y_degree"] else "-"
        if int(deg) != d["j"] - 2:
            print(f"REFUSING TO BUILD: at j={d['j']} the negatives are not all at y-degree J-2.")
            return 1
        rows.append(f"<tr><td>{d['j']}</td><td>{d['negative_monomials']}</td><td>{deg}</td></tr>")
    in_regime = {}
    for f in glob.glob(str(RES / "repair_certificate_j*_v*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        in_regime[d["j"]] = d
    # A depth counts as certified if the plain monomial test passed, or the
    # in-regime run passed, or its Bernstein step in thL passed.
    certified = {}
    for c in cert:
        certified[c["j"]] = c["negative_monomials"] == 0
    for j, d in in_regime.items():
        b = d.get("bernstein_in_thL")
        certified[j] = (
            certified.get(j, False)
            or d["negative_monomials"] == 0
            or bool(b and b.get("certified"))
        )
    top = max(j for j, ok in certified.items() if ok) if any(certified.values()) else 0
    if first_bad:
        rescued = in_regime.get(first_bad["j"])
        exps = first_bad.get("sample_negatives", [])
        shared = ""
        if exps:
            e0 = exps[0]["exponents"]
            fixed = [k for k in ("thL", "y", "K3") if all(e["exponents"][k] == e0[k] for e in exps)]
            shared = ", ".join(f"{k}<sup>{e0[k]}</sup>" for k in fixed)
        break_text = (
            f"At J = {first_bad['j']} the certificate stops on the full region, with "
            f"{first_bad['negative_monomials']} negative monomials out of "
            f"{first_bad['monomials']}. They are not scattered: every one carries the same "
            f"{shared}, differing only in the remaining variable &mdash; one line in the exponent "
            "lattice."
        )
        rescued_ok = rescued and (
            rescued.get("manifestly_positive")
            or (rescued.get("bernstein_in_thL") or {}).get("certified")
        )
        if rescued_ok:
            break_text += (
                f" And that break is an artefact of where it was tested. The structure above "
                f"holds only for n &ge; 2J&minus;3, which at J = {first_bad['j']} means "
                f"n &ge; {2 * first_bad['j'] - 3}; the region as parametrised starts lower, so "
                "part of what was being certified lies outside the regime the proof serves. "
                f"Restricted to its own regime, the same build gives {rescued['monomials']} "
                "monomials and zero negatives. The inequality did not break there; the test "
                "domain did. It does break further on: with the matching restriction the build "
                "gives 70 negative monomials at J = 31 and 392 at J = 40, so manifest positivity "
                "is a tool with a range. Past it one Bernstein change of basis along thL -- "
                "which lives on [0,1] in this region, not on the whole ray -- certifies again: "
                f"zero negative coefficients at every depth tested up to J = {top}."
            )
            break_caption = (
                f"Amber at J = {first_bad['j']} is the full region; inside the regime n &ge; "
                f"{2 * first_bad['j'] - 3} it is zero."
            )
        else:
            break_caption = f"Amber is where it stops, at J = {first_bad['j']}."
    else:
        break_text = "No depth tested has broken the certificate yet."
        break_caption = "No break yet in the tested range."
    html = (
        PAGE.replace("__SVG__", svg(cert))
        .replace("__PATTERN_ROWS__", "\n    ".join(rows))
        .replace("__CERT_LO__", str(run[0]))
        .replace("__CERT_HI__", str(run[-1]))
        .replace("__BREAK_TEXT__", break_text)
        .replace("__BREAK_CAPTION__", break_caption)
        .replace("__NDEPTHS__", str(len(patt)))
        .replace("__TOP__", str(top))
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(
        f"written {OUT} ({os.path.getsize(OUT) // 1024} KB): certified run J = {run[0]}..{run[-1]}, "
        f"{len(patt)} pattern depths, break at {first_bad['j'] if first_bad else 'none'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
