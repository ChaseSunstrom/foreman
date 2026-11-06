---
id: T-3213
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T15:01:24Z
updated: 2026-11-05T18:24:23Z
builder_model: sonnet
base: 300e0783dde9fb6438b9f9539184b5eb5182b3a3
base_tree: f43f32ad76d6c7c4401f6222039fb1070fce7074
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T17:32:06Z
plan0_scope: []
builder_returned: 2026-11-05T17:33:59Z
lane_stop: merged 2026-11-05T17:57:22Z
verified: strong
unproven: [meaning]
lane_verified: 2552f051feea9c03c290ab3d5d869c3507544ce2
---
# Post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went…
## Raw request
> post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went red and was reverted, then T-3189's verify judged a tree that still held T-3160 and reverted T-3189 for T-3160's BoardVerbs/ToolTaint failures; T-3189 alone on main passes them. A verify must judge its merge on top of main as it is now (minus reverted merges), and a red class another landed merge already owns is not this merge's
## Interpretation
Reading 1 (chosen): a merge's post-merge verify reverts it for a red it inherited from a merge beneath it (T-3154 and T-3189 landed on top of T-3160 and were reverted for T-3160's red); before reverting, check the red isn't already there without this merge. Reading 2 (ruled out): serialise all merges until each verify is green; that undoes T-3141's throughput gain.
## Assumptions (confidence)
## Acceptance criteria
- [x] a merge whose red classes also fail on its first parent is not reverted: its record says inherited with the classes; a merge whose red classes pass on its first parent is reverted as before — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
1) use what exists: in pm_verify, after a red that stays red alone (T-3216), re-run the same classes on the merge's first parent (main just before it, in the same throwaway worktree); red there too means inherited: no revert, state 'inherited' naming the classes, and the red stays with the merge that introduced it; likely outcome: only the merge that brought a red is reverted. 2) judge on current main minus reverted merges: fails if: rebuilding that tree conflicts, and it still can't tell an inherited red. 3) serialise verifies: fails if: merges wait on every full suite again. 4) do less: let reverts stand and re-land by hand: fails if: every inherited red costs a manual re-land (three tonight). Choice 1 (85%): one more targeted run decides blame exactly.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: an inherited red keeps the merge, an own red reverts it
2. [x] the first-parent re-run in pm_verify
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify 2>&1 | grep -B3 -A18 "^FAIL"` → ✗ exit 1 · Ran 17 tests in 2.2s (17 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_revert_requeues_the_merges_stacked_on_it 1s, Post [ran] [tree f704aeba9230] [world 2f1906870a] (2026-11-05T17:32:48Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 17 tests in 1.7s (17 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_dirty_index_leaves_the_red_retryable_not_a_confli [ran] [tree eee7053da2c5] [world 2f1906870a] (2026-11-05T17:32:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_twins test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 173 tests across 6 files. [12.36s] [ran] [tree eee7053da2c5] [world 2f1906870a] (2026-11-05T17:33:50Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 17 tests in 9.8s (1 jobs, 16 at a time; slowest: PostMergeVerify 9s) / OK [ran] [tree f026d9aecbff] [world 2f1906870a] (2026-11-05T18:07:06Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 17 tests in 12.8s (1 jobs, 16 at a time; slowest: PostMergeVerify 9s) / FAILED (1 classes: test_lanes.PostMergeVerify) (start tree + this task's tests) [ran] [tree f026d9aecbff] [world 2f1906870a] (2026-11-05T18:07:23Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 17 tests in 2.4s (17 jobs, 16 at a time; slowest: PostMergeVerify.test_a_revert_requeues_the_merges_stacked_on_it 1s, PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, Post [ran] [tree f026d9aecbff] [world 2f1906870a] (2026-11-05T18:07:23Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T18:07:23Z [ran] [tree f026d9aecbff] [world 2f1906870a] (2026-11-05T18:07:32Z)
- (audit intent) `lane diff read before queueing; the first-parent re-run uses pm_rerun_cmd's class whitelist; merged with post-merge verify green` → a red that also fails on the first parent is recorded as inherited and kept; an own red still reverts [tree f026d9aecbff] (2026-11-05T18:07:32Z)
- (audit adversary) `lane diff read before queueing; the first-parent re-run uses pm_rerun_cmd's class whitelist; merged with post-merge verify green` → class names stay [\w.]+ so the parent re-run can't inject a command [tree f026d9aecbff] (2026-11-05T18:07:32Z)
- (audit edge) `lane diff read before queueing; the first-parent re-run uses pm_rerun_cmd's class whitelist; merged with post-merge verify green` → a parent re-run that can't start counts as not inherited, so the merge reverts as before (fail closed) [tree f026d9aecbff] (2026-11-05T18:07:32Z)
- (audit self) `lane diff read before queueing; the first-parent re-run uses pm_rerun_cmd's class whitelist; merged with post-merge verify green` → no findings [tree f026d9aecbff] (2026-11-05T18:07:32Z)
## Log
- 2026-11-05T15:01:24Z created
- 2026-11-05T15:27:15Z planned: it has criteria and steps
- 2026-11-05T15:27:16Z set tier=S, approved=True
- 2026-11-05T17:31:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3213.builder.md
- 2026-11-05T17:32:05Z focused
- 2026-11-05T17:32:06Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T17:57:22Z merged worktree-agent-aa4850efa99eeced3 (2 file(s))
- 2026-11-05T17:57:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa4850efa99eeced3
- 2026-11-05T18:06:47Z focused
- 2026-11-05T18:07:30Z set scope=['plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-11-05T18:07:30Z scope: the merge 2552f051's two files plus the CHANGELOG line
- 2026-11-05T18:07:35Z affected tests waived: merged lane; the post-merge verify already ran the full suite
- 2026-11-05T18:07:38Z done
- 2026-11-05T18:07:43Z committed 06b9f0f4 (1 file)
- 2026-11-05T18:08:27Z correction: the edge lens 'a parent re-run that can't start counts as not inherited' was wrong: any non-zero parent re-run (e.g. run.py's 'no test matches' for a class the merge added) is called inherited, so a merge's own new red is kept. Fixed in T-3224.
- 2026-11-05T18:24:23Z verified: the full suite is green on 2552f051f
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3216 [FIX S, done, 2 steps] Post-merge verify re-runs the red classes alone before reverting: a class red only inside the full suite (green alone) is a flake, logged, …
- T-3119 [PERFORMANCE M, blocked, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-3141 [PERFORMANCE M, done, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge …
- decision 2026-11-05: Hold main-checkout test runs and closes after T-3151's close until the queued merges (T-3087, T-3108, then T-3053's chain) land
- similar finished tasks took 2–2 steps
## Why not caught
the post-merge tests only stacked one merge; the new tests stack two with the red beneath
## Lessons
- blame a red on a merge only after the same classes pass on its first parent
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
