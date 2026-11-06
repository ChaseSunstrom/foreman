# Brainstorm — lens: configuration inside the TUI

- **Confirm-or-revert on every risky setting** — FEATURE — value 5 — effort M — risk low — category: safety
  Why: the pack says every setting is hand-edited TOML, and a bad theme, layout or key remap can make the app unreadable. The existing ideas cover atomic writes and last-good copies, but nothing covers the live screen.
  Done when: applying a theme, layout or key change shows "Keep? 12s" and reverts on timeout or Esc. A pty test that sends no key sees the old tui.toml restored.

- **Settings carry a "takes effect" badge** — FEATURE — value 4 — effort S — risk low — category: clarity
  Why: assumption: some settings apply instantly (theme), some need a pane rebuild, and some apply only to the next run (runner, caps). Hand-editing doesn't tell you which.
  Done when: every registry entry declares `live | restart | next-run`, and the settings view shows the badge. A test fails when an entry lacks one.

- **Scope picker on save: this run, this project, everywhere** — FEATURE — value 5 — effort M — risk med — category: layers
  Why: the pack has global code.toml, per-project `.foreman/code.toml` and env overrides. Edits inside the TUI need a target layer, and the "tighten-only" lattice must hold.
  Done when: saving prompts for a scope with the file path shown. A "this run" change leaves no file changed. A project edit that loosens a guard-related key is refused with the reason.

- **Keybinding recorder with live conflict detection** — FEATURE — value 4 — effort M — risk low — category: keys
  Why: keys come from tui.toml and there is no UI for them. You press the action's new keys, and the app shows what already uses them, including chords and terminal-reserved keys.
  Done when: rebinding to a used key shows the clash and offers swap or cancel. The binding works at once and survives a restart.

- **Modified-only view with one-key reset** — FEATURE — value 3 — effort S — risk low — category: clarity
  Why: assumption: after months of hand-editing the user can't tell which values differ from defaults.
  Done when: a filter lists only non-default keys, each with its default shown, and `r` resets one and removes it from the TOML.

- **Runner editor with a test button and masked key entry** — FEATURE — value 5 — effort M — risk med — category: runners
  Why: runners come from the built-in registry and code.toml, and the pack lists a probe plus secret handling as separate ideas. Editing them in the TUI should tie those together.
  Done when: a new endpoint runner gets a one-token probe result before it can be saved. The key is entered masked and stored as an env or keychain reference. Neither the file, the log nor the frame contains the key.

- **Layout builder on the real running frame** — FEATURE — value 4 — effort L — risk med — category: layout
  Why: layout is TOML and the extensions add panels. Moving, resizing, hiding and reordering panels with live feedback, snapped to the named breakpoints, would replace guessing.
  Done when: in edit mode, arrow keys move a panel while the app keeps running. The saved tui.toml reproduces the same golden frame at 80, 120 and 200 columns.

- **External-edit merge when tui.toml changes under the app** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: users will keep editing the file in `$EDITOR` while the app is open, and an in-app save could overwrite those edits.
  Done when: if tui.toml's mtime or hash changed since load, a save shows a three-way diff. A test that edits the file externally and then saves in-app loses neither change.

- **Conflict and dead-setting linter in the settings view** — FEATURE — value 3 — effort M — risk low — category: validation
  Why: layered config produces overridden values (project over global) and contradictory pairs (reduced motion on, shimmer theme on).
  Done when: overridden values appear struck through with the winning layer named. A seeded contradiction in a fixture shows a warning with a one-key fix.

- **Wild: A/B flicker key** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: assumption: it is hard to judge a theme or density change from memory. Holding `\` flips between the saved value and the pending one on the same frame, with no commit.
  Done when: holding the key renders the old value and releasing it renders the new one, and the golden frames of the two states differ only in the changed setting.

- **Wild: Mixing console for motion and density** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: animation speed, frame budget, contrast, density and calm level are numbers. Sliders with the run's real frames behind them make them tangible. They also tie into the existing frame-budget and "cost of this look" ideas.
  Done when: moving a slider changes the live frame immediately, shows the frame-time cost beside it, and Enter writes the value to tui.toml.

- **Wild: Config session as a replayable macro** — FEATURE — value 2 — effort M — risk low — category: profiles — wild
  Why: assumption: users change five things to get a "presentation look" and want it back with one key. Recording the session's edits as a named profile, rather than a snapshot of everything, lets it be layered over any setup.
  Done when: record, stop and name saves a profile of only the changed keys. Applying it to a different baseline changes just those keys, and undo restores them.

- **Wild: Settings changelog the app writes itself** — FEATURE — value 2 — effort S — risk low — category: observability — wild
  Why: assumption: "why did my pane change?" is answered only by guessing. Each in-app change appends a line with key, old value, new value, scope and time.
  Done when: a settings history view lists the last 50 changes and `u` undoes one. A change made through the TUI is always recorded.
