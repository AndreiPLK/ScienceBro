# vendor/

`upstream-manifest.yaml` pins every donor and upstream repository (commit SHA, license
status, what is reused, and security notes). No donor code is vendored in V1.

Rules:

- Verify a donor's license (mark it in the manifest) BEFORE copying any code.
- Local checkouts go under `vendor/checkouts/<name>/` (gitignored).
- Update pins manually and record the reason in docs/DECISIONS.md.
- Optional donors must be absent-safe: the core never depends on them.
