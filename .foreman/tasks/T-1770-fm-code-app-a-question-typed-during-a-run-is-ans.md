---
id: T-1770
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T09:49:56Z
updated: 2026-10-23T11:31:51Z
base: 819a6ddebb2faded5e67d22369e9d42d81356629
base_tree: 6e2fd31b70fbdae7bfb65caede4e193c80bc2354
plan0_at: 2026-10-23T11:28:22Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code app: a question typed during a run is answered read-only beside it (the rest of T-
## Raw request
> fm code app: a question typed during a run is answered read-only beside it (the rest of T-1340)
## Interpretation
In the fm code app, a question typed during a run is answered read-only beside it: the run goes on untouched, and the answer lands in Activity. The CLI half: fm code --ask runs a question with no task and without the one-run-per-tree lock (T-1342), and refuses if the planner plans a change instead of answering.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --ask answers beside a run holding the tree and refuses a plan; n during a run asks beside it and the answer lands in Activity with the run unchanged — verify with `python3 plugin/tests/run.py test_code.AskBeside test_code_tui.AskBeside`
## Non-goals
## Approach (options → choice → why)
Options: (1) n during a run opens an ask prompt; Enter spawns fm code --ask beside the run and only its answer event comes back, as an aside entry (chosen: reuses T-1320's answer mode, read/search/done only); (2) answer in the app's own process with the model client (rejected: a second model path to keep in step with fm code's); (3) queue the question until the run ends (rejected: not beside it). --ask skips the tree lock because it can't change anything: the planner must answer (a plan is refused before any check runs), and --resume, --task and --verify are refused with it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm code --ask, test first
2. [x] the app's ask beside a run, test first
## Resume here
## Docs impact
CHANGELOG line; fm code -h documents --ask. MASTER lists no fm code flags (--after isn't there either).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.AskBeside` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: AskBeside 1s) / FAILED (1 classes) [ran] [tree 9dcb5fbd7c6f] (2026-10-23T11:28:30Z)
- (step 1) `python3 plugin/tests/run.py test_code.AskBeside test_code.TreeLock test_code.AnyRequest` → exit 0 · Ran 6 tests in 3.0s (3 classes, 16 at a time; slowest: AnyRequest 3s, TreeLock 3s, AskBeside 2s) / OK [ran] [tree 7dea158d0412] (2026-10-23T11:28:39Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui.AskBeside` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: AskBeside 0s) / FAILED (1 classes) [ran] [tree 7e62e311e818] (2026-10-23T11:28:40Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code test_cli` → exit 0 · Ran 535 tests in 79.3s (123 classes, 16 at a time; slowest: Worker 79s, Fakes 45s, TaskLifecycle 29s) / OK [ran] [tree 4c7bc078e6cc] (2026-10-23T11:30:03Z)
- (ac 1) `python3 plugin/tests/run.py test_code.AskBeside test_code_tui.AskBeside` → exit 0 · Ran 2 tests in 1.8s (2 classes, 16 at a time; slowest: AskBeside 2s, AskBeside 0s) / OK [ran] [tree 4c7bc078e6cc] (2026-10-23T11:30:26Z)
- (ac 1) `python3 plugin/tests/run.py test_code.AskBeside test_code_tui.AskBeside` → exit 0 · Ran 2 tests in 1.8s (2 classes, 16 at a time; slowest: AskBeside 2s, AskBeside 0s) / OK [ran] [tree 4c7bc078e6cc] (2026-10-23T11:30:28Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): traced every way an --ask run could change files: a model planner's answer runs with read/search/done only (T-1320's read_only), a CLI planner's answer is its read-only plan text, a plan is refused before any check or task, and --resume, --task and --verify (each of which skips the planner's answer) are refused with --ask; the app passes only the side run's answer back, filtered to printable text` → n during a run opens an ask prompt; Enter asks fm code --ask beside the run; the answer lands in Activity under its question while the run goes on; outside a run n is a fresh request as before [tree 4c7bc078e6cc] (2026-10-23T11:30:28Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): traced every way an --ask run could change files: a model planner's answer runs with read/search/done only (T-1320's read_only), a CLI planner's answer is its read-only plan text, a plan is refused before any check or task, and --resume, --task and --verify (each of which skips the planner's answer) are refused with --ask; the app passes only the side run's answer back, filtered to printable text` → a side run that ends without an answer (a planned change, a bad flag, a crash) shows its question with the last error line; Esc leaves ask mode; s and q end any ask still going; an answer's control characters never reach the terminal; an ask that outlives its run lands in the next run's Activity, still under its question [tree 4c7bc078e6cc] (2026-10-23T11:30:28Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): traced every way an --ask run could change files: a model planner's answer runs with read/search/done only (T-1320's read_only), a CLI planner's answer is its read-only plan text, a plan is refused before any check or task, and --resume, --task and --verify (each of which skips the planner's answer) are refused with --ask; the app passes only the side run's answer back, filtered to printable text` → --ask holds no tree lock, so it must never write: the planner's plan is refused at the slot, before checks, task or work; the answer phase allows read, search and done only; --verify, whose plan is Foreman's own, is refused with --ask as are --task and --resume; a side run's other events never reach the app [tree 4c7bc078e6cc] (2026-10-23T11:30:28Z)
## Log
- 2026-10-23T09:49:56Z created
- 2026-10-23T11:28:17Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T11:28:21Z focused
- 2026-10-23T11:31:49Z done
- 2026-10-23T11:31:51Z committed a1e62b90 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- T-1765 [FEATURE M, done, 2 steps] Fm code: a slot-format ladder — after two failed JSON repairs, ask one field per question — lesson: A weak model that can't hold a JSON…
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A mode that skips a lock must be refused on every path that would reach the work the lock guards, not only the usual one: --verify planned without the planner
## Plan gaps
- failed first: step 1 fm code --ask, test first
- failed first: step 2 the app's ask beside a run, test first
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/tests/test_code_tui.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
