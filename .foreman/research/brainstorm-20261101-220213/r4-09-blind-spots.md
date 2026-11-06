# Brainstorm — lens: blind spots

The asks in the pack fall into five classes. For each, I name the question a brainstorm should have asked and apply it to #12 (lean and safe, 61 empty cells). The first four classes carry the numbered ideas; the fifth, a number's premise changing under it (T-2525), is covered by idea 11.

- **T-2499** — Question: what only advances while a session is open?
- **T-2500** — Question: which ledger row lacks a dimension the user will split by?
- **T-2501/2502** — Question: what is checked per task but never across the whole?
- **T-2503/2504** — Question: which gauge measures form rather than substance?
- **T-2525** — Question: what other premise sits under a fixed number?

- **Probe hooks from the night tick, not from sessions** — FIX — value 4 — effort S — risk low — category: lean
  Why: the 278 ms p95 over 13533 runs is sampled only when a session is open, so it misses cold caches, idle boxes and headless runs. (Class T-2499.)
  Done when: `fm night`'s tick fires a synthetic event per hook type, `fm doctor` prints p95 for tick-sourced and session-sourced samples separately, and a test with a stubbed slow hook turns the tick row red.

- **Split hook and guard ledgers by harness, host version and Python** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-2500 had to ask for `--by harness` on bets. Friction, guard blocks and context bytes carry the same gap, and the project claims to be harness-neutral.
  Done when: `fm friction --by harness|host|python` returns non-empty groups from a fixture with three harnesses, and a row without the dimension fails a unit test.

- **Add a time-boxed ratchet waiver** — FEATURE — value 4 — effort S — risk med — category: lean ratchet
  Why: assumption: a hard lean cap will block an urgent fix, and the user will then disable the ratchet by hand. A waiver with a reason and an expiry stays on the record and ends by itself.
  Done when: `fm lean waive --until 2d --reason …` lets one task close, the final report lists it, and after expiry the same growth fails again.

- **Lock ratchet baselines against quiet rebasing** — SECURITY — value 3 — effort S — risk low — category: lean ratchet
  Why: T-2503 makes growth "pending" until it is measured, and a rebase would hide that growth. (Class T-2503.)
  Done when: changing a baseline file without a matching `fm decide --kind costly` entry fails `fm genesis sweep`.

- **Check guard rules for shadowing and conflicts** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard is checked rule by rule, but nothing checks across rules (T-2501's class). An allow or an earlier match can make a deny unreachable.
  Done when: a static pass lists every deny rule that no input can reach, and a planted shadowed rule is caught.

- **Pair every guard false-positive fix with a mirrored evasion case** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the two brief-guard false positives (a dict key and `.join(` read as written paths) will be fixed by loosening the matcher, and a loosened matcher can open a hole.
  Done when: the fix commit adds the false-positive fixture and a near-identical true-positive fixture, and both are asserted.

- **Define a headless blocked-command contract** — FEATURE — value 4 — effort M — risk med — category: headless/server
  Why: the headless/server column of the grid is empty. A guard block with no human present must not hang waiting for approval.
  Done when: a headless run that hits a denied command exits with a distinct code and writes a JSON block record naming the safe alternative, and an e2e test passes with stdin closed.

- **Fence strings from untrusted sources in the SessionStart note** — SECURITY — value 4 — effort M — risk low — category: injection
  Why: assumption: the note (~2k chars, injected 89 times) carries task titles and CI or commit text that Foreman did not author.
  Done when: every non-user string in the note is wrapped in a data fence, and a planted instruction in a CI log title is not obeyed by a cold child reading the note.

- **Budget instruction count, not only bytes** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: T-2503 asked for substance over form, and 387k tokens per reply measures form. Fifty tiny imperatives can cost more attention than one long block.
  Done when: `fm cost` prints imperative sentences injected per reply by source, and a ratchet row fails when the count grows without an exam gain.

- **Switch to safe mode when the host version drifts** — SECURITY — value 4 — effort M — risk med — category: hooks
  Why: hook contracts vary by host (Gemini's AfterAgent deny discards the answer, T-0337). A new host build can silently break the guard in bypass mode.
  Done when: on an unseen host version, `fm doctor` runs the guard corpus, and if any case fails it disables only the affected hooks and says so, fail-closed on the guard.

- **Meter the lean machinery's own cost** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: filling 61 cells, nightly probes and cold reads can outweigh what they protect. The pack has no figure for sweep runtime or tokens.
  Done when: `fm genesis sweep` prints its seconds and tokens per row, and the lean row is red if their total exceeds a stated share of the generation's cost.

- **Map every verb back to a grid cell (reverse coverage)** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: the grid asks which cells lack features, but not which features lack cells. Orphan verbs are also the unused-verb candidates for subtraction.
  Done when: a command lists verbs that no cell cites, and each orphan gets a cell or a retirement task.

- **Wild: Add phantom mode** — FEATURE — value 4 — effort L — risk med — category: lean proof
  Why: wild. Foreman records what it would have injected or blocked but injects nothing, so one session gives per-block counterfactuals without a second run.
  Done when: `fm phantom on` makes a session log bytes and blocks that would have fired, and `fm cost` reports the saving per source.

- **Wild: Ship a standalone guard in one stdlib file** — FEATURE — value 4 — effort L — risk med — category: other agents
  Why: wild. A file under 300 lines, with no Foreman dependency, that any agent can call as a pre-command check. This fits the standing rule that Foreman is not tied to Claude Code and gives "other agents" a minimal safe cell.
  Done when: the file runs the full guard corpus on a machine with no `fm`, and its output matches the in-process guard.

- **Wild: Add a steer replay drill** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: wild. When the user gives a new steer, a cold child tries to violate it against current gates and reports which gate would have let it through. That puts the missed question to work before the next ask.
  Done when: a steer entered through `fm decide --check` produces a pass or fail drill record.

Next question: which standing rules have never fired, and would a tool-less child say they are still needed?
Next question: what do the 61 cells say about surfaces the user has never opened, and who verified they are real?
