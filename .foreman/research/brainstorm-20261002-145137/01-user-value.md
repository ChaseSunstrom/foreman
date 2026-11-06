# Brainstorm — lens: user value

- **Suggest the next prompt as ghost text** — FEATURE — value 4 — effort S — risk low
  Why: `prompt.suggest` is unused, and every turn already ends with a computed "Next: <one required action>". Showing it as ghost text lets one keystroke accept it, which helps a user who is told not to be handed commands.
  Done when: with an active task, the prompt box shows the ghost text from `fm next --json`, Tab accepts it, and a mod test asserts it is empty when no task is active.

- **Show a "needs you" footer and prompt tail** — FEATURE — value 3 — effort S — risk low
  Why: `SessionMode` labels and the PromptHint `tail` are unused. They could show `drive · 3 queued · 1 waits on you` at all times, even when the AbovePrompt band is collapsed or the width is narrow.
  Done when: the footer shows autonomy mode and pending-approval count, and the count updates within one refresh after `fm task approve`.

- **Fold tool rows into per-step groups** — FEATURE — value 3 — effort M — risk med
  Why: `ToolGroup` is unused, and animated rows for "literally everything" will get noisy in long turns. Folding them into rows like "Step 3: 7 tools, +42 −9, 1 subagent" keeps the UI readable. Assumption: ToolGroup exposes `isActive` and `isExpanded` per group.
  Done when: a turn with 6 or more tool calls renders one group row. It stays animated while any tool in it runs, and expands on keypress.

- **Add a Haiku-written session handoff on compact and end** — FEATURE — value 4 — effort M — risk med
  Why: Foreman resumes at the exact step after /compact, but the narrative of why is lost. `session.compact` and `$.model.fork` are unused, and fork is served from the cache, so it is cheap for a user who is usage-sensitive.
  Done when: after compact, a 3-line "where we are / what's decided / what's next" note is stored in `$.store` and `fm`. It appears in the Pane, and a test checks it is capped at 400 characters.

- **Add a completion chime and desktop notification for waits on you** — FEATURE — value 2 — effort S — risk low
  Why: `$.audio.play` is unused. Drive and unattended runs (`fm run`, `fm notify`) need an audible cue when a yes is needed or a task finishes. It must be off by default and settable via `$.store`.
  Done when: the mod plays the bundled sound once per needed-yes event, never twice for the same event, and a mock-audio test confirms it respects the mute setting.

- **Add an inbox triage Pane with Input and Select** — FEATURE — value 4 — effort M — risk low
  Why: the inbox has 8 open items and the Pane only offers Start/Drop. `Input` and `Select` are unused, so the user could change an item's type, effort or priority, or edit its title and capture notes inline without leaving the session.
  Done when: editing a title or changing a type in the Pane persists via `fm`, and the edit appears in `fm queue --json`.

- **Show a per-turn context and cost burn meter** — FEATURE — value 3 — effort S — risk low
  Why: the user is usage-sensitive. `$.session.usage()` and `turns()` are unused, and the TurnDuration line has no tokens or cost yet. Adding "+12k tok · $0.08 · ctx 61%" per turn, and warning when a step exceeds its estimate, gives live budget feedback.
  Done when: each TurnDuration line shows tokens and cost matching `$.session.usage()` deltas, and a toast fires when a step crosses a configurable threshold.

- **Ship a model-callable `foreman_status` tool** — FEATURE — value 3 — effort M — risk med
  Why: `$.tool.register` is unused. The model currently learns state only through injected "Next:" text, which costs tokens every prompt. An on-demand tool would let it query state when needed, and could replace some of the always-on rule lines. Assumption: tool descriptions add less cost than the rules they replace.
  Done when: `mcp__foreman-ui__status` returns the same data as `fm state --json`. The always-on rule count drops, and a test shows the tool is registered only when the mod is active.
