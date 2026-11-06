---
id: T-1836
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T10:33:21Z
updated: 2026-10-28T15:47:58Z
base: e0a0c3be8caa53029d086d2c78ee690a0fae940a
base_tree: 82dacab0bff5a6e0410efb8d04dd9f6ef7e2bce9
plan0_at: 2026-10-28T15:45:37Z
plan0_scope: []
verified: strong
---
# Bench_playbooks.py: skip or widen the warm-route CPU limit when the 1-min load is above th
## Raw request
> bench_playbooks.py: skip or widen the warm-route CPU limit when the 1-min load is above the core count/2 (p95 57 ms at load 9 vs 43 ms at load 3)
## Interpretation
The warm-route CPU p95 limit (50 ms) fails under heavy load (57 ms at load 9 vs 43.9 ms at load 3): CPU time inflates under contention too. Widen the limit when the 1-min load per core is above 0.5, like bench_hooks.py's load_per_core.
## Assumptions (confidence)
## Acceptance criteria
- [x] the warm-route CPU limit is 1.5x when load per core is above 0.5, and the result names the load and limit — verify with `python3 plugin/tests/run.py test_playbook_route`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test for route_cpu_limit(load), then the limit in bench_playbooks.py
## Resume here
<!-- auto -->
- 2026-10-28T15:45:38Z step 1/1: red test for route_cpu_limit(load), then the limit in bench_playbooks.py
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_playbook_route 2>&1 | tail -4` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (3.4 s; last 14 of 14 lines) [ran] [tree c88f5718a83c] (2026-10-28T15:47:03Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 20 tests in 2.0s (2 classes, 16 at a time; slowest: Cli 2s, Rank 0s) / OK [ran] [tree f0ed0e563b96] (2026-10-28T15:47:33Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 20 tests in 2.0s (2 classes, 16 at a time; slowest: Cli 2s, Rank 0s) / OK [ran] [tree f0ed0e563b96] (2026-10-28T15:47:55Z)
- (audit intent) `self: read the diff; route_cpu_limit is 50 at load<=0.5/core and 75 above, load_per_core reused from bench_hooks (0.0 on OSError keeps the strict limit), the result and the problem line name load and limit; bench run at 500 books exits 0` → a busy machine (parallel suite) no longer fails the warm-route CPU check, an idle one keeps the 50 ms bar; the result says which bar applied [tree f0ed0e563b96] (2026-10-28T15:47:55Z)
- (audit edge) `self: read the diff; route_cpu_limit is 50 at load<=0.5/core and 75 above, load_per_core reused from bench_hooks (0.0 on OSError keeps the strict limit), the result and the problem line name load and limit; bench run at 500 books exits 0` → getloadavg OSError gives 0.0 so the strict limit holds; boundary 0.5 stays strict (tested 0.5 and 0.51) [tree f0ed0e563b96] (2026-10-28T15:47:55Z)
- (audit self) `self: read the diff; route_cpu_limit is 50 at load<=0.5/core and 75 above, load_per_core reused from bench_hooks (0.0 on OSError keeps the strict limit), the result and the problem line name load and limit; bench run at 500 books exits 0` → no findings [tree f0ed0e563b96] (2026-10-28T15:47:55Z)
## Log
- 2026-10-28T10:33:21Z created
- 2026-10-28T15:45:31Z set tier=S
- 2026-10-28T15:45:36Z focused
- 2026-10-28T15:47:56Z done
- 2026-10-28T15:47:58Z committed 415be9e7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1777 [PERFORMANCE M, done, 2 steps] PreToolUse:Bash:script hook runs at about 90% of its 300 ms budget (p50 271 ms, p95 277 ms — lesson: A latency budget for a time-bo…
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- research T-1518-review: Verdict:** approve with nits. I found nothing in `--repeat` that forges or weakens evidence. The canary has two real weaknesses. I had no shell, …
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar finished tasks took 2–2 steps
## Files touched
- plugin/tests/test_playbook_route.py
- plugin/tests/bench_playbooks.py
