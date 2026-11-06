=== T-1028
INTERPRETATION: When the session that launched a builder ends, the task stays bound to a dead builder (`meta["builder"]` and `meta["lane"]`). The user gets `fm lane resume ID`, which saves the WIP, frees the worktree and writes a new builder brief that starts from the old branch. `fm next` and the pane flag stopped builders. Already covered: `fm lane rm` frees a builder slot that never launched (fmlanes.py:96-100); `remove()` frees a lane but refuses uncommitted work (fmlanes.py:348-392); `fmbus.claude_pid()` and `_proc()` give a pid plus start time (fmbus.py:132-186); `builder_brief` writes the brief (fmlanes.py:139-194).
APPROACH: (a) SendMessage to the dead agent; (b) re-enter the old worktree path; (c) hand off through the branch, as the brief's design says. Choice: (c), the harness-independent one. Changes:
- `builder_brief` records `meta["builder_proc"]={pid,start}` from `fmbus.claude_pid()` plus a new `fmbus.proc_alive(pid,start)`.
- New `resume()` in fmlanes.py: `git add -A && commit` on the lane branch, `git worktree remove`, pop `lane`/`builder`, then write a brief with a "Resume" section that merges `foreman/ID` first.
- `cmd_lane` gets a `resume` choice (fmcli.py:4915) and `--json`.
- `fm next` (fmcli.py:3825) gets a "stopped builder" line.
Ship as M in two commits: lane resume plus detection first, then the `fm next` and pane flags. The pane is TSX, so split it into a later task. Skip `--all` and the SessionStart offer.
AC: A builder whose recorded pid is dead is flagged by `fm next` with `fm lane resume T-ID` :: python3 plugin/tests/run.py test_lanes
AC: `fm lane resume` commits WIP, removes the folder, keeps the branch, resets the task and writes the brief :: python3 plugin/tests/run.py test_lanes
STEP: Failing tests in test_lanes.py: a fake pid recorded in `builder_proc` is reported stopped; a real worktree with a dirty file gets a WIP commit on `foreman/ID`; the folder is gone; the branch exists; `lane` and `builder` metadata are cleared; the brief mentions the branch.
STEP: Add `fmbus.proc_alive` and record `builder_proc` in `builder_brief`.
STEP: Add `resume()` and the CLI choice; add the stopped line to `fm next`.
SCOPE: plugin/lib/fmlanes.py, plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/tests/test_lanes.py
TIER: M

=== T-1037
INTERPRETATION: The user gets bulk, quality-checked card drafts for uncovered dependencies. Already covered: `probe_lib_gaps` finds the uncovered deps and captures a task (fmscout.py:68-93); the card format and linter exist (`fmlib._card_problems`, fmlib.py:171-205, with `SECTIONS`/`SIZE`/`KEYS` at fmlib.py:19-21); `fm lib check` runs the lint (fmlib.py:841). Missing: a command that drafts from real docs and gates each draft.
APPROACH: (a) Python fetches docs and writes drafts. This is not possible, because context7 is an MCP tool only Claude can call. (b) Claude writes the drafts; a new `fm lib draft` stages them and admits only those that pass the lint. (c) A full pipeline. Choice: (b). Python stays stdlib, and the format check stays in code.
- Split into 2 M tasks. Piece 1 adds `fm lib draft NAME` and `fm lib admit` to fmlib.py: drafts sit in state `lib-drafts/<area>/<name>.md`; `admit` runs `lint_card` and moves passing drafts into `CARDS`, reporting failures. It also adds `fm lib gaps [--json]`, reusing the `probe_lib_gaps` logic split into a function.
- Piece 2 updates the `probe_lib_gaps` finding text and the library skill so a writer subagent reads context7 or the package README and runs `fm lib admit`. It adds a source-line requirement ("Sources:" in Notes), checked by a new lint rule.
AC: `fm lib admit` moves a well-formed draft into the library and rejects a malformed one with its problems :: python3 plugin/tests/run.py test_library
AC: `fm lib gaps --json` lists uncovered deps :: python3 plugin/tests/run.py test_library test_scout
STEP: Failing tests: a staged good card is admitted (file in cards dir, exit 0); a card with a missing section stays staged (exit 1, the lint message printed); gaps lists an uncovered dep and not a covered one.
STEP: Refactor the dep loop out of `probe_lib_gaps` into `uncovered_deps(roots)`; add the `draft`, `admit` and `gaps` actions in `cmd_lib`.
SCOPE: plugin/lib/fmlib.py, plugin/lib/fmscout.py, plugin/lib/fmcli.py, plugin/tests/test_library.py, plugin/tests/test_scout.py, plugin/skills/library/SKILL.md
TIER: L

