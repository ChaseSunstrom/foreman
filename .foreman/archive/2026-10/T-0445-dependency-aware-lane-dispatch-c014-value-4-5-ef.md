---
id: T-0445
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:43:40Z
base: e323c688e49ee6ba60d94bcdf207517349791a17
base_tree: 8baf7c62a751ee98fb5ec85fb2b0bd5de2f43030
verified: strong
---
# Lane dispatch respects relate groups and co-change footprints
## Raw request
> FEATURE: Dependency-aware lane dispatch (C014, value 4/5, effort M, risk low)
>   first version: Make --parallel pick lanes from the fm relate graph plus a predicted file footprint (scope plus fm impact/co-change), and have drive offer the same set; skip solver/cost-prediction extras.
>   what it is: Dispatch the queue as a dependency graph across builder lanes, scheduled by predicted cost, risk and file footprint, with a durable scheduler.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
fm run --parallel batches tasks by explicit scope overlap and c._deps; it ignores fm relate's groups and misses files that change together. Tasks in one relate group never share a batch, and a task's footprint is its scope plus fm map's co-change companions, so overlap is computed on what will really change.
## Assumptions (confidence)
## Acceptance criteria
- [x] tasks in one relate group don't share a batch — verify with `python3 plugin/tests/run.py -k test_same_group_never_batches`
- [x] a scope whose co-change companion is in another task's scope doesn't batch with it — verify with `python3 plugin/tests/run.py -k test_cochange_footprint_blocks_batch`
## Non-goals
## Approach (options → choice → why)
(B, chosen) group exclusion + _footprint(b, pairs) from fmmap's co-change pairs, falling back to scope when the map is missing. (A) group only. (C, rejected) a solver. Over-serializing is safe.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first in test_parallel.py
2. [x] group check + _footprint in fmserve._batch
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_same_group_never_batches -k test_cochange_footprint_blocks_batch` → ✗ exit 1 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Parallel 1s) / FAILED (1 classes) [ran] [tree 4f0de119c24e] (2026-10-09T14:43:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_same_group_never_batches -k test_cochange_footprint_blocks_batch` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Parallel 1s) / OK [ran] [tree 8d64955bbcc4] (2026-10-09T14:43:13Z)
- (ac 1) `python3 plugin/tests/run.py -k test_same_group_never_batches` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Parallel 1s) / OK [ran] [tree c1a1727ae444] (2026-10-09T14:43:39Z)
- (ac 2) `python3 plugin/tests/run.py -k test_cochange_footprint_blocks_batch` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Parallel 1s) / OK [ran] [tree c1a1727ae444] (2026-10-09T14:43:39Z)
- (audit edge) `self: group exclusion + _footprint over fm map's co-change pairs, falling back to scopes; red→green; parallel + serve suites OK` → no map or a map error → no widening; pairs are keyed by exact files, so only literal scopes widen; over-serializing is the safe failure [tree c1a1727ae444] (2026-10-09T14:43:39Z)
- (audit intent) `self: group exclusion + _footprint over fm map's co-change pairs, falling back to scopes; red→green; parallel + serve suites OK` → lane dispatch now respects relate groups and co-change footprints [tree c1a1727ae444] (2026-10-09T14:43:39Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:38:30Z planned from capture
- 2026-10-09T14:42:41Z focused
- 2026-10-09T14:43:39Z done
- 2026-10-09T14:43:40Z committed 2953644 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0515 [FEATURE M, dropped, 0 steps] Dependency-aware lane dispatch (C014, value 4/5, effort M, risk low)
- T-0535 [FEATURE M, dropped, 0 steps] Lane isolation and host health (C017, value 3/5, effort S, risk low)
- T-0521 [FEATURE M, dropped, 0 steps] Estimates, pace and time budgets (C051, value 4/5, effort M, risk low)
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- Scopes say where a task means to write; history says where it will.
## Files touched
- plugin/tests/test_parallel.py
- plugin/lib/fmserve.py
- CHANGELOG.md
