---
id: T-1106
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, plugin/tests/test_outcomes.py]
depends_on: []
source: discovered
created: 2026-10-16T05:04:24Z
updated: 2026-10-16T07:09:30Z
base: f4af16c318f0d59a74a093682d834e972a2d0993
base_tree: 347cabb507f6ce87f08db7fc0de79b4ae8a63da5
verified: strong
---
# - `fmtidy.unblocked` (fmtidy.py:118) has the same lane and fresh-clone mtime false positiv
## Raw request
> - `fmtidy.unblocked` (fmtidy.py:118) has the same lane and fresh-clone mtime false positive as finding 1. It needs its own task
> (noticed by an agent; research T-1077-review)
## Interpretation
fmtidy.unblocked says a blocked task may be worth retrying when a file its block reason names changed since the block, judged by the file's mtime. A fresh clone or a builder's worktree gives every file a new mtime, so every such blocked task reads 'changed'. Judge by git, as T-1077's stale-plan sweep does: a commit touching the file after the block, or uncommitted changes to it (mtime then counts, since a real edit made it dirty).
## Assumptions (confidence)
## Acceptance criteria
- [x] In a fresh clone a blocked task naming an unchanged file is not flagged; a commit to that file after the block flags it — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test with a clone, then judge by git
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 32 tests in 7.5s (13 classes, 16 at a time; slowest: StalePlans 7s, Apply 6s, DeferredTriage 6s) / FAILED (1 classes) [ran] [tree 127314270bba] (2026-10-16T07:05:52Z)
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 32 tests in 3.0s (13 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 3s, Apply 3s) / FAILED (1 classes) [ran] [tree 5e0194f5d2a9] (2026-10-16T07:06:17Z)
- (step 1) `python3 plugin/tests/run.py test_tidy test_outcomes` → exit 0 · Ran 46 tests in 18.2s (21 classes, 16 at a time; slowest: Survival 18s, StalePlans 4s, DeferredTriage 3s) / OK [ran] [tree 01cffb1e4a85] (2026-10-16T07:06:49Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 32 tests in 6.0s (13 classes, 16 at a time; slowest: StalePlans 6s, DeferredTriage 5s, Apply 5s) / OK [ran] [tree 340fae867eb9] (2026-10-16T07:07:37Z)
- `python3 plugin/tests/run.py test_tidy test_outcomes` → exit 0 · Ran 46 tests in 34.1s (21 classes, 16 at a time; slowest: Survival 34s, StalePlans 7s, Apply 6s) / OK [ran] [tree 340fae867eb9] (2026-10-16T07:07:37Z)
- (audit self) `self: fresh-mtime case (no flag) and committed change (flag) tested; the existing Reopen test now uses a real commit; no-git projects keep the mtime rule` → no findings [tree 340fae867eb9] (2026-10-16T07:07:37Z)
## Log
- 2026-10-16T05:04:24Z created
- 2026-10-16T07:05:25Z set type=FIX, tier=S, scope=['plugin/lib/fmtidy.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T07:05:27Z focused
- 2026-10-16T07:06:31Z set scope=['plugin/lib/fmtidy.py', 'plugin/tests/test_tidy.py', 'plugin/tests/test_outcomes.py']
- 2026-10-16T07:06:56Z scope: CHANGELOG.md — release note
- 2026-10-16T07:09:26Z done
- 2026-10-16T07:09:30Z committed 649ef78 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- research T-1077-review: Verdict: approve with nits** (one MEDIUM to fix before merge). [stale: plugin/lib/fmtidy.py changed since it was written]
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmtidy.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Lessons
- mtime says when a file was written, not when it changed: anything that copies a tree resets it
## Plan gaps
- failed first: step 1 Failing test with a clone, then judge by git
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- plugin/tests/test_outcomes.py
- CHANGELOG.md
