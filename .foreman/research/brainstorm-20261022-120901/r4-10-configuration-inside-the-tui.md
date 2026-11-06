# Brainstorm — lens: configuration inside the TUI

- **Add a settings undo/redo stack that spans sessions** — FEATURE — value 4 — effort M — risk low — category: tui-config
  Why: the pack lists "confirm-or-revert", "config time machine" and "last-good copy", but each covers one change or a named snapshot. Nothing says Ctrl-Z/Ctrl-Y works across individual edits, or survives a restart. Assumption: edits are written as small diffs, so a journal is cheap.
  Done when: change a theme, a key and a panel, quit, relaunch, press the undo chord three times, and `tui.toml` is byte-identical to the original.

- **Show a "who set this" blame column for every setting** — FEATURE — value 4 — effort S — risk low — category: tui-config
  Why: the pack has provenance chips and a layered config. It doesn't have a history of who changed a value: the user, a profile, a pasted setup code, an auto-applied terminal profile or a release default change. Assumption: the journal above records the actor.
  Done when: focusing a row shows its last change as "you, 3 days ago", "profile: ssh" or "default changed in 1.2.51", and the history survives restart.

- **Group settings into goals, not file sections** — FEATURE — value 4 — effort M — risk low — category: tui-config
  Why: the user's stated need is a fully featured TUI config, and a flat TOML-shaped tree is hard to browse. The pack has search-first palettes but no task-shaped entry points. Goals such as "calmer", "denser", "cheaper runs", "safer overnight" and "work over ssh" would each bundle 5–10 settings with a one-line trade-off. Assumption: the schema can tag settings with goals.
  Done when: picking "cheaper runs" shows a diff of the settings it would change, with its trade-offs, and applying it changes exactly those keys.

- **Explain a setting's cost in the numbers the user cares about** — FEATURE — value 3 — effort M — risk low — category: tui-config
  Why: the pack has an "in-TUI cost of this look" meter and the render-time budget, but no per-setting effect estimate for CPU, tokens or dollars. Examples: "shimmer: +4% CPU", "verify every step: ~+30% time". Assumption: the bench and the event log can supply measured numbers per setting.
  Done when: each numeric or toggle row that has a measurement shows its delta, and a test fails if a row claims a delta without a bench entry.

- **Add a settings diff-from-defaults export as one reviewable file** — FEATURE — value 3 — effort S — risk low — category: tui-config
  Why: the pack proposes a pasteable setup code and a "modified-only view", but nothing that produces a plain, commentable patch a user can commit to a repo or send to a teammate. Assumption: the schema separates default values from user values.
  Done when: `fm code tui --config-diff` prints only non-default keys with their defaults as comments, and applying that output to a clean install reproduces the same frame.

- **Lock settings behind a reason when a repo's policy pins them** — SECURITY — value 3 — effort M — risk med — category: tui-config
  Why: the constraints say guard safety is never weakened, and the pack has a tighten-only lattice and a trust pin on `.foreman/code.toml`. Neither tells the user in the settings screen why a row is read-only or who pinned it. Assumption: policy and project layers can carry a reason string.
  Done when: a row pinned by a project or policy layer shows the layer and the reason, refuses edits in the UI, and the refusal is covered by a test.

- **Run a config "what breaks if" simulator on past runs** — FEATURE — value 4 — effort L — risk med — category: tui-config
  Why: the pack has dry-run against a recorded event stream, but only against the candidate config. It lacks a question the user would actually ask: "what would my last 20 runs have cost, or when would they have stopped, with this cap or timeout?" Assumption: event logs hold enough data to re-evaluate caps and timeouts.
  Done when: changing a cap shows "would have stopped 3 of your last 20 runs", computed from the logs, and a test pins the arithmetic on a fixture log.

- **Offer settings that adapt to what the user keeps undoing** — FEATURE — value 3 — effort M — risk med — category: tui-config
  Why: the pack has taste ledgers and a `+`/`-` learning idea for looks, but nothing for behaviour settings. If a user reverts the same change repeatedly, Foreman should stop offering it and say so. Assumption: the journal records reverts as well as edits.
  Done when: after three reverts of one suggestion, the suggestion no longer appears, and a "show hidden suggestions" row lists it.

- **Make every setting scriptable through one `fm code config` verb and a socket** — FEATURE — value 3 — effort M — risk low — category: tui-config
  Why: the pack has "verb first, settings screen second", but not a live path. A running app should accept `set` from another terminal, an editor or a tmux binding, and show the change as it would from a keypress. Assumption: the app already reads an event or command channel.
  Done when: `fm code config set theme=amber` in a second shell changes the running app's theme within one frame, and the change appears in the undo journal.

- **Wild: Ship a "config duel" that runs two configs on the same live run and lets the user vote with a key** — FEATURE — value 3 — effort L — risk med — category: tui-config — wild
  Why: assumption: the pack has side-by-side candidate rendering on a recorded stream, but not on a live run, and not as a choice that persists. Splitting the screen and pressing 1 or 2 commits the winner.
  Done when: with a live event stream, the screen shows two configs side by side, pressing a key commits one to `tui.toml`, and the loser is discarded.

- **Wild: Let a setting be a small rule with a trigger, not just a value** — FEATURE — value 4 — effort L — risk med — category: tui-config — wild
  Why: the pack has profiles keyed to the terminal and layout rules such as "show tests while verify runs". Generalising to when/then rules ("when cost passes 80% of cap, switch to minimal layout and ring the bell") makes the config a behaviour, and the settings screen could edit the rules as sentences. Assumption: the event bus exposes the run state needed for conditions.
  Done when: a rule written in the settings screen fires on the matching event in a replayed run, and invalid rules are rejected at save with a line-accurate error.

- **Wild: Turn the settings screen into a physical-feeling mixing desk with persistent presets on number keys** — FEATURE — value 2 — effort M — risk low — category: tui-config — wild
  Why: assumption: the pack has dials and a motion-density mixing console, but no way to snapshot the whole desk to keys 1–9 and recall them mid-run. A user in a hurry could jump between "recording", "overnight", "pairing" and "low-power" looks instantly.
  Done when: pressing Ctrl-Shift-3 saves the current state, pressing 3 later restores it within one frame, and the slots persist across restarts.

- **Detect config that works in the TUI but not in the headless run, and say which** — FIX — value 3 — effort M — risk low — category: tui-config
  Why: the pack shows `fm code` split across the app, `--plain`, `--json` and the foreman-ui pane, with `tui.toml` and `code.toml` as separate files. Assumption: some keys silently apply to only one surface. The settings screen should tag each row with the surfaces it affects.
  Done when: every schema key declares its surfaces, the screen shows them, and a test fails when a key is read by a surface it doesn't declare.

- **Add a first-run "config tour" that edits nothing until you press apply** — FEATURE — value 2 — effort S — risk low — category: tui-config
  Why: the user asked for a fully featured, discoverable config, and a settings screen with many rows is easy to miss. Assumption: new users won't open it unprompted. A five-step guided pass, covering theme, motion, keys, runner and caps, would show each as a preview and write nothing until the final apply.
  Done when: quitting the tour at any step leaves `tui.toml` unchanged, and completing it writes exactly the chosen keys.
