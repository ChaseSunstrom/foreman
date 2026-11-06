# Brainstorm — lens: approaches

- **Add a lookbook command** — FEATURE — value 4 — effort M — risk low — category: dev tooling
  Why: the "Ideas so far" list proposes many visual states (empty, error, verdict, transition) but gives no way to see them without running a real session. The user already said the TUI "looked like crap", and a complete state gallery shows that before it ships. Assumption: views are separable render functions.
  Done when: `fm code tui --lookbook` draws every component in every state (idle, running, red, green, empty, error) side by side from fixture data, with no model call, and exits 0.

- **Write looks as a stylesheet with state selectors and transitions** — FEATURE — value 4 — effort M — risk med — category: styling
  Why: the request is "not just static colors". Themes today are likely fixed color slots (assumption). A small CSS-like file (`.station.running { fg: ramp(hot); transition: 200ms }`) makes motion and color data, so users can extend them, and it avoids hardcoding each animation in Python.
  Done when: a user stylesheet changes the running-station color ramp and its fade time with no code change, and a bad selector reports its line number.

- **Ship the redesign in strangler slices behind a look flag** — CLEAN — value 3 — effort S — risk low — category: delivery
  Why: the TUI was already redesigned once after a "looks like crap" steer, and T-0166 (moving the band and pane out of register.tsx) is still deferred. Migrating one view at a time under `--look=next`, with the old look as the default and one release per slice, limits the damage of a bad redesign, and the user already allows releasing at any time.
  Done when: `--look=next` swaps exactly one named view to the new renderer, the other views are byte-identical to the old frames, and the golden test proves it.

- **Import base16, VS Code and iTerm themes** — FEATURE — value 4 — effort S — risk low — category: themes
  Why: none of the listed theme ideas let people bring a palette they already have, and the ideas that derive palettes from the terminal assume the terminal exposes its own. Assumption: themes are palette maps that an import can fill. A converter gives dozens of palettes for little work and keeps the contrast check as the gate.
  Done when: `fm code theme import FILE` converts a base16 YAML into a working theme, and the converted theme fails loading with a named reason if its text color on its background is below the contrast threshold.

- **Load animations as frame-sheet files** — FEATURE — value 3 — effort M — risk med — category: extensibility
  Why: the extension ideas cover widgets and palettes but not the motion itself. A plain-text sheet (frames, per-frame duration, loop or once, trigger event) plus a 60-line player lets people author a spinner or a closing flourish like drawing art. Assumption: there is a tick loop to hook into.
  Done when: dropping a `.fmanim` file in the config dir binds it to the "task closed" event, and a malformed sheet falls back to the built-in with a one-line note.

- **Post a look diff on every pull request** — FEATURE — value 3 — effort M — risk low — category: CI
  Why: CI exists and has been red repeatedly (several recent asks fix it). Golden frames are proposed, but nobody sees a visual change until someone reads a text diff. Rendering the changed views as SVG into a PR comment or CI artifact makes style regressions reviewable.
  Done when: a PR that changes a station glyph uploads before and after SVGs for the affected views, and a PR that changes nothing uploads none.

- **Give each model and worker a signature hue and glyph** — FEATURE — value 3 — effort S — risk low — category: identity
  Why: `fm code --worker` and `fm code bench` now run many models and CLIs, and a user glancing at the screen can't tell which one is working. A stable identity color on the header and the Gantt row, hashed from the worker name and overridable, makes it visible. Assumption: the event stream names the worker.
  Done when: two workers in one run render with different hues and glyphs in the Gantt, and the same worker gets the same pair across runs.

- **Run a sidecar renderer written in a compiled language** — FEATURE — value 3 — effort L — risk high — category: architecture
  Why: the stdlib-only Python constraint caps what animation and diff drawing can do. A small Rust or Go binary that reads the event log and draws with a real cell buffer would give smooth frames at low CPU. The cost is a build and distribution burden, which the macOS CI work shows is already heavy, so it should be optional and Python stays the fallback.
  Done when: with the binary installed `fm code tui` uses it and its frame time is lower in the bench; without the binary the Python TUI runs unchanged.

- **Offer tmux popup and status line as a render-free surface** — FEATURE — value 2 — effort M — risk low — category: reuse
  Why: users running Foreman beside Claude Code are often already in tmux. `display-popup` for the decision inbox and `status-right` for the one-line run state need no frame drawing and no animation budget. Assumption: a meaningful share of users use tmux.
  Done when: `fm code tui --tmux` sets a status-right segment showing the current station and a popup key opens the "needs you" view, and it unsets both on exit.

- **Tune motion constants automatically against measured limits** — PERFORMANCE — value 3 — effort M — risk med — category: tuning — wild
  Why: durations, easing and ramp lengths get chosen by feel. A script that sweeps them and keeps the best set under three measurable limits (contrast ratio, color changes per second, bytes per second) turns taste into constraints. This is like the hook benchmark budget, which the project already runs.
  Done when: `fm code tui --tune` writes a constants file, and the replay test shows bytes per second at or below the previous budget with no contrast failures.

- **Let `+` and `-` teach the UI what the user likes** — FEATURE — value 3 — effort M — risk med — category: personalization — wild
  Why: every proposal so far assumes one designer deciding the density and motion. A key to say "more of this" or "less of this" on the focused element, with a small local bandit adjusting density and motion per view, lets the TUI converge on the user's taste. Everything is stored in the config and never sent anywhere.
  Done when: pressing `-` five times on the Gantt lowers its motion to the calm setting and persists it, and `--forget` resets it.

- **Grow an edit-seeded Life garden while the run is idle** — FEATURE — value 2 — effort M — risk low — category: ambient — wild
  Why: the ambient ideas so far (factory floor, weather, pet) are all metaphors. A Conway grid seeded by each file the run edits and colored by that file's test status is an ambient view that only changes when there is real work, so idle stays still.
  Done when: `fm code tui --view garden` seeds one cell cluster per touched file, a red verify turns its cluster red, and the grid stops updating after 30 seconds without events.
