---
id: T-3526
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/tests/test_close_affected.py]
depends_on: []
source: self
created: 2026-11-06T19:26:43Z
updated: 2026-11-07T00:42:52Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:27:50Z
plan0_scope: []
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [perf-typed]
---
# A close after a merge train skips its linked-tests run when the gates' full pass holds for the same code tree: the train's suite already ran them (50-300 s per close, about 10 min a train)
## Raw request
> A close after a merge train skips its linked-tests run when the gates' full pass holds for the same code tree: the train's suite already ran them (50-300 s per close, about 10 min a train)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task finish skips _close_affected's run, logging that the gates' pass covered it, when the affected command is the gate runner plus module names and cli._cached_pass holds for the current tree or code tree; with no such pass, or a different runner, it runs as today — verify with `python3 plugin/tests/run.py test_close_affected`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reuse the gates' pass in _close_affected, test-first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_close_affected` → ✗ exit 1 · Ran 3 tests in 54.9s (1 jobs, 16 at a time; slowest: CloseAffectedReuse 5s) / FAILED (1 classes: test_close_affected.CloseAffectedReuse) [ran] [tree 88649b88d97b] [world 2f1906870a] (2026-11-06T19:31:17Z)
- (step 1) `python3 plugin/tests/run.py test_close_affected test_close_gates test_risk test_round_f` → exit 0 · Ran 56 tests in 51.0s (4 jobs, 16 at a time; slowest: CloseGates 30s, RoundF 10s, Risk 4s) / OK [ran] [tree 891833655a7f] [world 2f1906870a] (2026-11-06T19:32:30Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 4af507089c60] (2026-11-06T22:16:07Z)
- (ac 1) `python3 plugin/tests/run.py test_close_affected` → exit 0 · Ran 3 tests in 3.2s (1 jobs, 16 at a time; slowest: CloseAffectedReuse 3s) / OK [ran] [tree 4af507089c60] [world 2f1906870a] (2026-11-06T22:16:13Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 4af507089c60] (2026-11-06T22:16:13Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 4af507089c60] (2026-11-06T22:16:13Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 4af507089c60] (2026-11-06T22:16:13Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 4af507089c60] (2026-11-06T22:16:13Z)
## Log
- 2026-11-06T19:26:43Z created
- 2026-11-06T19:27:25Z lane: ~/.claude/foreman.lanes/T-3526 on foreman/T-3526
- 2026-11-06T19:27:49Z focused
- 2026-11-06T19:27:50Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T21:46:50Z merged foreman/T-3526 in merge train
- 2026-11-06T22:16:07Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_close_affected.py']
- 2026-11-06T22:16:07Z scope: widened at merge to the reviewed lane's own diff (7910c09a5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:17:06Z done
- 2026-11-06T22:17:09Z committed 12d2c6092 (1 file)
- 2026-11-07T00:42:52Z lane removed: ~/.claude/foreman.lanes/T-3526; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3120 [PERFORMANCE S, done, 2 steps] sampo task finish reuses a full-gates pass on the same tree from any task when the only change since is CHANGELOG.md lines, rerunni…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- research T-2352-review: T-2352 review (fm-reviewer, one pass): changes needed; fixed before close (tests added after the fixes, so not seen red first).
- decision 2026-11-06: Post-merge suite back on (supersedes the pause): a close runs only its criteria and affected tests, not the full suite, so the post-merge run is the…
- similar finished tasks took 2–5 steps
## Measurements
close linked-tests seconds after a train: 50–300 s per close (ledger close_affected s) → 0 s when the train's pass covers it (test_close_affected)
## Lessons
- When a cheaper check is covered by a pass that already ran, reuse the helper that decides whether that pass still holds, not a copy of its rules.
## Plan gaps
- failed first: step 1 reuse the gates' pass in _close_affected, test-first
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/tests/test_close_affected.py
