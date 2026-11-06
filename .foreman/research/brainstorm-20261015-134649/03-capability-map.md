# Brainstorm — lens: capability map

- **Pin a one-row mission strip above everything** — FEATURE — value 5 — effort M — risk low — category: layout
  Why: the user asked to "reorganize things so they're on the top". The band already holds task, stage, steps, context, chips and today/queue/inbox, but the pane buries these under the header card and a mascot. Make one shared strip (task id and title, stage rail, n/m steps, context %, mode chips, today $) that both the pane top and the band render from the same snapshot.
  Done when: with the pane open at 76 columns, the first two rows show task, stage, steps, context % and spend. A test compares the strip's text to the band's for the same `fm ui --json` fixture.

- **Float Needs-you to the top and pulse it** — FEATURE — value 5 — effort S — risk low — category: layout
  Why: approvals and red signals matter most but sit below the task card. Colour is meant to signal only here, on the active task and on failing gates. Order the cards by urgency: needs-you, then active task, then everything else collapsed.
  Done when: a snapshot with one approval waiting renders that card first. With none waiting, the card is absent and nothing pulses.

- **Draw the stage rail as a real pipeline with time-in-stage** — FEATURE — value 4 — effort M — risk low — category: task view
  Why: today's "● planning ● ready ◉ executing ○ verifying…" wraps and is noisy. Use a compact connected rail with the current stage lit. Show elapsed against the typical minutes for that TYPE/TIER from the snapshot, so a stage that runs long turns amber.
  Done when: the rail fits in 70 columns. A fixture with on_task_s above the typical time shows the amber marker.

- **Show done-when criteria as live proof chips** — FEATURE — value 5 — effort M — risk low — category: evidence
  Why: the snapshot has criteria with checked state, the evidence log and red→green proofs, but the pane only lists them. Give each criterion a chip (unproven / red / green / checked by hand). Hovering reveals the verify command and its last exit. Buttons only run `fm` commands.
  Done when: a criterion with a red→green proof renders green with a proof mark. Hover shows the verify command text.

- **Add a braille swimlane timeline of tool calls** — FEATURE — value 4 — effort L — risk med — category: graphs
  Why: the mod sees every tool call with start and end times, subagents and background shells. A Raster swimlane (main, each subagent, each shell) over the last N minutes shows what ran in parallel and where the time went, which the "more detail" request implies.
  Done when: a recorded session fixture renders one lane per actor with bars proportional to duration. The raster is blitted without a full redraw.

- **Add an ETA bar with an expected-duration marker** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: the pack has typical minutes per TYPE/TIER and on_task_s, so an "about N min left" forecast is cheap. It replaces the noisy size-legend line.
  Done when: the size legend line is gone. The bar shows elapsed against the typical time, and an overrun renders amber.

- **Chart context % with a compaction forecast** — FEATURE — value 3 — effort M — risk low — category: graphs
  Why: the context gauge is only a point value. A sparkline of context % over time, with a "compacts in about N turns" estimate, uses data the mod already sees. Assumption: the mod keeps per-turn context history, or can start recording it.
  Done when: after 5 or more turns the gauge shows a history sparkline. A fixture trending toward 100% shows a compaction warning.

- **Plot spend as a braille cumulative curve against the cap** — FEATURE — value 3 — effort M — risk low — category: graphs
  Why: Spend today currently shows only a $ figure against a cap and the top features. A cumulative curve with a cap line, and stacked segments for the top features, shows burn rate at a glance.
  Done when: a fixture at 80% of the cap shows the curve approaching the cap line and an amber state. The feature segments sum to the total.

- **Replace the hook and gate text with a health heatmap** — FEATURE — value 3 — effort M — risk low — category: health
  Why: the pack has a latency series, p95, guard blocks, hook errors and gate runs (cmd, exit, seconds). A single row of latency cells coloured against p95, plus ticks for guard blocks and a red/green cell per gate, makes it scannable.
  Done when: the Gates and Activity health lines collapse into one strip. A failing gate shows a red cell whose hover shows the command and exit code.

- **Make cards collapsible, remember which are open, and auto-collapse idle ones** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: about 15 stacked cards force scrolling at full height. Keep the active task, needs-you and fleet open, and collapse Bench, Research and Brainstorm to a one-line summary when idle. Each header row shows its counts.
  Done when: toggling a card changes its height without a flicker. The open set persists across pane close and reopen.

- **Run one frame clock only while work is live, and honour reduced motion** — PERFORMANCE — value 4 — effort S — risk low — category: motion
  Why: the constraints say calm when idle, no flicker and no wasted CPU. Today's 8 fps clock should stop when nothing runs, and everything animated should go through `blit`. Add a setting that turns animation off for accessibility.
  Done when: with no live tool call the clock does not tick, and the pane's CPU use stays near zero. With the setting off, all spinners and comets render static.

- **Add a deterministic `fm ui --demo` fixture for the showcase** — FEATURE — value 4 — effort S — risk low — category: showcase
  Why: the user wants a README video that shows the real Claude Code UI with the mod. A scripted snapshot sequence (task starts, steps tick, a red→green proof, a gate fails then passes, a close) makes the recording repeatable.
  Done when: running the demo twice produces identical frames at a fixed seed. Every card type appears at least once.

- **Wild: Turn the mascot into a state reporter with a close celebration** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: the mascot already dances. Let it look worried on a red gate, sleep when idle, and burst a raster confetti on a clean close with an A grade. The burst fires once, then the clock stops.
  Done when: the closing of a task fixture plays about 1.5 s of confetti, then no more ticks. A red gate shows the worried pose.

- **Wild: Draw a "day skyline" of closed tasks** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: the snapshot has tasks done today, closed tasks with grades, and per-type colours. A half-block skyline with one tower per closed task (height from tier, colour from grade) turns the day into a visual streak users will want to screenshot.
  Done when: N closed tasks render as N towers. Hovering one shows its title and grade.

- **Wild: Add a task replay scrubber** — FEATURE — value 3 — effort L — risk med — category: replay — wild
  Why: with tool calls, evidence and edits all timestamped, a slider could scrub back through the active task and show the step, files and proofs as they stood at that moment. This reuses the timeline data and the "fm at REF" idea.
  Done when: moving the scrubber to a past time changes the steps and criteria shown to their state then. A "live" button returns to now.
