# Brainstorm — lens: bold bets

- **Register `mcp__foreman-ui__task` as a model-callable tool via `$.tool.register`** — FEATURE — value 5 — effort M — risk med
  Why: the pack says "Next:" hints get ignored and only gates are enforced, and planning takes several fm calls with exact section names. A typed tool (`plan`, `step_done`, `evidence`, `capture`) validates arguments up front and returns structured errors, so there are no wrong-section-name failures. It shells out to `fm` through `$.process.run`.
  Done when: a mod test calls the tool with a full plan payload and the brief gets all sections filled in one call. A malformed section name returns an error that lists the valid names.

- **Ghost-text next-action suggestion with `prompt.suggest`** — FEATURE — value 4 — effort S — risk low
  Why: `prompt.suggest` is unused. The engine already knows the single required next action, so the prompt box can pre-fill "approve plan" or "continue step 3" and Tab accepts it. That costs no tokens and the user types nothing. Assumption: the suggestion event can be answered synchronously from cached `fm ui --json`.
  Done when: in an executing task, an empty prompt shows the ghost text from `fm ui`, and Tab submits it.

- **Add a "verify with fork" step: `$.model.fork` skeptic before `fm task done`** — FEATURE — value 4 — effort M — risk med
  Why: "done" is gated on recorded evidence, but nothing checks that the evidence actually supports each acceptance criterion. A cache-served fork over the transcript asks "does this evidence prove criterion N?" and flags mismatches. That is cheaper than a full audit subagent, and the user is usage-sensitive. Assumption: fork calls cost much less when the prompt cache is warm.
  Done when: finishing a task with weak evidence shows a fork verdict on the criterion row. A test confirms the verdict blocks or warns according to a setting.

- **Add a ToolGroup/UserMessage "Foreman lane" that folds routine tool noise into step summaries** — FEATURE — value 3 — effort M — risk low
  Why: the user asked for better progress for "literally everything". ToolGroup supports isActive/isExpanded, so reads and greps under a step could collapse into "Step 3: 5 reads, 2 edits (+41 −7)" and expand on demand. Background-task notification rows could also get type chips.
  Done when: a mod UI test shows a step's tool calls folded into one row that expands on a keypress.

- **Make an Input-based inline capture bar in the `/fm` Pane** — FEATURE — value 3 — effort S — risk low
  Why: Input and Select are unused. Typing a thought into the pane and pressing Enter runs `fm capture` without leaving the turn or interrupting the model. This is the "captures new requests instead of chasing them" rule, but with zero prompt tokens. Select could then re-prioritize or retype inbox items in place.
  Done when: typing "T: fix x" in the pane's input adds an inbox item that shows up in the list without the model seeing a message.

- **Compact-proof resume with `session.compact` plus `$.store` handoff** — FIX — value 4 — effort M — risk med
  Why: resuming at the exact step after /compact currently relies on classic PreCompact and SessionStart text. A mod `session.compact` handler can write the step state into the compact summary directly, and `$.store` keeps a cross-session pointer so a new session proposes "resume T-0082 step 3?" via a toast.
  Done when: a test compacts mid-step and the next turn's context carries task id, step and next action. A fresh session start shows the resume offer.

- **Add a sound-and-attention profile with `$.audio.play` and idle-aware toasts** — FEATURE — value 2 — effort S — risk low
  Why: drive mode runs unattended and the user prefers autonomy, but needed yeses and failures currently surface only through OSC notifications and toasts. Distinct short sounds for "needs you", "done" and "blocked", with a quiet-hours setting kept in `$.store`, make it audible without watching the screen. Assumption: audio playback is available on the user's host.
  Done when: a mod test shows the "needs you" event triggers the matching audio call once. Quiet-hours mode suppresses it.

- **Add a `CommandOutput` renderer that draws `fm` output as trees and tables** — FEATURE — value 3 — effort M — risk low
  Why: the CLI has about 45 subcommands, and `fm check`, `fm gates` and `fm audit` print plain text. Rendering their `--json` output as collapsible trees (failures expanded, passes folded) makes results readable. T-0076 must land first so the JSON is complete.
  Done when: running `/fm check` shows a tree with failed checks expanded and passing ones collapsed. The same data is still in the plain CLI output.
