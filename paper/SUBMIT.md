# Where to click — step by step

> **Progress (2026-08-13):** Steps 0–2 DONE. ORCID 0009-0005-5660-2603 · repo
> github.com/AndreiPLK/spacetime-verifier · release v0.1.1 · DOI 10.5281/zenodo.21915627.
>
> **Step 3 (JOSS) checked and POSTPONED — this is deliberate.** JOSS requires the
> repository to be public for MORE THAN SIX MONTHS with iterative development history and
> evidence of use by other researchers ("a single burst of commits" is explicitly out of
> scope). Our repo went public 2026-08-13, so the earliest eligible submission is
> **2027-02-13**, and only if by then the history shows ongoing commits and some external
> use. JOSS profile is already complete (email + @AndreiPLK), CI and the JOSS paper-build
> action run in the repo, so on the day of eligibility the submission is a 5-minute form.
> What to accumulate until then: iterative commits (the SMBH work will provide them),
> at least one external user or citation, and reviewer-friendly docs.

Everything below is prepared. Nothing here requires a connection, an invitation or an
endorsement. Total hands-on time: about 25 minutes, spread over three sittings.

Before you start, one 5-minute prerequisite that every later step reuses:

## 0. Get an ORCID (5 min, once, forever)

1. Open <https://orcid.org/register>
2. Register with your email. That is it — you get an ID like `0009-1234-5678-901X`.
3. Tell me the ID. I will write it into `CITATION.cff`, `paper/paper.md` and the Zenodo
   metadata, all of which currently carry a placeholder.

This is your permanent scientific identity. Journals, Zenodo and arXiv all key off it.

---

## 1. GitHub repository (10 min) — makes the work public and citable

1. Open <https://github.com/new>
2. Repository name: `sciencebro` · Description: *Independent curvature verifier and
   proof-gate workbench for machine-learned spacetimes* · **Public** · do **not** add a README
   or licence (we already have both).
3. Click **Create repository**.
4. Copy the URL it shows you (`https://github.com/<you>/sciencebro.git`) and send it to me.
   I will push, verify the push, and confirm what became public.

I do not push on my own initiative: pushing is the moment the work leaves your machine, so it
stays your decision.

## 2. Zenodo DOI (5 min) — turns the repository into a citable publication

1. Open <https://zenodo.org/> and sign in **with GitHub** (button on the login page).
2. Go to <https://zenodo.org/account/settings/github/>
3. Find `sciencebro` in the list and flip its switch **On**.
4. Back on GitHub: **Releases → Create a new release** → tag `v0.1.0` → title
   `v0.1.0 — instrument and case study` → paste the text of `RELEASE_NOTE.md` into the body →
   **Publish release**.
5. Zenodo picks it up within a minute and issues a DOI. Copy the DOI and send it to me; I will
   write it into `projects/ainstein-audit/release/ZENODO_DOI.txt`, which flips the last
   requirement of the stage-6 gate.

After this step the work is permanently archived and anyone can cite it as
*Pluzhnik, A. (2026). ScienceBro v0.1.0. Zenodo. https://doi.org/…*

## 3. JOSS submission (10 min) — a peer-reviewed journal, no connections required

The Journal of Open Source Software reviews the *software*, in public, on GitHub. Anyone may
submit; there is no endorsement and no fee. Review typically takes a few weeks and the
reviewers' comments are the useful part.

1. Read the two-minute checklist: <https://joss.readthedocs.io/en/latest/submitting.html>
2. Open <https://joss.theoj.org/papers/new>
3. Fill in: repository URL `https://github.com/AndreiPLK/spacetime-verifier`, branch `main`, version `v0.1.1`, archive DOI `10.5281/zenodo.21915627`.
4. `paper/paper.md` and `paper/paper.bib` are already in the format JOSS expects, in the
   location it looks for.
5. Submit. An editor opens a public GitHub issue; reviewers comment there; I answer every
   technical point and make the changes.

**What JOSS will and will not accept.** It accepts the *instrument* — that is what the paper is
about. It does not review the physics claims of the case study, which is correct: those are
recorded in the repository with their own limitations and are not the subject of the submission.

## 4. Optional, later: arXiv

Only worth doing if you want the audit itself to circulate as a preprint. arXiv needs a
one-time endorsement in `gr-qc` from someone who has posted there — the natural person to ask
is one of the AInstein authors, since we are already in correspondence with them. Not a blocker
for anything above. `paper/note.pdf` is the ready preprint.

---

## What is already prepared

| File | Purpose |
| --- | --- |
| `paper/note.md`, `note.html`, `note.pdf` | the note itself, ready to attach or post |
| `paper/paper.md`, `paper.bib` | JOSS submission, in JOSS format |
| `RELEASE_NOTE.md` | release scope, and an explicit list of what is *not* claimed |
| `CITATION.cff` | how to cite; needs your ORCID |
| `AI_DISCLOSURE.md` | who did what, in full |
| `projects/ainstein-audit/release/ZENODO_METADATA.json` | prefilled Zenodo fields |
| `projects/ainstein-audit/reports/RELEASE_REPORT.md` | the long-form audit report |
| `projects/ainstein-audit/proof/stage-*/` | proof packs with attestations and checksums |
| `article/one-pager.html` | the plain-language page for non-specialists |

## The honest expectation

This is a software paper plus a reproducibility note. It gives you a DOI, a citable artifact, a
public review record, and a first line in your bibliography. It is not a physics discovery, and
nothing in the prepared material claims to be one.
