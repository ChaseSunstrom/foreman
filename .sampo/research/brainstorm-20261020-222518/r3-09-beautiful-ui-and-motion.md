# Brainstorm — lens: beautiful UI and motion

- **Morph a project card into its run screen** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: T-1330 makes `fm code` a home over many projects, but opening a run is a hard cut, so you lose where you were. Assumption: the renderer's tween clock can interpolate rectangles.
  Done when: a golden-frame test shows frames 0, mid and last of a card's rect growing to full screen, and Esc plays it in reverse back onto the same card.

- **Slide drawers over the run, not full-screen views** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: the user hit the "TUI looked like crap" problem, and the d, t and h keys swap whole views. Assumption: a drawer keeps the track and "now" line visible beside the diff or thoughts.
  Done when: pressing d slides a diff drawer over the right 40% in 6 frames, the station track stays drawn, and a golden frame at 100 columns proves it.

- **Show a typed-ahead request as resolved chips** — FEATURE — value 4 — effort M — risk med — category: input
  Why: the user says "I shouldn't even need to say anything" and hit the wrong-directory run in nixie. Assumption: the request box can tokenize against project names, runner names and files.
  Done when: typing `fix the parser in nixie with codex` renders project, runner and file chips under the box, each in its own colour, and Enter with an unresolved chip is refused inline.

- **Draw the queue as a dependency graph with flowing edges** — FEATURE — value 3 — effort M — risk low — category: queue view
  Why: the open work is full of "blocked" and "deferred" tasks (T-0325, T-0335, T-1207) that a flat list can't relate. Assumption: task blocked-by data is exposed.
  Done when: `fm code` home shows nodes with edges, and a task flipping from blocked to ready sends a light along its edges, shown in two golden frames.

- **Add a transcript minimap scrollbar** — FEATURE — value 3 — effort S — risk low — category: navigation
  Why: long runs (66k–133k tokens per call) mean the transcript gets deep. Assumption: events carry a kind (guard, verify, edit, thought).
  Done when: the right edge shows a one-column strip coloured by event kind with a viewport marker, and clicking or pressing `[` and `]` jumps to the next red event.

- **Paste a folder path to adopt a project** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the user started a run in ~/projects/nixie without the TUI knowing the project. Assumption: bracketed paste is already handled as data.
  Done when: pasting an existing directory path on the home screen adds a card that slides in with a "new" shimmer, and a non-directory paste is ignored.

- **Fold the breadcrumb into a morphing header path** — FEATURE — value 3 — effort S — risk low — category: wayfinding
  Why: with many projects, runners and tasks, "where am I and who is running this" gets lost. Assumption: the header has room for one line.
  Done when: the header reads `nixie › T-1330 › step 3 · claude` and, on a change, only the changed segment cross-fades (golden frames show the others unchanged).

- **Use the full width on big monitors** — FEATURE — value 2 — effort M — risk low — category: layout
  Why: the existing breakpoints only go down, to a docked pane and a one-line mode. Assumption: the user also uses a wide terminal.
  Done when: at 220 columns or wider, the home shows a third column (the across-projects activity feed) and golden frames at 80, 140 and 220 columns each lay out cleanly.

- **Show inline screenshots when the task is about UI (wild)** — FEATURE — value 3 — effort L — risk med — category: graphics
  Why: assumption: the user's projects include web UIs, and a diff alone doesn't show whether they look right. Assumption: kitty or sixel graphics are available and a headless browser can be run.
  Done when: on a kitty-capable terminal, a verify step that produces a screenshot shows before and after side by side in the done receipt, and other terminals get a half-block rendering instead.

- **Send a runner to the pit lane when rate-limited (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the user runs several CLIs and hits usage limits. A silent wait looks like "it just isn't doing anything".
  Done when: a lane paused for a limit shows a slowed-down animation, a countdown to the reset time and the line "waiting on claude's limit", and it resumes with a flash when the clock hits zero.

- **Show a shared "now" spotlight across all projects (wild)** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: with several lanes running, the user needs to know which one wants them. Assumption: lane state is readable from the event logs.
  Done when: the home dims all lanes except the one needing attention or just changed, and the spotlight moves with an eased slide when another lane takes over.

- **Give errors one three-row face: happened, did, next** — FEATURE — value 4 — effort S — risk low — category: error states
  Why: the planner failures and the orphaned planner left the user with silence, not an explanation. Assumption: each failure class maps to a "Next:" command.
  Done when: all five failure classes render the same card with its "Next:" command copyable by one key, and a lint fails any new error path without one.

- **Pick the whole look from a preview strip of live frames (wild)** — FEATURE — value 2 — effort M — risk low — category: theming
  Why: the many themes and the gallery idea show choice is wanted, but a picker on static swatches doesn't show motion. Assumption: the renderer can run a miniature scene per theme.
  Done when: the picker shows four small scenes (idle, running, red, closed) per theme, each playing in place, and Enter applies the choice to config atomically.
