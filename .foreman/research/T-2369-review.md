**Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-miss resolution contradicts the acceptance criterion, and two hot-path and matching weaknesses are real. I read the code and the 13 `MissLoop` tests. I did not run anything: no Bash tool was available here.

## lens: intent
- HIGH — `plugin/lib/fmmiss.py:69` (`_written`, lines 31-40) and the test at `plugin/tests/test_tool_loop.py:115-121` — The AC says "a red-first test's missing module resolves only when that test command goes green; no … file's existence resolves a miss". The code does the opposite. For `kind == "module"` it drops the miss as soon as any code file or package of that name exists in the tree (`git ls-files --cached --others`), and the test asserts that this closes the task. Scenario: `python3 app.py` fails with "No module named 'yaml'". The agent runs `touch yaml.py`, `fm next` shows no miss, and finish closes with the test never run. The stem match is loose (`base.endswith("/" + stem)`), so any unrelated `x/yaml.py` also clears it. — Delete the `_written` branch and its test. A module miss then clears only through the same command going green, a pairing, or the other two events. Flip the test to assert that the file does not clear it. — high

## lens: adversary
- MEDIUM — `plugin/lib/fmmiss.py:43-47` — The Bash-event resolution has no lane, session or cwd filter, only `project == p.slug`. A passing run of the same command in another lane, session or subagent of this project resolves the miss. This repo's parallel builder lanes routinely run identical `python3 plugin/tests/run.py …` commands. Tool events carry `session_id`, and the miss event records one. — Count only events whose `session_id` is in the set of sessions with ledger events on this task (or the miss's own session). — high
- MEDIUM — `plugin/lib/fmmiss.py:16,74` with `plugin/lib/fmfixes.py:27-37,346` — `fix_paired` resolves on any later passing command that "relates" to the failed one, meaning it contains the failed command's subject as a word. `_LOOK` excludes `echo` and `which`, but `touch gizmo`, `true gizmo` and `mkdir gizmo` all pass `_relates`. Scenario: `gizmo --x` is "command not found", the agent runs `touch gizmo`, a `fix_paired` event is logged, and the miss closes with no real run. This is a no-op acting as a typed claim. — Resolve a pairing only if the tool is actually present now (`shutil.which(name)` for a command, an import check for a module), or exclude `touch|mkdir|true|:|test|[` from pairing. — medium
- MEDIUM — `plugin/lib/fmmiss.py:24` — `key()` cuts to 120 characters, so two different long commands collide. `fm check --affected` lists run to 200+ characters, and a command that differs only past character 120, or has `|| true` appended, shares the key and resolves the miss. — Compare on the full normalised command, and use the event-target path only when the command is under 120 characters. — high
- LOW — `plugin/lib/fmmiss.py:92` — `m['cmd']` goes into the refusal text through `c.fit` only. It is redacted at log time but not passed through `c.plain` or `c.defang`. — Wrap it in `c.defang(c.plain(...))`. — high
- LOW — `plugin/lib/fmmiss.py:74,77` — `tool_proved` and `grant_queued` have no emitter anywhere in the tree. Their payload shape (`name`, `step`) is an unwritten contract that the later briefs must meet, and only the tests exercise it. Note this contract in the task. — high

## lens: edge
- MEDIUM — `plugin/lib/fmmiss.py:21-24,45` — For a command with a `cd X &&` prefix, the event target is cut to 120 characters before the prefix is stripped, while the miss key is cut after. The two keys differ, so the Bash-event path never matches for such commands. — Fixed by the same change as the key finding above. — medium
- MEDIUM — `plugin/lib/fmcli.py:1124-1127` — Finish checks miss gaps before it runs `--run`. `fm task finish … --run <the missed command>` is therefore refused with "nothing ran". The agent must first run `fm task evidence --step N --run <exact cmd>`. — Say so in the refusal, or exempt a `--run` equal to a miss's key. — high
- LOW — a later wider green run, such as `fm check --affected` after a red-first `run.py test_x`, does not close the miss. Only the exact command does. — Document it in the refusal text. — medium
- LOW — `plugin/lib/fmcli.py:755,1124` call `fmmiss.gaps` with no try/except, while `fmcore.py:3672` guards it. An exception in `_written` or `ledger_events` would break finish and done. — Guard both, failing open with a logged error. — low

## lens: operator
- HIGH — `plugin/lib/fmmiss.py:45`, called from `fmcore.py:3671` — With an open miss that no pairing or [ran] run has resolved, `_bash_ok` calls `c.global_events`. That reads `tail_jsonl(path, 200000)` of every rotated `events-*.jsonl` plus the live file. The live file has 68,613 lines and there are 3 rotated files. `next_for` runs on every prompt (`fmhooks.py:1468`), at Stop (`:4024`), at `:633`, and on every `fmwatch` poll (`fmwatch.py:606`). Each hook is a new process, so the tail memo never helps. Cost is roughly (lines parsed) × (prompts + stops + polls) × (sessions), for as long as a miss stays open, and the task recorded no timing. The repo has long sessions with pane polling, so this can add seconds per call. A typical open miss, such as an incidental `rg: command not found` the agent worked around, stays open indefinitely. — Skip rotated files whose name stamp is earlier than `since`, and read the live file only from `since`. Better, have the PostToolUse hook log a `miss_resolved` event when a passing key matches an open miss, so the readers do no events scan. — high
- MEDIUM — `plugin/lib/fmmiss.py:31-40` — Each `open_misses` call for a module miss runs `git ls-files` as a subprocess. This goes away with the `_written` fix. — high
- MEDIUM — Incidental misses such as `python: command not found` followed by `python3` are not paired when the subject differs. They then block finish until the exact failing command goes green or the task is blocked. Check how often this fires. — low
- LOW — The refusal truncates the command to 80 characters, so the agent cannot rerun it exactly. Print the full command, and the `fm task evidence ID --step N --run '<cmd>'` form. — high

## lens: maintainer
- LOW — `CHANGELOG.md` has no capability-miss entry, though step 4 is ticked done. `MASTER.md:242` is updated. — Add the entry. — medium
- LOW — The `fmfixes.on_success` return-value change and the new `fix_paired` event are not documented in `fmfixes`. — Add one line. — medium

## Acceptance criteria
- Miss logged with task and command; `fm next` names it: met (`fmhooks.py:3299-3302`, `fmcore.py:3670`, test at `test_tool_loop.py:44`).
- Finish refuses on every try while a miss is open; closes on a later green same command, a fmfixes pair, a `tool_proved` event, or a grant plus a green fallback step: met in the tests. The weaknesses above (cross-lane runs, 120-character collisions, weak pairing) qualify it.
- "A red-first test's missing module resolves only when that test command goes green; no file's existence resolves a miss": **not met** (`fmmiss.py:69`).
- No typed line or flag resolves a miss: met for [ran] evidence, typed evidence and flags. The `touch`-pairing path weakens it.
- A task with no miss gets no new check: partly met. It pays one ledger read per `next_for`, finish and done call; the rest only runs once a miss is logged.

## Implicit decisions
- Resolution matches by name plus the 120-character normalised command.
- Timestamps are strict "later" at whole-second resolution.
- Subagent misses are not logged.
- The newest miss per (name, command) wins.
- `fix_paired` is a new ledger event.
- Misses are scanned only from the task's creation time.

## Not checked
- I did not run the tests.
- I did not measure the cost of `global_events`.
- I did not read the `MASTER.md` wording.

Noticed: `fmfixes._relates` pairing accepts no-op commands such as `touch NAME`, which pollutes the fix store (`fmfixes.add`) as well as the new gate.
