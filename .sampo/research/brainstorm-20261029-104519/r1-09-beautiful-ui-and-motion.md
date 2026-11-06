# Brainstorm — lens: beautiful UI and motion

- **Ship one design-token file for every surface** — CLEAN — value 4 — effort M — risk low — category: design system
  Why: the pack shows at least four surfaces (foreman-ui pane, web UI `index.html`, `site/index.html`, Desktop) and no shared palette or spacing. Assumption: each hardcodes its own colors.
  Done when: a single `tokens.json` generates the CSS variables and the terminal 256/truecolor palette, and a test fails if any surface has a color literal not in it.

- **Make pane background follow the terminal theme** — FIX — value 4 — effort S — risk low — category: terminal UI
  Why: T-1217 is blocked because Claude Code paints the docked pane's background `#262626`, which clashes with other themes. Pick a foreground-only palette and probe the real background, so the pane never paints its own.
  Done when: a snapshot test renders the pane under light, dark and `#262626` backgrounds with no visible seams and a contrast ratio of at least 4.5.

- **Animate stage-rail transitions that explain state** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the pane has a stage rail, steps and a work bar, but the demo shows state changes as redraws. A 150 ms fill and a one-frame pulse when a step is proven would show what just changed. T-0796 already lists motion and a spinner.
  Done when: closing a step triggers a visible transition, and `FM_REDUCE_MOTION=1` or `NO_MOTION` turns it into an instant swap, verified by a frame-capture test.

- **Add designed empty, loading and error states to every web UI panel** — FEATURE — value 4 — effort M — risk low — category: states
  Why: assumption: panels such as Activity lanes, Agents graph, History and Today charts show blank space or raw text when there is no data, which is common for a new project. First-run guidance (T-0862/T-0863) has nowhere to appear.
  Done when: each panel has a fixture for empty, loading and error, all three render a distinct state with a next-step command, and a screenshot test covers them.

- **Make task and step ids clickable everywhere** — FEATURE — value 4 — effort M — risk low — category: navigation
  Why: T-0796 lists clickable ids. The recent commits cite ids like T-1998 constantly, and each is a dead string today. Use OSC 8 links in the terminal and anchors in the web UI.
  Done when: Ctrl-clicking `T-1998` in the pane opens its detail view, and the web UI deep-links to `#/task/T-1998`.

- **Show a close-out receipt card with proof marks** — FEATURE — value 5 — effort M — risk low — category: close-out
  Why: T-0795 asks for plain receipts and a landing ladder, and "prove its work with commands it actually ran" is the core promise. A card showing the test failing without the change, then passing, with durations, makes that visible and shareable.
  Done when: `fm task done` prints a boxed receipt listing the commands run, red-to-green state and time, and the same card appears in the web UI.

- **Add a keyboard command palette to the web UI** — FEATURE — value 3 — effort M — risk low — category: interaction
  Why: T-0796 lists a palette, and the project is a CLI-first tool with dozens of `fm` verbs. Typing to jump to a task, gate or lens is faster than hunting.
  Done when: Ctrl-K opens a fuzzy list of tasks and commands, Enter runs or navigates, and focus returns on Esc.

- **Pass an accessibility audit across the web UI** — FIX — value 3 — effort M — risk low — category: accessibility
  Why: assumption: charts and status colors rely on color alone. Foreman has a Today charts section, so add shape or label redundancy, focus rings, ARIA live regions for the work bar, and `prefers-reduced-motion`.
  Done when: axe reports 0 serious issues on every view, and every status has a non-color cue.

- **Make the live tree breathe with time bars that settle** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the demo shows a live tree with subagent calls and time bars. Ease bar growth, fade finished branches to a dim tone, and keep only running calls bright, so the eye lands on what is active.
  Done when: a recorded 30 s session shows finished branches at reduced contrast within 500 ms and the number of full-brightness rows never exceeds the running count.

- **Replay a finished task as a scrubbable timeline** — FEATURE — value 4 — effort L — risk med — category: replay — wild
  Why: assumption: events and timings are stored per task (T-0798 mentions replay). A web-UI slider that rewinds the plan, edits, diffs and proofs would turn the receipt into a story you can show others.
  Done when: opening a closed task shows a scrubber, and dragging it to 50% displays the files and step state as they were at that moment.

- **Render the agent graph as a living constellation** — FEATURE — value 3 — effort L — risk med — category: visualization — wild
  Why: the pane already has an Agents graph. Nodes could pulse with token rate, edges animate when work is handed off, and a finished node could dim into a star trail. The "agents of agents" work in the backlog makes the graph bigger over time.
  Done when: the web UI graph animates a live fan-out of 8 sub-agents at 60 fps and stays readable with 50 nodes.

- **Turn the demo SVG into a self-updating hero from real sessions** — FEATURE — value 3 — effort M — risk low — category: marketing — wild
  Why: `demo/live.svg` and the MP4 are hand-recorded from one task (T-1213) and age as the UI changes. Regenerating from a recorded session in CI would keep the site honest and let `fm demo` replay it in the terminal.
  Done when: CI rebuilds `demo/live.svg` from a stored session log, and the build fails if the output differs from the committed file without a flag.

- **Add a tray icon that shows the guard state at a glance** — FEATURE — value 3 — effort S — risk low — category: desktop
  Why: T-0325 is blocked only on `libappindicator-gtk3` on Arch. A three-state glyph (idle, working, needs-you) with a soft pulse, and a fallback window badge when the library is missing, would unblock it.
  Done when: the Desktop app shows the right glyph for each state, and the missing-library case degrades to a badge without a crash.

- **Split the pane out of `register.tsx` into themed components** — CLEAN — value 3 — effort M — risk med — category: foundation
  Why: T-0166 is deferred because the band and pane sit in `register.tsx` with stateful helpers. Splitting them is a prerequisite for the token file, the motion layer and the theme probe above.
  Done when: band and pane live in separate modules, `register.tsx` shrinks to wiring, and the existing pane snapshot tests pass unchanged.
