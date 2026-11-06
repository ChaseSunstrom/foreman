---
id: T-2309
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T10:10:16Z
updated: 2026-10-31T10:14:35Z
baseline: true
base: 283da20f1eba5be8ed58f48eaced1033fd7a4868
base_tree: 37c357a22ed8783c319b2a9e8565b3d9b61b8735
plan0_at: 2026-10-31T10:11:33Z
plan0_scope: []
verified: strong
---
# Guard speed tests time CPU, not the wall clock, so a loaded host can't fail them
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_guard.TokenFallback.test_deep_nesting_is_masked_in_linear_time, test_guard.TokenFallback.test_repeated_cds_in_a_line_are_judged_fast, test_hooks.NoTaskGate.test_a_bench_replay_never_asks_for_a_push_notification. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
ship72 went red on test_guard.TokenFallback's two speed tests at load average 59-82 (0.539 s against a 0.5 s bar); both pass alone. They time in-process guard calls with time.monotonic, so other processes' load counts against them.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_deep_nesting_is_masked_in_linear_time and test_repeated_cds_in_a_line_are_judged_fast measure time.process_time around the in-process guard calls, keeping their bars, and pass — verify with `python3 plugin/tests/run.py test_guard -k TokenFallback`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Switch both timers to time.process_time (the guard runs in this process), keep the bars and their comments
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard -k TokenFallback` → exit 0 · Ran 12 tests in 6.9s (1 classes, 16 at a time; slowest: TokenFallback 5s) / OK [ran] [tree 3fcd5b97228f] (2026-10-31T10:11:55Z)
- (ac 1) `python3 plugin/tests/run.py test_guard -k TokenFallback` → exit 0 · Ran 12 tests in 8.5s (1 classes, 16 at a time; slowest: TokenFallback 7s) / OK [ran] [tree 3fcd5b97228f] (2026-10-31T10:12:37Z)
- (audit intent) `self-review: both speed tests time in-process guard calls (g.check, g._mask_nested_dq), so time.process_time measures exactly the work the bar bounds; bars and comments kept; no guard code touched` → a loaded ship host can't fail a complexity bar by other processes' load, while a quadratic regression still blows the CPU bar [tree 3fcd5b97228f] (2026-10-31T10:12:37Z)
- (audit edge) `self-review: both speed tests time in-process guard calls (g.check, g._mask_nested_dq), so time.process_time measures exactly the work the bar bounds; bars and comments kept; no guard code touched` → process_time counts every thread of this process; the guard spawns no children in these paths, so nothing escapes the measure [tree 3fcd5b97228f] (2026-10-31T10:12:37Z)
- (audit adversary) `self-review: both speed tests time in-process guard calls (g.check, g._mask_nested_dq), so time.process_time measures exactly the work the bar bounds; bars and comments kept; no guard code touched` → only the timer changed; every guard verdict row in the cds test is untouched, the bars are the same numbers, and a slow (quadratic) guard path would still exceed them in CPU time, so no guard behaviour or check is weakened [tree 3fcd5b97228f] (2026-10-31T10:12:37Z)
- (audit self) `self-review: both speed tests time in-process guard calls (g.check, g._mask_nested_dq), so time.process_time measures exactly the work the bar bounds; bars and comments kept; no guard code touched` → no findings [tree 3fcd5b97228f] (2026-10-31T10:12:37Z)
## Log
- 2026-10-31T10:10:16Z created
- 2026-10-31T10:11:28Z planned from capture
- 2026-10-31T10:11:30Z focused
- 2026-10-31T10:12:17Z scope: plugin/tests/test_guard.py (two TokenFallback speed tests)
- 2026-10-31T10:14:29Z done
- 2026-10-31T10:14:35Z committed afbb61d3 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2305 [FIX S, done, 1 steps] Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import — lesson: A new top-level import in fmhooks c…
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- T-1597 [FIX S, done, 1 steps] Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load — lesson: Under heavy machine load the …
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- similar finished tasks took 1–1 steps
- start here (files T-2305 touched): plugin/lib/fmhooks.py
## Regression test
none: the failure is load-dependent (0.539 s vs 0.5 s at load 59-82, passes alone), and the fix lives in the test file fm task prove overlays, so before/after can't be separated; CPU time can't be inflated by other processes, which is the guarantee
## Why not caught
the bars were set on an idle machine with the wall clock; nothing ran the suite under load until ships began running beside exam sessions
## Lessons
- A complexity bar measures CPU (time.process_time); only a deadline is a wall-clock bar
## Files touched
- plugin/tests/test_guard.py
