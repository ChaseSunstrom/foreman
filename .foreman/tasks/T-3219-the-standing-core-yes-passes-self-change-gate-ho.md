---
id: T-3219
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T17:22:56Z
updated: 2026-11-05T17:24:09Z
base: 4fae5ddafa18169c1d3481091b653c4a670f4338
base_tree: c28c00338e6c6c6f74d9ecebcfaff3c6b4337428
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T17:22:58Z
plan0_scope: []
verified: strong
---
# The standing core yes passes self-change gate holds made only of footprint, verb-count or hook-speed rows; a hold that weakens the guard (or a gate that can't run) still needs the user's own yes
## Raw request
> The standing core yes passes self-change gate holds made only of footprint, verb-count or hook-speed rows; a hold that weakens the guard (or a gate that can't run) still needs the user's own yes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a branch held only for footprint, verbs or hook speed merges under the standing core yes, logged; a branch that makes the guard block less still refuses under it — verify with `python3 plugin/tests/run.py test_lanes.SelfChangeGate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: standing yes passes a quality hold, never a guard hold
2. [x] the quality-only pass in selfgate.gate
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.SelfChangeGate` → ✗ exit 1 · Ran 18 tests in 3.8s (18 jobs, 16 at a time; slowest: SelfChangeGate.test_only_the_users_yes_after_the_refusal_passes_never_a_decision 3s, SelfChangeGate.test_the_yes_is_bound_to_the_commit_it_answere [ran] [tree c28c00338e6c] [world 2f1906870a] (2026-11-05T17:23:12Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.SelfChangeGate test_selfgate` → exit 0 · Ran 54 tests in 3.9s (26 jobs, 16 at a time; slowest: SelfChangeGate.test_only_the_users_yes_after_the_refusal_passes_never_a_decision 3s, SelfChangeGate.test_the_yes_is_bound_to_the_commit_it_answere [ran] [tree 7fd5e5da9bf9] [world 2f1906870a] (2026-11-05T17:23:19Z)
- `python3 plugin/tests/run.py test_lanes.SelfChangeGate` → ✗ exit 1 · Ran 18 tests in 13.4s (1 jobs, 16 at a time; slowest: SelfChangeGate 11s) / FAILED (1 classes: test_lanes.SelfChangeGate) (start tree + this task's tests) [ran] [tree de1818c93dd1] [world 2f1906870a] (2026-11-05T17:23:46Z)
- `python3 plugin/tests/run.py test_lanes.SelfChangeGate` → exit 0 · Ran 18 tests in 3.7s (18 jobs, 16 at a time; slowest: SelfChangeGate.test_only_the_users_yes_after_the_refusal_passes_never_a_decision 3s, SelfChangeGate.test_the_yes_is_bound_to_the_commit_it_answere [ran] [tree de1818c93dd1] [world 2f1906870a] (2026-11-05T17:23:46Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.SelfChangeGate` → exit 0 · Ran 18 tests in 3.8s (18 jobs, 16 at a time; slowest: SelfChangeGate.test_only_the_users_yes_after_the_refusal_passes_never_a_decision 3s, SelfChangeGate.test_the_yes_is_bound_to_the_commit_it_answere [ran] [tree b082195c665e] [world 2f1906870a] (2026-11-05T17:24:02Z)
- (audit adversary) `test_lanes.SelfChangeGate + test_selfgate 54 OK, proved red→green; the old test that pinned 'never the standing yes' became two: a quality hold passes under the standing yes (logged self_change_standing_pass), a guard-weakening hold still refuses under it` → the pass needs every refusal row to start with footprint, verbs or hook; a guard row ('guard…', a removed case) or 'couldn't run' keeps the hold, so a branch can't make the guard block less on the standing yes; rows are built by the base's harness (the branch can't rewrite the judge); the standing yes itself is set only through the user's own prompt answer (hooks.py) [tree b082195c665e] (2026-11-05T17:24:02Z)
- (audit intent) `test_lanes.SelfChangeGate + test_selfgate 54 OK, proved red→green; the old test that pinned 'never the standing yes' became two: a quality hold passes under the standing yes (logged self_change_standing_pass), a guard-weakening hold still refuses under it` → the user said stop asking; quality holds (today: new verbs, SessionStart +13%, hook p95 past budget) no longer prompt; the safety part of the gate stays [tree b082195c665e] (2026-11-05T17:24:02Z)
- (audit edge) `test_lanes.SelfChangeGate + test_selfgate 54 OK, proved red→green; the old test that pinned 'never the standing yes' became two: a quality hold passes under the standing yes (logged self_change_standing_pass), a guard-weakening hold still refuses under it` → with no standing core yes the hold stands exactly as before; a mixed hold (quality + guard) refuses [tree b082195c665e] (2026-11-05T17:24:02Z)
- (audit self) `test_lanes.SelfChangeGate + test_selfgate 54 OK, proved red→green; the old test that pinned 'never the standing yes' became two: a quality hold passes under the standing yes (logged self_change_standing_pass), a guard-weakening hold still refuses under it` → no findings [tree b082195c665e] (2026-11-05T17:24:02Z)
## Log
- 2026-11-05T17:22:56Z created
- 2026-11-05T17:22:57Z focused
- 2026-11-05T17:22:58Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T17:24:03Z affected tests waived: the only names that can't match are T-3160's modules (merged and reverted inside this window, not on disk); test_lanes.SelfChangeGate and test_selfgate pass (54 OK)
- 2026-11-05T17:24:05Z done
- 2026-11-05T17:24:09Z committed 2664b1d0 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3091 [FIX M, blocked, 3 steps] Self-change gate holds on T-3034, T-3047 and T-3053: bench each held hook on base and branch at low load, fix a real slowdown in its lan…
- T-2430 [FIX M, done, 2 steps] fm pr train runs the self-change gate on each PR head before merging it — lesson: Every path that merges into main needs the same gates; li…
- decision 2026-11-05: merge speed order: T-3118 (bench only the hook path) first, the biggest cut; then T-3109 (closes yield to a waiting merge), T-3120 (closes reuse a g…
## Lessons
- When the user says stop asking, separate what a gate protects for safety from what it guards for quality, and let a standing yes cover only the second
## Plan gaps
- failed first: step 1 failing tests: standing yes passes a quality hold, never a guard hold
## Files touched
- plugin/lib/sampo/selfgate.py
- CHANGELOG.md
