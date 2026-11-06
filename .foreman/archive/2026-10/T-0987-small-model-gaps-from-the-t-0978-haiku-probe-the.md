---
id: T-0987
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmmap.py,plugin/lib/fmhooks.py,plugin/lib/fmcli.py,plugin/tests/test_firstrun_shell.py,plugin/tests/test_hooks.py,plugin/tests/test_cli.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:09:40Z
updated: 2026-10-15T23:14:34Z
base: b6158b64802d6b77b3985528739140e2bac1bf8f
base_tree: 9086caa53cfcbc6cd33b11148130e52c511202ef
verified: strong
---
# Small-model gaps from the T-0978 Haiku probe: the repo's own test runner, for-loop waits, unknown task ids
## Raw request
> Small-model gaps from the T-0978 Haiku probe: the repo's own test runner, for-loop waits, unknown task ids
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmmap gates offer a repo's own runner script (tests/run.py, run_tests.py) first; a foreground for-loop that sleeps ≥5 s is refused like until/while; an unknown task id names the active and newest open ids — verify with `python3 plugin/tests/run.py test_firstrun_shell test_hooks test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] fixes
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_firstrun_shell test_hooks test_cli` → ✗ exit 1 · Ran 254 tests in 73.1s (50 classes, 16 at a time; slowest: Stop 73s, TaskLifecycle 57s, PreToolUse 53s) / FAILED (3 classes) [ran] [tree e384c6b4da9a] (2026-10-15T23:11:10Z)
- (step 2) `python3 plugin/tests/run.py test_firstrun_shell test_hooks test_cli` → exit 0 · Ran 254 tests in 41.1s (50 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 29s, PreToolUse 26s) / OK [ran] [tree 06d206057bcf] (2026-10-15T23:13:00Z)
- (ac 1) `python3 plugin/tests/run.py test_firstrun_shell test_hooks test_cli` → exit 0 · Ran 254 tests in 42.7s (50 classes, 16 at a time; slowest: Stop 43s, TaskLifecycle 30s, PreToolUse 25s) / OK [ran] [tree 4430e0dcb0ac] (2026-10-15T23:14:32Z)
- (audit edge) `self: three small changes each with a red→green test; the for-loop deny keeps 'for f in a b; do echo; done' and short sleeps allowed (existing subtests)` → a for loop without sleep or with sleep <5 s still runs; no runner script → old gate order; no open tasks → plain 'no task' message [tree 4430e0dcb0ac] (2026-10-15T23:14:32Z)
- (audit self) `self: three small changes each with a red→green test; the for-loop deny keeps 'for f in a b; do echo; done' and short sleeps allowed (existing subtests)` → no findings [tree 4430e0dcb0ac] (2026-10-15T23:14:32Z)
## Log
- 2026-10-15T23:09:40Z created
- 2026-10-15T23:09:40Z focused
- 2026-10-15T23:14:33Z done
- 2026-10-15T23:14:34Z committed 3f282cf (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0809 [FIX S, dropped, 2 steps] fm task prove treats only test files as tests, not every file in a tests folder
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py, plugin/tests/test_map.py
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_cli.py
- plugin/tests/test_hooks.py
- plugin/tests/test_firstrun_shell.py
- plugin/lib/fmmap.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
