---
id: T-0805
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/bench_hooks.py, plugin/tests/test_bench_hooks.py]
depends_on: []
source: discovered
created: 2026-10-14T16:37:31Z
updated: 2026-10-14T16:53:09Z
base: e4d735e05d6641e6315c88872908dc346c0d454e
base_tree: e8e1290229c090feaa6f6bab165024b0d057e5e1
verified: strong
---
# The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate
## Raw request
> bench_hooks.py's fixed latency budget fails every hook under machine load (load avg 23 with 3 concurrent fm check runs today: T-0776, T-0781, T-0785 gates), while alone every hook is 30-45 ms of 150: retry once or scale by os.getloadavg/cores before failing
## Interpretation
bench_hooks.py fails when any hook's wall-clock p95 passes its budget. Today three gate runs on one machine (load 23, later 74) put every hook over 150 ms, while alone every hook is 30-45 ms; builders and the main thread each saw a red gate for load. A hook's CPU time (the child's user+sys) doesn't grow with load but does with a real regression (more imports, more work). When load per core is above 1, a hook passes if its CPU-time p95 is within budget, and the table says the machine was busy.
## Assumptions (confidence)
## Acceptance criteria
- [x] with load per core above 1 a hook over budget on wall time but within it on CPU time passes; a hook over on CPU time fails; on a quiet machine wall time decides as before — verify with `cd plugin/tests && python3 -m unittest test_bench_hooks`
## Non-goals
## Approach (options → choice → why)
Options: retry the over-budget hooks (load persists across a retry); skip the bench when busy (hides regressions); judge by CPU time when busy (keeps catching code regressions). Chose CPU time when busy.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for the judging rule
2. [x] CPU time per run and the busy rule in bench_hooks
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_bench_hooks` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 9ccebec302da] (2026-10-14T16:52:11Z)
- (step 2) `python3 plugin/tests/bench_hooks.py --runs 5` → exit 0 · SessionEnd                  73.0   101.5     150  [0] / machine busy (load 2.1 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree 4328fe059698] (2026-10-14T16:52:56Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_bench_hooks` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree 4328fe059698] (2026-10-14T16:52:57Z)
- `cd plugin/tests && python3 -m unittest test_bench_hooks` → exit 0 · Ran 1 test in 0.000s / OK (start tree + this task's tests) [ran] [tree 4328fe059698] (2026-10-14T16:52:58Z)
- `cd plugin/tests && python3 -m unittest test_bench_hooks` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree 4328fe059698] (2026-10-14T16:52:58Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_bench_hooks` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree 4328fe059698] (2026-10-14T16:53:07Z)
- (audit edge) `self: diff read; per run the child's CPU time comes from RUSAGE_CHILDREN deltas; above 1.0 load per core the verdict uses the CPU-time p95, else wall p95 as before; the table says when the machine was busy` → a regression that adds wall time without CPU (a sleep, a slow subprocess wait) is only caught on a quiet machine; such waits are already refused in hooks (T-0426 fg waits) and the quiet runs still judge wall time [tree 4328fe059698] (2026-10-14T16:53:07Z)
- (audit self) `self: diff read; per run the child's CPU time comes from RUSAGE_CHILDREN deltas; above 1.0 load per core the verdict uses the CPU-time p95, else wall p95 as before; the table says when the machine was busy` → no findings [tree 4328fe059698] (2026-10-14T16:53:07Z)
## Log
- 2026-10-14T16:37:31Z created
- 2026-10-14T16:52:03Z planned from capture
- 2026-10-14T16:52:03Z focused
- 2026-10-14T16:53:08Z done
- 2026-10-14T16:53:09Z committed a74febe (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- T-0367 [PERFORMANCE S, done, 1 steps] fm doctor doesn't time hooks on a busy machine: one bench run for exit codes, latency reported as not measured — lesson: A latency …
- decision 2026-09-26: Brainstorm subagents get no tools; the main thread builds one context pack and grounds every idea against the code afterwards
- similar finished tasks took 1–7 steps
## Regression test
test_bench_hooks.Verdict (red before the change: step 1's ✗ run, 'module has no attribute within'). fm task prove can't separate it: the fix lives in plugin/tests/bench_hooks.py, which prove carries over as a test file
## Lessons
- a latency gate on a shared machine needs a load-independent measure, or every concurrent run turns it red
## Plan gaps
- failed first: step 1 Failing test for the judging rule
## Files touched
- plugin/tests/test_bench_hooks.py
- plugin/tests/bench_hooks.py
