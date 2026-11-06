---
id: T-0765
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-10-14T15:40:58Z
updated: 2026-10-14T16:07:52Z
group: fm task add and evidence hardening
base: 76c2090fc7b85aa5c18b1d75cafd4fcd389881ef
base_tree: d7c13935a282a7485438a0ff42c033719d8d64b8
verified: strong
---
# A verify that can't run at all (python3 -m <missing module>, an fm subcommand fm doesn't have) is refused when the criterion is added
## Raw request
> fm task new/ac add lint: a verify that runs 'python3 -m <module>' for a module this python can't import (pytest here) should be refused at add time — a criterion with evidence can't be edited, so the task had to be dropped and recreated (T-0761)
## Interpretation
Three criteria today named checks that could never run: 'python3 -m pytest' (pytest isn't installed) and 'fm research list' (no such action). A criterion with evidence can't be edited (T-0342), so each task was dropped and recreated. lint_verify only warns about programs missing from PATH. Refuse, before the brief changes, a verify whose 'python -m X' module the named python can't import or whose 'fm …' words fm's own parser rejects.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task new/ac add/ac edit refuse a verify naming an unimportable python -m module or an unknown fm subcommand, and write nothing; valid ones pass — verify with `cd plugin/tests && python3 -m unittest test_cli.VerifyLint`
## Non-goals
## Approach (options → choice → why)
Options: warn louder; refuse at add time; let ac edit change an evidenced criterion when the old verify never ran its program. Chose refuse at add time: the check can't run, so there is nothing to weaken, and nothing is written.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CLI test
2. [x] Unrunnable-verify check before the brief is written
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.VerifyLint` → ✗ exit 1 · Ran 1 test in 0.138s / FAILED (failures=1) [ran] [tree c928e5288860] (2026-10-14T16:04:39Z)
- (step 2) `python3 plugin/tests/run.py -k test_cli -k test_core` → exit 0 · Ran 146 tests in 17.2s (36 classes, 16 at a time; slowest: TaskLifecycle 17s, StateViews 6s, Checks 4s) / OK [ran] [tree a7f7c3d50d83] (2026-10-14T16:05:58Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.VerifyLint` → exit 0 · Ran 1 test in 0.633s / OK [ran] [tree a7f7c3d50d83] (2026-10-14T16:05:59Z)
- `cd plugin/tests && python3 -m unittest test_cli.VerifyLint` → ✗ exit 1 · Ran 1 test in 0.191s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree a7f7c3d50d83] (2026-10-14T16:06:00Z)
- `cd plugin/tests && python3 -m unittest test_cli.VerifyLint` → exit 0 · Ran 1 test in 0.609s / OK [ran] [tree a7f7c3d50d83] (2026-10-14T16:06:00Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.VerifyLint` → exit 0 · Ran 1 test in 0.627s / OK [ran] [tree a7f7c3d50d83] (2026-10-14T16:07:51Z)
- (audit edge) `self: diff read; the check runs before the brief changes in task new, ac add and ac edit; it parses only literal words (anything with $ or a backtick, or an unreadable quote, is left alone), follows literal cd links for where python -m imports, and asks fm's own parser about fm words` → scanned all 1,663 recorded criteria in this install: 10 refused, every one genuinely unrunnable (fm research list/show, prose like 'fm doctor (file map)', python3 -m pytest without pytest); no false refusals [tree a7f7c3d50d83] (2026-10-14T16:07:51Z)
- (audit self) `self: diff read; the check runs before the brief changes in task new, ac add and ac edit; it parses only literal words (anything with $ or a backtick, or an unreadable quote, is left alone), follows literal cd links for where python -m imports, and asks fm's own parser about fm words` → no findings [tree a7f7c3d50d83] (2026-10-14T16:07:51Z)
## Log
- 2026-10-14T15:40:58Z created
- 2026-10-14T16:01:20Z planned from capture
- 2026-10-14T16:04:27Z focused
- 2026-10-14T16:07:51Z done
- 2026-10-14T16:07:52Z committed 3799cde (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0766 [FIX S, done, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman — lesson: a guard relaxation keyed on what a…
- research rsi-20261006: 1. **Answer.** Four of the five friction points trace to small, local causes. The guard leaves a variable unknown when its value starts with `~`. …
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- decision 2026-10-14: Block T-0760 rather than edit its failing AC, since the AC already has evidence
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Lessons
- a check that can never run should be refused when it's written, not discovered when it fails
## Plan gaps
- failed first: step 1 Failing CLI test
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
