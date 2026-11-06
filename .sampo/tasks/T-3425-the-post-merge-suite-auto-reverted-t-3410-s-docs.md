---
id: T-3425
type: FIX
tier: M
status: done
priority: urgent
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-11-06T10:32:50Z
updated: 2026-11-06T12:40:36Z
base: 45804224777bebea4d4b8fd9f7374ddf631a46d9
base_tree: 1dd49205a84d78a4b7a802302d6ffeb25b24288a
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T10:34:35Z
plan0_scope: []
builder_returned: 2026-11-06T11:18:15Z
lane_stop: merged 2026-11-06T12:37:48Z
verified: strong
---
# The post-merge suite auto-reverted T-3410's docs-only merge (0cad059e5: a MASTER.md…
## Raw request
> FIX!: the post-merge suite auto-reverted T-3410's docs-only merge (0cad059e5: a MASTER.md bullet) because test_check_paths.CheckSkip, test_cli.AffectedPairs and test_close_gates.CloseGates were red in the full suite AND alone at load ~30 while green on the parent; a merge can only be blamed for classes its changed files reach (sampo map / affected selection): unreached red classes count as flaky, the alone-rerun waits for load like gates do, and the revert note names the reach check
## Interpretation
Reading 1: a merge is blamed only for red classes its changed files reach, via the affected selection. Reading 2 (ruled out): disable the revert under load, which would hide real reds.
## Assumptions (confidence)
## Acceptance criteria
- [x] docs-only merge with unreached red class is not reverted; reaching merge still is — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
1) Reuse cli.affected with explicit files and a tree, so no new map; likely outcome: same reach as sampo check --affected. 2) A new reach map in lanes, duplicating hubs and pairs; fails if it drifts from affected. 3) Only skip docs-only merges by extension; fails on load flakes in code merges. Choice 1 (80%): same selection as sampo check --affected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first, then implement reach in pm_verify
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 20 tests in 9.3s (1 jobs, 16 at a time; slowest: PostMergeVerify 6s) / FAILED (1 classes: test_lanes.PostMergeVerify) [ran] [tree ce4c90663e56] [world 2f1906870a] (2026-11-06T10:35:12Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify 2>&1 | grep -E "^(FAIL|ERROR)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (2 classes: test_lanes.PostMergeVerify.test_a_merge_is_not_blamed_for_a_red_class_its_files_do_not_reach, test_lanes.PostMergeVerify.test_a_merge_whose_file_reaches_the_re [ran] [tree ce4c90663e56] [world 2f1906870a] (2026-11-06T10:35:57Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 20 tests in 4.2s (1 jobs, 16 at a time; slowest: PostMergeVerify 4s) / FAILED (1 classes: test_lanes.PostMergeVerify) [ran] [tree 40f03e1ef205] [world 2f1906870a] (2026-11-06T10:36:58Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify 2>&1 | grep -B3 -A18 "^FAIL:" | head -50` → ✗ exit 1 · <sys>:0: ResourceWarning: unclosed file <_io.BufferedReader name=4> / Ran 20 tests in 4.1s (1 jobs, 16 at a time; slowest: PostMergeVerify 4s) [ran] [tree 40f03e1ef205] [world 2f1906870a] (2026-11-06T10:37:05Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 20 tests in 4.1s (1 jobs, 16 at a time; slowest: PostMergeVerify 4s) / OK [ran] [tree 66a8fcc006c4] [world 2f1906870a] (2026-11-06T10:37:14Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 713 tests in 26.4s (144 jobs, 16 at a time; slowest: LaneRecovery 26s, Lanes 21s, TaskLifecycle 16s) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree 66a8fcc006c4] [world 2f1906870a] (2026-11-06T10:37:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.31s] [ran] [tree d4f5590a807d] [world 2f1906870a] (2026-11-06T10:38:38Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 22 tests in 8.0s (1 jobs, 16 at a time; slowest: PostMergeVerify 6s) / OK [ran] [tree af328d69b8da] [world 2f1906870a] (2026-11-06T10:55:36Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_twins test_lanes test_left_out test_models test_rename_scan test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.53s] [ran] [tree 3bdbbbc6ea11] [world 2f1906870a] (2026-11-06T10:56:43Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 24 tests in 3.6s (1 jobs, 16 at a time; slowest: PostMergeVerify 3s) / OK [ran] [tree 63cb5d127c55] [world 2f1906870a] (2026-11-06T11:17:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_twins test_lanes test_left_out test_models test_rename_scan test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.01s] [ran] [tree 63cb5d127c55] [world 2f1906870a] (2026-11-06T11:18:07Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 2d7e4f16be1e] (2026-11-06T12:37:51Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 24 tests in 18.5s (1 jobs, 16 at a time; slowest: PostMergeVerify 5s) / OK [ran] [tree 2d7e4f16be1e] [world 2f1906870a] (2026-11-06T12:38:18Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 2d7e4f16be1e] (2026-11-06T12:38:18Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 2d7e4f16be1e] (2026-11-06T12:38:18Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 2d7e4f16be1e] (2026-11-06T12:38:18Z)
## Log
- 2026-11-06T10:32:50Z created
- 2026-11-06T10:34:15Z planned: it has criteria and steps
- 2026-11-06T10:34:33Z focused
- 2026-11-06T10:34:35Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T12:37:48Z merged worktree-agent-a1188eccec4ddfb02 (2 file(s))
- 2026-11-06T12:37:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1188eccec4ddfb02
- 2026-11-06T12:37:49Z focused
- 2026-11-06T12:37:51Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py']
- 2026-11-06T12:37:51Z scope: widened at merge to the reviewed lane's own diff (bf7e8f588), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T12:40:32Z done
- 2026-11-06T12:40:36Z committed 1f5c52c04 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- T-3417 [PERFORMANCE M, done, 1 steps] test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight… — lesson: none: a reviewed builder lane; i…
- T-3213 [FIX S, done, 2 steps] Post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went… — lesson: blame a red on a merge only after the same…
- T-3426 [FIX S, active, 1 steps] Re-land T-3410 (MASTER.md fmtrain bullet), auto-reverted by c8b6b5ecf on load-only…
- similar finished tasks took 1–2 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 tests first, then implement reach in pm_verify
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/cli.py
- .fm-scratch/e.json
- plugin/lib/sampo/lanes.py
- .fm-scratch/e2.json
- CHANGELOG.md
