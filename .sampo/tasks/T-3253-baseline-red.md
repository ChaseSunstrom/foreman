---
id: T-3253
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/tests/test_hunks.py, CHANGELOG.md]
depends_on: []
source: baseline
created: 2026-11-06T00:12:32Z
updated: 2026-11-06T00:14:58Z
trigger: baseline
trigger_key: ecd9e4a5d8fd7772
baseline: true
base: 1abcaddff1f0976804e109c8dc7fdaed858a4e0f
base_tree: f73da2d5e1c76b3a5ff20ef38f18723dfd79d458
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T00:13:20Z
plan0_scope: [plugin/tests/test_hunks.py, CHANGELOG.md]
verified: strong
unproven: [meaning, ui-unshot]
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_hunks.Ablate.test_a_slow_run_is_cut_at_the_deadline. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_hunks.Ablate's deadline test proves the cut without a wall-clock bar a loaded machine breaks — verify with `python3 plugin/tests/run.py test_hunks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test's sleep 60 s and its bar 30 s: the cut still shows (uncapped is 60 s+), load can't fail it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hunks` → exit 0 · Ran 13 tests in 2.8s (10 jobs, 16 at a time; slowest: Hunks 2s, Ablate.test_a_slow_run_is_cut_at_the_deadline 2s, Ablate.test_names_the_untested_hunk 1s) / OK [ran] [tree e4289656610a] [world 2f1906870a] (2026-11-06T00:13:25Z)
- (ac 1) `python3 plugin/tests/run.py test_hunks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T00:13:25Z [ran] [tree e4289656610a] [world 2f1906870a] (2026-11-06T00:13:36Z)
- (audit edge) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → a close under load 60 took ~5-10 s, the bar is 30 s; a missing cut runs 60 s+ and fails [tree e4289656610a] (2026-11-06T00:13:36Z)
- (audit intent) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → the test proves FM_ABLATE_BUDGET cuts a slow ablation run, not the close's speed [tree e4289656610a] (2026-11-06T00:13:36Z)
- (audit self) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → no findings [tree e4289656610a] (2026-11-06T00:13:36Z)
- (audit edge) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → a close under load 60 took ~5-10 s, the bar is 30 s; a missing cut runs 60 s+ and fails [tree e4289656610a] (2026-11-06T00:14:16Z)
- (audit intent) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → the test proves FM_ABLATE_BUDGET cuts a slow ablation run, not the close's speed [tree e4289656610a] (2026-11-06T00:14:16Z)
- (audit self) `self: one test's bar changed; the deadline still proven by a 60 s sleep against a 30 s bar` → no findings [tree e4289656610a] (2026-11-06T00:14:16Z)
## Log
- 2026-11-06T00:12:32Z created
- 2026-11-06T00:13:11Z planned: it has criteria and steps
- 2026-11-06T00:13:19Z set type=FIX, tier=S
- 2026-11-06T00:13:19Z set scope=['plugin/tests/test_hunks.py', 'CHANGELOG.md']
- 2026-11-06T00:13:20Z focused
- 2026-11-06T00:13:20Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T00:14:14Z scope: mods/foreman-ui/hooks/register.tsx is the T-3163 builder's edit in its own worktree (same session), not this task's; main's copy is unchanged
- 2026-11-06T00:14:55Z done
- 2026-11-06T00:14:58Z committed 4a79fe32 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- T-2436 [FIX M, dropped, 0 steps] Baseline red:…
- T-2529 [FIX S, done, 2 steps] The exam drops the package kind on a host whose Python has no setuptools, as its docstring promises — lesson: a gate that runs on one inter…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- the similar finished task took 2 steps
- start here (files T-2529 touched): plugin/tests/test_exam.py, plugin/lib/fmexam.py, CHANGELOG.md
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
The fix is in the test itself, so sampo task prove can't split it. Red: sampo ship's scratch-tree run at load 60 on 16 CPUs failed test_hunks.Ablate.test_a_slow_run_is_cut_at_the_deadline (the whole close took over 5 s), while two reruns at load 26 passed: the bar timed the close, not the cut. Green: python3 plugin/tests/run.py test_hunks, 13 tests OK; uncapped, the 60 s sleep still fails the 30 s bar, so the cut stays proven.
## Why not caught
The bar was set on a quiet machine; the ship's scratch run was the first at load 60
## Lessons
- A wall-clock bar must sit far from both the load-inflated pass time and the uncapped fail time; 5 s against a 5 s sleep had no margin on a busy box
## Files touched
- mods/foreman-ui/hooks/register.tsx
- plugin/tests/test_hunks.py
