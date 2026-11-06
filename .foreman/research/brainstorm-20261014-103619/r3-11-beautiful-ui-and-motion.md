# Brainstorm — lens: beautiful UI and motion

- **Freeze the band's geometry** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: assumption: the band and statusline redraw on every state change, and counters like "T-0754", "12m" and "3/7" change width as they tick, which causes reflow flicker. Tabular, fixed-width fields with a stable column budget make the band readable at a glance.
  Done when: a test renders the band across 500 generated states (task ids, step counts, durations, long titles) at 80, 100 and 140 columns, and every state yields the same line count, with fixed-field offsets unchanged.

- **Report step progress through OSC 9;4 and the terminal title** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: assumption: terminals that support OSC 9;4 (Ghostty, iTerm2, Windows Terminal, kitty) show native tab or taskbar progress, which the user can see while in another window. The user complained that Foreman "sits idle" and doesn't update steps, and a visible native progress bar makes both obvious. Yellow means waiting on the user, red means blocked, and the bar clears on done.
  Done when: a pty test captures the exact OSC 9;4 sequences emitted for start, step advance, ask-pending and done, and unsupported terminals (`TERM=dumb`, no TTY) receive nothing.

- **Inherit the host's theme and terminal background** — FEATURE — value 3 — effort M — risk low — category: theming
  Why: assumption: the band, pane and mod use a fixed palette. Claude Code has dark, light, colorblind and ANSI themes plus `NO_COLOR`/`COLORFGBG`, and a palette that ignores them is unreadable on some setups. A single resolver would map the host theme to Foreman's semantic colors for the band, statusline and mod.
  Done when: rendering the same state under dark, light, daltonized and `NO_COLOR` produces four distinct outputs, and `NO_COLOR` output contains no escape sequences.

- **Contrast-test every palette pair in CI** — CLEAN — value 3 — effort S — risk low — category: accessibility
  Why: assumption: no automated check exists for color legibility. Foreman uses color for state (ok, warn, block), and a failing pair means the state is invisible to some users.
  Done when: `fm doctor` computes the WCAG contrast of every foreground/background pair in each theme and fails the release gate when any text pair is below 4.5:1 (3:1 for large glyphs), naming the offending pair.

- **Make every T-id and file:line an OSC 8 link** — FEATURE — value 3 — effort S — risk low — category: terminal UI
  Why: close-outs, the band and refusal messages constantly cite `T-0754` and paths like `file_path:line_number`, which are plain text today. Clickable links turn each reference into a one-click jump to the brief, the Artifact card or the editor. Terminals without OSC 8 show plain text.
  Done when: a captured close-out contains OSC 8 sequences around each task id and path, and the same output piped to a file (non-TTY) contains none.

- **Give Artifact pages a live title and favicon ring** — FEATURE — value 3 — effort S — risk low — category: Artifact
  Why: assumption: an Artifact cockpit is a browser tab the user will leave open and glance at. Rendering `document.title` as "3/7 · needs you" and a canvas favicon ring (green running, amber waiting, red blocked) makes the tab itself a status light.
  Done when: updating the page's state data changes `document.title` and the favicon data URL within one refresh, and a unit test asserts the title string for running, waiting, blocked and done.

- **Highlight only the cells that changed** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: Artifact and pane refreshes repaint wholesale, so the user can't tell what moved. A keyed diff that fades a 600ms highlight on changed cells, and skips it under `prefers-reduced-motion`, makes updates explain themselves.
  Done when: a DOM test updates one task's step and shows exactly one element gets the highlight class, and none do when reduced motion is set.

- **Render all `fm` output through one table and truncation engine** — CLEAN — value 3 — effort M — risk med — category: CLI design
  Why: assumption: with 73 skills and many commands, tables, id columns and long titles are likely formatted ad hoc, so wrapping differs by command. One renderer would own column priority, middle-ellipsis for paths, width detection and plain output when not a TTY.
  Done when: the ten most-used commands all call the renderer, and a snapshot test at 60, 80 and 120 columns shows no line exceeds the width and ids are never truncated.

- **Show stage-named progress on slow `fm` commands** — FEATURE — value 2 — effort S — risk low — category: CLI design
  Why: assumption: commands such as `fm doctor`, `fm map` and `fm ideas` can run for seconds with no output, which looks like a hang. A single in-place line showing the current stage ("indexing 341 files", "running gates 2/5") appears after 300ms and is replaced by the result.
  Done when: a pty test of a command with an injected 2s delay shows a stage line that is overwritten in place, and a non-TTY run prints only the final result.

- **Show a context-aware key legend in the pane** — FEATURE — value 2 — effort S — risk low — category: pane UI
  Why: assumption: the pane is keyboard-driven and the available keys differ by selection (task, ask, lane). A one-line legend that changes with the focused item, plus `?` for the full map, removes guessing.
  Done when: a pane test shows a different legend for each of task, ask and lane focus, and `?` lists every bound key.

- **Wild: Shift the palette from midnight to dawn over a night run** — FEATURE — value 2 — effort M — risk low — category: ambient UI
  Why: wild; assumption: `fm night` runs unattended while the user sleeps. The Artifact and desktop window slowly warm from deep blue to dawn gold as the queue drains, so the first glance in the morning reads "finished" or "stuck" (it freezes cold when stalled) without reading anything.
  Done when: rendering the cockpit at 0%, 50% and 100% of a fixture queue yields three different hue values, and a stalled queue (no progress for 30 minutes) renders the frozen cold palette.

- **Wild: Reveal the finished product as criteria turn green** — FEATURE — value 3 — effort M — risk med — category: Artifact
  Why: wild; assumption: `fm smoke` already produces screenshots for UI tasks. The Artifact shows the "after" screenshot blurred and desaturated, and each acceptance criterion that goes green sharpens one band of it, so progress is visible as an image coming into focus. The last step is full resolution beside the "before".
  Done when: a fixture task with 4 criteria renders blur radii that step down 4 times as criteria pass, and zero criteria passed renders the maximum blur.

- **Wild: Generate a skyline poster for each release** — FEATURE — value 2 — effort M — risk low — category: releases
  Why: wild; assumption: releases like 1.2.25 to 1.2.27 are announced with a task-id list. Release notes become a deterministic SVG poster where each milestone is a building whose height is its diff size and whose windows are its criteria, attached to the GitHub release and shown in the Artifact.
  Done when: `release.py --poster` writes an SVG for 1.2.27, the same inputs produce a byte-identical file, and the file contains one building per milestone listed in the changelog.
