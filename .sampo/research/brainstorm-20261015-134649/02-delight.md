# Brainstorm — lens: delight

- **Make the stage rail a living pipeline** — FEATURE — value 5 — effort M — risk low — category: task card
  Why: the user asked for better visuals for "tasks things going on"; today the stage list is "● planning ● ready ◉ executing ○ verifying…" and the size legend line is noisy.
  Done when: the pane shows capture→record as one connected rail drawn in a Raster; the current stage glows, finished stages are solid, and a transition between stages plays a short sweep (≤400 ms) then goes still.

- **Draw steps as a segmented ribbon with a travelling pulse** — FEATURE — value 5 — effort M — risk low — category: progress
  Why: the steps bar n/m is a plain bar with a comet; the user wants "super improve" animations.
  Done when: each step is a ribbon segment (done solid, current shimmering, pending dim), with the step title shown on hover. When nothing is running, no frame clock ticks.

- **Add a "Now" hero strip at the top of the pane** — FEATURE — value 5 — effort M — risk low — category: layout
  Why: the user said "reorganize things so they're on the top". Assumption: the top should answer "what is happening and what do you need from me" at a glance.
  Done when: the first 4 rows of the pane hold the task title, stage, current step, elapsed time versus typical minutes for the TYPE/TIER, and a Needs-you badge when approvals wait. Everything else sits below.

- **Show an ETA arc against the typical minutes for the type and tier** — FEATURE — value 4 — effort M — risk low — category: graphs
  Why: the snapshot has on_task_s and typical minutes per TYPE/TIER, but they aren't visualised ("more detail maybe").
  Done when: a thin gauge fills as on_task_s approaches the typical time and turns amber past 1.5×; hovering reveals the numbers.

- **Replace the latency sparkline with a braille hook-health chart** — FEATURE — value 4 — effort M — risk low — category: graphs
  Why: the latency series and the hook p95 are in the snapshot, and Raster supports braille 2×4 dots for finer resolution.
  Done when: Activity shows a braille line with a p95 marker and a red dot for each hook error, readable at 70 columns.

- **Collapse idle cards into a one-line "calm" row** — CLEAN — value 4 — effort S — risk low — category: layout
  Why: the pane is a long column of cards (Bench, Research, Brainstorm and others), and the constraint is "calm when idle". Assumption: empty cards waste the top of the pane.
  Done when: any card with no data collapses to a single dim line, and the active task and Needs-you stay expanded.

- **Draw the session as a swim-lane timeline** — FEATURE — value 4 — effort L — risk med — category: activity
  Why: the mod sees every tool call with start and end times, plus subagents and background shells. Today they are separate lists.
  Done when: one Raster lane chart shows tool calls, subagents and shells over the last N minutes, with a hover tooltip naming each bar.

- **Play a red→green evidence moment** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Foreman's core is red→green proofs, but they are logged quietly.
  Done when: when a verify command flips from failing to passing, the criterion's checkbox plays a one-second fill with a brief glow, and nothing animates afterwards.

- **Make the mascot reflect real state** — FEATURE — value 3 — effort S — risk low — category: mascot
  Why: the mascot only dances today. Assumption: the mascot can read the snapshot.
  Done when: the mascot shows distinct poses for idle, working, waiting-on-you, gate failing and all-done, and sits still when idle.

- **Add a closing ceremony with a grade** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: closed tasks have a grade and lenses, but closing is silent.
  Done when: on close, a brief card shows the grade, the criteria proven and the time versus typical, then settles into the "✓ n today" counter.

- **Wild: turn the day into a skyline** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: wild. Tasks done today are a number; the user posts showcase material (README and demo requests).
  Done when: a half-block Raster strip draws one building per closed task today, with height set by tier and colour by type, plus a lit window per criterion, and it is screenshot-worthy for the README.

- **Wild: show a heartbeat monitor for the fleet** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. The fleet has sessions with task and context %, and today they sit in a list.
  Done when: each session draws an ECG-style line whose pulse rate follows its tool-call rate, flatlines when it is wedged, and shows its context % as a fill.

- **Wild: add a "replay the task" scrubber for demo recording** — FEATURE — value 4 — effort L — risk med — category: wild
  Why: wild. The user wants a showcase video of the real Claude Code UI with the mod, and recording real runs is slow.
  Done when: a command replays a closed task's recorded steps, tool calls and evidence through the band and pane at adjustable speed, so a demo can be recorded deterministically.

- **Add a theme and density setting** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: some users want denser output at 70 columns, and muted-grey-plus-signal colour needs a consistent palette.
  Done when: a compact/comfortable toggle and one shared palette module drive every card and the band, with colour used only where it signals.