=== T-1099
INTERPRETATION: The ledger roll must not lose or reorder lines. Already covered: `_roll_ledger` runs under `c.lock(p.dir)` (fmtidy.py:254), but that is the `.lock` file. `log_event` flocks `ledger.jsonl` itself (fmcore.py:780), so the roll never excludes a writer. Still wrong: a line whose `ts` is unparseable goes to the current month and stays live (fmtidy.py:259-262); the file is read in text mode (fmtidy.py:256), so a bad byte raises `UnicodeDecodeError`; and the 23-hour `ts` and `prev` order can break.
APPROACH: (a) Patch the three symptoms separately. (b) Rewrite `_roll_ledger` in binary under the ledger flock, with an unparseable `ts` inheriting the previous line's month. (c) Add a lock helper to fmcore. Choice: (b). The old-version-writer race can't be closed without changing old writers, so document it as a ceiling in a `ponytail:` comment.
- Open `ledger.jsonl` as `r+b`, take `fcntl.flock(LOCK_EX)`, and read the lines as bytes.
- Decode each line with `errors="replace"` only for the `ts` lookup.
- Roll a line to the archive only when its month, or the carried-forward month, is below the current one. Never keep a line live that sits between rolled lines.
- Write the live remainder back in place, still under the flock. `write_atomic` swaps the inode, so a writer that already holds the old fd would write to the unlinked file. Truncate and rewrite instead.
AC: A racing writer's line survives the roll, and `verify-ledger` stays green :: python3 plugin/tests/run.py test_ledger_chain
AC: A bad byte or an unparseable `ts` doesn't break the roll or reorder the chain :: python3 plugin/tests/run.py test_ledger_chain
STEP: Failing tests in test_ledger_chain.py: a ledger with an invalid utf-8 byte rolls without raising; an unparseable-ts line between old lines is archived with them; with the flock held in a thread, the roll waits and then keeps the writer's line.
STEP: Rewrite `_roll_ledger` as above.
SCOPE: plugin/lib/fmtidy.py, plugin/tests/test_ledger_chain.py
TIER: S

=== T-1101
INTERPRETATION: `fm check` runs the gates as stored strings (fmcli.py:3066-3074). With the project's suite as a gate, another open task's recorded failing tests fail this task's close. The user gets a run that leaves those test files out and says so. Already covered: `run.py` takes names and `-k` (run.py:46-56) but has no exclude option; `c.run_command` accepts `env` (fmcore.py:429); step evidence has the `(step N)` tag, the cmd and a ✗ mark (fmcore.py:903, 1206-1212).
APPROACH: (a) Rewrite the gate command. This is fragile with arbitrary strings. (b) Pass the exclusions in an env var that `run.py` honours. (c) Park the files by hand, which is today's behaviour. Choice: (b).
- New `red_first_tests(p, act)` in fmcli.py. For every other brief with status in `c.OPEN` and not the active one, it reads step-1 evidence lines that are ✗ and whose cmd contains `tests/run.py`, takes the module names, and keeps only names with no passing evidence line. Names that also appear in the active task's evidence or scope are never excluded.
- `cmd_check` passes `env={**os.environ, "FOREMAN_SKIP_TESTS": "a,b"}` to `run_command`.
- `run.py` `classes()` drops modules in that env var.
- Output gains a line "skipped N test file(s) that are only task T-XXXX's red-first tests: …".
AC: With task B holding step-1 red evidence for `test_x`, `fm check` for task A passes and names `test_x` as skipped :: python3 plugin/tests/run.py test_check_paths
AC: `run.py` honours `FOREMAN_SKIP_TESTS` :: python3 plugin/tests/run.py test_check_paths
STEP: Failing tests in test_check_paths.py (or a new test_check_skip.py): `run.py` with the env var omits the module; `fm check` output contains "skipped".
STEP: Implement `red_first_tests`, the env pass-through and the `run.py` filter.
SCOPE: plugin/lib/fmcli.py, plugin/tests/run.py, plugin/tests/test_check_paths.py
TIER: S
