---
id: T-3519
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, docs/map/ops-1.md, plugin/lib/sampo/hooks.py, plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-11-06T19:11:48Z
updated: 2026-11-07T00:42:52Z
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T19:19:29Z
plan0_scope: []
lane_stop: merged 2026-11-07T00:04:53Z
group: guard refuses legitimate lane and task work
verified: strong
unproven: [docs]
---
# Builders hit the brief guard 140 times today, 113 on files inside lane worktrees with no…
## Raw request
> FIX: builders hit the brief guard 140 times today, 113 on files inside lane worktrees with no task attached (95 Python files, mostly 06-09h): a lane whose branch names a task (foreman/T-N) or whose builder brief names it attaches that task before the first edit
## Interpretation
Reading 1 (chosen): when the brief guard refuses an edit in a lane (the hook's project is a linked worktree) with no task active there, look up the lane's task first: its branch foreman/T-N, or an open brief whose lane/lane_branch meta records this lane's path or branch. Exactly one → run sampo focus on it in-process (the same verb, reused via _fm_inline), log one auto_focus event, re-run the guard so the edit passes. Several or none, or focus refuses → refuse as today, the hint naming the candidates or focus's reason. Reading 2 (ruled out): guess among builder-brief tasks with no lane recorded (parallel builders launch together, so that guess is ambiguous exactly when it would fire).
## Assumptions (confidence)
## Acceptance criteria
- [x] an edit inside a lane whose branch is foreman/T-N, or whose builder brief names T-N, attaches that task before the brief guard judges it, so the first edit passes; a lane with no task still refuses — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
1) use what exists: hook-side lookup in the brief-refusal path before _first_brief, reusing sampo focus in-process via _fm_inline (as _queue_requests does). Likely outcome: only the refusal path pays one git branch read plus a brief load; cmd_focus keeps every safety check (closed, held elsewhere, plan gaps). Fails if: cmd_focus is slow on a loaded host (one-time, first lane edit).
2) make fmguard's brief check lane-aware. Fails if: the guard must stay pure (no state writes), so it can't focus anything; it could only soften the refusal.
3) have sampo lane new focus the task at creation. Likely outcome: Sampo lanes covered, but fails if: the Claude Code worktree and knocked-off-focus cases (59 of today's refusals came after a focus) stay broken.
4) do less: only improve the refusal hint to name the lane's task. Fails if: each builder still burns a turn per refusal, the cost the task exists to remove.
Choice 1 (85%): smallest diff, reuses focus's checks, covers both lane kinds.
## Risks and rollback
Risk: focus in the hook adds time on the first lane edit (one-time; cmd_focus already runs in-hook for _queue_requests). Wrong-task focus is prevented by requiring exactly one candidate. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] attach the lane's task before the brief check, test-first
2. [x] review fixes: lookup+focus deadline, a hint stops the first brief, lanes only in the lane folders
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard.LaneAutoFocus` → ✗ exit 1 · Ran 3 tests in 37.6s (1 jobs, 16 at a time; slowest: LaneAutoFocus 2s) / FAILED (1 classes: test_guard.LaneAutoFocus) [ran] [tree 5611e9c30186] [world 2f1906870a] (2026-11-06T19:23:01Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard` → exit 0 · Ran 340 tests in 18.1s (121 jobs, 16 at a time; slowest: Mutation 18s, GuardAgainstBash.test_every_form_that_runs_a_dangerous_call_is_blocked 9s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangero [ran] [tree d2c839f80add] [world 2f1906870a] (2026-11-06T19:26:57Z)
- (step 1) `nice -n 10 python3 plugin/tests/bench_hooks.py --runs 5` → exit 0 · SessionEnd                  33.6    42.4     150  [0] / machine busy (load 1.3 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree d2c839f80add] [world 2f1906870a] (2026-11-06T19:27:21Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard.LaneAutoFocus` → ✗ exit 1 · Ran 5 tests in 2.1s (1 jobs, 16 at a time; slowest: LaneAutoFocus 2s) / FAILED (1 classes: test_guard.LaneAutoFocus) [ran] [tree 7ed3353b5c92] [world 2f1906870a] (2026-11-06T19:59:13Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard test_hooks` → exit 0 · Ran 609 tests in 41.2s (344 jobs, 16 at a time; slowest: Mutation 20s, SessionStart.test_budget_holds_with_large_queue 11s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_pyt [ran] [tree efc802bddbc6] [world 2f1906870a] (2026-11-06T20:01:12Z)
- (step 2) `nice -n 10 python3 plugin/tests/bench_hooks.py --runs 5` → exit 0 · SessionEnd                  42.8    43.9     150  [0] / machine busy (load 1.2 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree efc802bddbc6] [world 2f1906870a] (2026-11-06T20:01:28Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 34ab8cd74598] (2026-11-07T00:31:57Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · ^^^^^^^^^^^^^^^^^^^ / AttributeError: module 'sampo.core' has no attribute 'private_terms' (start tree + this task's tests) [ran] [tree 34ab8cd74598] [world 2f1906870a] (2026-11-07T00:32:17Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 342 tests in 15.2s (101 jobs, 16 at a time; slowest: Mutation 15s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 9s, Latency 9s) / OK [ran] [tree 34ab8cd74598] [world 2f1906870a] (2026-11-07T00:32:17Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · reused: the same command passed on this tree and world at 2026-11-07T00:32:17Z [ran] [tree 34ab8cd74598] [world 2f1906870a] (2026-11-07T00:32:19Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 34ab8cd74598] (2026-11-07T00:32:19Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 34ab8cd74598] (2026-11-07T00:32:19Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 34ab8cd74598] (2026-11-07T00:32:19Z)
## Log
- 2026-11-06T19:11:48Z created
- 2026-11-06T19:12:35Z set tier=M
- 2026-11-06T19:12:36Z planned: it has criteria and steps
- 2026-11-06T19:12:41Z lane: ~/.claude/foreman.lanes/T-3519 on foreman/T-3519
- 2026-11-06T19:19:27Z focused
- 2026-11-06T19:19:29Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T19:56:43Z focused
- 2026-11-06T19:56:47Z focused
- 2026-11-07T00:04:53Z merged foreman/T-3519 in merge train
- 2026-11-07T00:31:56Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'docs/map/ops-1.md', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_guard.py']
- 2026-11-07T00:31:56Z scope: widened at merge to the reviewed lane's own diff (a6f9b31c9), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T00:36:17Z done
- 2026-11-07T00:36:22Z committed 0033ea276 (1 file)
- 2026-11-07T00:42:52Z lane removed: ~/.claude/foreman.lanes/T-3519; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
## Measurements
brief refusals inside lane worktrees: 124 of 142 on 2026-11-06 (ledger guard_block, category brief) → expected 0 for lanes on foreman/T-N or recording their lane (recount tomorrow; count auto_focus events)
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- When a guard refuses something whose fix is fully determined, the hook applies that fix itself through the same verb and keeps the refusal for the ambiguous cases.
## Plan gaps
- added late: review fixes: lookup+focus deadline, a hint stops the first brief, lanes only in the lane folders
- failed first: step 1 attach the lane's task before the brief check, test-first
- failed first: step 2 review fixes: lookup+focus deadline, a hint stops the first brief, lanes only in the lane folders
## Files touched
- CHANGELOG.md
- docs/map/ops-1.md
- plugin/lib/sampo/hooks.py
- plugin/tests/test_guard.py
- scripts/probe-plugin-rename.sh
