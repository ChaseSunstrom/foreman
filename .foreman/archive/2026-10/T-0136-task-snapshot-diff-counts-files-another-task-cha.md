---
id: T-0136
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_paused.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-03T05:28:59Z
updated: 2026-10-03T07:57:32Z
base: c9397da8a0d9c96ba93f1b69e6368207798a1049
base_tree: 6ab7d40009c9c907d8105399e46d29774466cdef
verified: strong
---
# Work done while a task was paused isn't its own change
## Raw request
> Task snapshot diff counts files another task changed (and committed) while this one was paused: refresh or subtract other tasks' touches on re-focus
## Interpretation
A task's own changes are measured from a snapshot taken at focus. When it's paused and other work (another task's, or the user's) changes files, re-focusing it counted those files as its own: scope refusals, audit diffs, --affected tests and commits all saw them.
## Assumptions (confidence)
## Acceptance criteria
- [x] Re-focused after another task committed a file and the user edited one, a task finishes in scope and commits only its own file; overlapping changes keep the start point and log it — verify with `python3 plugin/tests/run.py -k test_paused`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) at re-focus, record the files changed while paused and subtract them in each of the five callers of task_base; (b) at pause, snapshot the files; at re-focus, if they changed since, move the start snapshot to the files as they are now with the task's own changes (start → pause) reverse-applied in a throwaway index, so every caller keeps using task_base. Choice: (b), one fix where all callers route through, and a file both changed stays correct line by line; when the changes overlap and won't come apart, the start point stays and the log says so.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: the two paused-task tests
2. [x] Snapshot at pause (focus switch, block, defer) and re-base at re-focus
3. [x] CHANGELOG and MASTER
## Resume here
## Docs impact
MASTER (how a task's own changes are measured across pauses) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_paused` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: PausedTask 1s) / OK [ran] [tree 4e006bb124b7] (2026-10-03T07:54:26Z)
- (step 2) `python3 plugin/tests/run.py -k test_paused -k TaskLifecycle` → exit 0 · Ran 30 tests in 17.4s (2 classes, 16 at a time; slowest: TaskLifecycle 17s, PausedTask 1s) / OK [ran] [tree 4e006bb124b7] (2026-10-03T07:54:44Z)
- (step 3) `grep -q T-0136 CHANGELOG.md && grep -q T-0136 MASTER.md` → exit 0 · (no output) [ran] [tree 4e006bb124b7] (2026-10-03T07:54:44Z)
- (step 2) `python3 plugin/tests/run.py -k test_paused -k TaskLifecycle` → exit 0 · Ran 30 tests in 12.3s (2 classes, 16 at a time; slowest: TaskLifecycle 12s, PausedTask 1s) / OK [ran] [tree dabcd62aa99b] (2026-10-03T07:56:21Z)
- (ac 1) `python3 plugin/tests/run.py -k test_paused` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: PausedTask 1s) / OK [ran] [tree dabcd62aa99b] (2026-10-03T07:57:21Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 07:57 UTC); cached (fm check --fresh reruns) [ran] [tree dabcd62aa99b] (2026-10-03T07:57:21Z)
- (audit intent) `One fm-reviewer pass (intent + edge): approved with 3 LOW nits; fixed the pruned-snapshot log (False vs None from rebase_snapshot) and the stale pause point when a task was set active by hand (re-base only when focus resumes a paused task); the subdirectory-root note is a coverage limit (both snapshots share the outside files).` → re-focus subtracts other tasks' and the user's work at the source (task_base), so scope, commit, audit prep and --affected all see only the task's own change; red→green on the two tests [tree dabcd62aa99b] (2026-10-03T07:57:21Z)
- (audit edge) `One fm-reviewer pass (intent + edge): approved with 3 LOW nits; fixed the pruned-snapshot log (False vs None from rebase_snapshot) and the stale pause point when a task was set active by hand (re-base only when focus resumes a paused task); the subdirectory-root note is a coverage limit (both snapshots share the outside files).` → binary, rename, delete, user-committed own files (same tree, no rebase), paused twice (overwrite), pruned snapshot (logged, start point kept), overlapping lines (logged, start point kept), set active by hand (no rebase) [tree dabcd62aa99b] (2026-10-03T07:57:21Z)
- `python3 plugin/tests/run.py -k test_paused` → ✗ exit 1 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: PausedTask 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree dabcd62aa99b] (2026-10-03T07:57:27Z)
- `python3 plugin/tests/run.py -k test_paused` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: PausedTask 1s) / OK [ran] [tree dabcd62aa99b] (2026-10-03T07:57:27Z)
- (audit intent) `One fm-reviewer pass (intent + edge): approved with 3 LOW nits; fixed the pruned-snapshot log (False vs None from rebase_snapshot) and the stale pause point when a task was set active by hand (re-base only when focus resumes a paused task); the subdirectory-root note is a coverage limit (both snapshots share the outside files).` → re-focus subtracts other tasks' and the user's work at the source (task_base), so scope, commit, audit prep and --affected all see only the task's own change; red→green proved on the start tree [tree dabcd62aa99b] (2026-10-03T07:57:32Z)
- (audit edge) `One fm-reviewer pass (intent + edge): approved with 3 LOW nits; fixed the pruned-snapshot log (False vs None from rebase_snapshot) and the stale pause point when a task was set active by hand (re-base only when focus resumes a paused task); the subdirectory-root note is a coverage limit (both snapshots share the outside files).` → binary, rename, delete, user-committed own files (same tree, no rebase), paused twice (overwrite), pruned snapshot (logged, start point kept), overlapping lines (logged, start point kept), set active by hand (no rebase) [tree dabcd62aa99b] (2026-10-03T07:57:32Z)
## Log
- 2026-10-03T05:28:59Z created
- 2026-10-03T07:51:47Z planned from capture
- 2026-10-03T07:51:47Z focused
- 2026-10-03T07:57:32Z done
- 2026-10-03T07:57:32Z committed 5afeacb (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0078 [FEATURE L, done, 4 steps] A task's own changes: diff from a working-tree snapshot taken at focus, not the last commit — lesson: A check that reads a diff must te…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- T-0132 [SECURITY M, done, 5 steps] Credential audit (fm secrets) and task-tagged commits — lesson: A scanner that gates a commit must read exactly what the commit will t…
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py; re-ground the plan against them before editing
## Lessons
- When several callers read the same derived value (task_base), fix the value where it is produced; subtracting at each caller would have left the audit diff and --affected tests wrong.
## Files touched
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_paused.py
