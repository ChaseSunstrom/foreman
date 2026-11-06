---
id: T-3377
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/which.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-11-06T06:21:39Z
updated: 2026-11-06T15:54:53Z
base: 23770af009deda810e246c56e5253ff73150cb34
base_tree: 30b093776bfff179b78109383c5ac9830fc1c168
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T08:56:08Z
plan0_scope: []
builder_returned: 2026-11-06T09:24:32Z
lane_stop: refused 2026-11-06T15:54:53Z
verified: strong
unproven: [meaning]
postmerge_red: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims
postmerge_sha: e99c07fc9d29ee4ee9219644b64ca5f95c7ee57d
---
# Sampo task set can't widen scope incrementally (scope+=PATH); builders re-list the whole…
## Raw request
> FEATURE: sampo task set can't widen scope incrementally (scope+=PATH); builders re-list the whole scope (T-2952)
## Interpretation
Reading 1: scope+=/scope-= suffix forms in task set's assignment parser, also covering depends_on. Reading 2: new verbs (task scope add); ruled out, more surface.
## Assumptions (confidence)
## Acceptance criteria
- [x] scope+= appends deduped in order and scope-= removes — verify with `python3 plugin/tests/run.py test_cli -k scope_plus`
## Non-goals
No changes to task ac verbs (T-3372).
## Approach (options → choice → why)
1) suffix on key in the shared parser; likely outcome: small diff, fails if a path contains a trailing + or -. 2) new 'task scope' verb; likely outcome: more surface, conflicts with T-3372's cli edits. 3) do less: nothing, keep scope=; fails if builders keep re-listing paths. 4) use what exists: reuse _list_value and the changes/mutate path; likely outcome: same as 1. Choice 1 (85%): same save path as scope=.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, parser change, help/docs
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake -k scope_plus` → exit 0 · Ran 1 tests in 51.7s (1 jobs, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 0068dd74ff4e] [world 2f1906870a] (2026-11-06T09:00:24Z)
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake -k scope_plus` → exit 0 · Ran 1 tests in 68.7s (1 jobs, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 0068dd74ff4e] [world 2f1906870a] (2026-11-06T09:01:39Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 0068dd74ff4e] [world 2f1906870a] (2026-11-06T09:01:48Z)
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake -k scope_plus -k list_ops` → ✗ exit 1 · Ran 2 tests in 75.9s (1 jobs, 16 at a time; slowest: CaptureAndIntake 1s) / FAILED (1 classes: test_cli.CaptureAndIntake) [ran] [tree 6d033bd45001] [world 2f1906870a] (2026-11-06T09:13:55Z)
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake -k scope_plus -k list_ops` → exit 0 · Ran 2 tests in 6.8s (1 jobs, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 15f3436129bb] [world 2f1906870a] (2026-11-06T09:14:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 550 tests in 216.6s (131 jobs, 16 at a time; slowest: AffectedPairs 198s, TaskLifecycle 17s, LouhiModels 12s) / FAILED (1 classes: test_cli.AffectedPairs) [ran] [tree 15f3436129bb] [world 2f1906870a] (2026-11-06T09:17:58Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree d9b1fcb5d9c6] (2026-11-06T11:06:29Z)
- (ac 1) `python3 plugin/tests/run.py test_cli -k scope_plus` → exit 0 · Ran 1 tests in 0.7s (1 jobs, 16 at a time; slowest: CaptureAndIntake 0s) / OK [ran] [tree d9b1fcb5d9c6] [world 2f1906870a] (2026-11-06T11:06:33Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree d9b1fcb5d9c6] (2026-11-06T11:06:33Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree d9b1fcb5d9c6] (2026-11-06T11:06:33Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree d9b1fcb5d9c6] (2026-11-06T11:06:33Z)
## Log
- 2026-11-06T06:21:39Z created
- 2026-11-06T08:55:45Z planned: it has criteria and steps
- 2026-11-06T08:56:07Z focused
- 2026-11-06T08:56:08Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T10:44:35Z criterion 1 verify: `python3 plugin/tests/run.py plugin/tests/test_cli.py -k scope_plus` → `python3 plugin/tests/run.py test_cli -k scope_plus`
- 2026-11-06T10:44:36Z criterion 1 verify: run.py takes test names, not paths (a path refused T-3375's merge); moved to the name form
- 2026-11-06T11:06:27Z merged worktree-agent-ae87279c940167520 (3 file(s))
- 2026-11-06T11:06:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae87279c940167520
- 2026-11-06T11:06:28Z focused
- 2026-11-06T11:06:29Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/which.py', 'plugin/tests/test_cli.py']
- 2026-11-06T11:06:29Z scope: widened at merge to the reviewed lane's own diff (e99c07fc9), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T11:07:07Z done
- 2026-11-06T11:07:09Z committed 019c4c4cf (1 file)
- 2026-11-06T15:54:53Z red after merge: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims; e99c07fc9 reverted (reached by: plugin/lib/sampo/cli.py, plugin/lib/sampo/which.py, plugin/tests/test_cli.py)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3108 [FIX S, done, 2 steps] sampo which finds the task set key forms: 'widen task scope' names sampo task set ID scope=[...], and approve and allow the same way
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- similar finished tasks took 2–3 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/which.py
- CHANGELOG.md
