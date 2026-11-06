# Brainstorm — lens: beautiful UI and motion

- **Give every animated surface a still frame** — FEATURE — value 4 — effort S — risk low — category: motion accessibility
  Why: assumption: the charts, pet glyph and pane have no reduced-motion or `NO_COLOR` path; the pack shows only animation, never a static fallback.
  Done when: with `prefers-reduced-motion` or `NO_COLOR` set, each animated surface renders its final frame and schedules zero timers, checked by a test that counts frames.

- **Draw the diff in the order it was applied** — FEATURE — value 4 — effort M — risk low — category: motion explains change
  Why: the live demo shows diffs appearing under each call. Assumption: a replay in apply order makes the edit's reasoning readable at a glance.
  Done when: a recorded edit replays hunks in apply order within 1.5 s, and the last frame equals the static diff byte for byte.

- **Scrub a run like a film** — FEATURE — value 4 — effort M — risk med — category: history navigation
  Why: History and Today are shown as lists and charts. Assumption: one scrubber that drives the work bar, stage rail and Activity lanes together would show what the run looked like at any moment.
  Done when: moving the scrubber to time t shows the same stage, bar and lane state the journal records at t.

- **Give each status a distinct shape, not just a colour** — CLEAN — value 4 — effort S — risk low — category: legibility
  Why: T-1217 shows colour fighting the terminal theme. Assumption: colour-only state is unreadable on some themes and for colour-blind users.
  Done when: waiting, running, passed, failed and stalled are distinct in a greyscale render, checked by a test that strips colour.

- **Define colours once for web, pane, desk and mod** — CLEAN — value 4 — effort M — risk low — category: design system
  Why: T-0166 and T-1217 both come from colour and layout duplicated across surfaces. Assumption: one generated token file would end that drift.
  Done when: the token file is the only place colours are defined, and a test fails if any surface hard-codes a hex value.

- **Show a full pass as a seal and a failure as a crack** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: a check's result is currently only text, so the moment of passing has no weight. A seal stamps once on a full pass; a failing test name sits on a crack line.
  Done when: a full pass draws the seal once, a failure shows the test name on the crack, and both show as static frames under reduced motion.

- **Skeletons sized by the last run** — FEATURE — value 3 — effort S — risk low — category: loading states
  Why: empty and loading states are already on the list. Assumption: a skeleton shaped like the previous run's lanes shows the real layout before the data arrives.
  Done when: the first frame of a loading Activity lane has the previous run's lane count and widths within 20%.

- **A density dial: calm, normal, dense** — FEATURE — value 3 — effort S — risk low — category: layout
  Why: the web UI and pane show work bar, stage rail, lanes, graph, History and Today at once. Assumption: people differ in how much they want on screen.
  Done when: each density level keeps every panel reachable with one key, and the calm level hides no state.

- **Pass one run glyph between surfaces** — FEATURE — value 3 — effort M — risk low — category: cross-surface continuity
  Why: the web UI, pane, desk card and mod all show the same run. Assumption: a glyph that moves from one surface to the next shows where the work went.
  Done when: the glyph's exit on the old surface and entry on the new share one event ID in the log.

- **Cap animation frame rate under load** — PERFORMANCE — value 3 — effort S — risk low — category: motion cost
  Why: the hook bench is budgeted at 300 ms and was noisy under load. Assumption: animation shares that CPU, so it should drop to a lower frame rate when load is above 0.6 per core.
  Done when: `bench_hooks --runs 20` with animations on shows no change in the PreToolUse:Bash:script p95 beyond noise.

- **Wild: a lamp that lights the files the model read** — FEATURE — value 3 — effort L — risk med — category: provenance
  Why: wild. Assumption: a reviewer wants to see what Claude read before it edited. Read files glow faintly in the diff view and fade after the edit.
  Done when: every file in the run's read set is lit, and the set matches the read calls in the transcript.

- **Wild: a receipt that tears off the pane at close** — FEATURE — value 3 — effort S — risk low — category: close moment
  Why: wild. T-0795 is redoing close receipts. Assumption: a slip that tears away with a short motion makes the close feel finished, and the same text is saved to a file.
  Done when: the saved text equals the on-screen slip, and the tear motion finishes within 600 ms.

- **Wild: a work-bar pulse that keeps the model's tempo** — FEATURE — value 2 — effort S — risk low — category: ambient motion
  Why: wild. Assumption: a pulse matching tokens per second shows the run is alive without a number, and it stops when the run does.
  Done when: the pulse rate stays within 25% of tokens per second and stops within one second of the run ending.
