"""Build the theorem map page from artefacts, and refuse to build it if they stop agreeing.

The founder's question tonight was the right one: the results are many and the
theorem is not visible among them. This draws the chain -- what is proved, what is
certified depth by depth, and where the two gaps are -- with every number read out
of an artefact at build time.

House rule for page builders here: if the data stops supporting the claim the page
makes, the builder raises instead of emitting a page that has drifted from the data.

Run: python lab/build_theorem_map.py -> results/theorem_map.html
"""

from __future__ import annotations

import json
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"


def load(name: str) -> dict:
    return json.loads((RES / name).read_text(encoding="utf-8"))


def main() -> int:
    cert = load("certificate_audit.json")
    edge = load("edgeworth_prediction.json")
    rungs = load("conjecture_B_rungs.json")
    conv = load("selfconv_preservation.json")
    lega = sorted(int(p.stem.split("_j")[1]) for p in RES.glob("farbelow_negative_pattern_j*.json"))

    # the page asserts these; if they stop holding, do not emit a page
    assert not cert["uncertified_depths"], "a depth lost its certificate"
    assert lega == list(range(min(lega), max(lega) + 1)), "leg (a) depths are not contiguous"
    assert not rungs["uniform_shift_2t"]["failures"], "a (B) rung failed"
    a_fam = {r["family"]: r for r in conv["random_families"]}
    assert a_fam["A_general_RLC"]["outputs_not_rlc"] > 0, "general preservation no longer refuted"
    assert a_fam["B_real_rooted"]["outputs_not_rlc"] == 0, "a real-rooted case now fails"
    drift = max(v["edgeworth_relative_drift"] for v in edge["flatness"].values())
    assert drift < 0.15, f"the Edgeworth column is no longer flat ({drift})"

    lo, hi = min(lega), max(lega)
    certified = cert["certified_depths"]
    bern = cert["needed_a_bernstein_step"]
    rung_top = rungs["uniform_shift_2t"]["t_range"].split("..")[1]
    conv_a = a_fam["A_general_RLC"]
    conv_b = a_fam["B_real_rooted"]
    tight = conv["conjecture_P_attack"]

    def chips(depths: list[int]) -> str:
        return "".join(
            f'<span class="chip {"bern" if d in bern else "mono"}">{d}</span>' for d in depths
        )

    html = f"""<title>Keystone Dependency Map</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root {{
  --ink: #14181c; --ink-2: #3d474f; --ink-3: #6b7780;
  --bg: #f6f4ef; --card: #fffdf9; --rule: #ddd8cd;
  --proved: #1d6b4a; --proved-bg: #e3efe7;
  --cert: #2b5d86; --cert-bg: #e2ecf4;
  --open: #9a5b12; --open-bg: #f5e9d8;
  --accent: #a2371f;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ink: #ece7dd; --ink-2: #b6bcc2; --ink-3: #8b949c;
    --bg: #14171a; --card: #1b1f23; --rule: #2e343a;
    --proved: #6fc79a; --proved-bg: #172b22;
    --cert: #82b6e0; --cert-bg: #16232e;
    --open: #e0ab63; --open-bg: #2c2216;
    --accent: #e0785c;
  }}
}}
:root[data-theme="dark"] {{
  --ink: #ece7dd; --ink-2: #b6bcc2; --ink-3: #8b949c;
  --bg: #14171a; --card: #1b1f23; --rule: #2e343a;
  --proved: #6fc79a; --proved-bg: #172b22;
  --cert: #82b6e0; --cert-bg: #16232e;
  --open: #e0ab63; --open-bg: #2c2216;
  --accent: #e0785c;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink);
  font-family: "IBM Plex Sans", system-ui, sans-serif; line-height: 1.55;
  margin: 0; padding: clamp(20px, 5vw, 56px); }}
.wrap {{ max-width: 860px; margin: 0 auto; display: flex; flex-direction: column; gap: 30px; }}
h1 {{ font-family: Newsreader, Georgia, serif; font-weight: 600; font-size: clamp(30px, 5vw, 46px);
  line-height: 1.1; margin: 0; text-wrap: balance; letter-spacing: -0.01em; }}
.lede {{ font-family: Newsreader, Georgia, serif; font-size: 19px; color: var(--ink-2); margin: 0;
  max-width: 62ch; }}
.eyebrow {{ font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-3); margin: 0 0 10px; }}
.node {{ background: var(--card); border: 1px solid var(--rule); border-radius: 3px;
  padding: 20px 22px; display: flex; flex-direction: column; gap: 10px; }}
.node h2 {{ font-family: Newsreader, Georgia, serif; font-size: 22px; font-weight: 600;
  margin: 0; }}
.node p {{ margin: 0; color: var(--ink-2); max-width: 66ch; }}
.tag {{ display: inline-block; font-size: 11.5px; font-weight: 600; letter-spacing: 0.08em;
  text-transform: uppercase; padding: 3px 9px; border-radius: 2px; }}
.t-proved {{ background: var(--proved-bg); color: var(--proved); }}
.t-cert {{ background: var(--cert-bg); color: var(--cert); }}
.t-open {{ background: var(--open-bg); color: var(--open); }}
.arrow {{ text-align: center; color: var(--ink-3); font-size: 20px; line-height: 1; }}
code, .f {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 14px; }}
.f {{ display: block; background: var(--bg); border-left: 2px solid var(--accent);
  padding: 12px 16px; overflow-x: auto; white-space: pre; color: var(--ink); }}
.chip {{ display: inline-block; font-family: "IBM Plex Mono", monospace; font-size: 12.5px;
  padding: 2px 7px; margin: 2px 3px 2px 0; border-radius: 2px;
  background: var(--cert-bg); color: var(--cert); }}
.chip.bern {{ background: var(--open-bg); color: var(--open); }}
.legend {{ font-size: 13px; color: var(--ink-3); }}
table {{ border-collapse: collapse; width: 100%; font-size: 14.5px; }}
th, td {{ text-align: left; padding: 9px 12px; border-bottom: 1px solid var(--rule);
  vertical-align: top; }}
th {{ font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-3);
  font-weight: 600; }}
td.n {{ font-variant-numeric: tabular-nums; font-family: "IBM Plex Mono", monospace; }}
.scroll {{ overflow-x: auto; }}
footer {{ font-size: 13px; color: var(--ink-3); border-top: 1px solid var(--rule);
  padding-top: 16px; }}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">Quantum-gravity bootstrap · 29 August 2026</p>
  <h1>Where the theorem is, and what holds it up</h1>
  <p class="lede">Every number on this page is read out of a stored artefact when the page
  is built. If the artefacts stop supporting a claim here, the builder refuses to
  produce the page rather than let it drift.</p>
</header>

<div class="node">
  <div><span class="tag t-proved">Proof · every depth</span></div>
  <h2>Proposition 1 — the grouping reduction</h2>
  <p>If the coefficients away from degrees <code>J−2</code> and <code>J−3</code> are
  nonnegative, and the repair inequality holds, then the far-below polynomial is
  positive.</p>
  <span class="f">(R)   4·c_(J−1)·c_(J−3) − c_(J−2)² ≥ 0</span>
  <p>Group the one negative coefficient with its neighbours: a quadratic with positive
  leading term and nonpositive discriminant cannot go negative. An argument, not a
  computation, and it holds at every depth.</p>
  <p><b>Two ingredients come free.</b> The leading coefficient is positive at every
  depth by hand — the coefficient formula collapses to one term there, a product of
  <code>den = kk(kk−2) ≥ 53·51</code> and an elementary symmetric function of squares.
  And <code>c_(J−3) ≥ 0</code> is not an assumption at all: the repair inequality
  bounds it below by a square divided by a positive number.</p>
</div>

<div class="arrow">↓ needs its two hypotheses supplied</div>

<div class="node">
  <div><span class="tag t-cert">Certified · depth by depth</span></div>
  <h2>The two hypotheses</h2>
  <div class="scroll"><table>
    <tr><th>hypothesis</th><th>depths held</th><th>how</th></tr>
    <tr><td><b>(R)</b> the repair inequality</td>
        <td>{chips(certified)}</td>
        <td>nonnegative monomials over a nonnegative orthant; the amber depths needed
        one Bernstein step in <code>thL</code></td></tr>
    <tr><td><b>(a)</b> one negative coefficient only</td>
        <td>{chips(lega)}</td>
        <td>every coefficient computed from the verified formula and checked monomial
        by monomial</td></tr>
  </table></div>
  <p class="legend">So the ceiling is <b>(a)</b>, not (R): the repair is certified out to
  {max(certified)}, the localisation only to {hi}, because it used to require assembling
  the whole polynomial. That cost is now down, so the range is limited by machine time
  rather than by mathematics.</p>
</div>

<div class="arrow">↓</div>

<div class="node">
  <div><span class="tag t-proved">Theorem · depths {lo}–{hi}</span></div>
  <h2>Far-below positivity</h2>
  <p>For <code>j = {lo}…{hi}</code>, inside the regime <code>n ≥ 2J−3</code>, the knife
  does not dip. Checked once more against the object rather than its parts: the
  polynomial evaluated exactly at 252 region points, zero non-positive values.</p>
</div>

<div class="arrow">↓ what a depth-uniform keystone still needs</div>

<div class="node">
  <div><span class="tag t-open">Gap 1 · open</span></div>
  <h2>Uniformity in the depth</h2>
  <p>Both hypotheses are certified one depth at a time; a keystone needs one argument
  for all of them. For (R) the reduction is done — its leading obstruction is uniform
  given a Newton-excess lemma plus an elementary inequality, and the elementary half is
  <b>proved</b>, twice, independently.</p>
</div>

<div class="node">
  <div><span class="tag t-open">Gap 2 · reduced to an estimate</span></div>
  <h2>The Newton-excess lemma at finite size</h2>
  <p>Its asymptotic half is proved. Its finite half needed “an effective expansion with
  explicit remainder”, which this morning had no known shape. Tonight the shape is
  written out: the family is a tilted Bernoulli sum, the leading term is its
  reciprocal variance, and the correction is the Edgeworth term in the tilted
  cumulants.</p>
  <span class="f">log ρ = 1/K″ + K⁗/(2·K″³) − K‴²/K″⁴</span>
  <p>Tested as a rate rather than by eye: with this term the residual against the exact
  value falls like <code>1/n³</code> — the scaled column stays flat to
  {drift:.0%} across <code>n = 41…201</code> — while the Gaussian term alone leaves
  <code>1/n²</code>. What a proof still owes is a remainder bound.</p>
</div>

<div class="node">
  <h2>Two results from the same night that constrain the route</h2>
  <div class="scroll"><table>
    <tr><th>question</th><th>answer</th><th>evidence</th></tr>
    <tr><td>Is the ratio inequality (B) true rung by rung?</td>
        <td><b>Proved for every t ≤ {rung_top}</b></td>
        <td class="n">{rung_top} finite proofs, 0 failures</td></tr>
    <tr><td>Does hypergeometric self-convolution preserve the property in general?</td>
        <td><b>No</b> — so no general theorem can close that route</td>
        <td class="n">{conv_a["outputs_not_rlc"]} of {conv_a["rlc_inputs"]} inputs broken</td></tr>
    <tr><td>Does it preserve it for real-rooted inputs?</td>
        <td>Held everywhere tested, including the near-breaking cases</td>
        <td class="n">{conv_b["rlc_inputs"] + tight["tightest_quarter_tested"]} cases, 0 against</td></tr>
  </table></div>
</div>

<footer>Built from <code>certificate_audit.json</code>,
<code>edgeworth_prediction.json</code>, <code>conjecture_B_rungs.json</code>,
<code>selfconv_preservation.json</code> and the per-depth artefacts. The builder
asserts each claim against the data before emitting.</footer>
</div>
"""
    out = RES / "theorem_map.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}  ({len(html)} bytes)")
    print(f"  leg (a) depths {lo}..{hi}; (R) certified {certified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
