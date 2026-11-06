---
id: T-1835
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T10:12:58Z
updated: 2026-10-28T15:54:51Z
base: 52ba8c8feccad48c24aa12c5df3ce0f7daedc3a8
base_tree: 860f7ab983ec7ff9df9198f6945d4d6805402519
plan0_at: 2026-10-28T15:53:12Z
plan0_scope: []
verified: strong
---
# Fm which ranks playbooks by reading every header; at 10k+ books call fmplaybooks.find (FTS
## Raw request
> fm which ranks playbooks by reading every header; at 10k+ books call fmplaybooks.find (FTS5) instead so there is one ranker (from T-1833 review)
## Interpretation
fm which reads every playbook header to rank them. Past BIG (2000) books, take its playbook rows from fmplaybooks.find's FTS5 top hits for the task instead, so a large library costs one index query and route and which agree on candidates.
## Assumptions (confidence)
## Acceptance criteria
- [x] past BIG books fm which reads only the headers find() returns — verify with `python3 plugin/tests/run.py test_which`
## Non-goals
## Approach (options → choice → why)
Options: (1) above BIG, read only find()'s top 4xSHOWN headers, rank as today; (2) always use find for playbooks and drop the header ranker (changes today's 80-book results, which tests pin); (3) skip, no real library is that big. Choice: 1, small and leaves today's ranking unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_which, then the BIG branch in fmwhich.playbooks
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 13 tests in 1.6s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / OK [ran] [tree 68f1b355bd9e] (2026-10-28T15:54:11Z)
- (ac 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 13 tests in 1.6s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / OK [ran] [tree 68f1b355bd9e] (2026-10-28T15:54:48Z)
- (audit intent) `self: playbooks(task) reads only find()'s top 20 when the library passes BIG=2000, else every header as before (today's ~80-book results unchanged, test_which green); find gets ROOT explicitly since its default binds at import` → a 10k+ library costs one FTS5 query plus 20 header reads in fm which, and route and which share the candidate ranker [tree 68f1b355bd9e] (2026-10-28T15:54:48Z)
- (audit edge) `self: playbooks(task) reads only find()'s top 20 when the library passes BIG=2000, else every header as before (today's ~80-book results unchanged, test_which green); find gets ROOT explicitly since its default binds at import` → a task with no index terms gives find() [] so no playbooks are listed, the same as no fit; no task (other callers) keeps the full read [tree 68f1b355bd9e] (2026-10-28T15:54:48Z)
- (audit self) `self: playbooks(task) reads only find()'s top 20 when the library passes BIG=2000, else every header as before (today's ~80-book results unchanged, test_which green); find gets ROOT explicitly since its default binds at import` → no findings [tree 68f1b355bd9e] (2026-10-28T15:54:48Z)
## Log
- 2026-10-28T10:12:58Z created
- 2026-10-28T15:53:07Z set tier=S
- 2026-10-28T15:53:11Z focused
- 2026-10-28T15:54:49Z done
- 2026-10-28T15:54:51Z committed cd12a7d5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1833 [FEATURE M, done, 3 steps] fm playbooks route TEXT|--task ID: top playbooks by relevance over an incremental FTS5 index, fast at 20k (part of T-1803) — lesson: Tw…
- T-1803 [FEATURE L, done, 3 steps] Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk — lesson: A regex that reads a command's arg…
- playbook SQL: query review, indexes and plans (fm playbooks show fix/sql)
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–3 steps
## Files touched
- plugin/tests/test_which.py
- plugin/lib/fmwhich.py
