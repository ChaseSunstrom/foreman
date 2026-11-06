---
id: T-1349
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:39Z
updated: 2026-10-23T08:25:27Z
base: 444a6cb120a10d0d0d02d843edf7fc89979b5383
base_tree: fecc42095f906d0077cb6c7b2f3e8939a210a8cf
plan0_at: 2026-10-23T08:13:57Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code delight: a project's first closed run says so once (a brighter, longer close wave and 'first proved change in <project>'), and picking a runner says hello with its last result
## Raw request
> fm code delight (U13): a project's first closed run plays a once-only celebration (a brighter close wave, 'first proved change in <project>'); picking a runner shows a one-line hello with its last result
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] only a project's first closed run carries first_in on its closed event, and the app notes it once with a brighter close — verify with `python3 plugin/tests/run.py test_code.FirstClose test_code_tui.Delight`
- [x] picking a worker in the app names its newest run's end and age, or that it has none yet — verify with `python3 plugin/tests/run.py test_code_tui.Delight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests then _closed_before, last_run_of, the first note, the brighter wave and the picker hello
## Resume here
<!-- auto -->
- 2026-10-23T08:18:00Z step 1/1: tests then _closed_before, last_run_of, the first note, the brighter wave and the picker hello
- git: foreman/build; 4 uncommitted: plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py
- touched since last checkpoint: plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.FirstClose test_code_tui.Delight test_code_tui.Command` → ✗ exit 1 · Ran 13 tests in 7.2s (3 classes, 16 at a time; slowest: Command 7s, FirstClose 1s, Delight 0s) / FAILED (1 classes) [ran] [tree 7981e49ee6be] (2026-10-23T08:22:01Z)
- (audit intent) `self` → pass: once per project (only when no other run there ever closed), a brighter close and the note; the picker hello [tree f1aceb242aca] (2026-10-23T08:22:02Z)
- (step 1) `python3 plugin/tests/run.py test_code.FirstClose test_code.Leases test_code_tui.Delight test_code_tui.Command` → exit 0 · Ran 14 tests in 7.2s (4 classes, 16 at a time; slowest: Command 7s, Leases 2s, FirstClose 2s) / OK [ran] [tree e112a9e6fda0] (2026-10-23T08:24:02Z)
- (ac 1) `python3 plugin/tests/run.py test_code.FirstClose test_code_tui.Delight` → exit 0 · Ran 2 tests in 2.6s (2 classes, 16 at a time; slowest: FirstClose 2s, Delight 0s) / OK [ran] [tree e112a9e6fda0] (2026-10-23T08:24:06Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.Delight` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Delight 0s) / OK [ran] [tree e112a9e6fda0] (2026-10-23T08:24:06Z)
- (audit intent) `self: intent, edge` → both criteria met [tree e112a9e6fda0] (2026-10-23T08:24:06Z)
- (audit edge) `self: intent, edge` → a project whose earlier runs never closed still gets its first; the wave stays off with motion reduced or off (fx.moving); a picked runner with no runs says so; a broken events file is skipped [tree e112a9e6fda0] (2026-10-23T08:24:06Z)
- (audit self) `self: intent, edge` → no findings [tree e112a9e6fda0] (2026-10-23T08:24:06Z)
## Log
- 2026-10-21T03:47:39Z created
- 2026-10-23T08:13:48Z planned from capture
- 2026-10-23T08:13:48Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T08:13:55Z focused
- 2026-10-23T08:18:06Z paused: focus moved to T-1764
- 2026-10-23T08:21:53Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-23T08:21:53Z focused
- 2026-10-23T08:23:40Z scope: plugin/tests/test_code.py — its FirstClose test (committed with T-1764) rewrites calc.py at a new size, so a stale .pyc can't pass the check
- 2026-10-23T08:23:41Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T08:25:25Z done
- 2026-10-23T08:25:27Z committed 34c9ef5c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Rewriting a Python file at the same size within the same second lets a stale .pyc win: change the size in tests
## Plan gaps
- failed first: step 1 tests then _closed_before, last_run_of, the first note, the brighter wave and the picker hello
## Files touched
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- CHANGELOG.md
