---
id: T-2870
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T02:11:34Z
updated: 2026-11-04T02:14:45Z
base: 5570d538424bb1a7bf35317ad629dbbc1b099429
base_tree: 8115e58c8ef1a04850ef649d4a2d671ad56673eb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T02:12:17Z
plan0_scope: []
verified: strong
---
# Sampo lease drop run from a builder lane drops every lease the session holds (16 at once…
## Raw request
> FIX: sampo lease drop run from a builder lane drops every lease the session holds (16 at once in T-2868, the main thread's T-2861 and T-2866 included) because lanes share the parent's session id; it must drop only the lane's own task's leases
## Interpretation
Reading 1 (chosen): a bare lease drop with no active task (a builder between steps, or the main thread idle) matched every lease the session holds, and builder lanes share the main session's id, so T-2868's builder dropped 16 leases including the main thread's T-2861 and T-2866. With no active task, a bare drop frees only leases with no task or a closed one, never another open task's. Reading 2 (ruled out): give each lane its own session id; that would break every T-1216/T-1416/T-1588 rule that reads the shared id.
## Assumptions (confidence)
## Acceptance criteria
- [x] with no active task, a bare lease drop keeps every open task's leases and frees a closed task's — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then mine() with no active task matches only task-less or closed-task leases
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 21 tests in 10.4s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 4s, Stop 3s) / FAILED (1 classes: test_claims.Claims) (start tree + this task's tests) [ran] [tree b8133fcc05cd] [world 2f1906870a] (2026-11-04T02:12:45Z)
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 21 tests in 9.0s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 4s, Stop 3s) / FAILED (1 classes: test_claims.Claims) [ran] [tree b8133fcc05cd] [world 2f1906870a] (2026-11-04T02:12:45Z)
- (step 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 21 tests in 9.8s (3 classes, 16 at a time; slowest: Claims 10s, ClaimsReview 4s, Stop 3s) / OK [ran] [tree 972b1ddda90f] [world 2f1906870a] (2026-11-04T02:14:00Z)
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 21 tests in 10.1s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 4s, Stop 3s) / FAILED (1 classes: test_claims.Claims) (start tree + this task's tests) [ran] [tree 972b1ddda90f] [world 2f1906870a] (2026-11-04T02:14:20Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 21 tests in 9.1s (3 classes, 16 at a time; slowest: Claims 9s, ClaimsReview 4s, Stop 3s) / OK [ran] [tree 972b1ddda90f] [world 2f1906870a] (2026-11-04T02:14:20Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T02:14:20Z [ran] [tree 972b1ddda90f] [world 2f1906870a] (2026-11-04T02:14:20Z)
- (audit edge) `self-review: with an active task, unchanged (its own and task-less leases); with none, a bare or file-named drop matches only task-less leases and those of closed tasks, so a builder between steps or an idle main thread can't free another open task's leases` → an open-but-blocked task keeps its lease until it closes; its close or merge releases it (bus.release) [tree 972b1ddda90f] (2026-11-04T02:14:20Z)
- (audit adversary) `self-review: with an active task, unchanged (its own and task-less leases); with none, a bare or file-named drop matches only task-less leases and those of closed tasks, so a builder between steps or an idle main thread can't free another open task's leases` → a narrower match only; nothing new is released [tree 972b1ddda90f] (2026-11-04T02:14:20Z)
- (audit self) `self-review: with an active task, unchanged (its own and task-less leases); with none, a bare or file-named drop matches only task-less leases and those of closed tasks, so a builder between steps or an idle main thread can't free another open task's leases` → no findings [tree 972b1ddda90f] (2026-11-04T02:14:20Z)
## Log
- 2026-11-04T02:11:34Z created
- 2026-11-04T02:12:16Z set tier=S
- 2026-11-04T02:12:16Z planned: it has criteria and steps
- 2026-11-04T02:12:17Z focused
- 2026-11-04T02:12:17Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T02:14:44Z done
- 2026-11-04T02:14:45Z committed b59945b0 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1216 [FIX S, done, 2 steps] fm lease drop releases only the current task's leases, and a file's drop releases all its symbols
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar finished tasks took 1–3 steps
## Why not caught
T-1216 scoped drops to the active task, but with none active the old match-everything path stayed
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/sampo/bus.py
