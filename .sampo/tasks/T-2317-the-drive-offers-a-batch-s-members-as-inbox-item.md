---
id: T-2317
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T10:57:32Z
updated: 2026-10-31T11:06:39Z
base: 9866470356a0e3d7a8527cb4417227cac7749f24
base_tree: 7db7647415c313b073b13aeb4c48d4796b285fc1
plan0_at: 2026-10-31T11:01:28Z
plan0_scope: []
verified: strong
---
# A batch host held by a builder lane keeps its members out of the main inbox
## Raw request
> The drive offers a batch's members as inbox items to plan (T-2313 after fm batch made T-2316 and a builder took it): fm next/the Stop drive should skip tasks that are members of an open batch (fm batch records them), or fm batch should mark members as held by the batch
## Interpretation
state_dict builds the inbox from lane_view(everything, lane), which hides tasks held by another lane; once a builder took batch host T-2316, its members' batched() check no longer found the host and T-2313..2315 came back as inbox items the drive offered.
## Assumptions (confidence)
## Acceptance criteria
- [x] With a batch host held by another lane, state's inbox and fm next show none of its members — verify with `python3 plugin/tests/run.py test_batch`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: batch three, mark the host held by another lane, state's inbox holds no member; then lane_view also drops members whose open host is held elsewhere
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_batch -k held_by_a_lane` → ✗ exit 1 · Ran 1 tests in 4.5s (1 classes, 16 at a time; slowest: Batch 3s) / FAILED (1 classes) [ran] [tree b958b600c058] (2026-10-31T11:01:51Z)
- `python3 plugin/tests/run.py test_batch -k held_by_a_lane` → ✗ exit 1 · Ran 1 tests in 10.2s (1 classes, 16 at a time; slowest: Batch 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 10cc99e93aac] (2026-10-31T11:02:49Z)
- `python3 plugin/tests/run.py test_batch -k held_by_a_lane` → exit 0 · Ran 1 tests in 5.2s (1 classes, 16 at a time; slowest: Batch 4s) / OK [ran] [tree 10cc99e93aac] (2026-10-31T11:02:49Z)
- (step 1) `python3 plugin/tests/run.py test_batch test_lanes test_core` → exit 0 · Ran 180 tests in 136.9s (36 classes, 16 at a time; slowest: Lanes 135s, BatchEdit 71s, Batch 45s) / OK [ran] [tree 10cc99e93aac] (2026-10-31T11:05:08Z)
- (ac 1) `python3 plugin/tests/run.py test_batch` → exit 0 · Ran 37 tests in 39.1s (7 classes, 16 at a time; slowest: BatchEdit 37s, Batch 29s, Related 14s) / OK [ran] [tree 966fe9bb4f35] (2026-10-31T11:06:12Z)
- (audit intent) `self-review: lane_view now drops a member whose batched_in host is held elsewhere and still open (batched); members of a closed host come back as before; one place serves state_dict, fm next and every lane-view caller` → once a builder takes a batch host, its members stay out of the main inbox and the drive stops offering them [tree 966fe9bb4f35] (2026-10-31T11:06:12Z)
- (audit edge) `self-review: lane_view now drops a member whose batched_in host is held elsewhere and still open (batched); members of a closed host come back as before; one place serves state_dict, fm next and every lane-view caller` → a host that's done or dropped releases its members (batched() is false); a member whose host is in this lane stays visible as before [tree 966fe9bb4f35] (2026-10-31T11:06:12Z)
- (audit self) `self-review: lane_view now drops a member whose batched_in host is held elsewhere and still open (batched); members of a closed host come back as before; one place serves state_dict, fm next and every lane-view caller` → no findings [tree 966fe9bb4f35] (2026-10-31T11:06:12Z)
## Log
- 2026-10-31T10:57:32Z created
- 2026-10-31T10:59:04Z note: rank_inbox already skips batched members (fmcore.batched via batched_in) and T-2313 carries batched_in: T-2316, so the offer may have come from a stale state view at the Stop hook; reproduce (batch, then stop) before changing anything
- 2026-10-31T11:01:18Z planned from capture
- 2026-10-31T11:01:23Z focused
- 2026-10-31T11:05:23Z scope: plugin/lib/fmcore.py (lane_view), plugin/tests/test_batch.py, CHANGELOG.md
- 2026-10-31T11:06:37Z done
- 2026-10-31T11:06:39Z committed b67d45dc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- research T-2123-review: Verdict: changes needed (2 HIGH, 6 MEDIUM, 5 LOW); fixed or skipped with reason. Reviewer: one foreman:fm-reviewer, five lenses, read-only.
- decision 2026-10-23: Pause the feature backlog (112 FEATURE items: 77 M, 34 S, 1 L) until weekly usage is back on pace; every FIX, SECURITY, PERFORMANCE and CLEAN item i…
## Why not caught
test_batch checked members leave the inbox only with the host in the main checkout; no test held the host in a lane, the normal case once a builder takes it
## Lessons
- A filter that looks things up by id must look in the full set: a lane view hid the host its members were checked against
## Plan gaps
- failed first: step 1 Red test: batch three, mark the host held by another lane, state's inbox holds no member; then lane…
## Files touched
- plugin/tests/test_batch.py
- plugin/lib/fmcore.py
- CHANGELOG.md
