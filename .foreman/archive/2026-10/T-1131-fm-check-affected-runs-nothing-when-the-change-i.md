---
id: T-1131
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T08:36:58Z
updated: 2026-10-16T09:20:33Z
base: d19ea2c19f613fb496a175fe76b4e76c804401e6
base_tree: 7f52c0c5b488e172b8ae0af56c6a1f187d2eacdb
plan0_at: 2026-10-16T09:15:53Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# Fm check --affected runs nothing when the change is only a new test file ("No tests linked
## Raw request
> fm check --affected runs nothing when the change is only a new test file ("No tests linked to the 1 changed file(s)", T-1050 lane: mods/foreman-ui/tests/pane-sweep.test.tsx): a changed test file should be its own linked test
## Interpretation
The changed test file was found (T-0875 includes changed test files), but _runnable dropped it: the project's affected template is Python's runner, and a .tsx test can't run through it. So fm check --affected said 'No tests linked' and ran nothing, silently.
## Assumptions (confidence)
## Acceptance criteria
- [x] a changed test file the template can't run is named in fm check --affected's output instead of 'No tests linked' — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
Say it. When the template's runner filters out changed test files, the result names them ('N changed test file(s) this template can't run: …; run their suite'), in text and JSON. Per-extension templates (an affected command per runner) are captured as a follow-up M.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then name the filtered-out test files
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_changed_test_the_template_cannot_run_is_named test_cli` → ✗ exit 1 · Ran 101 tests in 26.0s (28 classes, 16 at a time; slowest: TaskLifecycle 26s, StateViews 12s, AuditPrep 10s) / FAILED (1 classes) [ran] [tree 57518d8ebce0] (2026-10-16T09:16:36Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_ambient test_map` → exit 0 · Ran 112 tests in 47.9s (32 classes, 16 at a time; slowest: TaskLifecycle 48s, StateViews 19s, AuditPrep 17s) / OK [ran] [tree a7eb6eec9491] (2026-10-16T09:17:36Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 101 tests in 52.8s (28 classes, 16 at a time; slowest: TaskLifecycle 52s, StateViews 24s, AuditPrep 17s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 405e02a1877b] (2026-10-16T09:19:19Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 101 tests in 42.2s (28 classes, 16 at a time; slowest: TaskLifecycle 42s, StateViews 20s, AuditPrep 17s) / OK [ran] [tree 405e02a1877b] (2026-10-16T09:19:19Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 101 tests in 23.6s (28 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 10s, AuditPrep 9s) / OK [ran] [tree 405e02a1877b] (2026-10-16T09:19:43Z)
- (audit self) `self: a changed test file is always in the affected set unless the runner filter drops it, so 'changed test file not in tests' is exactly the unrunnable set; named in text and JSON (unrunnable), with or without other linked tests` → no findings [tree 405e02a1877b] (2026-10-16T09:19:43Z)
## Log
- 2026-10-16T08:36:58Z created
- 2026-10-16T08:52:15Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_affected.py', 'CHANGELOG.md']
- 2026-10-16T08:52:22Z criterion 1 verify: `python3 plugin/tests/run.py test_affected` → `python3 plugin/tests/run.py test_cli`
- 2026-10-16T08:52:22Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-16T09:15:52Z focused
- 2026-10-16T09:17:43Z scope: CHANGELOG.md — release note
- 2026-10-16T09:20:32Z done
- 2026-10-16T09:20:33Z committed 56f910e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- decision 2026-10-16: Pane remake drops spend-by-feature, bench, research, vetoes, files churn and the week's skills list; skill calls get a lane in Activity; small meter…
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A filter that silently drops input must say what it dropped
## Plan gaps
- failed first: step 1 Test then name the filtered-out test files
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
