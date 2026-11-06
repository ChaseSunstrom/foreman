# Brainstorm — lens: bold bets

- **Add holdout checks the executor never sees** — FEATURE — value 5 — effort M — risk med
  Why: verify commands are the only oracle, and the pack lists vacuous-command lint and mutation checks as patches for Goodhart failures. Nothing tests for overfitting to the visible criteria. Assumption: a read-only reviewer can write checks and hand them to `fm` to store.
  Done when: for an M/L task, `fm task done` runs 1–2 stored holdout checks written at plan time from the brief alone, and a planted overfit solution (hard-coded output) that passes the visible criteria fails a holdout.

- **Turn pasted errors into a repro at intake** — FEATURE — value 4 — effort M — risk low
  Why: the user never runs commands and mostly pastes symptoms. Tagged-intake parsing exists, but stack traces and error text aren't resolved into files. Assumption: pasted traces show up in the UserPromptSubmit payload.
  Done when: a prompt with a Python or JS trace creates a FIX brief whose "Start here" lists the resolved frames, with a draft failing-check command in the evidence section, and no file search was needed.

- **Gate manifest and lockfile changes as supply-chain events** — SECURITY — value 4 — effort S — risk low
  Why: the security-path check forces the adversary lens, but a new or bumped dependency in `requirements`, `package.json` or a lockfile isn't treated specially. Assumption: manifests are recognizable by filename.
  Done when: a diff adding a dependency makes `fm task done` demand a one-line reason plus a pinned version, and a lockfile-only change with no manifest change is flagged.

- **Run README and docs code fences as checks** — FEATURE — value 3 — effort M — risk med
  Why: the Docs impact gate only asks whether docs were considered. It doesn't check that the documented commands still work. Assumption: fences can be opted in with a marker so nothing destructive runs.
  Done when: `fm docs check` runs marked fences in the sandbox and reports the stale one, and a task that renames a CLI flag fails done until the doc is fixed.

- **Set a blast-radius budget and abandon criteria at plan time** — FEATURE — value 4 — effort S — risk low
  Why: scope drift checks which files were touched, not how much. Recall already records the effort of similar tasks, and thrash notes only fire on repeated failures. Assumption: the plan can record an estimated file and line count.
  Done when: the brief carries "expect ≤N files / ≤M lines; abandon if …". At 2× the estimate, a note tells the model to re-plan or ask, and the note fires in a replayed trace.

- **Cap the final chat message and put the detail in the outcome report** — PERFORMANCE — value 4 — effort S — risk low
  Why: the user is sensitive to token use, and every earlier idea cuts input tokens. Output tokens and the user's own reading time are untouched. Assumption: the Stop hook can see the last assistant message length.
  Done when: at task done the chat reply is ≤5 lines pointing to the report file, and an over-budget reply gets one nudge. `fm cost` shows a drop in output tokens per finished task.

- **Rank gates by catches per token and minute, then auto-tune the profile** — CLEAN — value 3 — effort M — risk med
  Why: there are now many gates and audits, and the pack has the pieces to weigh them: `fm cost`, the guard-denial log, the rework signal, and one lean/standard/strict profile. Assumption: enough finished tasks exist for the ranking to mean something.
  Done when: `fm doctor` prints a table of each gate's catches, rework it missed and cost. It proposes demoting a gate with zero catches over N tasks, and applies the change only after a yes.
