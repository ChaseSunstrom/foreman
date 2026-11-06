---
id: T-3410
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, MASTER.md, docs/map/files-lib-3.md]
depends_on: []
source: discovered
created: 2026-11-06T08:56:09Z
updated: 2026-11-06T09:58:16Z
base: c579ca3540234672dcc713fa0d11bb31ee05da64
base_tree: 24458fc8169de8accb4ea00728ae4dc70e45813b
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:56:41Z
plan0_scope: []
builder_returned: 2026-11-06T09:12:34Z
lane_stop: refused 2026-11-06T09:58:16Z
verified: strong
unproven: [docs, meaning]
postmerge_red: test_check_paths.CheckSkip, test_cli.AffectedPairs, test_close_gates.CloseGates
postmerge_sha: 0cad059e5a42fed5c560b1b061a6d801ada4d1f6
---
# MASTER.md has no fmtrain bullet (the T-3405 shim), so test_docs.PluginFiles and…
## Raw request
> FIX: MASTER.md has no fmtrain bullet (the T-3405 shim), so test_docs.PluginFiles and test_docs.MapShards fail on foreman/build; add its bullet like fmrepro's
## Interpretation
Add the missing fmtrain shim bullet to MASTER.md and its map shard.
## Assumptions (confidence)
## Acceptance criteria
- [x] MapShards and PluginFiles pass — verify with `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles`
## Non-goals
## Approach (options → choice → why)
Copy the fmrepro bullet form; one line in MASTER.md and one in docs/map/files-lib-3.md.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Add the fmtrain bullet to MASTER.md and the shard
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles 2>&1 | tail -8` → exit 0 · Ran 13 tests in 87.0s (2 jobs, 16 at a time; slowest: MapShards 0s, PluginFiles 0s) / OK [ran] [tree 57faab62a5a0] [world 2f1906870a] (2026-11-06T08:58:19Z)
- (step 1) `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles` → exit 0 · Ran 13 tests in 270.6s (2 jobs, 16 at a time; slowest: MapShards 0s, PluginFiles 0s) / OK [ran] [tree 57faab62a5a0] [world 2f1906870a] (2026-11-06T09:02:51Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 048e9221710e] (2026-11-06T09:14:47Z)
- (ac 1) `python3 plugin/tests/run.py test_docs.MapShards test_docs.PluginFiles` → exit 0 · Ran 13 tests in 33.4s (2 jobs, 16 at a time; slowest: MapShards 0s, PluginFiles 0s) / OK [ran] [tree 048e9221710e] [world 2f1906870a] (2026-11-06T09:15:25Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 048e9221710e] (2026-11-06T09:15:25Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 048e9221710e] (2026-11-06T09:15:25Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 048e9221710e] (2026-11-06T09:15:25Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 048e9221710e] (2026-11-06T09:15:25Z)
## Log
- 2026-11-06T08:56:09Z created
- 2026-11-06T08:56:22Z set tier=S
- 2026-11-06T08:56:39Z planned: it has criteria and steps
- 2026-11-06T08:56:39Z focused
- 2026-11-06T08:56:41Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T09:14:44Z merged worktree-agent-a0823a0e177358810 (2 file(s))
- 2026-11-06T09:14:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0823a0e177358810
- 2026-11-06T09:14:45Z focused
- 2026-11-06T09:14:47Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'MASTER.md', 'docs/map/files-lib-3.md']
- 2026-11-06T09:14:47Z scope: widened at merge to the reviewed lane's own diff (0cad059e5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T09:31:27Z done
- 2026-11-06T09:31:31Z committed 9d9fa0fbb (1 file)
- 2026-11-06T09:58:16Z red after merge: test_check_paths.CheckSkip, test_cli.AffectedPairs, test_close_gates.CloseGates; 0cad059e5 reverted
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3094 [FIX S, dropped, 0 steps] test_docs.MapShards says MASTER.md's File map and Operations moved into docs/map shards,…
- T-2943 [FIX S, done, 1 steps] The fmmint and fmtraces shims match the exact old-path shim, so the rename alias test passes — lesson: A new sampo module's old-path shim m…
- decision 2026-11-05: [cites: research T-2879-probe] T-2879: rename the plugins inside the existing 'foreman' marketplace with a renames map (foreman→sampo, foreman-ui→sa…
- similar finished tasks took 1–4 steps
## Regression test
none: the lane changed no test module; its behaviour is covered by the full gates at this close
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- MASTER.md
- docs/map/files-lib-3.md
- CHANGELOG.md
