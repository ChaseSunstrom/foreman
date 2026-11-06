# Brainstorm — lens: bold bets

- **Close the Bash blind spot with tool.call diffing** — FEATURE — value 5 — effort M — risk med
  Why: Known limitation: Bash edits are invisible to scope/tripwires. A mod's tool.call can wrap every Bash call: snapshot `git status`/mtime via `$.fs`/`$.process.run` before, `await next(e)` and diff after, then feed the touched files into the task's scope and tripwire checks.
  Done when: a task whose Bash command (`sed -i`, `mv`) edits an out-of-scope file shows up in `fm gates` as scope drift, with a test in `claude plugin test`.

- **Fork-based verifier that reviews evidence before "done"** — FEATURE — value 5 — effort M — risk med
  Why: Gates only check that evidence is recorded, not that it supports the criterion. `$.model.fork` can ask a question over the session transcript, reusing the prompt cache so it is cheap, e.g. "does this evidence prove AC-2?". The result is advisory, recorded as a ledger entry, and blocks only on an explicit contradiction.
  Done when: finishing a task with evidence that is unrelated to its criterion yields a flagged verdict in `fm task show`, and a matching one passes silently.

- **Add a replayable session ledger with time-travel in a Pane** — FEATURE — value 4 — effort L — risk low
  Why: The ledger, tool timeline and events already exist, but they are only viewable live. A Pane scrubber could step through a past task (steps, tool calls, evidence, gates) and `fm why` could cite it. Assumption: the ledger has timestamps and tool events persisted per task.
  Done when: `fm replay T-00XX --json` emits an ordered event stream, and the Pane can scrub it and show the stage at each point.

- **Make a self-tuning gate budget from outcomes** — FEATURE — value 4 — effort M — risk med
  Why: The user is usage-sensitive, and the pack shows ~62 rule lines plus a "Next:" on every prompt. Track which hints and gates were ignored or overridden and which ones preceded a real catch, then auto-demote noisy ones to silent and promote effective ones. Keep it deterministic, with no model involved.
  Done when: `fm cost` reports injected tokens per rule, and after N sessions a never-triggered hint is dropped, with a unit test over a fixture ledger.

- **Add inline Pane diff review with accept/revert buttons** — FEATURE — value 4 — effort M — risk med
  Why: Audits are read-only text today. Showing the task's own diff (scoped as in T-0078) in a Pane with per-hunk Buttons, and writing the verdict into the record, turns audits into a clickable review. Assumption: Markdown/Box can render a diff well enough.
  Done when: pressing "revert hunk" in a mounted test runs the reverse patch via `$.process.run` and records an evidence line.

- **Drive-mode watchdog that re-wakes stalled sessions** — FEATURE — value 4 — effort M — risk med
  Why: `$.prompt.submit` and `$.clock.every` can detect "queue non-empty, idle for N minutes, no pending question" and resume with the exact "Next:" step. This is the real unattended story beyond `fm run`, and it needs a loop guard (max wakes, backoff, cost cap from `fm cost`).
  Done when: in a mock-clock test, an idle session with a ready brief gets exactly one wake prompt, and it stops after the cap.

- **Cross-project memory via `$.store` and `fm recall`** — FEATURE — value 3 — effort M — risk low
  Why: Foreman keeps one record per project, so lessons like "this repo's tests need X" or "this guard pattern is a false positive" never carry across projects. Assumption: `$.store` is per-plugin and persistent. Promote reflect-stage lessons with their confidence and surface them at the plan stage in a new project.
  Done when: a lesson recorded in project A appears in `fm recall` output for a similar task in project B, and can be deleted with one command.

- **Add a mod-vs-classic parity contract test** — CLEAN — value 3 — effort S — risk low
  Why: Mods are additive and classic hooks must keep working, so drift between the two paths is the main regression risk. Run the same scripted event sequence through both, and assert identical gate decisions and ledger entries.
  Done when: one test feeds a shared fixture of events to the Python hooks and to the mod handlers, and the decisions match.
