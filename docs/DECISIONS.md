# Architectural decisions and deviations from the specification

Format: date — decision — reason. Newest last.

- 2026-08-11 — **No Docker isolation**: Docker is not installed on this machine.
  Fallback per roadmap §9: upstream/AI-generated code runs in a separate uv virtual
  environment, inspected before execution, project-scoped paths only. Documented blocker;
  Docker can be added later without architecture changes.
- 2026-08-11 — **Sibling projects inspected, nothing imported**: NOVA, THE BOSS, Firebird,
  GodotGame1/GodotSchool, SuckAndStick, TokenMP are game/content projects. No reusable code
  for a scientific workbench. Reused only working patterns already encoded in the roadmap
  (append-only logs, blocker-first reporting).
- 2026-08-11 — **Donor repositories pinned, not vendored**: V1 pins commits + licenses in
  `vendor/upstream-manifest.yaml` and implements adapters with filesystem fallbacks.
  Cloning all donors is deferred until an adapter actually needs the code (roadmap §7
  "never install all donor systems blindly").
- 2026-08-11 — **PyYAML instead of ruamel for reads, ruamel for round-trip writes**:
  simplification; both are allowed by roadmap §9. (If only one ends up used, the lock
  reflects it.)
- 2026-08-11 — **SQLite index deferred**: V1 file sizes are small; JSONL/YAML scans are
  fast enough. Roadmap allows SQLite only as a rebuildable index — not needed yet.
- 2026-08-11 — **paper_pilot / paperqa / scholar_search adapters are stubs with a
  filesystem fallback in V1**: network-dependent donors are optional (roadmap §7); the
  core evidence flow works from local files. arXiv metadata fetch implemented natively
  via the public API (no key needed).
- 2026-08-28 — **Outreach artifacts are interactive 3D pages built from the exact
  engine, and this is the house style**: the founder asked for a visualisation of the
  keystone problem for children and, on seeing it, made it the standard for how this
  project shows its work ("we will share our work like this style and interactive").
  The pattern, so it can be repeated: a `lab/*_data.py` script exports the objects from
  the same exact engine the certificates use, stamped into `results/`; a
  `lab/build_*_viz.py` script injects that data into a template under `outreach/` and
  computes every number quoted in the prose from the data, so the text cannot drift
  from the picture; the builder REFUSES to emit the page if the data would make the
  page's central claim false. Published as a hosted page so it can be opened from a
  phone. First instance: `outreach/shore_of_universes.html` (the shore landscape),
  https://claude.ai/code/artifact/7e16abf9-09a6-463b-822f-b1ebc5382bd8
  Non-negotiable: an outreach page states only what the gates allow, names what is
  still open, and marks display conveniences (clamps, downsampling) as such.
