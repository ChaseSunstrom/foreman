---
id: T-2323
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T11:45:29Z
updated: 2026-10-31T12:10:00Z
builder_model: sonnet
base: 75b9e49a92e31788eeda9dfda04768d83193cb1a
base_tree: 002d632cd3b751a9a120d6c3f23bafce6976620e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T11:46:15Z
plan0_scope: []
verified: strong
---
# fm ship runs the affected tests over its range before the full suite, so a red one stops it in minutes
## Raw request
> fm ship failed 3 times today on causes unrelated to the shipped change's intent (load flakes twice, a stray rename once), ~15 min each: before the full suite, run fm check --affected over the ship range (seconds to a few minutes) so a red affected test stops the ship early with its class named
## Interpretation
Three ships failed today in the full suite (~15 min each) on causes an affected run over the shipped range would have shown in a few minutes (a stray rename's NameError in test_verify_strength; load flakes).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship runs fm check's affected-test selection over origin/main..HEAD in the scratch tree before the full suite; a red affected run stops the ship with the failing classes named and nothing pushed; a green one goes on to the full suite as before — verify with `python3 plugin/tests/run.py test_ship test_release`
## Non-goals
## Approach (options → choice → why)
Options: 1) reuse fm check's affected() over the ship range first; 2) shard the full suite and fail fast on the first red shard; 3) skip the full suite when affected is green. Choice 1: reuses what exists, catches the common case in minutes; 3 would ship untested code paths.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test with a stubbed affected run returning red: ship stops before the full suite and names it; green: the full suite runs
2. [x] Call the existing affected() selection for the ship range inside ship's scratch tree before its test command
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 28 tests in 72.2s (1 classes, 16 at a time; slowest: Ship 71s) / OK [ran] [tree 93d82b995f32] (2026-10-31T11:49:53Z)
- (step 2) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 31 tests in 26.1s (5 classes, 16 at a time; slowest: Release 25s, BoardVerbs 8s, Release 3s) / OK [ran] [tree 93d82b995f32] (2026-10-31T11:50:20Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused test_release test_robustness test_ship test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 255 tests in 90.9s (54 classes, 16 at a time; slowest: Ship 90s, TaskLifecycle 74s, Release 39s) / FAILED (1 classes: test_robustness.Robustness) [ran] [tree 93d82b995f32] (2026-10-31T11:51:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused test_release test_robustness test_ship test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 255 tests in 73.0s (54 classes, 16 at a time; slowest: Ship 71s, TaskLifecycle 64s, Release 46s) / FAILED (1 classes: test_robustness.Robustness) [ran] [tree 93d82b995f32] (2026-10-31T11:53:42Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused test_release test_robustness test_ship test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [39.34s] [ran] [tree 93d82b995f32] (2026-10-31T12:00:58Z)
- (step 1) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 59 tests in 22.9s (6 classes, 16 at a time; slowest: Ship 23s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 22948685983d] (2026-10-31T12:07:21Z)
- (step 2) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 59 tests in 22.8s (6 classes, 16 at a time; slowest: Ship 23s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 22948685983d] (2026-10-31T12:07:44Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 28 tests in 21.2s (1 classes, 16 at a time; slowest: Ship 20s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 22948685983d] (2026-10-31T12:08:29Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 28 tests in 23.0s (1 classes, 16 at a time; slowest: Ship 23s) / OK [ran] [tree 22948685983d] (2026-10-31T12:08:29Z)
- (ac 1) `python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 59 tests in 25.2s (6 classes, 16 at a time; slowest: Ship 25s, Release 13s, BoardVerbs 4s) / OK [ran] [tree 43c819fdfd94] (2026-10-31T12:09:09Z)
- (audit intent) `self-review of the merged diff: affected() takes since= (the ship's main) and then ignores the active task; _affected_first runs that selection in the scratch tree with the shipped tree's env and a 900 s cap, inside the ship_testing marker; red raises the ship error naming FAIL/ERROR classes; a selection error or no linked test goes straight to the full suite; tests cover red (no full suite, main unchanged, grant kept) and green` → a ship that would go red on a linked test now stops in minutes instead of after the 15-minute suite [tree 43c819fdfd94] (2026-10-31T12:09:09Z)
- (audit edge) `self-review of the merged diff: affected() takes since= (the ship's main) and then ignores the active task; _affected_first runs that selection in the scratch tree with the shipped tree's env and a 900 s cap, inside the ship_testing marker; red raises the ship error naming FAIL/ERROR classes; a selection error or no linked test goes straight to the full suite; tests cover red (no full suite, main unchanged, grant kept) and green` → no affected command or no linked test skips to the full suite; a hung affected run is cut at 900 s and counts as red; class names depend on unittest's FAIL: format, and the ship still stops without them [tree 43c819fdfd94] (2026-10-31T12:09:09Z)
- (audit operator) `self-review of the merged diff: affected() takes since= (the ship's main) and then ignores the active task; _affected_first runs that selection in the scratch tree with the shipped tree's env and a 900 s cap, inside the ship_testing marker; red raises the ship error naming FAIL/ERROR classes; a selection error or no linked test goes straight to the full suite; tests cover red (no full suite, main unchanged, grant kept) and green` → one extra run of a few test files per ship; the full suite is unchanged [tree 43c819fdfd94] (2026-10-31T12:09:09Z)
## Log
- 2026-10-31T11:45:29Z created
- 2026-10-31T11:45:50Z planned from capture
- 2026-10-31T11:45:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2323.builder.md
- 2026-10-31T11:46:14Z focused
- 2026-10-31T11:46:15Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T12:06:56Z merged worktree-agent-a8de7ac87459c7e9f (3 file(s))
- 2026-10-31T12:06:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8de7ac87459c7e9f
- 2026-10-31T12:06:56Z focused
- 2026-10-31T12:06:57Z criterion 1 verify: `python3 plugin/tests/run.py test_release` → `python3 plugin/tests/run.py test_ship test_release`
- 2026-10-31T12:08:41Z scope: plugin/lib/fmrelease.py (_affected_first, ship), plugin/lib/fmcli.py (affected since=), plugin/tests/test_ship.py, MASTER.md, CHANGELOG.md
- 2026-10-31T12:09:58Z done
- 2026-10-31T12:10:00Z committed 7cd5aac8 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1462 [PERFORMANCE S, done, 2 steps] fm task finish names its slowest run
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-2311 [FIX S, done, 1 steps] fm task evidence --repeat works again: _repeat_runs calls run_command with its own root — lesson: A scripted rename spreads past the functi…
- decision 2026-10-30: [revisited: feel free to push to main] [cites: user steer 2026-10-29: push to main without asking] [check: python3 plugin/tests/run.py test_ship.Shi…
- similar finished tasks took 1–2 steps
## Lessons
- Run the cheap, likely-to-fail check first: the full suite is the last gate, not the first
## Files touched
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/tests/test_ship.py
- MASTER.md
- CHANGELOG.md
