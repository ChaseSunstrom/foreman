---
id: T-0409
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:33:08Z
updated: 2026-10-09T04:35:02Z
base: 3b671a7e5be339671a06550ce77dfc25471eb5e2
base_tree: 5fa7213ec03e669a991975af0c312549ee08ae1f
verified: strong
---
# A 'no active task' refusal should name the queued task to resume (JARVIS edited between closing a lane task and refocusing T-0278; the refusal offered fm task new)
## Raw request
> A 'no active task' refusal should name the queued task to resume (JARVIS edited between closing a lane task and refocusing T-0278; the refusal offered fm task new)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with queued work, the brief refusal names the next task and fm focus ID — verify with `python3 plugin/tests/run.py -k test_brief_refusal_names_the_task_to_resume`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the hook appends it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 04:32 UTC) [ran] [tree 5fa7213ec03e] (2026-10-09T04:33:09Z)
- `python3 plugin/tests/run.py -k test_brief_refusal_names_the_task_to_resume` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: PreToolUse 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree dd71eb680421] (2026-10-09T04:33:29Z)
- `python3 plugin/tests/run.py -k test_brief_refusal_names_the_task_to_resume` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree dd71eb680421] (2026-10-09T04:33:29Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.2    33.6     150  [0] / SessionEnd                  29.3    31.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 942 tests in [ran] [tree 484c23a2ef98] (2026-10-09T04:35:01Z)
- (ac 1) `python3 plugin/tests/run.py -k test_brief_refusal_names_the_task_to_resume` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 484c23a2ef98] (2026-10-09T04:35:02Z)
- (audit intent) `self: message text on a brief refusal only; refusal latency measured (p95 38.5 ms)` → the refusal names fm focus <next queued> (test) [tree 484c23a2ef98] (2026-10-09T04:35:02Z)
- (audit edge) `self: message text on a brief refusal only; refusal latency measured (p95 38.5 ms)` → an empty queue adds nothing; a broken queue read is caught, the plain refusal stands [tree 484c23a2ef98] (2026-10-09T04:35:02Z)
- (audit operator) `self: message text on a brief refusal only; refusal latency measured (p95 38.5 ms)` → the extra read runs only on a refusal [tree 484c23a2ef98] (2026-10-09T04:35:02Z)
- (audit self) `self: message text on a brief refusal only; refusal latency measured (p95 38.5 ms)` → no findings [tree 484c23a2ef98] (2026-10-09T04:35:02Z)
## Log
- 2026-10-09T04:33:08Z created
- 2026-10-09T04:33:08Z focused
- 2026-10-09T04:35:02Z done
- 2026-10-09T04:35:02Z committed 9ed87a7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- T-0402 [FIX S, done, 2 steps] Foreman 1.2.9: the drive offers queued work during background jobs (T-0401) to GitHub main and JARVIS
- T-0134 [FEATURE L, done, 5 steps] Lanes: a git worktree is a lane of its project with its own active task — lesson: When a 'single X per project' rule becomes 'per lane'…
- decision 2026-10-03: T-0110 (one yes for several queued core tasks) closed as done in T-0119: the standing core yes covers every task; plugin and remote stay per-task by…
- similar finished tasks took 2–5 steps
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
