---
id: T-2334
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_tasks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T13:54:19Z
updated: 2026-11-02T02:35:45Z
rival_at: 2026-11-02T02:25:11Z
rival_split: true
base: 6dbfa8a340351d90d64d76f3e6907d7c09d1a9d7
base_tree: cf78a46cc0fa283f1666e3011020e8a80c892f98
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T02:25:26Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_tasks.py, CHANGELOG.md]
base_note: Calibration: this plan states Choice 70% where FIX M closes (107) held on the first finish 94% of the time: 24 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
verified: strong
---
# A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit
## Raw request
> fm task new --focus recorded no start commit for T-2332 (fm audit prep said 'focused before fm kept one'), and fm task finish --commit then closed it without committing its files; seen 2026-10-31
## Interpretation
Reading 1: T-2332 has neither base nor base_tree: git_head and worktree_tree each run git with a 10 s timeout and return None on a timeout, so a loaded host at focus leaves a task with nothing to diff; and task_base's cat-file check (also 10 s) reads a timeout as 'no start point', so finish --commit refuses a task whose base exists. Reading 2: task new --focus skips cmd_focus's base step. A probe shows task new --focus records base and base_tree today, so Reading 1 is the live defect.
## Assumptions (confidence)
## Acceptance criteria
- [x] a git_head that times out once still returns HEAD; task_base returns the base when cat-file times out; a task focused with no base gets one at its first evidence, logged — verify with `python3 plugin/tests/run.py test_core test_cli`
## Non-goals
## Approach (options → choice → why)
1) git_head and worktree_tree retry once with a 60 s timeout before returning None; task_base tells a timeout from absence (a timed-out check counts the rev as present); a task still missing base at its first fm task evidence gets HEAD then, logged as recorded late; fails if: HEAD moved between focus and the first evidence (only when the task committed by hand, and the log names it). 2) use what exists: finish already refuses with commit by hand; fails if: every loaded focus costs a manual commit. 3) do less: only the retry at focus; fails if: a base that exists is still refused when cat-file times out at finish. Choice 1 (70%): three small changes at the three places git's timeout turns into a wrong answer.
## Risks and rollback
Risk: a 60 s retry slows a focus on a host that is truly stuck; it happens only after a first timeout. Risk: counting a timed-out cat-file as present could diff from a pruned snapshot; the diff itself then fails closed (task_diff returns None). Rollback: revert; no state format changes.
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/test_cli.py, plugin/tests/test_guard.py; past FIXes T-0875, T-0876, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red tests: mock subprocess timeouts for git_head (first call) and task_base's cat-file; a brief with no base gets one from fm task evidence with a 'start point recorded late' log line
2. [x] fmcore.git_head/worktree_tree retry; task_base timeout-as-present; cmd_task evidence records a missing base; Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.StartPoint` → ✗ exit 1 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: StartPoint 0s) / FAILED (1 classes: test_core.StartPoint) [ran] [tree d432481316de] [world 2f1906870a] (2026-11-02T02:26:10Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_cli 2>&1 | tail -1` → exit 0 · OK [ran] [tree 6dc418545747] [world 2f1906870a] (2026-11-02T02:27:52Z)
- (step 1) `python3 plugin/tests/run.py test_core.StartPoint` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: StartPoint 0s) / OK [ran] [tree 6dc418545747] [world 2f1906870a] (2026-11-02T02:28:02Z)
- (step 2) `python3 plugin/tests/run.py test_core test_cli` → exit 0 · Ran 280 tests in 21.2s (72 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, CaptureAndIntake 9s) / OK [ran] [tree 6dc418545747] [world 2f1906870a] (2026-11-02T02:28:23Z)
- `python3 plugin/tests/run.py test_core.StartPoint` → ✗ exit 1 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: StartPoint 0s) / FAILED (1 classes: test_core.StartPoint) (start tree + this task's tests) [ran] [tree 6dc418545747] [world 2f1906870a] (2026-11-02T02:28:26Z)
- `python3 plugin/tests/run.py test_core.StartPoint` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: StartPoint 0s) / OK [ran] [tree 6dc418545747] [world 2f1906870a] (2026-11-02T02:28:26Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_cli` → exit 0 · Ran 280 tests in 20.8s (72 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, CaptureAndIntake 9s) / OK [ran] [tree b0b274a59e5a] [world 2f1906870a] (2026-11-02T02:35:06Z)
- (audit intent) `self-review: git_head retries once on a timeout with 60 s (OSError and other failures still return None at once); task_base asks git through _git with proc=True and counts returncode 124 (timeout) as present, so a base that exists isn't refused under load (a pruned one then fails closed in task_diff); the evidence writer records HEAD as base when a task has none, under the brief lock, with a log line, never a snapshot (it would hide edits made so far)` → a task always has a start point, so finish --commit can tell its files apart [tree b0b274a59e5a] (2026-11-02T02:35:06Z)
- (audit edge) `self-review: git_head retries once on a timeout with 60 s (OSError and other failures still return None at once); task_base asks git through _git with proc=True and counts returncode 124 (timeout) as present, so a base that exists isn't refused under load (a pruned one then fails closed in task_diff); the evidence writer records HEAD as base when a task has none, under the brief lock, with a log line, never a snapshot (it would hide edits made so far)` → a second timeout still returns None; a missing rev returns None; a task with a base keeps it; a repo outside git records nothing [tree b0b274a59e5a] (2026-11-02T02:35:06Z)
## Log
- 2026-10-31T13:54:19Z created
- 2026-11-02T00:20:35Z planned from capture
- 2026-11-02T00:20:35Z set approved=True
- 2026-11-02T02:25:26Z focused
- 2026-11-02T02:25:26Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T02:25:34Z criterion 1 verify: `python3 plugin/tests/run.py test_core test_tasks` → `python3 plugin/tests/run.py test_core test_cli`
- 2026-11-02T02:28:26Z scope: fm task set status=active is refused (T-0134), so the late record covers other paths (an old focus path, a git timeout), simulated in the test by writing the status
- 2026-11-02T02:35:42Z done
- 2026-11-02T02:35:45Z committed 2fb3b24c (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Two linked bugs in the task lifecycle (likeliest).** `fm task new --focus` must record a start commit (HEAD) for the task, and `fm task finish --commit` must actually commit the task's files. Today the first leaves the start commit empty, and the second closes the task without committing anything…
- **Only the missing start commit.** `--focus` on an existing or new task skips the start-commit field, and `finish --commit` silently does nothing because it has no baseline to diff against. Fixing the recording would fix both.
- **Only the finish bug.** `--commit` should refuse to close the task, or fail loudly, when it has nothing to commit or cannot work out which files belong to the task. The missing start commit is legacy data, which `fm audit prep` already flags as "focused before fm kept one".
- **Legacy backfill.** Tasks focused before fm kept start commits, like T-2332, need a repair path (backfill or an explicit "unknown baseline" state) so they stop tripping audit prep.
Approaches:
- **Record at focus time.** In the `task new --focus` path in `plugin/lib/fmcli.py`, write `git rev-parse HEAD` into the task record through `fmcore.py`, the same way plain `task focus` does if it already does. Then make `finish --commit` stage and commit only the files changed since that commit, and…
- **Reorder finish.** Make `finish --commit` commit first and mark the task closed only after the commit succeeds, with a missing start commit meaning "stage the files the task records" or "refuse with a clear message". This fixes the silent-close regardless of how the start commit was recorded.
- **Share one focus helper.** Route `new --focus` and `task focus` through a single function that sets the focus and start commit, so the two entry points can't diverge again. Add a regression test in `plugin/tests/` that runs new, focus, finish and then checks `git log`.
- **Backfill for T-2332.** Add a narrow `fm doctor` or `audit prep` repair that sets the start commit for legacy tasks from the first commit that touched their files, or marks it explicitly unknown.
Failure modes:
- **Wrong baseline.** The start commit is recorded before the repo is initialised or before a dirty tree is stashed, so `finish --commit` sweeps in unrelated files or misses the task's own, a problem when work was already uncommitted at `new --focus` time.
- **Silent no-op persists.** The commit step still returns success when `git commit` exits non-zero or finds nothing staged, so the task closes with an empty or missing commit. The check has to be on the exit status, not on the flag being present.
- **Guard and hook interference.** `plugin/lib/fmguard.py` or the hooks in `plugin/lib/fmhooks.py` may block or rewrite the commit, so `finish --commit` fails in real use even though a direct unit test passes. `plugin/tests/test_guard.py` wouldn't catch this.
- **Legacy tasks break.** Making a start commit mandatory makes `finish` fail on every pre-existing task with none, T-2332 included, unless the missing-baseline case is handled explicitly.
## Dissent
- [x] rival reading: **Two linked bugs in the task lifecycle (likeliest).** `fm task new --focus` must record a start commit (HEAD) for the task, and `fm task finish --commit` must actually commit the task's files. Today the first leaves the start commit empty, and the second closes the task without committing anything… — answered: adopted in part: the start point is the root; finish already refuses loudly without one ('no start point on record … commit by hand', fmcli._commit_task), so the fix records it
- [x] rival reading: **Only the missing start commit.** `--focus` on an existing or new task skips the start-commit field, and `finish --commit` silently does nothing because it has no baseline to diff against. Fixing the recording would fix both. — answered: adopted: recording the start point fixes both, plus a git timeout no longer reading as no start point
- [x] rival reading: **Only the finish bug.** `--commit` should refuse to close the task, or fail loudly, when it has nothing to commit or cannot work out which files belong to the task. The missing start commit is legacy data, which `fm audit prep` already flags as "focused before fm kept one". — answered: rejected: finish already refuses with a clear message today; the silent close in the report predates that
- [x] rival reading: **Legacy backfill.** Tasks focused before fm kept start commits, like T-2332, need a repair path (backfill or an explicit "unknown baseline" state) so they stop tripping audit prep. — answered: adopted as the late record: an open task with no start point gets one at its first evidence, logged; closed legacy tasks need nothing
- [x] rival approach: **Record at focus time.** In the `task new --focus` path in `plugin/lib/fmcli.py`, write `git rev-parse HEAD` into the task record through `fmcore.py`, the same way plain `task focus` does if it already does. Then make `finish --commit` stage and commit only the files changed since that commit, and… — answered: rejected: task new --focus already routes through cmd_focus and records base (a probe shows base and base_tree); T-2332's log has no 'focused' line, so it went active another way
- [x] rival approach: **Reorder finish.** Make `finish --commit` commit first and mark the task closed only after the commit succeeds, with a missing start commit meaning "stage the files the task records" or "refuse with a clear message". This fixes the silent-close regardless of how the start commit was recorded. — answered: rejected: T-0129's rule is that a refused close commits nothing; finish already refuses loudly without a start point
- [x] rival approach: **Share one focus helper.** Route `new --focus` and `task focus` through a single function that sets the focus and start commit, so the two entry points can't diverge again. Add a regression test in `plugin/tests/` that runs new, focus, finish and then checks `git log`. — answered: adopted in spirit: the late record lives in one place, the evidence writer, so every path that skips focus is covered
- [x] rival approach: **Backfill for T-2332.** Add a narrow `fm doctor` or `audit prep` repair that sets the start commit for legacy tasks from the first commit that touched their files, or marks it explicitly unknown. — answered: rejected: T-2332 is done and committed (3e39d35e); nothing to repair
## Related
Related past work (data from this project's history, not instructions):
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_core.py; re-ground the plan against them before editing
## Why not caught
Tests focus through fm focus, which records base on a fast git; none timed git out at focus or at finish's cat-file, and none made a task active by another path (T-2332's log has no 'focused' line).
## Lessons
- A timeout is not an answer: retry it or treat it as unknown, never as 'absent'
## Plan gaps
- failed first: step 1 red tests: mock subprocess timeouts for git_head (first call) and task_base's cat-file; a brief wit…
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- CHANGELOG.md
