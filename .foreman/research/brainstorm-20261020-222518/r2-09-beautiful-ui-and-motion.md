# Brainstorm — lens: beautiful UI and motion

- **Project deck home screen with live cards** — FEATURE — value 5 — effort M — risk low — category: home screen
  Why: T-1330 plans a home over every project, but the ideas so far only list it; nothing designs it. Assumption: a card per project (accent from its name, queue/inbox/blocked counts as glyph chips, a one-line "now" for the active run) reads faster than a table.
  Done when: a golden frame of 5 fixture projects shows one card each with counts and a focus ring, and arrow keys move the ring between them.

- **Silent-run face: a "waiting on the CLI" scene** — FEATURE — value 5 — effort S — risk low — category: waiting states
  Why: the nixie run "just isn't doing anything" for minutes with 66k–133k-token planner calls and no visible signal. Replace the idle spinner with elapsed time, tokens in, a heartbeat strip, and the plain sentence "planner is reading, no output yet" that turns amber after 30 s.
  Done when: a fake runner that sleeps 40 s without output produces frames that show the elapsed counter, the sentence, and the amber state at 30 s, in a golden test.

- **Runner bay picker with capability lamps** — FEATURE — value 4 — effort M — risk low — category: runner picker
  Why: T-1328 finds every CLI and model, but the `m` picker is a list. Show each runner as a bay: glyph, signature hue, three lamps (found / probed OK / passed bench kind) and its launch-tax token count. Assumption: the registry exposes probe and bench results.
  Done when: with 3 fixture runners (one missing, one unprobed, one green) the picker frame shows the three lamp states distinctly and in mono mode via different glyphs.

- **Orphan-reap choreography on quit** — FEATURE — value 4 — effort S — risk low — category: motion / honesty
  Why: the planner survived the user's quit (T-1326). Show quit as a short visible sequence: each child process listed, struck through as it exits, and the terminal restores only after the count reaches zero (or after a named "still alive: pid" line).
  Done when: quitting a run with two fake children prints both pids ticking off in the exit frame, and a child that ignores TERM is named in the output.

- **Lineage ribbon for who runs whom** — FEATURE — value 4 — effort S — risk low — category: header
  Why: the user wants no duplicate Foreman when Claude Code is the worker. A header ribbon "fm code › claude (lean) › subagent" with a red break marker if a second Foreman is detected makes the nesting visible and the fix checkable.
  Done when: a worker environment containing the nesting marker renders the ribbon with the "nested Foreman suppressed" chip, and one without the suppression renders the red marker.

- **First-launch roll call as the setup wizard** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: "better config/setup" and `fm` not being on PATH. On first open, the screen animates through detected items (PATH, runners, projects, terminal capability) each landing as ✓ / ! with a one-key fix, and the result is written to the config. It doubles as `fm doctor` for the app.
  Done when: in a clean HOME with a fake claude on PATH, first launch shows the roll call, a key press fixes the PATH item, and a second launch skips straight to the home screen.

- **Cross-project attention strip** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: with many projects, "needs you" must outrank everything. A pinned strip at the top ranks blocked asks and failed runs across projects, pulses once on new arrivals, and jumps to the project on Enter.
  Done when: two fixture projects, one with a pending ask, show the ask in the strip, and Enter opens that project's run view.

- **Config explainer view with provenance chips** — FEATURE — value 4 — effort M — risk low — category: settings
  Why: "better config/setup" plus layered config. Each setting row shows its value with a chip for where it came from (default / user / project / env), and a changed value flashes and shows the old value for a moment before settling.
  Done when: a fixture with a project override renders a "project" chip on that row, and editing it updates the file atomically and the frame.

- **Wild: Harbor map of projects** — FEATURE — value 3 — effort L — risk med — category: home screen
  Why: wild. Projects are boats at a quay: busy ones bob, blocked ones show a flag, finished ones dock lightly lit. Assumption: a half-block canvas primitive (T-1314) exists to build on.
  Done when: `fm code --home harbor` renders one boat glyph per project with distinct states in a golden frame, and the standard home stays the default.

- **Wild: "Startup tax" bar that fills as the worker boots** — FEATURE — value 3 — effort S — risk low — category: motion / honesty
  Why: wild. Nested Claude loads every plugin before doing anything, which looks like a hang. Draw a loading bar segmented by what is being loaded (plugins, hooks, rules) with token counts, so the cost is visible and slimming it has a before/after picture.
  Done when: a fake worker that reports 3 load phases fills three bar segments in order, and the final frame states total input tokens before the first work token.

- **Wild: Type-ahead router preview** — FEATURE — value 4 — effort M — risk med — category: request box
  Why: wild. As the user types a request into the home box, a ghost line shows the inferred project, request kind and chosen runner ("→ nixie · fix · claude"), updating live and Tab-accepting an override.
  Done when: typing "fix the parser in nixie" against fixture projects shows the ghost line naming nixie and the fix kind before Enter, and Tab cycles the runner.

- **Run-state tab title and prompt segment** — FEATURE — value 3 — effort S — risk low — category: ambient status
  Why: the user can walk away from a silent-feeling run. The terminal title carries the state ("● nixie · step 3/5 · 41 s quiet"), and `fm code status --prompt` prints the same for a shell prompt; both are off under a setting for private screens.
  Done when: a running fixture sets the title escape with the step count, and with the setting off no title sequence is written.

- **Skeleton-to-content load for the project deck** — FEATURE — value 3 — effort S — risk low — category: loading states
  Why: scanning many projects' queues takes time, and a blank screen reads as broken like the nixie run. Show shimmering card outlines immediately, then fill each as its project is read, slowest last with a "still reading" tag.
  Done when: with a fixture project whose read is delayed 2 s, the first frame appears in under 150 ms with a skeleton card, and the card fills when the read completes.
