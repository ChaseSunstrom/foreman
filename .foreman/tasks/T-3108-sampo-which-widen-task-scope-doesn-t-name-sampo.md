---
id: T-3108
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/which.py, plugin/tests/test_which.py]
depends_on: []
source: discovered
created: 2026-11-05T03:07:29Z
updated: 2026-11-05T08:37:09Z
base: c1d6c5442813a9ac49abb2fe47ee0c3d838fef2f
base_tree: 9ff1569cf979050a5822a80e9e20c0fd96109e25
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T03:11:37Z
plan0_scope: [plugin/lib/sampo/which.py, plugin/tests/test_which.py]
lane_stop: merged 2026-11-05T08:34:56Z
verified: strong
---
# sampo which finds the task set key forms: 'widen task scope' names sampo task set ID scope=[...], and approve and allow the same way
## Raw request
> sampo which 'widen task scope' doesn't name sampo task set ID scope=[...] (the refusal text does, the lookup doesn't): index the task set key=value forms (scope, approved, allow) in which
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo which 'widen task scope' lists 'fm task set ID scope=[...]' among its commands; 'approve a task' lists approved=true, and 'allow a guard category on a task' lists --allow — verify with `python3 plugin/tests/run.py test_which`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_which: the three needs find their task set forms
2. [x] which.commands() adds one entry per task set key form (scope, approved, allow) with a plain summary
## Resume here
released to the local lane: the 27B works T-3108 in .claude/worktrees/local-T-3108
<!-- auto -->
- 2026-11-05T03:12:07Z step 1/2: failing test in test_which: the three needs find their task set forms
- git: foreman/build; 1 uncommitted: scripts/
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 32 tests in 5.3s (6 classes, 16 at a time; slowest: Shelves 5s, Which 4s, ToolsTools 0s) / OK [ran] [tree cf2ff5a8707c] [world 2f1906870a] (2026-11-05T03:12:37Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | head -20` → exit 0 · Ran 32 tests in 6.4s (6 classes, 16 at a time; slowest: Shelves 6s, Which 5s, ToolsTools 1s) / OK [ran] [tree cf2ff5a8707c] [world 2f1906870a] (2026-11-05T03:14:52Z)
- (step 1) `python3 plugin/tests/run.py test_which 2>&1 | head -20` → exit 0 · Ran 32 tests in 6.4s (6 classes, 16 at a time; slowest: Shelves 6s, Which 5s, ToolsTools 1s) / OK [ran] [tree cf2ff5a8707c] [world 2f1906870a] (2026-11-05T03:14:52Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | tail -5` → exit 0 · Ran 32 tests in 6.8s (6 classes, 16 at a time; slowest: Shelves 6s, Which 6s, ToolsTools 1s) / OK [ran] [tree cf2ff5a8707c] [world 2f1906870a] (2026-11-05T03:15:16Z)
- (step 2) `python3 plugin/tests/run.py test_which 2>&1 | tail -5` → exit 0 · Ran 32 tests in 6.8s (6 classes, 16 at a time; slowest: Shelves 6s, Which 6s, ToolsTools 1s) / OK [ran] [tree cf2ff5a8707c] [world 2f1906870a] (2026-11-05T03:15:16Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | tail -20` → ✗ exit 1 · Ran 33 tests in 5.3s (6 classes, 16 at a time; slowest: Shelves 5s, Which 5s, ToolsTools 1s) / FAILED (1 classes: test_which.Which) [ran] [tree d90040415ff3] [world 2f1906870a] (2026-11-05T03:15:38Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | tail -10` → exit 0 · Ran 33 tests in 12.1s (6 classes, 16 at a time; slowest: Which 11s, Shelves 11s, ToolsTools 1s) / OK [ran] [tree 74bd1608f15e] [world 2f1906870a] (2026-11-05T03:16:40Z)
- (step 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 33 tests in 6.4s (6 classes, 16 at a time; slowest: Which 6s, Shelves 6s, ToolsTools 1s) / OK [ran] [tree 74bd1608f15e] [world 2f1906870a] (2026-11-05T03:21:22Z)
- (step 2) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 33 tests in 5.5s (6 classes, 16 at a time; slowest: Which 5s, Shelves 5s, ToolsTools 0s) / OK [ran] [tree 74bd1608f15e] [world 2f1906870a] (2026-11-05T03:21:28Z)
- `python3 plugin/tests/run.py test_which` → exit 0 · Ran 33 tests in 6.2s (6 classes, 16 at a time; slowest: Which 6s, Shelves 5s, ToolsTools 1s) / OK [ran] [tree 2a443c5667f9] [world 2f1906870a] (2026-11-05T08:35:52Z)
- `python3 plugin/tests/run.py test_which` → ✗ exit 1 · Ran 33 tests in 8.0s (6 classes, 16 at a time; slowest: Shelves 6s, Which 6s, ToolsTools 1s) / FAILED (1 classes: test_which.Which) (start tree + this task's tests) [ran] [tree 2a443c5667f9] [world 2f1906870a] (2026-11-05T08:36:13Z)
- `python3 plugin/tests/run.py test_which` → exit 0 · Ran 33 tests in 11.4s (6 classes, 16 at a time; slowest: Which 11s, Shelves 10s, ToolsTools 1s) / OK [ran] [tree 2a443c5667f9] [world 2f1906870a] (2026-11-05T08:36:13Z)
- (ac 1) `python3 plugin/tests/run.py test_which` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T08:36:13Z [ran] [tree 2a443c5667f9] [world 2f1906870a] (2026-11-05T08:36:16Z)
- (audit edge) `worked end to end by Smith on the local 27B (jarvis-nothink) in a local lane; the main thread reviewed the diff before merge; test_which re-run on main green; red→green proved` → sampo which finds 'widen task scope', 'approve a task' and 'grant a guard category' through the task set key forms (scope, approved, allow), each with its exact command [tree 2a443c5667f9] (2026-11-05T08:36:16Z)
- (audit intent) `worked end to end by Smith on the local 27B (jarvis-nothink) in a local lane; the main thread reviewed the diff before merge; test_which re-run on main green; red→green proved` → the first real task the local 27B built for Sampo end to end (T-3117's lane), merged after review [tree 2a443c5667f9] (2026-11-05T08:36:16Z)
- (audit self) `worked end to end by Smith on the local 27B (jarvis-nothink) in a local lane; the main thread reviewed the diff before merge; test_which re-run on main green; red→green proved` → no findings [tree 2a443c5667f9] (2026-11-05T08:36:16Z)
## Log
- 2026-11-05T03:07:29Z created
- 2026-11-05T03:11:28Z planned from capture
- 2026-11-05T03:11:29Z set approved=True
- 2026-11-05T03:11:29Z set scope=['plugin/lib/sampo/which.py', 'plugin/tests/test_which.py']
- 2026-11-05T03:11:37Z focused
- 2026-11-05T03:11:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T03:12:22Z set status=planned
- 2026-11-05T03:12:22Z handed to the local lane .claude/worktrees/local-T-3108 (Smith on jarvis-nothink); main focused it only to create the worktree
- 2026-11-05T03:12:30Z focused
- 2026-11-05T08:34:56Z merged local/T-3108 (2 file(s))
- 2026-11-05T08:34:57Z lane removed: ~/.claude/foreman/.claude/worktrees/local-T-3108
- 2026-11-05T08:35:12Z focused
- 2026-11-05T08:36:14Z scope: files outside its globs came from other tasks' merges and closes landing between its merge and this close
- 2026-11-05T08:37:09Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- research T-1573-review: Verdict:** approve with nits. I found no way for a kept value to differ from the previewed one, or for the app to stay in the previewed look afte…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_which.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/which.py, plugin/tests/test_which.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_which.py
- plugin/lib/sampo/which.py
