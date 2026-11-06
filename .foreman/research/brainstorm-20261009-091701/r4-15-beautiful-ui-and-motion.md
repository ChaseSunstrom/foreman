# Brainstorm — lens: beautiful UI and motion

- **Follow the agent's cursor** — FEATURE — value 4 — effort M — risk low — category: desktop UI
  Why: the user steered toward "control every session" in a Tauri app, and nothing in the pack lets them watch a session without reading its transcript. Assumption: the PostToolUse hooks already record which file, step and criterion each event touches.
  Done when: with follow mode on, the file tree, step list and criteria board auto-scroll and highlight the target of each new tool event within 300 ms, and any manual scroll pauses follow with a visible "resume follow" chip.

- **Render transcripts as structured cards** — FEATURE — value 4 — effort M — risk low — category: session view
  Why: `fm claude show` and `fm session tail` exist but print raw text. Assumption: transcripts are JSONL with typed tool events.
  Done when: opening a session in the desktop app shows prompts, tool calls, edits, guard blocks and evidence as collapsible typed cards, and a fixture session renders identically in a snapshot test.

- **Edit criteria live with a "can this fail?" button** — FEATURE — value 4 — effort M — risk med — category: briefs UI
  Why: a past task's criterion used a `-k` flag that `run.py` ignored, so it ran no tests, and a checked criterion can't be edited. Assumption: the UI can invoke `fm` verbs for a criterion's verify command.
  Done when: editing a criterion's verify command in the UI offers a Run button that streams the output, and a command that exits 0 on a deliberately broken fixture is flagged vacuous before saving.

- **Morph the queue between groupings** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: `fm relate` and `fm queue` order the same tasks differently (priority, dependency, age, type), but the UI jumps between them. Assumption: the view model exposes all the orderings.
  Done when: switching grouping animates each card to its new position (FLIP) in under 400 ms, the same card keeps its identity, and reduced-motion makes it an instant swap.

- **Deep-link every view with `foreman://`** — FEATURE — value 3 — effort S — risk low — category: navigation
  Why: refusals, notifications and `fm next` all name tasks and sessions in text the user can't click. Assumption: Tauri can register a URL scheme on Linux and macOS.
  Done when: `foreman://task/T-0432?step=3` opens the desktop app on that task and step, and `fm next` prints such a link in terminals that support hyperlinks.

- **Snapshot-test the terminal band through a real pty** — FIX — value 3 — effort M — risk low — category: terminal UI
  Why: the UI mod's band and pane have only logic tests, and T-0166 and T-0418 show the mod drifting. The "stuck on step 1/5" bug in the user's words went unseen until JARVIS hit it. Assumption: a pty plus terminal emulator can render the band to a text grid.
  Done when: a test renders the band for 6 states (idle, step 3/5, blocked, no task, narrow width, 16-color) to golden grids, and a deliberate layout change fails the diff.

- **Save and restore workspace layouts** — FEATURE — value 3 — effort S — risk low — category: desktop UI
  Why: the app manages many projects and sessions (the "control every session and project" steer). Assumption: it has panes the user can arrange.
  Done when: named layouts (for example "night watch" or "review") persist per machine, restore on launch, and a layout referencing a removed project falls back to an empty-state pane rather than erroring.

- **Show a ghost cursor in smoke recordings** (wild) — FEATURE — value 4 — effort M — risk low — category: product check
  Why: `fm smoke` drives a headless browser at desktop and phone widths but leaves only pass/fail. Assumption: Playwright-style hooks can capture click and hover coordinates.
  Done when: each smoke run writes a short clip or filmstrip with an animated cursor and click ripples, linked from the task's evidence, and a failing step is marked in red on the timeline.

- **Wipe-compare lanes** (wild) — FEATURE — value 3 — effort M — risk low — category: review
  Why: lanes live in git worktrees and the user already races builders on L tasks. Assumption: both lanes can be smoke-screenshotted at the same viewport.
  Done when: the UI shows two lane screenshots with a draggable divider, and a keyboard shortcut toggles between "A", "B" and "difference highlighted".

- **Turn token burn into ambient light** (wild) — FEATURE — value 2 — effort S — risk low — category: ambient UI
  Why: the user said budget limits shouldn't block anything until 75% usage, and a gauge that is "quiet until it matters" is already proposed. This version is a faint background hue shift rather than a widget. Assumption: pace data is available to the UI.
  Done when: window chrome stays neutral below 75% and warms gradually above it, contrast stays at WCAG AA, and a setting turns it off.

- **Keep a pulse strip of session heartbeat** (wild) — FEATURE — value 3 — effort S — risk low — category: monitoring
  Why: a drive that idles with 20+ tasks queued ("nothing else to do") was a real failure, and stalled sessions are hard to spot. Assumption: the ledger has timestamps for each event.
  Done when: each session row shows a 60-minute strip of event ticks, a gap longer than a threshold turns amber with the reason "idle: waiting on background job" or "idle: nothing queued", and clicking a gap jumps to the transcript at that time.

- **Build an offline-first shell that never blanks** — FIX — value 3 — effort M — risk low — category: loading states
  Why: `fm projects --follow` is a stream, so a dead daemon or a slow disk can leave the UI empty. Assumption: the app can cache the last view model.
  Done when: killing the follow stream leaves the last-known view visible with a "stale since 14:02" badge, shimmer skeletons appear only on first load, and the view recovers without a restart when the stream returns.

- **Preview a theme change live across surfaces** — FEATURE — value 2 — effort M — risk med — category: theming
  Why: the UI exists on the band, pane, web UI and desktop, and the user wants a "beautiful UI". Assumption: tokens are shared from one source.
  Done when: changing an accent or density setting repaints a live preview of all four surfaces from fixtures at once, and an invalid choice (contrast below 4.5:1) is rejected with the failing pair named.
