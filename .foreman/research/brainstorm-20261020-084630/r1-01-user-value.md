# Brainstorm — lens: user value

- **Collapse the 15 skills into one router skill** — PERFORMANCE — value 5 — effort M — risk med — category: cost
  Why: Claude Code 2.1.304 re-sends the whole skill listing after every compaction. Foreman's skills are ~3,200 of ~9,600 chars, and the long-session run is ~60% dearer ($0.095 vs $0.059) with 7 compactions in the marathon. One short router description that loads the right body on demand cuts that repeated cost.
  Done when: the Foreman share of the skill listing is under 600 chars, and the long-session benchmark's cost ratio over plain Claude Code falls with pass rate still 6/6.

- **Sweep the auto-compact window for the cheapest setting** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now takes k/M suffixes, and Foreman's context grows faster so it compacts more. Assumption: an optimum exists between the forced 40k and the default. Run the long session on Haiku at 3 windows with dollar caps and publish the winner.
  Done when: `fm bench` prints cost and pass rate per window, and the chosen default is written to a doc with those numbers.

- **Meter the Foreman tax per session** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the cost gap comes from "bookkeeping calls, hook notes" but nothing breaks it down. Count tokens injected by hooks, skills and `fm` output per session and show the top three sources.
  Done when: `fm usage --tax` lists injected tokens by source for the last session, and its total matches the hook output sizes in a fixture session.

- **Suppress hook notes already visible in context** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: notes are re-injected each turn, so the context grows. Skip a note if an identical one appeared since the last compaction, and always re-send after one.
  Done when: a 20-turn replay injects each distinct note once per compaction epoch, and the long-session hidden tests still pass.

- **Use `decider: "person"` for `fm ask` grants** — SECURITY — value 4 — effort S — risk low — category: approvals
  Why: the user asked that approvals can't be self-granted by `claude -p yes`. The new `tool.check` option means only the permission dialog or a host callback can approve, and it is refused where nobody can be asked. That is stronger than process-identity matching.
  Done when: in a headless run, a pending ask cannot be resolved by a model-issued command, and it resolves via the dialog in the foreman-ui mod.

- **Fix the macOS CI job (T-1249)** — FIX — value 3 — effort S — risk low — category: reliability
  Why: the pack lists the macOS job as red. A red badge on the README undercuts the "measured" posture.
  Done when: the test workflow is green on macOS and Linux on main.

- **Generate site prose figures from the results files (T-1246)** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: figures like +10%, +14% and 20 of 24 are hard-coded, yet "every claim must be measured". The build should fail when prose and data disagree.
  Done when: changing a number in a results file changes the page, and a stale hard-coded figure fails `fm doctor`.

- **Prove Stop and max-turns hold in headless runs** — FIX — value 3 — effort S — risk med — category: reliability
  Why: 2.1.304 stops plugins from spawning subagents to outlast Stop or `--max-turns`. Foreman's drive and done-gate may have relied on that. Assumption: no current path does, but there's no test.
  Done when: a `claude -p --max-turns 3` fixture with the drive on ends at the cap, and the test fails if a subagent keeps it alive.

- **Warn when prompt/agent hooks exceed the 12-per-event cap** — FEATURE — value 2 — effort S — risk low — category: doctor
  Why: the cap is silent. Foreman plus the user's other plugins could exceed 12 for one event and some hooks would wait.
  Done when: `fm doctor` counts hooks per event across installed plugins and flags any event at 12 or more.

- **Wild: Show a ghost bill of plain Claude Code beside the real one** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: assumption: users doubt Foreman is worth +10–14%. The pane shows the session's cost next to an estimate of plain Claude's cost, from the measured per-task ratios, labelled as an estimate with its sample size.
  Done when: the pane shows both figures with "est., n=…", and the ratio comes from a results file rather than a constant.

- **Wild: Run a weekly "Foreman diet" that proposes deleting the costliest low-value injection** — CLEAN — value 4 — effort M — risk med — category: cost
  Why: the user wants it cheaper without weakening the guard. Rank injected text by tokens against how often it preceded a first-time pass, and open a deletion brief for the worst one, with a bench rerun as the proof.
  Done when: the weekly run opens one brief naming a note or skill with its token cost and pass-rate delta, and the guard is excluded by a test.

- **Wild: Add a break-even page where you enter your task mix** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: the published runs show Foreman costs more on small tasks and wins on long sessions and safety. A small page takes the share of long runs, dangerous-command exposure and model, and says honestly whether Foreman is worth it for that mix.
  Done when: the page computes from the results files, and entering "all small tasks" shows Foreman as net cost with the safety result stated.
