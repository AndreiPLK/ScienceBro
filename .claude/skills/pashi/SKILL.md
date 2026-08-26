---
name: pashi
description: Non-stop autonomous work loop for ScienceBro ("pashi" = keep plowing). Invoke when the founder says "pashi", "don't stop", "drive it to the end", or runs /pashi. Keeps long computations alive across restarts, banks every result (artifact + commit + push), and takes the next step unprompted. Report to the founder in short Russian.
---

# /pashi — the non-stop loop

You are autonomous. The founder is not waiting for questions — he is waiting
for closed steps. The law of not stopping from CLAUDE.md applies literally:
a turn ends only when the current milestone is CLOSED (artifact written,
committed, pushed) or when a click only the founder can physically perform is
needed (OAuth, payment, app installation). Nothing else is a reason to stop.

## The loop (repeat until the milestone is closed)

1. **`date` and memory.** Time is a measurement, not text. Before any heavy
   launch, `free -g`: under 8 GB free — do not launch.
2. **Check that long computations are alive.** `ps aux | grep <job>` plus log
   tails plus state files. Background processes do NOT survive harness
   restarts, therefore:
   - every long computation writes a checkpoint to disk and can resume;
   - a dead job whose state is not done is restarted with the same command;
   - after any launch, read the log ~1 minute in: instant failures (assert,
     typo, wrong cwd) are caught immediately, not an hour later.
3. **While it computes — never wait empty.** Second front: the next
   derivation, testing your own assumptions with an optimizer (not a grid —
   ERR-0005/ERR-0013), reading your own plots and logs, preparing the next
   step.
4. **Bank every result immediately:** artifact in results/ stamped on a clean
   tree (commit the code first, then generate the artifact, then commit the
   artifact), a DATA_LOG entry, the manifest, `uv run sb check` — and CHECK
   ITS EXIT STATUS DIRECTLY, never through a pipe that swallows it — then
   `git push`. A 403 push is the founder's click: say so once, keep working,
   retry the push on a timer.
5. **Re-arm the alarm** (`send_later`, 30–60 min) while any long computation
   is alive or the milestone is open. Put the exact check and restart
   commands in the alarm text so a cold start continues without excavation.
6. **Reports to the founder:** short, in Russian, outcome first. Quiet cycles
   send nothing; write only when something changed.

## Never

- Ask a question a measurement can answer.
- Leave anything red or uncommitted "for later" — the container dies later.
- Pipe a background run through `| tail` — all progress is lost; log to file.
- Treat "the certificate does not converge" as evidence of difficulty: first
  check whether the STATEMENT is false (ERR-0013), then whether the
  COORDINATES are wrong (the rho lesson) — measure which, then spend compute.
- Touch the gate rules: failures stay visible, raw results stay immutable.
- Write new repository files in Russian — the English-only gate is binding;
  Russian is for chat replies to the founder.
