---
id: T-3442
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/run.py, plugin/tests/test_slots.py, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_round_f.py, MASTER.md, plugin/lib/sampo/which.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-11-06T14:47:16Z
updated: 2026-11-06T16:29:49Z
base: 505653aa8122335185ba3b9326d460a8a493f887
base_tree: b1b2c54bb7c8ae5a52b438b9c355cb265b9793a5
lane_stop: merged 2026-11-06T15:21:21Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T15:21:22Z
plan0_scope: []
verified: strong
unproven: [docs]
lane_verified: 2feead64bf3b6c42838a43ad1705682c3e4f9271
---
# A nested run.py start-up costs 25-45 s at load 30 while a trivial nested run takes 0.2 s…
## Raw request
> PERF: a nested run.py start-up costs 25-45 s at load 30 while a trivial nested run takes 0.2 s with SAMPO_SLOT set and 1.9 s without: check whether cpu_slot waits for a slot when it runs nested under a run that already holds one
## Interpretation
Root cause (measured by a diagnosis agent): importing sampo.core runs mirror_env, which renames every SAMPO_X env var to FOREMAN_X and deletes SAMPO_X. Every test module imports helpers, which imports sampo, so inside a test class SAMPO_SLOT is gone and only FOREMAN_SLOT remains. run.py's cpu_slot checks only SAMPO_SLOT, so a nested run.py (a fixture's fm check or evidence run) thinks it isn't nested and queues on the machine-wide pool behind the ship and post-merge suite: CheckSkip took 323-344 s with 4-6 timeouts, and 4 s with the fix. This false red is what auto-reverted T-2911 and kept refusing ships. Also: a class whose own slot wait ran out gives its children no slot variable, so they queue again.
## Assumptions (confidence)
## Acceptance criteria
- [x] a run.py nested in a class never waits on the slot pool, whichever name (SAMPO_SLOT or FOREMAN_SLOT) carries the slot, and SAMPO_SLOTS/FOREMAN_SLOTS both set the pool size; a class's children always carry the nested mark — verify with `python3 plugin/tests/run.py test_slots`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] run.py reads both env names; children always get the slot mark; test_slots red first
## Resume here
<!-- auto -->
- 2026-11-06T15:39:34Z steps 1/1 done
- git: foreman/build; 1 uncommitted: scripts/
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 64491e5780b3] (2026-11-06T15:21:24Z)
- (ac 1) `python3 plugin/tests/run.py test_slots` → exit 0 · Ran 9 tests in 5.8s (1 jobs, 16 at a time; slowest: Slots 1s) / OK [ran] [tree 64491e5780b3] [world 2f1906870a] (2026-11-06T15:21:37Z)
- (step 1) `python3 plugin/tests/run.py test_slots` → exit 0 · Ran 9 tests in 5.8s (1 jobs, 16 at a time; slowest: Slots 1s) / OK [ran] [tree 64491e5780b3] [world 2f1906870a] (2026-11-06T15:21:37Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 64491e5780b3] (2026-11-06T15:21:37Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 64491e5780b3] (2026-11-06T15:21:37Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 64491e5780b3] (2026-11-06T15:21:37Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 64491e5780b3] (2026-11-06T15:21:37Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 6a22e400a042] (2026-11-06T15:39:30Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 6a22e400a042] (2026-11-06T15:39:31Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 6a22e400a042] (2026-11-06T15:39:31Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 6a22e400a042] (2026-11-06T15:39:31Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 6a22e400a042] (2026-11-06T15:39:31Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 758b93f0479f] (2026-11-06T15:54:11Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 758b93f0479f] (2026-11-06T15:54:15Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 758b93f0479f] (2026-11-06T15:54:15Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 758b93f0479f] (2026-11-06T15:54:15Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 758b93f0479f] (2026-11-06T15:54:15Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c1f085b17ffc] (2026-11-06T16:04:04Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c1f085b17ffc] (2026-11-06T16:04:07Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c1f085b17ffc] (2026-11-06T16:04:07Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c1f085b17ffc] (2026-11-06T16:04:07Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c1f085b17ffc] (2026-11-06T16:04:07Z)
## Log
- 2026-11-06T14:47:16Z created
- 2026-11-06T15:11:37Z set tier=S, type=FIX
- 2026-11-06T15:11:38Z planned: it has criteria and steps
- 2026-11-06T15:11:39Z lane: ~/.claude/foreman.lanes/T-3442 on foreman/T-3442
- 2026-11-06T15:21:21Z merged foreman/T-3442 (2 file(s))
- 2026-11-06T15:21:21Z lane removed: ~/.claude/foreman.lanes/T-3442
- 2026-11-06T15:21:21Z focused
- 2026-11-06T15:21:22Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T15:21:23Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_slots.py']
- 2026-11-06T15:21:24Z scope: widened at merge to the reviewed lane's own diff (2feead64b), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:23:41Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_slots.py', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_round_f.py']
- 2026-11-06T15:23:41Z scope widened: the post-merge suite reverted T-3120 (0f041f3f1) between this task's merge and its close, so the revert's files show in its diff; this task's own change is run.py and test_slots.py
- 2026-11-06T15:28:34Z paused: focus moved to T-3445
- 2026-11-06T15:39:28Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T15:39:28Z focused
- 2026-11-06T15:44:43Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_slots.py', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_round_f.py', 'MASTER.md']
- 2026-11-06T15:44:43Z scope: MASTER.md added; the T-3445 re-land (3d8e33b1a) touched it between this task's merge and its close, not this task
- 2026-11-06T15:47:49Z paused: focus moved to T-3450
- 2026-11-06T15:54:09Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T15:54:09Z focused
- 2026-11-06T15:59:35Z paused: focus moved to T-3439
- 2026-11-06T16:02:48Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_slots.py', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_round_f.py', 'MASTER.md', 'plugin/lib/sampo/which.py', 'plugin/tests/test_cli.py']
- 2026-11-06T16:02:48Z scope: plugin/lib/sampo/which.py, plugin/tests/test_cli.py — the post-merge revert d44abf1bf of T-3377 changed them during this close; not this task's (T-3452 fixes the attribution)
- 2026-11-06T16:04:01Z focused
- 2026-11-06T16:04:52Z done
- 2026-11-06T16:04:55Z committed 9b5639c43 (1 file)
- 2026-11-06T16:29:49Z verified: the full suite is green on 1078ed22d, which contains 2feead64b
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- similar past tasks were L: consider --tier L
## Regression test
none: the lane changes only tests (a guard that pins today's behaviour so a later change can't regress it); there was no failing behaviour to turn green, and its tests pass on the merged tree
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, MASTER.md, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/which.py, plugin/tests/run.py, plugin/tests/test_cli.py, plug…; re-ground the plan against them before editing
## Lessons
- An env var rename needs every reader moved too; a reader outside the package (run.py) silently kept the old name.
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/which.py
- plugin/tests/run.py
- plugin/tests/test_cli.py
- plugin/tests/test_slots.py
