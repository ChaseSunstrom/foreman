# Brainstorm — lens: plugin parity

- **Read hook timeouts from the plugin manifest in the CLI too** — FIX — value 4 — effort S — risk low — category: hook timing
  Why: Claude Code enforces each plugin hook's timeout, but the CLI runs the same hooks with no declared deadline (assumption: the CLI path has no matching timeout). A hook that passes under the plugin can hang the CLI indefinitely.
  Done when: a hook that sleeps past its manifest timeout is killed with the same verdict on both surfaces, and the test fails if either surface lacks a deadline.

- **Replay captured Claude Code hook payloads into the CLI guard** — CLEAN — value 4 — effort M — risk low — category: hook contract
  Why: The guard is tested against hand-written inputs, not the JSON Claude Code actually sends. Real payloads from a plugin run would catch field-shape drift that the CLI tests miss.
  Done when: a payload recorded from a real plugin session produces the same allow or refuse verdict when fed to the CLI guard, and a changed field name fails the gate.

- **Ship a shared guard verdict corpus both surfaces must pass** — FEATURE — value 4 — effort M — risk low — category: guard parity
  Why: Nothing proves that a command gets the same verdict from a plugin hook and from `fm`. A single corpus of commands with expected verdicts, run through both paths, turns that claim into a test.
  Done when: one corpus file of at least 200 commands runs through both paths in CI, and any disagreement fails the gate with the command named.

- **Show the permission mode each surface assumes, and flag a mismatch** — FEATURE — value 4 — effort S — risk low — category: permission modes
  Why: The plugin inherits Claude Code's permission mode, while the CLI assumes its own bypass setting (assumption). A run started in plan mode in one surface may act differently in the other with no sign of it.
  Done when: `fm status` prints the mode each surface assumes, and a mismatch adds one warning line naming both modes.

- **Stamp each run with the surface that started it** — FEATURE — value 3 — effort S — risk low — category: surface detection
  Why: A child `fm` cannot tell whether it runs inside the plugin or from a terminal, so receipts and `fm status` cannot say which surface did the work.
  Done when: a run started from the plugin records `surface=plugin` in its journal, a terminal run records `surface=cli`, and `fm status` shows the value.

- **Let a plugin-only install complete a first task with no CLI on PATH** — FEATURE — value 5 — effort M — risk med — category: install path
  Why: Users who install only the plugin hit "fm not found" in parts of the flow, the same problem the user raised about PATH. The plugin should be complete on its own, with the CLI as an optional upgrade.
  Done when: on a clean account with only the plugin installed and no `fm` on PATH, `/foreman init` and one task through close succeed without an error.

- **Publish a feature-availability table from live probes** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: The table of which verbs work on which surface is maintained by hand and drifts. Probes already know the answer.
  Done when: the docs table is regenerated from probe output, and CI fails when the committed table differs from the regenerated one.

- **Show a parity line in the status line when the surfaces disagree on the current task** — FEATURE — value 3 — effort S — risk low — category: status surface
  Why: When the plugin and the CLI hold different views of the same task (a different stage or a different last proof), the user sees only one of them. A single line makes the mismatch visible where they already look.
  Done when: forcing the two surfaces to disagree on a task's stage makes the status line show a mismatch marker, and agreement clears it.

- **Wild: a parity duet where the two surfaces argue a request before it runs** — FEATURE — value 2 — effort L — risk med — category: cross-check
  Why: Wild: the CLI proposes a plan, the plugin critiques it in chat, and only agreement lets the task queue. Disagreements are logged as evidence, not averaged away.
  Done when: a request with a planted surface-specific difference produces a logged disagreement entry, and a request with none queues without a pause.

- **Wild: drive both surfaces from one recorded keystroke script and diff the frames** — FEATURE — value 2 — effort M — risk low — category: UI parity
  Why: Wild: the terminal UI and the plugin's `/foreman` card are rendered from one keystroke script, and the state lines in each frame are compared. Drift between the two shows up as a text diff.
  Done when: the same recorded script produces matching state lines in both frames, and a changed label on one side fails the test.

- **Wild: a parity badge in the README, computed nightly from the matrix** — CLEAN — value 2 — effort S — risk low — category: transparency
  Why: Wild: the README shows how many plugin-and-CLI matrix cells passed last night, so a visitor can see parity without reading the test suite.
  Done when: the badge's number equals the count of passing matrix cells in the most recent nightly run, and the badge goes stale visibly after 36 hours without a run.
