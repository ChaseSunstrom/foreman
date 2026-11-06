---
id: T-0767
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-10-14T15:41:27Z
updated: 2026-10-14T16:11:03Z
group: fm task add and evidence hardening
base: 3799cde71af16315212120b0cb2e376147fae258
base_tree: a7f7c3d50d838967ee2a7d323aebb63b0347719f
verified: strong
---
# Recreating a dropped task keeps its diff: fm task new --redo ID takes over the dropped task's start point and edited files
## Raw request
> fm task finish --commit says 'nothing to commit' when the edits were made under a dropped task and the task was recreated (T-0761 → T-0766): the recreated task should inherit the dropped one's touched files (or --from should carry them)
## Interpretation
A criterion with evidence can't be edited, so the fix is drop and recreate (fmcore.py:1128 says so). The new task's start snapshot is taken after the edits, and the dropped task owns the touched events, so finish --commit said 'nothing to commit' (T-0761 → T-0766). fm task new --redo OLD copies OLD's base/base_tree and logs OLD's touched files under the new id; the locked-criterion message names --redo.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task recreated with --redo commits the dropped task's edits on finish --commit; --redo of a task that isn't dropped is refused — verify with `cd plugin/tests && python3 -m unittest test_cli.Redo`
## Non-goals
## Approach (options → choice → why)
Options: let ac edit change an evidenced criterion (weakens the lock); auto-adopt edits of any recently dropped task (magic, can steal another task's work); an explicit --redo OLD. Chose --redo: one flag, only a dropped task, nothing implicit.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CLI test
2. [x] --redo in task new; the locked-criterion hint names it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.Redo` → ✗ exit 1 · Ran 1 test in 0.147s / FAILED (failures=1) [ran] [tree 00c032620aa2] (2026-10-14T16:08:11Z)
- (step 2) `python3 plugin/tests/run.py -k test_cli -k test_core` → exit 0 · Ran 147 tests in 20.8s (37 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 6s, Checks 4s) / OK [ran] [tree 1cb62933d809] (2026-10-14T16:09:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.Redo` → exit 0 · Ran 1 test in 0.927s / OK [ran] [tree 1cb62933d809] (2026-10-14T16:09:09Z)
- `cd plugin/tests && python3 -m unittest test_cli.Redo` → ✗ exit 1 · Ran 1 test in 0.680s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 1cb62933d809] (2026-10-14T16:09:11Z)
- `cd plugin/tests && python3 -m unittest test_cli.Redo` → exit 0 · Ran 1 test in 0.920s / OK [ran] [tree 1cb62933d809] (2026-10-14T16:09:11Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.Redo` → exit 0 · Ran 1 test in 0.509s / OK [ran] [tree 1cb62933d809] (2026-10-14T16:11:02Z)
- (audit edge) `self: diff read; --redo refuses a task that isn't dropped, copies only base/base_tree (focus keeps an existing base), logs the dropped task's touched files under the new id, and the locked-criterion message names it` → a redo of a task with no base (never focused) copies nothing and the new task snapshots at its own focus as before; files another live task edited stay out (the commit's 'only other tasks edited' filter still applies) [tree 1cb62933d809] (2026-10-14T16:11:02Z)
- (audit self) `self: diff read; --redo refuses a task that isn't dropped, copies only base/base_tree (focus keeps an existing base), logs the dropped task's touched files under the new id, and the locked-criterion message names it` → no findings [tree 1cb62933d809] (2026-10-14T16:11:02Z)
## Log
- 2026-10-14T15:41:27Z created
- 2026-10-14T16:03:01Z planned from capture
- 2026-10-14T16:07:59Z focused
- 2026-10-14T16:11:02Z done
- 2026-10-14T16:11:03Z committed 6fa82e4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Lessons
- a recreate path must carry the state the original accrued (start point, edited files), or the recreate silently loses work
## Plan gaps
- failed first: step 1 Failing CLI test
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
