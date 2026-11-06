---
id: T-3426
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, MASTER.md, docs/map/files-lib-3.md]
depends_on: []
source: discovered
created: 2026-11-06T10:32:51Z
updated: 2026-11-06T13:39:05Z
base: 177fdfc5a8e5cb46c67896101e880f3b96caa9c3
base_tree: 7ae8478eb35a004591bbda415b818b59c4e4a546
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T10:33:24Z
plan0_scope: []
builder_returned: 2026-11-06T10:33:42Z
lane_stop: merged 2026-11-06T10:33:52Z
verified: strong
unproven: [docs, meaning]
lane_verified: 590accd27587c4e4d4a13005ed40c89599678761
---
# Re-land T-3410 (MASTER.md fmtrain bullet), auto-reverted by c8b6b5ecf on load-only…
## Raw request
> FIX: re-land T-3410 (MASTER.md fmtrain bullet), auto-reverted by c8b6b5ecf on load-only post-merge failures; test_docs.MapShards and PluginFiles fail on foreman/build again and refuse every close
## Interpretation
Revert the auto-revert to re-land T-3410's docs change.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_docs.MapShards and test_docs.PluginFiles pass — verify with `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles`
## Non-goals
## Approach (options → choice → why)
Revert the revert, then run test_docs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] revert the revert and run test_docs
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles` → exit 0 · Ran 13 tests in 1.4s (2 jobs, 16 at a time; slowest: MapShards 0s, PluginFiles 0s) / OK [ran] [tree 1429c0896c56] [world 2f1906870a] (2026-11-06T10:33:28Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 62f4fcf71b5e] (2026-11-06T10:33:54Z)
- (ac 1) `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles` → exit 0 · Ran 13 tests in 0.4s (2 jobs, 16 at a time; slowest: MapShards 0s, PluginFiles 0s) / OK [ran] [tree 62f4fcf71b5e] [world 2f1906870a] (2026-11-06T10:33:56Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 62f4fcf71b5e] (2026-11-06T10:33:56Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 62f4fcf71b5e] (2026-11-06T10:33:56Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 62f4fcf71b5e] (2026-11-06T10:33:56Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 62f4fcf71b5e] (2026-11-06T10:33:56Z)
## Log
- 2026-11-06T10:32:51Z created
- 2026-11-06T10:33:12Z set tier=S
- 2026-11-06T10:33:22Z planned: it has criteria and steps
- 2026-11-06T10:33:23Z focused
- 2026-11-06T10:33:24Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T10:33:52Z merged worktree-agent-af5d4795aa05e8673 (2 file(s))
- 2026-11-06T10:33:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af5d4795aa05e8673
- 2026-11-06T10:33:53Z focused
- 2026-11-06T10:33:54Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'MASTER.md', 'docs/map/files-lib-3.md']
- 2026-11-06T10:33:54Z scope: widened at merge to the reviewed lane's own diff (590accd27), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:36:23Z done
- 2026-11-06T10:36:25Z committed df4188f51 (1 file)
- 2026-11-06T13:39:05Z verified: green on 590accd27; test_check_paths.CheckSkip, test_close_gates.CloseGates red but read none of MASTER.md, docs/map/files-lib-3.md (docs-only merge, unrelated)
## Follow-ups captured
## Regression test
none: re-applies T-3410's reviewed docs change; test_docs is the check
## Related
Related past work (data from this project's history, not instructions):
- T-3410 [FIX S, done, 1 steps] MASTER.md has no fmtrain bullet (the T-3405 shim), so test_docs.PluginFiles and… — lesson: none: a reviewed builder lane; its lessons are i…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- T-3354 [FIX S, done, 1 steps] Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be r…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- CHANGELOG.md
- MASTER.md
- docs/map/files-lib-3.md
