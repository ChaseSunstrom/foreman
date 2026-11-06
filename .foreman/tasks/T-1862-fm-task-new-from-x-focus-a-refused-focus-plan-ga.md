---
id: T-1862
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T20:10:37Z
updated: 2026-10-28T20:35:01Z
base: 17149151c7eaaf50691df494c0708ee755a576e7
base_tree: 168b2178479eb8413b9f4d53a566e9b6a482b914
plan0_at: 2026-10-28T20:24:35Z
plan0_scope: []
verified: strong
---
# fm task new --from re-plans a planned, unstarted task
## Raw request
> fm task new --from X --focus: a refused focus (plan gate) leaves X planned, and --from then refuses a planned task, so the missing sections can't be added; check the gate before the status change, or let --from re-plan a planned, unstarted task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] --from on a planned task (a refused --focus left it there) adds the missing sections and focuses; a started task is still refused — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then one-line status check
## Resume here
<!-- auto -->
- 2026-10-28T20:33:31Z steps 1/1 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/tests/test_cli.py
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 123 tests in 40.3s (37 classes, 16 at a time; slowest: TaskLifecycle 40s, AuditPrep 17s, StateViews 17s) / FAILED (1 classes) [ran] [tree ee259d1d783e] (2026-10-28T20:26:50Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 123 tests in 23.4s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree ee563ee2d004] (2026-10-28T20:29:21Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 123 tests in 24.9s (37 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 68b2e78f43c6] (2026-10-28T20:30:25Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 123 tests in 24.1s (37 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree 68b2e78f43c6] (2026-10-28T20:30:25Z)
- (audit self) `read the guard and every path into a planned status (focus sets base; tidy reopen keeps it)` → only a planned task with no start commit passes; active, done, dropped and focused-then-parked tasks are still refused [tree 68b2e78f43c6] (2026-10-28T20:30:31Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 123 tests in 23.3s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree 68b2e78f43c6] (2026-10-28T20:34:58Z)
- (audit self) `self: the guard admits only planned tasks with no base (never focused); active/done/blocked still refused; test covers re-plan then refusal once active` → no findings [tree 68b2e78f43c6] (2026-10-28T20:34:58Z)
## Log
- 2026-10-28T20:10:37Z created
- 2026-10-28T20:14:38Z planned from capture
- 2026-10-28T20:24:34Z focused
- 2026-10-28T20:35:00Z done
- 2026-10-28T20:35:01Z committed 1c85af03 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261016-round4: 195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are rela…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- T-1849 [FEATURE M, done, 2 steps] 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16 — lesson: A playbook trim can delete text a …
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Lessons
- a refused --focus leaves an M task planned; --from must accept planned-never-started, keyed on meta base
## Plan gaps
- failed first: step 1 test then one-line status check
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
