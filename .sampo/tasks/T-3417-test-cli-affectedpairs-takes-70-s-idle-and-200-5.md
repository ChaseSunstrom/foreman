---
id: T-3417
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-11-06T09:31:29Z
updated: 2026-11-06T13:28:40Z
base_note: 
base: c8b6b5ecff483c58ff5e937d1eb82842193cbc88
base_tree: 6acd074b4d3f66a75270173c994be562228b5deb
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T09:35:05Z
plan0_scope: []
builder_returned: 2026-11-06T09:56:17Z
lane_stop: merged 2026-11-06T10:04:21Z
verified: strong
unproven: [meaning, perf-typed]
---
# test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight…
## Raw request
> PERF: test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight hit its nested fm check --affected timeouts); make each test's nested check cheap (a tiny temp repo and map, no real-repo-sized affected selection) or split the class so run.py spreads it, and keep the 300 s hang guard as a backstop
## Interpretation
Reading 1: the nested fm check --affected is slow because of work inside it (map, history, hub analysis). Reading 2 (ruled out until measured): only interpreter startup under load.
## Assumptions (confidence)
## Acceptance criteria
- [x] AffectedPairs total time drops, assertions kept — verify with `python3 plugin/tests/run.py test_cli.AffectedPairs`
## Non-goals
## Approach (options → choice → why)
1) tiny repos/stub map: likely outcome cuts per-call cost; fails if cost is interpreter startup. 2) use what exists: merge nested calls, reuse red_lane setup; likely outcome fewer calls. 3) do less: just raise guards; likely outcome hides the slowness, fails the goal. Choice 2 (85%): measure first, then fewer calls plus cheaper map.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1473, T-1579, T-1588, T-1589.
## Execution prompt
## Steps
1. [x] measure, cheapen, re-measure
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k AffectedPairs test_cli` → exit 0 · Ran 5 tests in 20.1s (1 jobs, 16 at a time; slowest: AffectedPairs 3s) / OK [ran] [tree e2052c8d2d4f] [world 2f1906870a] (2026-11-06T09:54:33Z)
- (step 1) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.31s] [ran] [tree e2052c8d2d4f] [world 2f1906870a] (2026-11-06T09:56:04Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 7ae8478eb35a] (2026-11-06T10:04:25Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 7ae8478eb35a] (2026-11-06T10:05:35Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 101.5s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 1s, AffectedPairs.test_every_linked_test_skipped_is_said_so 1s, AffectedPairs.test_a_s [ran] [tree 7ae8478eb35a] [world 2f1906870a] (2026-11-06T10:07:19Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 7ae8478eb35a] (2026-11-06T10:07:19Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 7ae8478eb35a] (2026-11-06T10:07:19Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 7ae8478eb35a] (2026-11-06T10:07:19Z)
## Log
- 2026-11-06T09:31:29Z created
- 2026-11-06T09:34:37Z planned: it has criteria and steps
- 2026-11-06T09:35:02Z focused
- 2026-11-06T09:35:05Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T10:04:21Z merged worktree-agent-ab71a6d1079c1d04c (1 file(s))
- 2026-11-06T10:04:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab71a6d1079c1d04c
- 2026-11-06T10:04:22Z focused
- 2026-11-06T10:04:24Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/test_cli.py']
- 2026-11-06T10:04:24Z scope: widened at merge to the reviewed lane's own diff (f1c14cc60), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:05:30Z focused
- 2026-11-06T10:09:31Z done
- 2026-11-06T10:09:35Z committed 177fdfc5a (1 file)
- 2026-11-06T13:28:40Z not reverted: test_check_paths.CheckSkip, test_docs.MapShards, test_docs.PluginFiles already fail on f1c14cc60's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3306 [FEATURE M, done, 3 steps] Sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file… — lesson: none: a reviewed builder lane; its lessons…
- T-3390 [FIX S, done, 1 steps] test_cli.AffectedPairs forks a full fm repo per test and nests fm check --affected; each… — lesson: a test that runs a nested fm check need…
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
## Measurements
test_cli.AffectedPairs: 90-240 s -> 3.1 s (python3 plugin/tests/run.py -k AffectedPairs test_cli in the lane, host load ~14-20)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- .fm-scratch-dur.txt
- .fm-scratch/prof.sh
- .fm-scratch/tfm.py
- plugin/tests/test_cli.py
- CHANGELOG.md
