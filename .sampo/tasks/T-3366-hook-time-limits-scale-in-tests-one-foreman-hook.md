---
id: T-3366
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: followup
created: 2026-11-06T05:55:37Z
updated: 2026-11-06T09:43:12Z
base: 3d1fb1b45301fd28e7778307c206b18fb6b25aa6
base_tree: 1e30d1a5a46be27c1535ed757775e8f6b68ace58
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:10Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py]
builder_returned: 2026-11-06T06:50:17Z
lane_stop: merged 2026-11-06T08:55:39Z
verified: ok
unproven: [typed]
---
# Hook time limits scale in tests: one FOREMAN_HOOK_SLACK factor (default 1) multiplies hooks.py's fixed limits (fm task new 3 s ~790, queueing 3.2 s ~853, fm focus 3 s ~901, Stop close 25/20 s ~1152/1160), and the test helper's hook() passes busy_factor()
## Raw request
> Hook time limits scale in tests: one FOREMAN_HOOK_SLACK factor (default 1) multiplies hooks.py's fixed limits (fm task new 3 s ~790, queueing 3.2 s ~853, fm focus 3 s ~901, Stop close 25/20 s ~1152/1160), and the test helper's hook() passes busy_factor()
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] NoTaskGate classes pass under simulated load and production limits are unchanged at slack 1 — verify with `python3 plugin/tests/run.py --load 48 test_hooks -k NoTaskGate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] slack constant and helper env
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py --load 48 test_hooks -k NoTaskGate` → exit 0 · Ran 31 tests in 199.3s (6 jobs, 16 at a time; slowest: NoTaskGateClose 25s, NoTaskGateMulti 23s, NoTaskGateKinds 19s) / OK (ran] (tree afec363fa052] (world 2f1906870a] (2026-11-06T06:08:18Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 617 tests in 942.6s (239 jobs, 16 at a time; slowest: Approvals 22s, UserPromptSubmit 20s, PromptApprovals 19s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree afec363fa052] (world 2f1906870a] (2026-11-06T06:24:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 629 tests in 572.1s (349 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 14s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_tak (ran] (tree c32bb8c7e546] (world 2f1906870a] (2026-11-06T06:50:04Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 24458fc8169d] (2026-11-06T08:55:48Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 260 tests in 82.9s (153 jobs, 16 at a time; slowest: Approvals 13s, UserPromptSubmit 12s, PromptApprovals 10s) / FAILED (1 classes: test_hooks.HookSlack) (start tree + this task's tests) [ran] [tree 24458fc8169d] [world 2f1906870a] (2026-11-06T09:03:38Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 260 tests in 383.2s (234 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 7s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 24458fc8169d] [world 2f1906870a] (2026-11-06T09:03:38Z)
- (ac 1) `python3 plugin/tests/run.py --load 48 test_hooks -k NoTaskGate` → exit 0 · Ran 31 tests in 490.4s (13 jobs, 16 at a time; slowest: NoTaskGateQueue 18s, NoTaskGateKinds 18s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_takes_0_4_s 13s) [ran] [tree 24458fc8169d] [world 2f1906870a] (2026-11-06T09:11:50Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 24458fc8169d] (2026-11-06T09:11:50Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 24458fc8169d] (2026-11-06T09:11:50Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 24458fc8169d] (2026-11-06T09:11:50Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 24458fc8169d] (2026-11-06T09:11:50Z)
## Log
- 2026-11-06T05:55:37Z created
- 2026-11-06T05:56:07Z focused
- 2026-11-06T05:56:10Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T08:55:39Z merged worktree-agent-a03cf6a68eef026f5 (3 file(s))
- 2026-11-06T08:55:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a03cf6a68eef026f5
- 2026-11-06T08:55:43Z focused
- 2026-11-06T08:55:47Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/helpers.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T08:55:48Z scope: widened at merge to the reviewed lane's own diff (e82c630e4), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T09:14:27Z done
- 2026-11-06T09:14:34Z committed c579ca354 (1 file)
- 2026-11-06T09:43:12Z not reverted: test_check_paths.CheckSkip, test_close_gates.CloseGates, test_docs.MapShards, test_docs.PluginFiles already fail on e82c630e4's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/hooks.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/lib/sampo/hooks.py
- plugin/tests/helpers.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
