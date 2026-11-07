---
id: T-3435
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/release.py, plugin/tests/test_ship.py]
depends_on: []
source: discovered
created: 2026-11-06T12:25:10Z
updated: 2026-11-06T16:29:47Z
base: 1f5c52c04454b3dc054a804d2913fffb11fcabb6
base_tree: 2d7e4f16be1ef9286c172ea07a38adb1b0b753ac
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T12:26:27Z
plan0_scope: []
builder_returned: 2026-11-06T12:30:08Z
lane_stop: merged 2026-11-06T12:41:39Z
verified: strong
unproven: [meaning]
lane_verified: a0f6762fe1caa0759184a50b4705d78d478a5878
---
# Sampo ship's scratch-tree full suite refuses on any red class with no flake rerun:…
## Raw request
> FIX: sampo ship's scratch-tree full suite refuses on any red class with no flake rerun: tonight at load ~20 it refused on test_close_gates.CloseGates and test_check_paths.CheckSkip forkcli socket timeouts (green alone), and filed baseline task T-3434; rerun the red classes alone after a load wait (as the post-merge suite does, T-3216) and refuse only on classes still red alone; the affected-first step gets the same rerun
## Interpretation
Reading 1: rerun red classes alone in both ship steps, refuse only on still-red. Reading 2 (ruled out): retry the whole suite, which costs minutes and hides which class flaked.
## Assumptions (confidence)
## Acceptance criteria
- [x] red-then-green-alone ship pushes and names the flaky class; red alone still refuses — verify with `python3 plugin/tests/run.py test_ship.Ship`
## Non-goals
## Approach (options → choice → why)
1) Copy pm_verify logic into release: likely outcome drift between two copies. 2) Use what exists: small release helper calling lanes.pm_classes/pm_rerun_cmd; likely outcome flakes pass, real reds refuse. 3) Do less: do nothing and rerun ship by hand; fails if load stays high. Choice 2 (85%): reuses the post-merge helpers, reruns only red classes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] rerun red classes alone in both ship steps
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship.Ship` → exit 0 · Ran 43 tests in 33.6s (1 jobs, 16 at a time; slowest: Ship 30s) / OK [ran] [tree 58a7ff34f40e] [world 2f1906870a] (2026-11-06T12:27:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_release test_rename_scan test_ship && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 318 tests in 39.5s (115 jobs, 16 at a time; slowest: Release 9s, ReleaseProofWithoutSetuptools 8s, RenameScan 7s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree 58a7ff34f40e] [world 2f1906870a] (2026-11-06T12:28:18Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_ship` → exit 0 · Ran 63 tests in 28.5s (55 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 4s, ShipNext 3s, RenameScan.test_no_library_code_hardcodes_the_old_mirror_name 3s) / OK [ran] [tree bd2895499f62] [world 2f1906870a] (2026-11-06T12:29:57Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 94e4bcdb7a59] (2026-11-06T12:41:43Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 52 tests in 279.1s (2 jobs, 16 at a time; slowest: Ship 27s, ShipNext 2s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 94e4bcdb7a59] [world 2f1906870a] (2026-11-06T12:48:26Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 52 tests in 117.2s (2 jobs, 16 at a time; slowest: Ship 36s, ShipNext 2s) / OK [ran] [tree 94e4bcdb7a59] [world 2f1906870a] (2026-11-06T12:48:26Z)
- (ac 1) `python3 plugin/tests/run.py test_ship.Ship` → exit 0 · Ran 43 tests in 102.5s (43 jobs, 16 at a time; slowest: Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_check 3s, Ship.test_a_tower_update_pushed_while_the_ship_tests_is_re_picked_ [ran] [tree 94e4bcdb7a59] [world 2f1906870a] (2026-11-06T12:50:13Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 94e4bcdb7a59] (2026-11-06T12:50:13Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 94e4bcdb7a59] (2026-11-06T12:50:13Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 94e4bcdb7a59] (2026-11-06T12:50:13Z)
## Log
- 2026-11-06T12:25:10Z created
- 2026-11-06T12:26:07Z planned: it has criteria and steps
- 2026-11-06T12:26:26Z focused
- 2026-11-06T12:26:27Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T12:41:39Z merged worktree-agent-a9a62c5f5ec8b7dd2 (2 file(s))
- 2026-11-06T12:41:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9a62c5f5ec8b7dd2
- 2026-11-06T12:41:41Z focused
- 2026-11-06T12:41:43Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/release.py', 'plugin/tests/test_ship.py']
- 2026-11-06T12:41:43Z scope: widened at merge to the reviewed lane's own diff (a0f6762fe), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T12:53:32Z done
- 2026-11-06T12:53:36Z committed b61801502 (1 file)
- 2026-11-06T16:29:47Z verified: the full suite is green on 1078ed22d, which contains a0f6762fe
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3425 [FIX M, active, 1 steps] The post-merge suite auto-reverted T-3410's docs-only merge (0cad059e5: a MASTER.md…
- T-3417 [PERFORMANCE M, done, 1 steps] test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight… — lesson: none: a reviewed builder lane; i…
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- the similar finished task took 1 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/sampo/release.py
- CHANGELOG.md
