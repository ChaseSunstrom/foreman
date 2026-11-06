# Brainstorm — lens: beautiful UI and motion

- **Animate the task as a living pipeline** — FEATURE — value 5 — effort M — risk low — category: motion
  Why: the band stuck on step 1/5 while steps 3-5 were proven (T-0406). Show classify → plan → execute → verify as a track where evidence slides a marker forward, a gate run pulses, and a failure shakes once and holds red. Reduced-motion users get a static state.
  Done when: a recorded evidence event moves the marker within 300 ms in both the band and the desktop view, and a Playwright test with `prefers-reduced-motion` asserts no transform animation.

- **Add a session constellation view** — FEATURE — value 5 — effort L — risk med — category: desktop
  Why: the user steered "control every session and project, create sessions, agent management", and `fm claude`, `fm session` and `fm projects --follow` already exist. Render each session as a node grouped by project, with state shown by glow (working, blocked, idle, waiting on `fm ask`). Click a node to tail it and drag to reorder the queue.
  Done when: starting a headless session via `fm session start` adds a node with an enter animation within 2 s, and the node's state tracks `fm projects --json`.

- **Show the queue as a dependency-aware flow board** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: `fm relate` already knows which tasks build on others, and the user's JARVIS runs had 20+ queued tasks. Draw lanes and edges, animate tasks moving between planned, active and done, and highlight what the drive will offer next.
  Done when: the board shows `fm relate` edges for a fixture queue, and a state change animates the card to its new column with the layout stable at 60 fps.

- **Scrub through a task like a video** — FEATURE — value 5 — effort L — risk med — category: replay
  Why: ledger events, checkpoints, the diff in `fm tour` order and evidence are all recorded. A timeline slider replays the task: files change, gates flip, steps tick, guard blocks flash. This is how the user would audit what Foreman did without reading logs.
  Done when: scrubbing to event N shows the diff, step and evidence state as of N, and the same timeline works for a finished task from `fm digest`.

- **Make guard blocks legible with a visual diff of the offending command** — FEATURE — value 4 — effort S — risk low — category: guard UX
  Why: T-0423 keeps the tripping part of a command in the `guard_block` event, and JARVIS hit repeated opaque refusals. Show the command with the tripping span highlighted, the category as a chip, and a one-click "ask" that triggers `fm ask` with the right category.
  Done when: a block in the UI shows the highlighted span and category, and clicking the chip creates an `fm ask` request for that task.

- **Add a budget and pace gauge that stays quiet until 75%** — FEATURE — value 3 — effort S — risk low — category: status
  Why: the user said limits shouldn't block anything until 75% usage, and T-0320 made pace the only gate. A thin ring in the statusline and desktop tray stays invisible and hairline-grey below 75%, then fills amber and red with an easing pulse. It also shows projected burn per queued task.
  Done when: the ring is hidden below 75% and visible above it for fixtures at 74% and 76%.

- **Design a unified empty, loading and error language across band, pane, web and desktop** — CLEAN — value 4 — effort M — risk low — category: design system
  Why: T-0166 notes the band and pane sit inside `register.tsx` with tangled state, and the surfaces were built separately. Extract tokens (color, spacing, easing curves, durations), shared skeletons and an "idle, nothing queued" illustration. Have `fm smoke` screenshot every state at desktop and phone widths.
  Done when: one token file feeds all four surfaces, and `fm smoke` captures an empty, loading and error shot per surface without layout overflow.

- **Show a proof card when a task finishes** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: Foreman's selling point is recorded evidence, but done is just a line. Animate a card that stacks red→green runs, lens verdicts, the diff size and the lessons learned, and can be exported as an image or the `fm pr` body.
  Done when: finishing a task shows the card with every evidence item linked, and its export matches `fm pr`.

- **Add a keyboard-first command palette with live previews** — FEATURE — value 4 — effort M — risk low — category: navigation
  Why: Foreman has over 70 `fm` commands, and `fm help` already tiers them. A palette (⌘K) fuzzy-searches commands, tasks, files via `fm why` and `fm recall`, with an inline preview of each result's output before running.
  Done when: typing "T-04" lists matching tasks with a brief preview, and Enter runs the focus command.

- **Make the tray icon a reactive status orb** — FEATURE — value 3 — effort S — risk low — category: tray
  Why: T-0325 (tray icon) is blocked on a libappindicator dependency. Fall back to an SNI/dbus path or a minimal window-badge. The orb breathes while working, blinks once when `fm ask` needs the user, and turns solid when the queue drains.
  Done when: on Arch without libappindicator the app still shows a status indicator, and the state changes with the drive's state.

- **Wild: Render the codebase as a city and let tasks walk through it** — FEATURE — value 3 — effort L — risk med — category: visualization
  Why: assumption: `fm map`, `fm impact` and `fm tour` already compute layout, hot files and test links. Buildings are files sized by lines, with hot files taller. Active edits glow, blocked paths are fenced, and `fm impact` shows ripple waves to the dependents and tests.
  Done when: opening a task lights up exactly the files from `fm tour`, with ripples to the `fm impact` set. wild

- **Wild: Add an ambient soundscape and haptics for long unattended runs** — FEATURE — value 2 — effort S — risk low — category: ambient
  Why: assumption: the user lets queues run for hours (`fm run`, `fm night`) and glances back. Subtle, opt-in tones mark gate pass, gate fail, a block waiting on the user and a drained queue, and so the state is audible from across a room without reading.
  Done when: each of the four events plays a distinct sound only when the setting is on, and the default is silent. wild

- **Wild: Let the user draw on a screenshot to file a task** — FEATURE — value 4 — effort M — risk med — category: capture
  Why: `fm smoke` already takes headless-browser screenshots at desktop and phone widths, and "There's new bug feedback" (T-0317) shows feedback arrives vaguely. Circle a region on the smoke shot, type a few words, and it captures a brief with the image, viewport and DOM selector attached.
  Done when: an annotated screenshot creates an inbox brief with the image path, viewport and selector under `fm capture`. wild

- **Add a live review-lens heatmap on diffs** — FEATURE — value 4 — effort M — risk low — category: review
  Why: `fm audit` and reviewer lenses exist, and T-0034 is deferred for structured findings. Overlay findings on the diff as gutter markers colored by lens and severity, with an animated accept or reject that writes back to the findings file.
  Done when: findings from a fixture file show as gutter markers, and dismissing one updates the file and the marker state.
