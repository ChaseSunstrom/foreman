# Brainstorm — lens: capability map

- **Browse past runs like a session picker** — FEATURE — value 4 — effort M — risk low — category: history
  Why: the pack covers replaying one run, but nothing for finding it. Foreman keeps many tasks and bench runs, and lazygit and `claude --resume` both put a list first. Assumption: run logs are already stored per task.
  Done when: `fm code tui --runs` lists past runs with outcome, cost, duration and task id, filters by typing, and Enter opens a replay.

- **Explore tests as a tree with rerun-one** — FEATURE — value 4 — effort M — risk low — category: verify
  Why: verify runs only appear as check chips. A pytest-style tree (module, test, status, time) with `r` to rerun the failing test fits the "finish names a red step" work (1.2.43) and the `run.py` unknown-name error.
  Done when: after a red verify, the Tests view lists each failing test and `r` reruns only that one, updating its chip.

- **Hand off to $EDITOR at the exact line** — FEATURE — value 4 — effort S — risk low — category: integration
  Why: diffs and guard verdicts name files, but a hunk can't be opened where it happened. Add `e` to open `$EDITOR +line file`, with OSC 8 `file://` links as the fallback. This extends the clickable-ids idea to the editor.
  Done when: pressing `e` on a diff hunk opens the editor at that hunk's first line and returns to the TUI on exit.

- **Show the lease and lock lane** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: T-1294 made a worker's edits lease as the run's, and the judge keeps what is leased. A lane showing which files are leased, by whom and since when makes that visible.
  Done when: editing a file in a worker run adds a row in the Leases lane that clears when the lease releases.

- **Review and edit the plan before the run starts** — FEATURE — value 4 — effort M — risk med — category: control
  Why: Foreman's premise is plan before edit, yet the TUI only shows the plan. Let the user reorder or skip steps and add criteria at a gate. This is deeper than editing the queue. Assumption: the harness can pause after planning.
  Done when: with `--review-plan`, the run halts at the plan, an edit is saved, and the harness executes the edited step list.

- **Surface the worker's process tree with kill** — FEATURE — value 3 — effort M — risk med — category: ops
  Why: reaper and macOS fixes in recent commits show child processes matter. An htop-style tree with CPU, memory and age, plus a confirmed kill key, covers hung verify commands.
  Done when: a sleeping child shows in the Processes view, and a confirmed `k` kills it and the run logs the event.

- **Import community themes (base16, Gogh, VS Code JSON)** — FEATURE — value 3 — effort S — risk low — category: themes
  Why: the idea list has a theme engine and a gallery but only user-written files. Importers give hundreds of palettes at once, with the existing contrast check applied on import.
  Done when: `fm code theme import base16.yaml` produces a theme that loads, passes the contrast check, or says which role failed.

- **Add Kitty keyboard protocol, focus events and vim/emacs presets** — FEATURE — value 3 — effort M — risk med — category: input
  Why: the plan lists keybindings and a palette but not key disambiguation (Shift-Enter, Ctrl-I vs Tab). Focus events also give a reliable animation pause when the pane is unfocused. Assumption: the TUI reads raw input itself.
  Done when: in a Kitty-protocol terminal Shift-Enter and Tab are distinct keys, and losing focus stops the frame clock.

- **Jump between marks and annotate moments** — FEATURE — value 3 — effort S — risk low — category: navigation
  Why: search and filter exist, but long runs need `n`/`N` to hop between refusals, red verifies and user bookmarks. Notes saved to the log feed post-mortems.
  Done when: `m` bookmarks the current event, `]` jumps to the next refusal or bookmark, and notes appear on replay.

- **Show the model's bench grade in the header** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: `fm code bench` (T-1215) grades a model on five seeded tasks, but that result never reaches the run view. Showing "model X: 4/5 seeded" with its cost per task sets expectations and supports the duel story.
  Done when: a run using a benched model shows its last grade in the header, and an unbenched one shows "unbenched".

- **Send desktop notifications with approve/deny buttons** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the plan has "needs you" and the bell. A native `notify-send --action` that answers the decision inbox works from another window. It stays off by default and local-only.
  Done when: a pending decision raises a notification, and clicking Approve resumes the run.

- **Diff two runs of one task to find where they diverged** — FEATURE — value 4 — effort M — risk low — category: analysis — wild
  Why: the bench runs each task N times, and "Where Foreman loses" (T-1261) needs explanations. Align two event logs and highlight the first differing tool call, station time and verdict.
  Done when: `fm code tui --diff RUN_A RUN_B` opens at the first event where the runs differ, with a station-time comparison.

- **Add a raw tap pane for the worker's own screen** — FEATURE — value 3 — effort M — risk med — category: debug — wild
  Why: a worker CLI's native UI is hidden behind Foreman's picture. A toggle that shows the raw PTY output in an overlay lets the user check the picture against the worker itself.
  Done when: pressing `~` shows the worker's raw terminal output and pressing it again returns to the composed view without disturbing the worker.

- **Wire a physical kill switch and approve button** — FEATURE — value 2 — effort S — risk med — category: hardware — wild
  Why: unattended runs have a dollar cap, but the nearest stop is a keystroke. Map a USB pedal, macro-pad key or MIDI pad through evdev to pause, approve or abort, local only. Assumption: user has a device.
  Done when: a configured key press pauses a running harness within one second and the header shows "paused by device".

- **Play the day back as a match-report reel** — FEATURE — value 3 — effort M — risk low — category: reporting — wild
  Why: the pack covers per-run receipts and the shift report as text. A 30-second auto-cut of the day's runs, showing each task's station track and verdict stamps, makes a shareable summary that exports as an SVG. Assumption: replay and the SVG export exist first.
  Done when: `fm code tui --reel today` plays every closed task from today in sequence and exports the same as one SVG.
