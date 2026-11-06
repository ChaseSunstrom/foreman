---
id: T-3241
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/bench_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T20:34:00Z
updated: 2026-11-05T20:55:58Z
base: 040f45d389ee49ffefd91899184eb2fe484b03c8
base_tree: c89f9cf83effd77b95da7a8db4fafbaedc3a9279
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T20:53:40Z
plan0_scope: [plugin/tests/bench_hooks.py, CHANGELOG.md]
verified: strong
unproven: [meaning]
---
# CI ubuntu flake: test_bench_hooks.Modules teardown hit OSError 39 Directory not empty on…
## Raw request
> CI ubuntu flake: test_bench_hooks.Modules teardown hit OSError 39 Directory not empty on fhome/state/projects/app-* (run 42086502367): something still writes the project's state while TemporaryDirectory cleans up; wait for it or ignore_errors
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the hook bench runs its scratch project with background work off and its temp folders' cleanup tolerates a late writer, so test_bench_hooks passes repeatedly — verify with `python3 plugin/tests/run.py test_bench_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] FOREMAN_NO_BACKGROUND=1 in the scratch env; ignore_cleanup_errors on the bench's temp folders
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 5 tests in 5.6s (5 jobs, 16 at a time; slowest: Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 5s, Modules.test_the_hook_writes_only_under_the_temp_dir 1s, Verdict 0s) / OK [ran] [tree 0b52f656751a] [world 2f1906870a] (2026-11-05T20:54:23Z)
- (step 1) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 5 tests in 5.7s (3 jobs, 16 at a time; slowest: Modules 5s, ScriptBudget 0s, Verdict 0s) / OK [ran] [tree eb483e12c1aa] [world 2f1906870a] (2026-11-05T20:55:00Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 5 tests in 5.4s (5 jobs, 16 at a time; slowest: Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 5s, Modules.test_the_hook_writes_only_under_the_temp_dir 1s, Verdict 0s) / OK [ran] [tree 525b4eec745f] [world 2f1906870a] (2026-11-05T20:55:22Z)
- (audit intent) `self: FOREMAN_NO_BACKGROUND=1 only in hook_modules (the imports bench), so the hook timing bench still measures what hooks really spawn; ignore_cleanup_errors on the bench's temp folders (run.py removes the class folder after anyway)` → the CI teardown flake can't recur from a background writer [tree 525b4eec745f] (2026-11-05T20:55:22Z)
- (audit edge) `self: FOREMAN_NO_BACKGROUND=1 only in hook_modules (the imports bench), so the hook timing bench still measures what hooks really spawn; ignore_cleanup_errors on the bench's temp folders (run.py removes the class folder after anyway)` → timing benches keep background work on, so a hook that spawns too eagerly still shows [tree 525b4eec745f] (2026-11-05T20:55:22Z)
- (audit self) `self: FOREMAN_NO_BACKGROUND=1 only in hook_modules (the imports bench), so the hook timing bench still measures what hooks really spawn; ignore_cleanup_errors on the bench's temp folders (run.py removes the class folder after anyway)` → no findings [tree 525b4eec745f] (2026-11-05T20:55:22Z)
## Log
- 2026-11-05T20:34:00Z created
- 2026-11-05T20:53:36Z planned: it has criteria and steps
- 2026-11-05T20:53:36Z set scope=['plugin/tests/bench_hooks.py', 'CHANGELOG.md']
- 2026-11-05T20:53:37Z focused
- 2026-11-05T20:53:40Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T20:55:55Z done
- 2026-11-05T20:55:58Z committed 7807c598 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1873-review: Approve with nits. The feature works as described, and the refactor of `cmd_scene` into `_builtin` keeps the existing behaviour. One MEDIUM findi…
- research long-false-done: Source: fm exam long l001 and l002, foreman arm (2026-10-31). Each goal's hidden checks were rerun on the session's kept tree the grader's way …
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- decision 2026-11-05: [costly] T-3177: don't merge the pool at cpu_count slots (2-run bench 28.2 s pooled vs 21.4 s unpooled: test jobs wait on subprocesses, so 16 slots …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
none: a teardown race seen once on CI; the bench now runs without background work and tolerates a late writer; test_bench_hooks green three times in a row here
## Why not caught
a race: it needs a background writer to outlive the hook; seen once on CI
## Lessons
- a bench that runs real hooks must switch off their background hand-offs or wait for them before cleanup
## Files touched
- plugin/tests/bench_hooks.py
- CHANGELOG.md
