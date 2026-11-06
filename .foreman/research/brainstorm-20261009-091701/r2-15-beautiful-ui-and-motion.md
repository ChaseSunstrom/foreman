# Brainstorm — lens: beautiful UI and motion

- **Compile one design spec to every surface** — FEATURE — value 4 — effort M — risk low — category: design system
  Why: assumption: band (terminal), pane, web UI, Tauri desktop and tray each style state on their own. The pack lists "unified empty/loading/error language" only as a design intent. A single tokens file (colors, state glyphs, durations, easings) would compile to ANSI, CSS variables and Tauri theme values.
  Done when: changing one token in the spec changes the band, web UI and desktop output, and a test fails if any surface hardcodes a value the spec defines.

- **Gate the UI with screenshot-and-motion diffs** — FEATURE — value 5 — effort L — risk med — category: visual QA
  Why: `fm smoke` already drives a headless browser at desktop and phone sizes. Extending it to capture a frame sequence at fixed moments (before, 150 ms, settled) lets a done-gate catch broken animations, layout shift and contrast regressions, not just broken pages.
  Done when: a task that changes the UI attaches before/after frames and an axe contrast result to its evidence, and a deliberately broken transition fails `fm task done`.

- **Render every UI state from a fixture gallery** — FEATURE — value 4 — effort M — risk low — category: state coverage
  Why: T-0166 and T-0406 (band stuck on step 1/5) show stateful UI drifting from the model. A gallery generated from `fm ui --json` fixtures (empty, resumed after compact, blocked, over-budget, 20+ queued, stale data) would show every combination and feed the screenshot gate.
  Done when: `fm ui gallery` renders at least 12 named states from fixtures, and adding a view-model field with no fixture fails a test.

- **Dispatch by dragging queue cards onto sessions** — FEATURE — value 5 — effort L — risk med — category: mission control
  Why: the user steered toward "control every session and project, create sessions", and JARVIS idled with 20+ queued tasks. A board of live session tiles (activity sparkline, current step) where dropping a queued task starts a builder lane or hands it to that session would turn the idle queue into one gesture.
  Done when: in the desktop app, dragging a queued task onto a session tile makes `fm lane new` and focus happen, and the tile shows the new task within 2 s.

- **Show the guard's reasoning as an interactive parse tree** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: the pack shows repeated confusion over refusals (`fm focus …; sed -i` refused twice, rm of a symlink read as confine, `bash -lc` missed). Beyond a visual diff of the offending command, a playground that parses a typed command, animates the nodes it judged, marks the tripped category and lets the user edit and re-judge live would teach the guard's model.
  Done when: pasting `fm focus T-1; sed -i x f` highlights the focus node as the cause and shows the split form passing, using the real `fmguard` parser rather than a copy.

- **Give acceptance criteria a red-to-green board** — FEATURE — value 4 — effort M — risk low — category: proof display
  Why: evidence now moves the current step (T-0406), but criteria and steps are still text. Criteria as cards that flip from red to green with a drawer holding the verify command, its output and its timing would make "verified with recorded evidence" visible. Vacuous verifies (like the `-k a or b` that ran no tests) could show as a distinct hollow state.
  Done when: finishing a criterion animates its card and opens its recorded output, and a criterion whose verify ran zero tests renders as hollow.

- **Mark data freshness in the UI** — FEATURE — value 3 — effort S — risk low — category: loading states
  Why: assumption: hooks and `fm ui --json` can lag, and the band can be stale (T-0406 showed it lying). Dimming stale panels with a live "updated 4 s ago" stamp, and a soft shimmer only while a refresh is in flight, makes wrong-looking state honest.
  Done when: stopping the data source dims the pane after a threshold and shows the age, and it recovers without a flash when data returns.

- **Swipe through pending asks and decisions as a deck** — FEATURE — value 4 — effort M — risk low — category: approvals
  Why: `fm ask` grants, deferred items and "needs you" blocks currently wait on typed replies. A card deck on desktop or phone (approve, decline, defer; each card shows the exact command and its category) clears a morning backlog in seconds. Signed device approvals would sit behind it.
  Done when: three pending asks can be resolved from the deck and each outcome appears in the ledger with the same text a typed answer would produce.

- **Give each project a generated identity across all surfaces** — FEATURE — value 3 — effort S — risk low — category: identity
  Why: the user runs many projects at once (JARVIS, Foreman, others) and sessions. A stable color and glyph per project, used in the band, tray icon, notifications and session tiles, prevents acting in the wrong project.
  Done when: a notification, tray state and band for the same project share one color and glyph, and two projects never get colors under a minimum contrast distance.

- **Wild: Stream a builder lane's edits as a live code morph** — FEATURE — value 4 — effort L — risk med — category: live diff
  Why: wild. Instead of reading a final diff, watch the lane's files change in place with a gutter that lights up per hunk as the linked tests from `fm impact` pass or fail. Reviewing starts while the work is happening.
  Done when: during a lane run, the desktop shows hunks appearing as they are written, with each hunk's linked test status updating in the gutter.

- **Wild: Float a pill that expands only when you're needed** — FEATURE — value 4 — effort M — risk low — category: ambient desktop
  Why: wild. A small always-on-top pill (like a phone's Dynamic Island) shows the queue's pulse while idle, expands into the question when a task blocks or an ask arrives, and collapses after an answer. This replaces the tray orb for the moments that matter.
  Done when: a blocked task makes the pill expand with the question and its approve/decline actions, and answering it collapses the pill within 1 s.

- **Wild: Make the queue a physical gravity field** — FEATURE — value 3 — effort M — risk low — category: queue visualization
  Why: wild. `fm relate` already knows which tasks build on others. A force layout where related tasks attract, blocked ones sag, and finishing one lets its dependents drift forward would show which task is holding up the rest.
  Done when: tasks that `fm relate` groups appear as clusters, and closing a blocking task visibly releases its dependents.

- **Honor reduced motion and screen readers everywhere** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: assumption: the planned smooth animations (Tauri request) have no fallback. Every transition would need a reduced-motion variant, plain-text band mode for narrow terminals, and live-region announcements of state changes ("step 3 of 5 proven"), so the motion explains state without being the only signal.
  Done when: with reduced motion set, no transition exceeds a fade, and a screen-reader test hears each step change announced once.
