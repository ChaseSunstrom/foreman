---
id: T-1364
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T04:44:35Z
updated: 2026-10-21T06:31:02Z
base: fbb2a0b25f6108f464b99da21a4a8696693ce931
base_tree: 19add743662cd58d2c0dd3b36a40cbced78af086
plan0_at: 2026-10-21T06:21:31Z
plan0_scope: []
verified: strong
---
# fm task new --from replaces a capture's criteria and steps with the ones given, never appends
## Raw request
> Brief steps and criteria duplicate when a plan revision is merged into the brief (T-1315 had steps 1-3 repeated as 4-6)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] planning a capture that already has criteria and steps with fm task new --from ID --ac … --step … leaves exactly the criteria and steps given; a --from with no --ac keeps the capture's own — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: --from on a capture with criteria and steps
2. [x] task_new's plan(): with --from, --ac and --step replace the capture's sections
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli -k test_planning_a_capture_replaces` → ✗ exit 1 · Ran 105 tests in 55.8s (29 classes, 16 at a time; slowest: TaskLifecycle 56s, StateViews 24s, AuditPrep 20s) / FAILED (1 classes) [ran] [tree b11820331c7c] (2026-10-21T06:22:37Z)
- (ac 1) `python3 plugin/tests/run.py test_cli 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error" | head` → exit 0 · OK [ran] [tree 1b944efe4832] (2026-10-21T06:23:48Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_bookkeeping test_session` → exit 0 · Ran 146 tests in 65.3s (52 classes, 16 at a time; slowest: TaskLifecycle 65s, StateViews 30s, AuditPrep 26s) / OK [ran] [tree 1b944efe4832] (2026-10-21T06:25:01Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 105 tests in 54.7s (29 classes, 16 at a time; slowest: TaskLifecycle 53s, StateViews 23s, AuditPrep 19s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1b944efe4832] (2026-10-21T06:26:48Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 105 tests in 50.8s (29 classes, 16 at a time; slowest: TaskLifecycle 51s, StateViews 21s, AuditPrep 18s) / OK [ran] [tree 1b944efe4832] (2026-10-21T06:26:48Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 105 tests in 50.4s (29 classes, 16 at a time; slowest: TaskLifecycle 50s, StateViews 22s, AuditPrep 18s) / OK [ran] [tree ab079f9c6c55] (2026-10-21T06:27:53Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 105 tests in 50.4s (29 classes, 16 at a time; slowest: TaskLifecycle 50s, StateViews 21s, AuditPrep 17s) / OK [ran] [tree ab079f9c6c55] (2026-10-21T06:28:44Z)
- (audit edge) `self: read the diff; set_section clears only the sections a --ac or --step replaces, and only with --from; a --from with neither keeps the capture's own (tested)` → --from with --ac only keeps the capture's steps, and the reverse; a fresh task (no --from) is untouched [tree ab079f9c6c55] (2026-10-21T06:28:44Z)
- (audit self) `self: read the diff; set_section clears only the sections a --ac or --step replaces, and only with --from; a --from with neither keeps the capture's own (tested)` → no findings [tree ab079f9c6c55] (2026-10-21T06:28:44Z)
## Log
- 2026-10-21T04:44:35Z created
- 2026-10-21T06:11:46Z planned from capture
- 2026-10-21T06:12:23Z grounded: fmcli.task_new's plan() calls b.add_ac/b.add_step onto the capture's existing sections when --from is given (T-1315 and T-1331 were both 'planned from capture' at 03:43 and got every criterion and step twice); fix: with --from, --ac and --step each replace their section first. Test drafted (scratchpad t1364_test.txt). Second plan skipped: S, cause read in code
- 2026-10-21T06:21:31Z focused
- 2026-10-21T06:26:56Z scope: CHANGELOG.md — its line
- 2026-10-21T06:30:59Z done
- 2026-10-21T06:31:02Z committed 330d4ea3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Whole-repo cleanup sweep (Foreman's own, T-0364) (skills/playbooks/references/clean/repo-sweep.md)
- T-1071 [FEATURE M, done, 3 steps] Night gardening: fm night composts merged or abandoned worktrees and branches and consolid — lesson: An unattended job runs the narrowe…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- decision 2026-09-26: fm sync keeps the automatic import at session start and before fm commands: imported content can't grant, mark runs, count as audits or take focus, …
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- Turning one record into another must say per field whether the new value replaces or extends; add_* on an existing record extends by default
## Plan gaps
- failed first: step 1 Failing test: --from on a capture with criteria and steps
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
